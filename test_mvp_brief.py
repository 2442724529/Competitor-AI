"""Offline contract regressions, including fail-closed input and output handling."""

from contextlib import redirect_stdout
from copy import deepcopy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from v3 import mvp_brief as m


def candidate(selection):
    cells = []
    for d in m.DIMENSIONS:
        for p in m.PRODUCTS:
            es = [
                e
                for e in selection["entries"]
                if e["product"] == p and d in e["dimensions"]
            ]
            cells.append(
                dict(
                    product=p,
                    dimension=d,
                    statement=(
                        dict(
                            text=" ".join(e["evidence"]["claim"] for e in es),
                            fact_ids=[e["fact_id"] for e in es],
                        )
                        if es
                        else None
                    ),
                )
            )
    return dict(
        cells=cells,
        observations=[
            dict(
                text="Slides 支持直接编辑和对话修改；Claude Free 的已选证据只明确文件创建及代码执行，不能据此比较编辑质量。",
                fact_ids=["F99", "F60"],
            ),
            dict(
                text="Projects 组织聊天与文档，Gemini skills 复用指令；两类机制不能直接等同于同一成果的实时协作。",
                fact_ids=["F68", "F92"],
            ),
        ],
        hypothesis="可以尝试将可编辑成果、授权执行和可复用任务模板组织在同一工作界面；需用户研究与实测验证，不能当作竞品已具备的能力。",
    )


class MVPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # A real offline integration check; absence/corruption fails rather than skips.
        cls.selection = m.load_selection()

    def setUp(self):
        self.draft = candidate(self.selection)

    def test_local_pass_is_not_semantic_or_original_v3_pass(self):
        result = m.evaluate(self.draft, self.selection)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["semantic_review"], "PENDING")
        self.assertEqual(result["original_v3_status"], "NOT_EVALUATED")
        self.assertEqual(result["model_calls"], 0)
        self.assertIn("证据不足", result["body"])
        self.assertIn("产品设计假设（未验证）", result["body"])
        self.assertEqual(len(result["sources"]), 12)
        self.assertTrue(all(s["confidence"] == "High" for s in result["sources"]))

    def test_bad_shapes_ids_scope_and_injection_fail(self):
        variants = [None, {}, dict(self.draft, status="PASS")]
        for field, value in [
            ("observations", []),
            ("hypothesis", ""),
            ("hypothesis", "[F999]"),
            ("hypothesis", "x\n| forged |"),
        ]:
            variants.append(dict(self.draft, **{field: value}))
        for ids in [[], ["F999"], ["F63"], ["F98", "F98"], ["F0"], [None]]:
            x = deepcopy(self.draft)
            x["cells"][0]["statement"]["fact_ids"] = ids
            variants.append(x)
        for x in variants:
            with self.subTest(candidate=x):
                self.assertEqual(m.evaluate(x, self.selection)["status"], "FAIL")

    def test_missing_duplicate_and_filled_gap_cells_fail(self):
        for mode in ["missing", "duplicate", "fill_gap"]:
            x = deepcopy(self.draft)
            if mode == "missing":
                x["cells"].pop()
            elif mode == "duplicate":
                x["cells"][1] = x["cells"][0]
            else:
                x["cells"][3]["statement"] = dict(text="可执行任务", fact_ids=["F98"])
            self.assertEqual(m.evaluate(x, self.selection)["status"], "FAIL")

    def test_character_boundaries_and_target_warning(self):
        self.draft["hypothesis"] = "假设"
        base = len(m.render_brief(self.draft, self.selection)) - 2
        # Compact fixture so both target boundaries can be checked independently.
        for c in self.draft["cells"]:
            if c["statement"]:
                c["statement"]["text"] = "冻结能力描述"
        base = len(m.render_brief(self.draft, self.selection)) - 2
        for size in [1499, 1500, 2500, 2501, 5000, 5001]:
            self.draft["hypothesis"] = "假" * (size - base)
            r = m.evaluate(self.draft, self.selection)
            self.assertEqual(r["status"], "FAIL" if size > 5000 else "PASS")
            if size <= 5000:
                self.assertEqual(r["body_characters"], size)
                self.assertEqual(
                    r["length_target"],
                    "MET" if 1500 <= size <= 2500 else "OUTSIDE_TARGET",
                )

    def test_standard_table_and_surrounding_blank_lines_pass(self):
        body = m.render_brief(self.draft, self.selection)
        m.check_markdown_table("\n\n" + body + "\n\n")
        self.assertEqual(m.evaluate(self.draft, self.selection)["table_format"], "PASS")

    def assert_broken_table_rejected(self, after_row):
        lines = m.render_brief(self.draft, self.selection).splitlines()
        rows = [i for i, line in enumerate(lines) if line.startswith("|")]
        lines.insert(rows[after_row] + 1, "")
        broken = "\n".join(lines)
        with self.assertRaisesRegex(ValueError, "contiguous"):
            m.check_markdown_table(broken)
        # Even a regressed renderer must not turn invalid output into PASS.
        with patch.object(m, "render_brief", return_value=broken):
            self.assertEqual(m.evaluate(self.draft, self.selection)["status"], "FAIL")

    def test_blank_between_header_and_separator_fails(self):
        self.assert_broken_table_rejected(0)

    def test_blank_between_separator_and_first_data_fails(self):
        self.assert_broken_table_rejected(1)

    def test_blank_between_data_rows_fails(self):
        for row in (2, 3):
            with self.subTest(row=row):
                self.assert_broken_table_rejected(row)

    def test_malformed_table_shape_fails(self):
        body = m.render_brief(self.draft, self.selection)
        for broken in (
            body.replace("| --- | --- | --- | --- |", "| -- | --- | --- | --- |"),
            body.replace(
                "| 比较维度 | ChatGPT | Claude | Gemini |",
                "| 比较维度 | Claude | ChatGPT | Gemini |",
            ),
            body.replace("| --- | --- | --- | --- |", "| --- | --- | --- |"),
        ):
            with self.assertRaises(ValueError):
                m.check_markdown_table(broken)

    def test_input_tampering_and_coverage_fail_closed(self):
        changes = [
            lambda s: s["entries"][0].update(fact_id="F999"),
            lambda s: s["entries"].append(s["entries"][0]),
            lambda s: s["entries"][0]["evidence"].update(claim="changed"),
            lambda s: s.update(input_hashes={}),
            lambda s: s.update(
                entries=[e for e in s["entries"] if e["product"] == "Claude"]
            ),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "selection.json"
            for change in changes:
                s = deepcopy(self.selection)
                change(s)
                p.write_text(json.dumps(s), encoding="utf-8")
                with self.assertRaises(ValueError):
                    m.load_selection(path=p)

    def test_cli_no_model_and_errors_never_pass(self):
        with (
            patch(
                "v3.frozen_downstream.model_client",
                side_effect=AssertionError("No model"),
            ),
            patch("v3.report.assemble", side_effect=AssertionError("No full report")),
            patch(
                "v3.report.validate", side_effect=AssertionError("No full validator")
            ),
        ):
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(m.main([]), 0)
            self.assertEqual(json.loads(out.getvalue())["status"], "INPUT_READY")
            with tempfile.TemporaryDirectory() as tmp:
                p = Path(tmp) / "candidate.json"
                for raw in ["{", "{}", json.dumps(candidate(self.selection))]:
                    p.write_text(raw, encoding="utf-8")
                    out = io.StringIO()
                    with redirect_stdout(out):
                        code = m.main(["--candidate", str(p)])
                    result = json.loads(out.getvalue())
                    self.assertEqual(code, 0 if raw.startswith('{"cells"') else 1)
                    self.assertEqual(result["status"], "PASS" if code == 0 else "FAIL")
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(m.main(["--input", "/nonexistent-mvp-input"]), 1)
            self.assertEqual(json.loads(out.getvalue())["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()

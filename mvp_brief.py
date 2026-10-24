"""Offline narrow brief contract. No provider, full-report validator or repair loop."""

import argparse
import json
from pathlib import Path
import re

from v3.frozen_downstream import DEFAULT_INPUT, read_inputs, require

SELECTION = Path(__file__).with_name("mvp_selection.json")
PRODUCTS = ("ChatGPT", "Claude", "Gemini")
DIMENSIONS = ("工作成果创建与编辑", "工具连接与任务执行", "复用与协作机制")
SCOPE = "仅限冻结证据的历史能力描述；非当前最新信息，不作性能、价格或优劣排名。"


def evidence_record(fact):
    return {
        k: fact[k]
        for k in (
            "fact_id",
            "competitor",
            "claim",
            "confidence",
            "research_scope",
            "limitation",
            "event_date",
            "checked_date",
            "validated_source_ids",
        )
    } | {
        "sources": [
            s
            for s in fact["supports"]
            if s["source_id"] in fact["validated_source_ids"]
        ]
    }


def load_selection(directory=DEFAULT_INPUT, path=SELECTION):
    facts, _, _, hashes, _ = read_inputs(directory)
    selection = json.loads(path.read_text(encoding="utf-8"))
    # Pin captured bytes as well as read_inputs' saved relationships.
    actual = {
        str(Path(p).relative_to(directory.resolve().parent)): h
        for p, h in hashes.items()
    }
    require(actual == selection["input_hashes"], "MVP frozen input hash mismatch")
    entries = selection["entries"]
    require(0 < len(entries) <= 18, "Selection must contain 1..18 facts")
    require(
        len({e["fact_id"] for e in entries}) == len(entries), "Duplicate selection ID"
    )
    by_id = {f["fact_id"]: f for f in facts}
    for e in entries:
        require(e["fact_id"] in by_id, "Unknown or unverified selection ID")
        require(
            e["evidence"] == evidence_record(by_id[e["fact_id"]]),
            "Evidence snapshot differs",
        )
        require(e["product"] == e["evidence"]["competitor"], "Product mismatch")
        require(
            bool(e["dimensions"]) and set(e["dimensions"]) <= set(DIMENSIONS),
            "Bad dimension",
        )
        require(
            bool(e["reason"].strip()) and bool(e["scope_limit"].strip()),
            "Selection explanation missing",
        )
    for d in DIMENSIONS:
        require(
            len({e["product"] for e in entries if d in e["dimensions"]}) >= 2,
            "Insufficient two-product coverage: " + d,
        )
    return selection


def text_field(value):
    require(isinstance(value, str) and bool(value.strip()), "Empty text")
    require(
        not re.search(r"[\n\r|<>]|```|https?://|\bF\d+\b", value),
        "Text must be plain; citations and sources are program-owned",
    )
    return value


def check_markdown_table(body):
    """Validate the MVP's one contiguous, four-column Markdown table."""
    require(isinstance(body, str), "Body must be text")
    lines = body.splitlines()
    positions = [i for i, line in enumerate(lines) if line.lstrip().startswith("|")]
    require(len(positions) == 5, "Table requires header, separator and three data rows")
    require(
        positions == list(range(positions[0], positions[0] + 5)),
        "Table rows must be contiguous; blank lines inside table are forbidden",
    )
    rows = []
    for i in positions:
        line = lines[i].strip()
        require(line.endswith("|"), "Table row must end with pipe")
        cells = [cell.strip() for cell in line[1:-1].split("|")]
        require(len(cells) == 4 and all(cells), "Table requires four nonempty columns")
        rows.append(cells)
    require(rows[0] == ["比较维度", *PRODUCTS], "Invalid table header")
    require(
        all(re.fullmatch(r":?-{3,}:?", c) for c in rows[1]), "Invalid table separator"
    )
    require(
        [row[0] for row in rows[2:]] == list(DIMENSIONS), "Invalid table dimensions"
    )


def render_brief(draft, selection):
    """Strict structured candidate -> program-owned Markdown, never a ledger."""
    require(
        isinstance(draft, dict)
        and set(draft) == {"cells", "observations", "hypothesis"},
        "Bad draft schema",
    )
    entries = {e["fact_id"]: e for e in selection["entries"]}

    def statement(item, allowed):
        require(
            isinstance(item, dict) and set(item) == {"text", "fact_ids"},
            "Bad statement schema",
        )
        ids = item["fact_ids"]
        require(
            isinstance(ids, list)
            and bool(ids)
            and all(isinstance(i, str) for i in ids),
            "Missing Fact IDs",
        )
        require(
            len(set(ids)) == len(ids) and set(ids) <= allowed,
            "Invalid Fact IDs or scope",
        )
        return text_field(item["text"]) + " " + "".join(f"[{i}]" for i in ids)

    cells = draft["cells"]
    require(isinstance(cells, list) and len(cells) == 9, "Need nine cells")
    indexed = {}
    for c in cells:
        require(
            isinstance(c, dict) and set(c) == {"product", "dimension", "statement"},
            "Bad cell schema",
        )
        key = (c["product"], c["dimension"])
        require(
            key[0] in PRODUCTS and key[1] in DIMENSIONS and key not in indexed,
            "Invalid/duplicate cell",
        )
        allowed = {
            i
            for i, e in entries.items()
            if e["product"] == key[0] and key[1] in e["dimensions"]
        }
        if not allowed:
            require(c["statement"] is None, "Unsupported cell must be null")
            indexed[key] = (
                "证据不足：未选择该范围的已核验证据；不能据此判定产品不具备该能力。"
            )
        else:
            indexed[key] = statement(c["statement"], allowed)
    table_lines = [
        "| 比较维度 | ChatGPT | Claude | Gemini |",
        "| --- | --- | --- | --- |",
    ]
    table_lines += [
        "| " + d + " | " + " | ".join(indexed[p, d] for p in PRODUCTS) + " |"
        for d in DIMENSIONS
    ]
    # Table rows are one block; only prose blocks receive paragraph spacing.
    lines = [SCOPE, "\n".join(table_lines)]
    obs = draft["observations"]
    require(isinstance(obs, list) and len(obs) == 2, "Need exactly two observations")
    for n, o in enumerate(obs, 1):
        lines.append(f"观察 {n}：" + statement(o, set(entries)))
    lines.append("产品设计假设（未验证）：" + text_field(draft["hypothesis"]))
    lines.append(
        "审查状态：待语义与人工审查。程序检查仅验证结构、引用范围及字符数，不保证引用蕴含或事实绝对可靠。"
    )
    body = "\n\n".join(lines)
    require(len(body) <= 5000, "Body exceeds 5000 characters")
    return body


def evaluate(draft, selection):
    """No semantic PASS can be manufactured by a candidate or a missing reviewer."""
    result = dict(
        status="FAIL",
        acceptance_scope="MVP_OFFLINE_CONTRACT_ONLY",
        original_v3_status="NOT_EVALUATED",
        semantic_review="PENDING",
        model_calls=0,
        errors=[],
    )
    try:
        body = render_brief(draft, selection)
        check_markdown_table(body)
        result.update(
            table_format="PASS",
            status="PASS",
            body=body,
            body_characters=len(body),
            length_target="MET" if 1500 <= len(body) <= 2500 else "OUTSIDE_TARGET",
            sources=[e["evidence"] for e in selection["entries"]],
            scope_limits=[
                dict(fact_id=e["fact_id"], limit=e["scope_limit"])
                for e in selection["entries"]
            ],
            evidence_gaps=selection["gaps"],
        )
    except (ValueError, KeyError, TypeError) as exc:
        result["errors"].append(str(exc))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument(
        "--candidate", type=Path, help="Optional offline structured JSON candidate"
    )
    args = parser.parse_args(argv)
    try:
        selection = load_selection(args.input)
        if args.candidate:
            result = evaluate(
                json.loads(args.candidate.read_text(encoding="utf-8")), selection
            )
        else:
            result = dict(
                status="INPUT_READY",
                acceptance_scope="MVP_INPUT_ONLY",
                model_calls=0,
                semantic_review="NOT_RUN",
                original_v3_status="NOT_EVALUATED",
                fact_ids=[e["fact_id"] for e in selection["entries"]],
                gaps=selection["gaps"],
            )
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result = dict(status="FAIL", errors=[str(exc)], model_calls=0)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())

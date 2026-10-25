# CompetitorAI

**Evidence-Grounded Competitive Intelligence Copilot**

CompetitorAI 是一个面向产品经理的竞品研究助手。

当前版本围绕 ChatGPT、Claude 和 Gemini，生成带有 **Evidence ID、来源、证据缺口和审查状态** 的竞品简报。

项目主要关注一个问题：

> 生成一份竞品报告并不难，难的是判断其中的结论到底有什么依据。

因此，CompetitorAI 不只生成结果，也保留结论与 Evidence 之间的对应关系，并在证据不足时明确展示 Gap。

---

## Current MVP

当前 MVP 比较三款产品：

- ChatGPT
- Claude
- Gemini

覆盖三个维度：

1. 工作成果创建与编辑
2. 工具连接与任务执行
3. 复用与协作机制

最终输出包括：

- 三方能力对照表
- 两条基于现有 Evidence 的观察
- 一个明确标记为 Hypothesis 的产品设计假设
- Evidence ID
- Source
- Confidence
- Scope / Limitation
- Evidence Gap
- Review Status

当前示例使用固定的历史 Evidence，因此主要用于展示和验证当前工作流，不代表三款产品的最新实时状态。

---

## Workflow

```text
Verified Evidence
       ↓
Evidence Selection
       ↓
Brief Generation
       ↓
Programmatic Checks
       ↓
Semantic Review
       ↓
Competitive Brief
```

### 1. Evidence Selection

当前 MVP 使用 12 条 Verified Evidence。

每条 Evidence 保留：

- Evidence ID
- Product
- Dimension
- Claim
- Source
- Confidence
- Scope / Limitation

在进入生成阶段前，会检查 Evidence ID、产品归属、比较维度和固定输入的一致性。

如果某个产品在某个维度没有足够 Evidence，该位置会保留为 Evidence Gap，而不是用模型已有知识补齐。

---

### 2. Brief Generation

模型根据选定 Evidence 生成结构化竞品简报。

事实性内容需要关联对应的 Evidence ID。

例如：

```text
Claim
  ↓
Evidence ID
  ↓
Source
  ↓
Scope / Limitation
```

对于证据不足的比较项，系统会明确说明：

> 当前研究输入不足以支持结论。

这不代表该产品不存在相关能力，只代表当前 Evidence 无法支持这一判断。

---

### 3. Programmatic Checks

生成结果首先经过程序化检查。

当前主要检查：

- Evidence ID 是否有效
- Product 是否匹配
- Dimension 是否匹配
- 引用是否处于允许范围
- 必要字段是否存在
- Markdown 表格结构是否正确
- Evidence Gap 是否正确展示
- 正文长度是否符合约束

当前正文长度规则：

- Target：1,500–2,500 字符
- Hard limit：5,000 字符

这部分主要负责可以通过确定性规则判断的问题。

---

### 4. Semantic Review

程序规则无法直接判断一条自然语言 Claim 是否真正得到 Evidence 支持，因此在程序检查之外增加了单独的 Semantic Review。

主要检查：

- Claim 是否得到对应 Evidence 支持
- 是否存在过度概括
- 产品或套餐归属是否合理
- 是否遗漏重要限制
- Hypothesis 是否与事实内容明确区分

Semantic Review 是质量控制的一层，而不是最终事实来源。

因此：

**Review PASS 不等于所有事实绝对正确。**

---

## Example Output

简报的核心结构类似：

| 比较维度 | ChatGPT | Claude | Gemini |
|---|---|---|---|
| 工作成果创建与编辑 | Evidence | Evidence | Evidence |
| 工具连接与任务执行 | Evidence Gap | Evidence | Evidence |
| 复用与协作机制 | Evidence | Evidence | Evidence |

完整示例：

[examples/sample-brief.md](examples/sample-brief.md)

Semantic Review 示例：

[examples/sample-review.md](examples/sample-review.md)

---

## Validation

当前 MVP 已完成真实生成、审查和离线回归测试。

### 当前验证结果

- 12 条 Frozen Verified Evidence
- 1 次真实 Competitive Brief 生成
- 1 次主流程 Semantic Review
- 内容调整后 1 次针对受影响范围的 Semantic Review
- 30 项相关离线测试通过
- Evidence ID / Scope 检查
- Evidence Gap 检查
- Markdown Table Validation
- 长度边界测试
- 输入篡改测试
- Deterministic Replay
- Ruff Check
- Ruff Format Check

最终候选 Brief 正文约 **1,804 字符**。

30 项测试主要覆盖输入契约、输出契约和程序化 fail-closed 行为。

它们不代表系统事实准确率为 100%。

---

## A Real Failure Case

真实运行过程中曾发现一个 Markdown 表格问题。

原来的渲染逻辑在表头、separator 和数据行之间插入了空行。

结果是：

- 生成内容正常；
- 部分已有检查可以通过；
- 但最终 Markdown 表格不能按照预期展示。

后续处理：

1. 定位表格渲染逻辑；
2. 修复表格内部换行；
3. 新增 `check_markdown_table()`；
4. 增加对应的回归测试；
5. 使用原始结构化模型结果重新渲染；
6. 不重新调用模型生成内容；
7. 保留原始失败记录。

修复后：

- 已知错误格式会被拒绝；
- 正确格式可以通过；
- 相同模型结果可以进行确定性重放。

这个问题也促使当前版本把“输出是否符合要求”本身纳入测试范围，而不是只检查模型有没有返回内容。

---

## Evidence Handling

当前实现不会因为某个单元格缺少 Evidence 就允许模型自由补全。

例如，如果某个 Product × Dimension 没有对应的已选 Evidence：

```text
No allowed Evidence
        ↓
Statement must be empty
        ↓
Program renders Evidence Gap
```

这样可以区分：

- **没有证据支持**
- **产品没有这个能力**

这两种完全不同的情况。

在内容复核过程中，也曾发现 Evidence 边界需要进一步收紧。

例如：

- F68 可以直接支持 Claude Projects 用于组织聊天和文档；
- 但不能仅凭该 Evidence 推导出更具体的“复用机制”。

因此最终版本只保留 Evidence 能够直接支持的表述。

---

## Architecture

```text
┌─────────────────────────┐
│    Verified Evidence    │
│ ID / Source / Claim     │
│ Confidence / Scope      │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│   Evidence Selection    │
│ Product / Dimension     │
│ Reason / Evidence Gap   │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│     Brief Generation    │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│  Programmatic Checks    │
│ ID / Scope / Format     │
│ Length / Required Fields│
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│    Semantic Review      │
│    Claim ↔ Evidence     │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│   Competitive Brief     │
│ Sources / Gaps / Status │
└─────────────────────────┘
```

更详细的架构说明：

[docs/architecture.md](docs/architecture.md)

---

## Repository Structure

```text
Competitor-AI/
├── README.md
├── .gitignore
│
├── docs/
│   ├── architecture.md
│   ├── product-design.md
│   └── validation-and-limitations.md
│
├── examples/
│   ├── sample-brief.md
│   └── sample-review.md
│
├── src/
│   ├── README.md
│   └── v3/
│       └── mvp_brief.py
│
└── tests/
    └── test_mvp_brief.py
```

### Core Implementation

[src/v3/mvp_brief.py](src/v3/mvp_brief.py)

主要包含：

- Evidence Selection Validation
- Frozen Input Validation
- Evidence Scope
- Evidence Gap Handling
- Brief Rendering
- Markdown Table Validation
- Length Validation
- Offline MVP Evaluation

### Regression Tests

[tests/test_mvp_brief.py](tests/test_mvp_brief.py)

主要覆盖：

- Invalid Evidence ID
- Duplicate / Missing Selection
- Wrong Citation Scope
- Evidence Gap
- Length Boundary
- Markdown Table Regression
- Input Tampering
- No-model Offline Behavior

---

## Documents

### Product Design

[docs/product-design.md](docs/product-design.md)

记录目标用户、当前场景、MVP Scope 和质量控制设计。

### Architecture

[docs/architecture.md](docs/architecture.md)

说明 Evidence Selection、Generation、Programmatic Checks 和 Semantic Review 之间的关系。

### Validation & Limitations

[docs/validation-and-limitations.md](docs/validation-and-limitations.md)

记录测试范围、真实失败案例和当前验证边界。

---

## Tech Stack

- Python
- ByteDance DeerFlow 2.0
- DeepSeek API
- unittest
- Ruff

---

## Public Repository

这个仓库用于展示 CompetitorAI 当前 MVP 的：

- 产品设计
- Evidence workflow
- 核心实现
- Regression Tests
- Sample Brief
- Semantic Review
- Validation Results

公开代码来自实际运行过的 CompetitorAI / DeerFlow 项目环境。

完整运行仍依赖原项目中的部分组件和输入，包括：

- `v3.frozen_downstream`
- Frozen Evidence
- `mvp_selection.json`
- DeerFlow 2.0 运行环境
- Model API configuration

因此，本仓库主要作为当前 MVP 的代码与产品设计 Snapshot，而不是独立发布的 Python Package。

仓库不会包含 API Key、私有配置、本地用户路径或敏感运行日志。

---

## Current Scope

当前版本已经验证了固定 Evidence 输入下的：

```text
Evidence
→ Generation
→ Programmatic Validation
→ Semantic Review
→ Competitive Brief
```

目前主要有两个使用边界：

1. 示例基于 Frozen Evidence，不代表产品当前最新状态；
2. 当前版本属于 MVP，尚未按照生产环境要求部署。

更完整的验证范围和限制见：

[docs/validation-and-limitations.md](docs/validation-and-limitations.md)

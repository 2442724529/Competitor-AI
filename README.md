# CompetitorAI

**Evidence-Grounded Competitive Intelligence Copilot**

基于证据追溯的 AI 竞品研究助手。

CompetitorAI 是一个面向产品经理、AI 产品经理和创业者的个人 MVP，用于比较 AI 产品能力差异，并生成带有 **Evidence ID、来源、证据缺口和审查状态** 的竞品简报。

当前 MVP 聚焦：

- ChatGPT
- Claude
- Gemini

以及三个比较维度：

1. 工作成果创建与编辑
2. 工具连接与任务执行
3. 内容组织、复用与协作

> 当前示例基于固定的历史 Frozen Evidence，用于验证产品链路，不代表 ChatGPT、Claude 或 Gemini 的最新实时状态。

---

## Why this project

这个项目关注的不是：

> AI 能不能生成一份看起来完整的竞品报告？

而是几个更具体的问题：

- 生成的结论能否追溯到具体 Evidence？
- 有引用时，引用是否真的支持对应 Claim？
- Evidence 不足时，系统能否明确暴露 Gap，而不是让模型自动补全？
- 格式检查通过之后，内容是否仍然可能存在事实或语义问题？

因此，CompetitorAI 将竞品简报拆成一条可检查的生成链路：

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

---

## MVP Scope

当前版本使用 **12 条固定 Verified Evidence**。

每条 Evidence 保留：

- Evidence ID
- Product
- Dimension
- Claim
- Source
- Confidence
- Scope / Limitation

POC 阶段暂时冻结 Search、Fetch 和 Evidence Extraction，先单独验证：

```text
Evidence → Generation → Validation → Review
```

这样做的目的不是证明完整产品已经成立，而是减少实验变量，优先验证最关键的不确定性：

1. Verified Evidence 能否稳定作为模型输入
2. Claim 能否绑定对应 Evidence ID
3. 确定性错误能否通过程序规则拦截
4. Claim 与 Evidence 的语义支持关系能否被单独审查
5. Evidence 不足时系统能否选择暴露 Gap，而不是自动补全

---

## Output

当前 Competitive Brief 包含：

- ChatGPT / Claude / Gemini 三方能力对照表
- 两条基于 Evidence 的观察
- 一个明确标记为 **Hypothesis** 的产品设计假设
- Evidence ID
- 来源与置信度
- Evidence Gap
- Scope / Limitation
- Review Status

如果某个产品在某个维度缺少足够 Evidence，系统不会允许模型自由补全，而是明确显示：

**Evidence Gap**

这里的 Gap 表示：

> 当前研究输入不足以支持结论。

它并不表示该产品一定不存在对应能力。

---

## Programmatic Checks

模型输出之后首先进入确定性检查。

当前检查包括：

- Evidence ID 是否存在
- Product 是否匹配
- Dimension 是否匹配
- 引用是否处于允许范围
- 必要字段是否存在
- Markdown 表格是否合法
- Evidence Gap 是否显式展示
- 正文长度是否符合约束

正文长度：

- Target：1,500–2,500 字符
- Hard limit：5,000 字符

这些检查主要处理可以通过程序规则明确判断的问题。

它们不会尝试判断一个 Claim 在语义上是否真的被 Evidence 支持。

---

## Semantic Review

Programmatic Checks 之后，会进行一次单独的 Semantic Review。

主要检查：

- Claim 是否得到 Evidence 支持
- 是否存在过度概括
- 产品或套餐归属是否错误
- 是否遗漏重要限制
- Hypothesis 是否被误写成事实

需要特别说明：

**Semantic Review PASS ≠ 所有事实绝对正确。**

它只是整个质量控制流程中的一层。

---

## Validation Snapshot

当前 MVP 已完成：

- 12 条 Frozen Verified Evidence 输入
- 1 次真实 Competitive Brief 生成
- 1 次独立 Semantic Review
- 30 项相关离线测试
- Evidence ID / scope 检查
- Evidence Gap 检查
- Markdown table validation
- 长度边界测试
- 输入篡改测试
- deterministic replay
- Ruff check
- Ruff format check

最终候选 Brief 正文约 **1,804 字符**。

> 30 项测试通过主要证明输入契约、输出契约以及程序化 fail-closed 行为。
>
> 它不代表事实准确率为 100%，目前也没有基于大规模人工标注数据集计算事实准确率。

---

## Failure Case

项目中保留了一个真实失败案例。

第一次真实运行时：

- Brief Generation 完成
- Semantic Review 返回 PASS
- 最终就绪评估仍然 FAIL

问题不是事实内容，而是 **Markdown 表格渲染错误**。

原来的渲染方式在：

```text
header
separator
data row
```

之间错误加入空行。

结果是：

> 部分原有程序检查能够通过，但 Markdown 表格实际上无法正常渲染。

后续处理：

1. 定位表格渲染逻辑
2. 修复表格内部换行
3. 新增 `check_markdown_table()`
4. 增加对应回归测试
5. 使用原始模型结构化输出进行 deterministic replay
6. 不重新调用模型生成内容
7. 保留原始失败记录

修复后：

- 错误格式会被拒绝
- 正确格式可以通过
- 不需要重新生成模型内容

这个案例也说明：

> Validation 本身同样需要被验证。

---

## Content Review Cases

除了程序错误，人工内容复核也发现过 Evidence 使用边界问题。

### F68

Evidence 直接支持：

> Claude Projects 可以组织聊天和文档。

但“特定复用机制”属于进一步解释，并没有被该 Evidence 直接证明。

最终改为只保留 Evidence 能够直接支持的内容。

### Enterprise

部分 Enterprise 排除理由来源于 Evidence Selection 的 Gap Metadata，而不是产品能力 Evidence。

因此最终将其归类为：

**证据选择范围说明**

而不是产品能力事实。

### Current availability

部分 Frozen Evidence 可以支持历史套餐或能力归属，但没有重新验证：

- 当前最新可用性
- 地域限制
- 部分套餐变化
- 部分来源脚注

因此这些内容保留 Scope / Limitation，而不作为实时产品状态使用。

---

## Example

查看最终候选简报：

[examples/sample-brief.md](examples/sample-brief.md)

查看 Semantic Review 示例：

[examples/sample-review.md](examples/sample-review.md)

示例重点展示：

```text
Claim
  ↓
Evidence ID
  ↓
Source
  ↓
Confidence
  ↓
Scope / Limitation
```

---

## Historical V3 Context

CompetitorAI 之前曾尝试过范围更完整的 V3 Report Pipeline。

原始结果为：

- Mandatory Coverage：**3/6 = 50%**
- Original Overall Acceptance：**FAIL**

这个结果没有为了 Portfolio 修改成 PASS。

当前求职版本将范围收窄到：

```text
Frozen Evidence
→ Generation
→ Validation
→ Review
```

目的是减少变量，单独验证 Evidence-grounded competitive brief 的核心链路。

因此：

**当前 MVP 核心链路验证通过，不代表原始完整 V3 Pipeline 已通过验收。**

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

核心实现：

[src/v3/mvp_brief.py](src/v3/mvp_brief.py)

Regression tests：

[tests/test_mvp_brief.py](tests/test_mvp_brief.py)

---

## Documents

### Architecture

[docs/architecture.md](docs/architecture.md)

说明 Evidence、Generation、Programmatic Validation 和 Semantic Review 之间的关系。

### Product Design

[docs/product-design.md](docs/product-design.md)

记录当前 MVP 的用户、问题定义、Scope 和产品取舍。

### Validation & Limitations

[docs/validation-and-limitations.md](docs/validation-and-limitations.md)

记录测试范围、真实失败案例以及当前项目不能证明的内容。

---

## Tech Stack

- Python
- ByteDance DeerFlow 2.0
- DeepSeek API
- unittest
- Ruff

---

## Public Repository Scope

这个公开仓库是 CompetitorAI 当前 MVP 的 **Portfolio Snapshot**。

它用于展示：

- 产品问题定义
- Evidence-grounded workflow
- Evidence selection contract
- Programmatic validation
- Semantic Review
- Failure case
- Regression tests
- Competitive Brief 示例
- 当前产品边界

公开的核心代码来自原 CompetitorAI / DeerFlow V3 项目环境。

完整原始运行仍依赖部分未包含在该 Portfolio Snapshot 中的组件，包括：

- `v3.frozen_downstream`
- Frozen Evidence 输入文件
- `mvp_selection.json`
- DeerFlow 2.0 原项目运行环境
- 模型 API 配置

因此，当前公开仓库**不是一个完全独立安装的 Python package，也不应被理解为生产级部署版本**。

仓库不会包含：

- API Key
- 私有配置
- 本地用户路径
- 敏感运行日志

---

## Current Status

当前项目定位：

**完成核心链路验证的 AIPM 个人 MVP。**

它已经验证：

- 固定 Verified Evidence 可以进入结构化生成流程
- Claim 可以绑定 Evidence ID
- Evidence Gap 可以被显式暴露
- 一部分确定性错误可以被程序拦截
- Claim ↔ Evidence 可以增加独立语义审查层
- 真实失败可以转化为 Regression Test

它还没有证明：

- 所有事实都正确
- 产品数据是实时最新状态
- 对所有竞品研究任务都有效
- 已达到生产级可靠性
- 已经存在真实用户增长或商业化验证

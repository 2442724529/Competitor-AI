# CompetitorAI

**Evidence-Grounded Competitive Intelligence Copilot**

CompetitorAI 是一个面向产品经理的竞品研究助手。

当前版本用于比较 ChatGPT、Claude 和 Gemini 在部分产品能力上的差异，并生成一份带有证据来源、Evidence ID 和证据缺口说明的竞品简报。

项目目前主要解决两个问题：

- 竞品分析中的关键结论能否追溯到具体证据；
- 当引用、格式或证据存在问题时，系统能否及时识别，而不是直接输出一份“看起来正确”的报告。

---

## 当前版本能做什么

目前支持对 ChatGPT、Claude 和 Gemini 进行三个维度的比较：

1. 工作成果创建与编辑
2. 工具连接与任务执行
3. 内容组织、复用与协作

系统最终输出：

- 三方能力对照表
- 基于现有证据的关键观察
- 明确区分事实与假设的产品设计假设
- Evidence ID
- 来源与置信度
- 适用范围
- Evidence Gap
- 检查与审查状态

---

## 工作流程

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

从已有 Verified Evidence 中选择与当前研究任务相关的证据。

每条证据保留：

- Evidence ID
- 对应产品
- 比较维度
- 原始主张
- 来源
- 置信度
- 使用限制

当前 MVP 使用 12 条 Verified Evidence。

---

### 2. Brief Generation

模型根据选定 Evidence 生成竞品简报。

事实内容需要关联对应 Evidence ID。

如果现有证据无法支持某项比较，系统会明确显示 Evidence Gap，而不是自动补充未经验证的信息。

---

### 3. Programmatic Checks

生成结果会经过程序化检查，目前包括：

- Evidence ID 是否存在
- 引用是否属于对应产品和比较维度
- 必要字段是否完整
- Markdown 表格结构是否正确
- 正文长度是否符合要求
- Evidence Gap 是否明确展示

这些检查主要用于处理可以通过确定性规则判断的问题。

---

### 4. Semantic Review

在程序检查之外，再进行一次单独的语义审查。

主要检查：

- Evidence 是否真正支持对应主张
- 是否存在过度概括
- 产品或套餐归属是否存在问题
- 是否遗漏重要限制
- 产品设计假设是否与事实内容区分

语义审查用于辅助发现程序规则难以识别的问题。

---

## Example Output

简报的核心结构类似：

| 能力维度 | ChatGPT | Claude | Gemini |
|---|---|---|---|
| 创建与编辑 | Evidence | Evidence | Evidence |
| 工具与任务执行 | Evidence Gap | Evidence | Evidence |
| 组织、复用与协作 | Evidence | Evidence | Evidence |

每个结论可以进一步查看对应的：

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

示例简报：

`examples/sample-brief.md`

审查结果：

`examples/sample-review.md`

---

## Validation

当前版本已经完成真实生成和审查流程验证。

目前完成：

- 12 条 Verified Evidence 作为固定输入
- 1 次真实竞品简报生成
- 1 次单独语义审查
- 30 项相关离线测试
- Evidence ID 检查
- 引用范围检查
- Markdown 表格检查
- 长度检查
- Evidence Gap 检查
- 历史结果的确定性重放验证

最终候选简报正文约 **1,804 字符**。

### 一个实际发现的问题

真实运行过程中曾出现 Markdown 表格内部存在空行的问题。

当时原有检查没有识别这个错误，导致部分程序检查通过，但最终表格无法按照预期展示。

后续处理包括：

1. 定位表格渲染逻辑
2. 修复表格行之间的换行方式
3. 增加对应的失败用例和回归测试
4. 使用原始模型输出重新渲染
5. 不重新调用模型生成内容

修复后，相关离线测试重新通过。

---

## Architecture

```text
┌──────────────────────┐
│  Verified Evidence   │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│  Evidence Selection  │
│ ID / Source / Scope  │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│   Brief Generation   │
└──────────┬───────────┘
           ↓
┌──────────────────────────┐
│   Programmatic Checks    │
│ ID / Format / Length     │
└──────────┬───────────────┘
           ↓
┌──────────────────────┐
│   Semantic Review    │
│ Claim ↔ Evidence     │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Competitive Brief    │
│ Sources / Gaps /     │
│ Review Status        │
└──────────────────────┘
```

更完整的说明见：

`docs/architecture.md`

---

## Repository Structure

```text
competitorai/
├── README.md
├── docs/
│   ├── architecture.md
│   ├── product-design.md
│   └── validation-and-limitations.md
├── examples/
│   ├── sample-brief.md
│   └── sample-review.md
├── src/
│   └── mvp/
│       └── mvp_brief.py
├── tests/
│   └── test_mvp_brief.py
└── assets/
```

---

## Tech Stack

- Python
- ByteDance DeerFlow 2.0
- DeepSeek API
- Unittest
- Ruff

---

## Current Scope

当前版本已经可以完成固定 Evidence 输入下的竞品简报生成、检查和审查流程。

目前有两个主要边界：

- 当前使用冻结的历史 Evidence，因此示例结果不代表相关产品的最新状态；
- 当前项目仍属于 MVP，没有按照生产环境要求进行部署。

更详细的验证范围与已知限制见：

`docs/validation-and-limitations.md`

---

## Reproduction

完整运行需要：

- DeerFlow 2.0 环境
- 项目使用的 Frozen Evidence
- 模型 API 配置

公开仓库不会包含：

- API Key
- 私有配置
- 本地用户路径
- 敏感运行日志

核心代码、测试逻辑、示例简报和验证说明会保留在仓库中，方便查看当前 MVP 的实现方式。

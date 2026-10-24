# Architecture

CompetitorAI 当前 MVP 采用一条相对简单的处理链路：

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
Final Brief
```

整体目标不是让模型一次性完成所有工作，而是把不同类型的问题拆开处理。

---

## 1. Evidence Layer

输入来自已经确认过的 Verified Evidence。

每条 Evidence 会保留：

- Evidence ID
- 对应产品
- 比较维度
- 原始主张
- 来源
- 置信度
- 使用限制

当前 MVP 使用 12 条固定 Evidence。

这一层主要解决两个问题：

1. 确保生成内容可以追溯到具体依据；
2. 避免模型在证据不足时自由补全事实。

---

## 2. Evidence Selection

不是所有 Evidence 都会进入一次生成任务。

在当前场景中，只选择与以下三个维度相关的证据：

- 工作成果创建与编辑
- 工具连接与任务执行
- 内容组织、复用与协作

选择结果会记录：

```text
Evidence ID
Product
Dimension
Reason
Source
Scope / Limitation
```

如果某个产品在某个维度缺少足够 Evidence，会保留为 Evidence Gap。

---

## 3. Brief Generation

选定 Evidence 后，模型生成一份结构化竞品简报。

输出主要包含：

- 三方能力对照表
- 两条关键观察
- 一条产品设计假设
- Evidence ID
- 来源与置信度
- Evidence Gap
- 使用限制

模型只能基于当前提供的 Evidence 进行生成。

当前版本不会使用实时 Search / Fetch 补充缺失信息。

---

## 4. Programmatic Checks

生成结果首先经过程序化检查。

这一层主要负责适合确定性判断的问题：

```text
Evidence ID
      ↓
Reference Scope
      ↓
Required Fields
      ↓
Markdown Table
      ↓
Length
      ↓
Evidence Gap
```

具体包括：

- Evidence ID 是否存在
- Evidence 是否属于正确产品
- Evidence 是否属于对应比较维度
- 必要字段是否存在
- Markdown 表格结构是否正确
- 正文长度是否符合要求
- Evidence Gap 是否被显式展示

如果关键检查失败，当前输出不会被视为通过。

---

## 5. Semantic Review

程序规则很难判断一句自然语言主张是否真正被 Evidence 支持。

因此，在程序检查之后增加一次单独的语义审查。

主要检查：

- Claim 与 Evidence 是否匹配
- 是否存在过度概括
- 产品或套餐归属是否错误
- 是否遗漏使用限制
- Hypothesis 是否被误写成事实

可以理解为：

```text
Claim
  ↕
Evidence
```

语义审查负责判断两者之间的支持关系。

它属于辅助检查，不被视为绝对事实验证。

---

## 6. Final Output

通过当前检查流程后，最终展示内容包括：

```text
Competitive Brief
├── Capability Comparison
├── Key Observations
├── Product Hypothesis
├── Evidence IDs
├── Sources
├── Confidence
├── Evidence Gaps
└── Review Status
```

用户看到的不只是最终结论，也可以看到结论对应的依据和限制。

---

## System Diagram

```text
┌─────────────────────────┐
│    Verified Evidence    │
│ ID / Source / Claim     │
│ Confidence / Scope      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Evidence Selection    │
│ Product / Dimension     │
│ Reason / Evidence Gap   │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│     LLM Generation      │
│   Competitive Brief     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Programmatic Checks    │
│ ID / Scope / Format     │
│ Length / Required Fields│
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│    Semantic Review      │
│    Claim ↔ Evidence     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│       Final Brief       │
│ Sources / Gaps / Status │
└─────────────────────────┘
```

---

## Why Split Validation Into Two Layers?

Programmatic Checks 和 Semantic Review 负责的问题不同。

### Programmatic Checks

适合：

- ID 是否存在
- 格式是否正确
- 长度是否超限
- 引用范围是否匹配

优点是结果稳定、可重复。

### Semantic Review

适合：

- 一条 Evidence 是否真正支持某个 Claim
- 是否存在过度概括
- 是否存在语义层面的归属错误

这类问题无法简单通过字符串或规则判断。

因此当前架构使用：

**确定性规则处理确定性问题，模型处理语义问题。**

---

## Current Implementation

当前 MVP 基于：

- ByteDance DeerFlow 2.0
- Python
- DeepSeek API
- Unittest
- Ruff

核心 MVP 逻辑主要位于：

```text
src/mvp/mvp_brief.py
```

相关测试位于：

```text
tests/test_mvp_brief.py
```

完整运行还依赖项目原始 Frozen Evidence 和模型 API 配置。

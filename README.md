# CompetitorAI

Evidence-Grounded Competitive Intelligence Copilot**

CompetitorAI 是一个面向产品经理、AI 产品经理和创业者的 AI 竞品研究助手。

项目重点不是让大模型生成更长的竞品报告，而是解决一个更核心的问题：

> AI 生成的竞品结论，是否真的有证据支持？用户能否快速追溯来源、限制和证据缺口?

当前版本为一个完成核心链路验证的 MVP，聚焦 ChatGPT、Claude 和 Gemini 三款 AI 产品的能力比较。

---

## Why CompetitorAI?

通用大模型已经可以快速生成竞品分析，但在实际使用中仍可能出现：

- 有引用，但引用并不能真正支持对应结论
- 产品功能、套餐或适用范围被过度概括
- Prompt 无法稳定保证输出结构和长度
- AI 自我审查仍可能漏掉具体事实错误
- 局部检查通过，但最终结果仍不可交付

因此，CompetitorAI 将竞品研究拆分为：

**Evidence → Generation → Validation → Review → Delivery**

通过证据追溯、程序化检查和语义审查，让 AI 输出更容易被检查，而不是默认相信模型生成结果。

---

## Target Users

首版目标用户：

- Product Manager
- AI Product Manager
- Founder / Startup Team

核心场景：

快速比较多个 AI 产品的能力差异，并获得一份包含证据、限制和审查状态的竞品决策简报。

---

## MVP Scope

当前 MVP 比较：

- ChatGPT
- Claude
- Gemini

聚焦三个能力维度：

1. 工作成果创建与编辑
2. 工具连接与任务执行
3. 内容复用与协作机制

输出包括：

- 三方能力对照表
- 两条有证据支持的观察
- 一项明确标记为假设的产品设计提案
- Evidence ID 与来源
- 置信度与适用范围
- Evidence Gap
- 程序检查与语义审查状态

当前版本使用冻结的历史 Evidence 进行验证，因此**不声称相关产品信息仍然是最新状态**。

---

## How It Works

```text
Frozen Evidence
      ↓
Evidence Selection
      ↓
AI Brief Generation
      ↓
Programmatic Validation
      ↓
Semantic Review
      ↓
Brief + Sources + Gaps + Review Status
```

### 1. Evidence Selection

从冻结数据中选择与当前比较场景相关的 Verified Evidence，并保留：

- Evidence ID
- 来源
- 原始主张
- 置信度
- 适用限制
- Evidence Gap

### 2. AI Brief Generation

模型基于选定 Evidence 生成竞品简报。

事实主张必须关联对应 Evidence ID；证据不足时显式标记，而不是自动补全。

### 3. Programmatic Validation

通过确定性规则检查：

- Evidence ID 是否有效
- 引用范围是否符合要求
- Markdown 表格是否可正常渲染
- 输出长度是否符合约束
- 必要字段是否存在
- Evidence Gap 是否被显式展示

### 4. Semantic Review

通过单独的模型调用检查：

- Evidence 是否真正支持对应主张
- 是否存在过度概括
- 产品、套餐或能力归属是否存在问题
- 是否遗漏重要限制
- 产品假设是否与已验证事实明确区分

语义审查仍可能漏检，因此不能将 Review PASS 等同于事实绝对正确。

---

## Architecture

```text
┌─────────────────────┐
│   Frozen Evidence   │
│  Verified Evidence  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Evidence Selection  │
│ ID / Source / Gap   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│   LLM Generation    │
│ Competitive Brief   │
└──────────┬──────────┘
           ↓
┌─────────────────────────┐
│ Programmatic Validation │
│ Format / ID / Length    │
└──────────┬──────────────┘
           ↓
┌─────────────────────┐
│   Semantic Review   │
│  Claim ↔ Evidence   │
└──────────┬──────────┘
           ↓
┌─────────────────────────┐
│     Final Deliverable   │
│ Brief / Sources / Gaps  │
│     Review Status       │
└─────────────────────────┘
```

---

## Validation Results

当前 MVP 已完成真实生成和审查流程验证。

### 已完成

- 12 条 Verified Evidence 作为 MVP 输入
- 完成一次真实 AI 简报生成
- 完成一次单独语义审查
- 30 项相关离线测试通过
- Fact ID 与引用范围检查
- Markdown 表格格式检查
- 输出长度检查
- Evidence Gap 检查
- 历史失败记录保留
- 使用历史模型产物完成确定性重放

最终候选简报正文约 **1,804 字符**。

### 一个真实失败案例

首次真实运行中，程序检查未发现 Markdown 表格内部存在空行，导致检查结果局部通过，但最终展示格式不合格。

随后：

1. 定位表格渲染逻辑问题
2. 修复 Markdown 输出
3. 增加错误格式回归测试
4. 使用原始模型产物重新渲染
5. 不重新调用模型
6. 保留原始失败记录

这个问题说明：

> **Validation PASS 不代表产品最终可交付，验收规则本身也需要通过真实失败案例持续验证。**

---

## Product Iteration

### Baseline

原版 DeerFlow 可以搜索并生成竞品报告，但存在来源优先级、事实准确性和引用支持关系问题。

### V1

增加：

- CompetitorAI Skill
- 固定报告结构
- Source Priority
- Fact Verification Prompt

结果：

结构改善，但事实质量验收仍未通过。

### V2

增加：

- 独立 Validator
- FAIL Gate
- Auto Revision
- Re-audit

结果：

能够拦截部分不合格报告，但正式 E2E 仍然 FAIL。

### V3

进一步增加 Evidence Admission、Fact Ledger 和更严格的验收逻辑。

实验中发现：

- 长篇 JSON 输出容易解析失败
- Prompt 无法稳定控制正文长度
- 格式正确不等于事实正确
- 语义审查也可能漏掉具体错误

因此，项目最终从完整长报告收敛为当前的窄场景 MVP。

---

## Key Product Decision

项目最重要的产品决策之一，是**停止继续追求完整 11 节竞品报告，转而验证一个更小、更可控的核心链路**。

原因：

- 完整链路中的不确定因素过多
- 输出长度和结构不稳定
- 难以定位事实错误来自哪个环节
- 继续扩展功能并不能证明产品核心价值

因此，当前阶段优先验证：

```text
Evidence → Generation → Validation → Review
```

而不是继续增加报告长度或复杂功能。

---

## Known Limitations

当前项目仍存在明确边界：

- 尚未进行真实用户实验
- 没有经过验证的准确率指标
- 没有经过验证的效率提升数据
- 冻结 Evidence 无法证明产品当前仍然可用
- 部分套餐、地域和来源脚注仍存在未核实项
- 语义审查仍可能漏检具体事实错误
- 当前结果仅验证窄场景 MVP
- 原始 V3 Coverage 仍为 **3/6**
- 原始 V3 Overall Acceptance 仍为 **FAIL**

因此，本项目不声称已经达到生产级可靠性。

---

## Tech Stack

- Python
- ByteDance DeerFlow 2.0
- DeepSeek API
- Unittest
- Ruff

---

## Repository Structure

```text
competitorai/
├── README.md
├── docs/
│   ├── architecture.md
│   ├── product-design.md
│   ├── validation-and-limitations.md
│   └── iteration-history.md
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

## Reproduction

本仓库主要用于展示 CompetitorAI MVP 的产品设计、核心实现和验证过程。

完整实验依赖：

- DeerFlow 2.0 环境
- 原始冻结 Evidence
- 模型 API 配置

本仓库不包含：

- API Key
- 私有配置
- 本地路径信息
- 敏感运行日志

---

## Project Status

**MVP Core Workflow Validated**

当前版本已经完成核心链路验证和求职作品集整理，但尚未完成真实用户验证和生产化。

---

## What I Learned

这个项目让我重点验证了几个 AI 产品设计原则：

1. AI 输出质量不能只依赖 Prompt。
2. 引用存在，不代表引用支持结论。
3. 程序化规则与语义审查应该解决不同类型的问题。
4. AI 审查结果本身也需要被限制和验证。
5. POC 的目标不是证明方案一定成功，而是尽快减少最大的不确定性。
6. 当完整方案验证成本过高时，应主动缩小 MVP，而不是继续堆功能。

# Product Design

## 1. Product Overview

CompetitorAI 是一个面向产品经理的竞品研究助手。

当前版本聚焦 ChatGPT、Claude 和 Gemini 三款 AI 产品，通过已有 Verified Evidence 生成一份带有来源、Evidence ID、证据缺口和审查状态的竞品简报。

项目重点不是自动生成尽可能长的报告，而是让用户更容易判断：

- 这条结论来自哪里；
- 当前证据是否足够；
- 哪些内容属于事实；
- 哪些内容属于推断或产品假设；
- 哪些地方仍然需要人工确认。

---

## 2. Target Users

当前主要面向：

- Product Manager
- AI Product Manager
- Founder / Startup Team

这些用户通常需要快速理解竞品能力差异，并将研究结果用于：

- 产品规划
- 功能对比
- Roadmap 讨论
- 新功能机会识别
- 竞品会议准备

---

## 3. User Problem

使用通用大模型进行竞品研究时，生成报告本身并不困难。

真正的问题在于：

### 问题一：结论缺少可追溯性

模型可能给出一个看起来合理的产品结论，但用户仍然需要重新判断：

> 这句话到底是从哪条资料得出的？

---

### 问题二：有引用不代表引用支持结论

一条来源可能确实提到了某项功能，但并不一定支持模型生成的完整判断。

例如：

```text
Source mentions Projects
        ↓
Model concludes "strong reusable collaboration mechanism"
```

中间可能存在额外推断。

---

### 问题三：证据不足时，模型容易补全

在做三方对比时，如果其中一家产品缺少对应 Evidence，模型可能倾向于利用已有知识补齐表格。

对于竞品研究而言：

**缺少证据本身也是一种结果。**

因此当前版本使用 Evidence Gap，而不是强制填满所有比较结果。

---

### 问题四：格式正确不代表内容可靠

即使报告：

- 结构完整
- 有来源
- 有表格
- 有引用

仍然可能存在：

- 产品归属错误
- 套餐范围错误
- 过度概括
- 使用限制遗漏

因此，输出格式和事实支持需要分开检查。

---

## 4. Product Goal

当前版本的目标是：

> 帮助产品经理生成一份可以继续核查，而不是只能直接相信的竞品简报。

具体表现为：

1. 关键主张可以追溯到 Evidence ID；
2. 证据不足时明确显示 Gap；
3. 事实和产品假设分开；
4. 程序规则负责可确定的问题；
5. 语义审查负责 Claim 与 Evidence 的支持关系；
6. 用户可以看到结果的适用范围和限制。

---

## 5. MVP Scope

当前 MVP 比较：

- ChatGPT
- Claude
- Gemini

只覆盖三个能力维度：

### 工作成果创建与编辑

关注：

- 内容创建
- 内容编辑
- 文件或工作成果生成

### 工具连接与任务执行

关注：

- 外部工具连接
- 服务调用
- 任务执行能力

### 内容组织、复用与协作

关注：

- 内容组织
- 可复用机制
- 团队协作相关能力

---

## 6. Current User Flow

```text
Select Competitors
        ↓
Load Verified Evidence
        ↓
Select Relevant Evidence
        ↓
Generate Competitive Brief
        ↓
Run Programmatic Checks
        ↓
Run Semantic Review
        ↓
Review Brief + Sources + Gaps
```

当前 MVP 没有设计复杂的交互界面。

重点验证的是竞品研究结果本身的可追溯性和质量控制流程。

---

## 7. Output Design

最终简报包含四类核心信息。

### Capability Comparison

使用三方对照表快速查看不同产品在三个维度上的已有 Evidence。

### Key Observations

从当前 Evidence 中提炼有支持的差异和共同点。

### Product Hypothesis

允许从研究结果提出产品设计思考，但必须明确标记为 Hypothesis。

Hypothesis 不会被包装成已被 Evidence 证明的事实。

### Evidence & Limitations

展示：

- Evidence ID
- Source
- Confidence
- Scope
- Evidence Gap
- Review Status

---

## 8. Quality Control Design

当前产品将质量控制拆成两部分。

### Programmatic Checks

适合判断规则明确的问题：

- Evidence ID 是否有效
- 引用范围是否正确
- 表格格式是否正确
- 是否超过长度限制
- 必要字段是否存在

### Semantic Review

适合处理：

- Evidence 是否真正支持 Claim
- 是否存在过度概括
- 是否遗漏重要限制
- 产品归属是否合理

这样可以避免把所有判断都交给模型完成。

---

## 9. Failure Handling

当前版本不会默认把所有输出视为可交付。

如果出现：

- Evidence ID 错误
- 表格格式错误
- 关键字段缺失
- 超过硬性长度限制
- Evidence Gap 未正确展示

系统会返回 FAIL，而不是静默继续。

对于证据本身不足的问题，则保留 Gap，而不是自动补全。

---

## 10. MVP Success Criteria

当前阶段主要关注以下几项：

### 可追溯性

核心事实是否可以找到对应 Evidence ID。

### 输出完整性

简报是否包含规定的结构和必要信息。

### 错误识别

已知格式、引用和输入错误是否能够被程序检测。

### 证据缺口

Evidence 不足时是否能够显式暴露，而不是补全。

### 可复现性

固定 Evidence 输入下，测试和重新渲染结果是否可以复现。

---

## 11. Current Results

当前版本已完成：

- 12 条 Verified Evidence 的固定输入
- ChatGPT、Claude、Gemini 三方比较
- 一次真实简报生成
- 一次单独语义审查
- 30 项相关离线测试
- Markdown 表格问题修复及回归验证
- Evidence Gap 展示
- Fact ID 和引用范围检查
- 确定性重放验证

这些结果主要证明当前 MVP 的核心工作流可以运行。

---

## 12. Next Step

如果继续推进，下一阶段更有价值的工作不是增加更多报告章节，而是验证真实使用价值。

优先考虑：

1. 让目标用户实际查看或使用当前简报；
2. 观察他们是否会查看 Evidence 和 Gap；
3. 记录哪些竞品信息最影响产品决策；
4. 基于真实反馈调整输出结构；
5. 再评估是否需要接入实时 Search / Fetch。

当前版本先保持简单，避免在用户价值尚未验证前增加过多功能。

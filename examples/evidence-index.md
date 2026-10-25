# Evidence 索引

本页汇总当前 CompetitorAI MVP 示例使用的 12 条 Verified Evidence。

这些 Evidence 来自实验阶段保存的 Frozen Evidence，用于支持当前竞品简报中的具体主张，并保留对应的来源、日期和适用范围。

> 本页记录的是本次实验使用的历史 Evidence，不代表 ChatGPT、Claude 或 Gemini 当前最新产品状态。

---

## Evidence 列表

| Evidence ID | 产品 | 比较维度 | 当前支持的内容 | 来源 | Evidence 日期 | 适用范围 / 限制 |
|---|---|---|---|---|---|---|
| F98 | ChatGPT | 工作成果创建与编辑 | ChatGPT Slides 支持从对话、文件、提纲或示例 Deck 创建演示文稿，并可在 Space 中继续协作 | [OpenAI Product Release Notes](https://openai.com/products/release-notes/) | 2026-10-16 | 仅支持 Slides 场景，不推及全部文档类型或当前套餐状态 |
| F99 | ChatGPT | 工作成果创建与编辑 | Slides 支持直接编辑文字、图片、形状和图表，也可要求 ChatGPT 修改内容 | [OpenAI Product Release Notes](https://openai.com/products/release-notes/) | 2026-10-16 | 仅证明存在对应编辑能力，不评价编辑质量或成功率 |
| F100 | ChatGPT | 复用与协作机制 | Slides 支持邀请团队成员实时编辑同一 Deck，并留下共享评论 | [OpenAI Product Release Notes](https://openai.com/products/release-notes/) | 2026-10-16 | 仅支持演示文稿共同编辑和评论，不推广为所有工作成果的协作能力 |
| F60 | Claude | 工作成果创建与编辑；工具连接与任务执行 | Claude Free 包含文件创建和代码执行能力 | [Claude 官方网站](https://claude.com/) | 未记录发布日期 | 仅对应 Free 方案；不证明所有格式均可编辑，也不等同于外部任务执行 |
| F63 | Claude | 工具连接与任务执行 | Claude Free 支持连接 Slack 和 Google Workspace 服务 | [Claude 官方网站](https://claude.com/) | 未记录发布日期 | 不据此推断连接后的具体读写权限或任务完成率 |
| F64 | Claude | 工具连接与任务执行 | Claude Free 支持通过 Remote MCP Connector 集成上下文或工具 | [Claude 官方网站](https://claude.com/) | 未记录发布日期 | 官方描述不代表任意工具都能实际兼容，也不保证授权成功 |
| F68 | Claude | 复用与协作机制 | Claude Pro 提供 Projects，可用于组织聊天和文档 | [Claude 官方网站](https://claude.com/) | 未记录发布日期 | Evidence 直接支持内容组织，不直接证明更具体的“复用机制”或实时共同编辑 |
| F76 | Claude | 复用与协作机制 | Claude 可通过 Team Account 与团队成员协作 | [Claude 官方网站](https://claude.com/) | 未记录发布日期 | 只支持 Team 协作范围，不证明实时同文档编辑或更具体的套餐权益 |
| F28 | Gemini | 工作成果创建与编辑 | Google AI Free 包含图像生成和编辑，以及 Deep Research、Gemini Live、Canvas、Gems 等能力 | [Gemini 官方订阅页](https://gemini.google/us/subscriptions/?hl=en) | 未记录发布日期 | 仅证明页面列出的功能，不根据 Canvas、Gems 等名称进一步推导其具体工作机制 |
| F89 | Gemini | 工具连接与任务执行 | Gemini 支持连接超过 40 个应用或服务，并在一次对话中完成相关任务 | [Gemini Release Notes](https://gemini.google/release-notes/) | 2026-10-13 | 不证明每个应用都具有相同操作权限，也不代表任务执行成功率 |
| F92 | Gemini | 复用与协作机制 | Gemini Skills 是用于特定任务的可复用指令集合，并被集成到 Gemini Chat | [Gemini Release Notes](https://gemini.google/release-notes/) | 2026-09-30 | Release Note 描述为全球 rollout，但不据此保证所有账户当前仍具备相同可用性 |
| F93 | Gemini | 复用与协作机制 | Gemini 可以从聊天中创建自定义 Skills，在匹配 Prompt 时自动运行，并组合多个 Skills | [Gemini Release Notes](https://gemini.google/release-notes/) | 2026-09-30 | 这里的复用机制不等同于多人共享或实时协作 |

---

## 日期说明

表格中的 **Evidence 日期** 优先使用 Frozen Evidence 中记录的 `event_date`。

对于 F60、F63、F64、F68、F76 和 F28，原始 Evidence 没有记录明确的 `event_date`，因此这里统一标记为：

**未记录发布日期**

这些 Evidence 的核查日期均为 **2026-10-20**，但核查日期不等于产品功能的首次发布日期，因此没有将其作为 Evidence 日期展示。

---

## Evidence ID 如何使用

简报中的事实性 Claim 会关联一个或多个 Evidence ID。

例如：

```text
Claude Projects 可用于组织聊天和文档
        ↓
       F68
        ↓
Claude 官方页面
        ↓
适用范围：Pro / 内容组织
        ↓
限制：不直接证明实时协作或特定复用机制
```

Evidence ID 的作用是让一条竞品结论能够回到对应的研究依据。

它并不自动代表：

- 该信息当前仍然有效；
- 来源能够支持更宽泛的产品判断；
- 该能力适用于所有套餐、地区或账户；
- Semantic Review 已经证明该事实绝对正确。

---

## Evidence Gap

如果当前选定 Evidence 无法支持某一个：

**Product × Dimension**

组合，CompetitorAI 不会为了填满比较表而自动补充结论。

系统会显示：

**Evidence Gap**

例如当前 MVP 中：

```text
ChatGPT
+
工具连接与任务执行
+
当前没有纳入足够的目标范围 Evidence

        ↓

Evidence Gap
```

这里的 Evidence Gap 表示：

> 当前研究输入不足以支持这一结论。

它并不表示：

> ChatGPT 不具备相关能力。

当前选择中没有纳入 ChatGPT 在这一维度的消费者 / 专业用户操作能力 Evidence，是因为已有相关 Evidence 主要涉及 Enterprise 管理控制，不属于本次比较范围。

---

## 为什么保留 Scope / Limitation

Evidence 能够支持的范围通常比模型可以生成的自然语言结论更窄。

例如 F68 能够直接支持：

> Claude Pro 提供 Projects，用于组织聊天和文档。

但不能仅凭这一条 Evidence 进一步得出：

> Claude 拥有完整的内容复用和实时协作机制。

因此，CompetitorAI 在 Evidence 记录中同时保留：

- 原始 Claim
- Source
- Confidence
- Research Scope
- Scope / Limitation

生成结果需要限制在 Evidence 实际能够支持的范围内。

---

## 当前 Evidence 覆盖情况

当前 12 条 Evidence 可以支持三个比较维度的基础分析，但仍存在明确的覆盖缺口：

- ChatGPT 的“工具连接与任务执行”在当前选择范围内缺少合适 Evidence；
- Claude 的文件编辑细节和实时同文档协作证据不足；
- Gemini 的多人协作证据不足；
- 当前没有对三款产品的任务成功率、质量、权限和套餐实际可用性进行实测。

因此，当前 MVP 不根据这些 Evidence 对三款产品进行整体优劣排名。

---

## 关于公开仓库

本页只公开当前 MVP 实际使用的 12 条 Evidence 索引。

完整 Frozen Evidence 数据集和原始研究环境没有全部包含在公开 Portfolio 仓库中。

公开这部分 Evidence 的主要目的是让示例中的：

```text
Claim
  ↓
Evidence ID
  ↓
Source
  ↓
Scope / Limitation
```

真正可以被查看和追溯。

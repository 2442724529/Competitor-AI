# Sample Competitive Brief

> 本示例基于项目中保存的 Frozen Evidence，用于展示 CompetitorAI 当前 MVP 的输出形式。  
> 示例反映的是实验时保存的 Evidence，不代表 ChatGPT、Claude 或 Gemini 当前最新产品状态。

完整 Evidence ID、来源、日期和适用范围见：

[查看 Evidence 索引](evidence-index.md)

---

## ChatGPT / Claude / Gemini 能力对比

| 比较维度 | ChatGPT | Claude | Gemini |
|---|---|---|---|
| 工作成果创建与编辑 | 支持 Slides 创建与直接编辑，包括文字、图片、形状和图表等内容。`F98` `F99` | 支持文件创建与代码执行；当前 Evidence 对更具体的编辑能力覆盖有限。`F60` | 当前 Evidence 支持图像生成与编辑能力。`F28` |
| 工具连接与任务执行 | **Evidence Gap**：当前选定 Evidence 不足以支持该维度的明确判断 | 支持连接 Slack、Google Workspace，并提供 Remote MCP Connector。`F63` `F64` | 支持连接应用或服务，并在单次对话中完成相关任务。`F89` |
| 复用与协作机制 | Slides 支持团队成员实时编辑同一 Deck，并留下共享评论。`F100` | Projects 可用于组织聊天与文档；Team Account 支持团队协作。`F68` `F76` | Skills 支持可复用指令、自定义创建、匹配触发及多个 Skills 组合使用。`F92` `F93` |

---

## Key Observations

### 1. 三款产品覆盖相似的工作场景，但实现方式不同

当前 Evidence 显示，三款产品都覆盖了部分内容创建、工具连接或协作相关能力，但具体产品形态并不相同。

- **ChatGPT**：当前选定 Evidence 主要覆盖 Slides 的创建、编辑与实时协作；
- **Claude**：覆盖文件创建、代码执行、外部服务连接，以及 Projects / Team 相关能力；
- **Gemini**：覆盖图像编辑、应用连接和 Skills 复用机制。

因此，竞品比较不能只判断“有没有某项功能”，还需要结合具体使用场景、产品形态和 Evidence 的适用范围进行理解。

**Evidence：** `F28` `F60` `F63` `F64` `F68` `F76` `F89` `F98` `F99` `F100` `F92` `F93`

---

### 2. Evidence Gap 本身也是研究结果

在“工具连接与任务执行”维度中，当前选定 Evidence 可以支持 Claude 和 Gemini 的部分能力，但不足以对 ChatGPT 做出同等范围的判断。

因此，该单元格被标记为：

**Evidence Gap**

这里的 Gap 表示：

> 当前研究输入不足以支持这一结论。

它不表示：

> ChatGPT 不具备相关能力。

CompetitorAI 在 Evidence 不足时保留缺口，而不是利用模型已有知识自动补齐比较结果。

---

## Product Hypothesis

> **Hypothesis — 尚未经过用户验证**

对于需要频繁进行 AI 产品竞品研究的产品经理，如果能够在阅读结论的同时看到对应 Evidence、来源范围和 Evidence Gap，可能会更容易判断：

- 哪些信息可以直接用于下一步分析；
- 哪些结论存在适用范围；
- 哪些内容仍需要进一步核查。

该内容属于产品设计假设，而不是由当前 Evidence 直接证明的事实。

---

## Evidence Notes

### ChatGPT

**F98**

支持 ChatGPT Slides 的创建场景，包括从对话、文件、提纲或示例 Deck 开始创建演示文稿。

**F99**

支持 Slides 中对文字、图片、形状和图表等元素进行直接编辑，或要求 ChatGPT 进行修改。

**F100**

支持团队成员实时编辑同一 Deck 并留下共享评论。

以上 Evidence 均只用于对应的 Slides 场景，不扩展为 ChatGPT 所有工作成果的通用能力。

---

### Claude

**F60**

支持 Claude Free 中的文件创建与代码执行能力。

**F63 / F64**

支持 Slack、Google Workspace 服务连接，以及 Remote MCP Connector 相关能力。

这些 Evidence 不用于推断连接后的具体读写权限、兼容性或任务执行成功率。

**F68**

直接支持 Claude Pro 的 Projects 用于组织聊天和文档。

这里不将“内容组织”进一步解释为已经被证明的完整复用机制。

**F76**

支持通过 Team Account 与团队成员协作，但不用于证明实时同文档编辑等更具体能力。

---

### Gemini

**F28**

支持 Google AI Free 中列出的图像生成与编辑能力。

不根据 Canvas、Gems 等功能名称进一步推导其具体工作机制。

**F89**

支持连接超过 40 个应用或服务，并在单次对话中完成相关任务。

当前 Evidence 不用于证明所有应用拥有相同权限或任务成功率。

**F92 / F93**

支持 Skills 作为可复用指令集合，以及自定义创建、匹配触发和多个 Skills 组合使用。

这里的复用机制不等同于多人实时协作。

---

## Confidence & Scope

当前示例中的 Evidence 均来自实验阶段保存的 Frozen Evidence。

因此：

- Evidence ID 可以追溯到本次实验使用的具体研究依据；
- 当前 Claim 被限制在对应 Evidence 能直接支持的范围内；
- Evidence 日期和核查日期不会混用；
- 没有 Evidence 支持的比较项会显示 Evidence Gap；
- 当前示例不代表相关功能目前仍保持相同的产品形态、套餐归属或地区可用性。

Evidence ID、官方来源及具体限制见：

[Evidence 索引](evidence-index.md)

---

## Review Status

本示例经过：

- Programmatic Checks
- Evidence ID / Scope 检查
- Markdown Table Validation
- Semantic Review

Semantic Review 仅作为质量控制的一层。

**Review PASS 不代表所有事实绝对正确，也不代表产品当前状态已经重新核实。**

详细审查示例见：

[Semantic Review](sample-review.md)

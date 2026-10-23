# CompetitorAI

CompetitorAI 是一个面向产品经理的竞品研究助手。

当前版本用于比较 ChatGPT、Claude 和 Gemini 在部分产品能力上的差异，并生成一份带有来源、证据编号和限制说明的竞品简报。

项目主要关注两个问题：

- 生成的结论能不能追溯到具体证据；
- 输出出现格式、引用或证据不足时，系统能不能明确识别出来。

---

## 当前功能

目前比较三个维度：

1. 工作成果创建与编辑
2. 工具连接与任务执行
3. 内容组织、复用与协作

输出内容包括：

- ChatGPT / Claude / Gemini 三方能力对照表
- 两条基于现有证据的观察
- 一条产品设计假设
- Evidence ID
- 来源和置信度
- 证据不足说明
- 检查和审查结果

当前版本使用固定的历史 Evidence 作为输入，因此示例结果不代表相关产品的最新状态。

---

## 工作流程

```text
Frozen Evidence
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

### Evidence Selection

从现有 Verified Evidence 中选择与当前比较任务相关的证据。

每条证据保留：

- Evidence ID
- 产品
- 对应比较维度
- 来源
- 原始主张
- 置信度
- 使用限制

当前 MVP 使用 12 条 Verified Evidence。

### Brief Generation

模型根据选定 Evidence 生成简报。

事实主张需要关联对应 Evidence ID；如果现有证据不足，则直接标记为证据不足，不自动补全。

### Programmatic Checks

生成后会进行确定性检查，包括：

- Evidence ID 是否有效
- 引用是否属于对应产品和比较维度
- Markdown 表格结构是否正确
- 必要字段是否存在
- 正文长度是否符合要求
- 证据缺口是否明确展示

### Semantic Review

另外进行一次语义审查，检查：

- Evidence 是否能够支持对应主张
- 是否存在过度概括
- 产品或套餐归属是否有问题
- 是否遗漏重要限制
- 产品假设是否和事实内容区分开

语义审查作为辅助检查使用，不代表事实一定正确。

---

## 示例输出

最终简报主要包含以下内容：

| 维度 | ChatGPT | Claude | Gemini |
|---|---|---|---|
| 创建与编辑 | Evidence | Evidence | Evidence |
| 工具与任务 | Evidence Gap | Evidence | Evidence |
| 复用与协作 | Evidence | Evidence | Evidence |

同时附带：

- Evidence ID
- 来源
- 置信度
- 适用范围
- Evidence Gap
- Review Status

示例简报：

`examples/sample-brief.md`

审查结果：

`examples/sample-review.md`

---

## 验证结果

当前版本已经完成一次真实简报生成和一次单独的语义审查。

目前完成：

- 12 条 Verified Evidence 输入
- 一次真实简报生成
- 一次独立语义审查
- 30 项相关离线测试
- Fact ID 检查
- 引用范围检查
- Markdown 表格检查
- 长度检查
- Evidence Gap 检查
- 确定性重放验证

最终候选简报正文约 1,804 字符。

在测试过程中曾发现 Markdown 表格行之间出现空行的问题。原有检查没有识别这一情况，后续修复了表格生成逻辑，并增加相应的回归测试。

修复后使用原始模型产物重新渲染，没有重新生成内容。

---

## 项目结构

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

## 技术栈

- Python
- ByteDance DeerFlow 2.0
- DeepSeek API
- Unittest
- Ruff

---

## 当前边界

这个项目目前是一个可运行的 MVP，并不是生产级产品。

当前还没有完成：

- 实时竞品搜索
- 最新产品信息验证
- 真实用户测试
- 大规模事实准确率评估
- 生产环境部署
- 多模型对比评测

部分历史 Evidence 还存在套餐资格、地域限制和来源脚注不完整的问题，因此这些内容在示例中会明确标注限制。

---

## 复现说明

完整运行依赖：

- DeerFlow 2.0 环境
- 原始冻结 Evidence
- 模型 API 配置

公开仓库不会包含：

- API Key
- 私有配置
- 本地用户路径
- 敏感运行日志

README 中展示的示例主要用于说明当前 MVP 的工作方式和验证结果。

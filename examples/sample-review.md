# Sample Semantic Review

本文件展示 CompetitorAI 当前 MVP 的语义审查结果示例。

审查目标不是判断报告“写得好不好”，而是检查：

- Claim 是否得到对应 Evidence 支持
- 是否存在过度概括
- 产品或套餐归属是否有问题
- 是否遗漏重要限制
- Hypothesis 是否被误写成事实

> 本示例基于项目保存的 Frozen Evidence，不代表相关产品当前最新状态。

---

## Review Summary

**Targeted Review Status: PASS**

**Review Scope：8 个修改及受影响单元**

本次审查只针对内容收尾阶段发生修改或受到修改影响的部分进行检查。

在当前 Frozen Evidence 和本次审查范围内，8 个受影响单元均未发现需要判定为 FAIL 的语义问题。

需要特别说明：

> 本次 PASS 只适用于上述审查范围，不代表整篇 Competitive Brief 被重新认证，也不代表所有事实绝对正确。

Semantic Review 是当前质量控制流程中的一层，最终结果仍需要结合 Evidence Scope、程序化检查和必要的人工复核进行理解。

---

## Review Cases

### 1. ChatGPT — 创建与编辑

**Claim**

当前 Evidence 支持 Slides 创建、编辑及相关协作能力。

**Evidence**

`F98` `F99` `F100`

**Result**

`SUPPORTED`

**Reason**

对应 Evidence 可以支持当前简报中的能力描述，且没有进一步扩展到未被 Evidence 证明的范围。

---

### 2. ChatGPT — 工具连接与任务执行

**Claim**

当前选定 Evidence 不足以对该维度做出明确判断。

**Result**

`EVIDENCE GAP`

**Reason**

当前 Selection 中没有足够 Evidence 支持这一单元。

该结果不代表 ChatGPT 不具备相关能力，只表示当前研究输入不足。

---

### 3. Claude — 文件创建与执行

**Claim**

Claude 的当前 Evidence 支持文件创建和代码执行能力。

**Evidence**

`F60`

**Result**

`SUPPORTED`

**Reason**

Claim 与冻结 Evidence 中记录的能力范围一致。

---

### 4. Claude — 工具连接

**Claim**

Claude 支持部分服务连接及 Remote MCP。

**Evidence**

`F63` `F64`

**Result**

`SUPPORTED`

**Reason**

Evidence 可以支持当前描述。

没有将这些 Evidence 扩展为“支持所有第三方服务”等更宽泛结论。

---

### 5. Claude — 内容组织

**Claim**

Projects 可以用于组织聊天和文档。

**Evidence**

`F68`

**Result**

`SUPPORTED`

**Reason**

Evidence 直接支持内容组织能力。

原版本曾将该 Evidence 延伸为“复用机制”，但这一表达超出了 Evidence 直接支持的范围。

最终版本已调整为：

> Evidence 直接支持内容组织；特定复用机制未被当前 Evidence 证明。

---

### 6. Claude — Team 协作

**Claim**

当前 Evidence 支持 Team 场景中的协作范围。

**Evidence**

`F76`

**Result**

`SUPPORTED WITH LIMITATION`

**Reason**

Evidence 可以支持团队协作相关描述，但不能用于证明：

- 实时同文档编辑
- 更具体的套餐权益
- 当前最新产品状态

因此相关限制需要保留。

---

### 7. Gemini — 工具连接与任务执行

**Claim**

当前 Evidence 支持应用连接及对话内任务相关能力。

**Evidence**

`F89`

**Result**

`SUPPORTED`

**Reason**

Claim 与当前冻结 Evidence 的支持范围一致。

但语言、地区及当前可用性仍需要单独核实。

---

### 8. Gemini — 可复用指令

**Claim**

当前 Evidence 支持可复用指令以及相关创建和触发机制。

**Evidence**

`F92` `F93`

**Result**

`SUPPORTED WITH LIMITATION`

**Reason**

当前 Evidence 支持该机制本身。

但部分来源脚注没有完整保存在 Frozen Evidence 中，因此不能进一步扩大适用范围。

---

## Hypothesis Review

**Content Type**

`PRODUCT HYPOTHESIS`

**Result**

`NOT_FACTUAL`

产品设计假设被明确标记为未经验证的提案，没有被包装成竞品已经具备的能力。

因此该内容不需要 Evidence 证明其为事实，但必须与事实观察明确分开。

---

## Scope Notes

本次审查仍有以下边界：

- 使用的是固定 Frozen Evidence
- 不验证产品当前实时可用性
- 不代表进行了全量事实核查
- 不代表模型审查能够发现所有错误
- PASS 仅适用于本次审查范围

因此：

> Semantic Review 是质量控制的一层，而不是最终事实真相来源。

更完整的验证范围见：

`../docs/validation-and-limitations.md`

# Source Code

该目录保留 CompetitorAI MVP 的核心实现代码。

当前公开版本主要用于展示：

- Evidence 输入与选择逻辑
- Evidence ID 和引用范围检查
- Evidence Gap 处理
- Markdown 简报渲染
- 输出格式与长度检查
- MVP 离线验收逻辑

核心实现：

`v3/mvp_brief.py`

该代码来自原 CompetitorAI / DeerFlow V3 项目环境，并经过实际运行和回归测试。

## Runtime Dependencies

完整运行仍依赖原项目中的部分组件，包括：

- `v3.frozen_downstream`
- Frozen Evidence 输入
- `mvp_selection.json`
- DeerFlow 2.0 项目环境

因此，本仓库中的 `src` 目录主要用于展示已经验证过的核心实现，而不是一个完全独立安装的 Python package。

公开仓库不包含 API Key、私有配置、本地路径或敏感运行数据。

完整的产品流程和验证范围请参考：

- `../docs/architecture.md`
- `../docs/validation-and-limitations.md`

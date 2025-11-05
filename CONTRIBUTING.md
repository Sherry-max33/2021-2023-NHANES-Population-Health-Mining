# Contributing (团队协作约定)

## 分支策略
- `main`：受保护，不直接推。
- `feature/<模块>-<姓名缩写>`：功能开发分支（例如 `feature/preprocess-sw`）。
- `fix/<问题>-<姓名缩写>`：修复分支。

## 提交流程
1. 从最新 `main` 切分支：`git checkout -b feature/preprocess-sw`
2. 开发 & 自测，提交规范信息：`[preprocess] impute BMI; add unit tests`
3. 发起 PR：填写描述、复现方法、影响范围、截图。
4. 至少 1 名同学 Review 通过后 `Merge` 到 `main`。

## 代码风格
- Python：PEP8；变量名清晰；函数注释（docstring）。
- Notebook：输出在提交前清理（推荐 `nbstripout`）。
- 数据/模型：不提交到仓库，遵循 `.gitignore`。

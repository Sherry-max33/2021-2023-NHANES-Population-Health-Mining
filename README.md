# Data Mining Project

A clean, minimal, and **team-friendly** template for your course project.

## Overview
- **Task**: (fill: classification / regression / clustering / association rules)
- **Dataset**: (briefly describe; source & license)
- **Status**: environment scaffolded on 2025-11-05.

## Repo Layout
```
data-mining-project/
├─ README.md
├─ LICENSE                    # optional
├─ .gitignore
├─ environment.yml           # or requirements.txt
├─ Makefile                  # optional, one-command workflows
├─ src/                      # reusable code (import from notebooks)
│  ├─ __init__.py
│  ├─ data.py                # data I/O, download, basic checks
│  ├─ features.py            # cleaning / feature engineering
│  ├─ models.py              # train, predict, persist
│  ├─ metrics.py             # metrics / plots
│  └─ utils.py
├─ notebooks/                # storytelling + visuals
│  ├─ 00_eda.ipynb           # (you add later)
│  ├─ 10_preprocess.ipynb
│  ├─ 20_model_baseline.ipynb
│  ├─ 30_model_tuning.ipynb
│  └─ 99_report.ipynb
├─ experiments/              # each run saves params/metrics/figures
├─ reports/
│  ├─ figures/
│  └─ report.pdf             # (export your final report here)
├─ data/
│  ├─ README.md              # how to get / regenerate data
│  ├─ raw/                   # never commit
│  ├─ external/              # 3rd-party static resources
│  └─ processed/             # clean/merged tables (not committed)
├─ configs/
│  └─ default.yml            # paths + common hyper-params
└─ docs/
   └─ proposal.md            # paste your proposal & findings
```

## Quickstart
```bash
# 1) (Conda) create env
conda env create -f environment.yml
conda activate dm-proj

# 2) (Optional) strip notebook outputs on commit
pip install nbstripout
nbstripout --install

# 3) Project workflow (examples)
python -m src.data --check
python -m src.features --build
python -m src.models --train --config configs/default.yml
python -m src.models --eval
```

## Where do I put things?
- **Your merged tables (已融合的表格)** → `data/processed/` （不要提交到 Git）。
- **原始表** → `data/raw/`（不要提交到 Git）。
- **用于合并/清洗的脚本** → 放到 `src/data.py`/`src/features.py` 并在 `notebooks/10_preprocess.ipynb` 调用。
- **实验产物（metrics、图）** → `experiments/<日期_描述>/` 与 `reports/figures/`。

## Collaboration (团队协作)
- 分支：`main` 受保护；功能分支用 `feature/<模块>-<姓名缩写>`（例：`feature/preprocess-sw`）
- 提交信息：`[preprocess] handle missing BMI`
- 开 PR：描述变更、如何复现、影响范围，1 人 approve 后 **merge**（不是 “mulch” 😄）。

## Reproducibility
- 所有路径在 `configs/default.yml` 里集中配置。
- 数据与模型文件不进 Git；如需版本化请用 Git LFS/DVC（可选）。

---
> Tip: 上交或展示前，可把关键图/表导出到 `reports/figures/` 并在 README 中展示 1–2 张代表图。

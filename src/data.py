import argparse
from pathlib import Path
import re
import pandas as pd
import numpy as np

from .utils import get_paths, ensure_dirs

# ---------- 配置：需要的模块文件名 ----------
MODULE_FILES = [
    "DEMO_L.XPT", "BMX_L.XPT", "BPXO_L.XPT",
    "GHB_L.XPT", "GLU_L.XPT",
    "SMQ_L.XPT", "PAQ_L.XPT", "SLQ_L.XPT",
    "DIQ_L.XPT", "INQ_L.XPT", "DBQ_L.XPT",
    "HIQ_L.XPT", "HSQ_L.XPT", "HUQ_L.XPT",
    "OCQ_L.XPT", "ALQ_L.XPT", "AGP_L.XPT",
]

# ---------- 列映射（你的命名） ----------
COLS_MAP = {
    "SEQN": "id",
    "RIDAGEYR": "age",
    "RIAGENDR": "gender",
    "RIDRETH3": "race",
    "DMDEDUC2": "education",
    "INDFMPIR": "income_poverty_ratio",

    "BMXWT": "weight_kg",
    "BMXHT": "height_cm",
    "BMXBMI": "bmi",

    "BPXOSY1": "sbp",
    "BPXODI1": "dbp",

    "LBXGH": "a1c",
    "LBXGLU": "glucose",

    "SMQ020": "smoking_current",
    "SMQ040": "smoking_ever",

    "PAD820": "physical_activity_freq",
    "SLD012": "sleep_hours",

    "DIQ010": "diabetes_self_report",
    "HIQ011": "has_health_insurance",
    "HUQ010": "doctor_visit_12m",
}

# ---------- 分类值映射 ----------
GENDER_MAP = {1: "Male", 2: "Female"}
RACE_MAP = {
    1: "Mexican American", 2: "Other Hispanic",
    3: "Non-Hispanic White", 4: "Non-Hispanic Black",
    6: "Non-Hispanic Asian", 7: "Other Race / Multi",
}
EDU_MAP = {
    1: "<9th grade", 2: "9-11th grade", 3: "High school/GED",
    4: "Some college/AA", 5: "College graduate or above",
}
YESNO_MAP = {1: "Yes", 2: "No", 7: "Refused", 9: "Don't know"}
DIAB_MAP = {1: "Yes", 2: "No", 3: "Borderline", 7: "Refused", 9: "Don't know"}
INS_MAP  = {1: "Insured", 2: "Not insured", 7: "Refused", 9: "Don't know"}
VISIT_MAP= {1: "Yes", 2: "No", 7: "Refused", 9: "Don't know"}

def _read_xpt(fp: Path) -> pd.DataFrame:
    # pandas.read_sas 支持 XPORT；列名保持大写更容易对齐
    return pd.read_sas(fp, format="xport")

def _load_all_raw(raw_dir: Path) -> dict:
    loaded = {}
    for name in MODULE_FILES:
        p = raw_dir / name
        if not p.exists():
            print(f"[warn] missing file: {p}")
            continue
        df = _read_xpt(p)
        # 统一列名为大写字符串，避免大小写/bytes 问题
        df.columns = [str(c).upper() for c in df.columns]
        loaded[name] = df
        print(f"[data] loaded {name} -> shape={df.shape}")
    if "DEMO_L.XPT" not in loaded:
        raise FileNotFoundError("DEMO_L.XPT 必须存在（包含主键 SEQN）")
    return loaded

def _merge_on_seqn(tables: dict) -> pd.DataFrame:
    # 以 DEMO 为基表（覆盖面最大）
    nhanes = tables["DEMO_L.XPT"].copy()
    for name, df in tables.items():
        if name == "DEMO_L.XPT":
            continue
        if "SEQN" not in df.columns:
            print(f"[warn] {name} 没有 SEQN，跳过")
            continue
        nhanes = nhanes.merge(df, on="SEQN", how="left")
    print(f"[data] merged shape: {nhanes.shape}")
    return nhanes

def _select_and_rename(nhanes: pd.DataFrame) -> pd.DataFrame:
    # 只保留映射里有的列，缺失的列会被忽略并提示
    missing = [c for c in COLS_MAP.keys() if c not in nhanes.columns]
    if missing:
        print(f"[warn] 下列列在合并后不存在，将被忽略: {missing}")
    keep = [c for c in COLS_MAP.keys() if c in nhanes.columns]
    out = nhanes[keep].rename(columns=COLS_MAP)
    return out

def _apply_value_maps(df: pd.DataFrame) -> pd.DataFrame:
    # 分类值映射
    if "gender" in df.columns: df["gender"] = df["gender"].map(GENDER_MAP)
    if "race" in df.columns: df["race"] = df["race"].map(RACE_MAP)
    if "education" in df.columns: df["education"] = df["education"].map(EDU_MAP)
    if "smoking_current" in df.columns: df["smoking_current"] = df["smoking_current"].map(YESNO_MAP)
    if "smoking_ever" in df.columns: df["smoking_ever"] = df["smoking_ever"].map(YESNO_MAP)
    if "diabetes_self_report" in df.columns: df["diabetes_self_report"] = df["diabetes_self_report"].map(DIAB_MAP)
    if "has_health_insurance" in df.columns: df["has_health_insurance"] = df["has_health_insurance"].map(INS_MAP)
    if "doctor_visit_12m" in df.columns: df["doctor_visit_12m"] = df["doctor_visit_12m"].map(VISIT_MAP)
    return df

def _derive_insurance_type(nhanes_full: pd.DataFrame, slim_df: pd.DataFrame) -> pd.DataFrame:
    """
    从原始合并表中提取 HIQ032 家族字段，推断保险类型，并合并到精简表（slim_df）里。
    规则与你 notebook 代码一致：1=private；{2,3,4,5,6,8,9}=public
    """
    # 收集 HIQ032* 列（不同模块可能带后缀）
    hiq_cols = [c for c in nhanes_full.columns if str(c).upper().startswith("HIQ032")]
    if not hiq_cols:
        slim_df["insurance_type"] = "Unknown"
        return slim_df

    # 按基础名（HIQ032A..I）去重，优先非空更多的列
    bases = {}
    pat = re.compile(r"^(HIQ032[ABCDEFGHI])(?:_.+)?$", re.I)
    for c in hiq_cols:
        m = pat.match(str(c))
        if m:
            base = m.group(1).upper()
            s = pd.to_numeric(nhanes_full[c], errors="coerce")
            if base not in bases or s.notna().sum() > bases[base].notna().sum():
                bases[base] = s
    hiq32 = pd.DataFrame(bases, index=nhanes_full.index) if bases else pd.DataFrame(index=nhanes_full.index)

    # has_any: 有保险（HIQ011=Insured 或原值=1）
    has_any = (slim_df.get("has_health_insurance") == "Insured") | (nhanes_full.get("HIQ011", pd.Series(index=nhanes_full.index)).eq(1))

    private_flag = hiq32.eq(1).any(axis=1).fillna(False).to_numpy() if not hiq32.empty else np.zeros(len(slim_df), bool)
    public_codes = {2,3,4,5,6,8,9}
    public_flag  = hiq32.isin(public_codes).any(axis=1).fillna(False).to_numpy() if not hiq32.empty else np.zeros(len(slim_df), bool)

    private_only = has_any & private_flag & np.logical_not(public_flag)
    public_only  = has_any & np.logical_not(private_flag) & public_flag
    both         = has_any & private_flag & public_flag
    uninsured    = (slim_df.get("has_health_insurance") == "Not insured") | (nhanes_full.get("HIQ011", pd.Series(index=nhanes_full.index)).eq(2))

    slim_df["insurance_type"] = np.select(
        [private_only, public_only, both, uninsured],
        ["Private only", "Public only", "Both", "Uninsured"],
        default="Unknown"
    )
    return slim_df

def build():
    """
    主入口：读取 raw XPT → 按 SEQN 合并 → 精选/重命名列 → 映射分类值 → 推断保险类型 → 保存到 data/processed/
    输出：data/processed/merged.csv 和 merged.parquet
    """
    paths = get_paths()
    raw_dir = Path(paths["raw_dir"])
    processed_dir = Path(paths["processed_dir"])
    ensure_dirs([processed_dir])

    print(f"[data] raw_dir={raw_dir}")
    tables = _load_all_raw(raw_dir)
    merged_full = _merge_on_seqn(tables)

    # 精简并重命名列
    slim = _select_and_rename(merged_full)
    slim = _apply_value_maps(slim)

    # 推导 insurance_type
    slim = _derive_insurance_type(merged_full, slim)

    # 保存
    csv_path = processed_dir / "merged.csv"
    pq_path  = processed_dir / "merged.parquet"
    slim.to_csv(csv_path, index=False)
    try:
        slim.to_parquet(pq_path, index=False)  # 需要 pyarrow 或 fastparquet；没有也没关系
        print(f"[data] saved: {csv_path.name}, {pq_path.name}")
    except Exception as e:
        print(f"[warn] parquet 未保存（可安装 pyarrow）：{e}")
        print(f"[data] saved: {csv_path.name}")

    print(f"[data] final shape: {slim.shape}")

def check():
    paths = get_paths()
    ensure_dirs([paths["raw_dir"], paths["processed_dir"]])
    print("[data] folders ready:", paths["raw_dir"], paths["processed_dir"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
    if args.build:
        build()
import argparse
from pathlib import Path
import pandas as pd

from .utils import get_paths, ensure_dirs

def build():
    paths = get_paths()
    ensure_dirs([paths['processed_dir']])
    # Example: merge pre-processed tables (user to replace with real logic)
    # df1 = pd.read_csv(Path(paths['processed_dir']) / "table1.csv")
    # df2 = pd.read_csv(Path(paths['processed_dir']) / "table2.csv")
    # df = df1.merge(df2, on="id", how="left")
    # df.to_parquet(Path(paths['processed_dir']) / "training.parquet", index=False)
    print("[features] placeholder: add your cleaning/feature engineering steps here.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    if args.build:
        build()

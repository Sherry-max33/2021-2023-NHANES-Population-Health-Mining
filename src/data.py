import argparse
from pathlib import Path
import pandas as pd

from .utils import ensure_dirs, get_paths

def check():
    paths = get_paths()
    ensure_dirs([paths['raw_dir'], paths['processed_dir']])
    print("[data] folders ready:", paths['raw_dir'], paths['processed_dir'])
    # Example sanity check: list files
    raw_files = list(Path(paths['raw_dir']).glob("*"))
    print(f"[data] raw files: {len(raw_files)}")
    for f in raw_files[:5]:
        print(" -", f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()

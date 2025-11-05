import yaml
from pathlib import Path

def get_paths():
    # centralize common paths; keep in sync with configs/default.yml
    return {
        "data_dir": "data",
        "raw_dir": "data/raw",
        "processed_dir": "data/processed",
        "external_dir": "data/external",
        "experiments_dir": "experiments",
        "reports_dir": "reports"
    }

def ensure_dirs(dirs):
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)

def load_config(path: str):
    with open(path, "r") as f:
        return yaml.safe_load(f)

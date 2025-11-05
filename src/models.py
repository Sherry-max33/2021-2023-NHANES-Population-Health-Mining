import argparse, json
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score

from .utils import get_paths, ensure_dirs, load_config

def train(config_path: str):
    cfg = load_config(config_path)
    paths = get_paths()
    ensure_dirs([paths['experiments_dir']])

    # NOTE: replace with your processed dataset path
    data_path = Path(paths['processed_dir']) / "training.parquet"
    if not data_path.exists():
        print(f"[models] Missing {data_path}. Please create processed data first.")
        return

    df = pd.read_parquet(data_path)
    y = df['target']             # <-- rename to your label column
    X = df.drop(columns=['target'])

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=cfg['experiment']['seed'])

    # Minimal baseline model (LogReg)
    model = LogisticRegression(**cfg['model'].get('params', {}))
    model.fit(X_tr, y_tr)

    proba = model.predict_proba(X_te)[:, 1] if hasattr(model, "predict_proba") else None
    preds = (proba >= 0.5).astype(int) if proba is not None else model.predict(X_te)

    metrics = {
        "roc_auc": float(roc_auc_score(y_te, proba)) if proba is not None else None,
        "classification_report": classification_report(y_te, preds, output_dict=True)
    }

    # Save run
    run_dir = Path(paths['experiments_dir']) / "baseline"
    run_dir.mkdir(parents=True, exist_ok=True)
    with open(run_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print("[models] training done. Metrics saved to", run_dir / "metrics.json")

def eval_model():
    print("[models] eval placeholder: load a saved model and evaluate on holdout / CV.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", action="store_true")
    parser.add_argument("--eval", action="store_true")
    parser.add_argument("--config", type=str, default="configs/default.yml")
    args = parser.parse_args()

    if args.train:
        train(args.config)
    if args.eval:
        eval_model()

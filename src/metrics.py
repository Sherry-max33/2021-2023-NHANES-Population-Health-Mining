from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score

def classification_metrics(y_true, y_pred, y_proba=None):
    acc = accuracy_score(y_true, y_pred)
    prec, rec, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='binary', zero_division=0)
    auc = roc_auc_score(y_true, y_proba) if y_proba is not None else None
    return {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1, "roc_auc": auc}

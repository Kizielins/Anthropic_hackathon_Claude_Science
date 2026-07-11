
"""Subject-grouped evaluation harness for CST transition prediction (PRJEB37731)."""
import numpy as np, pandas as pd
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import roc_auc_score, average_precision_score, balanced_accuracy_score, brier_score_loss

META = ("subject","cur_CST","y_transition","y_into_IV","has_prior_day")

def feature_cols(D):
    return [c for c in D.columns if c not in META]

def grouped_folds(y, groups, n=5, seed=42):
    sgkf = StratifiedGroupKFold(n_splits=n, shuffle=True, random_state=seed)
    return list(sgkf.split(np.zeros(len(y)), y, groups))

def eval_probs(y_true, p, name):
    return {"model":name,
            "AUROC":roc_auc_score(y_true,p) if np.std(p)>0 else np.nan,
            "AUPRC":average_precision_score(y_true,p),
            "balanced_acc":balanced_accuracy_score(y_true,(np.asarray(p)>=0.5).astype(int)),
            "brier":brier_score_loss(y_true,np.clip(p,0,1)),
            "n":len(y_true),"pos_rate":float(np.mean(y_true))}

def target_frame(D, target):
    return D if target=="y_transition" else D[D.y_into_IV.notna()].copy()

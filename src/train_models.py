
import numpy as np, pandas as pd, json, warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, average_precision_score, balanced_accuracy_score, brier_score_loss, roc_curve, precision_recall_curve
from xgboost import XGBClassifier

D=pd.read_parquet("modeling_dataset.parquet")
META=("subject","cur_CST","y_transition","y_into_IV","has_prior_day")
feat_cols=[c for c in D.columns if c not in META]

def folds(y,g,n=5,seed=42):
    return list(StratifiedGroupKFold(n_splits=n,shuffle=True,random_state=seed).split(np.zeros(len(y)),y,g))

def make_model(kind):
    if kind=="enet":
        return Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler()),
            ("lr",LogisticRegression(penalty="elasticnet",solver="saga",l1_ratio=0.5,C=0.5,
                                     max_iter=5000,class_weight="balanced"))])
    if kind=="rf":
        return Pipeline([("imp",SimpleImputer(strategy="median")),
            ("rf",RandomForestClassifier(n_estimators=400,max_depth=None,min_samples_leaf=5,
                                         class_weight="balanced_subsample",random_state=0,n_jobs=-1))])
    if kind=="xgb":
        return Pipeline([("imp",SimpleImputer(strategy="median")),
            ("xgb",XGBClassifier(n_estimators=300,max_depth=3,learning_rate=0.05,subsample=0.8,
                                 colsample_bytree=0.5,reg_lambda=2.0,random_state=0,n_jobs=-1,
                                 eval_metric="logloss"))])

def cv_eval(target):
    df=D if target=="y_transition" else D[D.y_into_IV.notna()].copy()
    y=df[target].astype(int).values; g=df.subject.values
    X=df[feat_cols].values
    # covariate+cur_CST baseline features
    cov=["host_age","host_bmi","cycle_day"]+[c for c in df.columns if c.startswith("bc_")]
    Xc=pd.concat([df[cov].reset_index(drop=True),pd.get_dummies(df["cur_CST"],prefix="cst").reset_index(drop=True)],axis=1)
    fl=folds(y,g,5)
    rows=[]; oof={}
    # baselines
    oof_marg=np.zeros(len(y)); oof_pers=np.zeros(len(y)); oof_cov=np.zeros(len(y))
    for tr,te in fl:
        oof_marg[te]=y[tr].mean()
        base=Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler()),
                       ("lr",LogisticRegression(max_iter=2000,class_weight="balanced"))])
        base.fit(Xc.values[tr],y[tr]); oof_cov[te]=base.predict_proba(Xc.values[te])[:,1]
    oof["marginal"]=oof_marg; oof["persistence"]=oof_pers; oof["cov_curCST"]=oof_cov
    # full-profile models
    for kind in ["enet","rf","xgb"]:
        p=np.zeros(len(y))
        for tr,te in fl:
            mdl=make_model(kind); mdl.fit(X[tr],y[tr]); p[te]=mdl.predict_proba(X[te])[:,1]
        oof[kind]=p
    # per-fold metrics (for CIs) + pooled
    def metrics(name,p):
        # per-fold
        aurocs=[]; auprcs=[]
        for tr,te in fl:
            if np.std(p[te])>0 and len(np.unique(y[te]))>1:
                aurocs.append(roc_auc_score(y[te],p[te])); auprcs.append(average_precision_score(y[te],p[te]))
        return {"model":name,"target":target,
                "AUROC":float(roc_auc_score(y,p)) if np.std(p)>0 else np.nan,
                "AUPRC":float(average_precision_score(y,p)),
                "balanced_acc":float(balanced_accuracy_score(y,(p>=0.5).astype(int))),
                "brier":float(brier_score_loss(y,np.clip(p,0,1))),
                "AUROC_fold_mean":float(np.mean(aurocs)) if aurocs else np.nan,
                "AUROC_fold_std":float(np.std(aurocs)) if aurocs else np.nan,
                "AUPRC_fold_mean":float(np.mean(auprcs)) if auprcs else np.nan,
                "AUPRC_fold_std":float(np.std(auprcs)) if auprcs else np.nan,
                "n":int(len(y)),"pos_rate":float(y.mean())}
    for name,p in oof.items(): rows.append(metrics(name,p))
    # save OOF preds for best model curves
    np.savez(f"oof_{target}.npz", y=y, **{k:v for k,v in oof.items()})
    return rows

allrows=[]
for tgt in ["y_transition","y_into_IV"]:
    allrows+=cv_eval(tgt)
res=pd.DataFrame(allrows)
res.to_csv("model_results.csv",index=False)
print(res.round(3).to_string(index=False))

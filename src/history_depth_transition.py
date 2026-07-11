# History-depth sweep — TRANSITION & DIRECTION targets (Analysis S3)
# Reconstructed from artifact lineage. Run from repo root.

import pandas as pd
import numpy as np
from itertools import product
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GroupKFold, cross_val_predict
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

cst = pd.read_csv('data/cst_calls.csv')
mod = pd.read_parquet('data/modeling_dataset.parquet')

cst_sorted = cst.sort_values(['subject','day']).reset_index(drop=True)
idx = {(r.subject, r.day): i for i,r in cst_sorted.iterrows()}

lab = cst[cst['next_CST_val'].notna() & (cst['gap_days']==1)]

cst_ord = {'I':0,'II':1,'V':1,'III':2,'IV':3}

def build_dataset(k):
    rows = []
    for _, r in lab.iterrows():
        subj, t = r.subject, r.day
        hist = []
        ok = True
        for j in range(1, k+1):
            key = (subj, t-j)
            if key not in idx:
                ok = False; break
            hist.append(cst_sorted.loc[idx[key]])
        if not ok:
            continue
        rec = dict(subject=subj, day=t, y_transition=int(r.transitions_val),
                   cur_CST=r.CST_val_coarse, next_CST=r.next_CST_val,
                   L_iners=r.L_iners, L_crispatus=r.L_crispatus,
                   Gardnerella=r.Gardnerella, shannon=r.shannon,
                   host_age=r.host_age, host_bmi=r.host_bmi, birth_control=r.birth_control)
        if k >= 1:
            liners_win = [r.L_iners] + [h.L_iners for h in hist]
            for j in range(1, k+1):
                rec[f'L_iners_lag{j}'] = hist[j-1].L_iners
                rec[f'cst_ord_lag{j}'] = cst_ord.get(hist[j-1].CST_val_coarse, 2)
            rec['liners_runmean'] = np.mean(liners_win)
            rec['liners_runvar'] = np.var(liners_win)
            rec['liners_delta1'] = r.L_iners - hist[0].L_iners
            seq = [h.CST_val_coarse for h in reversed(hist)] + [r.CST_val_coarse]
            rec['recent_transitions'] = sum(1 for a,b in zip(seq[:-1], seq[1:]) if a!=b)
            run3 = 0
            for c in [r.CST_val_coarse] + [h.CST_val_coarse for h in hist]:
                if c=='III': run3 += 1
                else: break
            rec['consec_days_III'] = run3
        rows.append(rec)
    return pd.DataFrame(rows)

def feature_cols(d, k):
    base_num = ['L_iners','L_crispatus','Gardnerella','shannon','host_age','host_bmi']
    hist_num = []
    if k>=1:
        hist_num = [f'L_iners_lag{j}' for j in range(1,k+1)] + \
                   [f'cst_ord_lag{j}' for j in range(1,k+1)] + \
                   ['liners_runmean','liners_runvar','liners_delta1','recent_transitions','consec_days_III']
    num = base_num + hist_num
    cat = ['cur_CST','birth_control']
    return num, cat

def make_pipe(model='logit'):
    def build(num, cat):
        pre = ColumnTransformer([
            ('num', Pipeline([('imp',SimpleImputer(strategy='median')),('sc',StandardScaler())]), num),
            ('cat', Pipeline([('imp',SimpleImputer(strategy='most_frequent')),
                              ('oh', __import__('sklearn.preprocessing',fromlist=['OneHotEncoder']).OneHotEncoder(handle_unknown='ignore'))]), cat),
        ])
        if model=='logit':
            clf = LogisticRegression(penalty='l2', C=0.5, max_iter=2000, class_weight='balanced')
        else:
            clf = HistGradientBoostingClassifier(max_depth=3, max_iter=200, learning_rate=0.05,
                                                 min_samples_leaf=20, l2_regularization=1.0, random_state=0)
        return Pipeline([('pre',pre),('clf',clf)])
    return build

def oof_predict(d, k, model='logit', n_splits=5):
    num, cat = feature_cols(d, k)
    X = d[num+cat]; y = d['y_transition'].values; groups = d['subject'].values
    build = make_pipe(model)
    pipe = build(num, cat)
    gkf = GroupKFold(n_splits=n_splits)
    oof = cross_val_predict(pipe, X, y, cv=gkf, groups=groups, method='predict_proba')[:,1]
    return oof, y, groups

rng = np.random.default_rng(42)

def subject_bootstrap_ci(oof, y, groups, metric_fn, n_boot=2000):
    subs = np.unique(groups)
    stats = []
    for _ in range(n_boot):
        samp = rng.choice(subs, size=len(subs), replace=True)
        mask_idx = np.concatenate([np.where(groups==s)[0] for s in samp])
        yy, pp = y[mask_idx], oof[mask_idx]
        if len(np.unique(yy))<2:
            continue
        stats.append(metric_fn(yy, pp))
    return np.percentile(stats, 2.5), np.percentile(stats, 97.5)

datasets = {k: build_dataset(k) for k in range(6)}
common_subset_pairs = set(zip(datasets[5]['subject'], datasets[5]['day']))

results = []
for model in ['logit','gbt']:
    for k in range(6):
        d = datasets[k]
        oof, y, groups = oof_predict(d, k, model=model)
        auroc = roc_auc_score(y, oof); auprc = average_precision_score(y, oof)
        lo_roc, hi_roc = subject_bootstrap_ci(oof, y, groups, roc_auc_score)
        lo_prc, hi_prc = subject_bootstrap_ci(oof, y, groups, average_precision_score)
        results.append(dict(model=model, k=k, sample='native', n_pairs=len(d), n_subj=d['subject'].nunique(),
                            n_transitions=int(y.sum()), base_rate=y.mean(),
                            AUROC=auroc, AUROC_lo=lo_roc, AUROC_hi=hi_roc,
                            AUPRC=auprc, AUPRC_lo=lo_prc, AUPRC_hi=hi_prc))
res = pd.DataFrame(results)

results_fixed = []
for model in ['logit','gbt']:
    for k in range(6):
        d = datasets[k]
        d = d[d.apply(lambda r:(r.subject,r.day) in common_subset_pairs, axis=1)].reset_index(drop=True)
        oof, y, groups = oof_predict(d, k, model=model)
        auroc = roc_auc_score(y, oof); auprc = average_precision_score(y, oof)
        lo_roc, hi_roc = subject_bootstrap_ci(oof, y, groups, roc_auc_score)
        lo_prc, hi_prc = subject_bootstrap_ci(oof, y, groups, average_precision_score)
        results_fixed.append(dict(model=model, k=k, sample='fixed750', n_pairs=len(d), n_subj=d['subject'].nunique(),
                            n_transitions=int(y.sum()), base_rate=y.mean(),
                            AUROC=auroc, AUROC_lo=lo_roc, AUROC_hi=hi_roc,
                            AUPRC=auprc, AUPRC_lo=lo_prc, AUPRC_hi=hi_prc))
res_fixed = pd.DataFrame(results_fixed)
res_all = pd.concat([res, res_fixed], ignore_index=True)

res_out = res_all[['model','sample','k','n_pairs','n_subj','n_transitions','base_rate',
                   'AUROC','AUROC_lo','AUROC_hi','AUPRC','AUPRC_lo','AUPRC_hi']].copy()
res_out = res_out.round(4)
res_out.to_csv('S3_history_depth_results.csv', index=False)
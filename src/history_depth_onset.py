# History-depth sweep — DYSBIOSIS ONSET target (Analysis S3b)
# Question: given a non-dysbiotic day, does adding prior-day history improve
# prediction of next-day onset of CST IV? Answer: no. Run from repo root.
import pandas as pd, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GroupKFold, cross_val_predict
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.impute import SimpleImputer
import warnings; warnings.filterwarnings('ignore')

cst = pd.read_csv('data/cst_calls.csv')
cst_sorted = cst.sort_values(['subject','day']).reset_index(drop=True)
idx = {(r.subject, r.day): i for i, r in cst_sorted.iterrows()}
cst_ord = {'I':0,'II':1,'V':1,'III':2,'IV':3}

# ONSET label: gap==1, next known, current NOT dysbiotic (cur != IV)
lab = cst[(cst['next_CST_val'].notna()) & (cst['gap_days']==1) & (cst['CST_val_coarse']!='IV')].copy()
lab['y_onset'] = (lab['next_CST_val']=='IV').astype(int)

def build_dataset(k):
    rows=[]
    for _, r in lab.iterrows():
        subj,t = r.subject, r.day; hist=[]; ok=True
        for j in range(1,k+1):
            key=(subj,t-j)
            if key not in idx: ok=False; break
            hist.append(cst_sorted.loc[idx[key]])
        if not ok: continue
        rec=dict(subject=subj, day=t, y_onset=int(r.y_onset), cur_CST=r.CST_val_coarse,
                 L_iners=r.L_iners, L_crispatus=r.L_crispatus, Gardnerella=r.Gardnerella,
                 shannon=r.shannon, host_age=r.host_age, host_bmi=r.host_bmi, birth_control=r.birth_control)
        if k>=1:
            liners_win=[r.L_iners]+[h.L_iners for h in hist]; gard_win=[r.Gardnerella]+[h.Gardnerella for h in hist]
            for j in range(1,k+1):
                rec[f'L_iners_lag{j}']=hist[j-1].L_iners; rec[f'Gardnerella_lag{j}']=hist[j-1].Gardnerella
                rec[f'cst_ord_lag{j}']=cst_ord.get(hist[j-1].CST_val_coarse,2)
            rec['liners_runmean']=np.mean(liners_win); rec['liners_runvar']=np.var(liners_win)
            rec['gard_runmean']=np.mean(gard_win); rec['gard_delta1']=r.Gardnerella-hist[0].Gardnerella
            rec['shannon_delta1']=r.shannon-hist[0].shannon
            seq=[h.CST_val_coarse for h in reversed(hist)]+[r.CST_val_coarse]
            rec['recent_transitions']=sum(1 for a,b in zip(seq[:-1],seq[1:]) if a!=b)
        rows.append(rec)
    return pd.DataFrame(rows)

def feature_cols(k):
    base=['L_iners','L_crispatus','Gardnerella','shannon','host_age','host_bmi']; hist=[]
    if k>=1:
        hist=[f'L_iners_lag{j}' for j in range(1,k+1)]+[f'Gardnerella_lag{j}' for j in range(1,k+1)]+\
             [f'cst_ord_lag{j}' for j in range(1,k+1)]+\
             ['liners_runmean','liners_runvar','gard_runmean','gard_delta1','shannon_delta1','recent_transitions']
    return base+hist, ['cur_CST','birth_control']

def make_pipe(num,cat,model):
    pre=ColumnTransformer([('num',Pipeline([('imp',SimpleImputer(strategy='median')),('sc',StandardScaler())]),num),
                           ('cat',Pipeline([('imp',SimpleImputer(strategy='most_frequent')),('oh',OneHotEncoder(handle_unknown='ignore'))]),cat)])
    clf=LogisticRegression(penalty='l2',C=0.5,max_iter=2000,class_weight='balanced') if model=='logit' else \
        HistGradientBoostingClassifier(max_depth=3,max_iter=200,learning_rate=0.05,min_samples_leaf=20,l2_regularization=1.0,random_state=0)
    return Pipeline([('pre',pre),('clf',clf)])

rng=np.random.default_rng(42)
def boot_ci(oof,y,groups,fn,nb=2000):
    subs=np.unique(groups); st=[]
    for _ in range(nb):
        samp=rng.choice(subs,size=len(subs),replace=True)
        mi=np.concatenate([np.where(groups==s)[0] for s in samp]); yy,pp=y[mi],oof[mi]
        if len(np.unique(yy))<2: continue
        st.append(fn(yy,pp))
    return np.percentile(st,2.5),np.percentile(st,97.5)

datasets={k:build_dataset(k) for k in range(6)}
common=set(zip(datasets[5]['subject'],datasets[5]['day']))
def run(d,k,model):
    num,cat=feature_cols(k); X=d[num+cat]; y=d['y_onset'].values; g=d['subject'].values
    oof=cross_val_predict(make_pipe(num,cat,model),X,y,cv=GroupKFold(5),groups=g,method='predict_proba')[:,1]
    return oof,y,g

results=[]
for sample in ['native','fixed544']:
    for model in ['logit','gbt']:
        for k in range(6):
            d=datasets[k]
            if sample=='fixed544': d=d[d.apply(lambda r:(r.subject,r.day) in common,axis=1)].reset_index(drop=True)
            oof,y,g=run(d,k,model)
            lr,hr=boot_ci(oof,y,g,roc_auc_score); lp,hp=boot_ci(oof,y,g,average_precision_score)
            results.append(dict(model=model,sample=sample,k=k,n_pairs=len(d),n_subj=d['subject'].nunique(),
                n_onset=int(y.sum()),base_rate=round(float(y.mean()),4),
                AUROC=round(roc_auc_score(y,oof),4),AUROC_lo=round(lr,4),AUROC_hi=round(hr,4),
                AUPRC=round(average_precision_score(y,oof),4),AUPRC_lo=round(lp,4),AUPRC_hi=round(hp,4)))
pd.DataFrame(results).to_csv('results/S3_onset_history_depth_results.csv',index=False)
print("done — no depth beats chance; see results/S3_onset_history_depth_results.csv")

# *L. iners* marks community mobility, not decline: a leakage-safe classifier, an honest negative, and the novel finding it uncovered

### Built with Claude: Life Sciences — Lab Track submission

**Where to read:** this is the full write-up — everything we tried, in narrative order (discovery → classifier → honest negative → pivot → novel finding → limitations). A one-page visual summary is `model_card.png`; the complete analysis inventory is `analysis_map.png`.

**The story in one line:** We built a rigorous, leakage-safe classifier to predict vaginal-microbiome transitions from a baseline profile; the primary result was honestly negative (the microbiome adds nothing beyond current state, and dysbiosis onset is unpredictable); so we tested a mechanistic hypothesis about *Lactobacillus iners* — and recovered a strong, reproducible, and **novel** result that refines a textbook claim.

---

## Part 0 — Discovery workflow (how Claude Science got us to the data)

Before any modelling, the hard problem was **finding a dataset that could answer a real question**. Public vaginal metagenomics is scarce and the outcome labels you'd want to predict usually live in the papers, not the archives. Claude Science ran this end to end:

| Stage | What Claude Science did | Result |
|---|---|---|
| Read the field | Literature + landscape deep-dive across health, disease, treatment response, industry | Framed the prediction problem |
| Find the data | Catalogued **90** public datasets (see `data/vaginal_microbiome_datasets.csv`) | 43 shotgun · 37 amplicon · 6 WGA · 4 controlled-access |
| Recover labels | Mined **30** publications to recover outcome labels behind **4** candidate targets | Intervention-response labels were **not read-joinable**; preterm-birth cohorts are 16S V3–V4 (poor *iners*/*crispatus* resolution) |
| Select cohort | Feasibility-vetted **8** candidate cohorts | Only **PRJEB37731** was turnkey: daily shotgun, 40 subjects, recoverable per-sample states |

This funnel — 90 → 30 → 4 → 8 → **1** — is why the modelling target became **next-day CST transition/onset**: it was the one abundant, per-sample, self-supervised label the available data could actually support. The full scope of analyses that followed is summarised in `analysis_map.png`.


## Part 1 — The classifier (what we built, and why it's solid)

**Goal.** Predict a clinically meaningful vaginal-microbiome state from a baseline profile, using only public data. Because intervention-response labels proved unrecoverable from public deposits (probiotic/live-biotherapeutic response had **zero read-joinable labels**; preterm-birth cohorts are dominated by V3–V4 16S that resolves *iners* from *crispatus* poorly), we selected the one abundant, per-sample, self-supervised target: **next-day CST transition**.

**Technical design — engineered for rigor, not just a number:**

| Element | Choice |
|---|---|
| Cohort | PRJEB37731 — Danish **daily** shotgun metagenomics, 40 subjects, ~967 consecutive day-pairs |
| Labels | VALENCIA CSTs computed uniformly from shotgun profiles (self-supervised) |
| Features | 184 CLR-transformed species + covariates (contraception, age, BMI, menstrual-cycle day) |
| Validation | **Leave-one-subject-out** CV — no subject in both train and test (prevents the dominant leakage mode in longitudinal microbiome data) |
| Baselines | prevalence (chance), persistence, current-CST + covariates — so any ML gain is measured against honest floors |
| Inference | subject-clustered GEE / GLMM for all effect estimates (respects repeated measures) |
| Power | synthetic-data simulation to calibrate what n=40 can and cannot detect |

**Results — an honest, mixed→negative primary outcome:**

| Target | Model | AUROC | AUPRC | Bal. acc |
|---|---|---|---|---|
| **Imminent transition** (n=967, 63.6% pos) | Current CST + covariates | **0.66** | 0.76 | 0.64 |
| | Random forest | 0.63 | 0.74 | 0.58 |
| | XGBoost | 0.62 | 0.73 | 0.57 |
| | Elastic net | 0.60 | 0.72 | 0.57 |
| | Prevalence (chance) | 0.49 | 0.63 | 0.50 |
| | Persistence | n.d. | 0.64 | 0.50 |
| **Onset of dysbiosis (CST IV)** (n=698, 27.7% pos) | Elastic net | **0.55** | 0.32 | 0.54 |
| | Current CST + covariates | 0.54 | 0.31 | 0.53 |
| | XGBoost | 0.51 | 0.28 | 0.49 |
| | Random forest | 0.51 | 0.27 | 0.48 |
| | Prevalence (chance) | 0.49 | 0.27 | 0.50 |
| | Persistence | n.d. | 0.28 | 0.50 |

*(AUPRC for prevalence/persistence equals the positive base rate by construction — 0.64 for transition, 0.28 for onset — which is why "beating chance" here is defined on AUROC and balanced accuracy, not AUPRC.)*

**What "baseline" means here (the original clinical question).** "Baseline" is **not** a fixed day 1. The dataset is built from every consecutive **day *t* → day *t+1*** pair, so each day acts as its own baseline ("today") predicting "tomorrow." The **onset target is exactly the question this project set out to answer**: *given a non-dysbiotic day, will the community be dysbiotic (CST IV) the next day?* Construction (verified in the data):

- Onset rows are restricted to baselines where **today is *not* CST IV** — the 269 already-dysbiotic day-pairs are dropped (confirmed: **zero** onset rows have today = CST IV). This is genuine *new* onset, not persistence.
- **n = 698** non-dysbiotic baseline days; **193 (27.7%)** tip into CST IV the next day.
- Which "clean" state you start from barely matters: next-day onset rate is **29% from CST I (*crispatus*)**, **24% from CST III (*iners*)**, 33% from CST V — starting from the most protective state is followed by dysbiosis *as often* as from *iners*. This is the "CST III is not a preferential gateway" result seen from the onset side (gateway χ² p = 0.56), and it is why current CST adds almost nothing (cov+CST AUROC 0.54).

**Two honest reads:**
- The **current CST + covariate baseline is the ceiling** — elastic net, random forest, and XGBoost on the full taxonomic profile do **not** beat it. The microbiome composition adds essentially nothing beyond the current state label.
- **Given a non-dysbiotic day, next-day onset of dysbiosis (CST IV) is not predictable** from that day's composition (every model ≈ chance, AUROC 0.51–0.55; AUPRC near the 0.277 base rate).

**Does adding memory help? (directly tested on the onset target.)** Because the original goal was next-day dysbiosis prediction, we ran the history-depth sweep **on the onset target specifically** — adding *k* = 1–5 prior days of features (lagged *L. iners* and *Gardnerella*, running mean/variance, day-over-day deltas, recent-transition count), same leave-one-subject-out CV and subject-bootstrap CIs. **Memory does not help:** onset AUROC is ~0.51–0.53 with no history and stays at **0.44–0.53 across all depths** — **no configuration beats chance** (of 24 model×depth×sample settings, 16 have a 95% CI including 0.5 and the other 8 fall *entirely below* 0.5; none sits above). A fixed-subject-subset control confirms this is not a sample-shrinkage artifact. So next-day dysbiosis onset is **not merely memoryless — it is unpredictable** from the microbiome time series at this resolution and sample size. See `onset_history_depth.png` and `S3_onset_history_depth_results.csv`. (For contrast, on the *transition* target history is also flat but *above* chance at ~0.65 — the signal there is real, just fully captured by the current day.)

**Why the null is credible (not just underpowered handwaving).** A synthetic-data simulation, holding the observed data structure fixed and injecting known effects, shows that at n=40 only **large** per-taxon effects (OR ≥ 1.6) are detectable. So the "taxa add nothing" result is strong evidence against a *large* hidden compositional signal — and it means the *L. iners* effect below is exactly the size of effect this cohort is powered to see.

See `hero_transition_vs_onset.png` and `model_card.png` (Part 1).

---

## Part 2 — The pivot and the novel finding

The negative primary result raised a sharper, mechanistic question. The field's working model treats CST III (*L. iners*) as the unstable **stepping-stone toward dysbiosis** (CST IV). We tested that directly at daily resolution:

1. ***L. iners* drives movement** — baseline *iners* abundance predicts a next-day transition, subject-clustered GEE **OR 5.87 (95% CI 3.15–10.94, p = 2.5×10⁻⁸)**, a monotone dose-response (transition probability ~0.58 → ~0.81 across the *iners* range). The clearest positive signal in the project.
2. **But movement is mostly recovery, not decline** — from a CST III baseline, daily risk of **escape → *L. crispatus* is 0.57** vs **descent → dysbiosis 0.24** (~2.4× more recovery). Independently reproduced in a separate session.
3. **CST III is not a preferential gateway to CST IV** — the probability of descent to CST IV does **not** differ by current CST (gateway χ² **p = 0.56**); next-day state is near-independent of current (independence χ² **p = 0.69**); CST III vs CST I → IV Fisher **OR 0.78, p = 0.21**.
4. **Direction is unpredictable** — among CST III movers, no measured feature separates escape from descent (*iners* OR 0.40, p = 0.36).
5. **The process is memoryless** — adding up to 5 prior days of history does not improve prediction (AUROC flat ~0.65).

**Interpretation.** *L. iners* is a **memoryless mobility biomarker**: it reliably flags a high-turnover community, but the turnover is predominantly benign recovery toward *L. crispatus*, and baseline composition does not forecast the minority descent to dysbiosis. This **refines the textbook "iners-as-gateway-to-BV" narrative**. See `hero_iners_mobility.png`.

---

## Background — why this matters

In the vaginal microbiome, **health means low diversity** — dominance by a single *Lactobacillus* species. When it shifts to the diverse **CST IV** state (bacterial vaginosis), risk rises for STI/HIV acquisition, preterm birth, and reduced assisted-reproduction success. Standard-of-care antibiotics clear symptomatic BV but **> 50% of women recur within 6–12 months**, because treatment does not reliably re-establish a *Lactobacillus*-dominant community. That recurrence problem is fundamentally a **prediction problem** — which is where this project began.

**Data-scarcity caveat (first-order, honestly reported).** Public vaginal metagenomics with linked longitudinal outcomes is sparse and population-skewed. Class imbalance, single-cohort validity, and label noise from irregular sampling are treated as design constraints, not footnotes.

## Limitations

- Single cohort, modest n — external validity untested; results are within-PRJEB37731 estimates.
- CST calls depend on the taxonomic pipeline; VALENCIA concordance mitigates but does not remove this dependence.
- "Transition" is defined at the observed sampling cadence; irregular intervals inject label noise.
- Associational only — no causal claim, no clinical use.

## Reproducibility

Built end-to-end on **Claude Science**. All inputs are public (ENA PRJEB37731). Key artifacts:

- `cst_calls.csv`, `valencia_taxon_mapping.csv` — community-state calls
- `modeling_dataset.parquet` / `.csv` — feature matrix
- `cv_harness.py` — leave-one-subject-out CV
- `train_models.py` — model training
- `model_results.csv`, `compact_model_results.csv`, `loso_encoding_results.csv`, `mdfs_model_results.csv` — all scored results
- `S3_onset_history_depth_results.csv` — history-depth sweep on the **onset** target (memory test)
- `hero_iners_mobility.png` — **primary** figure (novel finding); `hero_transition_vs_onset.png` — classifier backdrop; `onset_history_depth.png` — memory test; `model_card.png` — one-page summary
- `gateway_test_results.csv`, `S1_*` — competing-risks and gateway tests
- `S4_subCST_gee.csv`, `S4_subCST_counts.csv` — VALENCIA sub-CST (III-A/III-B) stratification
- `power_analysis_results.csv`, `power_analysis.png` — synthetic-data power calibration
- `claude_science_workflow.png`, `dataset_selection_funnel.png`, `analysis_map.png` — discovery-workflow & analysis-scope diagrams

## What a next cohort would unlock

The ceiling here is data, not method. A second longitudinal cohort with linked *intervention* outcomes would let this same, honest pipeline move from "predict the community's next move" to the project's north star: **predict who responds to a given microbiome-directed therapy** — the question that matters for the > 50% who recur.

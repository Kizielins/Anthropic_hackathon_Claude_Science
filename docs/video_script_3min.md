# 3-Minute Video Script — Built with Claude: Life Sciences

**Total: ~3:00 · ~450 spoken words · record voiceover over screen capture of the artifacts named in each row.**

> Delivery notes: ~150 wpm, unhurried. The arc is the story: *we built a rigorous classifier, got an honest negative, and that negative led us to a genuinely novel result.* Let the negative land — it earns the pivot. Every number is read straight from the saved LOSO / GEE / bootstrap tables.

---

### 0:00–0:20 — HOOK: THE QUESTION  *(on screen: `figures/cst_valencia_concordance.png`)*

"In the vaginal microbiome, health means one *Lactobacillus* species in charge, and dysbiosis is when that control breaks down. The clinical dream is a baseline test: measure the community today, and predict who tips into dysbiosis tomorrow. We set out to build exactly that classifier — on real daily data, done honestly."

### 0:20–0:52 — PART 1: THE CLASSIFIER  *(on screen: `figures/model_performance.png`)*

"We used PRJEB37731 — a Danish cohort sampled *daily* by shotgun sequencing — called community states with VALENCIA, and built a proper machine-learning pipeline: elastic net, random forest, and gradient boosting on 184 species, against honest baselines. Everything evaluated leave-one-subject-out, so no person appears in both training and test. Two targets: will the community transition tomorrow, and — the real question — will a non-dysbiotic day tip into dysbiosis?"

### 0:52–1:28 — THE HONEST NEGATIVE  *(on screen: `figures/hero_transition_vs_onset.png`)*

"Here's what we found, and we're not going to dress it up. For *any* transition, the best model reaches an AUROC of 0.66 — but a simple baseline using just the current state matches it. The full microbiome adds essentially nothing. And for the target we actually cared about — new onset of dysbiosis — every model sits at chance. We even added up to five days of memory; it didn't help, and several configurations scored *below* chance. Next-day dysbiosis onset is simply not predictable from baseline composition here — and a power analysis shows we could have detected any *large* compositional signal, so we're confident there isn't one, though small effects would need a bigger cohort."

### 1:28–1:52 — THE PIVOT  *(on screen: `figures/onset_history_depth.png`, then `figures/hero_iners_mobility.png` panel A)*

"A negative result is still a result — if you ask what it's telling you. The one thing that *did* carry signal was *Lactobacillus iners*, community state III, the species the textbook calls the unstable stepping-stone to dysbiosis. So we chased it. And *iners* is a strong, dose-graded marker of instability — the more iners at baseline, the more the community moves the next day, odds ratio nearly 6, p equals 2 times ten to the minus 8."

### 1:52–2:32 — THE NOVEL FINDING  *(on screen: `figures/hero_iners_mobility.png` panel B)*

"But here's the twist that overturns the textbook. When an iners community moves — where does it go? We separated *whether* it moves from *where*. From an iners day, it recovers upward to *L. crispatus* at a daily risk of 0.57 — and descends into dysbiosis at only 0.24. Recovery beats decline two-and-a-half to one. And CST III is *not* a preferential gateway to dysbiosis — the independence test comes back flat. *iners* marks a community that moves, and the movement is mostly benign recovery."

### 2:32–3:00 — CLOSE  *(on screen: `figures/model_card.png`)*

"So we built the classifier, reported the honest negative, and the negative led us somewhere new: *L. iners* is a marker of mobility, not decline — a real correction to a widely repeated story. Every input is public, every step reproducible on Claude Science — one cohort, no external validation yet. Give this pipeline a second cohort with intervention outcomes, and it goes after the real prize: predicting who responds to microbiome-directed therapy. Thanks for watching."

---

## Frame / asset checklist (export before recording — all in `figures/`)

| Beat | Artifact to show |
|---|---|
| Hook: the question | `cst_valencia_concordance.png` |
| Part 1: the classifier | `model_performance.png` |
| The honest negative | `hero_transition_vs_onset.png` |
| The pivot | `onset_history_depth.png` → `hero_iners_mobility.png` (panel A) |
| The novel finding | `hero_iners_mobility.png` (panel B) |
| Close | `model_card.png` |

**Title-card text:** *"A rigorous classifier, an honest negative, and the finding it uncovered — Built with Claude: Life Sciences."*

**Key numbers (say these exactly):** transition AUROC **0.66** (baseline matches it) · onset ≈ **0.51**, chance, and memory does not help · movement OR **5.9** (3.2–10.9), p=2×10⁻⁸ · escape **0.57** vs descend **0.24** daily risk (~2.4×) · gateway independence χ² p=**0.69**.

**Word count:** ~460 spoken words ≈ 3:00 at 150 wpm.

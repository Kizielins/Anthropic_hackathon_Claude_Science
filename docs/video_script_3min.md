# 3-Minute Video Script — Built with Claude: Life Sciences

**Total: ~3:00 · ~450 spoken words · record voiceover over screen capture of the artifacts named in each row.**

> Delivery notes: ~150 wpm, unhurried. The lead is the *L. iners* result — it overturns a textbook claim, so land it with confidence. Every number below is read straight from the saved GEE / bootstrap tables and the manuscript.

---

### 0:00–0:22 — HOOK  *(on screen: `fig_community_state_types.png`)*

"In the vaginal microbiome, health means one *Lactobacillus* species in charge. The textbook says *Lactobacillus iners* — community state type III — is the unstable stepping-stone: the state that hands you off toward dysbiosis, bacterial vaginosis, and everything that follows. We put that claim to the test on daily metagenomic data — and it doesn't hold."

### 0:22–0:48 — THE SETUP  *(on screen: `hero_transition_vs_onset.png` briefly, then dim)*

"Public vaginal metagenomics with outcome labels is genuinely scarce, so we didn't overclaim. We used PRJEB37731 — a Danish cohort sampled *daily* by shotgun sequencing — called community states with VALENCIA, and asked one honest, well-powered question: from a baseline day, what does the community do tomorrow? Everything validated leave-one-subject-out, every inference subject-clustered."

### 0:48–1:20 — iners DRIVES MOVEMENT  *(on screen: `hero_iners_mobility.png`, panel A)*

"First result: *L. iners* is a strong, dose-graded marker of instability. The more iners at baseline, the more likely the community moves the next day — the odds ratio is nearly 6, p equals 2 times ten to the minus 8. This is the clearest signal in the whole project. So far, the textbook looks right: iners means an unstable community."

### 1:20–2:05 — BUT MOVEMENT ISN'T DECLINE  *(on screen: `hero_iners_mobility.png`, panel B)*

"But here's the twist. When an iners community *does* move, where does it go? We built a competing-risks model separating *whether* it moves from *where* it goes. From an iners day, the community recovers upward to *L. crispatus* at a daily risk of 0.57 — and descends into dysbiosis at only 0.24. Recovery is about two-and-a-half times more likely than decline. And at daily resolution, CST III is *not* a preferential gateway to dysbiosis — that independence test comes back flat."

### 2:05–2:35 — THE REFRAME  *(on screen: `model_card.png`)*

"So *L. iners* marks a community that moves — but the movement is mostly benign recovery, not a one-way slide into disease. And no feature we measured predicts which direction a mover takes; adding up to five days of history doesn't help either — the process is effectively memoryless. That reframes iners from a gateway to dysbiosis into a marker of mobility. It's a small but real correction to a widely repeated story."

### 2:35–3:00 — CLOSE  *(on screen: `model_card.png` footer + title card)*

"Every input here is public, every step reproducible, built end-to-end on Claude Science — and we report the limits honestly: one cohort, no external validation yet. Give this pipeline a second cohort with intervention outcomes, and the same machinery goes after the real prize: predicting who responds to microbiome-directed therapy. Thanks for watching."

---

## Frame / asset checklist (export before recording)

| Beat | Artifact to show |
|---|---|
| Hook | `fig_community_state_types.png` |
| Setup | `hero_transition_vs_onset.png` (brief) |
| iners drives movement | `hero_iners_mobility.png` (panel A) |
| Movement ≠ decline | `hero_iners_mobility.png` (panel B) |
| Reframe | `model_card.png` |
| Close | `model_card.png` footer + title card |

**Title-card text:** *"L. iners marks mobility, not decline — Built with Claude: Life Sciences."*

**Key numbers (say these exactly):** movement OR **5.9** (3.2–10.9), p=2×10⁻⁸ · escape **0.57** vs descend **0.24** daily risk (~2.4×) · direction OR **0.40**, p=0.36 · gateway χ² p=**0.69** · transition AUROC **0.66**, onset ≈**0.51**.

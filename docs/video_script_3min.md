# 3-Minute Video Script — Built with Claude: Life Sciences

**Total: ~3:00 · ~478 spoken words · record voiceover over screen capture of the slides / figures named in each beat.**

> Framing: the story is **how we used Claude Science to run the entire discovery** — literature search, dataset identification, hypothesis formation — and how that pipeline led to the findings, especially the novel one. The model is evidence the workflow works, not the headline. ~160 wpm lands ≈ 2:59. Every number is real, pulled from this project's own survey / publication-mining / results artifacts.

---

### 0:00 — TITLE CARD  *(hold ~3s)*

"A workflow story: how Claude Science ran the whole discovery."

---

### 0:00–0:22 — THE CHALLENGE  *(on screen: `figures/vaginal_landscape.png`)*

"Human vaginal-microbiome data is scarce, scattered across archives, and the outcome labels you'd actually want to predict usually live buried in the papers, not in the data records. So our project wasn't just to build a model — it was to see whether Claude Science could run the *entire* discovery pipeline: read the field, find the data, form a hypothesis, and take it all the way to a novel finding."

### 0:22–0:52 — CLAUDE SCIENCE READ THE FIELD & FOUND THE DATA  *(on screen: `figures/claude_science_workflow.png`)*

"First, Claude Science read the field for us — a full literature and landscape deep-dive across health, disease, and treatment response. Then it went looking for data, surveying ninety public datasets: forty-three shotgun-metagenomic, thirty-seven amplicon, the rest whole-genome-amplified or restricted. All of this ran inside a single reproducible thread — this diagram is the whole pipeline, six stages from reading the literature to the finding we'll end on."

### 0:52–1:24 — IT RECOVERED THE HIDDEN LABELS & PICKED THE COHORT  *(on screen: `figures/dataset_selection_funnel.png`)*

"The catch: the archives don't expose the labels you need. So Claude Science mined the literature — reading thirty publications to recover outcome labels and score four candidate prediction targets on what was *actually* available. It vetted eight cohorts for feasibility, and only one was turnkey: PRJEB37731, a Danish cohort of forty women sampled daily by shotgun sequencing. That dataset selection — matching a question to the one dataset that could answer it — was the pivotal move, and Claude Science did it end to end."

### 1:24–1:52 — IT BUILT THE CLASSIFIER — AND REPORTED AN HONEST NEGATIVE  *(on screen: `figures/hero_transition_vs_onset.png`)*

"Then it built the classifier — elastic net, random forest, gradient boosting, all evaluated leave-one-subject-out so no person leaks between train and test. And it reported the result honestly, even though the result was negative: the microbiome composition adds essentially nothing beyond the current state, and predicting who newly tips into dysbiosis comes out at chance. Claude Science even tested adding five days of memory. It didn't help."

### 1:52–2:28 — THE NEGATIVE LED IT TO FORM A NEW HYPOTHESIS — THE NOVEL FINDING  *(on screen: `figures/hero_iners_mobility.png`)*

"But a negative result is a clue if you ask what it's telling you — and here's where it gets interesting. Claude Science flagged the one thing carrying signal, Lactobacillus iners, and formed a testable hypothesis about it. iners strongly predicts that the community will move — odds ratio near six. But when we asked *where* it moves, the textbook flips: from an iners day, the community recovers toward health at nearly two-and-a-half times the rate it declines into dysbiosis. iners marks mobility, not decline — a genuinely novel correction, reached because the platform followed the negative instead of hiding it."

### 2:28–3:00 — WHAT CLAUDE SCIENCE ENABLED  *(on screen: `figures/model_card.png`)*

"So the story here isn't really the model — it's the workflow. Claude Science read the literature, found and vetted the data, recovered the hidden labels, built and honestly tested the classifier, and then turned the negative into a novel finding — all in one reproducible thread on public data. Give that same pipeline a cohort with intervention outcomes, and it goes after the real prize: predicting who responds to microbiome-directed therapy. Thanks for watching."

---

## Frame / asset checklist (all in `figures/`)

| Beat | Artifact to show |
|---|---|
| The challenge | `vaginal_landscape.png` |
| Claude Science read the field & found the data | `claude_science_workflow.png` |
| It recovered the hidden labels & picked the cohort | `dataset_selection_funnel.png` |
| It built the classifier — and reported an honest negative | `hero_transition_vs_onset.png` |
| The negative led it to form a new hypothesis — the novel finding | `hero_iners_mobility.png` |
| What Claude Science enabled | `model_card.png` |

**Title-card text:** *"A workflow story: how Claude Science ran the whole discovery — Built with Claude: Life Sciences."*

**Workflow numbers to nail (all real):** 90 datasets surveyed · 30 publications mined · 4 targets scored · 8 cohorts vetted → 1 turnkey (PRJEB37731) · onset ≈ chance, memory doesn't help · movement OR ≈ 6 · recovery 0.57 vs descent 0.24 (~2.4×).

**Word count:** ~478 spoken words ≈ 2:59 at 160 wpm. Do a timed read-through; trim the two longest beats (Recover-labels, Novel-finding) if you run over.
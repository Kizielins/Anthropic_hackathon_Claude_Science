# 3-Minute Presentation — Exact Speaking Text
**Built with Claude: Life Sciences — Lab Track**

*Process-first framing: the story is HOW Claude Science ran the discovery — literature search, dataset identification, hypothesis formation — and how that led to the findings, especially the novel one. ~478 spoken words → ≈ 2:59 at 160 wpm. Advance the slide at each numbered cue; bracketed notes are stage directions, not spoken.*

---

**[Slide 1 — Title]** *(hold ~3s before speaking)*

> "A workflow story: how Claude Science ran the whole discovery."

---

### Cue 1 · Slide 2 — The challenge  ·  [0:00–0:22]

Human vaginal-microbiome data is scarce, scattered across archives, and the outcome labels you'd actually want to predict usually live buried in the papers, not in the data records. So our project wasn't just to build a model — it was to see whether Claude Science could run the *entire* discovery pipeline: read the field, find the data, form a hypothesis, and take it all the way to a novel finding.

---

### Cue 2 · Slide 3 — Claude Science read the field & found the data  ·  [0:22–0:52]

First, Claude Science read the field for us — a full literature and landscape deep-dive across health, disease, and treatment response. Then it went looking for data, surveying ninety public datasets: forty-three shotgun-metagenomic, thirty-seven amplicon, the rest whole-genome-amplified or restricted. All of this ran inside a single reproducible thread — this diagram is the whole pipeline, six stages from reading the literature to the finding we'll end on.

---

### Cue 3 · Slide 4 — It recovered the hidden labels & picked the cohort  ·  [0:52–1:24]

The catch: the archives don't expose the labels you need. So Claude Science mined the literature — reading thirty publications to recover outcome labels and score four candidate prediction targets on what was *actually* available. It vetted eight cohorts for feasibility, and only one was turnkey: PRJEB37731, a Danish cohort of forty women sampled daily by shotgun sequencing. That dataset selection — matching a question to the one dataset that could answer it — was the pivotal move, and Claude Science did it end to end.

---

### Cue 4 · Slide 5 — It built the classifier — and reported an honest negative  ·  [1:24–1:52]

Then it built the classifier — elastic net, random forest, gradient boosting, all evaluated leave-one-subject-out so no person leaks between train and test. And it reported the result honestly, even though the result was negative: the microbiome composition adds essentially nothing beyond the current state, and predicting who newly tips into dysbiosis comes out at chance. Claude Science even tested adding five days of memory. It didn't help.

---

### Cue 5 · Slide 6 — The negative led it to form a new hypothesis — the novel finding  ·  [1:52–2:28]

But a negative result is a clue if you ask what it's telling you — and here's where it gets interesting. Claude Science flagged the one thing carrying signal, Lactobacillus iners, and formed a testable hypothesis about it. iners strongly predicts that the community will move — odds ratio near six. But when we asked *where* it moves, the textbook flips: from an iners day, the community recovers toward health at nearly two-and-a-half times the rate it declines into dysbiosis. iners marks mobility, not decline — a genuinely novel correction, reached because the platform followed the negative instead of hiding it.

---

### Cue 6 · Slide 7 — What Claude Science enabled  ·  [2:28–3:00]

So the story here isn't really the model — it's the workflow. Claude Science read the literature, found and vetted the data, recovered the hidden labels, built and honestly tested the classifier, and then turned the negative into a novel finding — all in one reproducible thread on public data. Give that same pipeline a cohort with intervention outcomes, and it goes after the real prize: predicting who responds to microbiome-directed therapy. Thanks for watching.

---

## Delivery notes
- **Pace:** ~478 words → ≈ 2:59 at 160 wpm. Do one timed read-through; trim Cue 3 or 5 (the two longest) if you run over.
- **The spine is the workflow**, not the results. Keep returning to "Claude Science did X" — the model is evidence the pipeline works, not the headline.
- **Let the negative land** (Cue 4), then use "a negative result is a clue" to open Cue 5 — the pivot is the emotional peak.
- **Numbers to nail:** 90 datasets · 30 publications · 4 targets · 8 cohorts → PRJEB37731 · onset ≈ chance · movement OR ≈ 6 · recovery 0.57 vs descent 0.24 (~2.4×).
- **Tone:** you're demonstrating a discovery *engine*; confidence on the *iners* reframe, humility on the single-cohort limit.
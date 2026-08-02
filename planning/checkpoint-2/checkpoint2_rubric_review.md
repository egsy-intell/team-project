---
title: "Checkpoint 2 Rubric Review"
subtitle: "Alignment check: `notebooks/index.py` and `preso/checkpoint2_deck.md` against the Checkpoint 2 Evaluation Rubric"
author: "Team .egsy intelligence (Group 14)"
date: "August 2, 2026"
geometry: margin=1in
fontsize: 11pt
---

## Summary

Overall alignment against the Checkpoint 2 Evaluation Rubric is strong.
Seven of nine graded categories are fully met at the "Excellent" tier.
Two items still need attention before submission: an asymmetry between
the two model proposals' tooling/compute detail, and a comparison-of-
models section that is currently distributed rather than consolidated.
The presentation's speaker-notes typo has been fixed, and the deck's
timed run-through clocks in at 14 minutes, within the 15-minute budget.

## Category-by-Category Findings

### Problem Context (Steps 1-2 Summary) — 5 pts — Excellent

`checkpoint_2.py`'s opening cell explicitly bridges from Step 2 ("With
our data cleaned and scored in Step 2, we turn here to..."), and via
`index.py`'s embed/vstack, the full `checkpoint_1.py` (Steps 1-2)
precedes it in the combined write-up — not just a summary, the whole
thing.

### Step 3: Evaluation Metrics — 15 pts — Excellent

Per-class precision/recall/F1, recall-as-constraint, macro-F1 as the
ranking metric, and a 3x3 confusion matrix, each with an explicit
rationale (`checkpoint_2.py`, "Why plain accuracy is the wrong
headline metric" -> "Metric framework"). The deck's "Metrics & Success
Thresholds" slide mirrors this with matching numbers.

### Step 3: Success Criteria — 10 pts — Excellent

`RECALL_FLOOR` / `MACRO_F1_FLOOR` / `PRECISION_FLOOR` (0.70 / 0.60 /
0.45), each benchmarked against a random-uniform baseline and applied
identically to both models.

### Step 3: Evaluation Methodology — 15 pts — Excellent

Study-grouped split, exhaustive search vs. `StratifiedGroupKFold`
benchmark, and McMahon held out with stated reasoning —
`checkpoint_2.py`'s "Split strategy - group by study" section and the
deck's "Split Strategy" slide agree on the numbers (190/46 sites,
19.5% / 3.5%). A recent pass trimmed the split-comparison preview
table from 20 to 5 rows and combined count/percent columns for
print-width control; the deck never cited the dropped rows, so no
narrative inconsistency resulted.

### Step 4: Model Proposal #1 — 15 pts — Excellent

Model A has a dedicated "Tooling & compute plan for baseline" section
— specific libraries, an explicit operation-count estimate, hardware
needs, and reproducibility — plus the technique / rationale /
training-plan / strengths-limitations / suitability structure.

### Step 4: Model Proposal #2 — 15 pts — Good, not yet Excellent

Model B ("Model B: random forest classifier") has the same
technique/rationale/training-plan/strengths-limitations/suitability
structure, but **still has no equivalent standalone tools/compute-
estimate section**. Its "Training and optimization plan" mentions
`n_jobs=-1` and "standard CPU, no GPU" in passing, but nothing like
Model A's operation-count math or explicit software list. The rubric
explicitly asks for "tools, computational needs" on each proposal —
this remains the one place the two are not symmetric.

**Suggested fix:** add a short "Tooling & compute plan" subsection for
Model B mirroring Model A's, with a rough operation-count or
wall-clock estimate for the random forest grid search.

### Comparison of Models — 10 pts — Good, not yet Excellent

Trade-offs are covered, but only in a distributed way — each
proposal's own "Expected strengths and limitations" cross-references
the other, and the deck's "Two Competing Proposals" / "Validation &
Trade-offs" slides add a top-level framing. There is still no single
dedicated section in `checkpoint_2.py` that pulls scalability,
complexity, expected performance, and a stated preference into one
place. Not naming a preferred model is correct at this stage (no
Step 5 results exist yet), but a consolidated comparison section would
better match the rubric's "Excellent" tier.

**Suggested fix:** add a short "Comparison of Models" section to
`checkpoint_2.py` (before or after the two proposals) that explicitly
restates the scalability/deployment metric, complexity trade-off, and
expected-performance framing already present elsewhere, in one place.

### Individual Contributions — 5 pts — Excellent

Both `index.py`'s roles table/prose and the deck's "Team & Roles"
slide are specific and consistent with each other.

### Organization & Technical Writing — 5 pts — Excellent

The speaker-notes typo in `preso/checkpoint2_deck.md` ("...contain no
personally identifiable information. so there are no privacy
concerns...") has been fixed to a single, correctly-punctuated
sentence. A recent table-trimming pass across `checkpoint_1.py`,
`checkpoint_2.py`, and `footer.py` removed decorative/duplicative
tables (sample-identifier previews, redundant missing-value
breakdowns) and combined count/percent columns, keeping wide tables
within print width without losing any of the underlying suitability
assessments. Heading levels are consistent with this project's
current structure: each checkpoint notebook and `footer.py`'s
Conclusion use the same top-level header weight, matching how the
document is composed across multiple files rather than a single
notebook.

### Presentation Quality (15 min) — 5 pts — Excellent

The deck's timed run-through clocks in at 14 minutes, within the
15-minute budget, with every team member presenting a distinct
section.

## Outstanding Action Items

1. Add a "Tooling & compute plan" subsection for Model B in
   `checkpoint_2.py`.
2. Add a consolidated "Comparison of Models" section in
   `checkpoint_2.py`.

# Settling the McMahon scope question

**Branch:** `revise-mcmahon`  
**Session:** `d84e5dd5`  
**Span:** Aug 7, 15:13–16:04 UTC  
**Exchange:** 6 prompts, 10 responses

**Commits produced:**

- `bc940ae` Refine ToDos for McMahon (#78)

[← back to the pairing-log timeline](https://egsy-intell.github.io/team-project/ai/ytorresv.html)

---

### Yai

Let's pair program on Task T7. There are some dependencies that
haven't landed yet (model implementation is still TBD). However, it
would be nice to do some prep:
1. What do we mean by "retuning" for both models?
2. Do any pre-processing necessary for the McMahon data

Can we work together in those two subtasks?

### Claude

Let's pull the full Model A/B tuning grid sections and the McMahon
preprocessing/exclusion details in detail.

### Claude

I dug through the Step 4 proposal (`checkpoint_2.py`) and the
groundwater decision to ground both subtasks. Here's where I landed
on each, plus one real blocker I found on the McMahon side.

## 1. What "retuning" means for T7

Step 4 already locked in the tuning grids and the two-stage selection
rule, so "retuning" in T7 isn't free-form experimentation — it's a
bounded second pass triggered by held-out performance:

- **Model A (logistic regression)**: grid is `C`, L2 penalty, class
  weight (unweighted vs. `balanced`), iteration limit. Selection
  rule: discard candidates with cross-validated `mcl_exceedance`
  recall < 0.70, then pick max macro-F1 among survivors.
- **Model B (random forest)**: grid is `n_estimators`, max depth, min
  leaf size, max features. Same two-stage rule.

So "retune to improve accuracy" (T7's summary) = re-run/widen each
model's *own* approved grid against `StratifiedGroupKFold` results,
not swap in a different algorithm or invent new preprocessing. T7's
first guiding question ("if neither clears 0.70 recall, what does
retuning prioritize first?") implies the fallback order should be:
widen class-weighting / regularization strength before anything else,
since Step 4 already flagged class imbalance as the main lever, and
only widen the structural grid (tree depth/leaf size) second. Worth
confirming with Somya that this ordering is what "prioritize first"
should mean, but it's consistent with what Step 4 committed to.

## 2. McMahon preprocessing — found a real problem

I compared the actual predictor columns used to train Model A/B
against McMahon's geospatial file, and they don't share a feature
space:

- Training features come from **Seawolf** (`ss_scored_df`): NLCD
  land-cover fractions (`DevelopedLowIntensity`, `CultivatedCrop`,
  ...), burn-area fractions, PFAS-site proximity distances.
- McMahon's landscape data (`PFAS_GEOSPATIAL.csv`) is a **different
  source entirely**: coarse land-use percentages (`AGRI_12`,
  `NATU_12`, `URBA_12`), nitrogen loading, and facility-type counts
  (`FIRE_TRAIN`, `CHEM`, `OILGAS`, ...).

There's no column-name overlap and barely any conceptual overlap in
granularity. That matters because `preprocess_tapwater_features()`'s
`ColumnTransformer` is fit on Seawolf's exact column list — you can't
`.transform()` McMahon rows through it as-is; it'll KeyError on
missing columns.

The Step 4 text says McMahon predictions will show "the model's
*relative* ranking of McMahon sites," which reads as if the trained
model literally scores McMahon rows — but that's not possible with
the current feature sets without some kind of mapping.

Before I draft any actual prep code for McMahon, this is a real
design decision, not something I should just pick:

### Yai

[Request interrupted by user for tool use]

### Yai

McMahon folks did their own modeling with a BRT so wondering if that
could be included instead? Is there a way we could compare their
modeling results with ours?

### Claude

Good find — I read through the SI. Their Section S5 (Boosted
Regression Tree Modeling) is worth folding in, but not as a third
model we run side-by-side. Here's why, and what I'd do instead.

**Why it's not a drop-in comparison:**
- **Different target.** McMahon's BRT predicts binary *PFAS
  detection* (probability ≥ 0.5 threshold), not our three-tier
  `sum_tq_epa` risk classification
  (`within_reduced_monitoring`/`above_trigger`/`mcl_exceedance`).
  Detection presence and TQ-based severity aren't the same question.
- **Different, much wider predictor set.** Their top-ranked predictors
  (Table S10-adjacent text) are ³H (tritium, an age tracer), distance
  to nearest fire-training facility, DOC, urban land use, and VOC sum
  — of "57 potential predictor variables" spanning geochemistry
  (specific conductance, Ca+Mg, O2, pH) alongside geospatial features.
  Step 4 scoped Model A/B to *land-use and landscape predictors only*
  — we don't collect geochemistry at all, so most of their feature
  set isn't something we could reproduce even if we wanted to match
  their exact model.
- **Own train/test split**, not ours — their 10-fold tuning / 5-fold
  testing runs entirely within McMahon's well networks, so there's no
  shared holdout to score both models against.

**What genuinely is useful from this:** Table S7/S8 in the SI is the
actual provenance of the `mc_clean_df` geospatial columns (`AGRI_12`,
`NATU_12`, `URBA_12`, `N_LOAD`, the facility-type counts) — confirms
those are the raw USGS-derived predictors, not something we or a
prior contributor invented. Good to cite in the data dictionary if it
isn't already sourced there.

**My recommendation for T7/T9/T10:** don't try to run their BRT or
reproduce it — instead, cite their reported test-set metrics
(accuracy 0.84, sensitivity 0.96, specificity 0.72 at their chosen
0.5 threshold) in the deployment/discussion section as an *external
literature benchmark* — "a comparable USGS groundwater
PFAS-detection model using geochemical + geospatial predictors
reported X; our land-use-only model achieves Y" — framed as context,
not a head-to-head comparison, since the target and feature space
differ. That's a References addition (footer.py) plus maybe one
sentence in T9 or T10's discussion, not new modeling work, so it
doesn't expand T5/T6/T7 scope.

Want me to draft that citation/comparison sentence now for
`footer.py`'s References list, or hold it until T9 is actually being
written?

### Yai

It's probably worthwhile to wait. Could you be more details about how
it will go?

### Claude

Here's the concrete sequence, once T7's held-out numbers actually
exist:

**Where it lands — two small, separate additions, not a new table:**

1. **T9 (per-class metrics/benchmarking, Aug 10–11)**: right after the
   per-tier recall/macro-F1 table for Model A/B, one prose sentence
   citing McMahon et al. (2022) — already in `footer.py`'s References
   (line 106–110), so **no new citation entry needed**, just reuse it.
   Something like: "For context, McMahon et al. (2022)'s own
   boosted-regression-tree model reported 0.96 sensitivity / 0.72
   specificity predicting binary PFAS detection from a broader
   geochemical-plus-geospatial feature set (SI §S5) — not a direct
   comparison, since their target is detection presence rather than
   our ∑TQ-based tier and their predictors include water chemistry we
   don't collect, but it's a useful order-of-magnitude sense check."
   Framed as a caveat-first aside, not a benchmark row, so nobody
   skimming the table mistakes it for an apples-to-apples number.

2. **T10 (deployment/lessons-learned, Aug 11)**: a different angle —
   the SI shows McMahon's own top-ranked predictors were ³H (age
   tracer), DOC, and distance-to-fire-training-facility, i.e. mostly
   geochemistry, not land-use. That's a legitimate "lesson learned"
   point for T10's limitations discussion: our project scoped
   Model A/B to land-use/landscape predictors only (Step 4 decision),
   which the literature suggests may exclude some of the more
   informative signal for groundwater specifically. Worth one
   sentence there, tied to the McMahon generalization-gap point T10
   already plans to raise (`checkpoint_3.py:422-425`).

**What doesn't change:** no `footer.py` edit is needed for the
citation itself (already present), no `checkpoint3_task_plan.csv` row
(this is a detail within T9/T10's existing scope, not a new tracked
task), and no code — it's pure prose added when those sections are
actually drafted.

**Timing dependency:** both additions need T7's real numbers first,
so nothing to do until T9 starts. I'll flag it again when we pick up
T9/T10 rather than trying to remember it.

That leaves the two original prep items — the retuning definition and
the McMahon feature-alignment problem I found — still open. Want to
settle the McMahon question now (engineer a shared feature set vs.
drop literal scoring vs. raise it with the team), or hold that too
until T5/T6 land?

### Yai

Let's settle it now. Let's not use it as hold out, and use it instead
as reference within T9 and T10. Could you refine the guiding
questions in @notebooks/checkpoint_3.py to reflect that?

### Claude

Good — that settles it cleanly: McMahon stays fully out of T7's
scoring loop (no feature-alignment engineering needed after all), and
shows up only as narrative context in T9 (the BRT metrics-as-benchmark
framing) and T10 (the predictor-scope limitation framing) we
discussed. Let me update the three guiding questions that currently
imply otherwise.

### Claude

Now let me check line-length and lint compliance since
`notebooks/ruff.toml` enforces 79 columns.

### Claude

Lint and formatting both pass. Summary of the T7 prep work:

- **T7 (`checkpoint_3.py:293-299`)**: dropped the "McMahon-style"
  framing from the second guiding question and added an explicit note
  that McMahon is out of scoring entirely, staying a T9/T10 narrative
  reference instead.
- **T9 (`checkpoint_3.py:374-382`)**: added a guiding question for
  citing McMahon et al. (2022)'s BRT test metrics (0.96 sensitivity /
  0.72 specificity, SI §S5) as context only, explicitly flagged as
  not a scored benchmark given the different target and predictor
  set.
- **T10 (`checkpoint_3.py:421-427`)**: reworded the limitation
  guiding question from "McMahon generalization gap" (which implied a
  tested result) to the actual scope limitation — our land-use-only
  predictors exclude the geochemical/age-tracer signal McMahon's own
  model found most predictive.

No code changes needed elsewhere — this closes out the McMahon
question without any feature-engineering work, since it's never going
through the trained pipeline. The retuning definition from earlier
(bounded to each model's Step 4 grid, class-weighting first if the
0.70 recall floor isn't cleared) still stands as the working plan for
when T5/T6 land.

### Yai

Trying to decide on how to put the decision into a PRs description:

McMahon's own study produced a BRT. Considering that the data is not
apples-to-apples with Seawolf (no TQ, land use percentage vs.
land-cover fractions, etc), it would be best to hold it for analysis,
as opposed to validation set. Once we have our modeling results, we
can compare our predictors with McMahon and contribute to the
analysis that way.

could you help me refine it?

### Claude

Here's a tightened version:

---

**Decision: McMahon stays out of model scoring, used as analysis
reference instead**

McMahon et al. (2022) ran their own boosted-regression-tree model on
this same groundwater data, which raised the question of whether we
could validate our models against it directly. We're holding McMahon
out of T7's scoring entirely rather than treating it as a held-out
validation set — its data isn't apples-to-apples with
Smalling/Seawolf: no comparable ∑TQ target, land-use expressed as
buffer percentages rather than Seawolf's land-cover fractions, and a
broader predictor set that includes geochemistry we don't collect.

Once Model A/B produce results in T7, we'll reference McMahon's
reported metrics in T9/T10 as external context — not a scored
benchmark, since the target (binary detection vs. our ∑TQ tiers) and
predictors differ — and note where our land-use-only scope diverges
from what their study found most predictive.

---

A couple of things I tightened:
- Led with the decision, then the reasoning, since that's what a
  reviewer scanning PR descriptions needs first.
- "hold it for analysis" → made explicit *what* analysis (T9/T10
  narrative reference) so it doesn't read as open-ended future work.
- Spelled out the two concrete comparability issues explicit rather
  than "no TQ, land use percentage vs. land-cover fractions, etc." —
  the "etc." was doing a lot of work; the third issue (broader
  predictor set including geochemistry) is worth naming since it's
  the reason we can't just remap columns.
- Dropped "contribute to the analysis that way" — a little vague on
  its own — in favor of saying what the comparison actually is
  (context/limitation framing, not a benchmark row), matching what's
  now in the guiding questions.

Want it shorter (just the two paragraphs above, no bullets) or would
a one-line summary + this as the body work better for how your team
formats PR descriptions?

### Yai

I'm planning to post this in the team's group chat:

Hey all, I spend some time today trying to figure out what are we
going to do with the McMahon data, and I believe that the most
prudent would be to compare our landscape-specific modeling with
their own Binary Regression Tree-based modeling and results. This is
a little bit different from what we originally intended, but it will
be very hard to consolidate Seawolf and McMahon's predictors. Is not
an apples-to-apples comparison. As I originally thought they would
be.

Please take a look at the PR for more details on the pivot, and let
me know if you have any additional thoughts or questions!

Could you refine?

### Claude

A few things to flag before refining: McMahon's model is a **Boosted**
Regression Tree (BRT), not "Binary" — worth fixing since it's the
technical term. Also a couple of small grammar slips ("spend" →
"spent", "Is not" → "It's not"). Here's a cleaned-up version keeping
your casual tone:

---

Hey all, I spent some time today figuring out what we're going to do
with the McMahon data, and I believe the most prudent path is to
compare our landscape-specific modeling against McMahon's own Boosted
Regression Tree (BRT) modeling and results, instead of treating their
data as a validation set like we originally planned.

This is a bit of a pivot — turns out Seawolf's and McMahon's
predictors are hard to consolidate (different target, land-use
expressed differently, McMahon includes geochemistry we don't
collect), so it's not the apples-to-apples comparison I originally
thought it'd be.

Take a look at the PR for the full details on the pivot — let me know
if you have any thoughts or questions!

---

Want it even shorter, or is this level of detail right for the group
chat?

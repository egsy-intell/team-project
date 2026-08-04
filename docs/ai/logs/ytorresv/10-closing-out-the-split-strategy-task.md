# Closing out the split-strategy task

**Branch:** `Return-Task-callout-in-Checkpoint-1`  
**Session:** `56a54640`  
**Span:** Jul 26–27, 22:10–09:48 UTC  
**Exchange:** 23 prompts, 38 responses

**Commits produced:**

- `066ae73` Mark Task 3.3 complete: drop callout, mark CSV done
- `dbeb67d` Remove unreachable empty-partition guard in split search

[← back to the pairing-log timeline](https://egsy-intell.github.io/team-project/ai/ytorresv.html)

---

### Yai

walk me through the changes in diff in the current branch. I want to learn what was done. Once we go through it, I want to provide code review. The idea is to be as ideomatic as possible, if there's a tool we can use to minimize manual iteration, I want to learn about it and suggest code as feedback.

Let's start with the first phase

### Claude

I looked at the diff between `main` and this branch — it's entirely contained in one file, [checkpoint_2.py](notebooks/checkpoint_2.py), touching one cell plus two small preamble tweaks. Here's the walkthrough in three chunks:

## Phase 1: The two small changes (easy to skim)

1. **PEP 723 header** — `marimo>=0.23.14` → `marimo>=0.23.3` (loosened the minimum pin).
2. **Long URL wrapped** at 79 cols — `_RAW_BASE` string split across lines to satisfy the ruff line-length rule (this repo's `notebooks/ruff.toml` enforces 79 cols per [AGENTS.md](AGENTS.md)).

## Phase 2: The real change — a new train/test split cell (~190 new lines)

This replaces a cell that previously just rendered a `task_callout()` describing the *plan* to do a study-grouped split, with a cell that actually **implements** it:

- Builds `tapwater_split_df` from `ss_scored_df`, bins the continuous `sum_tq_epa` target into 3 risk tiers (`within_reduced_monitoring` / `above_trigger` / `mcl_exceedance`) via `pd.cut`.
- Picks `Study_smalling` (falling back to `Study_seawolf`) as the grouping column — sites from one study must stay together in train or test, never split across both.
- Brute-forces every possible combination of "which studies go in the test set" via `itertools.combinations`, scores each candidate on: missing risk tiers, deviation from a 20% test fraction, and distribution similarity to the full dataset — then picks the best-scoring candidate deterministically.
- Produces `tapwater_train_df` / `tapwater_test_df`, plus several summary tables: risk tiers per study, partition sizes, risk tiers per partition, and a leakage-check table (study/site overlap between partitions).

## Phase 3: Markdown/documentation rewrite in the same cell

The `task_callout()` summary text was rewritten to reflect the *actual* method now implemented (previously just describing intent), and several new `mo.md(...)` blocks were added: target/grouping definition, holdout-selection rules, a `StratifiedGroupKFold` code sample for future CV, and a note on why McMahon (groundwater, no GenX, different non-detect convention) is provisionally excluded pending "Task 3.4."

---

That's the full diff. Want me to move on to code review now — starting with the combinatorial search (Phase 2), since that's the part with the most idiomatic-Python and performance surface area?

### Yai

can you help me fix the import warning

### Claude

Confirmed the issue: `pd` is already a global from the first cell (line 18, returned at line 42), but the new split-strategy cell re-imports it locally with `import pandas as pd` (line 145-ish). marimo allows this because the cell doesn't take `pd` as a parameter, but it's a redundant, shadowing re-import — that's almost certainly the warning your IDE/marimo is flagging.

### Claude

I found one likely candidate but want to confirm before "fixing" the wrong thing. Ruff and `marimo check` both come back clean on this file, so the warning you're seeing is probably from your editor's Python language server (Pylance/pyright), not from the repo's own lint tools — and I can't see your Problems panel from here.

Two candidates I can see in the file:

1. **Line 26**: `from checkpoint_1 import app as checkpoint_1_app` — Pylance often can't resolve this statically since `checkpoint_1.py` isn't a package/on `sys.path` until the notebook runs; it's inside a documented `try/except ModuleNotFoundError` fallback pattern (per [AGENTS.md](AGENTS.md)) and is intentional, not a bug.
2. **Lines 145–147**: a leftover double-blank-line where `import pandas as pd` used to be, before marimo's autofix converted it into the `pd` cell parameter at line 144 (`def _(mo, pd, ss_scored_df, task_callout):`) — cosmetic only, not flagged by ruff.

Could you paste the exact warning text/message you're seeing (hover tooltip or Problems panel line)? That'll tell me which one it actually is rather than guessing.

### Yai

It's becuase of this line: from itertools import combinations

### Claude

That matches the repo's own convention in [AGENTS.md](AGENTS.md): imports/helpers should be defined once in the shared setup cell and passed to other cells as parameters (the same pattern already used for `pd`). Right now `combinations` is imported locally inside this one cell instead. Let me move it up.

### Claude

Now update the split-strategy cell to take `combinations` as a parameter instead of importing it locally.

### Claude

Now let's verify with ruff, marimo check, and the full test suite for this notebook.

### Claude

Fixed and verified: `combinations` now lives in the shared import cell alongside `mo`/`pd` and is passed into the split-strategy cell as a parameter (`def _(combinations, mo, pd, ss_scored_df, task_callout):`), matching the repo's own convention of defining imports once and wiring them via marimo's cell-parameter injection rather than re-importing per cell. Lint, `marimo check --strict`, and the notebook execution test all pass.

Ready to move on to the rest of the code review (the combinatorial split-selection logic, the `pd.cut` binning, etc.) whenever you are.

### Yai

re: phase 2 -- why we are grouping by study group and not by site?

### Claude

I have enough context from the code — here's the reasoning.

**Site-level grouping alone doesn't remove the leakage the split is designed to catch.** Each entry in `Study_smalling`/`Study_seawolf` (e.g. Smalling's national tapwater survey vs. Seawolf's landscape dataset) is a whole sampling *campaign*: one lab protocol, one non-detect convention, one time window, one sampling design, typically clustered in particular geographic regions, contributing many sites. If you split by `Site Code` alone (unique per row anyway, so it's a no-op as a grouping key here), sites from the *same study* still end up in both train and test.

That matters because sites within one study aren't independent of each other in ways a model can exploit — think batch effects, not biological signal:
- Smalling's non-detect convention/detection limits differ from Seawolf's and (per the McMahon note in the same cell) from McMahon's.
- Sites within a study share collection timeframe, lab, and regional sampling density.

A model can learn to recognize "this row came from Smalling" from those artifacts and use that as a shortcut to predict the risk tier, rather than learning the actual site-characteristic → PFAS-risk relationship. If test sites are drawn from a study the model already saw plenty of during training, that shortcut still works at test time, so the score looks good but doesn't tell you whether the model generalizes to a genuinely new study design.

Grouping at the **study** level instead forces the held-out studies to be entirely unseen — same reasoning as the code's own comment (`# Smalling provides the measured outcome, so Study_smalling is the canonical grouping field`) and matches the `task_callout` summary you saw in Phase 2: *"grouped by study... so evaluation measures generalization across studies/sampling designs instead of leaking sites from the same study into both sets."* This is the standard argument for group-based CV (`GroupKFold`/`StratifiedGroupKFold`) whenever rows cluster by a batch/cohort variable that could confound the target — group at the coarsest level the leakage could hide in, not just the row-identity level.

One thing worth flagging for review: the code does `dropna(subset=["Site Code", ...])` and later checks `site_overlap` between partitions as a leakage-validation table — that's a good belt-and-suspenders check, since if `Site Code` values *did* somehow repeat across studies, grouping by study wouldn't catch it. Worth confirming that check is meaningful (i.e., site codes aren't reused across the two source studies) rather than vacuously always empty.

### Yai

can you go into more details as to why samples from the same study aren't independent from each other?

### Claude

This confirms and grounds the mechanism directly from checkpoint_1's own text (`Study_seawolf` may capture differences in sampling design, geography, or time period"). Here's the fuller picture of *why* rows sharing a `Study` value are statistically dependent rather than independent draws:

**1. Shared sampling design and site-selection criteria.** Each study picked its sites for a reason — Smalling targeted public-supply and private wells in a specific national survey design; a different study might have targeted sites suspected of AFFF (firefighting foam) contamination, or a particular state's monitoring network. That selection criterion is a hidden variable correlated with PFAS levels across *every* site in that study — it's not something later sites "inherit" independently, it's baked into how the whole study was constructed.

**2. Shared geography and spatial autocorrelation.** PFAS contamination clusters geographically (near industrial sites, military bases, airports, landfills). If a study concentrated sampling in one region, its sites share proximity to the same contamination sources. Two sites 5 miles apart are not independent evidence the way two random sites nationally would be — this is classic spatial autocorrelation, and it's confounded with study identity here.

**3. Shared time window.** PFAS regulations, industrial use (e.g., the transition away from PFOA/PFOS toward GenX), and background environmental levels all shift over time. Samples collected in the same study are collected in the same window, so they share whatever was true of PFAS use/regulation at that moment — a different study run years later reflects a different regime.

**4. Shared lab protocol and analytical method.** Detection limits, which compounds get analyzed, and the non-detect convention (how "below detection limit" gets encoded — as 0, as half the limit, as missing) are set once per study, not per sample. You already saw this explicitly for McMahon (different non-detect convention than Smalling/Seawolf, and GenX excluded entirely) — that's a study-wide artifact, not sample-level noise. It directly biases `sum_tq_epa` (the toxicity-quotient target) up or down for every row in that study simultaneously.

**5. Shared predictor-generation pipeline.** Seawolf's landscape predictors (land-use fractions, proximal-facility counts) are computed once per study using one geospatial pipeline/vintage of source data; Smalling's are matched to those. Any systematic bias or resolution artifact in that pipeline shows up in every Seawolf-sourced row together.

The statistical consequence: rows within a study are **exchangeable with each other but not with rows from a different study** — they're clustered/nested data, not i.i.d. samples. A random or site-level split treats them as i.i.d. and lets the model fit study-level artifacts (items 1–5) as if they were signal about individual sites. That inflates test performance without proving the model would work on a new study collected under different conditions — exactly the generalization question checkpoint_1's own interpretation note calls out ("should not become a shortcut for predicting PFAS outcomes... use grouped cross-validation by study"), which checkpoint_2's split cell directly implements.

### Yai

Can you tell me more about this segment. What is being done here on a step by step basis. I'm trying to familiarize more with pndas

### Claude

Let's break this into the two logical pieces: building `study_risk_profile` (a summary table), then computing `all_studies` and `full_distribution` (inputs the later holdout search needs).

## Part 1: `study_risk_profile` — a study × risk-tier count table

```python
study_risk_profile = (
    tapwater_split_df.groupby(
        ["study_group", "pfas_risk_tier"],
        observed=False,
    )
    .size()
    ...
)
```

- **`.groupby(["study_group", "pfas_risk_tier"], observed=False)`** — groups rows by *every combination* of these two columns. `pfas_risk_tier` is a `Categorical` (created earlier via `pd.cut(..., labels=risk_labels)`), and `observed=False` tells pandas to keep every category combination in the output even if a given `(study, tier)` pair has zero rows, rather than silently dropping empty combos. That matters here: if one study happens to have zero `mcl_exceedance` sites, you still want that `0` to show up rather than the row disappearing.

- **`.size()`** — counts rows in each group. Result is a `Series` with a `MultiIndex` of `(study_group, pfas_risk_tier)`.

- **`.unstack(fill_value=0)`** — pivots the *second* index level (`pfas_risk_tier`) from rows into columns. So you go from a tall Series indexed by `(study, tier)` to a wide `DataFrame` indexed by `study_group`, with one column per tier. `fill_value=0` fills any still-missing cell with `0` (belt-and-suspenders alongside `observed=False`).

- **`.reindex(columns=risk_labels, fill_value=0)`** — forces the column order to match `risk_labels` (`within_reduced_monitoring`, `above_trigger`, `mcl_exceedance`) exactly, rather than whatever order `unstack` happened to produce (categorical ordering is preserved but this makes the order explicit/guaranteed).

- **`.reset_index()`** — moves `study_group` from being the row index back into a normal column, so the result is a plain flat table suitable for `mo.ui.table(...)` rendering.

```python
study_risk_profile["Sites"] = study_risk_profile[risk_labels].sum(axis=1)
```
Adds a `Sites` column = row-wise sum across the three tier-count columns (`axis=1` sums across columns, not down rows) — i.e., total sites per study.

```python
study_risk_profile = study_risk_profile[
    ["study_group", "Sites", *risk_labels]
].sort_values(["Sites", "study_group"], ascending=[False, True])
```
Reorders columns (`study_group`, `Sites`, then the three tier columns via the `*risk_labels` unpack), then sorts rows by `Sites` descending (largest study first), breaking ties alphabetically by `study_group` ascending — the two-element `ascending` list applies per sort key.

## Part 2: search inputs

```python
all_studies = sorted(tapwater_split_df["study_group"].unique().tolist())
```
`.unique()` returns the distinct `study_group` values as a numpy array (no guaranteed order); `.tolist()` converts to a plain Python list; `sorted()` gives a deterministic order. This becomes the pool `itertools.combinations` later iterates over to enumerate candidate held-out study sets.

```python
full_distribution = (
    tapwater_split_df["pfas_risk_tier"]
    .value_counts(normalize=True)
    .reindex(risk_labels, fill_value=0.0)
)
```
`.value_counts(normalize=True)` gives the *proportion* of rows in each tier across the whole dataset (fractions summing to 1, not raw counts). `.reindex(risk_labels, fill_value=0.0)` again forces a fixed label order (and a `0.0` if a tier had no rows at all) so it can be safely compared elementwise later against each candidate's test-set distribution — this is the baseline the later `distribution_gap` calculation subtracts from.

**Pandas idioms worth internalizing from this snippet:** `groupby → size → unstack` is the standard recipe for turning a "count by two categorical dimensions" question into a pivoted table (equivalent to but more explicit than `pd.crosstab`); `reindex` is the tool for forcing a known, fixed label order/set after an operation that doesn't guarantee one; and `value_counts(normalize=True)` is the idiomatic one-liner for a categorical distribution instead of manually dividing counts by `len(df)`.

### Yai

so what's the shape of the data up to this point?

### Claude

Ran the actual pipeline against the real data to get concrete shapes instead of guessing:

| Step | Object | Shape | What the dimensions mean |
|---|---|---|---|
| Input | `ss_scored_df` | `(236, 56)` | 236 tap-water sites, 56 columns (Smalling + matched Seawolf predictors + `sum_tq_epa`) |
| After adding 2 columns | `tapwater_split_df` | `(236, 58)` | same 236 rows; `+2` columns for `pfas_risk_tier` and `study_group` (no rows dropped by the `dropna` here — all 236 already have non-null `Site Code`/study/tier) |
| `study_group` values | — | **10 unique studies** | `California`, `Cape Cod`, `Chicago`, `Minnesota`, `Northeast Iowa`, `Northern Plains`, `PFAS Recon`, `Puerto Rico`, `TW Recon`, `Wisconsin` — so `study_group_column` resolved to `Study_smalling` |
| After `groupby → size → unstack → reindex` | intermediate | `(10, 4)` | **this is the key shape change**: 236 rows collapsed down to 10 rows (one per study), 4 columns = `study_group` (from the reset index) + the 3 `risk_labels` columns |
| After adding `Sites` + reordering | `study_risk_profile` | `(10, 5)` | same 10 rows, `+1` column (`Sites` = row sum) |

So the whole block is a **236-row site-level table → 10-row study-level summary table**. That collapse is exactly what `.groupby(...).size()` does: it goes from "one row per sample" to "one row per group" — here the group is `(study_group, pfas_risk_tier)`, and `.unstack()` then spreads the tier dimension out into columns so each study is one row.

Concretely from the printed table: `PFAS Recon` is the largest study (88 sites), `Northern Plains` the smallest (3 sites) — and note `Northeast Iowa` and `Northern Plains` have **zero** sites in `above_trigger` and `mcl_exceedance` (all their sites fall in `within_reduced_monitoring`). That's directly relevant to the later holdout search: if either of those small, single-tier-only studies gets picked for the test set, it triggers the `missing_class_penalty` logic you saw earlier, since the test partition wouldn't contain examples of all 3 risk tiers.

### Yai

so what's the shape here?

### Claude

`full_distribution` is a **1-D `pandas.Series` of shape `(3,)`** — not a DataFrame. It went from 236 rows (`tapwater_split_df["pfas_risk_tier"]`, a single column) down to one number per risk tier.

- **`.value_counts(normalize=True)`** collapses the 236 individual tier labels into 3 unique values, each mapped to its proportion of the whole (counts ÷ 236 instead of raw counts).
- **`.reindex(risk_labels, fill_value=0.0)`** doesn't change the shape here (all 3 labels are already present) — it just guarantees the *order* is `within_reduced_monitoring`, `above_trigger`, `mcl_exceedance` rather than whatever order `value_counts` returned (which sorts by frequency, descending, by default).

Actual values on the real data:

| pfas_risk_tier | proportion |
|---|---|
| within_reduced_monitoring | 0.534 |
| above_trigger | 0.169 |
| mcl_exceedance | 0.297 |

This 3-element Series is the fixed target this notebook's holdout search compares every candidate test partition against later (`distribution_gap = (test_distribution - full_distribution).abs().sum()`) — both sides need matching index labels/order for that subtraction to align correctly elementwise, which is exactly what the two `.reindex(risk_labels, ...)` calls (here and on `study_risk_profile`) guarantee.

### Yai

now, I want to understand this part

### Claude

This is the brute-force search over every possible way to hold out a subset of studies as the test set. Let's trace it with real numbers — you have 10 studies from the profile table.

## Outer loop: `for held_out_count in range(1, len(all_studies)):`

`len(all_studies) == 10`, so `held_out_count` runs `1, 2, ..., 9` — **never 0** (that would mean an empty test set) and **never 10** (that would mean an empty training set, holding out everything).

## Inner loop: `for held_out_studies in combinations(all_studies, held_out_count):`

`itertools.combinations` generates every subset of that exact size, order-independent. For `held_out_count=1` that's 10 single-study subsets (`('California',)`, `('Cape Cod',)`, ...); for `held_out_count=2` that's `C(10,2)=45` pairs, etc. Summed across all 9 values of `held_out_count`, that's `2^10 - 2 = 1022` total candidate splits evaluated — every non-trivial way to partition 10 studies into two groups.

## Build the candidate partition

```python
test_mask = tapwater_split_df["study_group"].isin(held_out_studies)
train_part = tapwater_split_df.loc[~test_mask]
test_part = tapwater_split_df.loc[test_mask]
if train_part.empty or test_part.empty:
    continue
```
`.isin(held_out_studies)` gives a boolean Series over all 236 rows — `True` if that row's study is in this candidate's held-out set. `~test_mask` inverts it for training rows. The `if ... continue` guard is actually **dead code** at this scale: since every study has at least 3 rows (`Northern Plains` from the earlier table) and `held_out_count` is bounded to `[1, n-1]`, neither side can ever be empty. Worth a mental note for the review pass — not wrong, just unreachable given the earlier guarantees.

## Score this candidate on three criteria

**1. Class coverage** — does every risk tier appear in *both* train and test?
```python
train_classes = set(train_part["pfas_risk_tier"].dropna())
test_classes = set(test_part["pfas_risk_tier"].dropna())
missing_class_penalty = (
    len(set(risk_labels) - train_classes)
    + len(set(risk_labels) - test_classes)
)
```
`set(risk_labels) - train_classes` is set difference — tiers in `risk_labels` but *not* seen in training. Its length (0, 1, 2, or 3) plus the same for test gives a penalty of 0 (perfect coverage) up to 6 (total failure). Recall from the earlier table: `Northeast Iowa` and `Northern Plains` only have `within_reduced_monitoring` rows — holding either out as the *entire* test set would make `missing_class_penalty > 0` immediately.

**2. Test-set size** — how close to a 20% holdout:
```python
test_fraction = len(test_part) / len(tapwater_split_df)
```

**3. Distribution match** — does the test set's tier mix resemble the full dataset's tier mix (the `full_distribution` you looked at earlier)?
```python
test_distribution = (
    test_part["pfas_risk_tier"]
    .value_counts(normalize=True)
    .reindex(risk_labels, fill_value=0.0)
)
distribution_gap = float(
    (test_distribution - full_distribution).abs().sum()
)
```
Same `value_counts(normalize=True).reindex(risk_labels, ...)` pattern as before, giving a 3-element Series aligned with `full_distribution`. Subtracting two aligned Series is elementwise; `.abs().sum()` collapses that to one number — the total absolute deviation across all three tiers (0 = identical distribution, up to 2.0 = completely disjoint).

## Combine into one score

```python
selection_score = (
    missing_class_penalty * 10
    + abs(test_fraction - 0.20)
    + distribution_gap
)
```
This is a weighted-sum scalarization: `missing_class_penalty` is weighted ×10 specifically so it dominates — any candidate missing a class scores far worse than one merely off on size or distribution (since `test_fraction`/`distribution_gap` terms are both bounded roughly in `[0, ~1-2]`). `abs(test_fraction - 0.20)` penalizes drifting from the 20% target in either direction.

## Record it

Each candidate's stats get appended as a dict to `candidate_rows`, which later (outside this snippet) becomes `pd.DataFrame(candidate_rows)` sorted to pick the single best one — this loop is purely the "generate and score every option" step; the "pick the winner" step happens after.

**One thing worth flagging for the review pass**: this is `O(2^n)` in the number of studies. It's completely fine at `n=10` (1022 iterations, trivial), but it would become infeasible if the number of studies grows much further — worth a comment noting that constraint, or switching to a greedy/sampled search if `all_studies` ever grows past ~20-25.

### Yai

so candidate rows are the list of possible test/held-out combinations by study group and a quality rating for each?

### Claude

Exactly — that's the right mental model.

Each entry in `candidate_rows` is: **"if I hold out *this* set of studies as the test set, here's how good that choice would be."** Concretely, each dict is one row of a future comparison table:

| field | meaning |
|---|---|
| `held_out_studies` | the specific tuple of study names proposed for the test set (e.g. `('Cape Cod', 'Wisconsin')`) |
| `test_fraction` | what % of all 236 sites that choice puts in test |
| `missing_class_penalty` | 0 if all 3 risk tiers survive in both train and test, higher if some tier gets isolated to just one side |
| `distribution_gap` | how much the test set's risk-tier mix deviates from the overall dataset's mix |
| `selection_score` | the single combined "badness" number (lower = better) used to rank all candidates against each other |

So by the end of this loop, `candidate_rows` holds all 1022 possible held-out-study combinations, each annotated with a quality score. The code right after this snippet (which you saw in the original diff) turns that list into `split_candidates_df`, sorts it by `missing_class_penalty` first, then `selection_score`, and takes `.iloc[0]` — i.e., "of every way we could hold out a group of studies, pick the one that keeps all classes present and is closest to a clean 20% stratified holdout." That's the deterministic winner that becomes `tapwater_train_df`/`tapwater_test_df`.

### Yai

can you go into more detail about this KFold plans? Is this cross-validation? If so, how does it work? Are we holding out within the test data itself?

### Claude

Good question — yes, this is cross-validation, and to be precise about where it happens: this is **all inside `tapwater_train_df`**, never touching `tapwater_test_df`. Let me unpack it.

## Where this sits in the pipeline

Recall the split from earlier: `tapwater_split_df` → `tapwater_train_df` (the studies *not* held out) and `tapwater_test_df` (the held-out studies). `tapwater_test_df` is set aside and untouched until final evaluation — the notebook's own text says so explicitly ("test studies must remain untouched during scaling, encoding, feature selection, and hyperparameter tuning"). This `StratifiedGroupKFold` block is only about how you responsibly use `tapwater_train_df` *by itself*, for hyperparameter tuning.

Also worth noting: this is a fenced code block inside an `mo.md(...)` string, i.e. **illustrative sample code for the write-up, not an executed cell** — `X_train`/`y_train` aren't defined anywhere else in the notebook. It's documentation of the *plan*, matching the notebook's framing as a design/proposal document (per the earlier markdown: "each section states what a task lead will argue... not yet an executed evaluation").

## What cross-validation is solving here

With only `tapwater_train_df` available, you still need to pick hyperparameters (tree depth, regularization strength, etc.) without ever looking at `tapwater_test_df`. A single train/validation split inside training data would waste data and be noisy with this few studies. Cross-validation instead repeatedly re-splits the training data into k folds, trains on k−1 of them, validates on the held-out fold, and rotates — so every row gets used for validation exactly once, and you average performance across folds for a more stable hyperparameter estimate.

## Why *this specific* variant — `StratifiedGroupKFold`, not plain `KFold`

It combines two constraints simultaneously:

1. **Group** — same leakage logic as the outer split: a `study_group` must not appear in both the CV-fit fold and the CV-validation fold within a single round. Otherwise you'd reintroduce exactly the study-level leakage the outer split was built to avoid, just one level down.
2. **Stratified** — it also tries to keep the `pfas_risk_tier` (that's what `y_train` would be) proportionally represented in each fold, so you're not accidentally validating on a fold that's 100% `mcl_exceedance` by chance.

Plain `GroupKFold` only respects constraint 1; plain `StratifiedKFold` only respects constraint 2 (and would leak groups). `StratifiedGroupKFold` does a best-effort of both — "best-effort" because with a small, uneven number of groups (10 studies, most now inside `tapwater_train_df`, holding a *very* uneven number of rows — 88 down to 3), it can't always achieve perfect stratification while also respecting hard group boundaries; it's a heuristic optimization, not an exact solve.

## Reading the parameters

```python
grouped_cv = StratifiedGroupKFold(
    n_splits=min(5, tapwater_train_df["study_group"].nunique()),
    shuffle=True,
    random_state=42,
)
```
- `n_splits=min(5, nunique())` — you can't have more folds than groups (each fold needs at least one whole group's worth of validation rows), so this caps at 5 or the actual number of training studies, whichever is smaller. If the winning split leaves, say, 7 studies in training, this gives 5 folds; if it leaves only 3, this gives 3.
- `shuffle=True, random_state=42` — randomizes group-to-fold assignment (rather than assigning in the array's original order) but deterministically, so results are reproducible run-to-run.

```python
for fit_idx, validation_idx in grouped_cv.split(
    X_train, y_train, groups=tapwater_train_df["study_group"],
):
    ...
```
`.split(...)` is a generator yielding `n_splits` pairs of row-index arrays. Each iteration: `fit_idx` rows train a model instance, `validation_idx` rows (whole studies, never seen in that fold's fit) score it. `groups=` is what makes it group-aware — without it, this would silently fall back to ignoring group boundaries within folds.

**One gap worth flagging for review**: at only ~5-9 studies remaining in training (10 total minus however many the outer search held out), some folds may end up validating on a single very small study (recall `Northern Plains` had just 3 rows) — that's a fold whose validation metric will be extremely noisy. Worth a caveat in the write-up that CV metric variance across folds may be high here, not because the method is wrong but because the group cardinality is thin.

### Yai

so the kfold is being design taking into consideration that the smalling rows need to be grouped by study and then it will also try to preserve a good ratio of the three categories?

### Claude

Yes, exactly — that's the right two-part summary.

1. **Group by study** — same reason as the outer train/test split: rows from the same study (same lab protocol, sampling design, region, time window — everything we walked through earlier about why they're not independent) must never be split across the "fit" and "validation" sides of a single CV fold. `groups=tapwater_train_df["study_group"]` is what enforces that — a whole study goes to one side or the other, never both, within each fold.

2. **Preserve the three risk-tier proportions** — the "Stratified" half tries to keep `within_reduced_monitoring` / `above_trigger` / `mcl_exceedance` represented in roughly their overall proportions in every fold's validation set, so no fold accidentally validates on an unrepresentative slice (e.g., all-`mcl_exceedance` by chance).

The one nuance to hold onto: it does **both at once, on a best-effort basis** — group integrity is a hard constraint (never violated), but with only a handful of unevenly-sized studies to distribute across folds, perfect class-balance per fold isn't always achievable. `StratifiedGroupKFold`'s algorithm optimizes for balance *subject to* never breaking a group apart, not the other way around. So you should expect folds to be closer to balanced than random grouping would give you, not exactly balanced.

### Yai

ok, so what's left out of task 3.3?

### Claude

Looking at both the CSV (`planning/checkpoint-2/checkpoint2_tasks.csv`) and the actual notebook content, task 3.3 ("Design the split strategy — group by study") is scoped narrowly, and the cell you've been reviewing has fully delivered its core: the study-grouped holdout logic, the leakage checks, and the risk-tier binning. But a few things are explicitly **out of scope for 3.3** and pushed elsewhere — and one thing looks like stale bookkeeping worth fixing.

**Deliberately deferred, by the notebook's own text:**
- **McMahon's placement** — explicitly punted to **Task 3.4** ("Decide groundwater's role: held-out vs combined"), which the CSV shows *depends on* 3.3. Right now McMahon sits outside the split entirely.
- **Actually running the CV / hyperparameter tuning** — the `StratifiedGroupKFold` block is illustrative code inside markdown, not an executed cell. Fitting real models against it is Step 4 (`4.1`/`4.3`) and Step 5 (`EVAL`), not 3.3.
- **Metric definitions** (precision/recall/F1, confusion matrix) — that's **Task 3.1** (separate owner, Somyaranjan), not part of this split-design cell at all.
- **The risk-tier cutoffs themselves** (`0.5`/`1.0` on `sum_tq_epa`) are used here but are officially owned by **Task 3.2** ("Set the success threshold"), which per the CSV depends on `PW` and isn't listed as done — worth checking with Somyaranjan/team whether `0.5`/`1.0` are the agreed final cutoffs or just a placeholder this cell borrowed to unblock the split design.

**Worth flagging, not a scope gap but a data-hygiene issue:** the CSV still lists task `3.3` status as `Not started`, with an end date of `2026-07-27` (today). Given the implementation is clearly done in this branch, that row should probably be updated to `Complete`/`In review` — and once it's marked done, per [AGENTS.md](AGENTS.md)'s task-tracking convention, the `task_callout()` for this section and its "Task 3.3"-style prose should eventually be stripped from the published notebook (the CSV row remains the durable record).

### Yai

ok, since this is good, and before we start the review feedback, let's add a commit that eliminates the card and updates the CSV

### Claude

Now I'll strip task 3.3's callout per the [AGENTS.md](AGENTS.md) convention (plain heading + reworded prose, since the CSV is the durable record), and update the CSV status. First the notebook:

### Claude

Now remove `task_callout` from this cell's signature since it's no longer used there:

### Claude

Now verify lint/marimo/tests pass, then update the CSV:

### Claude

Let's run the full notebook test suite before committing:

### Claude

All green. Here's the diff for this change before I commit:

### Claude

Ready to commit — should I go ahead?

### Claude

Committed as `066ae73`. Ready to move into the code-review feedback pass whenever you want to start.

### Yai

let's go into the feedback now

### Claude

Here's the review, ordered by what I think matters most. I'm presenting findings only — let me know which ones you want implemented.

## 1. The brute-force search is the best target for "use a tool instead" (your main ask)

The `itertools.combinations` double loop enumerates all `2^n - 2` subsets of studies and scores each one by hand for group-safety + stratification + size. `scikit-learn` already ships a tool that does group-safe + stratified splitting: **`StratifiedGroupKFold`**, which the notebook *already proposes* for CV further down (Task 3.3's own markdown references it). You could get a single 80/20-ish grouped-stratified split for free instead of hand-rolling the search:

```python
from sklearn.model_selection import StratifiedGroupKFold

splitter = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
fit_idx, holdout_idx = next(splitter.split(
    tapwater_split_df,
    tapwater_split_df["pfas_risk_tier"],
    groups=tapwater_split_df["study_group"],
))
tapwater_train_df = tapwater_split_df.iloc[fit_idx]
tapwater_test_df = tapwater_split_df.iloc[holdout_idx]
```

**Trade-off to be upfront about:** this is *not* a drop-in equivalent. The current code exhaustively searches for the single best split by an explicit, inspectable score (and reports *why* it won via `split_candidates_df`); `StratifiedGroupKFold` gives you one of several roughly-balanced folds via a greedy heuristic, with no guarantee it's the best of the `2^n` options, and no built-in `missing_class_penalty`-style guarantee (you'd still need to check `nunique()` per tier post-hoc, since sklearn's heuristic doesn't hard-guarantee full class coverage per fold either). Given you only have 10 studies (1022 candidates, sub-second), I'd lean toward **keeping the current exhaustive search** — it's more rigorous and this is a proposal-document notebook where showing your work matters — but it's worth a one-line comment noting *why* you didn't just use `StratifiedGroupKFold` here, so a future reader doesn't wonder why you reinvented it right next to where you cite it.

## 2. Hardcoded risk-tier thresholds duplicate an *open* task's ownership

```python
tapwater_split_df["pfas_risk_tier"] = pd.cut(
    tapwater_split_df["sum_tq_epa"],
    bins=[float("-inf"), 0.5, 1.0, float("inf")],
    ...
)
```
`0.5`/`1.0` are currently only documented as prose in checkpoint_1 (never materialized in code before this cell) — and **Task 3.2** ("Set the success threshold," owned by Somyaranjan, still "Not started" per the CSV) is the task that's supposed to finalize these exact cutoffs. Right now this cell silently bakes in a placeholder value for a decision someone else hasn't officially made yet. Suggest: pull these into named constants (`WITHIN_MONITORING_CUTOFF = 0.5`, `MCL_EXCEEDANCE_CUTOFF = 1.0`) with a comment noting they're provisional pending 3.2, so it's a one-line change (not a re-read of the whole `pd.cut` call) when 3.2 lands — and so grep for "3.2" surfaces this dependency.

## 3. Dead defensive branch

```python
if train_part.empty or test_part.empty:
    continue
```
Given `held_out_count` is bounded to `range(1, len(all_studies))` (never 0, never all) and every study has ≥1 row (confirmed earlier: smallest is `Northern Plains` with 3), neither `train_part` nor `test_part` can ever be empty. Harmless, but it's dead code masquerading as a real guard — either delete it, or if you want to keep it as a guard against a future data change (e.g., a study group with 0 rows after some future filter), say so in a comment so it doesn't read as leftover debugging cruft.

## 4. Minor duplication: the distribution-computation pattern repeats

```python
full_distribution = tapwater_split_df["pfas_risk_tier"].value_counts(normalize=True).reindex(risk_labels, fill_value=0.0)
...
test_distribution = test_part["pfas_risk_tier"].value_counts(normalize=True).reindex(risk_labels, fill_value=0.0)
```
Same three-call chain, twice, over different frames. Low priority at 2 occurrences, but if this pattern gets reused again later in the notebook (e.g., checking `train_part`'s own distribution too), it's worth a tiny helper:
```python
def tier_distribution(df):
    return df["pfas_risk_tier"].value_counts(normalize=True).reindex(
        risk_labels, fill_value=0.0
    )
```
per [AGENTS.md](AGENTS.md)'s "keep shared helpers in one cell" guidance.

## 5. Redundant-but-defensible sort key

```python
split_candidates_df.sort_values(
    ["missing_class_penalty", "selection_score", "held_out_studies"]
)
```
Since `selection_score` already includes `missing_class_penalty * 10` and the other two terms are bounded well under 10, sorting by `selection_score` alone would already respect the penalty priority in practice. Listing `missing_class_penalty` explicitly first is redundant *today* — but I'd actually keep it as-is: it makes the priority order self-documenting and robust against someone later tweaking the `*10` weight without noticing it breaks the implicit ordering. Not a change, just flagging so it doesn't get "simplified" away by someone who doesn't see why it's there.

---

Want me to implement any of these? #2 (named constants for the thresholds) and #3 (dead-code comment/removal) are quick, low-risk wins I'd suggest starting with; #1 is a judgment call on which philosophy you want documented.

### Yai

Re: #1, is there a way we could assing a score to the stratified version? In the same we're doing with the manual one?

### Claude

Yes — the cleanest way is to extract the scoring logic from inside the loop into a standalone function, then call that same function on whatever candidate split you hand it, whether it came from `itertools.combinations` or from `StratifiedGroupKFold`. That turns the exhaustive search from "the only way to get a score" into "one candidate-generator among possibly several," which is a nice validation move: you can empirically check whether the brute-force winner actually beats what sklearn's heuristic finds.

## Step 1: factor the scoring into a function

```python
def score_split(test_part, train_part, full_data, risk_labels, full_distribution):
    train_classes = set(train_part["pfas_risk_tier"].dropna())
    test_classes = set(test_part["pfas_risk_tier"].dropna())
    missing_class_penalty = (
        len(set(risk_labels) - train_classes)
        + len(set(risk_labels) - test_classes)
    )

    test_fraction = len(test_part) / len(full_data)
    test_distribution = (
        test_part["pfas_risk_tier"]
        .value_counts(normalize=True)
        .reindex(risk_labels, fill_value=0.0)
    )
    distribution_gap = float(
        (test_distribution - full_distribution).abs().sum()
    )

    selection_score = (
        missing_class_penalty * 10
        + abs(test_fraction - 0.20)
        + distribution_gap
    )
    return {
        "test_fraction": test_fraction,
        "missing_class_penalty": missing_class_penalty,
        "distribution_gap": distribution_gap,
        "selection_score": selection_score,
    }
```

The exhaustive-search loop becomes a thin wrapper that calls this per candidate and adds `held_out_studies`.

## Step 2: score every `StratifiedGroupKFold` fold with the same function

```python
from sklearn.model_selection import StratifiedGroupKFold

grouped_cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
kfold_candidate_rows = []
for fold_num, (train_idx, test_idx) in enumerate(
    grouped_cv.split(
        tapwater_split_df,
        tapwater_split_df["pfas_risk_tier"],
        groups=tapwater_split_df["study_group"],
    )
):
    train_part = tapwater_split_df.iloc[train_idx]
    test_part = tapwater_split_df.iloc[test_idx]
    row = score_split(
        test_part, train_part, tapwater_split_df, risk_labels, full_distribution
    )
    row["held_out_studies"] = tuple(
        sorted(test_part["study_group"].unique())
    )
    row["method"] = f"StratifiedGroupKFold fold {fold_num}"
    kfold_candidate_rows.append(row)
```

## Step 3: put them in the same comparison table

```python
split_candidates_df["method"] = "exhaustive search"
comparison_df = pd.concat(
    [split_candidates_df, pd.DataFrame(kfold_candidate_rows)],
    ignore_index=True,
).sort_values(["missing_class_penalty", "selection_score"])
```

Now `comparison_df.head()` shows, side by side, whether any `StratifiedGroupKFold` fold actually beats (or ties) the exhaustive search's winner on the exact same criteria. Two likely outcomes, both useful to report:

- **The exhaustive winner is strictly better** (lower `selection_score`, same or lower `missing_class_penalty`) — that's a concrete, quantified justification for keeping the brute-force approach over the sklearn shortcut, worth stating explicitly in the write-up rather than just asserting it.
- **A `StratifiedGroupKFold` fold ties or wins** — that would actually undercut the case for the custom search, and you'd want to know that before defending the more complex approach.

Want me to wire this into the notebook (as a real cell producing `comparison_df`), or keep it at the "here's how you'd do it" stage for now?

### Yai

let's open up a gh review and add this as an inline review comment. Please provide pseudocode and an explanation of what we would want to do.

Also offer a preview before posting

### Claude

Good — this maps to PR #47, head commit `066ae73` (the one we just pushed... let me confirm it's actually pushed, since inline comments need the commit to exist on GitHub).

### Claude

Found it: PR #47, "Update Checkpoint 2 grouped split strategy," head commit `066ae73` (already pushed, matches `origin/Return-Task-callout-in-Checkpoint-1`) — so I can anchor an inline comment on that commit. I'd place it at `notebooks/checkpoint_2.py:204` (`candidate_rows = []`, right where the exhaustive search begins), since that's the natural anchor point for "here's an alternative/complementary approach."

Here's the comment I'd post — **preview only, not posted yet**:

---

**Inline comment on `notebooks/checkpoint_2.py:204`:**

> **Suggestion: score `StratifiedGroupKFold`'s folds with this same rubric, as a sanity check**
>
> This exhaustive search is solid (small `n`, so `2^10` candidates is cheap, and it gives a fully inspectable "why this split won"). One thing worth adding: validate it against `sklearn`'s built-in group+stratified splitter using the *same* scoring function, so we have quantified evidence the brute-force search is worth its complexity rather than just asserting it.
>
> Pseudocode:
> ```
> # 1. Extract the scoring logic (missing_class_penalty, test_fraction,
> #    distribution_gap, selection_score) already computed inline below
> #    into a standalone function:
> def score_split(test_part, train_part, full_data, risk_labels, full_distribution):
>     ... same body as lines ~211-238 below ...
>     return {test_fraction, missing_class_penalty, distribution_gap, selection_score}
>
> # 2. Run StratifiedGroupKFold over the whole tapwater_split_df:
> grouped_cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
> for fold_num, (train_idx, test_idx) in enumerate(
>     grouped_cv.split(tapwater_split_df, tapwater_split_df["pfas_risk_tier"],
>                       groups=tapwater_split_df["study_group"])
> ):
>     score each fold with score_split(...), tag with fold_num
>
> # 3. Concat those scored folds with `split_candidates_df` into one
> #    comparison table, sorted by the same [missing_class_penalty, selection_score]
> #    key, and report whether the exhaustive winner actually beats every
> #    sklearn fold on identical criteria.
> ```
>
> Two possible outcomes and what each would mean:
> - Exhaustive winner strictly beats every `StratifiedGroupKFold` fold → good, quantified justification to keep the custom search in the write-up.
> - A fold ties or wins → worth knowing before defending the extra complexity; might mean we could swap in the sklearn call and simplify this cell.
>
> Happy to pair on wiring this in if useful — not blocking, just flagging since we already cite `StratifiedGroupKFold` a few cells down for CV and this would double as evidence for/against the design choice made here.

---

Want me to adjust tone/length, change the anchor line, or post it as-is via `gh pr review 47 --comment` (or `gh api` for a true inline/diff comment, since `gh pr review` doesn't support per-line comments directly — I'd need `gh api repos/egsy-intell/team-project/pulls/47/comments` with `commit_id`, `path`, and `line`)?

### Yai

yeah, that comment works. Let's post and continue the review. Do not finalize the review yet

### Claude

Posted as a **pending review** (`state: "PENDING"`, review ID `4785632332`) — it's not visible to others yet, exactly as requested. The inline comment landed on `notebooks/checkpoint_2.py:204`.

I'll keep adding comments to this same pending review as we continue — let me know the next thing you want to flag, and we'll submit (approve/comment/request-changes) only when you say the review is done.

### Yai

re: #2 -- that's a fair observation. Let's add an inline comment about it. Probably best to have them set closer to the corresponding task, and add a comment there about the pending state?

### Claude

Before posting — quick heads-up on a constraint I hit: GitHub only allows **one pending review per PR per user**, so I can't append a second standalone pending comment on top of the first one via the API. I deleted and will recreate the pending review with **both** comments in a single call (the first one, verbatim as before, plus this new one) — nothing has been visible on the PR at any point, so nothing is lost.

Here's the new comment, anchored at `notebooks/checkpoint_2.py:165` (the `pd.cut` bins line, since that's the only place these values currently live) — **preview before posting**:

---

**Inline comment on `notebooks/checkpoint_2.py:165`:**

> **Suggestion: extract these as named constants flagged against Task 3.2's pending decision**
>
> `0.5` and `1.0` here are currently the *only* place these cutoffs are materialized in code — checkpoint_1 only documents them as prose. But **Task 3.2** ("Set the success threshold — risk-tier cutoffs," owned by Somyaranjan/Team) is the task that's supposed to officially decide these values, and it's still "Not started" per the CSV. Right now this cell quietly bakes in a placeholder for a decision that hasn't been made yet.
>
> Suggest naming them and commenting the dependency, so it's a one-line change (and a `grep`-able pointer) once 3.2 lands instead of a re-read of this `pd.cut` call:
> ```python
> # Provisional cutoffs pending Task 3.2 (Somyaranjan/Team) — update
> # here once 3.2 finalizes the risk-tier thresholds.
> WITHIN_MONITORING_CUTOFF = 0.5
> MCL_EXCEEDANCE_CUTOFF = 1.0
>
> tapwater_split_df["pfas_risk_tier"] = pd.cut(
>     tapwater_split_df["sum_tq_epa"],
>     bins=[
>         float("-inf"),
>         WITHIN_MONITORING_CUTOFF,
>         MCL_EXCEEDANCE_CUTOFF,
>         float("inf"),
>     ],
>     labels=risk_labels,
>     right=False,
>     ordered=True,
> )
> ```
> Same constants could then be reused in the markdown f-string a few cells down (lines ~359-361) instead of restating `0.5`/`1.0` as separate literal text, so the two can't drift out of sync.

---

Want me to post this alongside the first comment now, tweak wording/anchor line, or hold off?

### Yai

got it. Let's hold onto generating the in-flight review until we have all the comments we will end up posting

### Claude

Sounds good — I'll keep drafting and previewing findings with you here, and hold off on any GitHub API calls (no pending review created) until you say we're ready to batch-post everything together. Both comments we've agreed on so far are saved in this conversation:

1. **`notebooks/checkpoint_2.py:204`** — score `StratifiedGroupKFold` folds with the same rubric as a sanity check on the exhaustive search.
2. **`notebooks/checkpoint_2.py:165`** — extract the `0.5`/`1.0` risk-tier cutoffs as named constants flagged against Task 3.2's pending decision.

Let me know when you want to look at more of the diff (findings #3–#5 from earlier, or something new), and we'll post the whole batch as one pending review at the end.

### Yai

Re: 3 -- that's fair, I would remove it since it's dead code. We're not changing the data set so I don't think to have it set. Otherwise, it could give the wrong signal. What do you think?

### Claude

Agreed — I think removing it is the right call, for exactly the reason you gave: since `held_out_count` is already bounded to `range(1, len(all_studies))` and every study has ≥1 row, the guard can never actually fire. Leaving it in reads as "this can happen," which is misleading for anyone maintaining this later — they might assume there's a real edge case here and go looking for one, or feel obligated to preserve behavior for a scenario that doesn't exist.

One thing to confirm: since this is our own PR/branch, do you want me to just make the code change directly (delete the guard, commit, push), or add it as a review comment instead (so it's tracked as review feedback rather than a silent fix)? Given we're mid-way through the exhaustive-search loop and you already know the reasoning, I'd lean toward just fixing it directly rather than commenting-on-then-fixing our own PR — but your call.

### Yai

let's directly fix. Makes sense to do that, ensure you add rationale in the commit

### Claude

Now verify and commit:

### Claude

All green.

### Claude

Committed as `dbeb67d`. Want to push this to the branch, or hold it locally until we're done with the rest of the review pass?

### Yai

let's end this batch of review before a final push

### Claude

Before I post anything or push, two quick confirmations since both are visible/hard-to-reverse actions:

### Claude

Review posted publicly as `COMMENTED` — [PR #47 review](https://github.com/egsy-intell/team-project/pull/47#pullrequestreview-4785696015), both inline comments included (line 204 on `StratifiedGroupKFold` scoring, line 165 on the threshold constants). Now pushing the dead-code-removal commit:

### Claude

Both done:

1. **Review posted** on [PR #47](https://github.com/egsy-intell/team-project/pull/47) as a `COMMENTED` review with two inline notes (StratifiedGroupKFold cross-check suggestion, and threshold-constants-vs-Task-3.2 suggestion).
2. **Pushed** `dbeb67d` (dead-code guard removal) to `origin/Return-Task-callout-in-Checkpoint-1` — the branch now matches local, `066ae73..dbeb67d`.

That closes out this review batch. Ready when you want to look at the remaining items (the DRY distribution-helper suggestion, or anything else) in a future pass.


# Reviewing Model B, then DRYing its training cells

**Branch:** `Emir_working_main → Fresh_Emir_working`  
**Session:** `c206c0d3`  
**Span:** Aug 12, 07:03–13:57 EDT  
**Exchange:** 6 prompts, 23 responses

**Commits produced:**

- `1925da5` Extract shared CV-results table builder for Model A/B training
- `de5d2de` Split Model B's cell into training + display, matching Model A
- `8b69f44` Revert T7 to Pending: guiding questions not yet answered in prose

[← back to the pairing-log timeline](https://egsy-intell.github.io/team-project/ai/ytorresv.html)

---

### Yai

The teammate working on task T6 asked me to take a look at his progress,
and give some additional feedback. I already shared with him partial
validation results (https://github.com/egsy-intell/team-project/pull/82),
as well as informed him about the work Raj did for Model A tuning
(https://github.com/egsy-intell/team-project/pull/79). Those two sources
should be good for him, but I wonder if there's anything else, base on the
diff in his PR: https://github.com/egsy-intell/team-project/pull/83

Could you provide some ToDos he could follow up with? Starting with helping
out to merge the partial validation work?

### Claude

I'll pull up the PR diffs to see what's actually there before drafting
ToDos.

### Claude

CI is already failing on this PR — let me pull the actual error logs
before writing feedback.

### Claude

Confirmed and traced through everything. Here's the ToDo list for your
teammate on T6, ordered so the earliest items unblock the rest.

## 1. Merge PR #82 first (as you offered)
It's `MERGEABLE`/open with green CI. Get it in before he does anything
else — his T6 cell currently only pulls `tapwater_train_df`,
`tapwater_test_df`, `preprocess_tapwater_features` off the checkpoint_2
embed, but he'll need `score_model()`, `evaluate_tier_model`,
`RECALL_FLOOR`, etc. from #82's harness once he wires Model B into it (see
#4 below).

## 2. Fix the CI failures already on PR #83 — it's currently red
Ran the checks: `Spelling, lint & notebook execution` is failing with 4
test failures. Concrete fixes:
- **`MultipleDefinitionError: 'StratifiedGroupKFold' was defined by
  another cell`** — `checkpoint_3.py` already imports
  `StratifiedGroupKFold` at
  [checkpoint_3.py:80](../../../notebooks/checkpoint_3.py#L80) for Model
  A's grouped CV
  ([checkpoint_3.py:291](../../../notebooks/checkpoint_3.py#L291)). The
  new T6 cell re-imports it as a second top-level global, which breaks
  execution of **both `checkpoint_3.py` and `index.py`** (since index
  embeds it) — this is why 4 tests failed, not just 1. Fix: drop the
  re-import and just take `StratifiedGroupKFold` as a cell parameter like
  the Model A cell does.
- **ruff `I001`** (unsorted imports), **`DTZ005`** (`datetime.now()` needs
  a `tz`), **`E501`** (the `joblib.dump(...)` line is 103 chars, limit is
  79). Run `uv run ruff format notebooks/checkpoint_3.py && uv run ruff
  check --fix notebooks/checkpoint_3.py`, then hand-fix the
  `datetime.now()` call (ruff won't autofix DTZ005) and rewrap the
  `joblib.dump` line.
- General ask: `uv run pytest tests/ -v` locally before pushing — all four
  failures would have caught this pre-CI.

## 3. The training cell doesn't actually expose Model B to anything
downstream
The cell ends with `return {"model": ..., "preprocessor": ...,
"cv_results": cv_results, "artifact_path": artifact_path}` — an anonymous
dict literal, not named variables. marimo only wires up cross-cell
references for names a cell returns *by identifier* (that's how
`model_a_best_estimator` at
[checkpoint_3.py:545](../../../notebooks/checkpoint_3.py#L545) becomes
usable elsewhere). As written, no other cell can reach Model B's fitted
estimator at all — this won't error in CI today (nothing references it
yet), but it'll silently block T7 the moment someone tries. Needs `return
model_b_best_estimator, model_b_preprocessor, model_b_cv_results,
model_b_artifact_path` bound to real variables in the cell body.

## 4. Model B isn't shaped to plug into the #82 scoring harness
This is the one worth flagging loudest. `score_model(pipeline, df,
model_name)` from #82 calls `pipeline.predict(df[model_predictors])`
directly on raw columns — it works for Model A because
`model_a_best_estimator` is a full `Pipeline` with `"preprocessor"` +
`"model"` steps
([checkpoint_3.py:500-545](../../../notebooks/checkpoint_3.py#L500-L545)),
fit end-to-end on raw predictor columns. T6 instead calls
`preprocess_tapwater_features()` to pre-transform into arrays, then fits a
bare `RandomForestClassifier` on those arrays — that estimator has no
`.predict()` path from a raw dataframe and will break the moment it's
passed into `score_model()`. Fix: wrap it as `Pipeline([("preprocessor",
ColumnTransformer(...)), ("model", rf)])` fit on
`tapwater_train_df[model_predictors]`, mirroring Model A's pattern
exactly.

## 5. Feature-set mismatch between Model A and Model B
`preprocess_tapwater_features()` (checkpoint_2.py) selects features by
**denylist** (`_LEAKAGE_AND_ID_COLS`), but Raj's #79 deliberately moved
Model A to an **allowlist** (`model_predictors`) specifically "to prevent
PFAS/TQ leakage." Training Model B through the denylist helper risks a
different, less-audited feature set than Model A — which both muddies the
T7 comparison and potentially reopens the leakage question #79 closed. He
should reuse `model_predictors` for Model B too, or explicitly
flag/justify why it differs.

## 6. Check the model-artifact side effect
`os.makedirs("data/models", exist_ok=True)` + a timestamped
`joblib.dump(...)` runs on every notebook execution — including CI's
`marimo export html` smoke test on every push. Worth confirming
`data/models/` is gitignored and whether persisting a new artifact file
per CI run/local edit is actually wanted, or if this should be skipped in
the exported/CI path.

Want me to leave these as review comments on PR #83, or would you rather
he see this as a message directly?

### Yai

would you agree that Emir should follow the same training strategy as Raj,
overall?

### Claude

Partially — the *contract* should match, but not every implementation
detail.

**Should match:** same feature allowlist (`model_predictors`), same
grouped CV by `study_group` (`StratifiedGroupKFold`), and the same
end-to-end `Pipeline` shape (preprocessor + model steps) so `score_model()`
works identically on both. That's not optional — it's what makes T7's
Model A vs. Model B comparison fair, and it's the fix for #4/#5 above
regardless of strategy questions.

**Shouldn't necessarily match:** the specific preprocessing steps Raj
tuned for a linear model (StandardScaler, log1p skew correction) don't do
anything useful for a tree ensemble — RandomForest is scale-invariant, so
those transforms are harmless but pointless overhead to copy verbatim.
More importantly, don't copy Model A's *hyperparameter-selection
criterion* — the class-weight ad hoc finding you already documented in #82
shows picking `class_weight` purely on CV macro-F1 caused Model A to
collapse to the majority class on the held-out set. That's a pitfall to
avoid repeating for Model B, not a pattern to inherit. Worth flagging that
nuance to Emir specifically, since "follow Raj's strategy" could be read
either way.

### Yai

ok, let's post a comment in the PR about your findings. I'll make sure to
relay that he shouldn't pick based by Macro F1 alone

### Claude

Posted:
https://github.com/egsy-intell/team-project/pull/83#issuecomment-5266212640

Covers the merge-#82-first ask, the 4 CI failures with fixes, the two
structural issues (dict-return not exposing Model B, and the pipeline-shape
mismatch that'll break `score_model()`), the feature-set/leakage concern,
the artifact side effect, and the strategy note on the
contract-vs-implementation split — including the class-weight/macro-F1
pitfall, so it's on record even before you relay it directly.

### Yai

model B landed: https://github.com/egsy-intell/team-project/pull/84
Can you evaluate for completeness? Also, make sure that we're keeping the
code DRY and imports in order. Otherwise, let's go through clean up rounds
-- same way we did with Model A.

### Claude

We already have this branch checked out locally, and #82 is merged into it
(`ce66a39`) — good, that resolves my #1 ask. Let me read the actual current
file state to check each of the earlier findings and look for DRY/import
issues.

### Claude

Read through the full diff against `main` (now that #82 is merged in) plus
the current file state. Good news first: the three structural issues I
flagged on #83 are genuinely fixed, and fixed well.

## What's resolved from the last review round
- **CI is green** — all three checks pass.
- **Anonymous dict return → fixed.** The cell now returns
  `(model_b_best_estimator,)` as a real named variable, so `score_model()`
  can consume it downstream.
- **Pipeline-shape mismatch → fixed, elegantly.** Instead of redefining a
  second `ColumnTransformer`, he does
  `clone(model_a_best_estimator).set_params(model=RandomForestClassifier(...))`
  — this clones Model A's *entire* unfitted preprocessing structure (same
  `model_predictors` allowlist, same skew-log1p/imputer/scaler/one-hot
  definitions) and only swaps the final estimator. That's the DRY move I'd
  have asked for: zero duplicated preprocessing code, and it automatically
  resolves the feature-set-mismatch concern too, since Model B trains on
  the exact same allowlisted columns as Model A rather than the
  leakage-prone denylist helper.
- **Artifact side effect → removed entirely.** No more
  `joblib.dump`/`data/models` writes on every notebook run.
- **T6 marked Complete in the CSV**, consistent with the task actually
  being done.

## Two things worth another cleanup pass

**1. Completeness gap on T7.** This PR also stripped T7's `task_callout()`
and marked it `Complete` in the CSV — but T7 is Yai/Somya's task, not
Emir's, and its three guiding questions (does either model clear the 0.70
recall floor? are errors concentrated in one study? does the comparison
change the team's recommendation?) are never answered in prose — only the
raw comparison table/plot are shown, then the notebook jumps straight to
T8's callout. The scoring plumbing is genuinely done, but "Complete"
implies the interpretive writeup is too, and it isn't yet. Worth either
adding that narrative paragraph or reverting T7's status until it is.

**2. Duplicated CV-summary boilerplate.** The "build a `Selected` column,
sort it to the top, assemble a one-row training-summary DataFrame" block is
hand-rolled almost identically in both the Model A cell
([checkpoint_3.py:829-894](../../../notebooks/checkpoint_3.py#L829-L894))
and the new Model B cell — same shape, different param names. Per the
repo's own DRY convention (the `print_sections()`/`make_plot_grid()`
precedent), this is a good candidate for a shared helper like
`summarize_cv_results(grid_search, param_labels)` that both cells call.

**3. Minor structural inconsistency.** Model A splits training and
summary-display into two cells (training cell returns
`model_a_cv_results`/`model_a_training_summary`, a separate `hide_code`
cell displays them). Model B does both in one cell and doesn't return
`model_b_cv_results`/`model_b_training_summary` — harmless today since
nothing else references them, but per the repo's underscore-prefix
convention they should either be `_`-prefixed (since they don't cross a
cell boundary) or the cell should be split to match Model A's pattern. I'd
lean toward splitting, for symmetry with the sibling section.

Imports checked out clean — no unused imports, ordering is sorted, no
leftover collisions.

Want me to post this as a PR comment on #84 the same way as last time?

### Yai

Emir's timezone is different so let's do the cleanup on his behalf. Go
ahead and address in logical commits

### Claude

I'll do this as two focused commits: extracting the shared CV-results
helper (DRY), then splitting Model B's cell to match Model A's
train/display structure. Let me implement both.

### Claude

Now let me add the shared helper cell right after `tier_model_scoring`:

### Claude

Now update Model A's training cell to use the helper:

### Claude

Now let's run checks and commit this first piece:

### Claude

Let me re-read the file since ruff reformatted it, then verify the Model A
cell reads correctly and proceed to the Model B split.

### Claude

Good, Model A's cell now uses the helper cleanly. Let's run the test suite
to confirm this first change is solid before committing.

### Claude

Passing. Let's commit this first piece.

### Claude

Now let's do commit 2: use the helper in Model B's cell **and** split it
into training/display cells to match Model A's structure.

### Claude

Now I'll replace this cell with a training cell (using the helper,
returning all three values) plus a separate display cell.

### Claude

Full suite passes, including `index.py` (which embeds checkpoint_3).
Committing the second piece.

### Claude

Both cleanup commits are in locally, and the full test suite (all 6
notebooks) passes clean. Two things before I go further:

### Claude

Now revert the CSV status for T7:

### Claude

All green. Committing this third piece, then pushing all three commits.

### Claude

CI is running now. I'll check back once it finishes rather than poll
manually.

### Claude

I've pushed all three cleanup commits to `Fresh_Emir_working` (updating PR
#84):

1. **Extract shared CV-results table builder** —
   `build_cv_results_table()`, used by Model A's training cell.
2. **Split Model B's cell into training + display**, using the same
   helper — matches Model A's structure exactly now.
3. **Revert T7 to Pending** — restored its `task_callout()` and CSV
   status, since the guiding questions aren't answered in prose yet.

All local checks pass (ruff, marimo check, full `pytest tests/` — 38
passed). CI just kicked off on the PR; I'll let you know when it's green.

### Yai

Check `gh pr checks 84 --repo egsy-intell/team-project` and report the
result to the user.

### Claude

All three checks are green on PR #84 — the cleanup commits are in and CI
is passing.

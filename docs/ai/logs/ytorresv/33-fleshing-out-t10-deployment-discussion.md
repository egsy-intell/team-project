# Fleshing out T10's deployment discussion, then closing T10/T11

**Branch:** `E_t10`  
**Session:** `f63333fd`  
**Span:** Aug 13, 23:07–23:37 EDT  
**Exchange:** 5 prompts, 24 responses

**Commits produced:**

- `6a109a8` Add site-sparsity, predictor-scope, and regional-scope context to Step 5 deployment discussion
- `d0ec21f` Mark T10/T11 complete: strip task callouts, move public-repo link to References

[← back to the pairing-log timeline](https://egsy-intell.github.io/team-project/ai/ytorresv.html)

---

### Yai

T10 landed in PR (https://github.com/egsy-intell/team-project/pull/90, available locally), and we need to add some additional context:
1. emphasis on site-sparsity. Use calculated sparsity numbers to emphasize the need for more data. To improve the numbers, we need to scale data sampling
2. Use mcmahon's findings and modeling to make the case of adding additional features, like chemical composition which may be easier to detect/sample (this needs to be fact-checked).
3. Use mcmahon and peer review feedback: "The data seems fine but I doubt whether the project is worth doing at all given how broad the scope is relative to the scale of the problem. It might be better to limit the analysis to a specific state so the landform and geographic analysis can be more precisely tailored and you don't have as many confounding variables." It might be better to focus on regional-based modeling, and see if that helps. This is what McMahon did (east coast only), so our results could improve.

### Claude

I'll start by looking at the current state of the repo and PR #90 to understand where T10 lives and what needs updating.

That worked. Let me extract the sparsity numbers from the rendered HTML.

Now let's update the "Pitfalls and lessons learned" and "Recommendation" cells.

No line-length violations. Let's run ruff and marimo check, plus re-export to confirm the notebook still executes and produces the numbers I expect. All the key numbers render properly: 236 sites, 36 states, 9 singleton states, 35.6% concentration, and the McMahon comparisons. Let's run the full test suite to be sure.

All checks pass — lint, ruff, execution, and spelling. Let's also confirm `checkpoint_3.py` still embeds cleanly into `index.py` and do a final review of the diff.

### Claude

All three pieces of context are now added to `notebooks/checkpoint_3.py`'s T10 deployment discussion, with tests/lint passing:

**1. Site-sparsity, with real numbers** — extended the benchmarking cell to compute (from the actual `tapwater_train_df`/`tapwater_test_df` data, not estimates): 236 combined sites span only 36 states/territories, 9 of them single-site, with the 3 best-covered states (IL, MN, CA) holding 35.6% of everything. These now flow into the Pitfalls and Recommendation sections, explicitly framing this as "a data-collection problem before it is a modeling one" and calling for scaling up site sampling.

**2. Chemical composition as a candidate feature** — I fact-checked this against the McMahon PDF. Their top-5 predictors are tritium, distance to fire-training area, DOC, % urban land use, and ΣVOC — 3 of 5 are chemical measurements outside this project's current land-use-only predictor set. I added the specific, sourced claim that DOC/VOC are the more *feasible* additions of the three, since McMahon's paper explicitly notes tritium is "rarely collected... because it requires specialized isotope-lab analysis," while DOC/VOC use standard water-quality lab methods. I flagged as an open item that it's unconfirmed whether a Seawolf-comparable source even reports DOC/VOC for our training sites — that needs checking before committing to it.

**3. Regional scope, per peer feedback + McMahon precedent** — added the new peer-review item to the "Feedback selected for integration" cell (now 3 items, not 2, so that summary stays accurate), and rewrote the Recommendation's closing paragraph: it now weighs a regional pilot as a *stronger* next step than the prior draft credited it, citing McMahon's narrower 5-aquifer-system/eastern-US design and its far better holdout metrics (0.96 sensitivity, 0.72 specificity) as consistent with the reviewer's concern — while still noting the caveat that it's not a controlled comparison and would need its own data/evaluation plan.

One thing worth double-checking: I attributed the new scope-related peer feedback to "Check-In #2" based on repo convention (that's the only peer-review round documented), but you gave me the quote directly — if it's actually from a different round, that label should change.

T10's `task_callout` is still open (status `Pending` in the CSV) since this felt like an in-progress enhancement rather than a final close-out — let me know if you'd like me to mark it `Complete` and strip the callout per the repo's task-tracking convention.

### Yai

let's do a header weight check. Also let's take a minute to call T11 complete and move it to the index. It's likely it can sit under the references section. Finally, let's make sure that T10 and T11 are marked complete.

### Claude

Header hierarchy checks out cleanly — every notebook's own top-level heading is H2, nesting downward without skipped levels, and there's exactly one H1 (in index.py, per the single-H1 rule). No fixes needed there. Now let's look at footer.py's References section and the T11 content to plan the move.

Now remove the now-unused `checkpoint_1_app`/`task_callout` plumbing from the top of the file, add the "Public codebase" content to `footer.py`'s References section, and update the task-plan CSV to mark T10 and T11 complete.

Confirmed that's pre-existing formatting debt (unrelated to my edits) — `ruff check` (the linter actually enforced in CI) already passes cleanly. Full suite passes. Let's clean up scratch files and do a final diff review.

### Claude

Done. Summary:

**Header weight check** — clean, no fixes needed. Traced every heading across `checkpoint_1/2/3.py`, `footer.py`, and `index.py`: exactly one H1 (the report title in `index.py`), every notebook's own top-level section is H2, and nesting goes strictly H2→H3→H4→H5 with no skipped levels anywhere.

**T11 moved to References** — pulled the "Public codebase" paragraph out of `checkpoint_3.py` and appended it as a new `### Public codebase` subsection at the end of `footer.py`'s `## References` cell, so it now shows up once, near the end of the combined report, per the repo's "trailing content lives in `footer.py`" convention.

**T10 and T11 marked complete**:
- Stripped both `task_callout()` blocks from `checkpoint_3.py` — the actual T10 deployment-discussion content stays untouched, since that's real report body, not scaffolding.
- Since both `task_callout` usages were the only reason `checkpoint_3.py` imported `checkpoint_1.py` directly, removed that now-dead import/embed cell too.
- Set both rows to `Complete` in `planning/checkpoint-3/checkpoint3_task_plan.csv`.

Full test suite (38 passed, 1 pre-existing skip for missing `pypandoc`) and `ruff check`/`marimo check` all pass on the touched files.

### Yai

could you disambiguate VOC here?

### Claude

Good catch — you're right, this is inconsistent. I spelled out "dissolved organic carbon (DOC)" on first use in that same paragraph, but never expanded VOC anywhere in the report before using it three times. Fixed — VOC now expands to "volatile organic compound (VOC)" on first use, matching the DOC pattern right next to it. All checks still pass.

### Yai

alright let's update the PR's description based on changes and make to commit logically, and push to origin

### Claude

Now let's split this into two logical commits. Let me use a non-destructive patch-staging approach: build a partial patch for just the content-addition hunks and stage it with `git apply --cached`, without ever touching the working tree.

Both diffs confirm a clean split. Now let's create the blob and stage it for commit 1, without touching the working tree. Commit 1 done. Now let's stage and commit the remaining working-tree changes (the T10/T11 cleanup + footer.py + CSV) as commit 2.

All pass. Now let's stage and commit. Working tree is clean and matches exactly what was intended. Now let's update the PR description and push.

### Claude

Pushed successfully. Final state:

**Two logical commits** on `E_t10` (PR #90):
1. `6a109a8` — Add site-sparsity, predictor-scope, and regional-scope context to Step 5 deployment discussion
2. `d0ec21f` — Mark T10/T11 complete: strip task callouts, move public-repo link to References

**PR #90 description** updated to reflect the full scope: pull/90.

All tests, lint, and marimo checks pass on the pushed state. Splitting this into two commits took a bit of surgery since both logical changes landed in the same working tree — I isolated them by constructing an intermediate file state via git's plumbing (`hash-object`/`update-index`) rather than a destructive `git checkout`, so nothing was ever at risk of being discarded.

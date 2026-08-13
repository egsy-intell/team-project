# Fixing heading hierarchy, then drafting and closing out T7

**Branch:** `validation-all-models`  
**Session:** `6305be49`  
**Span:** Aug 12, 21:52–23:13 EDT  
**Exchange:** 9 prompts, 76 responses

**Commits produced:**

- `43e90fb` CP-3: fix checkpoint_3.py heading hierarchy and dependency header
- `36b7c5f` CP-3: fix checkpoint_2.py and footer.py heading hierarchy
- `49a5116` CP-3: draft T7 findings and consolidate class-weight diagnostic
- `85a2fca` CP-3: carry T7 findings into T8-T10 guiding questions
- `24ae8a7` CP-3: close out T7

[← back to the pairing-log timeline](https://egsy-intell.github.io/team-project/ai/ytorresv.html)

---

### Yai

All modeling tasks are done, and now I need to make sense of the results in prose and answer the guiding questions for T7. First, let's discuss the results, and then think about how to wrap findings in a cohesive narrative, taking into account all the report so far

### Claude

Let me get the actual computed results by running the notebook, since marimo's reactive outputs aren't stored in the `.py` source itself.

### Claude

checkpoint_3.py's PEP 723 header is missing `matplotlib` as a dependency even though the notebook imports and uses it — that would break `uvx marimo edit --sandbox` for anyone running this standalone.

### Claude

That's a real bug — I'll fix checkpoint_3.py's dependency header before continuing (it's needed to actually get results anyway).

### Claude

Good, it exported cleanly now. Let me pull the actual computed numbers out of the rendered HTML.

### Claude

app.run() is a plain sync method — no asyncio wrapping needed. Let me use that directly.

### Claude

Let me check what Step 4 predicted about the two models, to answer T7's third guiding question properly.

### Claude

This raises something worth flagging before we write prose: Step 3's evaluation plan and the Step 4 proposals both describe a **two-stage selection rule** — discard CV candidates below the 0.70 recall floor, *then* rank survivors by macro-F1 — but T5/T6's actual code selects purely by macro-F1 (the notebook says this explicitly). Let me check whether any untried candidate in the grid would've cleared the floor, since that changes how big a deal this is.

### Claude

One more check before I bring this to you — Model B's actual code doesn't set `class_weight="balanced"`, even though Step 4's Model B proposal explicitly commits to it ("We will use `class_weight="balanced"`"). Let me test whether that fixed choice would've mattered, the same way the existing Model A diagnostic callout tests `balanced` vs `unweighted`.

### Claude

This inconsistency (Model A's headings bumped to `#####` while Model B's parallel section stayed `####`) would read as broken structure in the published report, so I'm fixing it to keep both sections at the same level.

### Claude

Now I have real numbers. Here's what the held-out evaluation actually shows.

## Held-out results

| Metric | Model A (logistic) | Model B (random forest) |
|---|---|---|
| `mcl_exceedance` recall | **0.0000** (0/14) | **0.0714** (1/14) |
| Macro F1 | 0.2347 | 0.2825 |
| `mcl_exceedance` precision | 0.0000 | 1.0000 (1/1) |
| Meets Step 3 criteria | No | No |

Both models collapse toward the majority tier on the 46 held-out sites. Model A predicts `within_reduced_monitoring` for *all 46*, missing every one of the 7 `above_trigger` and 14 `mcl_exceedance` sites. Model B breaks the tie on exactly one site — it's the only reason its recall/precision aren't both zero too. Neither comes remotely close to the 0.70 recall floor.

## Two things I found while pulling real numbers (not just prose issues)

1. **Fixed a real bug**: `checkpoint_3.py`'s PEP 723 header was missing `matplotlib`, even though the notebook imports and plots with it — `uvx marimo edit --sandbox` would've failed for anyone running this standalone. Fixed.
2. **Two methodology deviations worth disclosing, not fixing**: Step 3/Step 4 both describe a two-stage selection rule (discard CV candidates below 0.70 recall, *then* rank by macro-F1), but T5/T6's code selects by macro-F1 alone. And Step 4's Model B proposal commits to `class_weight="balanced"`, but the T6 code leaves it unweighted (default `None`). I tested both counterfactuals:
   - Best CV recall anywhere in either grid tops out at 0.52 (Model A) / 0.33 (Model B) — so the two-stage rule wouldn't have found a floor-clearing candidate either. Doesn't change the conclusion.
   - Forcing `class_weight="balanced"` on Model B's exact selected hyperparameters raises held-out recall to 0.1429 (2/14) but drops precision to 0.2857 — it would now *fail* the precision floor it currently (fragile, n=1) passes. Also doesn't flip the conclusion, but it's a real "we said X, we shipped Y" gap that the writeup should own rather than let a reader discover.

Neither deviation changes the bottom line, so I'd surface both briefly rather than rerun tuning.

## Reading the three T7 questions against this

**Q1 — recall floor:** Neither model clears it. Model A fails completely (0 recall); Model B clears it only by a single correct prediction out of 14. This isn't "close but not quite" — it's a near-total generalization failure on the tiers that matter, despite the same predictors producing CV `mcl_exceedance` recall of 0.41–0.52 during training. That gap between CV and held-out is itself a finding: with only 190 training rows across 7 study groups, held-out performance on 3 entirely unseen studies is highly volatile.

**Q2 — error concentration:** Sharply concentrated, and not randomly — it tracks each study's actual risk composition.
- Cape Cod: 92% error (Model A) / 85% error (Model B) — and Cape Cod's true composition is 9/13 `mcl_exceedance`, 3/13 `above_trigger`. It's almost entirely high-risk sites, exactly where a majority-collapsed model is guaranteed to fail.
- Minnesota: 33% error for both — mixed composition (18/4/5).
- Northeast Iowa: 0% error for both — but trivially, since all 6 Iowa test sites are `within_reduced_monitoring` already. A model that always predicts the majority tier gets Iowa "right" by construction, not by skill.

So the honest framing isn't "errors cluster in one study" as a standalone fact — it's that both models' errors track tier composition, which happens to concentrate in Cape Cod. That's a materially different (and more damning) claim than geographic variance alone.

**Q3 — does this change the Step 4 recommendation?** Step 4's own bar for Model B was: only prefer the ensemble if it "meaningfully outperforms" Model A, since it costs interpretability. It does not meaningfully outperform — its recall and macro-F1 gains reduce to catching one additional site out of 46, and its "perfect" precision is a statistical fluke of n=1. Given neither model passes Step 3's criteria, I'd frame T9/T10 around Model A as the retained choice on interpretability grounds (per Step 4's own tie-breaker), while being explicit that **neither is deployment-ready** — this is a negative result, not a "pick the winner" result.

Want to work through drafting the T7 prose cell together now, or talk through the framing more first (especially how blunt to be about "neither model works" given this doubles as T9's benchmarking input)?

### Yai

let's walk through the framing

### Claude

Let me lay out the shape I'd propose, then flag the two or three calls that are really the team's to make, not mine.

## Overall arc

T7's job is narrower than it might feel right now: answer its three questions with evidence, not deliver the full verdict. T9 does the benchmarking narrative (including the McMahon comparison and the sparsity tie-in), T10 does deployment. So T7 should land clearly on "neither model clears the bar" and *why*, but stop short of the "so here's what we recommend for deployment" language — that's T10's job, and T7 overreaching into it is exactly the kind of duplicated-narrative problem AGENTS.md flags.

Proposed internal order for T7's answer, evidence-first:
1. **Headline finding** (Q1): neither model clears 0.70 recall — state the two numbers immediately, no windup.
2. **Why** (this is where the CV-vs-held-out gap belongs): CV recall was 0.41–0.52 for Model A's grid, already below floor as a *tuning-time diagnostic* — so held-out failure isn't a surprise reveal, it's the CV signal playing out on unseen studies. This directly answers "what does that imply for T9" from Q1 without T7 having to write T9's content.
3. **Where** (Q2): the error-by-study table, but framed by composition, not just geography — Cape Cod's 92%/85% error rates track its 9/13-mcl_exceedance composition, Iowa's 0% error tracks its all-majority-tier composition. This is the more defensible claim and it's the one that sets up T9's sparsity question well, since "errors track tier composition" is a cleaner causal story than "errors track which study."
4. **Recommendation delta** (Q3): does this change Step 4's prediction — no, if anything it confirms Step 4's own tie-breaker (Model B must "meaningfully outperform" to justify losing interpretability; it doesn't — one site out of 46).

## Where the two methodology deviations go

I'd put both in a single short paragraph or callout right after the headline numbers — not buried, not dwelled on. One line each: "selection used macro-F1 alone rather than the two-stage recall-floor rule; the full grid's best CV recall (0.52) still falls short, so this doesn't change the outcome" and the same shape for the class_weight gap. Terse, disclosed, moved past.

## Calls I don't think are mine to make

### Claude

Both defaults taken. On the class_weight deviation specifically — I'd fold it into the same disclosure paragraph as the selection-rule one rather than giving it its own big callout (which would visually compete with the existing Model A diagnostic and risk making the section feel padded, working against the "lead with results, lighter on detail" feedback already threaded through T9/T10).

Here's a draft of the T7 findings cell — reacting to this before I touch the file:

### Claude

Good catch — let me pull every heading in this section so we can check the flow together.

### Claude

This is a bigger issue than I expected — let me check checkpoint_3.py's own top-level heading against the "one H1 for the whole report" rule from AGENTS.md, since I now suspect it violates it.

### Claude

Good instinct to zoom out — I found something bigger while checking. checkpoint_3.py's opening heading is `# Step 5: ...` — a single `#` (H1) — but AGENTS.md's convention (and checkpoint_1.py's actual practice) is that only `index.py` gets an H1; checkpoints start at `## Step N` (H2). checkpoint_2.py has the identical bug (`# Step 3-4...`). Once `index.py` stacks everything, that's **three H1s** in one report instead of one.

That's a report-wide structural bug, not just a "this section" issue. Let me fix it in checkpoint_3.py (in scope) and flag checkpoint_2.py separately since it's a different file.

### Claude

This is bigger than a one-line fix — bumping the title from H1 to H2 means every subsection below it needs to shift down one level too, or the hierarchy breaks (H2 body headings would become siblings of the title instead of children). Let me map every heading in the file first.

### Claude

Now let me disambiguate the duplicate confusion-matrix headings and check for leftover task-ID references in prose (T5/T6 are marked Complete in the CSV, so per AGENTS.md's "task-tracking prose is scaffolding" rule, those IDs shouldn't linger in reader-facing text).

### Claude

Line 1077's heading (`##### T5 findings summary`) plus several body sentences still reference "T5" even though T5 has no `task_callout()` left and is marked Complete — the callout got removed at some point but the prose cleanup was never finished. Let me look at the full context before rewriting.

### Claude

Now the remaining T5 references — the model coefficient-analysis section:

### Claude

Now the stale docstring — T6 already landed, and Model B already calls this function (used in the held-out error-breakdown cells above):

### Claude

Now the duplicate "Confusion matrix (held-out)" headings — disambiguating to match their sibling naming pattern (`Model A: held-out scoring`, `Model A: held-out error rate by study`):

### Claude

Let me verify the full structure now and check checkpoint_2.py's matching H1 bug before running validation.

### Claude

Hierarchy is clean now: H2 title → H3 major sections (Foundations, Check-In #2, Training, Prediction/Evaluation, Deployment, Public codebase) → H4 subsections → H5 fine-grained results. Let me validate the file still parses and runs correctly after all these edits.

### Claude

Good — check and lint both pass. Let me also re-export to confirm it still executes end-to-end with real output.

### Claude

Clean export, no errors. Everything's structurally sound. Here's where things stand:

## What I fixed in checkpoint_3.py

1. **Missing `matplotlib` dependency** in the PEP 723 header (real bug — would've broken standalone `uvx` runs).
2. **H1→H2 title bug**: the notebook's own title was `#` instead of `##`, which would've produced three H1s once `index.py` stacks all checkpoints. Fixed, and cascaded every subsection down one level to keep the hierarchy consistent (full mapping shown above — H2 title → H3 major sections → H4 subsections → H5 fine-grained results).
3. **Duplicate ambiguous headings**: both models had an identically-named "Confusion matrix (held-out)" heading with no way to tell them apart out of context; now "Model A: confusion matrix (held-out)" / "Model B: confusion matrix (held-out)", matching the naming pattern their sibling headings already used.
4. **Stale task-ID leakage**: T5 has no `task_callout()` left (already Complete) but its body prose still said "T5 uses...", "T5 audits...", "T5 avoids..." in five places, including the section heading itself (`T5 findings summary` → `Findings summary`). Reworded to first person/normal prose. Also fixed a stale docstring that still said "Model B calls this the same way once T6 lands" — T6 landed, Model B already calls it.

All verified with `marimo check`, `ruff check`, `ruff format --check`, and a clean `marimo export html`.

## One thing I didn't touch

**checkpoint_2.py has the identical H1 bug** (`# Step 3-4: Model Selection...` instead of `##`), which would need the same title-fix-plus-cascade treatment. I left it alone since it's outside today's scope and not a file we're pairing on right now — want me to fix it too, or flag it for whoever owns that file?

### Claude

Committed. Now let's fix checkpoint_2.py the same way.

### Claude

Good — 1662 lines total, so line 1641 is near the end, matching the last heading section. Let me apply the same bump script.

### Claude

Regex bug on my end — the quoted-heading lines using `mo.md("...")` syntax didn't match. Let me fix those 7 directly.

### Claude

All 45 headings bumped. Let me verify the full hierarchy and validate the file.

### Claude

All clean. Now let's confirm the full pipeline still executes end-to-end — checkpoint_2 → checkpoint_3 → index all chain together via `embed()`.

### Claude

All three exports are clean, including the full stacked `index.py`. Let me verify there's now exactly one H1 in the combined report.

### Claude

The static export is a client-hydrated SPA, so grepping for literal `<h1>` tags won't work — the source-level heading count is the real check, and I've already confirmed that systematically. Let me just double check `footer.py` isn't hiding a similar issue.

### Claude

One more — `footer.py`'s "# Conclusion" is also an H1 (which would be a second H1 stacked into the report), and it skips straight to H3 subsections beneath it without an H2 in between. Bumping it to H2 fixes both issues at once (its H3 children become correctly nested, and it lines up with References/AI usage appendix, which are already H2).

### Claude

Let's run the full test suite once as a final safety check before committing.

### Claude

All 38 tests pass. Let me commit checkpoint_2.py and footer.py together.

### Claude

Both commits are in. Here's the full state:

## Committed

**`43e90fb`** — checkpoint_3.py: missing matplotlib dependency, H1→H2 title + full cascade, disambiguated confusion-matrix headings, stale T5/T6 prose cleanup.

**`36b7c5f`** — checkpoint_2.py and footer.py: same H1→H2 title bug (checkpoint_2's own title, plus footer.py's Conclusion, which also skipped straight from H1 to H3 — fixed in one edit since bumping to H2 resolves both).

All three files pass `marimo check`, `ruff check`, `ruff format --check`, and the full `uv run pytest tests/` suite (38 passed). The stacked `index.py` export also runs clean end-to-end.

## Where this leaves the report

Every notebook now has exactly one H1 for the whole stacked report (in `index.py`), with each checkpoint's own title at H2 and consistent nesting beneath it — checkpoint_1.py was already correct; checkpoint_2, checkpoint_3, and footer had all drifted.

## Back to T7

The header work is done and committed. Next up is still the T7 findings cell itself — the draft I put together earlier (headline recall-floor miss → CV-vs-held-out gap and the two methodology disclosures → error concentration by composition → recommendation delta) is ready to turn into an actual cell, sitting as a new `#####` heading after "Model comparison: Model A vs. Model B" and before T8. Want to pick that back up now?

### Yai

yes, also, let's examine the model A callout and see if it makes sense to keep, compress or remove

### Claude

Good call — let me pull up where it sits and think through the options before we decide.

Looking at it: this callout is Model-A-only, and its closing line ("confirm `balanced` isn't dropped for Model B on a CV-macro-F1 technicality") is a dangling forward-reference — we now know the answer (Model B's code never set `balanced` at all, and I already tested forcing it: recall rises to 0.1429 but precision drops to 0.2857, still failing both floors). If we leave this as-is, we'd either duplicate the same disclosure in the new T7 findings prose, or leave Model B's half of the story untold right next to a callout that explicitly asks for it.

### Claude

Let me pull current line numbers and rewrite the callout.

### Claude

Now let's replace the callout with the consolidated version:

### Claude

Now let's write the T7 findings cell and insert it after the model comparison chart, before the T8 section.

### Claude

Let's validate this compiles, lints, and executes correctly with the real numbers filled in.

### Claude

The table rows exceed 79 columns. Let me shorten the headers and cell content to fit.

### Claude

All fit under 79 with `A unweighted`/`A balanced`/`B unweighted`/`B balanced` headers. Let me update the table.

### Claude

All clean. Now let's actually run the notebook and check the rendered prose with the real numbers substituted in.

### Claude

Let me check whether any currently-returned (global) names in checkpoint_3.py are actually only used within their own defining cell now — candidates that should be demoted to `_`-prefixed locals per the AGENTS.md convention.

### Claude

Let me look at the actual cells I just added/edited directly, since my automated cross-cell check found nothing — I might be missing something visible in the source itself.

### Claude

That's it exactly — `_comparison_df` in the "Model comparison" cell already holds the same three headline numbers my new cell was re-deriving from scratch via `.set_index().loc[...]` chains on the raw `held_out` dicts. Since another cell now needs that data, it should stop being cell-local. Let me fix it.

### Claude

Now let's simplify the findings cell to consume `comparison_df` instead of re-deriving the same numbers:

### Claude

Also fixing the T5/T6 prose I accidentally reintroduced in this new cell — same cleanup rule I just applied elsewhere:

### Claude

Now let's re-validate everything end to end.

### Claude

Clean. Let's run the full test suite and re-render the findings cell to confirm the numbers still come through correctly after the refactor.

### Claude

All 38 pass. Let's confirm the rendered output still has the right numbers post-refactor.

### Claude

Numbers all check out correctly after the refactor. Let's commit this.

### Claude

Committed. Here's where T7 stands now:

## What's done
- **T7 findings cell** drafted and validated, answering all three guiding questions with real held-out numbers, sourced from `comparison_df` (shared, not re-derived) and `model_a_cv_results`/`model_b_cv_results`.
- **Class-weight callout** consolidated into one table covering both models, closing its own dangling forward-reference.
- Full test suite passes (38/38), all three notebooks export clean individually and stacked through `index.py`.

## Still open for T7
The task_callout("T7", ...) cell itself is still sitting there, and T7 is still "Pending" in `checkpoint3_task_plan.csv` — per AGENTS.md's task-scaffolding rule, finishing T7 means converting that callout into a plain heading and flipping the CSV row to Complete, in the same change. I held off since you might want to review the findings prose first before we call it done.

### Claude

Sounds good — I'll leave the `task_callout("T7", ...)` and the CSV status untouched for now. Everything's committed on `validation-all-models` up through the findings draft, so it's ready whenever you want to review the prose and close it out. Let me know when you're ready to pick it back up, or if there's something else to work through in the meantime.

### Yai

I did some slight stylistic changes, but this is otherwise aligned with my understanding. In shorter words, both models are majority predictors and didn't learn anything specific to geographic markers. Is that correct?

### Claude

Close, with one sharpening worth making: it's not that the models specifically failed to learn *geography* — it's that they didn't learn enough discriminative signal from *any* predictor to override the majority-tier default in nearly every case. The study-level error pattern isn't evidence of a geographic blind spot; it's what you'd see from a near-constant predictor viewed through a lens (error rate by study) that happens to track each study's true tier mix. A model that always guesses the same class will look "right" wherever that guess is common and "wrong" wherever it isn't — regardless of what features it was given.

One more nuance against "didn't learn anything" read literally: the T5 coefficient audit earlier in the notebook found that predictors with a clear prior expectation (distance to PFAS sites, developed land use, urban burn area) mostly *did* point the expected direction in Model A's fitted coefficients. So there's real, directionally sensible signal in there — it's just too weak to ever flip a prediction away from the majority tier for all but one of the 46 held-out sites (Model B's single catch). "Learned weak signal that never won" is more accurate than "learned nothing."

So the corrected one-liner: **both models default almost entirely to the majority tier, and that failure is general (not geography-specific) — they picked up faint, plausible associations but never enough strength to act on them.**

### Yai

and that's the kind of insight that should belong in the next section?

### Claude

Yes, this belongs in T9, not T7 — and there's a sharper, more concrete version of it that T9 can make than what I put in the T7 cell.

**Why T9, not T7:** T7's job (per its own guiding questions) is to report the held-out scores and diagnose the error pattern — which the current cell does. T9's first guiding question is explicitly "how do the tuned models compare to the majority baseline" — that's the formal benchmarking comparison, and "both models are majority predictors" is exactly that comparison's headline answer. T7 diagnoses; T9 benchmarks against the plan's defined reference points and decides whether it moves the T10 recommendation.

**The sharper version, once you get there:** checkpoint_2.py already defines a `majority_baseline` dict (macro F1, `mcl_exceedance` recall/precision), but it's computed over the full 236-site `ss_scored_df`, not the specific 46-site held-out partition Model A/B were actually scored on. If T9 computes a majority baseline scoped to that exact held-out set instead, the comparison becomes almost embarrassing in the best way for a benchmarking narrative: **Model A's held-out macro F1 (0.2347) isn't just close to the majority baseline — it's numerically identical to it**, because Model A predicts the majority tier for all 46 sites, which is the literal definition of that baseline. Model B's 0.2825 is a marginal edge over that same number, from exactly one flipped prediction. That's a much stronger "lead with results" opener for T9 than a qualitative "both models default to majority" — it's "Model A is statistically indistinguishable from doing nothing; Model B barely clears that bar."

Want me to compute that held-out-scoped majority baseline now as groundwork for T9, or hold off until you're ready to start that section?

### Yai

let's hold that off for the next sections. For now, let's inject some of the contextual info we've gathered under the remaining callouts and guiding questions

### Claude

Good scoping — let's update the guiding questions in T8, T9, and T10's `task_callout()`s so the context we've built up isn't lost by the time someone picks those up. Let me pull the exact current text first.

### Claude

Now let's inject the T7 context into each. Starting with T8 — the "is this worth including" question should reflect that neither model even clears the bar yet:

### Claude

Now T9 — sharpening the majority-baseline question with the same-partition insight, and tying the sparsity question to T7's composition-not-geography finding:

### Claude

Now T10 — the "main limitation" framing currently presumes a deployment-ready pick, and the "biggest pitfall" question doesn't yet point at the generalization-gap finding:

### Claude

Let's validate.

### Claude

All clean. Let's run the full test suite before committing.

### Claude

All 38 pass. Let's commit.

### Claude

Committed. T8, T9, and T10's guiding questions now carry the T7 context forward — the same-partition majority baseline insight, the composition-vs-geography framing, and the CV-to-held-out generalization gap as a pitfall candidate — so whoever picks up those sections next isn't starting cold. All still validated clean (38/38 tests passing). T7 itself is still open pending your prose review, as decided earlier.

### Yai

let's close T7. Looks good to me now

### Claude

Now let's check for other "T7" references that should be cleaned up now that it's complete.

### Claude

Code comments referencing T5/T7/T9 (lines 330, 526) are dev-facing, not published prose — consistent with the scoping decision from the earlier cleanup pass, I'll leave those. Now let's update the CSV.

### Claude

Now let's validate everything end to end and run the full test suite before committing.

### Claude

That's the pattern — triple-quoted, dedented. Let me match it.

### Claude

All clean now. Let's run the full suite before committing.

### Claude

All 38 pass. Committing both files together.

### Claude

T7 is closed out — `task_callout()` stripped to a plain heading, CSV flipped to Complete, all validated (38/38 tests, clean lint/format/marimo check).

## Where things stand
T5, T6, and T7 are all Complete. T8 (scalability, optional), T9 (benchmarking), T10 (deployment narrative), and T11 (public repo) remain open, each now carrying forward context from T7's findings in their guiding questions — including the same-partition majority baseline lead and the generalization-gap pitfall candidate — so whenever you pick one up next, the framing's already there.

### Yai

Let's create a PR so that the team can review

### Claude

Authenticated, and `main` is the target. Let's push the branch and open the PR.

### Claude

Pushed. Now creating the PR.

### Claude

PR is up: **https://github.com/egsy-intell/team-project/pull/86**

Covers all 6 commits from this session — the T7 held-out evaluation and findings, the class-weight diagnostic consolidation, context carried into T8-T10, the heading-hierarchy fixes across checkpoint_2/3 and footer, and the matplotlib dependency fix. Test plan is filled in with what's already verified; team prose review is the one open checkbox.

### Yai

so now that we're done with T7. Is there anything else I could work on early tomorrow? We're aiming towards being done with the report on friday (a bit more than two days left), so I would like to start sooner rather than later

### Claude

Here's the state of play. You're actually eating into what was meant to be buffer time — the original plan (T12's own note) intended the writeup content wrapped by today (08-12) with 08-13 as slack before deck-building starts 08-14. T7 landing today puts tomorrow (Thu) as effectively your one full working day before Friday, so it's worth being deliberate about it.

## What's unblocked right now

**T9 — Model validation & benchmarking** (top priority). This is the one to open first thing tomorrow. It's fully unblocked now that T7's done, it's yours and Somyaranjan's, and its guiding questions are already loaded with the groundwork from today: the same-partition majority-baseline comparison (Model A's held-out macro F1 already matches it exactly), and the composition-vs-geography framing for the sparsity question. Most of the analytical thinking is done — this is largely translating what we already know into the benchmarking narrative, plus the McMahon comparison.

## One thing worth resolving before you start

**T4 — still Pending, and it's a little tangled.** It's supposed to be "the scoped change from T3," but T3's actual selected feedback item (site-sparsity quantification + lead-with-results) reads like it's already been folded into T9 and T10's guiding questions rather than being a separate standalone change — I don't see anywhere in the codebase that a real, computed site-sparsity-by-state table actually exists yet; the "~5 sites/state" figure in the prose right now looks like an illustrative placeholder, not something pulled from data. T4 also blocks T11 and T12 in the dependency graph, so it's worth 10 minutes tomorrow morning deciding: either (a) T4's real deliverable is computing that sparsity stat for real, as a small reusable piece T9 can cite, or (b) T4 is effectively subsumed by T9/T10 and should just be marked done. Either way, don't let it sit ambiguous while it's blocking two downstream tasks.

## Worth dropping

**T8 — scalability profiling.** It was optional from the start, and the guiding question we added to it already makes the case against running it: profiling throughput for a model that doesn't clear Step 3's floor yet is premature. I'd formally drop it rather than let it linger as an open item competing for time.

## Low-effort, batch whenever

**T11 — public repo check.** Quick sanity check (signed-out browser loads the repo, linked state matches the writeup), doesn't need dedicated focus — slot it in whenever, just before T12.

So: **T9 tomorrow morning**, decide T4's fate in the first 10 minutes, drop T8, and T11 whenever's convenient. Want me to start scaffolding T9 now so it's ready to go when you sit down tomorrow, or hold off until then?

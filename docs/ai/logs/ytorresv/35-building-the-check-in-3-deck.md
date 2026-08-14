# Building the Check-In #3 deck

**Branch:** `cp3-preso`  
**Session:** `10dc6b7b`  
**Span:** Aug 14, 00:10–01:06 EDT  
**Exchange:** 3 prompts, 15 responses

**Commits produced:**

- `bf6a31a` Add Check-In #3 (Final) presentation deck

[← back to the pairing-log timeline](https://egsy-intell.github.io/team-project/ai/ytorresv.html)

---

### Yai

based on @specs/checkpoint-3/GRAD 50400 - Project Checkpoint-3.pdf and @preso/checkpoint2_deck.md , let's generate the checkpoint3_deck.md. At a high-level, it should satisfy the spec and provide a continuation of the narrative, now that the project is done.

Additional context:
1. This will become a 15 minute preso. Make sure you validate scripts for that
2. Feel free to include illustration from the actual report. Pandoc should allow for that. Targets would be model comparison table, and held-out sample error rates.
3. Preso should focus on results, audience already saw the first half so we don't have to spend a lot of time in reintroducing the subject
4. Task delegation should be included, focus should be in step 5 tasks and role distribution
5. Use the purdue template to generate the final product
6. Language and narrative should be academical but friendly, it should reflect the overall narrative, and focus on findings. This is important since this was another feedback we got: "One recommendation is to simplify the final presentation by highlighting the most impactful results instead of covering every technical detail, as this will make it easier for a broader audience to follow." Find out a way to briefly mention that this is coming from peer feedback since this is part of the spec.
7. Make sure to include mentions of the peer feedback about site sparsity and regionality.
8. Ensure balanced talked time for all teammates: Me (Yai), Raj, Somya, and Emir. I can be the the icebreaker and wrap-up as before. The rest should mainly flow from roles.
9. Make sure that last remarks give thanks, in special to those that peer reviewed: Sky Alexander, Sereyroath So, Gavin Thompson, and Radman Zarbock. Their review was fair and thorough.

Also, please let me know if you have any questions along the way!

### Claude

I'll start by reading the checkpoint-3 spec and the current notebooks to pull in actual results.

*(API error: the connection dropped mid-response after the machine slept)*

### Yai

please resume

### Claude

It worked. Now let me pull the actual numbers from the executed notebook, then generate the two chart illustrations to embed in the deck, matching the actual report's plotting style. Let me pull a couple more specific figures (Model A/B's selected hyperparameters and top coefficients) to make the Model A/B slides concrete and accurate.

Now I have everything needed. Let me draft the deck, then validate timing and speaker balance before building the pptx.

First, let me fix the stray extra blank line, then rebalance speaking time (Raj is currently thin at 15.6%, Yai a bit heavy at 31.5%). Now expanding Raj's sections and trimming Yai's slightly to rebalance, then expanding Somya's divider transition and sparsity slide slightly.

Good balance now. Let me add a bit more substantive content — the deck is currently under-using the 15-minute slot; I'll flesh out a few results details to bring it closer to a natural 13–14 minute delivery.

Timing and balance both look solid now. Next, let's wire up the build script to support this new deck, then build it with the Purdue template.

Build succeeded. Let's verify the structure (slide count, layouts, notes, images) and confirm nothing regressed for the default checkpoint2 build. Default build path still works. Let's also verify the image slides render at a reasonable size and check the References table isn't cropped.

### Claude

Done. Here's what I built:

**`preso/checkpoint3_deck.md`** — 20 slides (title + 19 sections), continuing directly from `checkpoint2_deck.md`'s voice and structure. Highlights:

- **Peer feedback, explicitly named** (spec §1.3 requirement): a dedicated slide names all three items you listed — simplify/lead-with-results (which shapes the whole deck's leaner structure), site-sparsity quantification, and the regional-scope question — each pointing to where it's addressed later.
- **Real numbers only.** I actually executed `notebooks/checkpoint_3.py` (worked around a marimo nested-`embed()` limitation with `uv run --with nest_asyncio`) rather than trust stale exports, so every figure on the deck — CV scores, held-out recall/precision, the confusion-matrix breakdown, and the site-sparsity stats — is pulled live from the pipeline. One correction I caught this way: Model A actually predicted the majority tier for **all 46 of 46** held-out sites (not "44 of 46" as I first drafted).
- **Two illustrations from the actual report**, regenerated as PNGs with the notebook's own color/style conventions: the model-vs-threshold comparison chart and the held-out error-rate-by-study chart, both in `preso/assets/`.
- **Step 5 task delegation table** (T5/T6/T7/T9/T10/T11 → owners), per your ask to foreground role distribution.
- **Speaker balance**: Emir 26%, Somya 26%, Yai 25%, Raj 23% — Yai bookends only (icebreaker + wrap-up), the rest flows from each person's actual Step 5 task ownership.
- **Timing validated**: ~1,725 words ≈ 13.3 min at a conservative 130 wpm / 11.5 min at 150 wpm — under the 15-minute cap with real buffer.
- Closes by naming and thanking the four peer reviewers (Sky Alexander, Sereyroath So, Gavin Thompson, Radman Zarbock) for a fair, thorough review.

**Build tooling**: generalized `scripts/toolkit.py`'s `presentation` subcommand with a `--source` flag (previously hardcoded to `checkpoint2_deck.md`) plus two small bugfixes it surfaced (path resolution, pandoc image resource-path). Built the final product with the Purdue template:

```
uv run python scripts/toolkit.py presentation --source preso/checkpoint3_deck.md --template preso/purdue-reference.pptx
```

→ `preso/dist/checkpoint3_deck-purdue-reference.pptx` (20 slides verified: correct layouts, notes, image sizing, valid file). Existing test suite still passes. Also updated `README.md`'s presentation section.

One thing worth flagging: nothing's committed. Let me know if you'd like me to commit this, or if you want the team-branded `template.pptx` version built alongside the Purdue one for comparison (like you did at Check-In #2).

### Yai

let's commit the markdown files, and create a PR

### Claude

On branch `cp3-preso`, no upstream yet. Let me review the diffs, then stage and commit everything needed for the deck to actually build (markdown, chart assets, and the supporting toolkit/README changes).

All clean, all directly relevant to this deliverable. Staging and committing everything together, since the deck depends on the chart assets and the `--source` flag to actually build. Now let's push and open the PR.

That was already committed by Yai before this session — a footer/conclusion update. I'll include both commits in the PR since they're both ahead of `main` on this branch.

### Claude

PR created: **#92 — CP-3: Final presentation deck + conclusion update**

Pushed `cp3-preso` and opened the PR against `main`. It includes my commit (deck + assets + toolkit.py generalization) plus the `Write-up Wrap-up: Update conclusion` commit that was already on the branch. One item I left unchecked in the test plan: actually opening the built `.pptx` in PowerPoint/Keynote to eyeball it before recording — worth a quick look on your end since I can't render it visually from here.

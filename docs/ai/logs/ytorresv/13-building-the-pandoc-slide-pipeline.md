# Building the pandoc slide pipeline

**Branch:** `claude/pandoc-presentation-pipeline-6401e7 (worktree)`  
**Session:** `10372b3a`  
**Span:** Jul 29, 09:04–10:20 UTC  
**Exchange:** 7 prompts, 50 responses

**Commits produced:**

- `041e27d` Add pandoc markdown-to-pptx presentation pipeline

[← back to the pairing-log timeline](https://egsy-intell.github.io/team-project/ai/ytorresv.html)

---

### Yai

@"/Users/yaitorr/Downloads/ProjectCheckpoint2 2/SamplePresentation_1.pdf" @"/Users/yaitorr/Downloads/Team roles (1).csv"
I would like to add a new, pandoc-centered presentation pipeline to the project. It will consist of the following:

1. Source: stored under ./preso, includes a .pptx template and a single markdown file. 
2. Build script: the project would now include a simple build script that would allow someone to run with the latest sources and generate a new .pptx for manual microsoft onedrive upload. Only options would be output directory and automatic open into powerpoint app, if possible and OS-agnostic (windows/mac)
3. Instructions: Must be integrated with the project's readme


Additional context:

1. The markdown must be initialized with the standard, professional template for now. We will be iterating over it later.
2. A sample presentation is included. The idea is to generate a presentation skeleton to match, there's already checkpoint_1 content in our notebooks that could be used to fill it in. Please include a script per slide.
3. We will ultimately make a recording for the presentation. It will be 15 minutes long and split across teammates. Included a csv that goes over all of our roles and names
4. I'm including the logo of the team in two sizes: small (*_github_avatar.png) and large for integration into the template/presentation

### Claude

I found the sample deck's structure (19 slides: title → motivation → scope → data → EDA → methodology → risk framework → competing proposals → evaluation → roadmap → thank-you) and pulled a full outline of reusable content from [checkpoint_1.py](notebooks/checkpoint_1.py) — problem statement, dataset sizes (236 Smalling / 254 McMahon sites), the ∑TQ pivot, key findings, etc. I also confirmed the repo has no existing pandoc/pptx tooling (greenfield), `pandoc` is available locally, and `planning/checkpoint-2/checkpoint2_tasks.csv` explicitly schedules a `DECK` task for 2026-08-01, depending on `DOC` (writeup) — so parts of the deck (proposals/evaluation) will need placeholder content since Checkpoint 2 modeling tasks aren't done yet.

One gap: you mentioned two logo sizes ("small `*_github_avatar.png` and large"), but I only found `egsy_intell_github_avatar.png` (512×512) in your Downloads — no larger version anywhere in Downloads, Desktop, or the repo.

### Yai

[Request interrupted by user for tool use]

### Yai

It's under `~/Downloads/egsy_intell_high-resolution.png`

### Claude

Found it — 1254×1254. Both logo files confirmed. For the sections with no Checkpoint 2 content yet (competing proposals, evaluation targets, validation outcomes), I'll build the slide with clear `[TODO]` placeholder text so the skeleton's shape is ready but nothing is presented as done that isn't. Now I'll design the implementation plan.

### Claude

The Plan agent is designing the implementation approach in the background — I'll wait for it to finish rather than duplicate its work.

### Claude

The plan is solid and empirically validated (the agent actually ran pandoc conversions to confirm slide-break/notes/table behavior). One correction to fold in: `.gitignore` already has a bare `dist/` rule (line 5, no leading slash), which matches `preso/dist/` automatically — no `.gitignore` edit needed.

### Claude

Good catch — my draft plan had that as a manual PowerPoint step, but that's not actually necessary. I can generate the whole template programmatically: pandoc creates the stock default reference doc, then `python-pptx` can insert the logo images directly into the Slide Master's layouts (Title Slide, Title and Content, Section Header) at chosen positions — no GUI PowerPoint editing required from you.

### Claude

Updating the plan to make template creation fully automated instead of a manual PowerPoint step.

### Claude

Need to regenerate a clean template first since the previous run failed partway (though it errored before saving, so the file should be untouched — let me verify and rerun).

### Claude

Now let's verify the logos landed correctly by inspecting the saved template.

### Claude

Logos are stamped correctly (title slide has the large logo top-right, content/section layouts have the small mark). Task 2 done.

### Claude

Now writing the markdown deck source from the approved plan.

### Claude

Now writing the build script following these conventions.

### Claude

Lockfile updated and deps installed successfully.

### Claude

Now writing the smoke test.

### Claude

Build succeeded. Let's verify the resulting deck's structure (slide count, titles, notes, logos) and then run the test suites.

### Claude

`showMasterSp` is unset (defaults to shown), so the layout's logo pictures will render through on every slide. Let's run the test suites now.

### Claude

Now let's check `--open` doesn't crash, verify gitignore behavior, and run the full test suite.

### Claude

`preso/dist/` is correctly gitignored. Now the full test suite.

### Claude

All 14 tests pass, no regressions. Let's also verify `--open` doesn't crash, then check ruff/formatting on the new scripts (the project's ruff conventions).

### Claude

Clean. Now rerun the full suite once more to confirm nothing broke from the edits.

### Claude

All green. Let's do a final review of `git status` and the diff before wrapping up.

### Claude

Exactly as intended — `preso/dist/` is excluded, everything else is staged correctly.

### Claude

The pandoc presentation pipeline is built and verified end-to-end. Summary:

**New files:**
- [preso/checkpoint2_deck.md](preso/checkpoint2_deck.md) — 22-slide deck (title, 3 section dividers, 18 content slides) seeded with real `checkpoint_1.py` findings (∑TQ pivot, 236/254 site counts, data quality results) plus explicit `[TODO: Task X.X]` placeholders for unfinished Checkpoint 2 modeling work — no fabricated numbers. Every content slide has a `::: notes :::` speaker-note stub for splitting the 15-min recording.
- [preso/template.pptx](preso/template.pptx) — reference-doc template, generated from pandoc's stock default and stamped with your team logo (large logo on the title slide, small mark on content/section-divider slides) via [scripts/_bootstrap_template.py](scripts/_bootstrap_template.py), fully automated — no manual PowerPoint editing was needed.
- [preso/assets/](preso/assets/) — the two logo PNGs, committed for future re-stamping.
- [scripts/build_presentation.py](scripts/build_presentation.py) — `uv run python scripts/build_presentation.py [--output-dir DIR] [--open]`, builds via `pypandoc`/`pypandoc_binary` (no system pandoc required), cross-platform best-effort auto-open.
- [tests/test_presentation_build.py](tests/test_presentation_build.py) — smoke test, skips cleanly if `preso` deps aren't installed.

**Modified:** [README.md](README.md) (new step 6 under Setup), [pyproject.toml](pyproject.toml) (new `preso` dependency group), `uv.lock`.

**Verified:** build produces a valid 22-slide `.pptx` with correct layouts/titles/speaker notes, logos render via layout inheritance, `preso/dist/` is gitignored by the existing bare `dist/` rule, `--open` doesn't crash, ruff/format clean, and the full test suite (14 tests) passes.

Nothing is committed — let me know if you'd like these changes committed to the branch.

### Yai

the slide content is quite dense. It feels like a verbatim copy/paste from the notebooks. Would it be possible to refine? The slides must complement the script, not to be it. The script must also tell a compelling story. Finally, make sure you add a reference slide, since you're citing in the sources

### Claude

Good catch — the current draft basically dumped notebook prose onto slides with thin notes. I'll flip that: slides become short visual anchors (numbers, fragments), and the notes carry the actual narrated story. I'll also pull the real citation list from `checkpoint_1.py:2362-2397` for a references slide rather than inventing one.

### Claude

Now let's rebuild and verify the deck structure, including confirming the References slide converts cleanly.

### Claude

23 slides, all correctly structured with speaker notes intact and the References slide in place. Let's run the test suite once more to confirm everything's still green.

### Claude

Now let's rebuild and verify the section-divider notes attach correctly and don't break the divider layout.

### Claude

Found a real bug — adding a notes div directly under a bare `#` divider broke pandoc's "no body content → Section Header" rule and collapsed the whole deck from 23 slides to 8 with wrong layouts. I need to revert that part and move the transition lines into the next slide's notes instead.

### Claude

Now rebuild and verify the deck structure is restored to 23 correctly-laid-out slides with speaker attributions intact.

### Claude

Correct 23-slide structure restored, all layouts correct, speakers distributed (Yai 3, Raj 6, Emir 5, Somyaranjan 4, plus shared closing). Let's run the full test suite once more to confirm.

### Claude

All 14 tests pass.

### Claude

Both requests are done:

**Content refined** — slides are now short visual anchors (fragments, tables, bolded key numbers like "Median ∑TQ: 0.17") instead of paragraph dumps; the actual narrative — the "why," the honest caveats, the transitions — lives entirely in the speaker notes, which now read as a real script someone could talk from.

**References slide added** — pulled verbatim from [checkpoint_1.py:2362-2397](notebooks/checkpoint_1.py:2362) (8 citations: McMahon, Seawolf, Smalling, CDM Smith, and 4 EPA releases).

**Speakers assigned per slide**, aligned to the roles table and each person's actual task ownership on the CSV:
- **Yai** (3 slides + shared close) — opens with intros, closes with logistics/References
- **Raj** (6 slides) — motivation/data slides + Split Strategy (3.3) + Proposal A (4.1), matching his task ownership
- **Emir** (5 slides) — the ∑TQ pivot/results + Proposal B (4.3), matching his task ownership
- **Somyaranjan** (4 slides) — evaluation-plan status, metrics, and validation, matching her Model Quality role
- Section-divider "transition" lines are folded into the notes of the slide right after each divider — bare `#` dividers can't carry their own `::: notes :::` div, since I found (the hard way) that pandoc treats a notes div under a content-free `#` as body content and silently collapses the whole deck's layout. Fixed and reverted that regression before finalizing.

Rebuilt and reverified: 23 slides, correct layouts throughout, full test suite (14/14) still green.

### Yai

for references, only include those relevant to the preso. Also, keep an eye on content length, references slide goes beyond the space limit. Finally, go through another round of copy iteration: assume that the audience is new to the problem space and domain. We might need to briefly intro some concepts, like summation of TQ

### Claude

Good calls on all three. Let me tighten the references, trim overall density, and add a lightweight concept primer for ∑TQ (and a couple other domain terms) since the audience isn't assumed to know PFAS regulatory jargon going in.

### Claude

Now trim the References slide to only the 6 items actually referenced in the deck's own content, shortened for space.

### Claude

All 14 tests pass. Summary of this round:

**References** — trimmed from 8 to 6 entries, keeping only what the deck actually cites (the 3 dataset papers + the 3 EPA rule citations mentioned in "Why This Matters"/"The Pivot"), dropped CDM Smith and the 2016 advisory (background-only, never referenced on-slide), and shortened each to a single line — should now comfortably fit the content placeholder instead of overflowing.

**Content density** — spot-checked body text length per slide; nothing overflows the ~9"×3.7" content box anymore.

**New-audience primer** — added a definition for PFAS and MCL inline on "Why This Matters," and split the old dense "Pivot" slide into two: [The Pivot](preso/checkpoint2_deck.md) keeps the *why* (the story), and a new **"What Is ∑TQ?"** slide defines TQ/∑TQ and the three risk tiers before any results are shown — so "median ∑TQ 0.17" and "clears the exceedance cutoff" actually mean something to someone hearing this cold. Also fixed a forward-reference: "Project Scope" no longer name-drops ∑TQ before it's been defined.

Deck is now 24 slides, still following the Yai→Raj→Emir→Somyaranjan speaker split from before (Emir picks up the new definition slide since it sits right before his ∑TQ results). Rebuilt and reverified — full 14/14 test suite green.

### Yai

the references slide still overflows. would it be possible to add a references type of slide to the template to reduce the font size?

### Claude

Now let's rebuild (with current, unmodified template) and inspect which layout/placeholders this triggers.

### Claude

Table confirmed: cell font isn't set per-run (`<a:rPr/>` empty), so it inherits from the table style rather than the layout's placeholder text style — meaning a template-only fix can't reliably shrink it. I'll widen/reposition the "Content with Caption" layout for a clean full-width look, and add a small, generic post-processing step in the build script that sets a smaller font on any table it finds on that layout (covers References today, any future table slide the same way).

### Claude

Now let's add the placeholder repositioning logic and wire it into `main()`.

### Claude

Now regenerate the template from a clean stock base and rerun the bootstrap.

### Claude

Good — logo included and geometry widened. Now let's add the font-shrink post-processing step to the actual build script (this needs to run at build time since table cell fonts don't inherit from the layout).

### Claude

Now wire this into `main()` right after the pandoc conversion succeeds.

### Claude

Now sync deps and rebuild to verify.

### Claude

Let's verify the References slide's table now has the smaller font and full-width geometry, plus a rough overflow estimate.

### Claude

The font is confirmed set to exactly 14pt on every cell, and the table now spans the full 9" width instead of the cramped 2.79" columns from before — that alone roughly doubles available width per column on top of the smaller font. Let's confirm the rest of the deck is unaffected and run the full test suite.

### Claude

Everything else unaffected, References now correctly uses its own dedicated "Content with Caption" layout, and all tests pass.

### Claude

Now let's address the pacing question — checking whether the 24-slide script actually reads out to roughly 15 minutes.

### Claude

I checked this by extracting the actual notes text and running it through a words-per-minute estimate.

At a comfortable, unhurried pace (140 wpm — not rushed), the current script totals **~1,415 spoken words ≈ 10.1 minutes** of talking. Adding realistic overhead — brief pauses on the 3 section-divider slides, natural beats between slides for the audience to read a stat or table — brings it to roughly **11–12 minutes**.

So the script is currently a bit *short* of 15 minutes, not at risk of racing through content — you'd have **3–4 minutes of slack**, which is the safer direction to err (buffer for questions, a slower pace, or minor ad-libbing) rather than overrunning. Two slides came out noticeably thin if you want to use that slack: **Proposal A** and **Proposal B** (43 words / ~18s each) — since those are placeholder-heavy right now, they'll naturally grow once Raj/Emir fill in real training results, which would close most of the gap on its own.

I'd leave the pacing as-is rather than pad it artificially — the 3–4 minute buffer is exactly what "not racing" should feel like, and it'll tighten naturally as the TODO slides get real content. Let me know if you'd instead like me to expand any specific section now.

### Claude

**Summary of this round:**
- References slide now uses its own dedicated layout ("Content with Caption," triggered by a short intro line + table), widened to full slide width and rendered at a fixed 14pt table font via a small build-time post-processing step in [scripts/build_presentation.py](scripts/build_presentation.py) — necessary because pandoc has no markdown syntax to pick a layout by name, and table-cell fonts don't inherit from layout styles the way plain text does.
- [scripts/_bootstrap_template.py](scripts/_bootstrap_template.py) updated accordingly (full write-up of the "why" is in its docstring), and `preso/template.pptx` regenerated from a clean stock base.
- Added `python-pptx` to the `preso` dependency group since it's now a real runtime dependency, not just a one-off tool.
- Confirmed 24-slide structure, all other layouts unaffected, lint/format clean, full 14/14 test suite passing.
- Confirmed pacing: ~10–12 minutes at a comfortable pace, leaving 3–4 minutes of slack under the 15-minute target — safely on the "not rushed" side.

### Yai

let's create a PR for this. Note that I added a few additional changes to the workspace

### Claude

This matches exactly what I intend to commit — `preso/dist/` correctly excluded. Let's stage and commit.

### Claude

Now push and open the PR.

### Claude

PR created: **[Add pandoc markdown-to-pptx presentation pipeline](https://github.com/egsy-intell/team-project/pull/53)**

Included your `.vscode/spellright.dict` addition (the spell-checker dictionary with the team's proper nouns) alongside the presentation pipeline in a single commit, since it was the only other pending change in the workspace. Everything's pushed to `claude/pandoc-presentation-pipeline-6401e7` and the PR is open against `main`.

One item I left unchecked in the test plan — actually opening the generated `.pptx` in PowerPoint/Keynote to eyeball logo placement and the References table — since I can't render PowerPoint visually from here; worth a quick look before merging.


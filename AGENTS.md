# Agent guide for this repo

This is a marimo-notebook data science project (PFAS occurrence risk
modeling). Notebooks under `notebooks/` are published as **HTML** to
GitHub Pages via `scripts/export_notebooks.py` and
`.github/workflows/publish.yml`. HTML is the source of truth for this
project's published output — there is no PDF export step. This file
documents non-obvious constraints and quirks discovered while building
that pipeline — read it before editing anything under `notebooks/` or
the export scripts, especially before adding new tables or plots.

## Agent role

This is a 4-person team project, so consistency across contributors'
sessions matters more than usual — treat yourself as the thing keeping
the codebase and writeup aligned across everyone's work, not just the
person currently prompting you.

- Act as a pair-programming partner and copy-editor by default: flag
  unclear writing, inconsistent terminology, and structural issues in
  notebook prose/markdown, not just code correctness. Only drop this
  posture if the user explicitly says to.
- Prefer idiomatic Python (comprehensions, `pathlib`, vectorized
  pandas/numpy operations, etc.) over imperative loops when both are
  equally clear.
- Keep the codebase DRY across the whole team's contributions: when
  editing, actively look for duplicated logic or prose across notebooks
  (repeated cleaning steps, copy-pasted section intros, restated task
  descriptions) and propose consolidating it into a shared helper or a
  single source of truth — the same way `print_sections()` and
  `make_plot_grid()` already got consolidated (see below).

## Editorial conventions for the published report

These apply whenever you touch reader-facing prose or numeric output in
`notebooks/` — not just when a task explicitly asks for an editorial
pass. Check for them as part of any edit, the same way you'd run ruff.

**`index.py` must always read as a single flowing document, not
concatenated notebooks.** `checkpoint_1.py`'s and `checkpoint_2.py`'s
own body content starts directly at their first `## Step N` heading —
`index.py` owns the report-level metadata (title, team roster, roles
table) so there's no duplicate title/header when the checkpoints are
embedded and stacked. When adding a new checkpoint (see "Multi-notebook
checkpoint workflow" below) or editing `index.py`'s embed/vstack cells,
check that: there's exactly one H1 for the whole report (in `index.py`,
not repeated per checkpoint), each embedded section flows into the next
without an abrupt jump, and no checkpoint re-introduces its own
title/team block. This is a standing requirement, not a one-time fix —
re-verify it any time `index.py` or a checkpoint's opening cells change.

**No "checkpoint" in reader-facing prose.** Per the course spec (`GRAD
50400 - Project Checkpoint-1.pdf`), the document's own vocabulary is
"Step 1" ... "Step 5" for sections and "Check-In #1/#2" for the graded
milestones — "checkpoint" is only the internal course-milestone label
used in casual conversation and in this repo's own filenames/module
names. Use, depending on context: **"Step N"** for a section or
deliverable slice, **"report"** for the whole combined document, or
**"writeup"** when referring to the submission artifact itself (the
spec's own term). This rule is about prose only — module filenames
(`checkpoint_1.py`, `checkpoint_2.py`), their imports/variable names,
and internal repo paths (e.g. `planning/checkpoint-2/...`) are unaffected
and stay as-is.

**Numeric display: round to 4 decimal places, for raw computed
statistics only.** Medians, means, skewness, TQ scores, thresholds
derived from data, and similar computed floats should be rounded to 4
decimal places at the point they're displayed (`.round(4)` on a
DataFrame column being ` mo.ui.table()`'d, or `:.4f` in an f-string) —
not left unrounded (Python float repr can produce noise like
`0.17099999999999999`) and not rounded to some other inconsistent
precision. This does **not** apply to percentages (`:.1%`-style
displays, "Missing (%)" columns) or hand-picked policy thresholds
(`RECALL_FLOOR = 0.70` and similar, shown as `≥ 0.70 (70%)`) — those
keep their existing, deliberately coarser format since they're a
different kind of value than a computed statistic. See
`_make_numeric_summary_table()` and the skew/IQR `Outlier fence` column
in `checkpoint_1.py`, and `groundwater_comparison_df`'s `sum_tq_epa
median` in `checkpoint_2.py`, for the pattern.

**First person ("we"/"our"), not third-person passive, is the
report's voice.** `checkpoint_1.py` is written throughout in first
person (e.g. "We will also attempt...", "Our original provisional
classification..."). `checkpoint_2.py` had drifted into third-person
passive constructions ("will be used", "is appropriate", "will
remain") almost everywhere, with only a couple of first-person
slips. Since `index.py` stacks every checkpoint into one flowing
document, a voice mismatch at the checkpoint boundary reads as
jarring even when nothing else about the prose is wrong. When adding
or editing reader-facing prose, write "we"/"our" rather than passive
constructions like "will be used" or "is proposed" — check for this
the same way you'd check for the other conventions here.

## Printing / PDF output

We do not generate PDFs from this repo. An earlier version of this
pipeline used marimo's native `export pdf` (nbconvert's WebPDF exporter
via Playwright/Chromium) to publish a PDF alongside the HTML, but that
path hit several real, unfixable-from-our-side bugs in marimo
0.23.14/0.23.15's PDF rasterization (wide tables silently cropped
instead of scaled, a "not connected to a kernel" toast bleeding into
table/figure screenshots, and blank pages from a screenshot-stitching
bug) — see git history around the removal of `_check_table_widths()`,
`_drop_blank_pages()`, and the `marimo export pdf` step in
`scripts/export_notebooks.py` if you want the full investigation.
**Don't re-add a PDF export step to this repo without checking whether
those upstream bugs are fixed first.**

For print-quality output, the team currently uploads the notebook to
[molab](https://molab.marimo.io/) instead, which the team found prints
notably better. Point people there until a better in-repo alternative
is found.

## Repo layout

- `notebooks/*.py` — marimo notebooks (plain Python, PEP 723 inline
  script headers for standalone `uvx` execution). Each project checkpoint
  is its own independent notebook (`checkpoint_1.py`, `checkpoint_2.py`,
  ...); `notebooks/index.py` composes all of them into one combined
  artifact (see "Multi-notebook checkpoint workflow" below).
  `data_dictionary.py` documents predictors/compounds and is embedded
  into `checkpoint_1.py` via `data_dictionary_app.embed()`.
- `notebooks/ruff.toml` — lint config scoped to `notebooks/` only (ruff
  resolves the nearest config per directory, so this doesn't affect
  `scripts/`/`tests/`).
- `scripts/export_notebooks.py` — exports every notebook to
  `docs/notebooks/{stem}.{html,py}`, injects a banner into the HTML
  with a link to run the notebook via `uvx`.
- `tests/test_notebooks.py` — `marimo check`, `ruff check`, `marimo
  export html` (execution smoke test), and `codespell`, all parametrized
  over every notebook.
- `.github/workflows/publish.yml` — runs on push to `main`: tests, then
  `scripts/export_notebooks.py`, then publishes `docs/notebooks/` to
  `gh-pages`.
- `.github/workflows/autofix-lint.yml` — on PRs, runs `ruff check --fix`
  and `marimo check --fix` and auto-commits. **This can re-add code that
  a previous commit intentionally removed** — see the ruff/marimo
  conflict below.

## Notebook authoring constraints

**79-column line length, enforced by ruff.** `notebooks/ruff.toml` sets
`line-length = 79`. Run `uv run ruff format notebooks/` and `uv run
ruff check --fix notebooks/` after editing, then manually wrap anything
left over (long markdown paragraphs wrap safely at word boundaries —
markdown collapses single newlines within a paragraph — but ATX headers
like `#### Some Long Title` can't be split onto two lines; if a heading
is too long, either shorten it or use an inline `<h4>...</h4>` HTML
block spanning two physical lines instead, which CommonMark renders
identically).

**`PLR1711` is ignored, on purpose.** marimo's own formatter (`marimo
check --fix`, run by the autofix-lint workflow) enforces a trailing bare
`return` at the end of every cell function, even when it defines
nothing — that's how marimo marks a cell's outputs as complete. Ruff's
default rule set flags that same statement as "useless" (`PLR1711`).
These two tools fought over it (autofix workflow kept re-adding what
ruff had just removed) until we added `PLR1711` to `notebooks/ruff.toml`'s
`ignore` list. Don't remove that ignore or "clean up" a bare `return` at
the end of a cell — leave it as marimo's own convention.

**Tabs/accordions (`mo.ui.tabs`, `mo.accordion`) are fine to use now.**
They used to be banned in favor of the `print_sections(items: dict)`
helper because tabbed content was simply invisible in the old PDF
export (no JS at all in a rendered PDF). Now that HTML is the only
published output, tabs work fine (the published HTML is static —
no live kernel — but tab switching is a pure client-side JS
interaction, so it works without one). `print_sections` is still
available near the top of each notebook if you specifically want a
grouped/comparison view where every item stays visible at once without
requiring a click.

**Keep shared plotting/table-building helpers in one cell, referenced
by others — don't duplicate them per section.** marimo forbids two
cells from defining the same global name (including `import ... as x`
and function defs), which previously led to copy-pasted plotting code
with artificially different names per section (e.g. `plt` vs
`plt_mac`, `make_boxplot` vs `make_boxplot_mac`) just to dodge that
restriction. The correct pattern is to define the import/helper once in
its own cell and have downstream cells take it as a parameter (marimo
wires this up automatically from the function signature, e.g. `def
_(make_plot_grid, mo, ss_clean_df):`). See `make_plot_grid()` in
`checkpoint_1.py`, shared by both the Smalling+Seawolf and McMahon
exploratory-plot sections.

**Prefix cell-local variables with `_`; module-level constants are
`UPPER_SNAKE_CASE`.** marimo requires every non-underscore-prefixed name
to be globally unique across the notebook and makes it a `return`able,
cross-cell value — so a bare name reads as "this crosses cell
boundaries," while `_`-prefixed reads as "this cell's own scratch
work," even for names never at risk of colliding today. Prefix a
variable the moment it won't be in that cell's `return` tuple,
including loop variables and DataFrame intermediates in a
single-purpose cell (e.g. `_tapwater_split_df`, `_held_out_studies` in
the split-strategy section of `checkpoint_2.py`). A name a cell does
return — and that other cells take as a function parameter — stays
unprefixed, and if it's a fixed lookup table or label set rather than
computed data, name it `UPPER_SNAKE_CASE` in its own cell (e.g.
`RISK_LABELS` in `checkpoint_2.py`) instead of `lower_snake_case`, so
it reads as a constant at every call site that takes it as a
parameter.

**Small-multiple plots (one subplot per variable) should use a compact
grid, not one plot per row.** `make_plot_grid()` in `checkpoint_1.py`
lays out up to 3 columns (`grid_cols = min(3, n_vars)`) and wraps into
additional rows as needed, for both box plots and histograms. Follow
this pattern for any new multi-variable plot instead of stacking one
subplot per row.

**One cell per data pipeline unit, not one cell per pandas call.** A
step like "reshape wide to long," "join reference/benchmark data," or
"score and aggregate a target" is one cell, even if it takes several
statements/intermediate variables to get there — don't split each
`.assign()`/`.groupby()`/`.merge()` into its own cell. Reserve cell
boundaries for a change in what's being described (matches the
markdown-then-code pairing already used throughout `checkpoint_1.py`,
e.g. reshape / join benchmarks / compute ∑TQ in the ∑TQ construction
section). Splitting finer than that mainly pays off transiently while
debugging (isolating exactly which line in a chain broke); once a
pipeline is working, collapse it back to one cell per unit.

## Multi-notebook checkpoint workflow

Each project checkpoint gets its own notebook rather than one
ever-growing file. The pattern, established by `data_dictionary.py` and
followed by `checkpoint_2.py`:

- A later checkpoint embeds an earlier one to reuse its cleaned
  dataframes: `from checkpoint_1 import app as checkpoint_1_app`, then
  `await checkpoint_1_app.embed()` in an `async` cell, pulling needed
  names off `.defs["name"]` (e.g. `mc_clean_df`, `ss_clean_df`,
  `task_callout`). Anything a cell in `checkpoint_1.py` `return`s is
  reachable this way, including plain helper functions, not just
  dataframes.
- Copy the local-checkout-vs-standalone-URL `try/except
  ModuleNotFoundError` import fallback verbatim into the new notebook's
  first cell (see any existing notebook's first cell) — it lets `uvx
  marimo edit --sandbox <gh-pages-url>` download the sibling notebook
  from the same repo location when there's no local checkout to import
  from.
- `notebooks/index.py` embeds every checkpoint notebook's `app` and
  stacks their rendered output with `mo.vstack`, so the full project
  reads as one document. It's exported like any other notebook to
  `docs/notebooks/index.html`, which is what's served as the directory
  index at the gh-pages `/notebooks/` path — the one URL that shows the
  whole project.
- When adding checkpoint 3+: create `checkpoint_3.py` following the
  embed pattern above, then add its embed-and-stack cells to
  `notebooks/index.py`, positioned after checkpoint 2's pair and before
  `footer`'s (see "Trailing content lives in `footer.py`, not in the
  checkpoint notebooks" below for what to do with any Conclusion/
  References/AI-usage content the new checkpoint itself ends with).
  Nothing in `scripts/export_notebooks.py` or `tests/test_notebooks.py`
  needs to change — both glob `notebooks/*.py` and pick up new notebooks
  automatically.

## Trailing content lives in `footer.py`, not in the checkpoint notebooks

`App.embed()` returns one monolithic `Html` blob per notebook (see
`AppEmbedResult.output` in marimo's `_ast/app.py`) — there's no way for
`index.py` to pull out or reorder individual cells from an embedded
checkpoint's output. That's a problem for content that's logically
project-wide rather than specific to one checkpoint: a Conclusion,
References, and an AI usage appendix need to render *last*, after every
checkpoint's body, but if each `checkpoint_N.py` ended with its own copy
of that content, embedding it wholesale would place it wherever that
checkpoint falls in the stack — not necessarily last.

The fix is structural, not a change to `index.py` alone:
`notebooks/footer.py` is a small notebook (no sibling-notebook import
fallback needed — it's pure `mo.md()` prose with no data dependency,
just `import marimo as mo`) that holds all of this trailing content, and
`index.py` embeds it last, after every checkpoint. Checkpoint notebooks
themselves should contain only their own body content once integrated —
no trailing Conclusion/References/AI-usage cell of their own.

`footer.py` has two kinds of content that get updated differently as
checkpoints are added:

- **Conclusion**: replaced, not appended to. It's a single running
  narrative reflecting the project's current state, not a per-checkpoint
  log. When integrating a newly-finished `checkpoint_N.py` that ends
  with its own Conclusion cell, fold that content into `footer.py`'s
  existing Conclusion — merge the new substance into one coherent
  section (this is the one step in the recipe that isn't pure
  copy-paste; some light editorial rewriting to keep it coherent as a
  single narrative is expected) — then delete the cell from
  `checkpoint_N.py`.
- **References / AI usage appendix**: appended to, not replaced, as new
  sources or AI threads are used. Move new entries verbatim from
  `checkpoint_N.py` into `footer.py`'s existing lists, then delete them
  from `checkpoint_N.py`.

In both cases, also add `checkpoint_N.py` to the sibling-fetch fallback
list in `index.py`'s first cell (and in any later checkpoint that embeds
it for data, the same way `checkpoint_2.py` currently embeds
`checkpoint_1.py`).

## Task-tracking prose is scaffolding, not published content

`task_callout()` (see above) and inline "Task PW"/"Task 3.2"-style IDs in
markdown cells exist so the team can track ownership and dependencies
against `planning/checkpoint-2/checkpoint2_tasks.csv` while a task is
still open — they're a coordination aid for us, not something a reader of
the published notebook needs. **When a task is completed, strip its
`task_callout()` and any "Task <ID>" prose references from the notebook**
(the CSV row is the durable record of who did what and when; it doesn't
need to be duplicated in the published writeup). Replace a task's
`task_callout()` header with a plain section heading, and reword prose
that named the task ID into normal descriptive language. See the removal
of Task PW's callout/ID references from `checkpoint_1.py`'s ∑TQ
construction section for the pattern. Leave `task_callout()` calls for
still-open tasks (and their `depends_on=` links) alone until those tasks
are done too.

**Completing a task means updating both the notebook and the CSV in the
same change** — the two are meant to move together, not drift.
Alongside stripping the `task_callout()`/ID prose above, set that task's
`Status` to `Complete` in
`planning/checkpoint-2/checkpoint2_tasks.csv`. Prose elsewhere in the
notebook that references the completed task only as a *dependency* (a
still-open task's `depends_on=`, or text like "once Task PW's ... is
available") isn't part of this cleanup — it stays until that other task
is also done. But prose describing what the completed task itself
produced (e.g. a conclusion cell saying its output is still pending)
should be corrected to reflect that it's done, since a stale "not yet
implemented" claim is misleading even without a literal task ID
attached.

## Commands

```bash
uv run pytest tests/ -v                        # marimo check, ruff, execution, spelling
uv run ruff check notebooks/                   # lint only
uv run ruff format notebooks/                  # format only
uv run python -m marimo check --fix notebooks/<nb>.py
uv run python scripts/export_notebooks.py      # full HTML export to docs/notebooks/
```

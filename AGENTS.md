# Agent guide for this repo

This is a marimo-notebook data science project (PFAS occurrence risk
modeling). Notebooks under `notebooks/` are published as **HTML** to
GitHub Pages via `scripts/export_notebooks.py` and
`.github/workflows/publish.yml`. HTML is the source of truth for this
project's published output — there is no PDF export step. This file
documents non-obvious constraints and quirks discovered while building
that pipeline — read it before editing anything under `notebooks/` or
the export scripts, especially before adding new tables or plots.

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
  script headers for standalone `uvx` execution). `checkpoint_1.py` is
  the main analysis; `data_dictionary.py` documents predictors/compounds
  and is embedded into `checkpoint_1.py` via `data_dictionary_app.embed()`.
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

**Small-multiple plots (one subplot per variable) should use a compact
grid, not one plot per row.** `make_plot_grid()` in `checkpoint_1.py`
lays out up to 3 columns (`grid_cols = min(3, n_vars)`) and wraps into
additional rows as needed, for both box plots and histograms. Follow
this pattern for any new multi-variable plot instead of stacking one
subplot per row.

## Commands

```bash
uv run pytest tests/ -v                        # marimo check, ruff, execution, spelling
uv run ruff check notebooks/                   # lint only
uv run ruff format notebooks/                  # format only
uv run python -m marimo check --fix notebooks/<nb>.py
uv run python scripts/export_notebooks.py      # full HTML export to docs/notebooks/
```

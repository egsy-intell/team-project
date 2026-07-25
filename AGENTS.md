# Agent guide for this repo

This is a marimo-notebook data science project (PFAS occurrence risk
modeling). Notebooks under `notebooks/` are published as HTML + PDF to
GitHub Pages via `scripts/export_notebooks.py` and `.github/workflows/publish.yml`.
This file documents non-obvious constraints and quirks discovered while
building that pipeline — read it before editing anything under
`notebooks/` or the export scripts, especially before adding new tables
or plots.

## Repo layout

- `notebooks/*.py` — marimo notebooks (plain Python, PEP 723 inline
  script headers for standalone `uvx` execution). `checkpoint_1.py` is
  the main analysis; `data_dictionary.py` documents predictors/compounds
  and is embedded into `checkpoint_1.py` via `data_dictionary_app.embed()`.
- `notebooks/ruff.toml` — lint config scoped to `notebooks/` only (ruff
  resolves the nearest config per directory, so this doesn't affect
  `scripts/`/`tests/`).
- `scripts/export_notebooks.py` — exports every notebook to
  `docs/notebooks/{stem}.{html,pdf,py}`, injects a banner into the HTML
  with links to run the notebook via `uvx` or download the PDF.
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

**No tabs or accordions.** `mo.ui.tabs`/`mo.accordion` hide inactive
panes via JS, so their content is simply invisible in the PDF (and in
any browser print-to-PDF of the HTML). Use the `print_sections(items:
dict)` helper defined near the top of each notebook instead — it renders
every `{label: content}` item as an always-visible labeled section. If
you're adding a new grouped/comparison view, reuse this helper rather
than reaching for tabs.

**79-column line length, enforced by ruff.** `notebooks/ruff.toml` sets
`line-length = 79` — code wider than that gets clipped in the PDF. Run
`uv run ruff format notebooks/` and `uv run ruff check --fix
notebooks/` after editing, then manually wrap anything left over
(long markdown paragraphs wrap safely at word boundaries — markdown
collapses single newlines within a paragraph — but ATX headers like
`#### Some Long Title` can't be split onto two lines; if a heading is too
long, either shorten it or use an inline `<h4>...</h4>` HTML block
spanning two physical lines instead, which CommonMark renders identically).

**`PLR1711` is ignored, on purpose.** marimo's own formatter (`marimo
check --fix`, run by the autofix-lint workflow) enforces a trailing bare
`return` at the end of every cell function, even when it defines
nothing — that's how marimo marks a cell's outputs as complete. Ruff's
default rule set flags that same statement as "useless" (`PLR1711`).
These two tools fought over it (autofix workflow kept re-adding what
ruff had just removed) until we added `PLR1711` to `notebooks/ruff.toml`'s
`ignore` list. Don't remove that ignore or "clean up" a bare `return` at
the end of a cell — leave it as marimo's own convention.

**`notebooks/print.css` was deliberately removed** (see git history if
you're wondering why css_file support was ripped out). It was written to
patch the old browser-print-to-PDF path. Once PDFs moved to marimo's
native `export pdf` (nbconvert's WebPDF exporter via Playwright/Chromium,
not a literal print of the live HTML), we confirmed empirically — by
pixel-diffing every page of both notebooks' PDFs with the file present
vs. removed — that it had **zero effect** on that pipeline. Don't
re-add a `css_file` for print purposes; it won't do anything for
`marimo export pdf`, only for `marimo export html` printed manually via a
browser, which isn't part of this project's publish path.

## PDF export gotchas (read this before adding new tables/plots)

marimo's PDF export (`marimo export pdf`, used by
`scripts/export_notebooks.py`) rasterizes every `mo.ui.table` (and other
"interactive" outputs) into a static screenshot, in a **fixed 1440
CSS-pixel-wide browser viewport** (`_VIEWPORT_WIDTH` in marimo's own
`_server/export/_pdf_raster.py`), then renders the whole notebook as
HTML through nbconvert's WebPDF exporter (Playwright + Chromium). Three
real bugs/limitations in that pipeline (marimo 0.23.14/0.23.15, both
tested) show up as visible artifacts in the published PDF. We've worked
around all three, but **new tables/plots can retrigger them** if
they're big enough:

1. **Wide tables get silently cropped, not scaled down.** A table wider
   than the 1440px capture viewport doesn't shrink to fit — its trailing
   columns are simply cut off, with no visual sign in the PDF beyond the
   missing data (confirmed: a 14-column table at ~1670px wide lost its
   last two columns entirely). This is the most dangerous of the three
   because it's silent *data loss*, not just a cosmetic artifact.
   - **`_check_table_widths()` in `scripts/export_notebooks.py`** is a
     hard guard against this: it opens the exported HTML in a headless
     Chromium at a 1440px viewport (matching marimo's own capture
     width), measures every `<marimo-table>`'s actual rendered width
     (piercing its shadow root), and **fails the export** if any table
     exceeds 1440px — before the slow PDF export step even runs. This is
     a real guard, not a heuristic on the rendered PDF: we validated it
     against the original 14-column table (correctly flagged at
     ~1670px) and confirmed it stays silent on the fixed version.
   - If this check fails, the actual fix is to narrow the table: split
     off long-text columns into a separate, narrower table (see
     `categorical_panel()` in `checkpoint_1.py`, which splits a
     14-column profile table into a 12-column numeric/short-text table
     plus a 4-column free-text table), or drop/shorten columns.
   - We tried avoiding this by using `--raster-server live` (rasterizing
     against a real kernel connection instead of a disconnected static
     one - see bug #2 below) at one point, but that made cropping
     *worse*: the live, interactive `mo.ui.table` widget renders with
     extra chrome (checkboxes, search bar, wider padding) that pushes
     even normal tables past 1440px. **Don't use `--raster-server
     live`** - static mode's simpler read-only table rendering is the
     one that actually fits.

2. **"Static notebook" tooltip bleeding into a table screenshot.**
   marimo's default `--raster-server static` mode captures each widget
   without a live kernel, which makes the widget show a "not connected
   to a kernel" toast; that toast doesn't always get cleaned up between
   captures and can bleed into the *next* widget's screenshot, covering
   part of it (confirmed with a minimal 2-table reproduction). Unlike
   #1, this doesn't destroy data (the covered cells are still in the
   table, just visually obscured on that one export), and we did not
   find a fix that doesn't reintroduce #1 (see above) - it's a known,
   accepted cosmetic issue with static raster mode. If it starts
   appearing on a page that matters, re-running the export sometimes
   avoids it (it's timing-dependent), or reduce the number of tables
   rasterized close together.

3. **Blank pages from a bug in marimo's own screenshot stitching.**
   Long/tall rasterized outputs get captured via a multi-shot
   stitching process, and the stitched image can contain a blank band
   baked directly into its pixels (confirmed by extracting the raster
   images straight out of the PDF with `pdfimages` and inspecting them —
   this is not a CSS or print-pagination issue; our CSS has no effect on
   this pipeline at all, see above). This surfaced as several fully
   blank pages before we fixed it. Two mitigations, both already in place:
   - **Keep matplotlib figures compact.** The exploratory box
     plots/histograms used to stack one subplot per row
     (`figsize=(10, 2.8*n)` → up to 25in tall for 9 variables), which
     was tall enough to trigger the stitching bug. They now use a
     compact grid (`grid_cols = min(3, n)`, `grid_rows = ceil(n /
     grid_cols)`), keeping any figure under ~10in tall regardless of
     variable count. **Follow this pattern for any new multi-variable
     plot** — don't go back to a single tall column of subplots.
   - **`_drop_blank_pages()` in `scripts/export_notebooks.py`** opens
     the generated PDF with `pymupdf`, renders each page, and drops any
     page that's 100% pure white (every legitimate page in these
     notebooks has visible content, so this is an unambiguous signal of
     the bug, not a false positive). This is a safety net, not a fix —
     if you add a lot of new tables/plots and start seeing many blank
     pages again, the real fix is still to reduce individual output
     height (see above), not to lean on this post-processing step.

**When adding new tables or plots**: just run
`uv run python scripts/export_notebooks.py` - it now fails loudly with a
clear message if a table is too wide (bug #1). For the other two, also
look at the generated PDF page by page — `pdftoppm -png -r 100
docs/notebooks/checkpoint_1.pdf /tmp/page` then check each page, or use
ImageMagick (`magick page.png -format "%[fx:mean]" info:`) to
programmatically flag near-blank pages (`mean` close to `1.0` = white).
The live app and the HTML export look fine regardless of these bugs —
**only the generated PDF can show these artifacts**, so checking the
notebook in `marimo edit` or the exported HTML is not sufficient
verification for print-related changes.

## Commands

```bash
uv run pytest tests/ -v                        # marimo check, ruff, execution, spelling
uv run ruff check notebooks/                   # lint only
uv run ruff format notebooks/                  # format only
uv run python -m marimo check --fix notebooks/<nb>.py
uv run python scripts/export_notebooks.py      # full HTML+PDF export to docs/notebooks/
```

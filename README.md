# Setup

## 1. Install `uv`

`uv` is a fast Python package/project manager used to install dependencies and run commands.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 2. Install dependencies

From the project root, this installs `marimo` (and everything else pinned in `uv.lock`):

```bash
uv sync
```

## 3. Run the notebooks

Marimo notebooks live in the `notebooks/` directory. Start the editor from there:

```bash
cd notebooks
uv run marimo edit
```

This opens the marimo notebook editor in your browser. Pick a notebook file (e.g. `checkpoint_1.py`) to open it, or create a new one with `uv run marimo edit new_notebook.py`.

## 4. (Optional) Run a notebook without cloning the repo

Every notebook under `notebooks/` declares its own dependencies via a [PEP 723](https://peps.python.org/pep-0723/) inline script header, and `scripts/export_notebooks.py` publishes each notebook's raw `.py` source to `gh-pages` alongside its HTML export. That means `uvx` can download and run a notebook directly from its published URL, with `uv` installing exactly the packages it declares into an isolated environment — no local checkout, no `uv sync`:

```bash
uvx marimo edit --sandbox https://egsy-intell.github.io/team-project/notebooks/checkpoint_1.py
```

or, as a read-only app:

```bash
uvx marimo run --sandbox https://egsy-intell.github.io/team-project/notebooks/checkpoint_1.py
```

`scripts/run_notebook.sh [notebook-name] [edit|run]` wraps this for convenience (defaults to `checkpoint_1` in `edit` mode). The notebooks fetch `data/usgs/` and any sibling notebook modules (e.g. `data_dictionary.py`) straight from GitHub the first time they're needed when running this way, so no extra setup is required.

## 5. (Optional) VS Code extension

Install the [marimo extension](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo) for syntax support and running notebooks directly from the editor. It's already listed under recommended extensions for this workspace — VS Code should prompt you to install it when you open the project.

## 6. (Optional) Project utility CLI

`scripts/toolkit.py` bundles the project's build/export helpers behind one CLI, as subcommands — run `uv run python scripts/toolkit.py --help` to list them, or `... <subcommand> --help` for a subcommand's own options.

### Build the checkpoint slide deck

Presentation source lives under `preso/`: `checkpoint2_deck.md` is the deck content (pandoc slide-show markdown — `#`/`##` headings are slide breaks, `::: notes ... :::` blocks are per-slide speaker notes), and `template.pptx` is a reference-doc template (fonts, layouts, and the team logo — pandoc can only style master layouts from an existing `.pptx`, so this file is a styled copy of pandoc's stock reference doc, committed as-is; see `scripts/_bootstrap_template.py` if it ever needs regenerating).

Install the presentation-build dependencies (kept out of the default environment since they're only needed by whoever's building slides):

```bash
uv sync --group preso
```

Then regenerate the `.pptx` from the latest markdown source:

```bash
uv run python scripts/toolkit.py presentation
```

This writes `preso/dist/checkpoint2_deck.pptx` (gitignored — a build artifact, not committed) using `pypandoc`/`pypandoc_binary`, so no system `pandoc` install is required. Pass `--output-dir` to change where it's written, or `--open` to open it automatically in PowerPoint afterward (best-effort; macOS/Windows only, no-ops elsewhere). Upload the generated file to OneDrive manually — there's no automated publish step for slides, unlike the notebook HTML exports below.

### Print-friendly notebook export

marimo's HTML export is built as a single-page app, not a paginated document, and none of its layout survives Chrome's print pagination unmodified: the notebook body sits inside a viewport-height, scroll-clipped shell (so printing loses everything past the first screenful — blank pages, content cut off mid-page), `mo.vstack()` layout blocks render as CSS flex containers that Chrome's print engine won't fragment across a page break (a tall one gets shoved whole onto a fresh page, leaving a large blank gap on the page before it), the content column is hard-capped at a fixed desktop width wider than a printed page (wide tables run past the margin instead of wrapping), and headings have no "keep with next" rule (a heading can land alone at the bottom of a page with its content pushed to the next one).

`clean-notebook` exports a marimo notebook to HTML and patches in a print-only CSS/JS fix for all of the above, without touching the notebook's normal on-screen appearance:

```bash
uv run python scripts/toolkit.py clean-notebook
```

With no arguments this runs `marimo export html` locally against `notebooks/index.py` (the full report) and writes `index_clean.html` in the current directory — a fresh export straight from the notebook source, not the possibly-stale copy on `gh-pages`. Like `molab`, the export excludes the notebook's source code by default (marimo's own `--include-code`/`--no-include-code` flag, which `scripts/export_notebooks.py`'s `gh-pages` publish step doesn't set, so that copy still includes code); pass `--include-code` to embed it instead.

`INPUT` (the first positional argument) can override what gets exported/patched:

- a different local notebook `.py` file — exported the same way as the default
- a local `.html` file, or a URL (e.g. the published `https://egsy-intell.github.io/team-project/notebooks/`) — patched as-is, no export step; `--include-code` doesn't apply here, since the code was already baked in (or not) when that HTML was built

`--name` and `--output-dir` override the output filename (default: `<input stem>_clean.html`) and directory (default: current directory). Open the result in a browser and print/"Save as PDF" as usual — no extra tooling required at print time, the fix is baked into the file.

# Marimo Quick Reference

Marimo notebooks are just Python files — no hidden state, no `.ipynb` JSON.

- **Cells run automatically**: when you edit a cell, marimo re-runs it and any other cells that depend on its variables. No more "run all cells in order" bugs.
- **Variables are reactive**: define a variable in one cell, use it in another — marimo tracks the dependency graph for you.
- **No duplicate variable names**: unlike Jupyter, you can't redefine the same variable in two cells; each variable belongs to exactly one cell.
- **UI elements are reactive too**: widgets like `mo.ui.slider(...)` automatically re-run dependent cells when changed — no callbacks needed.
- **Run as a script**: any marimo notebook can be executed directly with `python notebook.py` or `uv run notebook.py`.
- **Keyboard shortcuts**: `Ctrl/Cmd+Enter` runs a cell, `Ctrl/Cmd+Shift+Enter` runs all cells.

Docs: https://docs.marimo.io

# CI/CD

GitHub Actions runs two workflows (see `.github/workflows/`):

- **`ci.yml`** — on every push/PR to `main`, installs dependencies with `uv` and runs `pytest tests/`, which:
  - spell-checks the text in every notebook under `notebooks/` with [`codespell`](https://github.com/codespell-project/codespell)
  - confirms every notebook executes cleanly via `marimo export html`
- **`autofix-typos.yml`** — on every PR into `main` (from a branch in this repo, not a fork), runs `codespell -w` on `notebooks/` and pushes a `Fix typos (autofix)` commit back to the PR branch if it finds anything to fix, so `ci.yml`'s spelling check turns green without manual effort.
- **`publish.yml`** — on push to `main` (i.e. after a merge), re-runs the tests, exports each notebook in `notebooks/` to a standalone HTML file (`docs/notebooks/<notebook_name>.html`) plus a copy of its raw `.py` source (`docs/notebooks/<notebook_name>.py`) via `scripts/export_notebooks.py`, and publishes that directory to the `gh-pages` branch under `docs/notebooks/` using [`peaceiris/actions-gh-pages`](https://github.com/peaceiris/actions-gh-pages) — matching this repo's GitHub Pages source (`gh-pages` branch, `/docs` folder), so the exported notebooks show up at `https://egsy-intell.github.io/team-project/notebooks/<notebook_name>.html` and the raw source at `https://egsy-intell.github.io/team-project/notebooks/<notebook_name>.py` (runnable directly with `uvx`, see step 4 above).

To reproduce the export locally:

```bash
uv run python scripts/export_notebooks.py
```

To fix typos locally instead of waiting on CI (e.g. when working from a fork):

```bash
uv run codespell -w notebooks/
```

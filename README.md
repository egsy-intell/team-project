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

## 4. (Optional) VS Code extension

Install the [marimo extension](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo) for syntax support and running notebooks directly from the editor. It's already listed under recommended extensions for this workspace — VS Code should prompt you to install it when you open the project.

# Marimo Quick Reference

Marimo notebooks are just Python files — no hidden state, no `.ipynb` JSON.

- **Cells run automatically**: when you edit a cell, marimo re-runs it and any other cells that depend on its variables. No more "run all cells in order" bugs.
- **Variables are reactive**: define a variable in one cell, use it in another — marimo tracks the dependency graph for you.
- **No duplicate variable names**: unlike Jupyter, you can't redefine the same variable in two cells; each variable belongs to exactly one cell.
- **UI elements are reactive too**: widgets like `mo.ui.slider(...)` automatically re-run dependent cells when changed — no callbacks needed.
- **Run as a script**: any marimo notebook can be executed directly with `python notebook.py` or `uv run notebook.py`.
- **Keyboard shortcuts**: `Ctrl/Cmd+Enter` runs a cell, `Ctrl/Cmd+Shift+Enter` runs all cells.

Docs: https://docs.marimo.io

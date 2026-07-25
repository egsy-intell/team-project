# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.14",
#     "pandas>=3.0.3",
# ]
# ///

import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    # When this notebook is opened from a local checkout, checkpoint_1.py
    # sits right next to it. When marimo downloads it standalone from a URL
    # (e.g. `uvx marimo edit --sandbox <gh-pages-url>`), that sibling file
    # isn't there, so fetch it from the same repo location it was published
    # from and import it from a temp dir instead.
    try:
        from checkpoint_1 import app as checkpoint_1_app
    except ModuleNotFoundError:
        import sys as _sys
        import tempfile as _tempfile
        import urllib.request as _urllib_request

        _RAW_BASE = "https://raw.githubusercontent.com/egsy-intell/team-project/main/notebooks"
        _tmp_dir = _tempfile.mkdtemp(prefix="egsy-pfas-")
        _dest = f"{_tmp_dir}/checkpoint_1.py"
        _urllib_request.urlretrieve(f"{_RAW_BASE}/checkpoint_1.py", _dest)
        _sys.path.insert(0, _tmp_dir)

        from checkpoint_1 import app as checkpoint_1_app
    return checkpoint_1_app, mo


@app.cell(hide_code=True)
async def _(checkpoint_1_app):
    checkpoint_1_result = await checkpoint_1_app.embed()
    mc_clean_df = checkpoint_1_result.defs["mc_clean_df"]
    ss_clean_df = checkpoint_1_result.defs["ss_clean_df"]
    return mc_clean_df, ss_clean_df


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Checkpoint 2 start!
    """)
    return


@app.cell(hide_code=True)
def _(mc_clean_df, mo, ss_clean_df):
    mo.md(
        f"Inherited from checkpoint 1: `mc_clean_df` "
        f"({mc_clean_df.shape[0]} rows), `ss_clean_df` "
        f"({ss_clean_df.shape[0]} rows)."
    )
    return


if __name__ == "__main__":
    app.run()

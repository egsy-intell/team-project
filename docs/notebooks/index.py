# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.14",
# ]
# ///

import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    # When this notebook is opened from a local checkout, checkpoint_1.py,
    # checkpoint_2.py, and footer.py sit right next to it. When marimo
    # downloads it standalone from a URL (e.g. `uvx marimo edit --sandbox
    # <gh-pages-url>`), those sibling files aren't there, so fetch them from
    # the same repo location this notebook was published from and import
    # them from a temp dir instead.
    try:
        from checkpoint_1 import app as checkpoint_1_app
        from checkpoint_2 import app as checkpoint_2_app
        from footer import app as footer_app
    except ModuleNotFoundError:
        import sys as _sys
        import tempfile as _tempfile
        import urllib.request as _urllib_request

        _RAW_BASE = "https://raw.githubusercontent.com/egsy-intell/team-project/main/notebooks"
        _tmp_dir = _tempfile.mkdtemp(prefix="egsy-pfas-")
        for _name in ("checkpoint_1.py", "checkpoint_2.py", "footer.py"):
            _urllib_request.urlretrieve(
                f"{_RAW_BASE}/{_name}", f"{_tmp_dir}/{_name}"
            )
        _sys.path.insert(0, _tmp_dir)

        from checkpoint_1 import app as checkpoint_1_app
        from checkpoint_2 import app as checkpoint_2_app
        from footer import app as footer_app
    return checkpoint_1_app, checkpoint_2_app, footer_app, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # PFAS Occurrence Risk — Combined Report
    """)
    return


@app.cell(hide_code=True)
async def _(checkpoint_1_app):
    checkpoint_1_result = await checkpoint_1_app.embed()
    return (checkpoint_1_result,)


@app.cell(hide_code=True)
def _(checkpoint_1_result, mo):
    mo.vstack([checkpoint_1_result.output])
    return


@app.cell(hide_code=True)
async def _(checkpoint_2_app):
    checkpoint_2_result = await checkpoint_2_app.embed()
    return (checkpoint_2_result,)


@app.cell(hide_code=True)
def _(checkpoint_2_result, mo):
    mo.vstack([checkpoint_2_result.output])
    return


@app.cell(hide_code=True)
async def _(footer_app):
    footer_result = await footer_app.embed()
    return (footer_result,)


@app.cell(hide_code=True)
def _(footer_result, mo):
    mo.vstack([footer_result.output])
    return


if __name__ == "__main__":
    app.run()

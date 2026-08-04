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
        from checkpoint_3 import app as checkpoint_3_app
        from footer import app as footer_app
    except ModuleNotFoundError:
        import sys as _sys
        import tempfile as _tempfile
        import urllib.request as _urllib_request

        _RAW_BASE = "https://raw.githubusercontent.com/egsy-intell/team-project/main/notebooks"
        _tmp_dir = _tempfile.mkdtemp(prefix="egsy-pfas-")
        for _name in (
            "checkpoint_1.py",
            "checkpoint_2.py",
            "checkpoint_3.py",
            "footer.py",
        ):
            _urllib_request.urlretrieve(
                f"{_RAW_BASE}/{_name}", f"{_tmp_dir}/{_name}"
            )
        _sys.path.insert(0, _tmp_dir)

        from checkpoint_1 import app as checkpoint_1_app
        from checkpoint_2 import app as checkpoint_2_app
        from checkpoint_3 import app as checkpoint_3_app
        from footer import app as footer_app
    return (
        checkpoint_1_app,
        checkpoint_2_app,
        checkpoint_3_app,
        footer_app,
        mo,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # PFAS Occurrence Risk — Full Report
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md("""
    ## Team .egsy intelligence (Group #14)
    * Emir Beg
    * Gulshan Raj Shetty (Raj)
    * Somyaranjan Sahu
    * Yaisiel (Yai) Torres

    ## Team roles and task delegation
    """),
            mo.center(
                mo.md("""
    | Name | Role | Superpowers |
    |---|---|---|
    | Yai Torres | Proposal/Docs/Presentation Lead | Web dev, organization |
    | Raj Shetty | Modeling & Press. Lead A | Data analysis, exploration |
    | Emir Beg | Modeling & Press. Lead B | Software arch., big data |
    | Somyaranjan | Model Quality & PM Support Lead | Problem-solving, QA |
    """)
            ),
            mo.md("""
    * **Yai** led problem definition, data curation across all three
      sources, and the data dictionary (Steps 1-2); has also served
      as the team's data-platform lead and a general technical
      resource across every workstream rather than one fixed slice;
      laid the validation groundwork in Step 3, co-leading its
      Step 5 model validation and benchmarking with Somyaranjan;
      leads the project write-up and slide deck through the final
      submission, co-leading the presentation with Emir.
    * **Raj** drafted the data source and ethical-considerations
      review and led the categorical-variable quality assessment
      (Step 2); leads the study-grouped split strategy, groundwater
      hold-out decision, and interpretable baseline classifier
      (Steps 3-4), carried into its Step 5 execution and evaluation.
    * **Emir** led the summary-statistics, outlier, and skewness
      analysis (Step 2); leads the optional scalability/deployment
      metric and the competing ensemble model (Steps 3-4), carried
      into its Step 5 execution and evaluation; co-leads the
      presentation with Yai.
    * **Somyaranjan** leads the per-class metrics framework,
      risk-tier threshold decision, skew handling/encoding on the
      finalized feature table, and the validation groundwork laid
      in Step 3 (Steps 3-4); leads running predictions and
      evaluation/retuning across both models, co-leading Step 5
      model validation and benchmarking with Yai; also provides
      project management support across the team.
    """),
        ]
    )
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
def _(mo):
    mo.md(r"""
    With the ∑TQ target constructed above, the report turns next to
    Steps 3–4: how a classifier trained on that target would be
    evaluated, and what modeling techniques are proposed to build it.
    """)
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
def _(mo):
    mo.md(r"""
    With an evaluation plan and two proposed modeling techniques in
    place, the report turns finally to Step 5: training and tuning
    both models, evaluating them against that plan, and discussing
    deployment feasibility.
    """)
    return


@app.cell(hide_code=True)
async def _(checkpoint_3_app):
    checkpoint_3_result = await checkpoint_3_app.embed()
    return (checkpoint_3_result,)


@app.cell(hide_code=True)
def _(checkpoint_3_result, mo):
    mo.vstack([checkpoint_3_result.output])
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

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
    task_callout = checkpoint_1_result.defs["task_callout"]
    return mc_clean_df, ss_clean_df, task_callout


@app.cell(hide_code=True)
def _(mc_clean_df, mo, ss_clean_df):
    mo.md(f"""
    # Step 3-4: Model Selection, Training & Evaluation Design (Checkpoint 2)

    This notebook is Check-In #2's deliverable: a formal evaluation plan
    (Step 3) and a set of proposed modeling techniques (Step 4), per
    `specs/checkpoint-2/GRAD 50400 - Project Checkpoint-2.pdf`. It's a
    **design/proposal document** — each section below states what a task
    lead will argue and how, not yet an executed evaluation. Execution and
    retuning (Step 5, task `EVAL`) is out of scope here and belongs to the
    final checkpoint.

    Every section carries a callout naming its task ID, category, lead, and
    dependencies, tied to `planning/checkpoint-2/checkpoint2_tasks.csv`; use
    the task ID to cross-reference the task board.

    Inherited from checkpoint 1's Step 2 cleaning and Pre-work (Task PW):
    `mc_clean_df` ({mc_clean_df.shape[0]} rows), `ss_clean_df`
    ({ss_clean_df.shape[0]} rows).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Step 3: Evaluation Plan

    Per spec section 2.3: a formal plan to evaluate model efficacy,
    identifying metrics and why they're appropriate, what constitutes
    success, what data evaluation uses (and whether that should differ from
    training data), and a method for evaluation.
    """)
    return


@app.cell(hide_code=True)
def _(mo, task_callout):
    mo.vstack(
        [
            mo.md(
                "### Per-class metrics (precision/recall/F1, confusion matrix)"
            ),
            task_callout(
                "3.1",
                category="Step 3 - Evaluation Plan",
                lead="Somyaranjan",
                summary=(
                    "Define the primary classification metrics for the "
                    "∑TQ risk-tier target: per-class precision/recall/F1 and "
                    "a confusion matrix, with an explanation of why these "
                    "matter more here than plain accuracy (class imbalance "
                    "across risk tiers, and asymmetric cost of missing a "
                    "high-risk site vs. a false alarm)."
                ),
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, task_callout):
    mo.vstack(
        [
            mo.md("### Success threshold - risk-tier cutoffs"),
            task_callout(
                "3.2",
                category="Step 3 - Evaluation Plan",
                lead="Somyaranjan, Team",
                depends_on="PW",
                summary=(
                    "Decide what constitutes success for the model against "
                    "the ∑TQ risk tiers (`within_reduced_monitoring`, "
                    "`above_trigger`, `mcl_exceedance`) — e.g. minimum "
                    "recall on the highest-risk tier — once Task PW's "
                    "reshaped/joined ∑TQ target is available to profile."
                ),
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, task_callout):
    mo.vstack(
        [
            mo.md("### Split strategy - group by study"),
            task_callout(
                "3.3",
                category="Step 3 - Evaluation Plan",
                lead="Raj",
                summary=(
                    "Design a train/test split grouped by study "
                    "(Smalling, Seawolf, McMahon) rather than a random "
                    "row-wise split, so evaluation measures generalization "
                    "across studies/sampling designs instead of leaking "
                    "sites from the same study into both sets."
                ),
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, task_callout):
    mo.vstack(
        [
            mo.md("### Groundwater's role - held-out vs. combined"),
            task_callout(
                "3.4",
                category="Step 3 - Evaluation Plan",
                lead="Raj, Yai",
                depends_on="3.3",
                summary=(
                    "Decide whether McMahon's groundwater data trains "
                    "alongside Smalling/Seawolf's surface-water data or is "
                    "held out as a separate evaluation slice, given "
                    "McMahon's already-noted join-ability and coverage "
                    "differences from Step 2, once the study-grouped split "
                    "strategy (3.3) is settled."
                ),
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, task_callout):
    mo.vstack(
        [
            mo.md(
                "### Scalability / deployment metric (optional third proposal)"
            ),
            task_callout(
                "3.5",
                category="Step 3 - Evaluation Plan",
                lead="Emir",
                summary=(
                    "Optional third evaluation proposal beyond predictive "
                    "accuracy: whether the model runs fast enough and "
                    "scales to the number of sites an operator would "
                    "realistically screen, per the spec's note that "
                    "metrics can extend past task accuracy alone."
                ),
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Step 4: Modeling Techniques

    Per spec section 2.4: identify specific modeling techniques, why each is
    appropriate, what tools will be used, and the computational/other
    resources needed. At least two proposals, led by different team
    members.
    """)
    return


@app.cell(hide_code=True)
def _(mo, task_callout):
    mo.vstack(
        [
            mo.md(
                "### Handling skew & encoding on the finalized feature table"
            ),
            task_callout(
                "4.4",
                category="Step 4 - Modeling Techniques",
                lead="Somyaranjan",
                depends_on="PW",
                summary=(
                    "Apply the scaling/encoding plan from checkpoint 1's "
                    "Step 2.5 to the finalized feature table produced by "
                    "Task PW: transform right-skewed geospatial/land-use "
                    "predictors, and finalize binary/one-hot encoding for "
                    "categorical fields, fit on training data only."
                ),
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, task_callout):
    mo.vstack(
        [
            mo.md("### Tooling & compute plan for baseline"),
            task_callout(
                "4.2",
                category="Step 4 - Modeling Techniques",
                lead="Raj, Yai",
                summary=(
                    "Tooling (e.g. scikit-learn) and compute needs shared "
                    "by the baseline model proposal below: expected "
                    "dataset size, training time, and hardware "
                    "requirements on a standard machine, no foundation "
                    "model or GPU dependency expected."
                ),
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, task_callout):
    mo.vstack(
        [
            mo.md("### Baseline model: interpretable classifier (Lead A)"),
            task_callout(
                "4.1",
                category="Step 4 - Modeling Techniques",
                lead="Raj",
                depends_on="3.2, 4.4",
                summary=(
                    "First modeling proposal: an interpretable classifier "
                    "(e.g. logistic regression or a shallow decision "
                    "tree) predicting the ∑TQ risk tier from land-use "
                    "predictors only, chosen for legibility to water-"
                    "resource operators and as a baseline the competing "
                    "proposal below is measured against."
                ),
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, task_callout):
    mo.vstack(
        [
            mo.md("### Competing model: hierarchical / ensemble (Lead B)"),
            task_callout(
                "4.3",
                category="Step 4 - Modeling Techniques",
                lead="Emir",
                depends_on="3.2, 4.4",
                summary=(
                    "Second modeling proposal: a hierarchical or ensemble "
                    "classifier (e.g. random forest / gradient boosting) "
                    "that can capture non-linear interactions between "
                    "land-use predictors the baseline's linear form "
                    "cannot, evaluated against the same metrics and split "
                    "as Model A for a direct comparison."
                ),
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Conclusion

    Checkpoint 2 establishes, but does not yet execute, the evaluation plan
    and modeling proposals for classifying site-level PFAS risk from
    land-use predictors: per-class metrics and a study-grouped split (Step
    3), and two competing classifiers, an interpretable baseline and a
    non-linear ensemble (Step 4). Implementing Task PW's ∑TQ target,
    training both models, and evaluating them against the plan above is
    Step 5 work for the final checkpoint.
    """)
    return


if __name__ == "__main__":
    app.run()

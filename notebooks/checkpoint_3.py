# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
#     "numpy",
#     "pandas>=3.0.3",
#     "scikit-learn",
# ]
# ///

import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    # When this notebook is opened from a local checkout, checkpoint_1.py
    # and checkpoint_2.py sit right next to it. When marimo downloads it
    # standalone from a URL (e.g. `uvx marimo edit --sandbox
    # <gh-pages-url>`), those sibling files aren't there, so fetch them
    # from the same repo location it was published from and import them
    # from a temp dir instead.
    try:
        from checkpoint_1 import app as checkpoint_1_app
        from checkpoint_2 import app as checkpoint_2_app
    except ModuleNotFoundError:
        import sys as _sys
        import tempfile as _tempfile
        import urllib.request as _urllib_request

        _RAW_BASE = (
            "https://raw.githubusercontent.com/egsy-intell/"
            "team-project/main/notebooks"
        )
        _tmp_dir = _tempfile.mkdtemp(prefix="egsy-pfas-")
        for _name in ("checkpoint_1.py", "checkpoint_2.py"):
            _urllib_request.urlretrieve(
                f"{_RAW_BASE}/{_name}", f"{_tmp_dir}/{_name}"
            )
        _sys.path.insert(0, _tmp_dir)

        from checkpoint_1 import app as checkpoint_1_app
        from checkpoint_2 import app as checkpoint_2_app
    return checkpoint_1_app, checkpoint_2_app, mo


@app.cell(hide_code=True)
async def _(checkpoint_1_app):
    checkpoint_1_result = await checkpoint_1_app.embed()
    task_callout = checkpoint_1_result.defs["task_callout"]
    return (task_callout,)


@app.cell(hide_code=True)
async def _(checkpoint_2_app):
    checkpoint_2_result = await checkpoint_2_app.embed()
    tapwater_train_df = checkpoint_2_result.defs["tapwater_train_df"]
    tapwater_test_df = checkpoint_2_result.defs["tapwater_test_df"]
    return tapwater_test_df, tapwater_train_df


@app.cell(hide_code=True)
def _(mo, tapwater_test_df, tapwater_train_df):
    mo.md(f"""
    # Step 5: Model Execution, Evaluation & Deployment

    This notebook is the final report's deliverable: training and
    tuning the two models proposed in Step 4, evaluating them against
    the Step 3 plan, and discussing deployment feasibility. It carries
    forward the Step 3-4 report's study-grouped training/test partition —
    `tapwater_train_df` ({tapwater_train_df.shape[0]} rows) and
    `tapwater_test_df` ({tapwater_test_df.shape[0]} rows) — and its
    per-class metrics, risk-tier thresholds, and preprocessing pipeline.

    This is a **header skeleton** — section structure and open questions
    only, per `planning/checkpoint-3/checkpoint3_task_plan.csv`. Pending
    sections carry a callout naming their task ID, lead, and
    dependencies from that plan; use the task ID to cross-reference the
    task board. Tasks tracking project logistics the spec doesn't ask
    the report itself to cover (the writeup/deck/video, submission, and
    individual peer review) aren't reflected here — only the public
    codebase link the spec does require the report to mention.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Foundations carried into Step 5

    Two closeout items from earlier steps feed directly into Step 5's
    model training and are settled before it begins.

    ### Finalized classification pipeline

    The ∑TQ classification pipeline now resolves the two compounds with
    no benchmark in either source, PFPeS and PFPrS, and runs against the
    complete 716-sample Table S10 dataset rather than a partial extract,
    so the training and test partitions above reflect the full available
    sample.

    ### Verified source citations

    The state-agency primary sources behind Table S5's state-only
    benchmarks, and the CDM Smith EPA Final PFAS Regulations fact sheet
    URL cited in the methods section, are confirmed against their
    original publications.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Check-In #2 feedback integration

    Per the spec, the final submission must integrate at least one item
    from the peer feedback the team received on Check-In #2.
    """)
    return


@app.cell(hide_code=True)
def _(mo, task_callout):
    mo.vstack(
        [
            mo.md("### Triage peer feedback"),
            task_callout(
                "T3",
                category="Feedback integration",
                lead="Yai, Somyaranjan",
                summary=(
                    "Review the peer feedback received on Check-In #2 "
                    "and select at least one item the team will "
                    "integrate into the final submission."
                ),
                guiding_questions=[
                    (
                        "Which feedback items are actionable within the "
                        "remaining Step 5 timeline versus out of scope for "
                        "this submission?"
                    ),
                    (
                        "Does any item conflict with a decision the team "
                        "already made in the Step 3-4 report (e.g. the "
                        "groundwater hold-out, the risk-tier thresholds), "
                        "and if so, which one wins?"
                    ),
                    (
                        "Is the selected item a modeling change, an "
                        "evaluation change, or a writeup/clarity change — "
                        "and does that determine who should own T4?"
                    ),
                ],
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, task_callout):
    mo.vstack(
        [
            mo.md("### Implement feedback change"),
            task_callout(
                "T4",
                category="Feedback integration",
                lead="Owner set by T3",
                depends_on="T3",
                summary=(
                    "Make the scoped change identified in T3, in "
                    "whichever part of the pipeline or notebook it "
                    "touches."
                ),
                guiding_questions=[
                    (
                        "Does this change touch anything upstream of model "
                        "training (T5/T6) closely enough that it should "
                        "land before those tasks start rather than after?"
                    ),
                    (
                        "How will the change be called out in the writeup "
                        "so a reader can see it was a direct response to "
                        "peer feedback, not an unrelated revision?"
                    ),
                ],
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Step 5: Model Training & Execution

    Carries Step 4's two proposed models, the interpretable baseline
    (Model A) and the competing ensemble (Model B), from proposal into
    trained, tuned classifiers.
    """)
    return


@app.cell(hide_code=True)
def _(mo, task_callout):
    mo.vstack(
        [
            mo.md("### Build baseline model"),
            task_callout(
                "T5",
                category="Step 5 - Model Training",
                lead="Raj",
                depends_on="T1",
                summary=(
                    "Implement and train the interpretable baseline "
                    "classifier (Model A) proposed in Step 4, using the "
                    "Step 3-4 report's study-grouped training partition "
                    "and tuning grid."
                ),
                guiding_questions=[
                    (
                        "Does the actual training run surface any predictor "
                        "or preprocessing issue the Step 4 proposal didn't "
                        "anticipate (e.g. a category unseen in a training "
                        "fold)?"
                    ),
                    (
                        "Do the tuned coefficients support the "
                        "interpretability claim made in Step 4, or do any "
                        "of them run counter to the expected direction?"
                    ),
                ],
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, task_callout):
    mo.vstack(
        [
            mo.md("### Build competing model"),
            task_callout(
                "T6",
                category="Step 5 - Model Training",
                lead="Emir",
                depends_on="T1",
                summary=(
                    "Implement and train the competing ensemble "
                    "classifier (Model B) proposed in Step 4, using the "
                    "same training partition and grouped "
                    "cross-validation as Model A."
                ),
                guiding_questions=[
                    (
                        "Does the tuned forest actually pick up the "
                        "nonlinear/interaction effects Step 4 predicted, or "
                        "do feature importances look close to Model A's "
                        "coefficient ranking?"
                    ),
                    (
                        "Is the tuning grid still computationally cheap "
                        "enough at the full 716-sample dataset size, or "
                        "does it need trimming?"
                    ),
                ],
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Step 5: Prediction, Evaluation & Benchmarking

    Scores both trained models against the held-out studies and Step
    3's success criteria.
    """)
    return


@app.cell(hide_code=True)
def _(mo, task_callout):
    mo.vstack(
        [
            mo.md("### Run predictions & retune"),
            task_callout(
                "T7",
                category="Step 5 - Evaluation",
                lead="Yai, Somyaranjan",
                depends_on="T5, T6",
                summary=(
                    "Score both trained models on the held-out test "
                    "set; evaluate and retune to improve accuracy. Run "
                    "as a joint execution, pairing directly through the "
                    "step."
                ),
                guiding_questions=[
                    (
                        "Does either model clear the 0.70 recall floor on "
                        "`mcl_exceedance` from Step 3, and if neither does, "
                        "what does the retuning pass prioritize first?"
                    ),
                    (
                        "Are the errors concentrated in one held-out study "
                        "(McMahon-style groundwater generalization risk) or "
                        "spread evenly, and does that change which model "
                        "looks preferable?"
                    ),
                    (
                        "After retuning, does the comparison between Model "
                        "A and Model B change which one the team "
                        "recommends, relative to the Step 4 prediction?"
                    ),
                ],
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, task_callout):
    mo.vstack(
        [
            mo.md("### Scalability / deployment metric"),
            task_callout(
                "T8",
                category="Step 5 - Evaluation",
                lead="Emir",
                depends_on="T6",
                summary=(
                    "Optional scalability and deployment-metric "
                    "analysis on the competing model, carrying Step "
                    "3's third evaluation proposal into execution."
                ),
                guiding_questions=[
                    (
                        "At what number of sites, if any, does batch-scoring "
                        "throughput become a practical concern for an "
                        "operator screening a full monitoring network?"
                    ),
                    (
                        "Is this worth including in the final writeup given "
                        "the team's remaining time, or does it stay "
                        "optional?"
                    ),
                ],
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, task_callout):
    mo.vstack(
        [
            mo.md("### Model validation & benchmarking"),
            task_callout(
                "T9",
                category="Step 5 - Evaluation",
                lead="Yai, Somyaranjan",
                depends_on="T7",
                summary=(
                    "Apply the per-class metrics framework and "
                    "risk-tier thresholds to both models; benchmark "
                    "against the Step 3 evaluation plan."
                ),
                guiding_questions=[
                    (
                        "How do the tuned models compare to the majority "
                        "baseline and to each other on macro-F1 and "
                        "per-tier recall, not just on `mcl_exceedance`?"
                    ),
                    (
                        "Does the benchmarking result change which model "
                        "the team recommends for the deployment discussion "
                        "in T10?"
                    ),
                ],
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Step 5: Deployment Discussion
    """)
    return


@app.cell(hide_code=True)
def _(mo, task_callout):
    mo.vstack(
        [
            mo.md("### Deployment & lessons-learned narrative"),
            task_callout(
                "T10",
                category="Step 5 - Deployment",
                lead="Emir, Yai",
                depends_on="T8, T9",
                summary=(
                    "Draft the discussion of deployment feasibility, "
                    "pitfalls, and lessons learned required by Step 5."
                ),
                guiding_questions=[
                    (
                        "What would an operator need beyond the model "
                        "itself to actually use it (input data availability, "
                        "refresh cadence, who interprets a flagged site)?"
                    ),
                    (
                        "What's the single biggest pitfall the team ran "
                        "into across Steps 1-5 that a future team repeating "
                        "this project should know about going in?"
                    ),
                    (
                        "Does the recommended model's main limitation "
                        "(interpretability vs. accuracy, or the McMahon "
                        "generalization gap) change the deployment "
                        "recommendation itself?"
                    ),
                ],
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, task_callout):
    mo.vstack(
        [
            mo.md("## Public codebase"),
            mo.md("""
    Per the spec, the report and presentation must both link the
    public codebase. This project's codebase is public at
    <https://github.com/egsy-intell/team-project>, the same repository
    this report itself is published from.
    """),
            task_callout(
                "T11",
                category="Step 5 - Submission",
                lead="Yai, Raj",
                depends_on="T4, T5, T6",
                summary=(
                    "Push Step 5 code to the public repo and confirm "
                    "it's publicly accessible for the writeup/deck link, "
                    "once the feedback change and both models have "
                    "landed."
                ),
                guiding_questions=[
                    (
                        "Right before submission, does a signed-out "
                        "browser (not just a logged-in team member) "
                        "actually load the repo without a permission "
                        "prompt?"
                    ),
                    (
                        "Does the linked repo state match what the "
                        "writeup describes, or is there unmerged work "
                        "the writeup depends on?"
                    ),
                ],
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()

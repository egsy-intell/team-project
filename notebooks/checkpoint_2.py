# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
#     "matplotlib>=3.11.1",
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

        _RAW_BASE = (
            "https://raw.githubusercontent.com/egsy-intell/"
            "team-project/main/notebooks"
        )
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
    mc_scored_df = checkpoint_1_result.defs["mc_scored_df"]
    ss_scored_df = checkpoint_1_result.defs["ss_scored_df"]
    task_callout = checkpoint_1_result.defs["task_callout"]
    return mc_clean_df, mc_scored_df, ss_scored_df, task_callout


@app.cell(hide_code=True)
def _(mc_clean_df, mc_scored_df, mo, ss_scored_df):
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

    Inherited from checkpoint 1's Step 2 cleaning and ∑TQ construction:
    `ss_scored_df` ({ss_scored_df.shape[0]} rows), `mc_scored_df`
    ({mc_scored_df.shape[0]} rows). `mc_clean_df` ({mc_clean_df.shape[0]}
    rows) is also available unscored — McMahon's role (combined vs.
    held-out, task `3.4`) isn't decided yet, so both are kept until
    that's settled.
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
def _(mc_scored_df, mo, ss_scored_df, task_callout):
    from itertools import combinations

    import pandas as pd
    from sklearn.model_selection import StratifiedGroupKFold

    risk_labels = [
        "within_reduced_monitoring",
        "above_trigger",
        "mcl_exceedance",
    ]

    # Smalling provides the measured outcome, so Study_smalling is the
    # canonical grouping field. The matched Seawolf predictor row follows the
    # same site into whichever partition that Smalling study is assigned to.
    study_group_column = (
        "Study_smalling"
        if "Study_smalling" in ss_scored_df.columns
        else "Study_seawolf"
    )

    # Provisional cutoffs pending Task 3.2 (Somyaranjan/Team).
    # Update these constants once the risk-tier thresholds are finalized.
    WITHIN_MONITORING_CUTOFF = 0.5
    MCL_EXCEEDANCE_CUTOFF = 1.0

    tapwater_split_df = ss_scored_df.copy()
    tapwater_split_df["pfas_risk_tier"] = pd.cut(
        tapwater_split_df["sum_tq_epa"],
        bins=[
            float("-inf"),
            WITHIN_MONITORING_CUTOFF,
            MCL_EXCEEDANCE_CUTOFF,
            float("inf"),
        ],
        labels=risk_labels,
        right=False,
        ordered=True,
    )
    tapwater_split_df["study_group"] = (
        tapwater_split_df[study_group_column]
        .astype("string")
        .str.strip()
    )
    tapwater_split_df = tapwater_split_df.dropna(
        subset=["Site Code", "study_group", "pfas_risk_tier"]
    ).copy()

    # Review the number of sites and target classes available in each study
    # before selecting a holdout. Whole-study splits cannot guarantee exact
    # row-level stratification.
    study_risk_profile = (
        tapwater_split_df.groupby(
            ["study_group", "pfas_risk_tier"],
            observed=False,
        )
        .size()
        .unstack(fill_value=0)
        .reindex(columns=risk_labels, fill_value=0)
        .reset_index()
    )
    study_risk_profile["Sites"] = study_risk_profile[risk_labels].sum(axis=1)
    study_risk_profile = study_risk_profile[
        ["study_group", "Sites", *risk_labels]
    ].sort_values(["Sites", "study_group"], ascending=[False, True])

    all_studies = sorted(
        tapwater_split_df["study_group"].unique().tolist()
    )
    full_distribution = (
        tapwater_split_df["pfas_risk_tier"]
        .value_counts(normalize=True)
        .reindex(risk_labels, fill_value=0.0)
    )

    def score_split(
        train_part,
        test_part,
        full_data,
        labels,
        overall_distribution,
    ):
        train_classes = set(train_part["pfas_risk_tier"].dropna())
        test_classes = set(test_part["pfas_risk_tier"].dropna())
        missing_class_penalty = (
            len(set(labels) - train_classes)
            + len(set(labels) - test_classes)
        )

        test_fraction = len(test_part) / len(full_data)
        test_distribution = (
            test_part["pfas_risk_tier"]
            .value_counts(normalize=True)
            .reindex(labels, fill_value=0.0)
        )
        distribution_gap = float(
            (test_distribution - overall_distribution).abs().sum()
        )

        selection_score = (
            missing_class_penalty * 10
            + abs(test_fraction - 0.20)
            + distribution_gap
        )
        return {
            "test_fraction": test_fraction,
            "missing_class_penalty": missing_class_penalty,
            "distribution_gap": distribution_gap,
            "selection_score": selection_score,
        }

    candidate_rows = []
    for held_out_count in range(1, len(all_studies)):
        for held_out_studies in combinations(
            all_studies,
            held_out_count,
        ):
            test_mask = tapwater_split_df["study_group"].isin(
                held_out_studies
            )
            train_part = tapwater_split_df.loc[~test_mask]
            test_part = tapwater_split_df.loc[test_mask]
            if train_part.empty or test_part.empty:
                continue

            split_score = score_split(
                train_part,
                test_part,
                tapwater_split_df,
                risk_labels,
                full_distribution,
            )
            candidate_rows.append(
                {
                    "Method": "Exhaustive search",
                    "Candidate": (
                        f"Candidate {len(candidate_rows) + 1}"
                    ),
                    "held_out_studies": held_out_studies,
                    "Held-out studies": ", ".join(held_out_studies),
                    **split_score,
                }
            )

    split_candidates_df = pd.DataFrame(candidate_rows).sort_values(
        [
            "missing_class_penalty",
            "selection_score",
            "Held-out studies",
        ]
    )
    selected_candidate = split_candidates_df.iloc[0]
    selected_test_studies = list(
        selected_candidate["held_out_studies"]
    )

    # Benchmark the custom search against sklearn's built-in grouped and
    # stratified splitter using the exact same scoring function.
    grouped_fold_count = min(5, len(all_studies))
    if grouped_fold_count < 2:
        raise ValueError(
            "At least two study groups are required for grouped splitting."
        )

    grouped_cv = StratifiedGroupKFold(
        n_splits=grouped_fold_count,
        shuffle=True,
        random_state=42,
    )
    sklearn_fold_rows = []
    for fold_num, (train_idx, test_idx) in enumerate(
        grouped_cv.split(
            tapwater_split_df,
            tapwater_split_df["pfas_risk_tier"],
            groups=tapwater_split_df["study_group"],
        ),
        start=1,
    ):
        train_part = tapwater_split_df.iloc[train_idx]
        test_part = tapwater_split_df.iloc[test_idx]
        held_out_studies = tuple(
            sorted(test_part["study_group"].unique().tolist())
        )
        split_score = score_split(
            train_part,
            test_part,
            tapwater_split_df,
            risk_labels,
            full_distribution,
        )
        sklearn_fold_rows.append(
            {
                "Method": "StratifiedGroupKFold",
                "Candidate": f"Fold {fold_num}",
                "held_out_studies": held_out_studies,
                "Held-out studies": ", ".join(held_out_studies),
                **split_score,
            }
        )

    sklearn_fold_scores_df = pd.DataFrame(
        sklearn_fold_rows
    ).sort_values(
        [
            "missing_class_penalty",
            "selection_score",
            "Held-out studies",
        ]
    )

    split_comparison_df = pd.concat(
        [
            split_candidates_df,
            sklearn_fold_scores_df,
        ],
        ignore_index=True,
    ).sort_values(
        [
            "missing_class_penalty",
            "selection_score",
            "Method",
            "Held-out studies",
        ]
    )

    best_sklearn_candidate = sklearn_fold_scores_df.iloc[0]
    exhaustive_penalty = int(
        selected_candidate["missing_class_penalty"]
    )
    sklearn_penalty = int(
        best_sklearn_candidate["missing_class_penalty"]
    )
    exhaustive_score = float(selected_candidate["selection_score"])
    sklearn_score = float(
        best_sklearn_candidate["selection_score"]
    )

    if (
        exhaustive_penalty < sklearn_penalty
        or (
            exhaustive_penalty == sklearn_penalty
            and exhaustive_score < sklearn_score - 1e-12
        )
    ):
        comparison_result = (
            "The exhaustive winner strictly outperforms every "
            "StratifiedGroupKFold fold under the shared rubric."
        )
    elif (
        exhaustive_penalty == sklearn_penalty
        and abs(exhaustive_score - sklearn_score) <= 1e-12
    ):
        comparison_result = (
            "The exhaustive winner ties the best "
            "StratifiedGroupKFold fold under the shared rubric."
        )
    else:
        comparison_result = (
            "A StratifiedGroupKFold fold outperforms the exhaustive "
            "winner under the shared rubric; the selection logic "
            "should be reviewed."
        )

    method_best_summary = pd.DataFrame(
        [
            {
                "Method": "Exhaustive search",
                "Candidate": selected_candidate["Candidate"],
                "Held-out studies": (
                    selected_candidate["Held-out studies"]
                ),
                "Missing-tier penalty": exhaustive_penalty,
                "Test fraction": float(
                    selected_candidate["test_fraction"]
                ),
                "Distribution gap": float(
                    selected_candidate["distribution_gap"]
                ),
                "Selection score": exhaustive_score,
            },
            {
                "Method": "StratifiedGroupKFold",
                "Candidate": best_sklearn_candidate["Candidate"],
                "Held-out studies": (
                    best_sklearn_candidate["Held-out studies"]
                ),
                "Missing-tier penalty": sklearn_penalty,
                "Test fraction": float(
                    best_sklearn_candidate["test_fraction"]
                ),
                "Distribution gap": float(
                    best_sklearn_candidate["distribution_gap"]
                ),
                "Selection score": sklearn_score,
            },
        ]
    )

    comparison_columns = [
        "Method",
        "Candidate",
        "Held-out studies",
        "test_fraction",
        "missing_class_penalty",
        "distribution_gap",
        "selection_score",
    ]
    split_comparison_preview = split_comparison_df[
        comparison_columns
    ].head(20)

    selected_test_mask = tapwater_split_df["study_group"].isin(
        selected_test_studies
    )
    tapwater_train_df = tapwater_split_df.loc[
        ~selected_test_mask
    ].copy()
    tapwater_test_df = tapwater_split_df.loc[
        selected_test_mask
    ].copy()

    train_studies = sorted(
        tapwater_train_df["study_group"].unique().tolist()
    )
    test_studies = sorted(
        tapwater_test_df["study_group"].unique().tolist()
    )
    study_overlap = sorted(
        set(train_studies).intersection(test_studies)
    )
    site_overlap = sorted(
        set(tapwater_train_df["Site Code"]).intersection(
            tapwater_test_df["Site Code"]
        )
    )

    partition_summary = pd.DataFrame(
        [
            {
                "Partition": "Training",
                "Sites": len(tapwater_train_df),
                "Study groups": len(train_studies),
                "Studies": ", ".join(train_studies),
            },
            {
                "Partition": "Test",
                "Sites": len(tapwater_test_df),
                "Study groups": len(test_studies),
                "Studies": ", ".join(test_studies),
            },
        ]
    )

    partition_class_summary = (
        pd.concat(
            [
                tapwater_train_df.assign(Partition="Training"),
                tapwater_test_df.assign(Partition="Test"),
            ]
        )
        .groupby(
            ["Partition", "pfas_risk_tier"],
            observed=False,
        )
        .size()
        .unstack(fill_value=0)
        .reindex(columns=risk_labels, fill_value=0)
        .reset_index()
    )

    leakage_summary = pd.DataFrame(
        [
            {
                "Validation check": (
                    "Study groups appearing in both partitions"
                ),
                "Result": len(study_overlap),
                "Assessment": (
                    "Pass" if not study_overlap else "Review"
                ),
            },
            {
                "Validation check": (
                    "Site identifiers appearing in both partitions"
                ),
                "Result": len(site_overlap),
                "Assessment": (
                    "Pass" if not site_overlap else "Review"
                ),
            },
            {
                "Validation check": (
                    "Risk tiers missing from either partition"
                ),
                "Result": exhaustive_penalty,
                "Assessment": (
                    "Pass"
                    if exhaustive_penalty == 0
                    else (
                        "Review; grouped data could not preserve "
                        "every tier"
                    )
                ),
            },
        ]
    )

    mo.vstack(
        [
            mo.md("### Split strategy - group by study"),
            task_callout(
                "3.3",
                category="Step 3 - Evaluation Plan",
                lead="Raj",
                summary=(
                    "Use the completed `ss_scored_df` target to "
                    "create a study-grouped train/test split for the "
                    "tap-water model. All sites from a contributing "
                    "study remain together, preventing study-design "
                    "and geographic leakage. Benchmark the custom "
                    "exhaustive search against "
                    "`StratifiedGroupKFold` using the same rubric."
                ),
            ),
            mo.md(
                f"""
                #### Target and grouping definition

                Checkpoint 1 supplies `ss_scored_df`, including the
                completed `sum_tq_epa` value. That continuous score is
                mapped to the three project classes:

                * `within_reduced_monitoring`:
                  `sum_tq_epa < {WITHIN_MONITORING_CUTOFF:.1f}`
                * `above_trigger`:
                  `{WITHIN_MONITORING_CUTOFF:.1f} <= sum_tq_epa < `
                  `{MCL_EXCEEDANCE_CUTOFF:.1f}`
                * `mcl_exceedance`:
                  `sum_tq_epa >= {MCL_EXCEEDANCE_CUTOFF:.1f}`

                `{study_group_column}` is the canonical grouping field
                because Smalling provides the measured PFAS outcome.
                The corresponding Seawolf landscape row describes the
                same site and follows it into the same partition.
                """
            ),
            mo.md("#### Current tap-water risk tiers by study"),
            mo.ui.table(study_risk_profile),
            mo.md(
                """
                #### Holdout-selection rules

                Candidate holdouts are complete study groups, not
                individual rows. Every candidate is scored using:

                1. Missing risk tiers in training or test data.
                2. Distance from the target 20% test fraction.
                3. Difference between test and full class shares.

                The missing-tier penalty receives a weight of 10, so
                preserving every class is prioritized before test size
                and distribution similarity.
                """
            ),
            mo.md("#### Exhaustive versus sklearn comparison"),
            mo.ui.table(method_best_summary),
            mo.md(comparison_result),
            mo.md(
                """
                The table below shows the 20 highest-ranked candidates
                from the combined comparison. The complete comparison
                remains available as `split_comparison_df`.
                """
            ),
            mo.ui.table(split_comparison_preview),
            mo.md("#### Selected partition"),
            mo.ui.table(partition_summary),
            mo.md("#### Risk-tier counts by partition"),
            mo.ui.table(partition_class_summary),
            mo.md("#### Leakage validation"),
            mo.ui.table(leakage_summary),
            mo.md(
                r"""
                #### Model optimization inside the training partition

                Hyperparameter selection will use grouped
                cross-validation only within `tapwater_train_df`.
                `StratifiedGroupKFold` attempts to preserve the
                risk-tier distribution while keeping each study intact:

                ```python
                from sklearn.model_selection import StratifiedGroupKFold

                grouped_cv = StratifiedGroupKFold(
                    n_splits=min(
                        5,
                        tapwater_train_df["study_group"].nunique(),
                    ),
                    shuffle=True,
                    random_state=42,
                )

                for fit_idx, validation_idx in grouped_cv.split(
                    X_train,
                    y_train,
                    groups=tapwater_train_df["study_group"],
                ):
                    ...
                ```

                Study labels, site identifiers, PFAS concentrations,
                `sum_tq_epa`, and `pfas_risk_tier` are not model
                predictors. All preprocessing must be fitted inside
                each training fold through one pipeline.

                #### McMahon treatment

                `mc_scored_df` remains outside this tap-water split.
                McMahon represents groundwater, omits GenX, and uses a
                different non-detect convention. Task 3.4 will decide
                whether it supports a separate groundwater model or a
                qualified external evaluation slice.
                """
            ),
        ]
    )
    return (
        split_comparison_df,
        tapwater_split_df,
        tapwater_test_df,
        tapwater_train_df,
    )


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

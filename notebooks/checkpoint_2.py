# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
#     "pandas>=3.0.3",
# ]
# ///

import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    from itertools import combinations

    import marimo as mo
    import pandas as pd

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
    return checkpoint_1_app, combinations, mo, pd


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
def _(combinations, mo, pd, ss_scored_df):
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

    tapwater_split_df = ss_scored_df.copy()
    tapwater_split_df["pfas_risk_tier"] = pd.cut(
        tapwater_split_df["sum_tq_epa"],
        bins=[float("-inf"), 0.5, 1.0, float("inf")],
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
    # before selecting a holdout. This is necessary because whole-study splits
    # cannot guarantee exact row-level stratification.
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

    all_studies = sorted(tapwater_split_df["study_group"].unique().tolist())
    full_distribution = (
        tapwater_split_df["pfas_risk_tier"]
        .value_counts(normalize=True)
        .reindex(risk_labels, fill_value=0.0)
    )

    candidate_rows = []
    for held_out_count in range(1, len(all_studies)):
        for held_out_studies in combinations(all_studies, held_out_count):
            test_mask = tapwater_split_df["study_group"].isin(
                held_out_studies
            )
            train_part = tapwater_split_df.loc[~test_mask]
            test_part = tapwater_split_df.loc[test_mask]
            if train_part.empty or test_part.empty:
                continue

            train_classes = set(train_part["pfas_risk_tier"].dropna())
            test_classes = set(test_part["pfas_risk_tier"].dropna())
            missing_class_penalty = (
                len(set(risk_labels) - train_classes)
                + len(set(risk_labels) - test_classes)
            )

            test_fraction = len(test_part) / len(tapwater_split_df)
            test_distribution = (
                test_part["pfas_risk_tier"]
                .value_counts(normalize=True)
                .reindex(risk_labels, fill_value=0.0)
            )
            distribution_gap = float(
                (test_distribution - full_distribution).abs().sum()
            )

            # Prefer a roughly 20% test set, preserve every class in both
            # partitions, and then choose the closest class distribution.
            selection_score = (
                missing_class_penalty * 10
                + abs(test_fraction - 0.20)
                + distribution_gap
            )
            candidate_rows.append(
                {
                    "held_out_studies": held_out_studies,
                    "test_fraction": test_fraction,
                    "missing_class_penalty": missing_class_penalty,
                    "distribution_gap": distribution_gap,
                    "selection_score": selection_score,
                }
            )

    split_candidates_df = pd.DataFrame(candidate_rows).sort_values(
        [
            "missing_class_penalty",
            "selection_score",
            "held_out_studies",
        ]
    )
    selected_candidate = split_candidates_df.iloc[0]
    selected_test_studies = list(selected_candidate["held_out_studies"])

    selected_test_mask = tapwater_split_df["study_group"].isin(
        selected_test_studies
    )
    tapwater_train_df = tapwater_split_df.loc[~selected_test_mask].copy()
    tapwater_test_df = tapwater_split_df.loc[selected_test_mask].copy()

    train_studies = sorted(tapwater_train_df["study_group"].unique().tolist())
    test_studies = sorted(tapwater_test_df["study_group"].unique().tolist())
    study_overlap = sorted(set(train_studies).intersection(test_studies))
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
        .groupby(["Partition", "pfas_risk_tier"], observed=False)
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
                "Assessment": "Pass" if not study_overlap else "Review",
            },
            {
                "Validation check": (
                    "Site identifiers appearing in both partitions"
                ),
                "Result": len(site_overlap),
                "Assessment": "Pass" if not site_overlap else "Review",
            },
            {
                "Validation check": "Risk tiers missing from either partition",
                "Result": int(selected_candidate["missing_class_penalty"]),
                "Assessment": (
                    "Pass"
                    if selected_candidate["missing_class_penalty"] == 0
                    else "Review; grouped data could not preserve every tier"
                ),
            },
        ]
    )

    mo.vstack(
        [
            mo.md(
                """
                ### Split strategy - group by study

                The train/test split for the tap-water model groups by
                study rather than shuffling individual rows, using the
                completed `ss_scored_df` target. All sites from a
                contributing study remain together, preventing
                study-design and geographic leakage into evaluation.
                McMahon is provisionally kept outside this split
                pending Task 3.4 because its groundwater target is not
                directly comparable to Smalling/Seawolf.
                """
            ),
            mo.md(
                f"""
                #### Target and grouping definition

                Checkpoint 1 now supplies `ss_scored_df`, including the
                completed
                `sum_tq_epa` value. For evaluation, that continuous
                score is mapped to
                the three project classes:

                * `within_reduced_monitoring`: `sum_tq_epa < 0.5`
                * `above_trigger`: `0.5 <= sum_tq_epa < 1.0`
                * `mcl_exceedance`: `sum_tq_epa >= 1.0`

                `{study_group_column}` is used as the canonical
                grouping field because
                Smalling provides the measured PFAS outcome. The
                corresponding Seawolf
                landscape record describes the same site and
                therefore follows it into
                the same partition. Smalling and Seawolf are not
                treated as separate
                train/test datasets.
                """
            ),
            mo.md("#### Current tap-water risk tiers by study"),
            mo.ui.table(study_risk_profile),
            mo.md(
                """
                #### Holdout-selection rules

                Candidate holdouts are created from complete study
                groups rather than
                individual rows. The selected split prioritizes, in order:

                1. All three PFAS risk tiers occurring in both
                   training and test data.
                2. A test partition close to 20% of eligible tap-water sites.
                3. A test-set class distribution close to the full dataset.
                4. Zero overlap in study labels and site identifiers.

                This produces a deterministic study-level holdout
                from the current
                data. The test studies must remain untouched during
                scaling, encoding,
                feature selection, and hyperparameter tuning.
                """
            ),
            mo.ui.table(partition_summary),
            mo.md("#### Risk-tier counts by partition"),
            mo.ui.table(partition_class_summary),
            mo.md("#### Leakage validation"),
            mo.ui.table(leakage_summary),
            mo.md(
                r"""
                #### Model optimization inside the training partition

                Hyperparameter selection will use grouped
                cross-validation only within
                `tapwater_train_df`. `StratifiedGroupKFold` is
                appropriate because it
                attempts to preserve the risk-tier distribution
                while still keeping
                every study intact:

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
                `sum_tq_epa`, and `pfas_risk_tier` are grouping,
                identification,
                or outcome fields—not model predictors. All
                preprocessing must be
                fitted inside each training fold through one pipeline.

                #### McMahon treatment

                `mc_scored_df` is provisionally excluded from this
                tap-water split.
                McMahon contains groundwater observations, omits
                GenX, and applies a
                different non-detect convention. Under the current
                construction its
                target distribution is therefore not on the same footing as
                Smalling/Seawolf. Task 3.4 will decide whether it
                should support a
                separate groundwater model or serve as a qualified external
                evaluation slice.
                """
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

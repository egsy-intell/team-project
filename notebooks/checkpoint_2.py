# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
#     "pandas>=3.0.3",
#     "scikit-learn",
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
def _():
    RISK_LABELS = [
        "within_reduced_monitoring",
        "above_trigger",
        "mcl_exceedance",
    ]
    return (RISK_LABELS,)


@app.cell(hide_code=True)
def _():
    RISK_TIER_BINS = [float("-inf"), 0.5, 1.0, float("inf")]
    return (RISK_TIER_BINS,)


@app.cell(hide_code=True)
def _(RISK_LABELS, RISK_TIER_BINS, pd):
    def classify_pfas_risk_tier(sum_tq_epa):
        return pd.cut(
            sum_tq_epa,
            bins=RISK_TIER_BINS,
            labels=RISK_LABELS,
            right=False,
            ordered=True,
        )

    return (classify_pfas_risk_tier,)


@app.cell(hide_code=True)
def _(
    RISK_LABELS,
    classify_pfas_risk_tier,
    combinations,
    mo,
    pd,
    ss_scored_df,
):
    from sklearn.model_selection import StratifiedGroupKFold

    # Smalling provides the measured outcome, so Study_smalling is the
    # canonical grouping field. The matched Seawolf predictor row follows the
    # same site into whichever partition that Smalling study is assigned to.
    _study_group_column = (
        "Study_smalling"
        if "Study_smalling" in ss_scored_df.columns
        else "Study_seawolf"
    )

    _tapwater_split_df = ss_scored_df.copy()
    _tapwater_split_df["pfas_risk_tier"] = classify_pfas_risk_tier(
        _tapwater_split_df["sum_tq_epa"]
    )
    _tapwater_split_df["study_group"] = (
        _tapwater_split_df[_study_group_column].astype("string").str.strip()
    )
    _tapwater_split_df = _tapwater_split_df.dropna(
        subset=["Site Code", "study_group", "pfas_risk_tier"]
    ).copy()

    # Review the number of sites and target classes available in each study
    # before selecting a holdout. Whole-study splits cannot guarantee exact
    # row-level stratification.
    _study_risk_profile = (
        _tapwater_split_df.groupby(
            ["study_group", "pfas_risk_tier"],
            observed=False,
        )
        .size()
        .unstack(fill_value=0)
        .reindex(columns=RISK_LABELS, fill_value=0)
        .reset_index()
    )
    _study_risk_profile["Sites"] = _study_risk_profile[RISK_LABELS].sum(axis=1)
    _study_risk_profile = _study_risk_profile[
        ["study_group", "Sites", *RISK_LABELS]
    ].sort_values(["Sites", "study_group"], ascending=[False, True])

    _all_studies = sorted(_tapwater_split_df["study_group"].unique().tolist())
    _full_distribution = (
        _tapwater_split_df["pfas_risk_tier"]
        .value_counts(normalize=True)
        .reindex(RISK_LABELS, fill_value=0.0)
    )

    def _score_split(
        train_part,
        test_part,
        full_data,
        labels,
        overall_distribution,
    ):
        train_classes = set(train_part["pfas_risk_tier"].dropna())
        test_classes = set(test_part["pfas_risk_tier"].dropna())
        missing_class_penalty = len(set(labels) - train_classes) + len(
            set(labels) - test_classes
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

    _candidate_rows = []
    for _held_out_count in range(1, len(_all_studies)):
        for _held_out_studies in combinations(_all_studies, _held_out_count):
            _test_mask = _tapwater_split_df["study_group"].isin(
                _held_out_studies
            )
            _train_part = _tapwater_split_df.loc[~_test_mask]
            _test_part = _tapwater_split_df.loc[_test_mask]
            if _train_part.empty or _test_part.empty:
                continue

            _split_score = _score_split(
                _train_part,
                _test_part,
                _tapwater_split_df,
                RISK_LABELS,
                _full_distribution,
            )
            _candidate_rows.append(
                {
                    "Method": "Exhaustive search",
                    "Candidate": f"Candidate {len(_candidate_rows) + 1}",
                    "held_out_studies": _held_out_studies,
                    "Held-out studies": ", ".join(_held_out_studies),
                    **_split_score,
                }
            )

    _split_candidates_df = pd.DataFrame(_candidate_rows).sort_values(
        [
            "missing_class_penalty",
            "selection_score",
            "Held-out studies",
        ]
    )
    _selected_candidate = _split_candidates_df.iloc[0]
    _selected_test_studies = list(_selected_candidate["held_out_studies"])

    # Benchmark the custom search against sklearn's built-in grouped and
    # stratified splitter using the exact same scoring function.
    _grouped_fold_count = min(5, len(_all_studies))
    if _grouped_fold_count < 2:
        raise ValueError(
            "At least two study groups are required for grouped splitting."
        )

    _grouped_cv = StratifiedGroupKFold(
        n_splits=_grouped_fold_count,
        shuffle=True,
        random_state=42,
    )
    _sklearn_fold_rows = []
    for _fold_num, (_train_idx, _test_idx) in enumerate(
        _grouped_cv.split(
            _tapwater_split_df,
            _tapwater_split_df["pfas_risk_tier"],
            groups=_tapwater_split_df["study_group"],
        ),
        start=1,
    ):
        _train_part = _tapwater_split_df.iloc[_train_idx]
        _test_part = _tapwater_split_df.iloc[_test_idx]
        _held_out_studies = tuple(
            sorted(_test_part["study_group"].unique().tolist())
        )
        _split_score = _score_split(
            _train_part,
            _test_part,
            _tapwater_split_df,
            RISK_LABELS,
            _full_distribution,
        )
        _sklearn_fold_rows.append(
            {
                "Method": "StratifiedGroupKFold",
                "Candidate": f"Fold {_fold_num}",
                "held_out_studies": _held_out_studies,
                "Held-out studies": ", ".join(_held_out_studies),
                **_split_score,
            }
        )

    _sklearn_fold_scores_df = pd.DataFrame(_sklearn_fold_rows).sort_values(
        [
            "missing_class_penalty",
            "selection_score",
            "Held-out studies",
        ]
    )

    _split_comparison_df = pd.concat(
        [_split_candidates_df, _sklearn_fold_scores_df],
        ignore_index=True,
    ).sort_values(
        [
            "missing_class_penalty",
            "selection_score",
            "Method",
            "Held-out studies",
        ]
    )

    _best_sklearn_candidate = _sklearn_fold_scores_df.iloc[0]
    _exhaustive_penalty = int(_selected_candidate["missing_class_penalty"])
    _sklearn_penalty = int(_best_sklearn_candidate["missing_class_penalty"])
    _exhaustive_score = float(_selected_candidate["selection_score"])
    _sklearn_score = float(_best_sklearn_candidate["selection_score"])

    _penalty_diff = _exhaustive_penalty - _sklearn_penalty
    _score_diff = _exhaustive_score - _sklearn_score
    if _penalty_diff < 0 or (_penalty_diff == 0 and _score_diff < -1e-12):
        _comparison_outcome = "better"
    elif _penalty_diff == 0 and abs(_score_diff) <= 1e-12:
        _comparison_outcome = "tie"
    else:
        _comparison_outcome = "worse"

    _comparison_result = {
        "better": (
            "The exhaustive winner strictly outperforms every "
            "StratifiedGroupKFold fold under the shared rubric."
        ),
        "tie": (
            "The exhaustive winner ties the best StratifiedGroupKFold "
            "fold under the shared rubric."
        ),
        "worse": (
            "A StratifiedGroupKFold fold outperforms the exhaustive "
            "winner under the shared rubric; the selection logic "
            "should be reviewed."
        ),
    }[_comparison_outcome]

    _method_best_summary = pd.DataFrame(
        [
            {
                "Method": "Exhaustive search",
                "Candidate": _selected_candidate["Candidate"],
                "Held-out studies": _selected_candidate["Held-out studies"],
                "Missing-tier penalty": _exhaustive_penalty,
                "Test fraction": float(_selected_candidate["test_fraction"]),
                "Distribution gap": float(
                    _selected_candidate["distribution_gap"]
                ),
                "Selection score": _exhaustive_score,
            },
            {
                "Method": "StratifiedGroupKFold",
                "Candidate": _best_sklearn_candidate["Candidate"],
                "Held-out studies": (
                    _best_sklearn_candidate["Held-out studies"]
                ),
                "Missing-tier penalty": _sklearn_penalty,
                "Test fraction": float(
                    _best_sklearn_candidate["test_fraction"]
                ),
                "Distribution gap": float(
                    _best_sklearn_candidate["distribution_gap"]
                ),
                "Selection score": _sklearn_score,
            },
        ]
    )

    _comparison_columns = [
        "Method",
        "Candidate",
        "Held-out studies",
        "test_fraction",
        "missing_class_penalty",
        "distribution_gap",
        "selection_score",
    ]
    _split_comparison_preview = _split_comparison_df[_comparison_columns].head(
        20
    )

    _selected_test_mask = _tapwater_split_df["study_group"].isin(
        _selected_test_studies
    )
    _tapwater_train_df = _tapwater_split_df.loc[~_selected_test_mask].copy()
    _tapwater_test_df = _tapwater_split_df.loc[_selected_test_mask].copy()

    _train_studies = sorted(
        _tapwater_train_df["study_group"].unique().tolist()
    )
    _test_studies = sorted(_tapwater_test_df["study_group"].unique().tolist())
    _study_overlap = sorted(set(_train_studies).intersection(_test_studies))
    _site_overlap = sorted(
        set(_tapwater_train_df["Site Code"]).intersection(
            _tapwater_test_df["Site Code"]
        )
    )

    _partition_summary = pd.DataFrame(
        [
            {
                "Partition": "Training",
                "Sites": len(_tapwater_train_df),
                "Study groups": len(_train_studies),
                "Studies": ", ".join(_train_studies),
            },
            {
                "Partition": "Test",
                "Sites": len(_tapwater_test_df),
                "Study groups": len(_test_studies),
                "Studies": ", ".join(_test_studies),
            },
        ]
    )

    _partition_class_summary = (
        pd.concat(
            [
                _tapwater_train_df.assign(Partition="Training"),
                _tapwater_test_df.assign(Partition="Test"),
            ]
        )
        .groupby(["Partition", "pfas_risk_tier"], observed=False)
        .size()
        .unstack(fill_value=0)
        .reindex(columns=RISK_LABELS, fill_value=0)
        .reset_index()
    )

    _leakage_summary = pd.DataFrame(
        [
            {
                "Validation check": (
                    "Study groups appearing in both partitions"
                ),
                "Result": len(_study_overlap),
                "Assessment": "Pass" if not _study_overlap else "Review",
            },
            {
                "Validation check": (
                    "Site identifiers appearing in both partitions"
                ),
                "Result": len(_site_overlap),
                "Assessment": "Pass" if not _site_overlap else "Review",
            },
            {
                "Validation check": "Risk tiers missing from either partition",
                "Result": _exhaustive_penalty,
                "Assessment": (
                    "Pass"
                    if _exhaustive_penalty == 0
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

                A study-grouped train/test split for the tap-water
                model uses the completed `ss_scored_df` target: all
                sites from a contributing study remain together,
                preventing study-design and geographic leakage. The
                custom exhaustive search below is benchmarked against
                `StratifiedGroupKFold` using the same rubric. McMahon
                is provisionally kept outside this split because its
                groundwater target is not directly comparable to
                Smalling/Seawolf, as the next section covers in more
                detail.
                """
            ),
            mo.md(
                f"""
                #### Target and grouping definition

                Checkpoint 1 supplies `ss_scored_df`, including the
                completed `sum_tq_epa` value. That continuous score is
                mapped to the three project classes via the shared
                `classify_pfas_risk_tier()` helper:

                * `within_reduced_monitoring`: `sum_tq_epa < 0.5`
                * `above_trigger`: `0.5 <= sum_tq_epa < 1.0`
                * `mcl_exceedance`: `sum_tq_epa >= 1.0`

                `{_study_group_column}` is the canonical grouping field
                because Smalling provides the measured PFAS outcome.
                The corresponding Seawolf landscape row describes the
                same site and follows it into the same partition.
                """
            ),
            mo.md("#### Current tap-water risk tiers by study"),
            mo.ui.table(_study_risk_profile),
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
            mo.ui.table(_method_best_summary),
            mo.md(_comparison_result),
            mo.md(
                """
                The table below shows the 20 highest-ranked candidates
                from the combined comparison.
                """
            ),
            mo.ui.table(_split_comparison_preview),
            mo.md("#### Selected partition"),
            mo.ui.table(_partition_summary),
            mo.md("#### Risk-tier counts by partition"),
            mo.ui.table(_partition_class_summary),
            mo.md("#### Leakage validation"),
            mo.ui.table(_leakage_summary),
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
                `sum_tq_epa`, and `pfas_risk_tier` are grouping,
                identification, or outcome fields — not model
                predictors. All preprocessing must be fitted inside
                each training fold through one pipeline.

                #### McMahon treatment

                `mc_scored_df` is provisionally excluded from this
                tap-water split. McMahon contains groundwater
                observations, omits GenX, and applies a different
                non-detect convention. Under the current construction
                its target distribution is therefore not on the same
                footing as Smalling/Seawolf. Whether it should support
                a separate groundwater model or serve as a qualified
                external evaluation slice is taken up next.
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
            mo.md(
                """
                **Draft proposal below, pending Yai/Raj sign-off** —
                left as a draft rather than a final decision since this
                task is co-owned and Raj hasn't weighed in yet.
                """
            ),
        ]
    )
    return


@app.cell
def _(RISK_LABELS, classify_pfas_risk_tier, mc_scored_df, pd, ss_scored_df):
    def _tier_distribution(scored_df):
        tiers = classify_pfas_risk_tier(scored_df["sum_tq_epa"])
        return tiers.value_counts(normalize=True).reindex(
            RISK_LABELS, fill_value=0.0
        )

    groundwater_comparison_df = pd.DataFrame(
        [
            {
                "Study": "Smalling/Seawolf (tap water)",
                "Sites": len(ss_scored_df),
                "Compounds summed": 6,
                "Non-detect convention": "0",
                "sum_tq_epa median": ss_scored_df["sum_tq_epa"].median(),
                **_tier_distribution(ss_scored_df).round(3).to_dict(),
            },
            {
                "Study": "McMahon (groundwater)",
                "Sites": len(mc_scored_df),
                "Compounds summed": 5,
                "Non-detect convention": "½ reporting limit",
                "sum_tq_epa median": mc_scored_df["sum_tq_epa"].median(),
                **_tier_distribution(mc_scored_df).round(3).to_dict(),
            },
        ]
    )
    return (groundwater_comparison_df,)


@app.cell(hide_code=True)
def _(groundwater_comparison_df, mo):
    mo.vstack(
        [
            mo.md(
                """
                #### Structural comparison

                McMahon's ∑TQ isn't on the same footing as
                Smalling/Seawolf's, for two compounding reasons: it sums
                5 of the 6 regulated compounds instead of 6 (no GenX
                column at all), and its non-detects are imputed as half
                the reporting limit instead of 0. That second difference
                dominates — it gives every McMahon site a non-zero
                baseline TQ, so `sum_tq_epa` never drops below ~1.0
                regardless of actual site conditions. McMahon's risk-tier
                column below is degenerate: 100% `mcl_exceedance` by
                construction, not by geology.
                """
            ),
            mo.ui.table(groundwater_comparison_df),
            mo.md(
                """
                #### Proposed decision: hold out, don't combine

                Combining McMahon into the Smalling/Seawolf training set
                would let a model achieve perfect recall on the
                `mcl_exceedance` tier simply by learning "is this a
                McMahon row," an artifact of imputation and compound
                coverage, not a land-use signal — exactly the kind of
                leakage the study-grouped split in 3.3 already guards
                against for cross-study effects. A single-class study
                also cannot exercise the per-class metrics defined in
                3.1, which need all three tiers represented.

                Proposed treatment instead: keep `mc_scored_df` fully
                outside both the training and 3.3 test partitions, and
                report model predictions on it separately as a
                qualified generalization check — framed explicitly as
                "does the model's *relative* ranking of McMahon sites
                look plausible," not as a comparable accuracy number,
                since the target itself isn't comparable across studies.
                Revisit combining groundwater and tap-water data only if
                a future checkpoint re-derives McMahon's ∑TQ with a
                matched non-detect convention and a GenX estimate.
                """
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
    non-linear ensemble (Step 4), against the already-computed ∑TQ
    target from checkpoint 1. Training both models and evaluating them
    against the plan above is Step 5 work for the final checkpoint.
    """)
    return


if __name__ == "__main__":
    app.run()

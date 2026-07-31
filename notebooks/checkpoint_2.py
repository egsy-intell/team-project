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
def _():
    # Shared third-party imports for this notebook, defined once so
    # downstream cells take them as parameters instead of each
    # re-importing pandas/sklearn locally.
    from itertools import combinations

    import numpy as np
    import pandas as pd
    from sklearn.compose import ColumnTransformer
    from sklearn.metrics import (
        classification_report,
        confusion_matrix,
        f1_score,
        recall_score,
    )
    from sklearn.model_selection import StratifiedGroupKFold
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    return (
        ColumnTransformer,
        OneHotEncoder,
        StandardScaler,
        StratifiedGroupKFold,
        classification_report,
        combinations,
        confusion_matrix,
        f1_score,
        np,
        pd,
        recall_score,
    )


@app.cell(hide_code=True)
def _(mc_clean_df, mc_scored_df, mo, ss_scored_df):
    mo.md(f"""
    # Step 3-4: Model Selection, Training & Evaluation Design

    This section is Check-In #2's deliverable: a formal evaluation plan
    (Step 3) and a set of proposed modeling techniques (Step 4), per
    `specs/checkpoint-2/GRAD 50400 - Project Checkpoint-2.pdf`. It's a
    **design/proposal document** — each section below states what a task
    lead will argue and how, not yet an executed evaluation. Execution and
    retuning (Step 5, task `EVAL`) is out of scope here and belongs to the
    project's final write-up and presentation.

    Every section carries a callout naming its task ID, category, lead, and
    dependencies, tied to `planning/checkpoint-2/checkpoint2_tasks.csv`; use
    the task ID to cross-reference the task board.

    Inherited from the Step 2 cleaning and ∑TQ construction sections above:
    `ss_scored_df` ({ss_scored_df.shape[0]} rows), `mc_scored_df`
    ({mc_scored_df.shape[0]} rows). `mc_clean_df` ({mc_clean_df.shape[0]}
    rows) is also available unscored — McMahon is held out of training
    entirely and used only as a qualified validation slice, per the
    groundwater-role decision below.
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
def _(mo, tier_distribution):
    mo.md(rf"""
    ### Per-class metrics and evaluation rationale

    **Target:** the ∑TQ risk tier — `within_reduced_monitoring`
    (∑TQ < 0.5), `above_trigger` (0.5 ≤ ∑TQ < 1.0), `mcl_exceedance`
    (∑TQ ≥ 1.0).

    #### Why plain accuracy is the wrong headline metric

    **Class imbalance.** The ∑TQ construction's `ss_scored_df` (236
    Smalling/Seawolf sites) splits
    {tier_distribution["within_reduced_monitoring"]:.1%}
    `within_reduced_monitoring`,
    {tier_distribution["above_trigger"]:.1%} `above_trigger`, and
    {tier_distribution["mcl_exceedance"]:.1%} `mcl_exceedance`: a
    classifier that predicts the majority tier for every site scores
    well above chance on accuracy while flagging no contaminated
    source at all.

    **Asymmetric error costs.** Accuracy weights every misclassification
    the same; this problem does not:

    * *False negative on `mcl_exceedance`* — an MCL-equivalent site
      predicted into a lower tier. A site that needs monitoring never
      reaches the operator's priority list, which is the failure the
      screening tool exists to prevent.
    * *False positive on `mcl_exceedance`* — a compliant site flagged
      for follow-up. Costs a confirmatory sample and a field visit.
      Recoverable, and consistent with the tool's stated role as
      sampling prioritization rather than a compliance determination.

    #### Metric framework

    * **Per-class precision, recall, and F1** reported for all three
      tiers separately, never collapsed into a single accuracy figure.
    * **Recall on `mcl_exceedance`** as the constraint. Model selection
      requires clearing a minimum recall floor of 0.70 on the
      highest-risk tier, set against the actual `ss_scored_df` tier
      distribution below.
    * **Macro-averaged F1** as the scalar comparison metric *subject
      to* that floor, so Model A and Model B (Tasks 4.1, 4.3) are
      ranked on one number without letting the majority tier dominate
      the score. Macro-averaging is chosen over weighted averaging
      precisely because the minority tier is the one that matters.
    * **3×3 confusion matrix** (actual × predicted). The tiers are
      ordinal, so the direction of error carries meaning that a scalar
      metric discards: a true `mcl_exceedance` site predicted as
      `above_trigger` still lands the operator in a follow-up posture,
      while the same site predicted as `within_reduced_monitoring`
      does not. The matrix is how we distinguish those two failures,
      and it maps directly onto the trigger-vs-MCL vocabulary
      operators already act on.

    #### Scope note

    This framework is defined per evaluation slice. The McMahon ∑TQ
    scoring found that all 254 McMahon sites carry `sum_tq_epa` ≥
    1.021 under the half-reporting-limit non-detect convention,
    placing every one of them in `mcl_exceedance` by construction.
    McMahon is held out of
    training and reported separately as a qualified validation slice
    (see the groundwater-role decision below), so the class
    proportions the recall floor is set against come from
    `ss_scored_df` alone.
    """)
    return


@app.cell(hide_code=True)
def _(pd):
    RISK_LABELS = [
        "within_reduced_monitoring",
        "above_trigger",
        "mcl_exceedance",
    ]

    _RISK_TIER_BINS = [float("-inf"), 0.5, 1.0, float("inf")]

    def classify_pfas_risk_tier(sum_tq_epa):
        return pd.cut(
            sum_tq_epa,
            bins=_RISK_TIER_BINS,
            labels=RISK_LABELS,
            right=False,
            ordered=True,
        )

    return RISK_LABELS, classify_pfas_risk_tier


@app.cell
def _(
    RISK_LABELS,
    classification_report,
    confusion_matrix,
    f1_score,
    pd,
    recall_score,
):
    def evaluate_tier_model(y_true, y_pred, model_name, recall_floor=None):
        """Standard evaluation for any ∑TQ tier classifier.

        Returns per-class precision/recall/F1, the two headline
        numbers the metric framework selects on (macro-F1 and
        mcl_exceedance recall), a labeled 3x3 confusion matrix, and a
        count of tier-skipping misses.
        """

        # zero_division=0: a model that never predicts a tier yields an
        # undefined precision. Score it 0 rather than dropping the row, or
        # the majority-tier failure mode this framework warns about
        # disappears from the report.
        report = pd.DataFrame(
            classification_report(
                y_true,
                y_pred,
                labels=RISK_LABELS,
                output_dict=True,
                zero_division=0,
            )
        ).T

        per_class = report.loc[RISK_LABELS].assign(
            support=lambda df: df["support"].astype(int)
        )

        matrix = pd.DataFrame(
            confusion_matrix(y_true, y_pred, labels=RISK_LABELS),
            index=pd.Index(RISK_LABELS, name="actual"),
            columns=pd.Index(RISK_LABELS, name="predicted"),
        )

        macro_f1 = f1_score(
            y_true,
            y_pred,
            labels=RISK_LABELS,
            average="macro",
            zero_division=0,
        )

        # Single-element labels + average="macro" isolates recall for just
        # mcl_exceedance rather than averaging across all three tiers.
        mcl_recall = recall_score(
            y_true,
            y_pred,
            labels=["mcl_exceedance"],
            average="macro",
            zero_division=0,
        )

        # The worst single error: an MCL-equivalent site predicted two tiers
        # down, which leaves the operator with no follow-up posture at all.
        critical_misses = int(
            matrix.loc["mcl_exceedance", "within_reduced_monitoring"]
        )

        summary = {
            "model": model_name,
            "macro_f1": round(macro_f1, 4),
            "mcl_exceedance_recall": round(mcl_recall, 4),
            "critical_misses": critical_misses,
            "n_evaluated": len(y_true),
        }

        if recall_floor is not None:
            summary["meets_recall_floor"] = bool(mcl_recall >= recall_floor)

        return {
            "summary": summary,
            "per_class": per_class,
            "confusion_matrix": matrix,
        }

    return (evaluate_tier_model,)


@app.cell
def _(RISK_LABELS, classify_pfas_risk_tier, evaluate_tier_model, ss_scored_df):
    tier_true = classify_pfas_risk_tier(ss_scored_df["sum_tq_epa"]).astype(str)
    tier_distribution = tier_true.value_counts(normalize=True).reindex(
        RISK_LABELS
    )

    _majority_tier = tier_distribution.idxmax()
    _majority_pred = [_majority_tier] * len(tier_true)
    _majority_result = evaluate_tier_model(
        tier_true, _majority_pred, "Majority class (zero-rule)"
    )
    majority_baseline = {
        **_majority_result["summary"],
        "mcl_exceedance_precision": round(
            _majority_result["per_class"].loc["mcl_exceedance", "precision"],
            4,
        ),
    }

    # Random-uniform prediction, independent of the input: recall_c = 1/k
    # and precision_c = prevalence_c follow directly from that
    # independence (k = number of tiers).
    _k = len(RISK_LABELS)
    _random_recall = 1 / _k
    _random_f1_by_tier = {
        _tier: 2
        * tier_distribution[_tier]
        * _random_recall
        / (tier_distribution[_tier] + _random_recall)
        for _tier in RISK_LABELS
    }
    random_baseline = {
        "macro_f1": round(sum(_random_f1_by_tier.values()) / _k, 4),
        "mcl_exceedance_recall": round(_random_recall, 4),
        "mcl_exceedance_precision": round(
            tier_distribution["mcl_exceedance"], 4
        ),
    }
    return majority_baseline, random_baseline, tier_distribution, tier_true


@app.cell(hide_code=True)
def _(majority_baseline, mo, random_baseline, tier_distribution):
    mo.md(rf"""
    ### Model success criteria and operational benchmarks

    Determining whether the land-use classification models provide
    actionable value for water-resource managers requires formal
    quantitative benchmarks, set against the three ∑TQ risk tiers
    (`within_reduced_monitoring`, `above_trigger`, `mcl_exceedance`)
    prior to model training.

    #### Baseline benchmark comparison
    Computed against `ss_scored_df`'s actual tier distribution
    ({tier_distribution["within_reduced_monitoring"]:.1%}
    `within_reduced_monitoring`,
    {tier_distribution["above_trigger"]:.1%} `above_trigger`,
    {tier_distribution["mcl_exceedance"]:.1%} `mcl_exceedance`), the
    models must significantly outperform two naive reference
    baselines:
    * **Random Uniform Classifier:** predicts each tier with equal
      1/3 probability, independent of the input. Its expected Macro
      F1-Score is $\approx {random_baseline["macro_f1"]:.2f}$ —
      recall on `mcl_exceedance` is exactly 1/3
      ({random_baseline["mcl_exceedance_recall"]:.2f}) by
      construction, but precision on `mcl_exceedance`
      ({random_baseline["mcl_exceedance_precision"]:.2f}) tracks the
      tier's actual prevalence, since a third of *all* predictions
      land on that tier regardless of correctness.
    * **Majority Class Classifier (Zero-Rule):** Always predicts
      `within_reduced_monitoring`
      ({tier_distribution["within_reduced_monitoring"]:.1%} of
      sites). Achieves
      {tier_distribution["within_reduced_monitoring"]:.1%} raw
      accuracy from class skew alone, but yields **0.0 Recall on
      `mcl_exceedance`** — it misses every high-risk site — and a low
      **Macro F1 of {majority_baseline["macro_f1"]:.2f}**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Quantitative operational thresholds
    Three core success thresholds apply when evaluating the models on
    held-out test data, each pegged to a multiple of the random-
    uniform baseline computed above rather than chosen arbitrarily:

    1. **High-Risk Class Recall ($\ge 70.0\%$):**
       * **Criterion:** $\text{Recall}_{\text{mcl\_exceedance}} \ge
         0.70$
       * **Rationale:** In environmental risk screening, Type II
         errors (missing a contaminated well) present severe public
         health hazards, so recall gets the strictest bar of the
         three — roughly 2x the random baseline's 1/3. Catching at
         least 70% of actual exceedance sites ensures the model
         serves as an effective screening tool for water operators.
    2. **Macro-Averaged F1-Score ($\ge 0.60$):**
       * **Criterion:** $\text{Macro F1} = \frac{F1_{\text{reduced}} +
         F1_{\text{trigger}} + F1_{\text{mcl}}}{3} \ge 0.60$
       * **Rationale:** Macro F1 is the overall "is it actually
         learning, not just biased toward one tier" check, so it's
         held to roughly the same ~2x-random bar as recall
         (baseline $\approx 0.32$). Weighting all classes equally
         regardless of support count means clearing 0.60 requires
         real signal across all three risk tiers, not just the
         majority class.
    3. **High-Risk Precision Floor ($\ge 45.0\%$):**
       * **Criterion:** $\text{Precision}_{\text{mcl\_exceedance}}
         \ge 0.45$
       * **Rationale:** False alarms here only cost a confirmatory
         re-test, not a missed contamination event, so precision is
         deliberately the least strict of the three — a floor against
         a degenerate "flag everything" strategy, not a primary
         target. A 0.45 floor sits well above the random baseline's
         $\approx 0.30$ (which precision tracks almost for free, on
         account of the tier's own prevalence) without demanding the
         same ~2x margin recall and macro-F1 do, which would fight the
         asymmetric cost structure above. It reads as "just under half
         of every `mcl_exceedance` alert is confirmed," a step up from
         "4 out of 10."
    """)
    return


@app.cell
def _():
    # Agreed model success thresholds. Each is roughly 2x the
    # random-uniform baseline computed above, except PRECISION_FLOOR,
    # deliberately held to a softer margin per the asymmetric cost
    # structure in the per-class metrics rationale above (a missed
    # exceedance is worse than a false alarm).
    RECALL_FLOOR = 0.70
    MACRO_F1_FLOOR = 0.60
    PRECISION_FLOOR = 0.45
    return MACRO_F1_FLOOR, PRECISION_FLOOR, RECALL_FLOOR


@app.cell(hide_code=True)
def _(MACRO_F1_FLOOR, PRECISION_FLOOR, RECALL_FLOOR, majority_baseline, mo):
    # Plain markdown table, not a DataFrame: this is a documentation
    # summary, not meant to be reused in code — check_success_criteria()
    # below is the one reusable piece.
    _recall_row = (
        "| High-Risk Tier Recall | `mcl_exceedance` | "
        f"{majority_baseline['mcl_exceedance_recall']:.2f} | "
        f"≥ {RECALL_FLOOR:.2f} ({RECALL_FLOOR:.0%}) | "
        "Minimize missed high-risk contamination sites |"
    )
    _f1_row = (
        "| Macro-Averaged F1-Score | All Tiers (Unweighted) | "
        f"{majority_baseline['macro_f1']:.2f} | "
        f"≥ {MACRO_F1_FLOOR:.2f} | "
        "Ensure active learning across imbalanced classes |"
    )
    _precision_row = (
        "| High-Risk Tier Precision | `mcl_exceedance` | "
        f"{majority_baseline['mcl_exceedance_precision']:.2f} | "
        f"≥ {PRECISION_FLOOR:.2f} ({PRECISION_FLOOR:.0%}) | "
        "Control false alarms and preserve re-testing budgets |"
    )
    mo.md(f"""
    #### Summary of evaluation targets

    | Metric | Target | Naive Baseline | Threshold | Rationale |
    |---|---|---|---|---|
    {_recall_row}
    {_f1_row}
    {_precision_row}
    """)
    return


@app.cell
def _(MACRO_F1_FLOOR, PRECISION_FLOOR, RECALL_FLOOR, evaluate_tier_model, pd):
    def check_success_criteria(y_true, y_pred, model_name):
        """Score a model's predictions against the success thresholds.

        Reuses evaluate_tier_model() for the underlying metrics, then
        checks mcl_exceedance recall, macro F1, and mcl_exceedance
        precision against RECALL_FLOOR/MACRO_F1_FLOOR/PRECISION_FLOOR.
        Returns a per-metric pass/fail table, an overall pass/fail
        flag, and a one-line summary string.
        """
        _result = evaluate_tier_model(
            y_true, y_pred, model_name, recall_floor=RECALL_FLOOR
        )
        _summary = _result["summary"]
        _precision = _result["per_class"].loc["mcl_exceedance", "precision"]

        criteria_df = pd.DataFrame(
            [
                {
                    "Metric": "mcl_exceedance recall",
                    "Value": round(_summary["mcl_exceedance_recall"], 4),
                    "Threshold": RECALL_FLOOR,
                },
                {
                    "Metric": "macro F1",
                    "Value": round(_summary["macro_f1"], 4),
                    "Threshold": MACRO_F1_FLOOR,
                },
                {
                    "Metric": "mcl_exceedance precision",
                    "Value": round(_precision, 4),
                    "Threshold": PRECISION_FLOOR,
                },
            ]
        )
        criteria_df["Passed"] = (
            criteria_df["Value"] >= criteria_df["Threshold"]
        )
        criteria_df["Result"] = criteria_df.apply(
            lambda row: (
                f"{'PASS' if row['Passed'] else 'FAIL'} "
                f"({row['Value']:.2f} vs ≥{row['Threshold']:.2f})"
            ),
            axis=1,
        )

        all_passed = bool(criteria_df["Passed"].all())
        summary_line = f"{model_name}: " + (
            "PASSES all success criteria"
            if all_passed
            else "DOES NOT meet all success criteria"
        )

        return {
            "criteria": criteria_df,
            "all_passed": all_passed,
            "summary_line": summary_line,
        }

    return (check_success_criteria,)


@app.cell(hide_code=True)
def _(check_success_criteria, mo, tier_distribution, tier_true):
    # Sanity check: the majority-class baseline should fail every
    # criterion, since it never predicts mcl_exceedance at all.
    _majority_pred = [tier_distribution.idxmax()] * len(tier_true)
    _majority_check = check_success_criteria(
        tier_true, _majority_pred, "Majority class (zero-rule)"
    )
    mo.vstack(
        [
            mo.md(f"**{_majority_check['summary_line']}**"),
            mo.ui.table(_majority_check["criteria"]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(
    RISK_LABELS,
    StratifiedGroupKFold,
    classify_pfas_risk_tier,
    combinations,
    mo,
    pd,
    ss_scored_df,
):
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
    ).round({"Test fraction": 4, "Distribution gap": 4, "Selection score": 4})

    _comparison_columns = [
        "Method",
        "Candidate",
        "Held-out studies",
        "test_fraction",
        "missing_class_penalty",
        "distribution_gap",
        "selection_score",
    ]
    _split_comparison_preview = (
        _split_comparison_df[_comparison_columns]
        .head(20)
        .round(
            {"test_fraction": 4, "distribution_gap": 4, "selection_score": 4}
        )
    )

    _selected_test_mask = _tapwater_split_df["study_group"].isin(
        _selected_test_studies
    )
    tapwater_train_df = _tapwater_split_df.loc[~_selected_test_mask].copy()
    tapwater_test_df = _tapwater_split_df.loc[_selected_test_mask].copy()

    _train_studies = sorted(tapwater_train_df["study_group"].unique().tolist())
    _test_studies = sorted(tapwater_test_df["study_group"].unique().tolist())
    _study_overlap = sorted(set(_train_studies).intersection(_test_studies))
    _site_overlap = sorted(
        set(tapwater_train_df["Site Code"]).intersection(
            tapwater_test_df["Site Code"]
        )
    )

    _partition_summary = pd.DataFrame(
        [
            {
                "Partition": "Training",
                "Sites": len(tapwater_train_df),
                "Study groups": len(_train_studies),
                "Studies": ", ".join(_train_studies),
            },
            {
                "Partition": "Test",
                "Sites": len(tapwater_test_df),
                "Study groups": len(_test_studies),
                "Studies": ", ".join(_test_studies),
            },
        ]
    )

    _partition_class_summary = (
        pd.concat(
            [
                tapwater_train_df.assign(Partition="Training"),
                tapwater_test_df.assign(Partition="Test"),
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

                The ∑TQ construction supplies `ss_scored_df`, including
                the completed `sum_tq_epa` value. That continuous score is
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

                `mc_scored_df` is excluded from this tap-water split
                entirely. McMahon contains groundwater observations,
                omits GenX, and applies a different non-detect
                convention, so its target distribution is not on the
                same footing as Smalling/Seawolf. It is used only as a
                qualified external validation slice, never for
                training — the next section covers why.
                """
            ),
        ]
    )
    return tapwater_test_df, tapwater_train_df


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Groundwater's role - held-out vs. combined
    """)
    return


@app.cell(hide_code=True)
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
                "sum_tq_epa median": round(
                    ss_scored_df["sum_tq_epa"].median(), 4
                ),
                **_tier_distribution(ss_scored_df).round(4).to_dict(),
            },
            {
                "Study": "McMahon (groundwater)",
                "Sites": len(mc_scored_df),
                "Compounds summed": 5,
                "Non-detect convention": "½ reporting limit",
                "sum_tq_epa median": round(
                    mc_scored_df["sum_tq_epa"].median(), 4
                ),
                **_tier_distribution(mc_scored_df).round(4).to_dict(),
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
            mo.ui.table(groundwater_comparison_df.set_index("Study").T),
            mo.md(
                """
                #### Decision: hold out, don't combine

                Combining McMahon into the Smalling/Seawolf training set
                would let a model achieve perfect recall on the
                `mcl_exceedance` tier simply by learning "is this a
                McMahon row," an artifact of imputation and compound
                coverage, not a land-use signal — exactly the kind of
                leakage the study-grouped split guards against for
                cross-study effects. A single-class study also cannot
                exercise the per-class metrics defined for the
                classification task, which need all three tiers
                represented.

                McMahon's data will not be used for training. It stays
                fully outside both the training and test partitions,
                and model predictions on it are reported separately as
                a qualified validation check — framed explicitly as
                "does the model's *relative* ranking of McMahon sites
                look plausible," not as a comparable accuracy number,
                since the target itself isn't comparable across studies.
                Revisit combining groundwater and tap-water data only if
                a future revision of this analysis re-derives McMahon's
                ∑TQ with a matched non-detect convention and a GenX
                estimate.
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
def _(mo):
    mo.md("""
    ### Handling skew & encoding on the finalized feature table
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before feeding the landscape predictors into classification
    algorithms, a clean feature matrix $X$ requires resolving two
    common dataset characteristics: **extreme numerical skewness** and
    **unencoded categorical features**. McMahon (`mc_scored_df`) is
    excluded here — per the groundwater-role decision, it's held out
    of training entirely and used only as a validation slice.

    #### Rationale for skew transformation ($\log_{1p}$)
    Environmental landscape variables — such as distances to nearest
    industrial facilities, military sites, or localized urban burn
    areas — frequently exhibit strong right-skewed distributions with
    long upper tails.
    * **Why this matters:** Unscaled, highly skewed features can
      distort linear models (like Logistic Regression) and
      distance-based estimators by placing disproportionate weight on
      extreme outlier values.
    * **Skew correction:** Calculate the Fisher-Pearson coefficient of
      skewness for all numeric predictors. For features exhibiting
      significant right-skewness ($\text{skewness} > 1.0$), apply a
      $\log_{1p}(x) = \log(1 + x)$ transformation, which compresses
      the upper tail while preserving zero values safely without
      mathematical division errors. Numeric columns are then
      standardized with `StandardScaler`.

    #### Categorical encoding, fit on the training split only
    Categorical flags — such as site type (public supply vs. private
    wells) and state — are converted into numeric format using
    **one-hot encoding**
    (`OneHotEncoder(handle_unknown="ignore", drop="first")`) inside a
    `ColumnTransformer`. Study identifiers (`Study_smalling`,
    `Study_seawolf`) are excluded from $X$ entirely — retained as
    controls, not predictors, per the Step 2.5 plan above.
    Dropping the first dummy column prevents perfect multicollinearity
    in linear baselines. The transformer is fit on `X_train` only and
    applied to `X_test` without refitting, so no information from the
    held-out split leaks into scaling or encoding.
    """)
    return


@app.cell
def _(ColumnTransformer, OneHotEncoder, StandardScaler, np, pd):
    # Columns that either leak the target (raw TQ/tier fields), aren't
    # predictors (identifiers/metadata), are study-split bookkeeping
    # added by the split-strategy section, or are study identifiers
    # retained as controls rather than predictors per the Step 2.5
    # plan get excluded from X.
    _LEAKAGE_AND_ID_COLS = [
        "Site Code",
        "SiteCode",
        "NAWQA_ID",
        "_merge",
        "Total_PFAS",
        "sum_TQ",
        "sum_tq_epa",
        "sum_tq_state_only",
        "Contamination_Class",
        "pfas_risk_tier",
        "study_group",
        "Study_smalling",
        "Study_seawolf",
    ]

    def preprocess_tapwater_features(train_df, test_df, skew_threshold=1.0):
        feature_cols = [
            c for c in train_df.columns if c not in _LEAKAGE_AND_ID_COLS
        ]
        X_train = train_df[feature_cols].copy()
        X_test = test_df[feature_cols].copy()
        y_train = train_df["pfas_risk_tier"].astype(str)
        y_test = test_df["pfas_risk_tier"].astype(str)

        numeric_cols = X_train.select_dtypes(
            include=[np.number]
        ).columns.tolist()
        categorical_cols = X_train.select_dtypes(
            exclude=[np.number]
        ).columns.tolist()

        # log1p right-skewed numeric predictors using training-split
        # skewness only, so no information from the test partition
        # informs which features get transformed.
        initial_skew = X_train[numeric_cols].skew(numeric_only=True)
        skewed_features = initial_skew[
            initial_skew > skew_threshold
        ].index.tolist()
        for col in skewed_features:
            if (X_train[col] >= 0).all() and (X_test[col] >= 0).all():
                X_train[col] = np.log1p(X_train[col])
                X_test[col] = np.log1p(X_test[col])

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), numeric_cols),
                (
                    "cat",
                    OneHotEncoder(handle_unknown="ignore", drop="first"),
                    categorical_cols,
                ),
            ],
            remainder="drop",
        )
        X_train_processed = preprocessor.fit_transform(X_train)
        X_test_processed = preprocessor.transform(X_test)

        skew_audit = pd.DataFrame(
            {
                "Feature": skewed_features,
                "Initial Skew": [
                    round(initial_skew[f], 4) for f in skewed_features
                ],
            }
        )

        return {
            "preprocessor": preprocessor,
            "X_train": X_train_processed,
            "X_test": X_test_processed,
            "y_train": y_train,
            "y_test": y_test,
            "feature_names": numeric_cols + categorical_cols,
            "skew_audit": skew_audit,
        }

    return (preprocess_tapwater_features,)


@app.cell(hide_code=True)
def _(mo, preprocess_tapwater_features, tapwater_test_df, tapwater_train_df):
    _tapwater_model_matrices = preprocess_tapwater_features(
        tapwater_train_df, tapwater_test_df
    )

    mo.vstack(
        [
            mo.md(
                "#### Feature-preprocessing audit: features transformed "
                "via $\\log_{1p}$ (tap-water set)"
            ),
            mo.ui.table(_tapwater_model_matrices["skew_audit"].head(10)),
            mo.md(
                f"**Train/test feature matrix shape:** "
                f"`{_tapwater_model_matrices['X_train'].shape}` / "
                f"`{_tapwater_model_matrices['X_test'].shape}`"
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


if __name__ == "__main__":
    app.run()

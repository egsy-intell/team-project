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
    evaluate_tier_model = checkpoint_2_result.defs["evaluate_tier_model"]
    check_success_criteria = checkpoint_2_result.defs["check_success_criteria"]
    RECALL_FLOOR = checkpoint_2_result.defs["RECALL_FLOOR"]
    MACRO_F1_FLOOR = checkpoint_2_result.defs["MACRO_F1_FLOOR"]
    PRECISION_FLOOR = checkpoint_2_result.defs["PRECISION_FLOOR"]
    return (
        MACRO_F1_FLOOR,
        PRECISION_FLOOR,
        RECALL_FLOOR,
        check_success_criteria,
        evaluate_tier_model,
        tapwater_test_df,
        tapwater_train_df,
    )


@app.cell(hide_code=True)
def _():
    # Shared third-party imports for this notebook, defined once so
    # downstream cells take them as parameters instead of each
    # re-importing numpy/pandas/sklearn locally.
    import warnings

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn.base import BaseEstimator, TransformerMixin, clone
    from sklearn.compose import ColumnTransformer
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import f1_score, precision_score, recall_score
    from sklearn.model_selection import (
        GridSearchCV,
        RandomizedSearchCV,
        StratifiedGroupKFold,
    )
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    return (
        BaseEstimator,
        ColumnTransformer,
        GridSearchCV,
        LogisticRegression,
        OneHotEncoder,
        Pipeline,
        RandomForestClassifier,
        RandomizedSearchCV,
        SimpleImputer,
        StandardScaler,
        StratifiedGroupKFold,
        TransformerMixin,
        clone,
        f1_score,
        np,
        pd,
        plt,
        precision_score,
        recall_score,
        warnings,
    )


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
def _(mo):
    mo.md("""
    ### Feedback selected for integration

    Peer review on Check-In #2 surfaced two items the team is
    integrating into this submission: keeping the results sections
    lighter on detail and leading with results, and quantifying the
    underlying site-count sparsity (e.g. ~5 sites/state on average
    across the bottom 15 states) to acknowledge the geographic
    generalizability limit it creates. Both are threaded into T9's
    and T10's guiding questions below.
    """)
    return


@app.cell(hide_code=True)
def _(mo, task_callout):
    mo.vstack(
        [
            mo.md("### Implement feedback change"),
            task_callout(
                "T4",
                category="Feedback integration",
                lead="Yai, Somyaranjan",
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
def _(mo):
    mo.md("""
    ### Shared setup for Model A & Model B

    Per the Step 4 proposals, Model B reuses Model A's approved
    predictor set, grouped cross-validation strategy, and scoring
    metrics. These are defined once here so both models can train
    against identical folds and report the same CV diagnostics.
    """)
    return


@app.cell(hide_code=True)
def _(tapwater_train_df):
    # Approved Seawolf landscape / land-use predictors, shared by
    # Model A and Model B per the Step 4 proposal.
    _candidate_numeric_predictors = [
        "number_pfas_sites_proximal",
        "mean_dist_to_pfas_site",
        "Burn_Area_5k_frac",
        "Burn_area_50k_frac",
        "Urbn_burn_5k_frac",
        "Urbn_burn_50k_frac",
        "OpenWater",
        "PerennialIceSnow",
        "DevelopedOpenSpace",
        "DevelopedLowIntensity",
        "DevelopedMediumIntensity",
        "DevelopedHighIntensity",
        "Barren",
        "DeciduousForest",
        "EvergreenForest",
        "MixedForest",
        "DwarfScrub",
        "ShrubScrub",
        "GrasslandHerbaceous",
        "SedgeHerbaceous",
        "Moss",
        "PastureHay",
        "CultivatedCrop",
        "WoodyWetlands",
        "EmergentHerbaceousWetlands",
    ]
    _candidate_categorical_predictors = ["State", "Site Type"]

    numeric_predictors = [
        c
        for c in _candidate_numeric_predictors
        if c in tapwater_train_df.columns
    ]
    categorical_predictors = [
        c
        for c in _candidate_categorical_predictors
        if c in tapwater_train_df.columns
    ]
    model_predictors = numeric_predictors + categorical_predictors

    if not numeric_predictors:
        raise ValueError("Could not find the Seawolf predictors.")
    return categorical_predictors, model_predictors, numeric_predictors


@app.cell(hide_code=True)
def _(StratifiedGroupKFold, tapwater_train_df):
    # Grouped CV strategy shared by Model A and Model B, so both
    # models' tuning candidates are scored on identical folds.
    study_groups = tapwater_train_df["study_group"].astype(str)
    grouped_cv = StratifiedGroupKFold(
        n_splits=min(5, study_groups.nunique()),
        shuffle=True,
        random_state=42,
    )
    return grouped_cv, study_groups


@app.cell(hide_code=True)
def _(f1_score, precision_score, recall_score):
    # Shared CV metrics. T5 selects Model A by macro-F1 only.
    # Recall and precision are retained as diagnostics for T7/T9.
    def _macro_f1(estimator, X_valid, y_valid):
        _pred = estimator.predict(X_valid)
        return f1_score(
            y_valid,
            _pred,
            average="macro",
            zero_division=0,
        )

    def _mcl_recall(estimator, X_valid, y_valid):
        _pred = estimator.predict(X_valid)
        return recall_score(
            y_valid,
            _pred,
            labels=["mcl_exceedance"],
            average="macro",
            zero_division=0,
        )

    def _mcl_precision(estimator, X_valid, y_valid):
        _pred = estimator.predict(X_valid)
        return precision_score(
            y_valid,
            _pred,
            labels=["mcl_exceedance"],
            average="macro",
            zero_division=0,
        )

    tier_model_scoring = {
        "macro_f1": _macro_f1,
        "mcl_recall": _mcl_recall,
        "mcl_precision": _mcl_precision,
    }
    return (tier_model_scoring,)


@app.cell(hide_code=True)
def _(pd):
    def build_cv_results_table(cv_results, param_columns, best_index):
        """Per-candidate CV results, selected candidate sorted to top.

        `param_columns` maps a display column name to `(param_key,
        format_fn)`, so Model A and Model B can each supply their own
        hyperparameter names/formatting while sharing the selection
        and sort logic.
        """
        _data = {
            _label: [_format(_v) for _v in cv_results[_param_key]]
            for _label, (_param_key, _format) in param_columns.items()
        }
        _data["CV macro F1"] = cv_results["mean_test_macro_f1"]
        _data["CV mcl recall"] = cv_results["mean_test_mcl_recall"]
        _data["CV mcl precision"] = cv_results["mean_test_mcl_precision"]

        _df = pd.DataFrame(_data)
        _df["Selected"] = False
        _df.loc[best_index, "Selected"] = True
        return _df.sort_values(
            ["Selected", "CV macro F1"], ascending=[False, False]
        ).reset_index(drop=True)

    return (build_cv_results_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### Held-out scoring harness

    Five thin wrappers score Model A and Model B the same way,
    without duplicating logic per model. `score_model()` wraps
    checkpoint_2's `evaluate_tier_model()` and `check_success_criteria()`
    against the held-out test set, the same way Step 3 already defined
    success. `error_breakdown_by_study()` takes a `score_model()`
    result and reports whether errors concentrate in one held-out
    study or spread evenly, `plot_error_rate_by_study()` renders that
    same breakdown as a chart, `build_model_comparison()` pulls each
    model's headline metrics into one row of a shared table - add a
    model by adding a dict entry, not by restructuring it - and
    `plot_model_comparison()` renders that table as small multiples,
    one panel per metric with its Step 3 threshold line. All five
    live here, next to `tier_model_scoring`, so T9's benchmarking can
    reuse them too.
    """)
    return


@app.cell(hide_code=True)
def _(
    RECALL_FLOOR,
    check_success_criteria,
    evaluate_tier_model,
    model_predictors,
):
    def score_model(pipeline, df, model_name):
        """Score a fitted pipeline against a held-out dataframe.

        Predicts with `pipeline` on `df[model_predictors]`, then hands
        the true/predicted tiers to `evaluate_tier_model()` and
        `check_success_criteria()`. `df` must carry a `pfas_risk_tier`
        column (both `tapwater_test_df` and `tapwater_train_df` do).
        """
        X = df[model_predictors]
        y_true = df["pfas_risk_tier"].astype(str)
        y_pred = pipeline.predict(X)
        return {
            "y_true": y_true,
            "y_pred": y_pred,
            "metrics": evaluate_tier_model(
                y_true, y_pred, model_name, recall_floor=RECALL_FLOOR
            ),
            "criteria": check_success_criteria(y_true, y_pred, model_name),
        }

    return (score_model,)


@app.cell(hide_code=True)
def _(pd):
    def error_breakdown_by_study(result, df):
        """Held-out error rate by `study_group`, for a score_model() result.

        Takes a score_model() result dict and the dataframe it was
        scored against, and reports whether errors concentrate in one
        held-out study or spread evenly (T7's second guiding
        question). Model B calls this the same way once T6 lands.
        """
        _breakdown = pd.DataFrame(
            {
                "study_group": df["study_group"].to_numpy(),
                "actual": result["y_true"].to_numpy(),
                "predicted": result["y_pred"],
            }
        )
        _breakdown["correct"] = _breakdown["actual"] == _breakdown["predicted"]
        return (
            _breakdown.groupby("study_group")
            .agg(
                sites=("correct", "size"),
                errors=("correct", lambda s: int((~s).sum())),
            )
            .assign(error_rate=lambda d: (d["errors"] / d["sites"]).round(4))
            .reset_index()
            .sort_values("error_rate", ascending=False)
        )

    return (error_breakdown_by_study,)


@app.cell(hide_code=True)
def _(mo, plt):
    def plot_error_rate_by_study(breakdown_df, title):
        # Sequential, single-hue (same blue family as make_plot_grid's
        # histograms): this is one measurement varying by study, not
        # distinct series, so magnitude gets light->dark shading, not
        # a categorical color per bar.
        _df = breakdown_df.sort_values("error_rate", ascending=True)
        _cmap = plt.get_cmap("Blues")
        _colors = [_cmap(0.35 + 0.55 * r) for r in _df["error_rate"]]

        fig, ax = plt.subplots(figsize=(6, 0.6 * len(_df) + 1))
        _bars = ax.barh(_df["study_group"], _df["error_rate"], color=_colors)
        for _bar, (_, _row) in zip(_bars, _df.iterrows()):
            ax.text(
                _bar.get_width() + 0.02,
                _bar.get_y() + _bar.get_height() / 2,
                f"{_row['error_rate']:.0%} ({_row['errors']}/{_row['sites']})",
                va="center",
                fontsize=9,
            )
        ax.set_xlim(0, 1.15)
        ax.set_xlabel("Held-out error rate")
        ax.set_title(title, fontsize=12, pad=10)
        ax.grid(True, axis="x", linestyle="--", alpha=0.35)
        ax.set_axisbelow(True)
        for _spine in ("top", "right", "left"):
            ax.spines[_spine].set_visible(False)
        fig.tight_layout()
        # mo.mpl.interactive adds pan/zoom/hover for anyone running the
        # notebook live; it degrades to the same static PNG as a plain
        # figure in the published static HTML, so there's no downside
        # there.
        return mo.mpl.interactive(fig)

    return (plot_error_rate_by_study,)


@app.cell(hide_code=True)
def _(pd):
    def build_model_comparison(results):
        """Model A vs. Model B comparison table from score_model() results.

        `results` is `{model_name: score_model() result}`; add a
        model by adding a dict entry, not by restructuring the table.
        Pulls the three T7/T9 headline metrics (mcl_exceedance
        recall, macro F1, mcl_exceedance precision) plus the overall
        Step 3 pass/fail from each model's `check_success_criteria()`
        output.
        """
        _rows = []
        for _name, _result in results.items():
            _criteria = _result["criteria"]["criteria"].set_index("Metric")[
                "Value"
            ]
            _rows.append(
                {
                    "Model": _name,
                    "mcl_exceedance recall": _criteria[
                        "mcl_exceedance recall"
                    ],
                    "Macro F1": _criteria["macro F1"],
                    "mcl_exceedance precision": _criteria[
                        "mcl_exceedance precision"
                    ],
                    "Meets all Step 3 criteria": _result["criteria"][
                        "all_passed"
                    ],
                }
            )
        return pd.DataFrame(_rows)

    return (build_model_comparison,)


@app.cell(hide_code=True)
def _():
    # Fixed categorical order for model identity in comparison charts:
    # blue/orange is a high-contrast, colorblind-safe pair. Assigned
    # by position (first model in the table gets slot 0), never by
    # value or rank, so a filter changing which models are shown
    # doesn't repaint the survivors.
    MODEL_COMPARISON_PALETTE = ("#2a6f97", "#e07b39", "#4c9f70", "#a6528c")
    return (MODEL_COMPARISON_PALETTE,)


@app.cell(hide_code=True)
def _(
    MACRO_F1_FLOOR,
    MODEL_COMPARISON_PALETTE,
    PRECISION_FLOOR,
    RECALL_FLOOR,
    mo,
    plt,
):
    def plot_model_comparison(comparison_df, title):
        """Small multiples: one panel per metric, bars by model.

        Each panel gets its own Step 3 threshold line, since recall,
        macro F1, and precision each have a different floor - one
        combined chart would need three crowded reference lines.
        """
        _metrics = (
            ("mcl_exceedance recall", RECALL_FLOOR),
            ("Macro F1", MACRO_F1_FLOOR),
            ("mcl_exceedance precision", PRECISION_FLOOR),
        )
        _models = comparison_df["Model"].tolist()
        _colors = dict(zip(_models, MODEL_COMPARISON_PALETTE))

        fig, axes = plt.subplots(
            1, len(_metrics), figsize=(4 * len(_metrics), 3.2)
        )
        for ax, (_metric, _floor) in zip(axes, _metrics):
            _values = comparison_df[_metric]
            _bars = ax.bar(
                _models,
                _values,
                color=[_colors[m] for m in _models],
                width=0.5,
            )
            ax.axhline(_floor, color="#444444", linestyle="--", linewidth=1)
            ax.text(
                len(_models) - 0.5,
                _floor,
                f"≥ {_floor:.2f}",
                va="bottom",
                ha="right",
                fontsize=8,
                color="#444444",
            )
            for _bar, _value in zip(_bars, _values):
                ax.text(
                    _bar.get_x() + _bar.get_width() / 2,
                    _bar.get_height() + 0.02,
                    f"{_value:.2f}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                )
            ax.set_ylim(0, 1.1)
            ax.set_title(_metric, fontsize=10, pad=8)
            ax.grid(True, axis="y", linestyle="--", alpha=0.35)
            ax.set_axisbelow(True)
            for _spine in ("top", "right"):
                ax.spines[_spine].set_visible(False)

        fig.suptitle(title, fontsize=12, y=1.04)
        if len(_models) > 1:
            _handles = [
                plt.Rectangle((0, 0), 1, 1, color=_colors[m]) for m in _models
            ]
            fig.legend(
                _handles,
                _models,
                loc="upper center",
                ncol=len(_models),
                bbox_to_anchor=(0.5, -0.05),
                frameon=False,
            )
        fig.tight_layout()
        return mo.mpl.interactive(fig)

    return (plot_model_comparison,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Baseline model A Implementation

    Model A is the multinomial logistic-regression baseline proposed in
    Step 4. It is trained only on `tapwater_train_df` using study-grouped
    cross-validation; the held-out test partition is not used here and
    remains untouched for held-out evaluation.

    Hyperparameter selection in T5 uses mean grouped-CV macro-F1 only.
    The CV recall and precision values for `mcl_exceedance` are retained
    as tuning diagnostics, not as the final Step 3 pass/fail decision.
    The held-out evaluation and benchmarking make that determination.

    This also uses an explicit predictor allowlist so raw PFAS
    concentrations, ∑TQ fields, identifiers, and study labels cannot
    accidentally enter the model.

    Because cross-validation is grouped by study, an entire
    `study_group` moves together into either the fitting or validation
    portion of a fold. A `State` or `Site Type` category concentrated in
    only one or two studies may therefore be absent from a fold's
    fitting data but appear in its validation data. T5 audits each fold
    for these unseen categories and uses full one-hot encoding with
    `handle_unknown="ignore"` and `drop=None` so they can be handled
    safely.

    The current allowlisted predictors contain no missing values in the
    T5 training partition, so both the numeric and categorical imputers
    are no-ops on the present data. They are retained as defensive
    preprocessing steps for future data that may contain missing values.
    """)
    return


@app.cell
def _(
    BaseEstimator,
    ColumnTransformer,
    GridSearchCV,
    LogisticRegression,
    OneHotEncoder,
    Pipeline,
    SimpleImputer,
    StandardScaler,
    TransformerMixin,
    build_cv_results_table,
    categorical_predictors,
    grouped_cv,
    model_predictors,
    np,
    numeric_predictors,
    pd,
    study_groups,
    tapwater_train_df,
    tier_model_scoring,
    warnings,
):
    _X_train = tapwater_train_df[model_predictors].copy()
    _y_train = tapwater_train_df["pfas_risk_tier"].astype(str)

    # Check whether a validation fold contains a categorical level that
    # is absent from that fold's fitting studies.
    _unseen_rows = []
    for _fold, (_fit_idx, _valid_idx) in enumerate(
        grouped_cv.split(_X_train, _y_train, groups=study_groups),
        start=1,
    ):
        _fit_part = _X_train.iloc[_fit_idx]
        _valid_part = _X_train.iloc[_valid_idx]

        for _column in categorical_predictors:
            _fit_levels = set(
                _fit_part[_column].dropna().astype(str).str.strip()
            )
            _valid_levels = set(
                _valid_part[_column].dropna().astype(str).str.strip()
            )
            _unseen = sorted(_valid_levels - _fit_levels)

            if _unseen:
                _unseen_rows.append(
                    {
                        "Fold": _fold,
                        "Feature": _column,
                        "Unseen categories": ", ".join(_unseen),
                    }
                )

    model_a_unseen_categories = pd.DataFrame(_unseen_rows)

    class _SkewLog1p(BaseEstimator, TransformerMixin):
        """Learn skewed numeric columns inside each training fold."""

        def __init__(self, threshold=1.0):
            self.threshold = threshold

        def fit(self, X, y=None):
            _frame = X.copy()
            self.feature_names_in_ = np.asarray(_frame.columns, dtype=object)
            _skew = _frame.skew(numeric_only=True)
            self.skewed_features_ = [
                c
                for c in _frame.columns
                if _skew.get(c, 0.0) > self.threshold
                and (_frame[c].dropna() >= 0).all()
            ]
            return self

        def transform(self, X):
            _frame = X.copy()
            for _column in self.skewed_features_:
                _frame[_column] = np.log1p(_frame[_column])
            return _frame

        def get_feature_names_out(self, input_features=None):
            if input_features is None:
                input_features = self.feature_names_in_
            return np.asarray(input_features, dtype=object)

    _numeric_pipeline = Pipeline(
        [
            ("skew_log1p", _SkewLog1p(threshold=1.0)),
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    # Step 4 proposed drop="first". With grouped CV, an unseen State
    # would also be encoded as all zeros, making it indistinguishable
    # from the dropped reference State. Keeping all one-hot columns
    # avoids that ambiguity. L2 regularization handles the redundancy.
    _categorical_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore",
                    drop=None,
                ),
            ),
        ]
    )

    _preprocessor = ColumnTransformer(
        [
            ("num", _numeric_pipeline, numeric_predictors),
            ("cat", _categorical_pipeline, categorical_predictors),
        ],
        remainder="drop",
    )

    # LogisticRegression uses L2 regularization by default.
    _pipeline = Pipeline(
        [
            ("preprocessor", _preprocessor),
            (
                "model",
                LogisticRegression(
                    solver="lbfgs",
                    max_iter=2000,
                ),
            ),
        ]
    )

    # Small Step 4 tuning grid.
    _param_grid = {
        "model__C": [0.1, 1.0, 10.0],
        "model__class_weight": [None, "balanced"],
    }

    # T5 selects the candidate with the highest mean grouped-CV
    # macro-F1. High-risk recall/precision remain diagnostics only.
    model_a_grid_search = GridSearchCV(
        estimator=_pipeline,
        param_grid=_param_grid,
        scoring=tier_model_scoring,
        refit="macro_f1",
        cv=grouped_cv,
        n_jobs=-1,
        error_score="raise",
    )

    # Unknown categories are audited above. Suppress repeated sklearn
    # warnings during every grid-search fold.
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="Found unknown categories.*",
            category=UserWarning,
        )
        model_a_grid_search.fit(
            _X_train,
            _y_train,
            groups=study_groups,
        )

    model_a_best_estimator = model_a_grid_search.best_estimator_

    model_a_cv_results = build_cv_results_table(
        model_a_grid_search.cv_results_,
        {
            "C": ("param_model__C", lambda x: x),
            "Class weight": (
                "param_model__class_weight",
                lambda x: "unweighted" if x is None else str(x),
            ),
        },
        model_a_grid_search.best_index_,
    )

    _pre = model_a_best_estimator.named_steps["preprocessor"]
    _model = model_a_best_estimator.named_steps["model"]
    _encoded_count = len(_pre.get_feature_names_out())
    _skewed_count = len(
        _pre.named_transformers_["num"]
        .named_steps["skew_log1p"]
        .skewed_features_
    )

    _selected = model_a_cv_results[model_a_cv_results["Selected"]].iloc[0]

    model_a_training_summary = pd.DataFrame(
        [
            {
                "Training rows": len(_X_train),
                "Study groups": study_groups.nunique(),
                "Raw predictors": len(model_predictors),
                "Encoded predictors": _encoded_count,
                "Missing predictor values": int(_X_train.isna().sum().sum()),
                "log1p predictors": _skewed_count,
                "Best C": model_a_grid_search.best_params_["model__C"],
                "Best class weight": (
                    "unweighted"
                    if model_a_grid_search.best_params_["model__class_weight"]
                    is None
                    else model_a_grid_search.best_params_[
                        "model__class_weight"
                    ]
                ),
                "CV macro F1": round(_selected["CV macro F1"], 4),
                "CV mcl recall": round(_selected["CV mcl recall"], 4),
                "CV mcl precision": round(_selected["CV mcl precision"], 4),
                "Iterations used": int(np.max(_model.n_iter_)),
            }
        ]
    )
    return (
        model_a_best_estimator,
        model_a_cv_results,
        model_a_training_summary,
        model_a_unseen_categories,
    )


@app.cell
def _(model_a_best_estimator, np, pd):
    _pre = model_a_best_estimator.named_steps["preprocessor"]
    _model = model_a_best_estimator.named_steps["model"]
    _feature_names = _pre.get_feature_names_out()
    _classes = list(_model.classes_)

    _mcl_idx = _classes.index("mcl_exceedance")
    _coefficients = _model.coef_[_mcl_idx]

    _coef_df = pd.DataFrame(
        {
            "Feature": _feature_names,
            "Coefficient": _coefficients,
        }
    )
    _coef_df["Abs coefficient"] = _coef_df["Coefficient"].abs()
    _coef_df["Direction"] = np.where(
        _coef_df["Coefficient"] > 0,
        "positive",
        np.where(_coef_df["Coefficient"] < 0, "negative", "zero"),
    )

    model_a_top_coefficients = (
        _coef_df.sort_values("Abs coefficient", ascending=False)
        .head(12)
        .reset_index(drop=True)
    )

    # Only test direction where there is a reasonable prior expectation.
    _expected = {
        "number_pfas_sites_proximal": "positive",
        "mean_dist_to_pfas_site": "negative",
        "DevelopedMediumIntensity": "positive",
        "DevelopedHighIntensity": "positive",
        "Urbn_burn_5k_frac": "positive",
        "Urbn_burn_50k_frac": "positive",
    }

    _rows = []
    for _feature, _expected_direction in _expected.items():
        _row = _coef_df[_coef_df["Feature"] == f"num__{_feature}"]
        if _row.empty:
            continue

        _value = float(_row.iloc[0]["Coefficient"])
        _observed = (
            "positive" if _value > 0 else "negative" if _value < 0 else "zero"
        )
        _rows.append(
            {
                "Feature": _feature,
                "Expected": _expected_direction,
                "Observed": _observed,
                "Coefficient": round(_value, 4),
                "Matches": _observed == _expected_direction,
            }
        )

    model_a_direction_audit = pd.DataFrame(_rows)
    return model_a_direction_audit, model_a_top_coefficients


@app.cell(hide_code=True)
def _(
    mo,
    model_a_cv_results,
    model_a_direction_audit,
    model_a_top_coefficients,
    model_a_training_summary,
    model_a_unseen_categories,
):
    if model_a_unseen_categories.empty:
        _unseen_text = (
            "No unseen categorical levels appeared in the current "
            "grouped cross-validation folds. The audit is still "
            "important because each study group moves entirely into "
            "either fitting or validation data, so a State or Site Type "
            "concentrated in a small number of studies could be absent "
            "from a fitting fold. If this occurs after a different fold "
            "assignment or future data update, "
            "`handle_unknown='ignore'` allows the pipeline to process "
            "the unseen category safely."
        )
        _unseen_view = mo.md(_unseen_text)
    else:
        _features = ", ".join(
            sorted(model_a_unseen_categories["Feature"].unique())
        )
        _unseen_text = (
            "Yes. Grouped cross-validation produced categorical levels "
            f"in {_features} that were not present in one or more fitting "
            "folds. `handle_unknown='ignore'` prevents a failure, but "
            "Step 4's `drop='first'` would make an unseen category look "
            "the same as the dropped reference category. T5 therefore "
            "uses full one-hot encoding (`drop=None`)."
        )
        _unseen_view = mo.ui.table(model_a_unseen_categories)

    if model_a_direction_audit.empty:
        _coef_text = (
            "No pre-specified directional checks were available in the "
            "final feature matrix."
        )
    else:
        _counter = model_a_direction_audit[~model_a_direction_audit["Matches"]]
        if _counter.empty:
            _coef_text = (
                "All predictors with a clear prior expectation have "
                "high-risk coefficients in the expected direction. This "
                "supports the Step 4 interpretability claim, while the "
                "coefficients should still be treated as associations, "
                "not causal effects."
            )
        else:
            _names = ", ".join(_counter["Feature"].tolist())
            _coef_text = (
                f"The coefficients remain inspectable, but {_names} run "
                "counter to the expected high-risk direction. This does "
                "not automatically invalidate Model A; it shows that "
                "effects are conditional on the other correlated "
                "predictors and should not be read causally."
            )

    _state_count = int(
        model_a_top_coefficients["Feature"]
        .astype(str)
        .str.startswith("cat__State_")
        .sum()
    )
    if _state_count:
        _coef_text += (
            f" {_state_count} of the 12 largest absolute coefficients "
            "are State indicators, so geographic effects also need "
            "cautious interpretation."
        )

    mo.vstack(
        [
            mo.md("#### Training and tuning summary"),
            mo.ui.table(model_a_training_summary),
            mo.md(
                """
                #### Tuning grid results

                The values below are mean cross-validation estimates from
                the grouped grid search. They describe how each
                hyperparameter setting performed across the training
                folds; they are not held-out test results for the final
                refit Model A.

                `Selected=True` identifies the hyperparameter setting
                with the highest mean grouped-CV macro-F1. The
                `mcl_exceedance` recall and precision values are retained
                as tuning diagnostics only and do not determine model
                selection in T5. Final threshold evaluation is performed
                in the evaluation using the held-out studies.
                """
            ),
            mo.ui.table(model_a_cv_results.round(4)),
            mo.md("#### Unseen-category audit"),
            _unseen_view,
            mo.md("#### Largest coefficients for `mcl_exceedance`"),
            mo.ui.table(
                model_a_top_coefficients[
                    ["Feature", "Coefficient", "Direction"]
                ].round(4)
            ),
            mo.md("#### Expected-direction check"),
            mo.ui.table(model_a_direction_audit),
            mo.md(
                f"""
                #### T5 findings summary

                Model A tuning is based on grouped-CV macro-F1 only.
                High-risk recall and precision remain visible as
                training-time diagnostics, while the authoritative
                threshold assessment is performed later on the
                held-out studies.

                {_unseen_text}

                The current T5 training predictors have no missing
                values, so the numeric and categorical imputers are
                currently no-ops. They remain in the pipeline as
                defensive preprocessing for future data.

                The training implementation also showed that the earlier
                generic feature-selection approach could allow raw PFAS
                concentration or outcome-related fields into the model.
                T5 avoids this leakage by using an explicit allowlist of
                landscape, land-use, State, and Site Type predictors.

                {_coef_text}
                """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Model B: random forest

    We train the competing ensemble on the same predictor set, training
    partition, fold-specific preprocessing, and grouped cross-validation
    splits as Model A. This keeps the comparison focused on the classifier
    rather than differences in data preparation.
    """)
    return


@app.cell
def _(
    RandomForestClassifier,
    RandomizedSearchCV,
    build_cv_results_table,
    clone,
    grouped_cv,
    model_a_best_estimator,
    model_predictors,
    pd,
    study_groups,
    tapwater_train_df,
    tier_model_scoring,
):
    """Train Model B with Emir's randomized Random Forest search."""
    _X_train = tapwater_train_df[model_predictors].copy()
    _y_train = tapwater_train_df["pfas_risk_tier"].astype(str)

    # Clone Model A's complete pipeline so both models receive the same
    # fold-fitted preprocessing. Replacing only the estimator prevents
    # preprocessing leakage and leaves a pipeline that score_model() can
    # call directly on the raw held-out predictor columns.
    _pipeline = clone(model_a_best_estimator).set_params(
        model=RandomForestClassifier(random_state=42, n_jobs=-1)
    )

    # Emir's original conservative six-candidate randomized search.
    _param_distributions = {
        "model__n_estimators": [100, 200, 300],
        "model__max_depth": [None, 10, 20],
        "model__min_samples_leaf": [1, 2, 4],
    }

    model_b_grid_search = RandomizedSearchCV(
        estimator=_pipeline,
        param_distributions=_param_distributions,
        n_iter=6,
        scoring=tier_model_scoring,
        refit="macro_f1",
        cv=grouped_cv,
        return_train_score=True,
        n_jobs=-1,
        random_state=42,
        error_score="raise",
    )
    model_b_grid_search.fit(
        _X_train,
        _y_train,
        groups=study_groups,
    )

    model_b_best_estimator = model_b_grid_search.best_estimator_
    model_b_cv_results = build_cv_results_table(
        model_b_grid_search.cv_results_,
        {
            "Trees": ("param_model__n_estimators", lambda x: x),
            "Maximum depth": (
                "param_model__max_depth",
                lambda x: "unlimited" if x is None else x,
            ),
            "Minimum leaf size": (
                "param_model__min_samples_leaf",
                lambda x: x,
            ),
        },
        model_b_grid_search.best_index_,
    )

    _selected = model_b_cv_results[model_b_cv_results["Selected"]].iloc[0]
    model_b_training_summary = pd.DataFrame(
        [
            {
                "Training rows": len(_X_train),
                "Study groups": study_groups.nunique(),
                "Raw predictors": len(model_predictors),
                "Best trees": model_b_grid_search.best_params_[
                    "model__n_estimators"
                ],
                "Best maximum depth": (
                    "unlimited"
                    if model_b_grid_search.best_params_["model__max_depth"]
                    is None
                    else model_b_grid_search.best_params_["model__max_depth"]
                ),
                "Best minimum leaf size": model_b_grid_search.best_params_[
                    "model__min_samples_leaf"
                ],
                "CV macro F1": round(_selected["CV macro F1"], 4),
                "CV mcl recall": round(_selected["CV mcl recall"], 4),
                "CV mcl precision": round(_selected["CV mcl precision"], 4),
            }
        ]
    )
    return model_b_best_estimator, model_b_cv_results, model_b_training_summary


@app.cell(hide_code=True)
def _(mo, model_b_cv_results, model_b_training_summary):
    mo.vstack(
        [
            mo.md("#### Model B training and tuning summary"),
            mo.ui.table(model_b_training_summary),
            mo.md("#### Randomized-search results"),
            mo.ui.table(model_b_cv_results.round(4)),
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
def _(mo):
    mo.md("""
    ### Held-out prediction and evaluation

    We score both tuned models on the same held-out studies and apply the
    success criteria fixed in Step 3. McMahon remains outside this scored
    comparison because its ∑TQ target is not directly comparable.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### Shared held-out evaluation

    The following results use the same scoring harness, test partition,
    class metrics, and success thresholds for both models.
    """)
    return


@app.cell(hide_code=True)
def _(mo, model_a_best_estimator, score_model, tapwater_test_df):
    model_a_held_out = score_model(
        model_a_best_estimator, tapwater_test_df, "Model A"
    )

    mo.vstack(
        [
            mo.md("#### Model A: held-out scoring"),
            mo.md(f"**{model_a_held_out['criteria']['summary_line']}**"),
            mo.ui.table(model_a_held_out["criteria"]["criteria"]),
            mo.md("#### Confusion matrix (held-out)"),
            mo.ui.table(model_a_held_out["metrics"]["confusion_matrix"]),
        ]
    )
    return (model_a_held_out,)


@app.cell(hide_code=True)
def _(
    error_breakdown_by_study,
    mo,
    model_a_held_out,
    plot_error_rate_by_study,
    tapwater_test_df,
):
    _model_a_error_breakdown = error_breakdown_by_study(
        model_a_held_out, tapwater_test_df
    )
    mo.vstack(
        [
            mo.md("#### Model A: held-out error rate by study"),
            mo.ui.table(_model_a_error_breakdown),
            plot_error_rate_by_study(_model_a_error_breakdown, "Model A"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, model_b_best_estimator, score_model, tapwater_test_df):
    model_b_held_out = score_model(
        model_b_best_estimator, tapwater_test_df, "Model B"
    )

    mo.vstack(
        [
            mo.md("#### Model B: held-out scoring"),
            mo.md(f"**{model_b_held_out['criteria']['summary_line']}**"),
            mo.ui.table(model_b_held_out["criteria"]["criteria"]),
            mo.md("#### Confusion matrix (held-out)"),
            mo.ui.table(model_b_held_out["metrics"]["confusion_matrix"]),
        ]
    )
    return (model_b_held_out,)


@app.cell(hide_code=True)
def _(
    error_breakdown_by_study,
    mo,
    model_b_held_out,
    plot_error_rate_by_study,
    tapwater_test_df,
):
    _model_b_error_breakdown = error_breakdown_by_study(
        model_b_held_out, tapwater_test_df
    )
    mo.vstack(
        [
            mo.md("#### Model B: held-out error rate by study"),
            mo.ui.table(_model_b_error_breakdown),
            plot_error_rate_by_study(_model_b_error_breakdown, "Model B"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md("""
        #### Model A class-weight diagnostic

        Model A's held-out collapse (predicts `within_reduced_monitoring`
        for all 46 sites; 0.0 recall on both `above_trigger` and
        `mcl_exceedance`) raised the question of whether the selected
        `class_weight="unweighted"` — which won on grouped-CV macro-F1
        among the training folds, per `model_a_cv_results` above — was
        the main cause. Tested by hand: same pipeline and `C` grid,
        `class_weight="balanced"` forced, refit on `tapwater_train_df`,
        scored on `tapwater_test_df` via `score_model()` (not part of
        the tracked Model A pipeline; a diagnostic only).

        | Metric | Unweighted (Model A) | Balanced |
        |---|---|---|
        | `mcl_exceedance` recall | 0.0000 | 0.0714 (1/14) |
        | `above_trigger` recall | 0.0000 | 0.1429 (1/7) |
        | Macro F1 | 0.2347 | 0.3368 |
        | `mcl_exceedance` precision | 0.0000 | 0.5000 (1/2) |
        | Non-majority-tier predictions | 0 of 46 | 7 of 46 |

        **Finding:** `"balanced"` measurably moves the model off pure
        majority-class collapse, but comes nowhere close to the 0.70
        recall floor (0.07, not 0.70) and only predicts a minority tier
        for 7 of 46 held-out sites. Class weighting was a real
        contributing factor, not the dominant one — the bigger story
        is a train/held-out generalization gap that a training-time
        hyperparameter alone doesn't fix. Worth keeping both threads
        in the benchmarking and deployment discussion: confirm
        `"balanced"` isn't dropped
        for Model B on a CV-macro-F1 technicality the way it was for
        Model A, but don't expect it to single-handedly clear the
        floor either.
        """),
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(
    build_model_comparison,
    mo,
    model_a_held_out,
    model_b_held_out,
    plot_model_comparison,
):
    _comparison_results = {
        "Model A": model_a_held_out,
        "Model B": model_b_held_out,
    }
    _comparison_df = build_model_comparison(_comparison_results)
    mo.vstack(
        [
            mo.md("#### Model comparison: Model A vs. Model B"),
            mo.ui.table(_comparison_df),
            plot_model_comparison(
                _comparison_df, "Model comparison vs. Step 3 thresholds"
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
                    (
                        "Per Check-In #2 peer feedback, does this section "
                        "stay lighter on detail and lead with results, "
                        "rather than listing every metric computed?"
                    ),
                    (
                        "Per that same feedback, can we quantify how "
                        "sparse the underlying site data is by state "
                        "(e.g. ~5 sites/state on average across the "
                        "bottom 15 states), and does that sparsity line "
                        "up with where either model's errors concentrate?"
                    ),
                    (
                        "For context only, not as a scored benchmark: how "
                        "does either model's `mcl_exceedance` recall/"
                        "precision compare to McMahon et al. (2022)'s own "
                        "boosted-regression-tree model (SI §S5: 0.96 "
                        "sensitivity, 0.72 specificity), given its target "
                        "(binary PFAS detection) and predictor set "
                        "(geochemistry-inclusive) both differ from ours?"
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
                        "Does the recommended model's main limitation — "
                        "interpretability vs. accuracy, or the land-use-"
                        "only predictor scope excluding the geochemical/"
                        "age-tracer signal McMahon et al. (2022) found "
                        "most predictive — change the deployment "
                        "recommendation itself?"
                    ),
                    (
                        "Per Check-In #2 peer feedback, does the "
                        "conclusion explicitly acknowledge that "
                        "state-level data sparsity limits how well the "
                        "benchmarking generalizes across geography, "
                        "rather than leaving that gap implicit?"
                    ),
                    (
                        "Given that gap, does the narrative recommend "
                        "narrowing the model's scope to a data-denser "
                        "subregion, or framing it as exploratory rather "
                        "than screening-ready — and which one does it "
                        "land on?"
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

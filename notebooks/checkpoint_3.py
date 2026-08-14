# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
#     "numpy",
#     "pandas>=3.0.3",
#     "scikit-learn",
#     "matplotlib>=3.9",
# ]
# ///

import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    # When this notebook is opened from a local checkout, checkpoint_2.py
    # sits right next to it. When marimo downloads it standalone from a
    # URL (e.g. `uvx marimo edit --sandbox <gh-pages-url>`), that sibling
    # file isn't there, so fetch it from the same repo location it was
    # published from and import it from a temp dir instead.
    try:
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
        _dest = f"{_tmp_dir}/checkpoint_2.py"
        _urllib_request.urlretrieve(f"{_RAW_BASE}/checkpoint_2.py", _dest)
        _sys.path.insert(0, _tmp_dir)

        from checkpoint_2 import app as checkpoint_2_app
    return checkpoint_2_app, mo


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
    ## Step 5: Model Execution, Evaluation & Deployment

    This notebook is the final report's deliverable: training and
    tuning the two models proposed in Step 4, evaluating them against
    the Step 3 plan, and discussing deployment feasibility. It carries
    forward the Step 3-4 report's study-grouped training/test partition —
    `tapwater_train_df` ({tapwater_train_df.shape[0]} rows) and
    `tapwater_test_df` ({tapwater_test_df.shape[0]} rows) — and its
    per-class metrics, risk-tier thresholds, and preprocessing pipeline.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Foundations carried into Step 5

    Two closeout items from earlier steps feed directly into Step 5's
    model training and are settled before it begins.

    #### Finalized classification pipeline

    The ∑TQ classification pipeline now resolves the two compounds with
    no benchmark in either source, PFPeS and PFPrS, and runs against the
    complete 716-sample Table S10 dataset rather than a partial extract,
    so the training and test partitions above reflect the full available
    sample.

    #### Verified source citations

    The state-agency primary sources behind Table S5's state-only
    benchmarks, and the CDM Smith EPA Final PFAS Regulations fact sheet
    URL cited in the methods section, are confirmed against their
    original publications.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Check-In #2 feedback integration

    Per the spec, the final submission must integrate at least one item
    from the peer feedback the team received on Check-In #2.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### Feedback selected for integration

    Peer review on Check-In #2 surfaced three items the team is
    integrating into this submission: keeping the results sections
    lighter on detail and leading with results; quantifying the
    underlying site-count sparsity (e.g. ~5 sites/state on average
    across the bottom 15 states) to acknowledge the geographic
    generalizability limit it creates; and a reviewer's doubt that a
    national-scope model is well matched to the available data,
    suggesting a single-state or regional analysis would control for
    landform and geography more precisely. All three are threaded
    into the benchmarking below and the deployment discussion's
    guiding questions and recommendation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Model Training & Execution

    Carries Step 4's two proposed models, the interpretable baseline
    (Model A) and the competing ensemble (Model B), from proposal into
    trained, tuned classifiers.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### Shared setup for Model A & Model B

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


@app.cell
def _(f1_score, precision_score, recall_score):
    # Shared CV metrics. Model A is selected by macro-F1 only; recall
    # and precision are retained as diagnostics for later evaluation.
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


@app.cell
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
    ##### Held-out scoring harness

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
    live here, next to `tier_model_scoring`, so the benchmarking
    section below can reuse them too.
    """)
    return


@app.cell
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


@app.cell
def _(pd):
    def error_breakdown_by_study(result, df):
        """Held-out error rate by `study_group`, for a score_model() result.

        Takes a score_model() result dict and the dataframe it was
        scored against, and reports whether errors concentrate in one
        held-out study or spread evenly. Model A and Model B both call
        this the same way.
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


@app.cell
def _(plt):
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
        return fig

    return (plot_error_rate_by_study,)


@app.cell
def _(pd):
    def build_model_comparison(results):
        """Model A vs. Model B comparison table from score_model() results.

        `results` is `{model_name: score_model() result}`; add a
        model by adding a dict entry, not by restructuring the table.
        Pulls recall on all three risk tiers, macro F1, mcl_exceedance
        precision, and the overall Step 3 pass/fail from each model's
        `check_success_criteria()`/`evaluate_tier_model()` output.
        """
        _rows = []
        for _name, _result in results.items():
            _criteria = _result["criteria"]["criteria"].set_index("Metric")[
                "Value"
            ]
            _pc = _result["metrics"]["per_class"]
            _rows.append(
                {
                    "Model": _name,
                    "within_reduced_monitoring recall": round(
                        _pc.loc["within_reduced_monitoring", "recall"], 2
                    ),
                    "above_trigger recall": round(
                        _pc.loc["above_trigger", "recall"], 2
                    ),
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


@app.cell
def _(
    MACRO_F1_FLOOR,
    MODEL_COMPARISON_PALETTE,
    PRECISION_FLOOR,
    RECALL_FLOOR,
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
        return fig

    return (plot_model_comparison,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### Baseline model A Implementation

    Model A is the multinomial logistic-regression baseline proposed in
    Step 4. It is trained only on `tapwater_train_df` using study-grouped
    cross-validation; the held-out test partition is not used here and
    remains untouched for held-out evaluation.

    Hyperparameter selection uses mean grouped-CV macro-F1 only. The CV
    recall and precision values for `mcl_exceedance` are retained as
    tuning diagnostics, not as the final Step 3 pass/fail decision. The
    held-out evaluation and benchmarking make that determination.

    This also uses an explicit predictor allowlist so raw PFAS
    concentrations, ∑TQ fields, identifiers, and study labels cannot
    accidentally enter the model.

    Because cross-validation is grouped by study, an entire
    `study_group` moves together into either the fitting or validation
    portion of a fold. A `State` or `Site Type` category concentrated in
    only one or two studies may therefore be absent from a fold's
    fitting data but appear in its validation data. We audit each fold
    for these unseen categories and use full one-hot encoding with
    `handle_unknown="ignore"` and `drop=None` so they can be handled
    safely.

    The current allowlisted predictors contain no missing values in the
    training partition, so both the numeric and categorical imputers
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

    # The candidate with the highest mean grouped-CV macro-F1 is
    # selected. High-risk recall/precision remain diagnostics only.
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

    # Split into two narrower tables rather than one 12-column row -
    # data counts on one side, selected hyperparameters/CV scores on
    # the other, so neither table risks cropping when printed.
    model_a_training_data_summary = pd.DataFrame(
        [
            {
                "Training rows": len(_X_train),
                "Study groups": study_groups.nunique(),
                "Raw predictors": len(model_predictors),
                "Encoded predictors": _encoded_count,
                "Missing predictor values": int(_X_train.isna().sum().sum()),
                "log1p predictors": _skewed_count,
            }
        ]
    )
    model_a_tuning_summary = pd.DataFrame(
        [
            {
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
        model_a_training_data_summary,
        model_a_tuning_summary,
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
    model_a_training_data_summary,
    model_a_tuning_summary,
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
            "the same as the dropped reference category. We therefore "
            "use full one-hot encoding (`drop=None`)."
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
            mo.md("##### Training data summary"),
            mo.ui.table(model_a_training_data_summary),
            mo.md("##### Selected hyperparameters & CV scores"),
            mo.ui.table(model_a_tuning_summary),
            mo.md(
                """
                ##### Tuning grid results

                The values below are mean cross-validation estimates from
                the grouped grid search. They describe how each
                hyperparameter setting performed across the training
                folds; they are not held-out test results for the final
                refit Model A.

                `Selected=True` identifies the hyperparameter setting
                with the highest mean grouped-CV macro-F1. The
                `mcl_exceedance` recall and precision values are retained
                as tuning diagnostics only and do not determine model
                selection. Final threshold evaluation is performed
                in the evaluation using the held-out studies.
                """
            ),
            mo.ui.table(model_a_cv_results.round(4)),
            mo.md("##### Unseen-category audit"),
            _unseen_view,
            mo.md("##### Largest coefficients for `mcl_exceedance`"),
            mo.ui.table(
                model_a_top_coefficients[
                    ["Feature", "Coefficient", "Direction"]
                ].round(4)
            ),
            mo.md("##### Expected-direction check"),
            mo.ui.table(model_a_direction_audit),
            mo.md(
                f"""
                ##### Findings summary

                Model A tuning is based on grouped-CV macro-F1 only.
                High-risk recall and precision remain visible as
                training-time diagnostics, while the authoritative
                threshold assessment is performed later on the
                held-out studies.

                {_unseen_text}

                The current training predictors have no missing
                values, so the numeric and categorical imputers are
                currently no-ops. They remain in the pipeline as
                defensive preprocessing for future data.

                The training implementation also showed that the earlier
                generic feature-selection approach could allow raw PFAS
                concentration or outcome-related fields into the model.
                We avoid this leakage by using an explicit allowlist of
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
    #### Model B: random forest

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

    # Split into two narrower tables rather than one 9-column row -
    # data counts on one side, selected hyperparameters/CV scores on
    # the other, so neither table risks cropping when printed.
    model_b_training_data_summary = pd.DataFrame(
        [
            {
                "Training rows": len(_X_train),
                "Study groups": study_groups.nunique(),
                "Raw predictors": len(model_predictors),
            }
        ]
    )
    model_b_tuning_summary = pd.DataFrame(
        [
            {
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
    return (
        model_b_best_estimator,
        model_b_cv_results,
        model_b_training_data_summary,
        model_b_tuning_summary,
    )


@app.cell(hide_code=True)
def _(
    mo,
    model_b_cv_results,
    model_b_training_data_summary,
    model_b_tuning_summary,
):
    mo.vstack(
        [
            mo.md("##### Model B training data summary"),
            mo.ui.table(model_b_training_data_summary),
            mo.md("##### Model B selected hyperparameters & CV scores"),
            mo.ui.table(model_b_tuning_summary),
            mo.md("##### Randomized-search results"),
            mo.ui.table(model_b_cv_results.round(4)),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Prediction, Evaluation & Benchmarking

    Scores both trained models against the held-out studies and Step
    3's success criteria.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### Run predictions & evaluate
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ##### Shared held-out evaluation

    The following results use the same scoring harness, test partition,
    class metrics, and success thresholds for both models.
    """)
    return


@app.cell
def _(mo, model_a_best_estimator, score_model, tapwater_test_df):
    model_a_held_out = score_model(
        model_a_best_estimator, tapwater_test_df, "Model A"
    )

    mo.vstack(
        [
            mo.md("##### Model A: held-out scoring"),
            mo.md(f"**{model_a_held_out['criteria']['summary_line']}**"),
            mo.ui.table(model_a_held_out["criteria"]["criteria"]),
            mo.md("##### Model A: confusion matrix (held-out)"),
            mo.ui.table(model_a_held_out["metrics"]["confusion_matrix"]),
        ]
    )
    return (model_a_held_out,)


@app.cell
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
            mo.md("##### Model A: held-out error rate by study"),
            mo.ui.table(_model_a_error_breakdown),
            plot_error_rate_by_study(_model_a_error_breakdown, "Model A"),
        ]
    )
    return


@app.cell
def _(mo, model_b_best_estimator, score_model, tapwater_test_df):
    model_b_held_out = score_model(
        model_b_best_estimator, tapwater_test_df, "Model B"
    )

    mo.vstack(
        [
            mo.md("##### Model B: held-out scoring"),
            mo.md(f"**{model_b_held_out['criteria']['summary_line']}**"),
            mo.ui.table(model_b_held_out["criteria"]["criteria"]),
            mo.md("##### Model B: confusion matrix (held-out)"),
            mo.ui.table(model_b_held_out["metrics"]["confusion_matrix"]),
        ]
    )
    return (model_b_held_out,)


@app.cell
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
            mo.md("##### Model B: held-out error rate by study"),
            mo.ui.table(_model_b_error_breakdown),
            plot_error_rate_by_study(_model_b_error_breakdown, "Model B"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md("""
        **Class-weight diagnostic (both models)**

        Both models' selected hyperparameters trained unweighted: Model A
        won grouped-CV macro-F1 with `class_weight="unweighted"`
        (`model_a_cv_results` above), and Model B's randomized search
        never included `class_weight` as a tuning axis, so it trained
        unweighted by default. We tested whether forcing
        `class_weight="balanced"` on each model's exact selected
        hyperparameters, refit on `tapwater_train_df` and scored on
        `tapwater_test_df` via `score_model()`, would meaningfully change
        the held-out result (diagnostic only, not part of either tracked
        pipeline).

        | Metric | A unweighted | A balanced | B unweighted | B balanced |
        |---|---|---|---|---|
        | `mcl_exceedance` recall | 0.0000 | 0.0714 | 0.0714 | 0.1429 |
        | `mcl_exceedance` precision | 0.0000 | 0.5000 | 1.0000 | 0.2857 |
        | Macro F1 | 0.2347 | 0.3368 | 0.2825 | 0.2718 |

        **Finding:** `"balanced"` measurably moves both models off pure
        majority-class collapse, but neither comes close to the 0.70
        recall floor, and for Model B it trades away the
        `mcl_exceedance` precision floor it currently (fragile, on a
        single correct prediction) passes. Class weighting is a real
        contributing factor, not the dominant one. The bigger story,
        covered below, is a train/held-out generalization gap that a
        training-time hyperparameter alone doesn't fix.
        """),
        kind="info",
    )
    return


@app.cell
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
    comparison_df = build_model_comparison(_comparison_results)
    mo.vstack(
        [
            mo.md("##### Model comparison: Model A vs. Model B"),
            # Show only the headline columns here - comparison_df also
            # carries all-three-tier recall for the benchmarking table
            # below, but this table stays narrow enough to print cleanly.
            mo.ui.table(
                comparison_df[
                    [
                        "Model",
                        "mcl_exceedance recall",
                        "Macro F1",
                        "mcl_exceedance precision",
                        "Meets all Step 3 criteria",
                    ]
                ]
            ),
            plot_model_comparison(
                comparison_df, "Model comparison vs. Step 3 thresholds"
            ),
        ]
    )
    return (comparison_df,)


@app.cell(hide_code=True)
def _(RECALL_FLOOR, comparison_df, mo, model_a_cv_results, model_b_cv_results):
    _by_model = comparison_df.set_index("Model")
    _a_recall = _by_model.loc["Model A", "mcl_exceedance recall"]
    _b_recall = _by_model.loc["Model B", "mcl_exceedance recall"]
    _b_precision = _by_model.loc["Model B", "mcl_exceedance precision"]
    _a_cv_recall_max = model_a_cv_results["CV mcl recall"].max()
    _b_cv_recall_max = model_b_cv_results["CV mcl recall"].max()
    _best_cv_recall = max(_a_cv_recall_max, _b_cv_recall_max)

    mo.md(f"""
    ##### Does either model clear the bar?

    No. Model A's held-out `mcl_exceedance` recall is {_a_recall:.4f}
    (0 of 14 high-risk sites caught); Model B's is {_b_recall:.4f} (1
    of 14). Both fall far short of the {RECALL_FLOOR:.2f} floor Step 3
    set as the binding constraint on model selection, not a soft
    target. Model B's {_b_precision:.4f} `mcl_exceedance` precision
    looks perfect in the table above, but it reflects a single correct
    positive prediction out of 46 held-out sites. One flipped
    prediction would erase it, so it should not be read as a reliable
    pattern.

    This is not a surprise the held-out set alone produced: both
    models' cross-validated `mcl_exceedance` recall during tuning
    topped out at {_a_cv_recall_max:.4f} (Model A's grid) and
    {_b_cv_recall_max:.4f} (Model B's grid), already well below the
    floor before either model saw a held-out study. Two disclosures,
    neither of which changes this conclusion: hyperparameters were
    selected by macro-F1 alone rather than the two-stage
    recall-floor-then-macro-F1 rule Step 3 and Step 4 describe (the
    best CV recall across both grids, {_best_cv_recall:.4f}, still
    misses the floor, so the outcome would not change); and the
    class-weight gap between plan and implementation covered in the
    diagnostic above also does not close it.

    ##### Where the errors concentrate

    Held-out errors are not spread evenly across the three test
    studies, and they track each study's actual risk composition more
    than the study identity itself. Cape Cod's test sites are
    overwhelmingly high-risk (9 of 13 `mcl_exceedance`, 3
    `above_trigger`), and both models miss almost all of them: a
    0.9231 error rate for Model A, 0.8462 for Model B. Minnesota, with
    a mixed composition, sits at 0.3333 for both. Northeast Iowa shows
    0.0000 error for both models, but trivially — every one of its 6
    held-out sites is already `within_reduced_monitoring`, so a model
    that always predicts the majority tier gets Iowa right without
    distinguishing any risk at all. The pattern reads as "both models
    default to the majority tier, and error rate by study is just how
    far each study's true composition diverges from that default,"
    not as a geography-specific failure.

    ##### Does this change the Step 4 recommendation?

    No — if anything it confirms Step 4's own tie-breaker. Step 4
    proposed keeping Model A unless Model B "meaningfully" outperformed
    it, since the ensemble costs direct coefficient interpretability.
    Model B's gain over Model A amounts to one additional correctly
    classified site out of 46, which does not meet that bar. Neither
    model meets Step 3's success criteria, so this is not a
    "which model wins" result. Both fail the same floor, which the
    benchmarking below addresses directly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Model validation & benchmarking

    We check that held-out result against a fairer baseline and a
    fuller picture: recall across all three risk tiers rather than
    just the highest-risk one, a majority baseline recomputed on the
    same 46-site partition rather than Step 3's original 236-site
    figure, and — per Check-In #2 feedback — how sparse the underlying
    site data actually is, set against where each model's errors
    concentrate by held-out study.

    For context only, not as a scored benchmark — its binary target
    and geochemistry-inclusive predictor set aren't directly
    comparable — McMahon et al. (2022)'s own model reaches 0.96
    sensitivity and 0.72 specificity (SI §S5).
    """)
    return


@app.cell
def _(comparison_df, mo, pd, tapwater_test_df, tapwater_train_df):
    # Majority baseline, computed correctly: on the SAME 46-site test
    # partition scored above, not Step 3's 236-site ss_scored_df.
    _majority_share = (
        tapwater_test_df["pfas_risk_tier"] == "within_reduced_monitoring"
    ).mean()
    majority_baseline_macro_f1 = round(
        2 * _majority_share / (3 * (1 + _majority_share)), 4
    )

    # Add the corrected baseline to the same per-tier recall columns
    # already built into comparison_df above, rather than re-deriving
    # each model's recall from its held-out result a second time.
    all_tier_recall_comparison_df = pd.concat(
        [
            pd.DataFrame([{
                "Model": (
                    "Majority baseline (always guesses "
                    "within_reduced_monitoring)"
                ),
                "within_reduced_monitoring recall": 1.0,
                "above_trigger recall": 0.0,
                "mcl_exceedance recall": 0.0,
                "Macro F1": majority_baseline_macro_f1,
            }]),
            comparison_df[
                [
                    "Model",
                    "within_reduced_monitoring recall",
                    "above_trigger recall",
                    "mcl_exceedance recall",
                    "Macro F1",
                ]
            ],
        ],
        ignore_index=True,
    )

    # Compute the real site-sparsity-by-state figure, replacing the
    # Check-In #2 placeholder estimate with an actual number.
    _sites_per_state = pd.concat(
        [tapwater_train_df["State"], tapwater_test_df["State"]]
    ).value_counts().sort_values()
    bottom_15_avg_sites = round(_sites_per_state.head(15).mean(), 1)
    sparsest_states = _sites_per_state.head(15)

    # Broader coverage figures for the deployment discussion's
    # data-scaling argument, off the same combined State column.
    total_site_count = int(_sites_per_state.sum())
    represented_state_count = int(_sites_per_state.shape[0])
    singleton_state_count = int((_sites_per_state == 1).sum())
    top3_state_share = round(
        _sites_per_state.tail(3).sum() / total_site_count, 4
    )

    mo.vstack([
        mo.md("##### Model comparison, all three risk tiers"),
        mo.ui.table(all_tier_recall_comparison_df),
        mo.md(
            f"15 sparsest states average "
            f"**{bottom_15_avg_sites} sites each**."
        ),
        mo.ui.table(
            sparsest_states.reset_index().rename(
                columns={"index": "state", "State": "sites"}
            )
        ),
        mo.md(
            "Against the corrected, same-partition baseline, Model A "
            "is statistically indistinguishable from it (identical "
            f"{majority_baseline_macro_f1} macro F1) - it predicts the "
            "majority tier for every held-out site. Model B moves "
            "slightly off that default but still misses every "
            "`above_trigger` site. State-level sparsity alone doesn't "
            "explain the gap: per the error-rate-by-study breakdown "
            "above, it lines up instead with each held-out study's "
            "true risk-tier mix."
        ),
        mo.md(
            f"Zooming out from the 15 sparsest states: our "
            f"{total_site_count} combined training and held-out sites "
            f"are spread across only {represented_state_count} states "
            f"and territories, {singleton_state_count} of them "
            f"represented by a single site, while the three "
            f"best-covered states alone (Illinois, Minnesota, "
            f"California) account for {top3_state_share:.1%} of every "
            "site we have. That skew, not model tuning, is the "
            "binding constraint on geographic generalization — see "
            "the deployment discussion below."
        ),
    ])
    return (
        represented_state_count,
        singleton_state_count,
        top3_state_share,
        total_site_count,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Deployment Discussion
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### Deployment feasibility

    Neither model is ready for operational deployment. On the held-out
    studies, both models failed our prespecified recall threshold for the
    `mcl_exceedance` tier and predominantly predicted the majority risk
    tier. In practice, this failure could cause water-resource operators
    to deprioritize sites that actually require confirmatory sampling—the
    outcome our recall threshold was specifically designed to prevent.

    We would retain Model A as the more suitable prototype for further
    development, but we do not recommend deploying it in its current form.
    Model B correctly classified only one additional site among the 46
    held-out observations, which is not enough improvement to justify its
    additional complexity and reduced interpretability. Model A's relative
    simplicity would make its behavior easier to inspect as we improve the
    data and modeling pipeline. This is a development preference, not
    evidence that Model A is presently safe for operational screening.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### Requirements for future operational use

    An operator would need more than a trained model to use this approach
    responsibly. Deployment would require a stable process for collecting
    the same land-use and potential PFAS-source predictors used during
    training, periodically refreshing those inputs, and retraining the
    model as new PFAS measurements become available. A water-quality
    specialist would also need to review predictions and determine which
    sites receive confirmatory testing.

    Until the model demonstrates reliable high-risk recall on unseen
    regions, its predictions should not be used to exclude sites from
    sampling. A future system could instead use predictions as one source
    of exploratory information alongside regulatory measurements, local
    knowledge, known PFAS sources, and existing monitoring priorities.
    Operators—not the model—would retain responsibility for final sampling
    decisions.
    """)
    return


@app.cell(hide_code=True)
def _(
    mo,
    represented_state_count,
    singleton_state_count,
    top3_state_share,
    total_site_count,
):
    mo.md(f"""
    #### Pitfalls and lessons learned

    The main lesson from this project is that validation performance
    within the available studies did not translate reliably to unseen
    studies. During grouped cross-validation, the best
    `mcl_exceedance` recall ranged from 0.41 to 0.52, but it fell to
    0.00-0.07 across the held-out studies. The training data contained
    only 190 sites across seven study groups, so even grouped
    cross-validation provided limited evidence about how the models
    would generalize to new populations.

    Sparse and uneven geographic coverage compounds that limitation.
    Our {total_site_count} combined training and held-out sites are
    spread across only {represented_state_count} states and
    territories, {singleton_state_count} of them represented by a
    single site, and the three best-covered states alone account for
    {top3_state_share:.1%} of every site we have. The held-out errors
    appeared to follow differences in each study's risk-tier
    composition rather than geography alone, but with coverage this
    thin we cannot separate geographic effects from study design and
    class composition with any confidence. Closing that gap is a
    data-collection problem before it is a modeling one: the next
    step is scaling up site sampling in the underrepresented states,
    not further tuning against the sites we already have.

    A second limitation is predictor scope. Our models use land-use
    and potential PFAS-source variables, whereas McMahon et al. (2022)
    found important predictive value in geochemical and
    groundwater-age variables for a different PFAS-detection target.
    Because the targets and predictor sets differ, their reported
    performance is not a directly comparable benchmark. Their top
    five predictors were tritium concentration, distance to the
    nearest fire-training area, dissolved organic carbon (DOC),
    percentage of urban land use, and summed volatile organic
    compound (VOC) concentration - three of five are chemical
    measurements we do not currently model. DOC
    and VOC look like the more feasible additions of the three: both
    are measured with standard water-quality lab methods, whereas
    McMahon et al. note that tritium is "rarely collected in
    assessments of PFAS contamination of groundwater" because it
    requires specialized isotope-lab analysis. We have not yet
    confirmed whether a source comparable to Seawolf reports DOC or
    VOC for our training sites, so this is a candidate for the next
    data-scoping pass, not a confirmed plan.
    """)
    return


@app.cell(hide_code=True)
def _(mo, represented_state_count, singleton_state_count, total_site_count):
    mo.md(f"""
    #### Recommendation

    We recommend treating the current model as an exploratory research
    prototype rather than a screening-ready tool. The next development
    cycle should prioritize: scaling up site sampling, since our
    {total_site_count}-site, {represented_state_count}-state footprint
    (including {singleton_state_count} single-site states) is too
    sparse to support a national model; incorporating additional
    scientifically supported predictors, such as McMahon et al.
    (2022)'s DOC and VOC measurements; and evaluating the revised
    model on entirely unseen regions or utilities. We should
    reconsider deployment only after the model consistently meets the
    high-risk recall threshold under that external validation.

    Check-In #2 peer review separately questioned whether a project
    this broad is well scoped for the data available, suggesting a
    single-state or regional analysis would let us control for
    landform and geography more precisely and remove confounding
    variables a national model has to absorb. McMahon et al. (2022)
    took exactly that narrower approach - five aquifer systems in the
    eastern United States rather than a national sample - and their
    model reached 0.96 sensitivity and 0.72 specificity, well above
    what either of our national models produced even during
    cross-validation. That comparison is not a controlled test of
    regional scope (different targets and predictor sets, as noted
    above), but it is consistent with the feedback, so we now weigh a
    regional pilot as a stronger next step than our earlier framing
    credited it as. It would still need its own representative
    training data, held-out evaluation, human-review procedure, and
    performance-monitoring plan - narrowing scope does not remove
    those requirements, it only makes them easier to satisfy with the
    data we can realistically collect.
    """)
    return


if __name__ == "__main__":
    app.run()

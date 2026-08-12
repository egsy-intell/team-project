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

__generated_with = "0.23.16"
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
def _():
    # Shared third-party imports for this notebook, defined once so
    # downstream cells take them as parameters instead of each
    # re-importing numpy/pandas/sklearn locally.
    import warnings

    import numpy as np
    import pandas as pd
    from sklearn.base import BaseEstimator, TransformerMixin
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import f1_score, precision_score, recall_score
    from sklearn.model_selection import GridSearchCV, StratifiedGroupKFold
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    return (
        BaseEstimator,
        ColumnTransformer,
        GridSearchCV,
        LogisticRegression,
        OneHotEncoder,
        Pipeline,
        SimpleImputer,
        StandardScaler,
        StratifiedGroupKFold,
        TransformerMixin,
        f1_score,
        np,
        pd,
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

    Per the Step 4 proposals, Model B (T6) reuses Model A's approved
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
def _(mo):
    mo.md("""
    ### Baseline model A Implementation

    Model A is the multinomial logistic-regression baseline proposed in
    Step 4. It is trained only on `tapwater_train_df` using study-grouped
    cross-validation; the held-out test partition is not used here and
    remains untouched for T7.

    Hyperparameter selection in T5 uses mean grouped-CV macro-F1 only.
    The CV recall and precision values for `mcl_exceedance` are retained
    as tuning diagnostics, not as the final Step 3 pass/fail decision.
    T7 and T9 will make that determination on the held-out studies.

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
            self.feature_names_in_ = np.asarray(
                _frame.columns, dtype=object
            )
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

    _cv = model_a_grid_search.cv_results_
    model_a_cv_results = pd.DataFrame(
        {
            "C": _cv["param_model__C"],
            "Class weight": [
                "unweighted" if x is None else str(x)
                for x in _cv["param_model__class_weight"]
            ],
            "CV macro F1": _cv["mean_test_macro_f1"],
            "CV mcl recall": _cv["mean_test_mcl_recall"],
            "CV mcl precision": _cv["mean_test_mcl_precision"],
        }
    )
    model_a_cv_results["Selected"] = False
    model_a_cv_results.loc[
        model_a_grid_search.best_index_, "Selected"
    ] = True
    model_a_cv_results = model_a_cv_results.sort_values(
        ["Selected", "CV macro F1"],
        ascending=[False, False],
    ).reset_index(drop=True)

    _pre = model_a_best_estimator.named_steps["preprocessor"]
    _model = model_a_best_estimator.named_steps["model"]
    _encoded_count = len(_pre.get_feature_names_out())
    _skewed_count = len(
        _pre.named_transformers_["num"]
        .named_steps["skew_log1p"]
        .skewed_features_
    )

    _selected = model_a_cv_results[
        model_a_cv_results["Selected"]
    ].iloc[0]

    model_a_training_summary = pd.DataFrame(
        [
            {
                "Training rows": len(_X_train),
                "Study groups": study_groups.nunique(),
                "Raw predictors": len(model_predictors),
                "Encoded predictors": _encoded_count,
                "Missing predictor values": int(
                    _X_train.isna().sum().sum()
                ),
                "log1p predictors": _skewed_count,
                "Best C": model_a_grid_search.best_params_["model__C"],
                "Best class weight": (
                    "unweighted"
                    if model_a_grid_search.best_params_[
                        "model__class_weight"
                    ]
                    is None
                    else model_a_grid_search.best_params_[
                        "model__class_weight"
                    ]
                ),
                "CV macro F1": round(_selected["CV macro F1"], 4),
                "CV mcl recall": round(_selected["CV mcl recall"], 4),
                "CV mcl precision": round(
                    _selected["CV mcl precision"], 4
                ),
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
        _row = _coef_df[
            _coef_df["Feature"] == f"num__{_feature}"
        ]
        if _row.empty:
            continue

        _value = float(_row.iloc[0]["Coefficient"])
        _observed = (
            "positive"
            if _value > 0
            else "negative"
            if _value < 0
            else "zero"
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
        _counter = model_a_direction_audit[
            ~model_a_direction_audit["Matches"]
        ]
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
                in T7/T9 using the held-out studies.
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
                threshold assessment is deferred to T7/T9 on the
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
                    "same training partition, grouped cross-validation, "
                    "and grid-search tuning approach as Model A (T5) so "
                    "Model B enters T7 already tuned rather than "
                    "deferring tuning to the evaluation step."
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
            mo.md("### Run predictions & evaluate"),
            task_callout(
                "T7",
                category="Step 5 - Evaluation",
                lead="Yai, Somyaranjan",
                depends_on="T5, T6",
                summary=(
                    "Score both already-tuned models on the held-out "
                    "test set and evaluate against Step 3's success "
                    "criteria. Run as a joint execution, pairing "
                    "directly through the step."
                ),
                guiding_questions=[
                    (
                        "Does either model clear the 0.70 recall floor on "
                        "`mcl_exceedance` from Step 3, and if neither does, "
                        "what does that imply for the T9 benchmarking "
                        "narrative and T10's deployment recommendation?"
                    ),
                    (
                        "Are the errors concentrated in one held-out study "
                        "or spread evenly across the test partition, and "
                        "does that change which model looks preferable? "
                        "(McMahon stays out of this scoring entirely — "
                        "its incomparable ∑TQ target keeps it a narrative "
                        "reference for T9/T10, not a held-out study here.)"
                    ),
                    (
                        "Does the held-out comparison between Model A and "
                        "Model B change which one the team recommends, "
                        "relative to the Step 4 prediction?"
                    ),
                ],
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### T7 prep work (unblocked ahead of T6)

    T7 itself is still blocked on T6 (Model B), but the pieces
    below only need Model A and can be dry-run against it now, so
    finishing T7 once T6 lands is mostly plugging Model B in
    rather than starting from scratch.
    """)
    return


@app.cell
def _():
    # T7 prep: a score_model(pipeline, df) helper that scores a fitted
    # pipeline against tapwater_test_df, reusing the same
    # tier_model_scoring functions T5 already defined for CV (macro
    # F1, mcl_exceedance recall/precision). Model A can exercise this
    # today; Model B just calls the same helper once T6 lands.
    #
    # Conversation starter: should this live next to `tier_model_scoring`
    # in the shared-setup section instead, so T9 can reuse it too
    # rather than duplicating a second scoring helper there?
    return


@app.cell
def _():
    # T7 prep: apply Step 3's 0.70 recall floor on `mcl_exceedance` to
    # Model A's held-out predictions, once the scoring harness above
    # exists. Model A alone can't answer T7's guiding question ("does
    # *either* model clear it"), but it tells us where Model A stands
    # ahead of Model B landing.
    #
    # Conversation starter: if Model A misses the floor on its own, is
    # that worth flagging to Emir before T6 wraps, in case it changes
    # what Model B's tuning should prioritize?
    return


@app.cell
def _():
    # T7 prep: break down Model A's held-out errors by `study_group`
    # to see whether they concentrate in one held-out study or spread
    # evenly (T7's second guiding question). Reuses the same
    # `study_group` values T5's grouped CV already keys on.
    #
    # Conversation starter: is a table enough given how few held-out
    # studies there are, or does this warrant a small bar plot of
    # error rate by study?
    return


@app.cell
def _():
    # T7 prep: comparison-table skeleton for Model A vs. Model B
    # (macro F1, mcl_exceedance recall/precision, per-study error
    # rate). Model A's row can be filled in now from the cells above;
    # Model B's row stays blank until T6 lands, so finishing this is a
    # drop-in, not a rewrite.
    #
    # Conversation starter: same columns as T9's benchmarking table,
    # or does T9 need more (majority-baseline column, per-tier recall
    # beyond mcl_exceedance)?
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

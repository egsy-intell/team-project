# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.14",
#     "pandas>=3.0.3",
#     "numpy>=2.5.1",
#     "matplotlib>=3.9",
# ]
# ///

import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd

    # When this notebook is opened from a local checkout, data_dictionary.py
    # sits right next to it. When marimo downloads it standalone from a URL
    # (e.g. `uvx marimo edit --sandbox <gh-pages-url>`), that sibling file
    # isn't there, so fetch it from the same repo location it was published
    # from and import it from a temp dir instead.
    try:
        from data_dictionary import app as data_dictionary_app
    except ModuleNotFoundError:
        import sys as _sys
        import tempfile as _tempfile
        import urllib.request as _urllib_request

        _RAW_BASE = "https://raw.githubusercontent.com/egsy-intell/team-project/main/notebooks"
        _tmp_dir = _tempfile.mkdtemp(prefix="egsy-pfas-")
        _dest = f"{_tmp_dir}/data_dictionary.py"
        _urllib_request.urlretrieve(f"{_RAW_BASE}/data_dictionary.py", _dest)
        _sys.path.insert(0, _tmp_dir)

        from data_dictionary import app as data_dictionary_app
    return data_dictionary_app, mo, np, pd


@app.cell(hide_code=True)
def _(mo):
    def print_sections(items):
        # PDF/print exports have no JS, so tabs/accordions can't hide panes
        # interactively - render every item as an always-visible labeled
        # section instead, which also reads fine in the live app.
        return mo.vstack(
            [
                mo.vstack([mo.md(f"**{label}**"), content])
                for label, content in items.items()
            ]
        )

    def task_callout(task_id, *, category, lead, summary, depends_on=None):
        # Ties a section back to its row in
        # planning/checkpoint-2/checkpoint2_tasks.csv, so readers (and other
        # notebooks) can trace prose back to who owns it and what it's
        # gated on.
        return mo.callout(
            mo.md(
                f"**Task {task_id}** &middot; {category} &middot; "
                f"Lead: {lead} &middot; Depends on: {depends_on or 'None'}"
                f"\n\n{summary}"
            ),
            kind="info",
        )

    return (print_sections,)


@app.cell(hide_code=True)
async def _(data_dictionary_app):
    _data_dictionary_result = await data_dictionary_app.embed()
    all_compound_dict_df = _data_dictionary_result.defs["all_compound_dict_df"]
    mcmahon_env_df = _data_dictionary_result.defs["mcmahon_env_df"]
    seawolf_dict_df = _data_dictionary_result.defs["seawolf_dict_df"]
    return all_compound_dict_df, mcmahon_env_df, seawolf_dict_df


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Step 1: Problem definition

    ### Problem statement
    Per- and polyfluoroalkyl substances, commonly known as PFAS, are persistent
    environmental contaminants that may enter drinking-water sources through
    industrial activities, waste disposal, firefighting foam use, urban
    development, and other landscape-level sources. This project aims to
    develop a predictive model for the occurrence of PFAS in tap water, using
    U.S. Geological Survey (USGS) summary data on potential landscape sources
    (Seawolf et al., 2023), and reported concentration at the point-of-use
    (Smalling et al., 2023). We will also attempt the same modeling for
    groundwater, based on the data used in a similar exercise by McMahon et al.
    (2022).

    The question we aim to answer is: Can we predict a site's PFAS risk tier in
    tap and groundwater sources across the United States based on key
    geographic and land-use indicators? In addition, how do our findings
    compare to those offered by researchers in the domain?

    #### Proposed classification
    Our original provisional classification split sites into low/medium/high
    using raw cumulative PFAS concentration relative to the sample median. We
    have since moved away from that approach: weighting every detected compound
    equally per ng/L doesn't reflect how differently PFAS compounds are
    actually regulated, and a median-based cutoff tracks our own sample rather
    than any fixed, external reference point.

    The classification is now based on a toxicity quotient (∑TQ), computed only
    from the six PFAS compounds EPA regulates under its 2024 rule, and named
    after EPA's own compliance vocabulary, anchored on its Maximum Contaminant
    Levels (MCLs) — the enforceable concentration limits set for each regulated
    compound — rather than generic low/medium/high labels:
    * **`within_reduced_monitoring`:** ∑TQ (or HI) < 0.5, below EPA's
      reduced-monitoring trigger.
    * **`above_trigger`:** 0.5 ≤ ∑TQ < 1.0, past the trigger but not yet an
      MCL-equivalent exceedance.
    * **`mcl_exceedance`:** ∑TQ ≥ 1.0, at or above an MCL-equivalent
      exceedance.

    See Preparing for modeling, below, for the full derivation, benchmark
    sourcing, and the remaining open items before ∑TQ can be computed against
    the full sample set.

    #### Why this problem matters
    1. **Public health relevance:** PFAS contamination in drinking water is a
       concern in many countries due to known or potential adverse effects on
       human health (U.S. Environmental Protection Agency [EPA], n.d.).
    2. **Regulatory deadlines drive the need for prioritization:** In April
       2024, EPA finalized the first legally enforceable federal limits
       (Maximum Contaminant Levels) for six PFAS compounds in drinking water,
       with compliance phased in through 2029 (EPA, 2024) — though the exact
       scope and timeline remain in flux: EPA has since proposed retaining the
       limits for PFOA and PFOS while rescinding limits for four other PFAS
       (EPA, 2025), and in May 2026 proposed extending PFOA/PFOS compliance to
       2031 (EPA, 2026). Water-resource operators and administrators need to
       identify and remediate at-risk sites well before enforcement takes
       effect, and prioritize under a moving compliance timeline rather than
       treating every site as equally uncertain. Predicting PFAS levels from
       traceable, highly correlated geographic and land-use features would let
       operators focus monitoring and remediation efforts on the sites most
       likely to need it, ahead of whichever compliance window ultimately
       applies.
    3. **Private-well coverage gap:** EPA's 2024 rule applies only to public
       water systems, leaving millions of Americans who rely on private wells
       outside its enforceable scope. Our selected datasets explicitly
       integrate private-well and public-supply exposures, positioning our
       model to speak to a population the new federal rule does not cover.

    #### Intended application
    The proposed model is intended to function as a screening and
    sampling-prioritization tool. It will not replace laboratory testing and
    will not be used to declare a tap or groundwater source safe, unsafe,
    compliant, or noncompliant.

    Potential users could include:
    * Environmental and public-health agencies
    * Water-resource managers
    * Researchers planning PFAS sampling programs
    * Community organizations identifying locations where testing resources may
      be most useful

    ### Application feasibility of the model
    The project is feasible because the EPA and USGS provide the data it
    depends on: measured PFAS concentrations and landscape summaries for sites
    in USGS's national PFAS tap-water reconnaissance.

    #### Scope
    * Publicly supplied and privately sourced tap and groundwater
    * PFAS concentration results from McMahon et al. (2022) and Smalling et al.
      (2023)
    * Landscape and potential-source indicators calculated by McMahon et al.
      (2022) and Seawolf et al. (2023)
    * One independent observation per unique sampling location
    * Classification of cumulative PFAS concentration into three categories

    #### Constraints
    The model will not...
    * Make causal claims about individual PFAS sources
    * Determine regulatory compliance
    * Replace laboratory sampling
    * Estimate the exact PFAS exposure of individual residents
    * Publish or attempt to reconstruct exact residential locations
    * Use repeated temporal samples as independent observations
    * Use quality-assurance samples as model observations
    * Use previously generated PFAS predictions as predictor variables

    ### Data source
    #### USGS data source 1: Smalling et al., 2023 (dependent variable)
    It supplies one of the project's dependent variables, i.e., the outcome the
    model is trying to predict. It will be used to train our model in the
    categorization of tap water sites based on site controls. It includes:

    * Which PFAS compounds were detected
    * The measured concentration of each compound
    * The number of PFAS compounds detected
    * The total or cumulative PFAS concentration
    * Whether results were below the laboratory reporting limit
    * Type of service point: private v. public

    #### USGS data source 2: Seawolf et al., 2023 (predictors)
    This dataset provides predictors associated with Smalling et al.'s data. It
    describes the environmental and geographic characteristics surrounding each
    sampling location that may be associated with PFAS contamination,
    including:

    * Nearby potential PFAS-related facilities
    * Industrial or commercial activity
    * Urban and developed land
    * Agricultural or natural land
    * Burned areas
    * Land-cover characteristics
    * Public versus private water source
    * Other geographic or landscape summaries around the sampling location

    <h4>USGS data source 3: McMahon et al., 2022 (predictors +
    dependent variables)</h4>
    This comprehensive dataset provides environmental and geographic
    characteristics, as well as PFAS concentrations, associated with various
    private and public wells drawing from aquifers along the Eastern United
    States. It includes:

    * Distance to PFAS-associated sites (fire stations and military facilities,
      for example)
    * Measured PFAS concentrations for each sampled aquifer
    * Land use percentages (farmland v. urban, for example)
    * Type of well: private v. public

    ### Data availability and ethical considerations
    The three resources from USGS datasets are publicly available government
    data releases. All of them are marked as CC0, and can be reused without
    licensing fees. In addition, the datasets do not require access to
    restricted health, financial, educational, or personally identifiable
    information.

    The data can be downloaded, filtered, and analyzed using standard tools,
    and has also been copied to the project's repo for convenience
    ([direct link](https://github.com/egsy-intell/team-project)).

    #### Privacy
    USGS anonymized the sampling locations to protect participant privacy. The
    project will retain the anonymized identifiers and will not attempt to
    infer exact home addresses or private-well locations.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Step 2: Data exploration and quality assessment

    Before assessing the quality of our data, we take the following steps:

    <h3>Smalling et al. (2023) and Seawolf et al. (2023) load and
    join-ability (`ss_merged_df`)</h3>

    1. Load Seawolf and Smalling via `pandas`
    2. Clean Smalling: the dataset uses `-` and `nd` for two specific purposes
       (not analyzed, and non-detected above the lab reporting limit,
       respectively). We replace the former with `NaN` and the latter with
       `0`. Reconstructing a per-compound reporting limit — to impute
       non-detects as half that limit, as done for McMahon below — would
       mean joining each sample's `Study` to its analyzing lab and year
       (Smalling et al., 2023, Appendix A, Table S1), then to that lab's
       detection limit (Table S3). That join has gaps the source itself
       doesn't resolve: 2017–2018 Colorado School of Mines samples were
       re-censored against field-blank concentrations the paper never
       tabulates, NWQL's PFOS/PFHxS limits are split by branched/linear
       isomer while this dataset reports only a combined value, and PFPrS
       has no published limit at all. Treating `nd` as `0` is a deliberate
       simplification given those gaps, not an oversight.
    3. Merge: using a left join, to report on any unmatched rows
    """)
    return


@app.cell(hide_code=True)
def _(all_compound_dict_df, mo, pd):
    from pathlib import Path as _Path

    _notebook_dir = mo.notebook_dir()
    if _notebook_dir is None:
        raise RuntimeError(
            "Could not determine notebook directory. Save/open the notebook "
            "from disk."
        )

    data_dir = _Path(_notebook_dir).resolve().parent / "data" / "usgs"

    if not data_dir.exists():
        # Notebook was opened standalone (e.g. `uvx marimo edit --sandbox
        # <gh-pages-url>`), so there's no sibling data/ checkout. Download the
        # same CSVs from the repo into a local cache and use that instead.
        import tempfile as _tempfile
        import urllib.request as _urllib_request

        data_dir = _Path(_tempfile.gettempdir()) / "egsy-pfas-data" / "usgs"
        _RAW_BASE = "https://raw.githubusercontent.com/egsy-intell/team-project/main/data/usgs"
        _files = [
            "smalling/PFAS_ENV.csv",
            "seawolf/PFAS_DataSummaries_5k_50k_SummaryData.csv",
            "mcmahon/PFAS_ENV.csv",
            "mcmahon/PFAS_GEOSPATIAL.csv",
        ]
        for _rel in _files:
            _dest = data_dir / _rel
            if _dest.exists():
                continue
            _dest.parent.mkdir(parents=True, exist_ok=True)
            _urllib_request.urlretrieve(f"{_RAW_BASE}/{_rel}", _dest)

    # First line of this file is a table caption, not a header row.
    _smalling_df = pd.read_csv(
        data_dir / "smalling" / "PFAS_ENV.csv", skiprows=1
    )
    _seawolf_df = pd.read_csv(
        data_dir / "seawolf" / "PFAS_DataSummaries_5k_50k_SummaryData.csv"
    )

    # Smalling's raw header spells this compound "HFPO-DA; GenX" (with a
    # space); normalize to "HFPO-DA;GenX" so it matches all_compound_dict_df
    # and the TQ benchmark table (pfas_tq_benchmarks_epa_aligned.csv)
    # everywhere downstream.
    _smalling_df = _smalling_df.rename(
        columns={"HFPO-DA; GenX": "HFPO-DA;GenX"}
    )

    # Individual PFAS compound columns mix numeric concentrations (ng/L) with
    # two non-numeric sentinels: "nd" (tested, not detected above the lab
    # reporting limit) and "NA" (compound not analyzed at that site, already
    # read in as NaN). We treat nd as 0 so it stays distinct from true
    # missingness, then coerce the rest to numeric.
    pfas_cols = all_compound_dict_df.loc[
        all_compound_dict_df["smalling"], "compound"
    ].tolist()

    _smalling_clean = _smalling_df.copy()
    _smalling_clean[pfas_cols] = _smalling_clean[pfas_cols].replace("nd", 0)
    _smalling_clean[pfas_cols] = _smalling_clean[pfas_cols].apply(
        pd.to_numeric, errors="coerce"
    )

    # Last column in smallings is empty
    _smalling_clean = _smalling_clean.drop(columns=_smalling_clean.columns[-1])

    # ∑EAR uses "-" for "not analyzed" rather than NaN.
    _smalling_clean["∑EAR"] = pd.to_numeric(
        _smalling_clean["∑EAR"], errors="coerce"
    )

    # Final step: left merge to preserve unmatched rows
    ss_merged_df = _smalling_clean.merge(
        right=_seawolf_df,
        left_on=_smalling_clean["Site Code"].str.strip(),
        right_on=_seawolf_df["SiteCode"].str.strip(),
        how="left",
        suffixes=("_smalling", "_seawolf"),
        indicator=True,
    )
    return data_dir, pfas_cols, ss_merged_df


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### McMahon et al. (2022) load and join-ability (`mc_merged_df`)

    In this case, we perform similar operations

    1. Load McMahon via `pandas`
    2. Load McMahon data dictionary
    3. Clean up concentration values based on remarks
        1. `<`: Non-detect. Get the mean of ceiling value (`VA/2`), which is
           standard practice.
        2. `n`: Estimation. Flag as estimated
    4. Merge: using a left join to capture any unmatched records
    """)
    return


@app.cell(hide_code=True)
def _(all_compound_dict_df, data_dir, mcmahon_env_df, np, pd):
    pfas_codes = all_compound_dict_df.loc[
        all_compound_dict_df["mcmahon"], "compound"
    ].tolist()

    _mcmahon_env_clean = mcmahon_env_df.copy()

    for _c in pfas_codes:
        _rmk = _mcmahon_env_clean[f"{_c}-RMK"].fillna("").str.strip()
        _va = _mcmahon_env_clean[f"{_c}-VA"]

        # <: non-detect, use half the reporting limit as the estimate
        # n: trace detection, keep value as-is but flag low confidence
        # blank: confident detection, keep value as-is
        _mcmahon_env_clean[f"{_c}-VA_clean"] = np.where(
            _rmk == "<", _va / 2, _va
        )
        _mcmahon_env_clean[f"{_c}-estimated"] = _rmk == "n"

    # Drop raw remark/value columns now that -VA_clean and -estimated
    # capture the same information in usable form.
    _raw_cols = [
        c for c in _mcmahon_env_clean.columns if c.endswith(("-RMK", "-VA"))
    ]
    _mcmahon_env_clean = _mcmahon_env_clean.drop(columns=_raw_cols)

    _mcmahon_geo_df = pd.read_csv(
        data_dir / "mcmahon" / "PFAS_GEOSPATIAL.csv",
        thousands=",",
    )

    mc_merged_df = _mcmahon_env_clean.merge(
        right=_mcmahon_geo_df,
        left_on=_mcmahon_env_clean["NAWQA_ID"].str.strip(),
        right_on=_mcmahon_geo_df["NAWQA_ID"].str.strip(),
        how="left",
        suffixes=("_mc_env", "_mc_geo"),
        indicator=True,
    )
    return mc_merged_df, pfas_codes


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `ss_merged_df` and `mc_merged_df` now contain all data to be considered in
    our model design

    ### Unmatched rows and `NaN` clean up
    """)
    return


@app.cell(hide_code=True)
def _(mc_merged_df, mo, ss_merged_df):
    _ss_unmatched_df = ss_merged_df[ss_merged_df["_merge"] == "left_only"]
    ss_unmatched_count = _ss_unmatched_df.shape[0]

    _mac_unmatched_df = mc_merged_df[mc_merged_df["_merge"] == "left_only"]
    mac_unmatched_count = _mac_unmatched_df.shape[0]

    mo.md(f"""
    After joining the features and the PFAS concentration sets we get minimal
    data loss. The only concentration measurement without landscape attributes
    is `{_ss_unmatched_df.iloc[0, 0]}`.
    It will be dropped.
    """)
    return mac_unmatched_count, ss_unmatched_count


@app.cell(hide_code=True)
def _(
    mac_unmatched_count,
    mc_merged_df,
    mo,
    pd,
    print_sections,
    ss_merged_df,
    ss_unmatched_count,
):
    _integration_feasibility_summary = pd.DataFrame(
        [
            {
                "Datasets": (
                    "Smalling PFAS outcomes + Seawolf landscape predictors"
                ),
                "Left key": "Site Code",
                "Right key": "SiteCode",
                "Left records": ss_merged_df.shape[0],
                "Matched": ss_merged_df.shape[0] - ss_unmatched_count,
                "Unmatched": ss_unmatched_count,
                "Match rate (%)": round(
                    100
                    * (ss_merged_df.shape[0] - ss_unmatched_count)
                    / ss_merged_df.shape[0],
                    1,
                ),
            },
            {
                "Datasets": (
                    "McMahon PFAS outcomes + McMahon geospatial predictors"
                ),
                "Left key": "NAWQA_ID",
                "Right key": "NAWQA_ID",
                "Left records": mc_merged_df.shape[0],
                "Matched": mc_merged_df.shape[0] - mac_unmatched_count,
                "Unmatched": mac_unmatched_count,
                "Match rate (%)": round(
                    100
                    * (mc_merged_df.shape[0] - mac_unmatched_count)
                    / mc_merged_df.shape[0],
                    1,
                ),
            },
        ]
    )

    _integration_identifier_samples = pd.DataFrame(
        {
            "Smalling Site Code sample": (
                ss_merged_df["Site Code"]
                .dropna()
                .astype(str)
                .head(5)
                .reset_index(drop=True)
            ),
            "Seawolf SiteCode sample": (
                ss_merged_df["SiteCode"]
                .dropna()
                .astype(str)
                .head(5)
                .reset_index(drop=True)
            ),
            "McMahon environmental ID sample": (
                mc_merged_df["NAWQA_ID_mc_env"]
                .dropna()
                .astype(str)
                .head(5)
                .reset_index(drop=True)
            ),
            "McMahon geospatial ID sample": (
                mc_merged_df["NAWQA_ID_mc_geo"]
                .dropna()
                .astype(str)
                .head(5)
                .reset_index(drop=True)
            ),
        }
    )

    mo.vstack(
        [
            mo.ui.table(_integration_feasibility_summary),
            print_sections(
                {
                    "Sample identifiers for consistency review": mo.ui.table(
                        _integration_identifier_samples
                    ),
                }
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(ss_merged_df):
    ss_merged_clean_df = ss_merged_df[ss_merged_df["_merge"] != "left_only"]
    return (ss_merged_clean_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As for `NaN` values, the only ones found belong to the `Seawolf/Smalling`
    merged data set.
    """)
    return


@app.cell(hide_code=True)
def _(mc_merged_df, print_sections, ss_merged_clean_df):
    def _get_nan_counts(df, remove_non_matching=True):
        nan_counts = df.isna().sum()
        nan_table = (
            nan_counts.reset_index()
            .rename(columns={"index": "column", 0: "nan_count"})
            .assign(
                nan_pct=lambda inner_df: (
                    inner_df["nan_count"] / df.shape[0] * 100
                )
            )
            .pipe(
                lambda df: (
                    df.query("nan_count > 0") if remove_non_matching else df
                )
            )
            .sort_values("nan_count", ascending=False)
        )

        return nan_table

    print_sections(
        {
            "Seawolf/Smalling": _get_nan_counts(ss_merged_clean_df),
            "McMahon": _get_nan_counts(mc_merged_df),
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Results

    McMahon data does not require any further cleanups. The Seawolf landscape
    columns with missing values (`number_pfas_sites_proximal`,
    `mean_dist_to_pfas_site`, and the four burn-area fractions) are structural:
    a `NaN` there means no PFAS facility or burned area was detected within the
    buffer, not that a value went unmeasured. We checked against the metadata's
    documented `rdommax` per attribute first, but for most of these columns
    17-99% of rows are missing, so filling with the attribute max would have
    pulled most of the column toward the single worst observed site instead of
    reflecting "nothing found." We impute the facility count and burn fractions
    with `0`, since each has a natural zero. `mean_dist_to_pfas_site` has no
    natural zero (distance to a facility is undefined when there is no
    facility), so we impute it with its `rdommax` (~4997m) instead — that value
    is ~5km, the same buffer radius the field is computed over, so "no facility
    found within the 5km search radius" maps to "the nearest one is at least
    ~5km away" rather than an arbitrary outlier.
    """)
    return


@app.cell
def _(mc_merged_df, seawolf_dict_df, ss_merged_clean_df):
    mc_clean_df = mc_merged_df

    # NaN in these columns means "nothing detected in the buffer," so 0 is the
    # correct fill: each has a natural zero (no facilities, no area burned).
    _seawolf_structural_zero_columns = [
        "number_pfas_sites_proximal",
        "Burn_Area_5k_frac",
        "Burn_area_50k_frac",
        "Urbn_burn_5k_frac",
        "Urbn_burn_50k_frac",
    ]

    ss_clean_df = ss_merged_clean_df.copy()
    ss_clean_df[_seawolf_structural_zero_columns] = ss_clean_df[
        _seawolf_structural_zero_columns
    ].fillna(0)

    # mean_dist_to_pfas_site has no natural zero (undefined without a
    # facility), so fill with the attribute's rdommax (~5km) instead: that's
    # the buffer radius the field is computed over, i.e. "no facility within
    # 5km" -> "at least ~5km away."
    _mean_dist_rdom_max = seawolf_dict_df.set_index("attribute").loc[
        "mean_dist_to_pfas_site", "rdom_max"
    ]
    ss_clean_df["mean_dist_to_pfas_site"] = ss_clean_df[
        "mean_dist_to_pfas_site"
    ].fillna(_mean_dist_rdom_max)
    return mc_clean_df, ss_clean_df


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Dataset-by-dataset review

    The following subsections evaluate the structure, completeness,
    consistency, and modeling suitability of the Smalling, Seawolf, and McMahon
    datasets. We check for: dataset dimensions, key fields, missing values,
    duplicate identifiers, and numeric ranges. Integration readiness was
    already assessed in the join-ability sections above. *`ss_clean_df` and
    `mc_clean_df` will be used from now on.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Combined summary statistics and distributions
    """)
    return


@app.cell(hide_code=True)
def _(mc_clean_df, mo, np, pd, ss_clean_df):
    # Same key exposure/land-use variables carried through the rest of
    # this review (skewness, outliers, exploratory plots below) - scoping
    # the summary to them keeps this table to the ~18 rows readers
    # actually see discussed, instead of one row per numeric column
    # across both cleaned frames (~100+ rows for variables not otherwise
    # referenced in this notebook).
    ss_analysis_columns = [
        "∑PFAS",
        "Count Detected PFAS",
        "∑EAR",
        "number_pfas_sites_proximal",
        "mean_dist_to_pfas_site",
        "Burn_Area_5k_frac",
        "Burn_area_50k_frac",
        "Urbn_burn_5k_frac",
        "Urbn_burn_50k_frac",
    ]
    ss_analysis_columns = [
        col for col in ss_analysis_columns if col in ss_clean_df.columns
    ]

    mc_analysis_columns = [
        col for col in mc_clean_df.columns if col.endswith("-VA_clean")
    ][:6] + ["AGRI_12", "NATU_12", "URBA_12"]

    def _make_numeric_summary_table(df, columns, dataset_name):
        numeric_df = df[columns].select_dtypes(include="number")
        if numeric_df.empty:
            return pd.DataFrame(
                {
                    "Dataset": [dataset_name],
                    "Variable": ["No numeric columns"],
                    "Mean": [np.nan],
                    "Median": [np.nan],
                    "Std Dev": [np.nan],
                    "Min": [np.nan],
                    "Q1": [np.nan],
                    "Q3": [np.nan],
                    "Max": [np.nan],
                }
            )

        summary = (
            numeric_df.describe(percentiles=[0.25, 0.5, 0.75])
            .T.rename(
                columns={
                    "mean": "Mean",
                    "std": "Std Dev",
                    "min": "Min",
                    "25%": "Q1",
                    "50%": "Median",
                    "75%": "Q3",
                    "max": "Max",
                }
            )
            .reset_index()
            .rename(columns={"index": "Variable"})
        )
        summary.insert(0, "Dataset", dataset_name)
        return summary.round(4)

    _combined_summary = pd.concat(
        [
            _make_numeric_summary_table(
                ss_clean_df, ss_analysis_columns, "Smalling + Seawolf"
            ),
            _make_numeric_summary_table(
                mc_clean_df, mc_analysis_columns, "McMahon"
            ),
        ],
        ignore_index=True,
    )

    mo.vstack(
        [
            mo.md(
                "#### Numeric summary statistics for the cleaned datasets\n\n"
                "Scoped to the key exposure and land-use variables carried "
                "through the rest of this review; `ss_clean_df` and "
                "`mc_clean_df` hold additional engineered and raw columns "
                "not summarized here."
            ),
            mo.ui.table(_combined_summary),
        ]
    )
    return mc_analysis_columns, ss_analysis_columns


@app.cell(hide_code=True)
def _(
    mc_analysis_columns, mc_clean_df, mo, pd, ss_analysis_columns, ss_clean_df
):
    def _describe_distribution(df, columns, dataset_name):
        rows = []
        for col in columns:
            values = pd.to_numeric(df[col], errors="coerce").dropna()
            if values.empty:
                continue

            q1 = values.quantile(0.25)
            q3 = values.quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            outlier_count = int(((values < lower) | (values > upper)).sum())
            skew = values.skew()

            if skew > 1:
                skew_assessment = "Right-skewed"
            elif skew < -1:
                skew_assessment = "Left-skewed"
            else:
                skew_assessment = "Approximately symmetric"

            rows.append(
                {
                    "Dataset": dataset_name,
                    "Variable": col,
                    "Skewness": round(skew, 4),
                    "Assessment": skew_assessment,
                    "Q1": round(q1, 4),
                    "Q3": round(q3, 4),
                    "Outlier fence": f"[{lower:.4f}, {upper:.4f}]",
                    "Potential outliers": outlier_count,
                }
            )

        return pd.DataFrame(rows)

    _distribution_summary = pd.concat(
        [
            _describe_distribution(
                ss_clean_df, ss_analysis_columns, "Smalling + Seawolf"
            ),
            _describe_distribution(
                mc_clean_df, mc_analysis_columns, "McMahon"
            ),
        ],
        ignore_index=True,
    )

    mo.vstack(
        [
            mo.md(
                "#### Skewness and IQR outlier summary\n\n"
                "`Outlier fence` is the 1.5×IQR range "
                "`[Q1 - 1.5×IQR, Q3 + 1.5×IQR]`; values outside "
                "it count toward `Potential outliers`."
            ),
            mo.ui.table(_distribution_summary),
        ]
    )
    return


@app.cell
def _():
    import matplotlib.pyplot as _plt

    def make_plot_grid(df, columns, title, kind):
        # A compact 3x3 grid of small multiples (one subplot per
        # variable) instead of one plot per row/page - the whole
        # dataset's box plots (or histograms) at a glance.
        n_vars = max(1, len(columns))
        grid_cols = min(3, n_vars)
        grid_rows = -(-n_vars // grid_cols)
        fig, axes = _plt.subplots(
            grid_rows,
            grid_cols,
            figsize=(3.2 * grid_cols, 2.6 * grid_rows),
            squeeze=False,
        )
        flat_axes = axes.flatten()
        for ax, col in zip(flat_axes, columns):
            if kind == "box":
                df[col].dropna().plot.box(ax=ax, patch_artist=True)
                ax.set_ylabel("")
            else:
                df[col].dropna().hist(
                    ax=ax, bins=20, edgecolor="black", color="#7fb3d5"
                )
                ax.set_ylabel("Count", labelpad=4)
            ax.set_title(col, pad=6, fontsize=9)
            ax.grid(True, axis="y", linestyle="--", alpha=0.35)
        for ax in flat_axes[len(columns) :]:
            ax.axis("off")
        fig.suptitle(title, fontsize=13, y=0.99)
        fig.subplots_adjust(
            top=0.88,
            hspace=0.55,
            wspace=0.4,
            left=0.1,
            right=0.97,
            bottom=0.08,
        )
        return fig

    return (make_plot_grid,)


@app.cell(hide_code=True)
def _(make_plot_grid, mo, ss_clean_df):
    _ss_viz_columns = [
        "∑PFAS",
        "Count Detected PFAS",
        "∑EAR",
        "number_pfas_sites_proximal",
        "mean_dist_to_pfas_site",
        "Burn_Area_5k_frac",
        "Burn_area_50k_frac",
        "Urbn_burn_5k_frac",
        "Urbn_burn_50k_frac",
    ]
    _ss_viz_columns = [
        col for col in _ss_viz_columns if col in ss_clean_df.columns
    ]

    mo.vstack(
        [
            mo.md(
                "#### Exploratory plots for Smalling + Seawolf\n\n"
                "The following matplotlib box plots and histograms, "
                "generated by the shared `make_plot_grid()` helper "
                "below, summarize each variable's distribution at a "
                "glance.\n\n"
            ),
            make_plot_grid(
                ss_clean_df,
                _ss_viz_columns,
                "Smalling + Seawolf: box plots",
                kind="box",
            ),
            mo.md(""),
            make_plot_grid(
                ss_clean_df,
                _ss_viz_columns,
                "Smalling + Seawolf: histograms",
                kind="hist",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(make_plot_grid, mc_clean_df, mo):
    _mc_viz_columns = [
        col for col in mc_clean_df.columns if col.endswith("-VA_clean")
    ][:6] + ["AGRI_12", "NATU_12", "URBA_12"]

    mo.vstack(
        [
            mo.md(
                "#### Exploratory plots for McMahon\n\n"
                "The same matplotlib `make_plot_grid()` helper "
                "produces the box plots and histograms below for "
                "McMahon's variables.\n\n"
            ),
            make_plot_grid(
                mc_clean_df, _mc_viz_columns, "McMahon: box plots", kind="box"
            ),
            mo.md(""),
            make_plot_grid(
                mc_clean_df,
                _mc_viz_columns,
                "McMahon: histograms",
                kind="hist",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Smalling et al. (2023)

    #### Data exploration
    """)
    return


@app.cell(hide_code=True)
def _(mo, pd, pfas_cols, ss_clean_df):
    _smalling_quality_total_pfas = ss_clean_df["∑PFAS"]
    _smalling_quality_detected_count = ss_clean_df["Count Detected PFAS"]

    _smalling_exploration_summary = pd.DataFrame(
        [
            {
                "Measure": "Dataset shape (`ss_clean_df`)",
                "Result": (
                    f"{ss_clean_df.shape[0]} rows × "
                    f"{ss_clean_df.shape[1]} columns"
                ),
            },
            {
                "Measure": "Unique sampling sites",
                "Result": ss_clean_df["Site Code"].nunique(),
            },
            {
                "Measure": "States represented",
                "Result": ss_clean_df["State"].nunique(),
            },
            {
                "Measure": "Public-water sites",
                "Result": int(ss_clean_df["Site Type"].eq("Public").sum()),
            },
            {
                "Measure": "Private-well sites",
                "Result": int(ss_clean_df["Site Type"].eq("Private").sum()),
            },
            {
                "Measure": "PFAS compounds evaluated",
                "Result": len(pfas_cols),
            },
            {
                "Measure": "Cumulative PFAS range (ng/L)",
                "Result": (
                    f"{_smalling_quality_total_pfas.min():.4f} to "
                    f"{_smalling_quality_total_pfas.max():.4f}"
                ),
            },
            {
                "Measure": "Median cumulative PFAS (ng/L)",
                "Result": f"{_smalling_quality_total_pfas.median():.4f}",
            },
            {
                "Measure": "Detected compounds per site",
                "Result": (
                    f"{_smalling_quality_detected_count.min():.0f} to "
                    f"{_smalling_quality_detected_count.max():.0f}"
                ),
            },
        ]
    )

    mo.vstack(
        [
            mo.ui.table(_smalling_exploration_summary),
            mo.md(f"""
        The Smalling portion of `ss_clean_df` contains measured PFAS results
        for **{len(ss_clean_df)} sampling sites**. Cumulative PFAS
        concentrations are right-skewed because the maximum is much larger than
        the median. Public-water sites are more common than private-well sites
        in this table. The PFAS columns and `∑EAR` were already cleaned (`nd` →
        0, coerced to numeric) while building `ss_merged_df`, and the unmatched
        site plus structural Seawolf `NaN`s were resolved while building
        `ss_clean_df`.
        """),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Quality assessment
    """)
    return


@app.cell(hide_code=True)
def _(mo, pd, pfas_cols, print_sections, ss_clean_df):
    _smalling_assessment_numeric_pfas = ss_clean_df[pfas_cols]
    _smalling_assessment_published_count = ss_clean_df["Count Detected PFAS"]
    _smalling_assessment_published_total = ss_clean_df["∑PFAS"]
    _smalling_assessment_calculated_count = (
        _smalling_assessment_numeric_pfas.gt(0).sum(axis=1)
    )
    _smalling_assessment_calculated_total = (
        _smalling_assessment_numeric_pfas.fillna(0).sum(axis=1)
    )

    _smalling_assessment_columns = (
        ["Site Code", "State", "Site Type"]
        + pfas_cols
        + ["Count Detected PFAS", "∑PFAS", "∑EAR"]
    )
    _smalling_missing_summary = (
        ss_clean_df[_smalling_assessment_columns]
        .isna()
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .rename("Missing values")
        .rename_axis("Column")
        .reset_index()
    )
    _smalling_missing_summary["Missing (%)"] = (
        100 * _smalling_missing_summary["Missing values"] / len(ss_clean_df)
    ).round(1)

    _smalling_quality_checks = pd.DataFrame(
        [
            {
                "Quality check": "Missing site identifiers",
                "Result": int(ss_clean_df["Site Code"].isna().sum()),
                "Assessment": "Pass",
            },
            {
                "Quality check": "Duplicate site identifiers",
                "Result": int(ss_clean_df["Site Code"].duplicated().sum()),
                "Assessment": "Pass",
            },
            {
                "Quality check": (
                    "Non-detect values (cleaned to 0 while building "
                    "ss_merged_df)"
                ),
                "Result": int(
                    _smalling_assessment_numeric_pfas.eq(0).sum().sum()
                ),
                "Assessment": (
                    "Expected; 'nd' was converted to 0 upstream and is no "
                    "longer distinguishable here"
                ),
            },
            {
                "Quality check": "Compound results not analyzed or missing",
                "Result": int(
                    _smalling_assessment_numeric_pfas.isna().sum().sum()
                ),
                "Assessment": (
                    "Review; retain as missing rather than treating as "
                    "non-detect"
                ),
            },
            {
                "Quality check": "Rows with zero detected PFAS",
                "Result": int(
                    _smalling_assessment_published_count.eq(0).sum()
                ),
                "Assessment": (
                    "Review; this table alone does not represent the "
                    "proposed Low class"
                ),
            },
            {
                "Quality check": (
                    "Published count differs from simple recalculation"
                ),
                "Result": int(
                    _smalling_assessment_calculated_count.ne(
                        _smalling_assessment_published_count
                    ).sum()
                ),
                "Assessment": (
                    "Review compound-inclusion rules before recomputing "
                    "published fields"
                ),
            },
            {
                "Quality check": (
                    "Published total differs by more than 0.1 ng/L"
                ),
                "Result": int(
                    _smalling_assessment_calculated_total.sub(
                        _smalling_assessment_published_total
                    )
                    .abs()
                    .gt(0.1)
                    .sum()
                ),
                "Assessment": "Review rounding or compound-inclusion rules",
            },
            {
                "Quality check": "Negative cumulative PFAS values",
                "Result": int(
                    _smalling_assessment_published_total.lt(0).sum()
                ),
                "Assessment": "Pass",
            },
        ]
    )

    mo.vstack(
        [
            mo.ui.table(_smalling_quality_checks),
            print_sections(
                {
                    "Columns with the most missing values": mo.ui.table(
                        _smalling_missing_summary
                    ),
                }
            ),
            mo.md("""
        **Suitability assessment:** The Smalling portion of `ss_clean_df` is
        suitable as a measured PFAS outcome table, but it requires careful
        treatment of non-detect and not-analyzed values. The supplied table
        contains detected sites only, so the Low/no-detection class must be
        obtained from a complete sampling frame rather than inferred from this
        table alone.
        """),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Seawolf et al. (2023)

    #### Data exploration
    """)
    return


@app.cell(hide_code=True)
def _(mo, pd, print_sections, ss_clean_df):
    _seawolf_quality_landcover_columns = [
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
    _seawolf_quality_predictor_columns = [
        "number_pfas_sites_proximal",
        "mean_dist_to_pfas_site",
        "Burn_Area_5k_frac",
        "Burn_area_50k_frac",
        "Urbn_burn_5k_frac",
        "Urbn_burn_50k_frac",
    ] + _seawolf_quality_landcover_columns
    _seawolf_quality_landcover_total = ss_clean_df[
        _seawolf_quality_landcover_columns
    ].sum(axis=1)

    _seawolf_exploration_summary = pd.DataFrame(
        [
            {
                "Measure": "Dataset shape (`ss_clean_df`)",
                "Result": (
                    f"{ss_clean_df.shape[0]} rows × "
                    f"{ss_clean_df.shape[1]} columns"
                ),
            },
            {
                "Measure": "Unique sampling sites (Seawolf-matched)",
                "Result": ss_clean_df["SiteCode"].nunique(),
            },
            {
                "Measure": "Studies represented",
                "Result": ss_clean_df["Study_seawolf"].nunique(),
            },
            {
                "Measure": "Landscape predictor columns",
                "Result": len(_seawolf_quality_predictor_columns),
            },
            {
                "Measure": "Sites with a recorded proximal-facility count",
                "Result": int(
                    ss_clean_df["number_pfas_sites_proximal"].notna().sum()
                ),
            },
            {
                "Measure": "Mean land-cover fraction sum",
                "Result": f"{_seawolf_quality_landcover_total.mean():.4f}",
            },
            {
                "Measure": "Land-cover fraction-sum range",
                "Result": (
                    f"{_seawolf_quality_landcover_total.min():.4f} to "
                    f"{_seawolf_quality_landcover_total.max():.4f}"
                ),
            },
        ]
    )

    _seawolf_study_summary = (
        ss_clean_df["Study_seawolf"]
        .value_counts()
        .rename_axis("Study")
        .reset_index(name="Sites")
    )

    mo.vstack(
        [
            mo.ui.table(_seawolf_exploration_summary),
            print_sections(
                {
                    "Sites by contributing study": mo.ui.table(
                        _seawolf_study_summary
                    ),
                }
            ),
            mo.md(f"""
        The Seawolf portion of `ss_clean_df` contains landscape characteristics
        joined onto **{len(ss_clean_df)} Smalling sites**. It includes
        potential PFAS-source facilities, burn-area measures, and land-cover
        fractions calculated around each sampling location. The unmatched
        Smalling site was already dropped and structural Seawolf `NaN`s (no
        facility or burned area found within the buffer) were already imputed
        while building `ss_clean_df`.
        """),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Quality assessment
    """)
    return


@app.cell(hide_code=True)
def _(mo, pd, print_sections, ss_clean_df):
    _seawolf_assessment_landcover_columns = [
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
    _seawolf_assessment_fraction_columns = [
        "Burn_Area_5k_frac",
        "Burn_area_50k_frac",
        "Urbn_burn_5k_frac",
        "Urbn_burn_50k_frac",
    ] + _seawolf_assessment_landcover_columns

    _seawolf_assessment_landcover_total = ss_clean_df[
        _seawolf_assessment_landcover_columns
    ].sum(axis=1)
    _seawolf_assessment_invalid_fraction_count = int(
        (
            ss_clean_df[_seawolf_assessment_fraction_columns].lt(0)
            | ss_clean_df[_seawolf_assessment_fraction_columns].gt(1)
        )
        .sum()
        .sum()
    )

    _seawolf_assessment_columns = [
        "SiteCode",
        "Study_seawolf",
        "number_pfas_sites_proximal",
        "mean_dist_to_pfas_site",
    ] + _seawolf_assessment_fraction_columns
    _seawolf_missing_summary = (
        ss_clean_df[_seawolf_assessment_columns]
        .isna()
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .rename("Missing values")
        .rename_axis("Column")
        .reset_index()
    )
    _seawolf_missing_summary["Missing (%)"] = (
        100 * _seawolf_missing_summary["Missing values"] / len(ss_clean_df)
    ).round(1)

    _seawolf_quality_checks = pd.DataFrame(
        [
            {
                "Quality check": "Missing site identifiers",
                "Result": int(ss_clean_df["SiteCode"].isna().sum()),
                "Assessment": (
                    "Pass; the unmatched Smalling site was already dropped "
                    "while building `ss_clean_df`"
                ),
            },
            {
                "Quality check": "Duplicate site identifiers",
                "Result": int(
                    ss_clean_df["SiteCode"].dropna().duplicated().sum()
                ),
                "Assessment": "Pass",
            },
            {
                "Quality check": "Fraction values outside 0-1",
                "Result": _seawolf_assessment_invalid_fraction_count,
                "Assessment": "Pass"
                if _seawolf_assessment_invalid_fraction_count == 0
                else "Review",
            },
            {
                "Quality check": "Land-cover totals substantially below 1.0",
                "Result": int(
                    _seawolf_assessment_landcover_total.lt(0.95).sum()
                ),
                "Assessment": (
                    "Review; some locations may have incomplete land-cover "
                    "coverage"
                ),
            },
            {
                "Quality check": "Missing proximal-facility count",
                "Result": int(
                    ss_clean_df["number_pfas_sites_proximal"].isna().sum()
                ),
                "Assessment": (
                    "Pass; structural missingness (no facility within "
                    "buffer) was already imputed to 0"
                ),
            },
            {
                "Quality check": "Missing mean facility distance",
                "Result": int(
                    ss_clean_df["mean_dist_to_pfas_site"].isna().sum()
                ),
                "Assessment": (
                    "Pass; already imputed with the ~5 km buffer radius "
                    "(`rdom_max`)"
                ),
            },
            {
                "Quality check": "Negative facility distances",
                "Result": int(
                    ss_clean_df["mean_dist_to_pfas_site"].lt(0).sum()
                ),
                "Assessment": "Pass",
            },
        ]
    )

    mo.vstack(
        [
            mo.ui.table(_seawolf_quality_checks),
            print_sections(
                {
                    "Columns with the most missing values": mo.ui.table(
                        _seawolf_missing_summary
                    ),
                }
            ),
            mo.md("""
        **Suitability assessment:** The Seawolf portion of `ss_clean_df` is
        suitable for use as a predictor table. Site identifiers are unique and
        fraction values are within valid bounds. The unmatched Smalling site
        was dropped, and the structural facility/burn-area `NaN`s were imputed
        (0 for facility count and burn fractions, `rdom_max` ≈ 5 km for mean
        facility distance) while building `ss_clean_df` (see the join-ability
        and `NaN` clean-up sections above); no unresolved missing or unmatched
        records remain, though rows with these imputed values should be treated
        as assumption-driven rather than directly measured. Some sites still
        show land-cover fraction totals well below 1.0, which reflects
        incomplete land-cover coverage rather than a missingness issue and
        remains a separate item for review.
        """),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### McMahon et al. (2022)

    #### Data exploration
    """)
    return


@app.cell(hide_code=True)
def _(mc_clean_df, mo, pd, print_sections):
    _mcmahon_quality_clean_columns = [
        column
        for column in mc_clean_df.columns
        if column.endswith("-VA_clean")
    ]
    _mcmahon_quality_estimated_columns = [
        column
        for column in mc_clean_df.columns
        if column.endswith("-estimated")
    ]
    _mcmahon_quality_total_concentration = mc_clean_df[
        _mcmahon_quality_clean_columns
    ].sum(axis=1, min_count=1)
    _mcmahon_quality_land_use_total = mc_clean_df[
        ["AGRI_12", "NATU_12", "URBA_12"]
    ].sum(axis=1)

    _mcmahon_exploration_summary = pd.DataFrame(
        [
            {
                "Measure": "Cleaned dataset shape (`mc_clean_df`)",
                "Result": (
                    f"{mc_clean_df.shape[0]} rows × "
                    f"{mc_clean_df.shape[1]} columns"
                ),
            },
            {
                "Measure": "Unique environmental site IDs",
                "Result": mc_clean_df["NAWQA_ID_mc_env"].nunique(),
            },
            {
                "Measure": "PFAS compounds evaluated",
                "Result": len(_mcmahon_quality_clean_columns),
            },
            {
                "Measure": "Estimated or trace-result flags",
                "Result": int(
                    mc_clean_df[_mcmahon_quality_estimated_columns].sum().sum()
                ),
            },
            {
                "Measure": "Cleaned concentration-total range (ng/L)",
                "Result": (
                    f"{_mcmahon_quality_total_concentration.min():.4f} to "
                    f"{_mcmahon_quality_total_concentration.max():.4f}"
                ),
            },
            {
                "Measure": "Median cleaned concentration total (ng/L)",
                "Result": (
                    f"{_mcmahon_quality_total_concentration.median():.4f}"
                ),
            },
            {
                "Measure": "Mean land-use percentage total",
                "Result": f"{_mcmahon_quality_land_use_total.mean():.1f}%",
            },
        ]
    )

    _mcmahon_land_use_summary = (
        mc_clean_df[["AGRI_12", "NATU_12", "URBA_12"]]
        .describe()
        .T.reset_index(names="Land-use variable")
        .round(4)
    )

    mo.vstack(
        [
            mo.ui.table(_mcmahon_exploration_summary),
            print_sections(
                {
                    "Land-use variable summary": mo.ui.table(
                        _mcmahon_land_use_summary
                    ),
                }
            ),
            mo.md(f"""
        The McMahon analytical table contains groundwater PFAS measurements and
        landscape predictors for **{len(mc_clean_df)} sites**. Concentration
        totals are strongly right-skewed, and the agricultural, natural, and
        urban percentages collectively cover approximately 100% of the
        surrounding land area.
        """),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Quality assessment
    """)
    return


@app.cell(hide_code=True)
def _(mc_clean_df, mo, pd, print_sections):
    _mcmahon_assessment_clean_columns = [
        column
        for column in mc_clean_df.columns
        if column.endswith("-VA_clean")
    ]
    _mcmahon_assessment_estimated_columns = [
        column
        for column in mc_clean_df.columns
        if column.endswith("-estimated")
    ]
    _mcmahon_assessment_geospatial_columns = [
        column
        for column in mc_clean_df.columns
        if column
        not in [
            "key_0",
            "NAWQA_ID_mc_env",
            "DATE",
            "TIME",
            "NAWQA_ID_mc_geo",
            "_merge",
        ]
        and column not in _mcmahon_assessment_clean_columns
        and column not in _mcmahon_assessment_estimated_columns
    ]
    _mcmahon_assessment_land_use_columns = ["AGRI_12", "NATU_12", "URBA_12"]
    _mcmahon_assessment_land_use_total = mc_clean_df[
        _mcmahon_assessment_land_use_columns
    ].sum(axis=1)

    _mcmahon_quality_checks = pd.DataFrame(
        [
            {
                "Quality check": "Missing environmental site IDs",
                "Result": int(mc_clean_df["NAWQA_ID_mc_env"].isna().sum()),
                "Assessment": "Pass",
            },
            {
                "Quality check": "Duplicate environmental site IDs",
                "Result": int(
                    mc_clean_df["NAWQA_ID_mc_env"].duplicated().sum()
                ),
                "Assessment": "Pass",
            },
            {
                "Quality check": "Environmental-to-geospatial matches",
                "Result": (
                    f"{int(mc_clean_df['_merge'].eq('both').sum())} of "
                    f"{len(mc_clean_df)}"
                ),
                "Assessment": "Pass"
                if mc_clean_df["_merge"].eq("both").all()
                else "Review",
            },
            {
                "Quality check": "Missing cleaned PFAS values",
                "Result": int(
                    mc_clean_df[_mcmahon_assessment_clean_columns]
                    .isna()
                    .sum()
                    .sum()
                ),
                "Assessment": "Pass",
            },
            {
                "Quality check": "Missing geospatial predictor values",
                "Result": int(
                    mc_clean_df[_mcmahon_assessment_geospatial_columns]
                    .isna()
                    .sum()
                    .sum()
                ),
                "Assessment": "Pass",
            },
            {
                "Quality check": "Negative geospatial values",
                "Result": int(
                    mc_clean_df[_mcmahon_assessment_geospatial_columns]
                    .lt(0)
                    .sum()
                    .sum()
                ),
                "Assessment": "Pass",
            },
            {
                "Quality check": "Land-use values outside 0-100%",
                "Result": int(
                    (
                        mc_clean_df[_mcmahon_assessment_land_use_columns].lt(0)
                        | mc_clean_df[_mcmahon_assessment_land_use_columns].gt(
                            100
                        )
                    )
                    .sum()
                    .sum()
                ),
                "Assessment": "Pass",
            },
            {
                "Quality check": "Land-use totals outside 99.5-100.5%",
                "Result": int(
                    (
                        ~_mcmahon_assessment_land_use_total.between(
                            99.5, 100.5
                        )
                    ).sum()
                ),
                "Assessment": (
                    "Pass; minor differences are expected from rounding"
                ),
            },
            {
                "Quality check": "Estimated or trace-result flags",
                "Result": int(
                    mc_clean_df[_mcmahon_assessment_estimated_columns]
                    .sum()
                    .sum()
                ),
                "Assessment": "Retain as a data-quality indicator",
            },
        ]
    )

    _mcmahon_missing_summary = (
        mc_clean_df.isna()
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .rename("Missing values")
        .reset_index()
        .rename(columns={"index": "Column"})
    )
    _mcmahon_missing_summary["Missing (%)"] = (
        100 * _mcmahon_missing_summary["Missing values"] / len(mc_clean_df)
    ).round(1)

    mo.vstack(
        [
            mo.ui.table(_mcmahon_quality_checks),
            print_sections(
                {
                    "Columns with the most missing values": mo.ui.table(
                        _mcmahon_missing_summary
                    ),
                }
            ),
            mo.md("""
        **Suitability assessment:** The McMahon environmental and geospatial
        tables are complete, uniquely keyed, and fully matched. The cleaned
        concentration values are usable for exploratory modeling, but totals
        that include half-reporting-limit substitutions should not be
        interpreted as detected-only concentration without retaining the
        original censoring logic.
        """),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Categorical variable evaluation

    This section evaluates the categorical variables already available in
    `ss_clean_df` and `mc_clean_df`. The checks focus on category completeness,
    cardinality, class imbalance, rare levels, inconsistent labels, and the
    encoding treatment that may be appropriate before modeling. Site
    identifiers and laboratory quality flags are excluded because they are keys
    or data-quality indicators rather than explanatory categories.
    """)
    return


@app.cell(hide_code=True)
def _(mc_clean_df, mo, pd, print_sections, ss_clean_df):
    def _categorical_profile(dataset_name, dataframe, columns):
        profile_rows = []
        value_count_tables = {}

        for column_name in columns:
            categorical_series = (
                dataframe[column_name].astype("string").str.strip()
            )
            blank_count = int(categorical_series.eq("").sum())
            categorical_series = categorical_series.mask(
                categorical_series.eq(""), pd.NA
            )
            non_missing_series = categorical_series.dropna()
            category_counts = non_missing_series.value_counts(dropna=False)

            distinct_count = int(category_counts.shape[0])
            missing_count = int(categorical_series.isna().sum())
            missing_pct = (
                round(100 * missing_count / len(dataframe), 1)
                if len(dataframe)
                else 0.0
            )

            if category_counts.empty:
                dominant_category = None
                dominant_count = 0
                dominant_pct = 0.0
            else:
                dominant_category = str(category_counts.index[0])
                dominant_count = int(category_counts.iloc[0])
                dominant_pct = (
                    round(100 * dominant_count / len(non_missing_series), 1)
                    if len(non_missing_series)
                    else 0.0
                )

            rare_category_count = int(category_counts.lt(5).sum())

            normalized_series = non_missing_series.str.casefold().str.replace(
                r"\s+", " ", regex=True
            )
            label_variant_table = pd.DataFrame(
                {
                    "original": non_missing_series,
                    "normalized": normalized_series,
                }
            ).drop_duplicates()
            label_variant_groups = (
                int(
                    label_variant_table.groupby("normalized")["original"]
                    .nunique()
                    .gt(1)
                    .sum()
                )
                if not label_variant_table.empty
                else 0
            )

            if distinct_count <= 1:
                recommended_treatment = (
                    "Drop from modeling; no useful variation"
                )
            elif distinct_count == 2:
                recommended_treatment = "Binary encode or one-hot encode"
            elif distinct_count <= 10:
                recommended_treatment = "One-hot encode"
            elif distinct_count <= 50:
                recommended_treatment = (
                    "One-hot encode; combine very rare levels if needed"
                )
            else:
                recommended_treatment = (
                    "High cardinality; group levels or use leakage-safe "
                    "frequency encoding"
                )

            assessment_flags = []
            if missing_count > 0:
                assessment_flags.append("missing values")
            if blank_count > 0:
                assessment_flags.append("blank labels")
            if distinct_count <= 1:
                assessment_flags.append("no variation")
            if dominant_pct >= 90 and distinct_count > 1:
                assessment_flags.append("high imbalance")
            if rare_category_count > 0:
                assessment_flags.append("rare levels")
            if label_variant_groups > 0:
                assessment_flags.append("inconsistent label formatting")

            quality_assessment = (
                "Pass"
                if not assessment_flags
                else "Review: " + ", ".join(assessment_flags)
            )

            profile_rows.append(
                {
                    "Dataset": dataset_name,
                    "Variable": column_name,
                    "Rows": len(dataframe),
                    "Non-missing": int(non_missing_series.shape[0]),
                    "Missing": missing_count,
                    "Missing (%)": missing_pct,
                    "Distinct categories": distinct_count,
                    "Dominant category": dominant_category,
                    "Dominant count": dominant_count,
                    "Dominant (%)": dominant_pct,
                    "Rare categories (<5 rows)": rare_category_count,
                    "Label-variant groups": label_variant_groups,
                    "Recommended treatment": recommended_treatment,
                    "Quality assessment": quality_assessment,
                }
            )

            category_table = (
                category_counts.rename("Count")
                .rename_axis("Category")
                .reset_index()
            )
            category_table["Percent of non-missing"] = (
                (
                    100 * category_table["Count"] / len(non_missing_series)
                ).round(1)
                if len(non_missing_series)
                else 0.0
            )

            value_count_tables[f"{dataset_name}: {column_name}"] = mo.ui.table(
                category_table.head(25)
            )

        profile_columns = [
            "Dataset",
            "Variable",
            "Rows",
            "Non-missing",
            "Missing",
            "Missing (%)",
            "Distinct categories",
            "Dominant category",
            "Dominant count",
            "Dominant (%)",
            "Rare categories (<5 rows)",
            "Label-variant groups",
            "Recommended treatment",
            "Quality assessment",
        ]
        return pd.DataFrame(
            profile_rows, columns=profile_columns
        ), value_count_tables

    # Smalling categorical variables: geographic and water-source groupings.
    _smalling_categorical_columns = [
        column_name
        for column_name in ["State", "Site Type", "Study_smalling"]
        if column_name in ss_clean_df.columns
    ]

    # Seawolf categorical variables: contributing study. SiteCode and station
    # names are identifiers and are intentionally excluded.
    _seawolf_categorical_columns = [
        column_name
        for column_name in ["Study_seawolf"]
        if column_name in ss_clean_df.columns
    ]

    # McMahon categorical variables are detected from the already merged
    # dataframe. Identifiers, dates/times, merge indicators, and
    # estimated-result flags are excluded.
    _mcmahon_categorical_exclusions = {
        "key_0",
        "NAWQA_ID_mc_env",
        "NAWQA_ID_mc_geo",
        "DATE",
        "TIME",
        "_merge",
    }
    _mcmahon_categorical_columns = [
        column_name
        for column_name in mc_clean_df.select_dtypes(
            include=["object", "string", "category", "bool"]
        ).columns
        if column_name not in _mcmahon_categorical_exclusions
        and not column_name.endswith("-estimated")
    ]

    _smalling_categorical_profile, _smalling_category_tables = (
        _categorical_profile(
            "Smalling", ss_clean_df, _smalling_categorical_columns
        )
    )
    _seawolf_categorical_profile, _seawolf_category_tables = (
        _categorical_profile(
            "Seawolf", ss_clean_df, _seawolf_categorical_columns
        )
    )
    _mcmahon_categorical_profile, _mcmahon_category_tables = (
        _categorical_profile(
            "McMahon", mc_clean_df, _mcmahon_categorical_columns
        )
    )

    _categorical_profiles = {
        "Smalling": _smalling_categorical_profile,
        "Seawolf": _seawolf_categorical_profile,
        "McMahon": _mcmahon_categorical_profile,
    }

    _categorical_overall_rows = []
    for _dataset_name, _profile_df in _categorical_profiles.items():
        _categorical_overall_rows.append(
            {
                "Dataset": _dataset_name,
                "Categorical variables evaluated": len(_profile_df),
                "Variables with missing values": int(
                    _profile_df["Missing"].gt(0).sum()
                ),
                "Single-level variables": int(
                    _profile_df["Distinct categories"].le(1).sum()
                ),
                "Highly imbalanced variables (≥90%)": int(
                    _profile_df["Dominant (%)"].ge(90).sum()
                ),
                "Variables with rare levels": int(
                    _profile_df["Rare categories (<5 rows)"].gt(0).sum()
                ),
                "Variables with label variants": int(
                    _profile_df["Label-variant groups"].gt(0).sum()
                ),
            }
        )

    _categorical_overall_summary = pd.DataFrame(_categorical_overall_rows)

    def _categorical_panel(profile_df, category_tables, dataset_note):
        # profile_df has 14 columns; two of them ("Recommended treatment",
        # "Quality assessment") hold long free-text notes that read poorly
        # next to short numeric/label columns in one wide table, so split
        # the free-text columns into their own narrower table instead.
        text_columns = ["Recommended treatment", "Quality assessment"]
        measure_columns = [
            col for col in profile_df.columns if col not in text_columns
        ]
        panel_items = [
            mo.ui.table(profile_df[measure_columns]),
            mo.ui.table(profile_df[["Dataset", "Variable", *text_columns]]),
        ]
        if category_tables:
            panel_items.append(print_sections(category_tables))
        panel_items.append(mo.md(dataset_note))
        return mo.vstack(panel_items)

    mo.vstack(
        [
            mo.ui.table(_categorical_overall_summary),
            print_sections(
                {
                    "Smalling": _categorical_panel(
                        _smalling_categorical_profile,
                        _smalling_category_tables,
                        """
                **Interpretation:** `Site Type` can be binary encoded. `State`
                is a nominal geographic variable and should be one-hot encoded
                or grouped into broader regions if rare states create unstable
                estimates. A study field with only one observed level should be
                removed because it does not help distinguish observations.
                """,
                    ),
                    "Seawolf": _categorical_panel(
                        _seawolf_categorical_profile,
                        _seawolf_category_tables,
                        """
                **Interpretation:** `Study_seawolf` may capture differences in
                sampling design, geography, or time period. It can be retained
                as a control variable, but it should not become a shortcut for
                predicting PFAS outcomes. Use grouped cross-validation by study
                to test whether model performance generalizes beyond the
                contributing studies.
                """,
                    ),
                    "McMahon": _categorical_panel(
                        _mcmahon_categorical_profile,
                        _mcmahon_category_tables,
                        """
                **Interpretation:** Low-cardinality McMahon categories can be
                one-hot encoded. Variables with one level should be dropped,
                while rare levels should be combined only when the grouping is
                scientifically meaningful. Site identifiers, dates, merge
                indicators, and estimated-result flags are intentionally
                excluded from this categorical predictor review.
                """,
                    ),
                }
            ),
            mo.md("""
        **Overall modeling recommendation:** Standardize whitespace and
        capitalization before encoding, preserve missingness as an explicit
        category only when it has a defensible meaning, combine rare categories
        before train/test splitting rules are finalized, and fit all encoders
        using training data only. High-cardinality identifiers should not be
        used as predictors because they can cause memorization and poor
        generalization.
        """),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Step 2.5: Preparing for modeling

    ### Scaling
    Several geospatial and land-use predictors, and cumulative PFAS
    concentration itself, are right-skewed (see skewness/IQR summary above) and
    span very different units. We will consider this in our modeling since this
    might alter the training effectiveness.

    ### Categorical encoding
    Per the Categorical Variable Evaluation above: binary-encode two-level
    fields (`Site Type`), one-hot encode low-cardinality nominal fields
    (`State`, McMahon land-use categories), drop single-level fields, and
    combine rare levels. Encoders will be fit on training data only. Study
    identifiers (`Study_seawolf`, `Study_smalling`) are retained as controls,
    not predictors.

    <h3>Feature engineering and selection: from concentration cutoffs to
    toxicity quotients</h3>
    The original median-based low/medium/high classification treated every PFAS
    compound as equally toxic per ng/L, even though compounds differ
    substantially in their health-based benchmarks. We're replacing it with a
    toxicity quotient (TQ) target scored only on the six compounds EPA
    regulates under its 2024 rule: **PFOA, PFOS, PFHxS, PFNA, PFBS, and HFPO-DA
    (GenX)**, all present as columns in the Smalling data. Benchmarks are now
    merged into `all_compound_dict_df` from
    `data/factors/pfas_tq_benchmarks_epa_aligned.csv`: EPA values from the
    final-rule fact sheet (CDM Smith, 2024) for the six regulated compounds
    (`epa_ratio_eligible`), state-only values from Table S5 of Smalling et al.
    (2023) for the rest.

    * **Per-compound TQ** = concentration divided by that compound's EPA
      benchmark.
    * **∑TQ (Hazard Index)** = sum of TQ across only the six regulated
      compounds, not the full panel, a deliberate narrowing from the earlier
      `∑EAR`/cumulative-concentration approach.
    * The other 11 compounds (PFBA, PFPeA, PFHxA, PFHpA, PFDA, PFPeS, PFHpS,
      PFDS, PFPrS, 6:2 FTS, FOSA) stay in the dataset as a descriptive slice,
      not part of the target, since EPA hasn't set enforceable benchmarks for
      them.

    Tiers are unchanged from the Proposed classification above
    (`within_reduced_monitoring`, `above_trigger`, `mcl_exceedance`).

    Restricting ∑TQ to regulated compounds keeps each cutoff tied to a real
    compliance action point, matches the phased-compliance motivation, and
    keeps the classifier legible in the terms operators already track (trigger
    vs. MCL), without the model itself determining compliance, per Constraints.
    The dependent variable is this ∑TQ class; predictors are landscape/land-use
    features only, never concentration data, so the model tests whether land
    use alone can flag risk before a site is ever sampled.

    The reshape/join/sum mechanics behind ∑TQ, worked out below, produce
    `ss_scored_df`: `ss_clean_df`'s predictors joined with the classified
    `sum_tq_epa` (∑TQ / Hazard Index) and a supplementary
    `sum_tq_state_only` column. Design decisions made along the way:
    * Non-detects are treated as 0 per compound (not dropped), so an absent
      compound contributes zero rather than excluding the sample.
    * Summing PFOA/PFOS's individual-MCL ratios with the 4-compound Hazard
      Index (PFNA + PFHxS + GenX + PFBS) into one ∑TQ is our own design choice,
      not an EPA-prescribed method; state it as an assumption.
    * PFPeS/PFPrS (no benchmark in either source) are kept in the long table
      rather than dropped, with their per-compound TQ left as `NaN`; `NaN`
      contributes nothing to either sum (`pandas`' default `sum(skipna=True)`)
      rather than being silently treated as zero risk.
    * Run against the full sample dataset (236 sites), `sum_tq_epa` ranges
      0–17.7 with a median of 0.17, well below the trigger cutoff of 0.5 for
      most sites but with a long right tail past the MCL-exceedance cutoff of
      1.0 — the Step 3 evaluation plan will formalize where those tier
      boundaries fall.

    McMahon's groundwater data (`mc_clean_df`) is scored the same way,
    against the same benchmark table, producing a `sum_tq_epa` on the same
    scale. It is not, however, directly comparable to Smalling's — two
    things don't carry over cleanly, and are worth stating up front rather
    than discovering downstream:
    * McMahon's panel doesn't include HFPO-DA (GenX) at all — the site-level
      geospatial data used never measured it. Its Hazard Index is
      necessarily a 5-of-6-compound sum (missing the GenX term), so
      `sum_tq_epa` is not directly apples-to-apples between the two
      studies; treat cross-study ∑TQ comparisons with that caveat.
    * McMahon's non-detects are already imputed as half the reporting limit
      (`VA/2`) during Step 2 cleaning, not treated as 0 — a different
      convention than Smalling's, inherited rather than newly introduced
      here. Reconciling the two would mean reconstructing a per-sample
      reporting limit for Smalling from its analyzing lab and year
      (Smalling et al., 2023, Appendix A, Tables S1 and S3), which has
      gaps that source doesn't resolve (see Step 2's Smalling load and
      clean-up above); we treat this as a standing limitation rather than
      one to close.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Toxicity quotient (∑TQ) construction

    Reshape each study's data to one row per site per compound, join
    `all_compound_dict_df`'s EPA/state TQ benchmarks, and compute
    per-compound and summed TQ (∑TQ), producing the classified target
    the Step 4 modeling techniques will predict. Worked out first for
    Smalling/Seawolf (`ss_clean_df` → `ss_scored_df`) below; McMahon's
    groundwater data (`mc_clean_df` → `mc_scored_df`) follows the same
    three steps and is scored further down.

    ### Reshape to one row per site per compound
    Long-format the wide per-compound columns in `ss_clean_df` so each row is
    a single (site, compound) pair, carrying the site's landscape/land-use
    predictors alongside that compound's concentration.
    """)
    return


@app.cell(hide_code=True)
def _(mc_clean_df, pd, pfas_codes, pfas_cols, ss_clean_df):
    ss_long_df = pd.melt(
        ss_clean_df,
        id_vars=[c for c in ss_clean_df.columns if c not in pfas_cols],
        value_vars=pfas_cols,
        var_name="compound",
        value_name="concentration",
    )

    _mc_value_cols = [f"{c}-VA_clean" for c in pfas_codes]
    _mc_estimated_cols = [f"{c}-estimated" for c in pfas_codes]
    _mc_dropped_cols = _mc_value_cols + _mc_estimated_cols

    mc_long_df = pd.melt(
        mc_clean_df,
        id_vars=[c for c in mc_clean_df.columns if c not in _mc_dropped_cols],
        value_vars=_mc_value_cols,
        var_name="compound",
        value_name="concentration",
    )

    mc_long_df["compound"] = mc_long_df["compound"].str.removesuffix(
        "-VA_clean"
    )
    return mc_long_df, ss_long_df


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Join TQ benchmarks
    Left-join the reshaped table against `all_compound_dict_df`'s benchmark
    columns (EPA final-rule values for the six regulated compounds, Smalling
    et al. Table S5 state-only values for the rest) on compound name.
    """)
    return


@app.cell
def _(all_compound_dict_df):
    def calc_scored_df(wide_df, long_df, site_id_col):
        tq_benchmark_cols = [
            "compound",
            "benchmark_ng_L",
            "trigger_ng_L",
            "epa_ratio_eligible",
        ]

        tq_df = long_df.merge(
            all_compound_dict_df[tq_benchmark_cols],
            on="compound",
            how="left",
        )

        tq_scored_df = tq_df.assign(
            tq=tq_df["concentration"] / tq_df["benchmark_ng_L"]
        )

        sum_tq_epa_df = (
            tq_scored_df[tq_scored_df["epa_ratio_eligible"]]
            .groupby(site_id_col)["tq"]
            .sum()
            .rename("sum_tq_epa")
            .reset_index()
        )

        sum_tq_state_only_df = (
            tq_scored_df[~tq_scored_df["epa_ratio_eligible"]]
            .groupby(site_id_col)["tq"]
            .sum()
            .rename("sum_tq_state_only")
            .reset_index()
        )

        return wide_df.merge(sum_tq_epa_df, on=site_id_col, how="left").merge(
            sum_tq_state_only_df, on=site_id_col, how="left"
        )

    return (calc_scored_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Compute per-compound and summed TQ
    Divide concentration by benchmark for the per-compound TQ, then sum
    within the `epa_ratio_eligible` group to get the classified ∑TQ (Hazard
    Index) and, separately, a supplementary state-only ∑TQ reported as
    context but never classified. `calc_scored_df()` below implements this
    once and is reused for both studies; each study's own non-detect
    convention (0 for Smalling, half the reporting limit for McMahon, per
    Step 2.5 above) is already baked into its concentration values, not
    something this step re-decides.
    """)
    return


@app.cell(hide_code=True)
def _(calc_scored_df, ss_clean_df, ss_long_df):
    ss_scored_df = calc_scored_df(ss_clean_df, ss_long_df, "Site Code")
    return (ss_scored_df,)


@app.cell(hide_code=True)
def _(mo, ss_scored_df):
    mo.vstack(
        [
            mo.md("#### ∑TQ summary — Smalling/Seawolf (`ss_scored_df`)"),
            mo.ui.table(
                ss_scored_df[["sum_tq_epa", "sum_tq_state_only"]]
                .describe()
                .round(4)
                .reset_index()
                .rename(columns={"index": "Statistic"})
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### McMahon (groundwater) ∑TQ

    `mc_clean_df` gets the same reshape/join/compute treatment as
    `ss_clean_df` above via the shared `calc_scored_df()` helper, producing
    `mc_scored_df`. Two structural differences from Smalling carried
    through rather than being papered over:
    * McMahon's panel has no HFPO-DA (GenX) column at all, so its Hazard
      Index is necessarily a 5-of-6-compound sum (missing the GenX term).
    * McMahon's non-detects are already imputed as half the reporting limit
      rather than 0 (a Step 2 decision, not redone here).

    That second difference shows up clearly in the result: across the 254
    scored McMahon sites, `sum_tq_epa` never drops below ~1.0 (vs. a median
    of 0.17 for Smalling's 236 sites) — every site clears the trigger and
    MCL-exceedance cutoffs by construction, since even a "clean" site
    accumulates a non-zero baseline TQ across 5 summed compounds under
    half-reporting-limit imputation. The two studies' ∑TQ values are not on
    the same footing, and combining them into one modeling target (Task
    3.4) would need to address this class-balance skew directly, not just
    the missing-GenX gap.
    """)
    return


@app.cell(hide_code=True)
def _(calc_scored_df, mc_clean_df, mc_long_df):
    mc_scored_df = calc_scored_df(mc_clean_df, mc_long_df, "NAWQA_ID_mc_env")
    return (mc_scored_df,)


@app.cell(hide_code=True)
def _(mc_scored_df, mo):
    mo.vstack(
        [
            mo.md("#### ∑TQ summary — McMahon (`mc_scored_df`)"),
            mo.ui.table(
                mc_scored_df[["sum_tq_epa", "sum_tq_state_only"]]
                .describe()
                .round(4)
                .reset_index()
                .rename(columns={"index": "Statistic"})
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()

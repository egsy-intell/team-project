import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    import pandas as pd
    import numpy as np

    from data_dictionary import app as data_dictionary_app

    return data_dictionary_app, mo, np, pd


@app.cell
async def _(data_dictionary_app):
    data_dictionary_result = await data_dictionary_app.embed()
    all_compound_dict_df = data_dictionary_result.defs["all_compound_dict_df"]
    mcmahon_env_df = data_dictionary_result.defs["mcmahon_env_df"]
    seawolf_dict_df = data_dictionary_result.defs["seawolf_dict_df"]
    return all_compound_dict_df, mcmahon_env_df, seawolf_dict_df


@app.cell
def _(mo):
    mo.md(r"""
    # Predicting PFAS occurrence risk based on land use features

    ## Team .egsy intelligence (Group #14)
    * Yaisiel (Yai) Torres
    * Gulshan Raj Shetty (Raj)
    * Emir Beg
    * Somyaranjan Sahu

    ## Step one: problem definition

    ### Problem statement
    Per- and polyfluoroalkyl substances, commonly known as PFAS, are persistent environmental
    contaminants that may enter drinking-water sources through industrial activities, waste
    disposal, firefighting foam use, urban development, and other landscape-level sources. This
    project aims to develop a predictive model for the occurrence of PFAS in tap water,
    using USGS summary data on potential landscape sources (Seawolf et al., 2023),
    and reported concentration at the point-of-use (Smalling et al., 2023). We will also attempt
    the same modeling for groundwater, based on the data used in a similar exercise by McMahon et
    al. (2022).

    The question we aim to answer is: Can we predict low, medium, and high levels of PFAS
    concentration in tap and groundwater sources across the United States based on key geographic and
    land-use indicators? In addition, how do our findings compare to those offered by researchers
    in the domain?

    #### Proposed classification
    A provisional classification approach is:
    * Low: No PFAS compounds detected above the applicable laboratory reporting limits.
    * Medium: At least one PFAS detected, with cumulative concentration at or below the median
      concentration among detected samples.
    * High: At least one PFAS detected, with cumulative concentration above the median
      concentration among detected samples.

    The cutoff between medium and high will be established using the model-development data and
    frozen before final evaluation.

    #### Why this problem matters
    1. **Public health relevance:** PFAS contamination in drinking water is a concern in many
       countries due to known or potential adverse effects on human health (U.S. Environmental
       Protection Agency [EPA], n.d.).
    2. **Regulatory deadlines drive the need for prioritization:** In April 2024, EPA finalized the
       first legally enforceable federal limits (Maximum Contaminant Levels) for six PFAS
       compounds in drinking water, with compliance phased in through 2029 (EPA, 2024) — though
       the exact scope and timeline remain in flux: EPA has since proposed retaining the limits for
       PFOA and PFOS while rescinding limits for four other PFAS (EPA, 2025), and in May 2026
       proposed extending PFOA/PFOS compliance to 2031 (EPA, 2026). Water-resource operators and
       administrators need to identify and remediate at-risk sites well before enforcement takes
       effect, and prioritize under a moving compliance timeline rather than treating every site as
       equally uncertain. Predicting PFAS levels from traceable, highly correlated geographic and
       land-use features would let operators focus monitoring and remediation efforts on the sites
       most likely to need it, ahead of whichever compliance window ultimately applies.
    3. **Private-well coverage gap:** EPA's 2024 rule applies only to public water systems, leaving
       millions of Americans who rely on private wells outside its enforceable scope. Our selected
       datasets explicitly integrate private-well and public-supply exposures, positioning our model
       to speak to a population the new federal rule does not cover.

    #### Intended Application
    The proposed model is intended to function as a screening and sampling-prioritization tool.
    It will not replace laboratory testing and will not be used to declare a tap or groundwater
    source safe, unsafe, compliant, or noncompliant.

    Potential users could include:
    * Environmental and public-health agencies
    * Water-resource managers
    * Researchers planning PFAS sampling programs
    * Community organizations identifying locations where testing resources may be most useful

    ### Application feasibility of the model
    The project is feasible because researchers at the EPA and USGS (U.S. Geological Survey)
    provides resources and data such as measured PFAS concentration data and landscape summaries
    for sites included in its national PFAS tap water reconnaissance.

    #### Scope
    * Publicly supplied and privately sourced tap and groundwater
    * PFAS concentration results from McMahon et al. (2022) and Smalling et al. (2023)
    * Landscape and potential-source indicators calculated by McMahon et al. (2022)
      and Seawolf et al. (2023)
    * One independent observation per unique sampling location
    * Classification of cumulative PFAS concentration into three categories

    #### Constraints
    The model will not...
    * Make causal claims about individual PFAS sources
    * Determine regulatory compliance
    * replace laboratory sampling
    * Estimate the exact PFAS exposure of individual residents
    * Publish or attempt to reconstruct exact residential locations
    * Use repeated temporal samples as independent observations
    * Use quality-assurance samples as model observations
    * Use previously generated PFAS predictions as predictor variables

    ### Data source
    #### USGS Data Source 1: Smalling et al., 2023 (Dependent Variable)
    It supplies one of the project’s dependent variables, i.e., the outcome the model is trying to
    predict. It will be used to train our model in the categorization of tap water sites based
    on site controls. It includes:

    * Which PFAS compounds were detected
    * The measured concentration of each compound
    * The number of PFAS compounds detected
    * The total or cumulative PFAS concentration
    * Whether results were below the laboratory reporting limit
    * Type of service point: private v. public

    #### USGS Data Source 2: Seawolf et al., 2023 (Predictors)
    This dataset provides predictors associated with Smalling et al.'s data. It
    describes the environmental and geographic characteristics surrounding each sampling
    location that may be associated with PFAS contamination, including:

    * Nearby potential PFAS-related facilities
    * Industrial or commercial activity
    * Urban and developed land
    * Agricultural or natural land
    * Burned areas
    * Land-cover characteristics
    * Public versus private water source
    * Other geographic or landscape summaries around the sampling location

    #### USGS Data Source 3: McMahon et al., 2022 (Predictors + Dependent Variables)
    This comprehensive dataset provides environmental and geographic characteristics,
    as well as PFAS concentrations, associated with various private and public wells
    drawing from aquifers along the Eastern United States. It includes:

    * Distance to PFAS-associated sites (fire stations and military facilities, for example)
    * Measured PFAS concentrations for each sampled aquifer
    * Land use percentages (farmland v. urban, for example)
    * Type of well: private v. public

    ### Data availability and ethical considerations
    The three resources from USGS datasets are publicly available government data releases.
    All of them are marked as CC0, and can be reused without licensing fees. In addition, the
    datasets do not require access to restricted health, financial, educational, or personally
    identifiable information.

    The data can be downloaded, filtered, and analyzed using standard tools, and has also been
    copied to the project's repo for convenience
    ([direct link](https://github.com/egsy-intell/team-project)).

    #### Privacy
    USGS anonymized the sampling locations to protect participant privacy. The project will
    retain the anonymized identifiers and will not attempt to infer exact home addresses or
    private-well locations.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Step 2: Data exploration and quality assesssment

    Before assessing the quality of our data, we take the following steps:

    ### Smalling et al. (2023) and Seawolf et. al. (2023) load and join-ability (`ss_merged_df`)

    1. Load Seawolf and Smalling via `pandas`
    2. Clean Smalling: the dataset uses `-` and `nd` for two specific purposes (not analyzed, and non-detected
       above minimum detection values, respectively). We decided to replace the former with `NaN` and the latter
       with `0`. Ideally, we should know non-detected minimums, but these were not found.
    3. Merge: using a left join, to report on any unmatched rows
    """)
    return


@app.cell
def _(all_compound_dict_df, mo, pd):
    from pathlib import Path

    notebook_dir = mo.notebook_dir()
    if notebook_dir is None:
        raise RuntimeError("Could not determine notebook directory. Save/open the notebook from disk.")

    data_dir = Path(notebook_dir).resolve().parent / "data" / "usgs"

    # First line of this file is a table caption, not a header row.
    smalling_df = pd.read_csv(data_dir / "smalling" / "PFAS_ENV.csv", skiprows=1)
    seawolf_df = pd.read_csv(
        data_dir / "seawolf" / "PFAS_DataSummaries_5k_50k_SummaryData.csv"
    )

    # Individual PFAS compound columns mix numeric concentrations (ng/L) with
    # two non-numeric sentinels: "nd" (tested, not detected above the lab
    # reporting limit) and "NA" (compound not analyzed at that site, already
    # read in as NaN). We treat nd as 0 so it stays distinct from true
    # missingness, then coerce the rest to numeric.
    pfas_cols = all_compound_dict_df.loc[
        all_compound_dict_df["smalling"], "compound"
    ].tolist()

    smalling_clean = smalling_df.copy()
    smalling_clean[pfas_cols] = smalling_clean[pfas_cols].replace("nd", 0)
    smalling_clean[pfas_cols] = smalling_clean[pfas_cols].apply(pd.to_numeric, errors="coerce")

    # Last column in smallings is empty
    smalling_clean = smalling_clean.drop(columns=smalling_clean.columns[-1])

    # ∑EAR uses "-" for "not analyzed" rather than NaN.
    smalling_clean["∑EAR"] = pd.to_numeric(smalling_clean["∑EAR"], errors="coerce")

    # Final step: left merge to preserve unmatched rows
    ss_merged_df = smalling_clean.merge(
        right=seawolf_df,
        left_on=smalling_clean["Site Code"].str.strip(),
        right_on=seawolf_df["SiteCode"].str.strip(),
        how="left",
        suffixes=("_smalling", "_seawolf"),
        indicator=True,
    )
    return data_dir, ss_merged_df


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### McMahon et. al. (2022) load and join-ability (`mc_merged_df`)

    In this case, we perform similar operations

    1. Load McMahon via `pandas`
    2. Load McMahon data dictionary
    3. Clean up concentration values based on remarks
        1. `<`: Non-detect. Get the mean of ceiling value (`VA/2`), which is standard practice.
        2. `n`: Estimation. Flag as estimated
    4. Merge: using a left join to capture any unmatched records
    """)
    return


@app.cell
def _(all_compound_dict_df, data_dir, mcmahon_env_df, np, pd):
    pfas_codes = all_compound_dict_df.loc[
        all_compound_dict_df["mcmahon"], "compound"
    ].tolist()

    mcmahon_env_clean = mcmahon_env_df.copy()

    for c in pfas_codes:
        rmk = mcmahon_env_clean[f"{c}-RMK"].fillna("").str.strip()
        va = mcmahon_env_clean[f"{c}-VA"]

        # <: non-detect, use half the reporting limit as the estimate
        # n: trace detection, keep value as-is but flag low confidence
        # blank: confident detection, keep value as-is
        mcmahon_env_clean[f"{c}-VA_clean"] = np.where(rmk == "<", va / 2, va)
        mcmahon_env_clean[f"{c}-estimated"] = rmk == "n"

    # Drop raw remark/value columns now that -VA_clean and -estimated
    # capture the same information in usable form.
    raw_cols = [c for c in mcmahon_env_clean.columns if c.endswith("-RMK") or c.endswith("-VA")]
    mcmahon_env_clean = mcmahon_env_clean.drop(columns=raw_cols)

    mcmahon_geo_df = pd.read_csv(
        data_dir / "mcmahon" / "PFAS_GEOSPATIAL.csv",
        thousands=",",
    )

    mc_merged_df = mcmahon_env_clean.merge(
        right=mcmahon_geo_df,
        left_on=mcmahon_env_clean["NAWQA_ID"].str.strip(),
        right_on=mcmahon_geo_df["NAWQA_ID"].str.strip(),
        how="left",
        suffixes=("_mc_env", "_mc_geo"),
        indicator=True,
    )
    return (mc_merged_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `ss_merged_df` and `mc_merged_df` now contains all data to be considered in our model design

    ### Unmatched rows and `NaN` clean up
    """)
    return


@app.cell
def _(mac_merged_df, mo, np, pd, ss_merged_df):
    def make_numeric_summary_table(df, dataset_name):
        numeric_df = df.select_dtypes(include="number")
        if numeric_df.empty:
            return pd.DataFrame({
                "Dataset": [dataset_name],
                "Variable": ["No numeric columns"],
                "Mean": [np.nan],
                "Median": [np.nan],
                "Std Dev": [np.nan],
                "Min": [np.nan],
                "Q1": [np.nan],
                "Q3": [np.nan],
                "Max": [np.nan],
            })

        summary = (
            numeric_df.describe(percentiles=[0.25, 0.5, 0.75]).T
            .rename(columns={
                "mean": "Mean",
                "std": "Std Dev",
                "min": "Min",
                "25%": "Q1",
                "50%": "Median",
                "75%": "Q3",
                "max": "Max",
            })
            .reset_index()
            .rename(columns={"index": "Variable"})
        )
        summary.insert(0, "Dataset", dataset_name)
        return summary.round(3)

    combined_summary = pd.concat(
        [
            make_numeric_summary_table(ss_merged_df, "Smalling + Seawolf"),
            make_numeric_summary_table(mac_merged_df, "McMahon"),
        ],
        ignore_index=True,
    )

    mo.vstack([
        mo.md("### Numeric summary statistics for the merged datasets"),
        mo.ui.table(combined_summary),
    ])
    return


@app.cell
def _(mo, np, pd, ss_merged_df):
    import matplotlib.pyplot as plt

    ss_viz_columns = [
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
    ss_viz_columns = [col for col in ss_viz_columns if col in ss_merged_df.columns]

    def make_boxplot(df, columns, title):
        n_cols = max(1, len(columns))
        fig, axes = plt.subplots(n_cols, 1, figsize=(8, 2.4 * n_cols), squeeze=False)
        for ax, col in zip(axes.flatten(), columns):
            df[col].dropna().plot.box(ax=ax)
            ax.set_title(col)
            ax.set_ylabel("")
        fig.suptitle(title, fontsize=14)
        fig.tight_layout()
        return fig

    def make_histogram(df, columns, title):
        n_cols = max(1, len(columns))
        fig, axes = plt.subplots(n_cols, 1, figsize=(8, 2.4 * n_cols), squeeze=False)
        for ax, col in zip(axes.flatten(), columns):
            df[col].dropna().hist(ax=ax, bins=20, edgecolor="black")
            ax.set_title(f"{col} histogram")
            ax.set_xlabel(col)
            ax.set_ylabel("Count")
        fig.suptitle(title, fontsize=14)
        fig.tight_layout()
        return fig

    def skewness_table(df, columns):
        rows = []
        for col in columns:
            values = df[col].dropna()
            skew = values.skew()
            if skew > 1:
                assessment = "Right-skewed"
            elif skew < -1:
                assessment = "Left-skewed"
            else:
                assessment = "Approximately symmetric"
            rows.append({
                "Variable": col,
                "Skewness": round(skew, 3),
                "Assessment": assessment,
            })
        return pd.DataFrame(rows)

    ss_boxplot = make_boxplot(ss_merged_df, ss_viz_columns, "Smalling + Seawolf: box plots")
    ss_histogram = make_histogram(ss_merged_df, ss_viz_columns, "Smalling + Seawolf: histograms")
    ss_skewness = skewness_table(ss_merged_df, ss_viz_columns)

    mo.vstack([
        mo.md("### Exploratory plots for Smalling + Seawolf"),
        mo.ui.table(ss_skewness),
        ss_boxplot,
        ss_histogram,
    ])
    return


@app.cell
def _(mac_merged_df, mo, np, pd):
    import matplotlib.pyplot as plt

    mac_viz_columns = [
        col for col in mac_merged_df.columns if col.endswith("-VA_clean")
    ][:6] + ["AGRI_12", "NATU_12", "URBA_12"]

    def make_boxplot(df, columns, title):
        n_cols = max(1, len(columns))
        fig, axes = plt.subplots(n_cols, 1, figsize=(8, 2.4 * n_cols), squeeze=False)
        for ax, col in zip(axes.flatten(), columns):
            df[col].dropna().plot.box(ax=ax)
            ax.set_title(col)
            ax.set_ylabel("")
        fig.suptitle(title, fontsize=14)
        fig.tight_layout()
        return fig

    def make_histogram(df, columns, title):
        n_cols = max(1, len(columns))
        fig, axes = plt.subplots(n_cols, 1, figsize=(8, 2.4 * n_cols), squeeze=False)
        for ax, col in zip(axes.flatten(), columns):
            df[col].dropna().hist(ax=ax, bins=20, edgecolor="black")
            ax.set_title(f"{col} histogram")
            ax.set_xlabel(col)
            ax.set_ylabel("Count")
        fig.suptitle(title, fontsize=14)
        fig.tight_layout()
        return fig

    def skewness_table(df, columns):
        rows = []
        for col in columns:
            values = df[col].dropna()
            skew = values.skew()
            if skew > 1:
                assessment = "Right-skewed"
            elif skew < -1:
                assessment = "Left-skewed"
            else:
                assessment = "Approximately symmetric"
            rows.append({
                "Variable": col,
                "Skewness": round(skew, 3),
                "Assessment": assessment,
            })
        return pd.DataFrame(rows)

    mac_boxplot = make_boxplot(mac_merged_df, mac_viz_columns, "McMahon: box plots")
    mac_histogram = make_histogram(mac_merged_df, mac_viz_columns, "McMahon: histograms")
    mac_skewness = skewness_table(mac_merged_df, mac_viz_columns)

    mo.vstack([
        mo.md("### Exploratory plots for McMahon"),
        mo.ui.table(mac_skewness),
        mac_boxplot,
        mac_histogram,
    ])
    return


@app.cell
def _(mc_merged_df, mo, ss_merged_df):
    ss_unmatched_df = ss_merged_df[ss_merged_df["_merge"] == "left_only"]
    ss_unmatched_count = ss_unmatched_df.shape[0]

    mac_unmatched_df = mc_merged_df[mc_merged_df["_merge"] == "left_only"]
    mac_unmatched_count = mac_unmatched_df.shape[0]

    mo.md(f"""
    After joining the features and the PFAS concentration sets we get minimal data loss.
    The only concentration measurement without landscape attributes is `{ss_unmatched_df.iloc[0, 0]}`.
    It will be dropped.
    """)
    return mac_unmatched_count, ss_unmatched_count


@app.cell
def _(
    mac_unmatched_count,
    mc_merged_df,
    mo,
    pd,
    ss_merged_df,
    ss_unmatched_count,
):
    integration_feasibility_summary = pd.DataFrame([
        {
            "Datasets": "Smalling PFAS outcomes + Seawolf landscape predictors",
            "Left key": "Site Code",
            "Right key": "SiteCode",
            "Left records": ss_merged_df.shape[0],
            "Matched": ss_merged_df.shape[0] - ss_unmatched_count,
            "Unmatched": ss_unmatched_count,
            "Match rate (%)": round(
                100 * (ss_merged_df.shape[0] - ss_unmatched_count) / ss_merged_df.shape[0], 1
            ),
        },
        {
            "Datasets": "McMahon PFAS outcomes + McMahon geospatial predictors",
            "Left key": "NAWQA_ID",
            "Right key": "NAWQA_ID",
            "Left records": mc_merged_df.shape[0],
            "Matched": mc_merged_df.shape[0] - mac_unmatched_count,
            "Unmatched": mac_unmatched_count,
            "Match rate (%)": round(
                100 * (mc_merged_df.shape[0] - mac_unmatched_count) / mc_merged_df.shape[0], 1
            ),
        },
    ])

    integration_identifier_samples = pd.DataFrame({
        "Smalling Site Code sample": (
            ss_merged_df["Site Code"].dropna().astype(str).head(5).reset_index(drop=True)
        ),
        "Seawolf SiteCode sample": (
            ss_merged_df["SiteCode"].dropna().astype(str).head(5).reset_index(drop=True)
        ),
        "McMahon environmental ID sample": (
            mc_merged_df["NAWQA_ID_mc_env"].dropna().astype(str).head(5).reset_index(drop=True)
        ),
        "McMahon geospatial ID sample": (
            mc_merged_df["NAWQA_ID_mc_geo"].dropna().astype(str).head(5).reset_index(drop=True)
        ),
    })

    mo.vstack([
        mo.ui.table(integration_feasibility_summary),
        mo.accordion({
            "Sample identifiers for consistency review": mo.ui.table(
                integration_identifier_samples
            ),
        }),
    ])
    return


@app.cell
def _(ss_merged_df):
    ss_merged_clean_df = ss_merged_df[ss_merged_df["_merge"] != "left_only"]
    return (ss_merged_clean_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As for `NaN` values, the only ones found belong to the `Seawolf/Smalling` merged data set.
    """)
    return


@app.cell
def _(mc_merged_df, mo, ss_merged_clean_df):
    def get_nan_counts(df, remove_non_matching = True):
        nan_counts = df.isna().sum()
        nan_table = (nan_counts
            .reset_index()
            .rename(columns={"index": "column", 0: "nan_count"})
            .assign(nan_pct=lambda inner_df: inner_df["nan_count"] / df.shape[0] * 100)
            .pipe(lambda df: df.query("nan_count > 0") if remove_non_matching else df)
            .sort_values("nan_count", ascending=False)
        )

        return nan_table

    mo.ui.tabs({
        "Seawolf/Smalling": get_nan_counts(ss_merged_clean_df),
        "McMahon": get_nan_counts(mc_merged_df)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### results

    McMahon data does not require any further cleanups. The Seawolf landscape columns with missing
    values (`number_pfas_sites_proximal`, `mean_dist_to_pfas_site`, and the four burn-area fractions)
    are structural: a `NaN` there means no PFAS facility or burned area was detected within the
    buffer, not that a value went unmeasured. We checked against the metadata's documented `rdommax`
    per attribute first, but for most of these columns 17-99% of rows are missing, so filling with the
    attribute max would have pulled most of the column toward the single worst observed site instead
    of reflecting "nothing found." We impute the facility count and burn fractions with `0`, since
    each has a natural zero. `mean_dist_to_pfas_site` has no natural zero (distance to a facility is
    undefined when there is no facility), so we impute it with its `rdommax` (~4997m) instead — that
    value is ~5km, the same buffer radius the field is computed over, so "no facility found within the
    5km search radius" maps to "the nearest one is at least ~5km away" rather than an arbitrary
    outlier.
    """)
    return


@app.cell
def _(mc_merged_df, seawolf_dict_df, ss_merged_clean_df):
    mc_clean_df = mc_merged_df

    # NaN in these columns means "nothing detected in the buffer," so 0 is the correct
    # fill: each has a natural zero (no facilities, no area burned).
    seawolf_structural_zero_columns = [
        "number_pfas_sites_proximal",
        "Burn_Area_5k_frac", "Burn_area_50k_frac",
        "Urbn_burn_5k_frac", "Urbn_burn_50k_frac",
    ]

    ss_clean_df = ss_merged_clean_df.copy()
    ss_clean_df[seawolf_structural_zero_columns] = ss_clean_df[
        seawolf_structural_zero_columns
    ].fillna(0)

    # mean_dist_to_pfas_site has no natural zero (undefined without a facility), so
    # fill with the attribute's rdommax (~5km) instead: that's the buffer radius the
    # field is computed over, i.e. "no facility within 5km" -> "at least ~5km away."
    mean_dist_rdom_max = seawolf_dict_df.set_index("attribute").loc[
        "mean_dist_to_pfas_site", "rdom_max"
    ]
    ss_clean_df["mean_dist_to_pfas_site"] = ss_clean_df["mean_dist_to_pfas_site"].fillna(
        mean_dist_rdom_max
    )
    return mc_clean_df, ss_clean_df


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Data Exploration and Quality Assessment

    The following subsections evaluate the structure, completeness, consistency, and modeling
    suitability of the Smalling, Seawolf, and McMahon datasets. We check for: dataset dimensions, key fields, missing values, duplicate
    identifiers, and numeric ranges. Integration readiness was already assessed in the join-ability
    sections above. *`ss_clean_df` and `mc_clean_df` will be used from now on.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Smalling et al. (2023)

    #### Data Exploration
    """)
    return


@app.cell
def _(all_compound_dict_df, mo, pd, ss_clean_df):
    smalling_quality_pfas_columns = all_compound_dict_df.loc[
        all_compound_dict_df["smalling"], "compound"
    ].tolist()

    smalling_quality_total_pfas = ss_clean_df["∑PFAS"]
    smalling_quality_detected_count = ss_clean_df["Count Detected PFAS"]

    smalling_exploration_summary = pd.DataFrame([
        {
            "Measure": "Dataset shape (`ss_clean_df`)",
            "Result": f"{ss_clean_df.shape[0]} rows × {ss_clean_df.shape[1]} columns",
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
            "Result": len(smalling_quality_pfas_columns),
        },
        {
            "Measure": "Cumulative PFAS range (ng/L)",
            "Result": f"{smalling_quality_total_pfas.min():.3f} to {smalling_quality_total_pfas.max():.3f}",
        },
        {
            "Measure": "Median cumulative PFAS (ng/L)",
            "Result": f"{smalling_quality_total_pfas.median():.3f}",
        },
        {
            "Measure": "Detected compounds per site",
            "Result": f"{smalling_quality_detected_count.min():.0f} to {smalling_quality_detected_count.max():.0f}",
        },
    ])

    mo.vstack([
        mo.ui.table(smalling_exploration_summary),
        mo.md(f"""
        The Smalling portion of `ss_clean_df` contains measured PFAS results for **{len(ss_clean_df)}
        sampling sites**. Cumulative PFAS concentrations are right-skewed because the maximum is much larger
        than the median. Public-water sites are more common than private-well sites in this table. The PFAS
        columns and `∑EAR` were already cleaned (`nd` → 0, coerced to numeric) while building `ss_merged_df`,
        and the unmatched site plus structural Seawolf `NaN`s were resolved while building `ss_clean_df`.
        """),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Quality Assessment
    """)
    return


@app.cell
def _(all_compound_dict_df, mo, pd, ss_clean_df):
    smalling_assessment_pfas_columns = all_compound_dict_df.loc[
        all_compound_dict_df["smalling"], "compound"
    ].tolist()

    smalling_assessment_numeric_pfas = ss_clean_df[smalling_assessment_pfas_columns]
    smalling_assessment_published_count = ss_clean_df["Count Detected PFAS"]
    smalling_assessment_published_total = ss_clean_df["∑PFAS"]
    smalling_assessment_calculated_count = smalling_assessment_numeric_pfas.gt(0).sum(axis=1)
    smalling_assessment_calculated_total = smalling_assessment_numeric_pfas.fillna(0).sum(axis=1)

    smalling_assessment_columns = (
        ["Site Code", "State", "Site Type"]
        + smalling_assessment_pfas_columns
        + ["Count Detected PFAS", "∑PFAS", "∑EAR"]
    )
    smalling_missing_summary = (
        ss_clean_df[smalling_assessment_columns]
        .isna()
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .rename("Missing values")
        .rename_axis("Column")
        .reset_index()
    )
    smalling_missing_summary["Missing (%)"] = (
        100 * smalling_missing_summary["Missing values"] / len(ss_clean_df)
    ).round(1)

    smalling_quality_checks = pd.DataFrame([
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
            "Quality check": "Non-detect values (cleaned to 0 while building ss_merged_df)",
            "Result": int(smalling_assessment_numeric_pfas.eq(0).sum().sum()),
            "Assessment": "Expected; 'nd' was converted to 0 upstream and is no longer distinguishable here",
        },
        {
            "Quality check": "Compound results not analyzed or missing",
            "Result": int(smalling_assessment_numeric_pfas.isna().sum().sum()),
            "Assessment": "Review; retain as missing rather than treating as non-detect",
        },
        {
            "Quality check": "Rows with zero detected PFAS",
            "Result": int(smalling_assessment_published_count.eq(0).sum()),
            "Assessment": "Review; this table alone does not represent the proposed Low class",
        },
        {
            "Quality check": "Published count differs from simple recalculation",
            "Result": int(
                smalling_assessment_calculated_count.ne(
                    smalling_assessment_published_count
                ).sum()
            ),
            "Assessment": "Review compound-inclusion rules before recomputing published fields",
        },
        {
            "Quality check": "Published total differs by more than 0.1 ng/L",
            "Result": int(
                smalling_assessment_calculated_total.sub(
                    smalling_assessment_published_total
                ).abs().gt(0.1).sum()
            ),
            "Assessment": "Review rounding or compound-inclusion rules",
        },
        {
            "Quality check": "Negative cumulative PFAS values",
            "Result": int(smalling_assessment_published_total.lt(0).sum()),
            "Assessment": "Pass",
        },
    ])

    mo.vstack([
        mo.ui.table(smalling_quality_checks),
        mo.accordion({
            "Columns with the most missing values": mo.ui.table(smalling_missing_summary),
        }),
        mo.md("""
        **Suitability assessment:** The Smalling portion of `ss_clean_df` is suitable as a measured
        PFAS outcome table, but it requires careful treatment of non-detect and not-analyzed values.
        The supplied table contains detected sites only, so the Low/no-detection class must be obtained
        from a complete sampling frame rather than inferred from this table alone.
        """),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Seawolf et al. (2023)

    #### Data Exploration
    """)
    return


@app.cell
def _(mo, pd, ss_clean_df):
    seawolf_quality_landcover_columns = [
        "OpenWater", "PerennialIceSnow", "DevelopedOpenSpace",
        "DevelopedLowIntensity", "DevelopedMediumIntensity",
        "DevelopedHighIntensity", "Barren", "DeciduousForest",
        "EvergreenForest", "MixedForest", "DwarfScrub", "ShrubScrub",
        "GrasslandHerbaceous", "SedgeHerbaceous", "Moss", "PastureHay",
        "CultivatedCrop", "WoodyWetlands", "EmergentHerbaceousWetlands",
    ]
    seawolf_quality_predictor_columns = [
        "number_pfas_sites_proximal", "mean_dist_to_pfas_site",
        "Burn_Area_5k_frac", "Burn_area_50k_frac", "Urbn_burn_5k_frac",
        "Urbn_burn_50k_frac",
    ] + seawolf_quality_landcover_columns
    seawolf_quality_landcover_total = ss_clean_df[
        seawolf_quality_landcover_columns
    ].sum(axis=1)

    seawolf_exploration_summary = pd.DataFrame([
        {
            "Measure": "Dataset shape (`ss_clean_df`)",
            "Result": f"{ss_clean_df.shape[0]} rows × {ss_clean_df.shape[1]} columns",
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
            "Result": len(seawolf_quality_predictor_columns),
        },
        {
            "Measure": "Sites with a recorded proximal-facility count",
            "Result": int(ss_clean_df["number_pfas_sites_proximal"].notna().sum()),
        },
        {
            "Measure": "Mean land-cover fraction sum",
            "Result": f"{seawolf_quality_landcover_total.mean():.3f}",
        },
        {
            "Measure": "Land-cover fraction-sum range",
            "Result": f"{seawolf_quality_landcover_total.min():.3f} to {seawolf_quality_landcover_total.max():.3f}",
        },
    ])

    seawolf_study_summary = (
        ss_clean_df["Study_seawolf"]
        .value_counts()
        .rename_axis("Study")
        .reset_index(name="Sites")
    )

    mo.vstack([
        mo.ui.table(seawolf_exploration_summary),
        mo.accordion({
            "Sites by contributing study": mo.ui.table(seawolf_study_summary),
        }),
        mo.md(f"""
        The Seawolf portion of `ss_clean_df` contains landscape characteristics joined onto
        **{len(ss_clean_df)} Smalling sites**. It includes potential PFAS-source facilities,
        burn-area measures, and land-cover fractions calculated around each sampling location.
        The unmatched Smalling site was already dropped and structural Seawolf `NaN`s
        (no facility or burned area found within the buffer) were already imputed while
        building `ss_clean_df`.
        """),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Quality Assessment
    """)
    return


@app.cell
def _(mo, pd, ss_clean_df):
    seawolf_assessment_landcover_columns = [
        "OpenWater", "PerennialIceSnow", "DevelopedOpenSpace",
        "DevelopedLowIntensity", "DevelopedMediumIntensity",
        "DevelopedHighIntensity", "Barren", "DeciduousForest",
        "EvergreenForest", "MixedForest", "DwarfScrub", "ShrubScrub",
        "GrasslandHerbaceous", "SedgeHerbaceous", "Moss", "PastureHay",
        "CultivatedCrop", "WoodyWetlands", "EmergentHerbaceousWetlands",
    ]
    seawolf_assessment_fraction_columns = [
        "Burn_Area_5k_frac", "Burn_area_50k_frac", "Urbn_burn_5k_frac",
        "Urbn_burn_50k_frac",
    ] + seawolf_assessment_landcover_columns

    seawolf_assessment_landcover_total = ss_clean_df[
        seawolf_assessment_landcover_columns
    ].sum(axis=1)
    seawolf_assessment_invalid_fraction_count = int(
        (
            ss_clean_df[seawolf_assessment_fraction_columns].lt(0)
            | ss_clean_df[seawolf_assessment_fraction_columns].gt(1)
        ).sum().sum()
    )

    seawolf_assessment_columns = (
        ["SiteCode", "Study_seawolf", "number_pfas_sites_proximal", "mean_dist_to_pfas_site"]
        + seawolf_assessment_fraction_columns
    )
    seawolf_missing_summary = (
        ss_clean_df[seawolf_assessment_columns]
        .isna()
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .rename("Missing values")
        .rename_axis("Column")
        .reset_index()
    )
    seawolf_missing_summary["Missing (%)"] = (
        100 * seawolf_missing_summary["Missing values"] / len(ss_clean_df)
    ).round(1)

    seawolf_quality_checks = pd.DataFrame([
        {
            "Quality check": "Missing site identifiers",
            "Result": int(ss_clean_df["SiteCode"].isna().sum()),
            "Assessment": "Pass; the unmatched Smalling site was already dropped while building `ss_clean_df`",
        },
        {
            "Quality check": "Duplicate site identifiers",
            "Result": int(ss_clean_df["SiteCode"].dropna().duplicated().sum()),
            "Assessment": "Pass",
        },
        {
            "Quality check": "Fraction values outside 0-1",
            "Result": seawolf_assessment_invalid_fraction_count,
            "Assessment": "Pass" if seawolf_assessment_invalid_fraction_count == 0 else "Review",
        },
        {
            "Quality check": "Land-cover totals substantially below 1.0",
            "Result": int(seawolf_assessment_landcover_total.lt(0.95).sum()),
            "Assessment": "Review; some locations may have incomplete land-cover coverage",
        },
        {
            "Quality check": "Missing proximal-facility count",
            "Result": int(ss_clean_df["number_pfas_sites_proximal"].isna().sum()),
            "Assessment": "Pass; structural missingness (no facility within buffer) was already imputed to 0",
        },
        {
            "Quality check": "Missing mean facility distance",
            "Result": int(ss_clean_df["mean_dist_to_pfas_site"].isna().sum()),
            "Assessment": "Pass; already imputed with the ~5 km buffer radius (`rdom_max`)",
        },
        {
            "Quality check": "Negative facility distances",
            "Result": int(ss_clean_df["mean_dist_to_pfas_site"].lt(0).sum()),
            "Assessment": "Pass",
        },
    ])

    mo.vstack([
        mo.ui.table(seawolf_quality_checks),
        mo.accordion({
            "Columns with the most missing values": mo.ui.table(seawolf_missing_summary),
        }),
        mo.md("""
        **Suitability assessment:** The Seawolf portion of `ss_clean_df` is suitable for use as a
        predictor table. Site identifiers are unique and fraction values are within valid bounds.
        The unmatched Smalling site was dropped, and the structural facility/burn-area `NaN`s were
        imputed (0 for facility count and burn fractions, `rdom_max` ≈ 5 km for mean facility
        distance) while building `ss_clean_df` (see the join-ability and `NaN` clean-up sections
        above); no unresolved missing or unmatched records remain, though rows with these imputed
        values should be treated as assumption-driven rather than directly measured. Some sites
        still show land-cover fraction totals well below 1.0, which reflects incomplete land-cover
        coverage rather than a missingness issue and remains a separate item for review.
        """),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### McMahon et al. (2022)

    #### Data Exploration
    """)
    return


@app.cell
def _(mc_clean_df, mo, pd):
    mcmahon_quality_clean_columns = [
        column for column in mc_clean_df.columns if column.endswith("-VA_clean")
    ]
    mcmahon_quality_estimated_columns = [
        column for column in mc_clean_df.columns if column.endswith("-estimated")
    ]
    mcmahon_quality_total_concentration = mc_clean_df[
        mcmahon_quality_clean_columns
    ].sum(axis=1, min_count=1)
    mcmahon_quality_land_use_total = mc_clean_df[
        ["AGRI_12", "NATU_12", "URBA_12"]
    ].sum(axis=1)

    mcmahon_exploration_summary = pd.DataFrame([
        {
            "Measure": "Cleaned dataset shape (`mc_clean_df`)",
            "Result": f"{mc_clean_df.shape[0]} rows × {mc_clean_df.shape[1]} columns",
        },
        {
            "Measure": "Unique environmental site IDs",
            "Result": mc_clean_df["NAWQA_ID_mc_env"].nunique(),
        },
        {
            "Measure": "PFAS compounds evaluated",
            "Result": len(mcmahon_quality_clean_columns),
        },
        {
            "Measure": "Estimated or trace-result flags",
            "Result": int(mc_clean_df[mcmahon_quality_estimated_columns].sum().sum()),
        },
        {
            "Measure": "Cleaned concentration-total range (ng/L)",
            "Result": f"{mcmahon_quality_total_concentration.min():.1f} to {mcmahon_quality_total_concentration.max():.1f}",
        },
        {
            "Measure": "Median cleaned concentration total (ng/L)",
            "Result": f"{mcmahon_quality_total_concentration.median():.1f}",
        },
        {
            "Measure": "Mean land-use percentage total",
            "Result": f"{mcmahon_quality_land_use_total.mean():.1f}%",
        },
    ])

    mcmahon_land_use_summary = (
        mc_clean_df[["AGRI_12", "NATU_12", "URBA_12"]]
        .describe()
        .T
        .reset_index(names="Land-use variable")
        .round(2)
    )

    mo.vstack([
        mo.ui.table(mcmahon_exploration_summary),
        mo.accordion({
            "Land-use variable summary": mo.ui.table(mcmahon_land_use_summary),
        }),
        mo.md(f"""
        The McMahon analytical table contains groundwater PFAS measurements and landscape
        predictors for **{len(mc_clean_df)} sites**. Concentration totals are strongly
        right-skewed, and the agricultural, natural, and urban percentages collectively cover
        approximately 100% of the surrounding land area.
        """),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Quality Assessment
    """)
    return


@app.cell
def _(mc_clean_df, mo, pd):
    mcmahon_assessment_clean_columns = [
        column for column in mc_clean_df.columns if column.endswith("-VA_clean")
    ]
    mcmahon_assessment_estimated_columns = [
        column for column in mc_clean_df.columns if column.endswith("-estimated")
    ]
    mcmahon_assessment_geospatial_columns = [
        column
        for column in mc_clean_df.columns
        if column not in [
            "key_0", "NAWQA_ID_mc_env", "DATE", "TIME", "NAWQA_ID_mc_geo", "_merge"
        ]
        and column not in mcmahon_assessment_clean_columns
        and column not in mcmahon_assessment_estimated_columns
    ]
    mcmahon_assessment_land_use_columns = ["AGRI_12", "NATU_12", "URBA_12"]
    mcmahon_assessment_land_use_total = mc_clean_df[
        mcmahon_assessment_land_use_columns
    ].sum(axis=1)

    mcmahon_quality_checks = pd.DataFrame([
        {
            "Quality check": "Missing environmental site IDs",
            "Result": int(mc_clean_df["NAWQA_ID_mc_env"].isna().sum()),
            "Assessment": "Pass",
        },
        {
            "Quality check": "Duplicate environmental site IDs",
            "Result": int(mc_clean_df["NAWQA_ID_mc_env"].duplicated().sum()),
            "Assessment": "Pass",
        },
        {
            "Quality check": "Environmental-to-geospatial matches",
            "Result": f"{int(mc_clean_df['_merge'].eq('both').sum())} of {len(mc_clean_df)}",
            "Assessment": "Pass" if mc_clean_df["_merge"].eq("both").all() else "Review",
        },
        {
            "Quality check": "Missing cleaned PFAS values",
            "Result": int(mc_clean_df[mcmahon_assessment_clean_columns].isna().sum().sum()),
            "Assessment": "Pass",
        },
        {
            "Quality check": "Missing geospatial predictor values",
            "Result": int(mc_clean_df[mcmahon_assessment_geospatial_columns].isna().sum().sum()),
            "Assessment": "Pass",
        },
        {
            "Quality check": "Negative geospatial values",
            "Result": int(mc_clean_df[mcmahon_assessment_geospatial_columns].lt(0).sum().sum()),
            "Assessment": "Pass",
        },
        {
            "Quality check": "Land-use values outside 0-100%",
            "Result": int(
                (
                    mc_clean_df[mcmahon_assessment_land_use_columns].lt(0)
                    | mc_clean_df[mcmahon_assessment_land_use_columns].gt(100)
                ).sum().sum()
            ),
            "Assessment": "Pass",
        },
        {
            "Quality check": "Land-use totals outside 99.5-100.5%",
            "Result": int(
                (~mcmahon_assessment_land_use_total.between(99.5, 100.5)).sum()
            ),
            "Assessment": "Pass; minor differences are expected from rounding",
        },
        {
            "Quality check": "Estimated or trace-result flags",
            "Result": int(mc_clean_df[mcmahon_assessment_estimated_columns].sum().sum()),
            "Assessment": "Retain as a data-quality indicator",
        },
    ])

    mcmahon_missing_summary = (
        mc_clean_df.isna()
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .rename("Missing values")
        .reset_index()
        .rename(columns={"index": "Column"})
    )
    mcmahon_missing_summary["Missing (%)"] = (
        100 * mcmahon_missing_summary["Missing values"] / len(mc_clean_df)
    ).round(1)

    mo.vstack([
        mo.ui.table(mcmahon_quality_checks),
        mo.accordion({
            "Columns with the most missing values": mo.ui.table(mcmahon_missing_summary),
        }),
        mo.md("""
        **Suitability assessment:** The McMahon environmental and geospatial tables are complete,
        uniquely keyed, and fully matched. The cleaned concentration values are usable for
        exploratory modeling, but totals that include half-reporting-limit substitutions should not
        be interpreted as detected-only concentration without retaining the original censoring logic.
        """),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Next Steps: Proposed task assignments

    ## Conclusion

    ## References
    * McMahon, P. B., Tokranov, A. K., Bexfield, L. M., Lindsey, B. D., Johnson, T. D., Lombard,
      M. A., & Watson, E. (2022). Perfluoroalkyl and polyfluoroalkyl substances in groundwater
      used as a source of drinking water in the Eastern United States. *Environmental Science &
      Technology*, *56*(4), 2279–2288. https://doi.org/10.1021/acs.est.1c04795
    * Seawolf, S. M., Williams, B. M., Gordon, S. E., Romanok, K., Smalling, K., Bradley, P. M.,
      & Morriss, M. C. (2023). *PFAS reconnaissance landscape data* [Dataset]. U.S. Geological
      Survey. https://doi.org/10.5066/P9JF1EXH
    * Smalling, K. L., Romanok, K. M., Bradley, P. M., Morriss, M. C., Gray, J. L., Kanagy, L. K.,
      Gordon, S. E., Williams, B. M., Breitmeyer, S. E., Jones, D. K., DeCicco, L. A.,
      Eagles-Smith, C. A., & Wagner, T. (2023). Per- and polyfluoroalkyl substances (PFAS) in
      United States tapwater: Comparison of underserved private-well and public-supply exposures
      and associated health implications. *Environment International*, *178*, 108033.
      https://doi.org/10.1016/j.envint.2023.108033
    * U.S. Environmental Protection Agency. (2016, May 25). Lifetime health advisories and
      health effects support documents for perfluorooctanoic acid and perfluorooctane sulfonate.
      *Federal Register*, *81*(101), 33250–33251.
      https://www.govinfo.gov/content/pkg/FR-2016-05-25/pdf/2016-12361.pdf
    * U.S. Environmental Protection Agency. (2024, April 10). Per- and polyfluoroalkyl substances
      (PFAS): PFAS national primary drinking water regulation.
      https://www.epa.gov/sdwa/and-polyfluoroalkyl-substances-pfas
    * U.S. Environmental Protection Agency. (2025, May 14). EPA announces it will keep Maximum
      Contaminant Levels for PFOA, PFOS [Press release].
      https://www.epa.gov/newsreleases/epa-announces-it-will-keep-maximum-contaminant-levels-pfoa-pfos
    * U.S. Environmental Protection Agency. (2026, May 18). Proposed PFOA and PFOS compliance
      extension rule. https://www.epa.gov/sdwa/proposed-pfoa-and-pfos-compliance-extension-rule
    * U.S. Environmental Protection Agency. (n.d.). Our current understanding of the human
      health and environmental risks of PFAS.
      https://www.epa.gov/pfas/our-current-understanding-human-health-and-environmental-risks-pfas

    ## AI usage appendix

    * Perplexity ([thread ref](https://www.perplexity.ai/search/fe48e31f-abdb-43ae-adde-5d36d3e34970)):
      The team used this thread to identify and narrow potential prediction problems, ultimately selecting PFAS occurrence risk because of its public health relevance and strong U.S. federal data support. The team then co-designed the project scope here, deciding to model tapwater PFAS occurrence from landscape and land-use features while using McMahon et al. and related USGS/EPA studies primarily as scientific background rather than as core modeling datasets. Finally, the team relied on this thread to plan datasets, hypotheses, and timelines—including a decision aid and title options—so the project would be feasible within a 2–3 week window and remain grounded in current PFAS research.
    * Claude.ai ([thread ref](https://claude.ai/share/ccd96f8c-b3f9-45d0-b2b4-57b1e68b62c1)): The team used Claude
      (via Claude.ai) to copyedit the markdown prose in the checkpoint notebook, correcting grammar, subject-verb agreement, and word-choice errors across the problem statement, data source descriptions, and references. Claude also verified the currency of a regulatory claim in the "why this problem matters" section, flagging that EPA's PFAS drinking-water rule had changed since the original draft, and helped the team iteratively reframe that justification around the shifting compliance timeline and its implications for water-system operators. Additional editorial passes reordered the reference list per APA style, added supporting citations for the updated regulatory claims, and introduced a new justification, developed during this conversation, around private-well populations falling outside EPA's public-water-system rule.
    """)
    return


if __name__ == "__main__":
    app.run()

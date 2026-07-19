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
    mcmahon_dict_df = data_dictionary_result.defs["mcmahon_dict_df"]
    mcmahon_alias = data_dictionary_result.defs["mcmahon_alias"]
    return (mcmahon_dict_df,)


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

    ### Smalling et al. (2023) and Sewolf et. al. (2023) load and join-ability (`ss_merged_df`)

    1. Load Seawolf and Smalling via `pandas`
    2. Clean Smalling: the dataset uses `-` and `nd` for two specific purposes (not analyzed, and non-detected
       above minimum detection values, respectively). We decided to replace the former with `NaN` and the latter
       with `0`. Ideally, we should know non-detected minimums, but these were not found.
    3. Merge: using a left join, to report on any unmatched rows
    """)
    return


@app.cell
def _(mo, pd):
    data_dir = mo.notebook_dir() / ".." / "data" / "usgs"

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
    pfas_cols = [
        "PFBA", "PFPeA", "PFHxA", "PFHpA", "PFOA", "PFNA", "PFDA", "PFBS",
        "PFPeS", "PFHxS", "PFHpS", "PFOS", "PFDS", "PFPrS", "6:2 FTS", "FOSA",
        "HFPO-DA; GenX",
    ]

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
    ### McMahon et. al. (2022) load and join-ability (`mac_merged_df`)

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
def _(data_dir, mcmahon_dict_df, np, pd):
    mcmahon_env_df= pd.read_csv(data_dir / "mcmahon" / "PFAS_ENV.csv")

    # Data quirk: All values are labeled with <<compound>>-VA
    # except for `"PFBS-V"`. This is a correction
    mcmahon_env_df = mcmahon_env_df.rename(columns={"PFBS-V": "PFBS-VA"})

    is_pfas_env = mcmahon_dict_df["TABLE"] == "PFAS_ENV"
    is_compound = mcmahon_dict_df["DEFINITION"].str.contains(r"nanograms per liter", regex=True, na=False)

    pfas_codes = mcmahon_dict_df.loc[is_pfas_env & is_compound, "PARAMETER"].str.strip().tolist()

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

    mac_merged_df = mcmahon_env_clean.merge(
        right=mcmahon_geo_df,
        left_on=mcmahon_env_clean["NAWQA_ID"].str.strip(),
        right_on=mcmahon_geo_df["NAWQA_ID"].str.strip(),
        how="left",
        suffixes=("_mac_env", "_mac_geo"),
        indicator=True,
    )
    return (mac_merged_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `ss_merged_df` and `mac_merged_df` now contains all data to be considered in our model design

    ### Unmatched rows and `NaN` clean up
    """)
    return


@app.cell
def _(mac_merged_df, mo, ss_merged_df):
    ss_unmatched_df = ss_merged_df[ss_merged_df["_merge"] == "left_only"]
    ss_unmatched_count = ss_unmatched_df.shape[0]

    mac_unmatched_df = mac_merged_df[mac_merged_df["_merge"] == "left_only"]
    mac_unmatched_count = mac_unmatched_df.shape[0]

    mo.md(f"""
    After joining the features and the PFAS concentration sets we get minimal data loss. 
    The only concentration measurement without landscape attributes is `{ss_unmatched_df.iloc[0, 0]}`.
    It will be dropped.
    """)
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
def _(mac_merged_df, mo, ss_merged_clean_df):
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
        "McMahon": get_nan_counts(mac_merged_df)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### results

    McMahon data does not require any further cleanups. However, we would want to impute for landscape indicators based on max values under the included metadata file.
    """)
    return


@app.cell
def _(mac_merged_df):
    mac_clean = mac_merged_df

    # TODO: Impute ss_merged_df based on ../data/usgs/NationalPFASReconLandscapeMetadata.xml values
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Preliminary data explorations

    ```
    TBD. Check Teams note. Thanks @emirbeg2017 for putting that together!
    ```
    """)
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

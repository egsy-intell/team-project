import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Predicting PFAS occurrence risk based on land use and hydrogeologic features

    ## Team .egsy intelligence (Group #14)
    * Yaisiel (Yai) Torres
    * Gulshan Raj Shetty (Raj)
    * Emir Beg
    * Somyaranjan Sahu

    ## Step one: problem definition

    ### Problem statement
    Per- and polyfluoroalkyl substances, commonly known as PFAS, are persistent environmental contaminants that may enter drinking-water sources through industrial activities, waste disposal, firefighting foam use, urban development, and other landscape-level sources. This project aims to develop a predictive model for the occurrence of Per- and polyfluoroalkyl substances (PFAS) in tap water, using USGS summary data on potential landscape sources (Seawolf et al., 2023), and reported concentration at the point-of-use (Smalling et al., 2023).

    The question we aim to answer is: Can we predict low, medium, and high levels of PFAS concentration in tap water sources across the U.S.A. sources based on key geographic and land-use indicators?

    #### Proposed classification
    A provisional classification approach is:
    * Low: No PFAS compounds detected above the applicable laboratory reporting limits.
    * Medium: At least one PFAS detected, with cumulative concentration at or below the median concentration among detected samples.
    * High: At least one PFAS detected, with cumulative concentration above the median concentration among detected samples.

    The cutoff between medium and high will be established using the model-development data and frozen before final evaluation.

    #### Why this problem matters
    1. **Public health relevance:** PFAS contamination in drinking water is a concern in many countries due to known
       or potential adverse effects on human health (US Environmental Protection Agency [EPA], 2021).
    2. **Regulatory gap:** The United States has no nationally enforceable drinking-water standard for PFAS. The EPA
       has only established a health advisory level of 70 ng/L for perfluorooctane sulfonate (PFOS) and
       perfluorooctanoate (PFOA), two of the most common PFAS found in drinking water (EPA, 2016). A predictive model
       could help fill this gap by flagging risk before formal standards exist.
    3. **Data-driven decision making:** Predicting PFAS levels from traceable, highly correlated geographic and
       land-use features would let water system operators prioritize remediation efforts efficiently.

    #### Intended Application
    The proposed model is intended to function as a screening and sampling-prioritization tool. It will not replace laboratory testing and will not be used to declare a drinking-water source safe, unsafe, compliant, or noncompliant.

    Potential users could include:
    * Environmental and public-health agencies
    * Water-resource managers
    * Researchers planning PFAS sampling programs
    * Community organizations identifying locations where testing resources may be most useful

    ### Application feasibility of the model
    The project is feasible because researchers at the EPA and USGS (U.S. Geological Survey) provides resources and data such as measured PFAS concentration data and landscape summaries for sites included in its national PFAS tap water reconnaissance.

    #### Scope
    * Publicly supplied and privately sourced drinking water
    * PFAS concentration results from the national reconnaissance dataset
    * Landscape and potential-source indicators calculated by USGS
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
    #### USGS Data Source 1: Per- and polyfluoroalkyl substances (PFAS) in United States tapwater: Comparison of underserved private-well and public-supply exposures and associated health implications (Smalling et al., 2023)
    It supplies the project’s dependent variable or target variable i.e Provides the outcome the model is trying to predict. It will be used to train our model in the categorization of tap water sites based on site controls. It includes:

    * Which PFAS compounds were detected
    * The measured concentration of each compound
    * The number of PFAS compounds detected
    * The total or cumulative PFAS concentration
    * Whether results were below the laboratory reporting limit

    #### USGS Data Source 2: PFAS Reconnaissance Landscape Data (Seawolf et al., 2023)
    This dataset provides most of the project’s independent variables, or predictors. It describes the environmental and geographic characteristics surrounding each sampling location that may be associated with PFAS contamination, including:

    * Nearby potential PFAS-related facilities
    * Industrial or commercial activity
    * Urban and developed land
    * Agricultural or natural land
    * Burned areas
    * Land-cover characteristics
    * Public versus private water source
    * Other geographic or landscape summaries around the sampling location

    #### USGS Data Source 3: Perfluoroalkyl and Polyfluoroalkyl Substances in Groundwater Used as a Source of Drinking Water in the Eastern United States (McMahon et al., 2022)
    Alternate data set reporting on PFAS concentrations at groundwater level. The team will use the data at the validation phase to see if the training is also applicable to groundwater sources and their associated landscapes. We will also compare our predictor findings against the McMahon et al. study (2022), and integrate into our model analysis.

    ### Data availability and ethical considerations
    The the three resources from USGS datasets are publicly available government data releases. All of them are marked as CC0, and can be reused without licensing fees. In addition, the datasets do not require access to restricted health, financial, educational, or personally identifiable information.

    The data can be downloaded, filtered, and analyzed using standard tools, and have also been copied to the project's repo for convenience ([direct link](https://github.com/egsy-intell/team-project)).

    #### Privacy
    USGS anonymized the sampling locations to protect participant privacy. The project will retain the anonymized identifiers and will not attempt to infer exact home addresses or private-well
    locations.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Step 2: Data exploration and quality assesssment
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Next Steps: Proposed task assignments

    ## Conclusion

    ## References
    * U.S. Environmental Protection Agency. (2016, May 25). Lifetime health advisories and health effects support
      documents for perfluorooctanoic acid and perfluorooctane sulfonate (No. 101; Vol. 81, pp. 33250–33251). https://www.govinfo.gov/content/pkg/FR-2016-05-25/pdf/2016-12361.pdf
    * McMahon, P. B., Tokranov, A. K., Bexfield, L. M., Lindsey, B. D., Johnson, T. D., Lombard, M. A., & Watson, E.
      (2022). Perfluoroalkyl and Polyfluoroalkyl Substances in Groundwater Used as a Source of Drinking Water in the Eastern United States. Environmental Science & Technology, 56(4), 2279–2288. https://doi.org/10.1021/acs.est.1c04795
    * Seawolf, S. M., Williams, B. M., Gordon, S. E., Romanok, K., Smalling, K., Bradley, P. M., & Morriss, M. C.
      (2023). PFAS Reconnaissance Landscape Data [Dataset]. U.S. Geological Survey. https://doi.org/10.5066/P9JF1EXH
    * Smalling, K. L., Romanok, K. M., Bradley, P. M., Morriss, M. C., Gray, J. L., Kanagy, L. K., Gordon, S. E.,
      Williams, B. M., Breitmeyer, S. E., Jones, D. K., DeCicco, L. A., Eagles-Smith, C. A., & Wagner, T. (2023). Per- and polyfluoroalkyl substances (PFAS) in United States tapwater: Comparison of underserved private-well and public-supply exposures and associated health implications. Environment International, 178, 108033. https://doi.org/10.1016/j.envint.2023.108033
    * U.S. Environmental Protection Agency. (n.d.). Our current understanding of the human health and environmental
      risks of PFAS. https://www.epa.gov/pfas/our-current-understanding-human-health-and-environmental-risks-pfas


    ## AI usage appendix

    * Perplexity ([thread ref](https://www.perplexity.ai/search/fe48e31f-abdb-43ae-adde-5d36d3e34970)): For brainstorming, scope, references, and data sourcing.
    """)
    return


if __name__ == "__main__":
    app.run()

import marimo

__generated_with = "0.23.14"
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
    Per- and polyfluoroalkyl substances, commonly known as PFAS, are persistent environmental contaminants that may enter drinking-water sources through industrial activities, waste disposal, firefighting foam use, urban development, and other landscape-level sources.
    This project aims to develop a predictive model for the occurrence of Per- and polyfluoroalkyl substances (PFAS) in
    drinking water, using USGS summary data on potential landscape sources (Seawolf et al., 2023). The question we aim
    to answer is: Can we predict low, medium, and high levels of PFAS concentration in U.S. drinking water sources based
    on key geographic and land-use indicators?

    A provisional classification approach is:

    Low: No PFAS compounds detected above the applicable laboratory reporting limits.
    Medium: At least one PFAS detected, with cumulative concentration at or below the median concentration among detected samples.
    High: At least one PFAS detected, with cumulative concentration above the median concentration among detected samples.

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

    Intended Application

    The proposed model is intended to function as a screening and sampling-prioritization tool. It will not replace laboratory testing and will not be used to declare a drinking-water source safe, unsafe, compliant, or noncompliant.

    Potential users could include:
    Environmental and public-health agencies
    Water-resource managers
    Researchers planning PFAS sampling programs
    Community organizations identifying locations where testing resources may be most useful

    ### Application feasibility of the model
    The project is feasible because EPA(US Environmental Protection Agency) and USGS(US Geological Survey) provides resources and data such as masured PFAS concentration data and landscape summaries for sites included in its national PFAS tap-water reconnaissance.The 2021–2022 USGS concentration release contains results for 34 PFAS compounds from 409 residential and commercial tap-water samples.

    ### Scope
    Publicly supplied and privately sourced drinking water
    PFAS concentration results from the national reconnaissance dataset
    Landscape and potential-source indicators calculated by USGS
    One observation per unique sampling location
    Classification of cumulative PFAS concentration into three categories

    ### Constraints
    The project will not:
    Make causal claims about individual PFAS sources
    Determine regulatory compliance
    replace laboratory sampling
    Estimate the exact PFAS exposure of individual residents
    Publish or attempt to reconstruct exact residential locations
    Use repeated temporal samples as independent observations
    Use quality-assurance samples as model observations
    Use previously generated PFAS predictions as predictor variables


    ## Step two: Data source identification
    USGS?
    EPA?

    ### Data source
    Data Source 1: USGS Tap-Water PFAS Concentration Data
    Data Source 2: USGS PFAS Reconnaissance Landscape Data
    Data Source 3: EPA UCMR 5 PFAS Results

    ### Data availability and ethical considerations
    The two primary USGS datasets are publicly available government data releases. The landscape release is marked CC0, and the concentration data are publicly accessible without licensing fees. The datasets do not require access to restricted health, financial, educational, or personally identifiable information.
    The data can be downloaded and analyzed using standard Python libraries such as:
    pandas
    NumPy
    matplotlib
    scikit-learn

    No unusual computing resources are expected to be required.

    Privacy
    USGS anonymized the sampling locations to protect participant privacy. The project will retain the anonymized identifiers and will not attempt to infer exact home addresses or private-well locations.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### Data exploration and quality assesssment
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Data suitability and project feasibility

    ## Proposed task assignments

    ## Conclusion

    ## References
    * US Environmental Protection Agency [EPA]. (2016, May 25). Lifetime health advisories and health effects support
       documents for perfluorooctanoic acid and perfluorooctane sulfonate (No. 101; Vol. 81, pp. 33250–33251).
       https://www.govinfo.gov/content/pkg/FR-2016-05-25/pdf/2016-12361.pdf
    * Seawolf, S. M., Williams, B. M., Gordon, S. E., Romanok, K., Smalling, K., Bradley, P. M., & Morriss, M. C.
      (2023). PFAS Reconnaissance Landscape Data [Dataset]. U.S. Geological Survey. https://doi.org/10.5066/P9JF1EXH
    * US Environmental Protection Agency. (n.d.). Our current understanding of the human health and
      environmental risks of PFAS. https://www.epa.gov/pfas/our-current-understanding-human-health-and-environmental-risks-pfas

    ## AI usage appendix

    * Perplexity ([thread ref](https://www.perplexity.ai/search/fe48e31f-abdb-43ae-adde-5d36d3e34970)): For brainstorming, scope, references, and data sourcing.
    """)
    return


if __name__ == "__main__":
    app.run()

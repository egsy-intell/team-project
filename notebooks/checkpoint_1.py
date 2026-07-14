import marimo

__generated_with = "0.23.9"
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
    * Gulshan Raj Shetty
    * Emir Beg
    * Somyaranjan Sahu

    ## Step one: problem definition

    ### Problem statement
    This project aims to develop a predictive model for the occurrence of Per- and polyfluoroalkyl substances (PFAS) in
    drinking water, using USGS summary data on potential landscape sources (Seawolf et al., 2023). The question we aim
    to answer is: can we predict low, medium, and high levels of PFAS concentration in U.S. drinking water sources based
    on key geographic and land-use indicators?

    #### Why this problem matters
    1. **Public health relevance:** PFAS contamination in drinking water is a concern in many countries due to known
       or potential adverse effects on human health (US Environmental Protection Agency [EPA], 2021).
    2. **Regulatory gap:** The United States has no nationally enforceable drinking-water standard for PFAS. The EPA
       has only established a health advisory level of 70 ng/L for perfluorooctane sulfonate (PFOS) and
       perfluorooctanoate (PFOA), two of the most common PFAS found in drinking water (EPA, 2016). A predictive model
       could help fill this gap by flagging risk before formal standards exist.
    3. **Data-driven decision making:** Predicting PFAS levels from traceable, highly correlated geographic and
       land-use features would let water system operators prioritize remediation efforts efficiently.

    ### Application feasability of the model

    ### Scope and Constraints

    ## Step two: Data source identification

    ### Data source

    ### Data availability and ethical considerations
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
    ### Data suitability and project feasability

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

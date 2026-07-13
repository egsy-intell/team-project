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
    * Gulshan Raj Shetty
    * Emir Beg
    * Somyaranjan Sahu

    ## Step one: problem definition

    ### Problem statement

    #### Why this problem matters?

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

    ## AI usage appendix

    * Perplexity ([thread ref](https://www.perplexity.ai/search/fe48e31f-abdb-43ae-adde-5d36d3e34970)): For brainstorming, scope, references, and data sourcing.
    """)
    return


if __name__ == "__main__":
    app.run()

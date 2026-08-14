# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.14",
# ]
# ///

import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Conclusion

    ### How we got here

    Every pivot in this project traced back to the same discovery:
    intuition about PFAS data did not survive contact with the data
    itself. Step 1-2 exploration showed that our original plan, a
    single cumulative-concentration variable split at its own sample
    median, could not work: non-detected and not-analyzed values are
    recorded identically low but mean different things, several
    variables are right-skewed rather than symmetric, and an
    equal-weight-per-compound median cutoff never reflected how
    differently PFAS compounds are actually regulated. That evidence
    moved us onto the toxicity quotient (∑TQ) target instead, anchored
    to the same trigger/MCL vocabulary water-resource operators already
    track — closer to our underlying goal of anticipating compliance
    with EPA's PFAS drinking-water rule than a sample-relative cutoff
    ever could. The pivot had a real cost: of the 17 PFAS compounds
    Smalling et al. (2023) report, EPA has set Maximum Contaminant
    Levels for only six, so 11 compounds stayed in the dataset as a
    descriptive slice rather than feeding the classified target, and
    McMahon's groundwater ∑TQ turned out not to be on the same footing
    as Smalling's, so we treated the two studies' scores as reported on
    different scales rather than reconciling them.

    Step 3-4 built directly on that output: risk-tier cutoffs against
    `ss_scored_df`'s ∑TQ, a study-grouped split and per-class evaluation
    metrics, McMahon's groundwater data held out of training entirely
    rather than combined with the tapwater set, and two competing
    classifiers proposed — an interpretable logistic-regression
    baseline (Model A) and a non-linear random-forest ensemble
    (Model B). Step 5 trained and evaluated both against that plan.

    ### What Step 5 found

    Neither model cleared the bar Step 3 set. Model A's held-out
    `mcl_exceedance` recall was 0.0000 (0 of 14 high-risk sites caught)
    and Model B's was 0.0714 (1 of 14), both far short of the 0.70
    recall floor — and this was not a held-out-set surprise, since both
    models' cross-validated recall during tuning already topped out
    well below that floor. Model B's one extra correct site is not a
    meaningful edge over Model A, and Model B's apparently "perfect"
    precision reflects a single correct prediction out of 46 held-out
    sites, not a reliable pattern. Both models defaulted to predicting
    the majority risk tier; against a same-partition majority baseline,
    Model A was statistically indistinguishable from just guessing.

    Chasing that gap with more tuning would have been the wrong
    response. Training used only 190 sites across seven study groups,
    and even our full 236-site combined training and held-out pool is
    spread across just 36 states and territories, 9 of them represented
    by a single site, while the three best-covered states alone
    (Illinois, Minnesota, California) account for 35.6% of every site
    we have. Held-out errors tracked each study's own risk-tier
    composition rather than geography, but coverage this thin cannot
    separate the two with any confidence. That is a data-collection
    ceiling, not a modeling one: no amount of hyperparameter search or
    model swapping fixes a model that has only ever seen a few hundred
    sites clustered in a handful of states. We were deliberately
    cautious about data leakage and selection bias throughout — the
    study-grouped split, the held-out evaluation, keeping McMahon's
    groundwater data out of training entirely rather than blending it
    in — and that caution was necessary but not sufficient. Careful
    modeling cannot substitute for volume and geographic breadth the
    underlying data simply does not have yet.

    ### Recommendation

    We recommend treating our models as exploratory research prototypes
    rather than screening-ready tools, and we do not recommend deploying
    either one operationally in its current form. Given the risks PFAS
    exposure poses to drinking water, the priority for anyone continuing
    this work — us, or another team, public or private — should be
    closing the data-sparsity gap before further modeling: scaling up
    site sampling in underrepresented states and regions, and
    incorporating additional scientifically supported predictors, such
    as McMahon et al. (2022)'s DOC and VOC measurements, where a
    comparable source can be identified. Check-In #2 peer review
    separately suggested a single-state or regional analysis would
    control for landform and geography more precisely; McMahon et al.
    (2022) took exactly that narrower approach and reached far higher
    sensitivity and specificity than either of our national models, a
    comparison that is not a controlled test of regional scope but is
    consistent with that feedback. Either path, national or regional,
    still needs the same thing before a model is worth deploying:
    government and private entities investing in denser, more
    representative PFAS site data. Only after that gap closes, and a
    model consistently meets the high-risk recall threshold under
    evaluation on entirely unseen regions, should deployment be
    reconsidered.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## References
    * CDM Smith. (2024). EPA's final regulations: What do you
      need to know? https://oldcolonyplanning.org/wp-content/uploads/2024/04/EPAs-Final-PFAS-Regulations-Fact-Sheet.pdf
    * McMahon, P. B., Tokranov, A. K., Bexfield, L. M., Lindsey, B. D.,
      Johnson, T. D., Lombard, M. A., & Watson, E. (2022). Perfluoroalkyl and
      polyfluoroalkyl substances in groundwater used as a source of drinking
      water in the Eastern United States. *Environmental Science & Technology*,
      *56*(4), 2279–2288. https://doi.org/10.1021/acs.est.1c04795
    * Scikit-learn developers. (2026a). 1.1.11. Logistic regression.
      https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression
    * Scikit-learn developers. (2026b). 1.10. Decision trees.
      https://scikit-learn.org/stable/modules/tree.html
    * Seawolf, S. M., Williams, B. M., Gordon, S. E., Romanok, K., Smalling,
      K., Bradley, P. M., & Morriss, M. C. (2023). *PFAS reconnaissance
      landscape data* [Dataset]. U.S. Geological Survey.
      https://doi.org/10.5066/P9JF1EXH
    * Smalling, K. L., Romanok, K. M., Bradley, P. M., Morriss, M. C., Gray, J.
      L., Kanagy, L. K., Gordon, S. E., Williams, B. M., Breitmeyer, S. E.,
      Jones, D. K., DeCicco, L. A., Eagles-Smith, C. A., & Wagner, T. (2023).
      Per- and polyfluoroalkyl substances (PFAS) in United States tapwater:
      Comparison of underserved private-well and public-supply exposures and
      associated health implications. *Environment International*, *178*,
      108033. https://doi.org/10.1016/j.envint.2023.108033
    * U.S. Environmental Protection Agency. (2016, May 25). Lifetime health
      advisories and health effects support documents for perfluorooctanoic
      acid and perfluorooctane sulfonate. *Federal Register*, *81*(101),
      33250–33251.
      https://www.govinfo.gov/content/pkg/FR-2016-05-25/pdf/2016-12361.pdf
    * U.S. Environmental Protection Agency. (2024, April 10). Per- and
      polyfluoroalkyl substances (PFAS): PFAS national primary drinking water
      regulation. https://www.epa.gov/sdwa/and-polyfluoroalkyl-substances-pfas
    * U.S. Environmental Protection Agency. (2025, May 14). EPA announces it
      will keep Maximum Contaminant Levels for PFOA, PFOS [Press release].
      https://www.epa.gov/newsreleases/epa-announces-it-will-keep-maximum-contaminant-levels-pfoa-pfos
    * U.S. Environmental Protection Agency. (2026, May 18). Proposed PFOA and
      PFOS compliance extension rule.
      https://www.epa.gov/sdwa/proposed-pfoa-and-pfos-compliance-extension-rule
    * U.S. Environmental Protection Agency. (n.d.). Our current understanding
      of the human health and environmental risks of PFAS.
      https://www.epa.gov/pfas/our-current-understanding-human-health-and-environmental-risks-pfas

    ### Public codebase

    Per the spec, the report and presentation must both link the
    public codebase. This project's codebase is public at
    <https://github.com/egsy-intell/team-project>, the same repository
    this report itself is published from.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## AI usage appendix

    * Perplexity ([thread ref](https://www.perplexity.ai/search/fe48e31f-abdb-43ae-adde-5d36d3e34970)):
      The team used this thread to identify and narrow potential prediction
      problems, ultimately selecting PFAS occurrence risk because of its public
      health relevance and strong U.S. federal data support. The team then
      co-designed the project scope here, deciding to model tapwater PFAS
      occurrence from landscape and land-use features while using McMahon et
      al. and related USGS/EPA studies primarily as scientific background
      rather than as core modeling datasets. Finally, the team relied on this
      thread to plan datasets, hypotheses, and timelines—including a decision
      aid and title options—so the project would be feasible within a 2–3 week
      window and remain grounded in current PFAS research.
    * Claude.ai ([thread ref](https://claude.ai/share/ccd96f8c-b3f9-45d0-b2b4-57b1e68b62c1)):
      The team used Claude (via Claude.ai) to copyedit the project's markdown
      prose — correcting grammar, subject-verb agreement, and word-choice
      errors across the problem statement, data source descriptions, and
      references. Claude also verified the currency of a
      regulatory claim in the "why this problem matters" section, flagging that
      EPA's PFAS drinking-water rule had changed since the original draft, and
      helped the team iteratively reframe that justification around the
      shifting compliance timeline and its implications for water-system
      operators. Additional editorial passes reordered the reference list per
      APA style, added supporting citations for the updated regulatory claims,
      and introduced a new justification, developed during this conversation,
      around private-well populations falling outside EPA's public-water-system
      rule.
    * For coding assistance disclosure please refer to the project's README.md
      ([direct link](https://github.com/egsy-intell/team-project#ai-use-disclosure))
    """)
    return


if __name__ == "__main__":
    app.run()

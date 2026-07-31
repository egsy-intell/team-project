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

    This project's biggest lesson from Checkpoint 1 was that intuition
    can mislead once real data is in front of you. We set out to
    clarify a single variable, cumulative PFAS concentration, expecting
    a straightforward low/medium/high split. Instead, the data's own
    properties argued against that plan: non-detected values and
    not-analyzed values are recorded identically low but mean different
    things (see Step 2's Smalling load and clean-up above), and several
    of the variables we care about are right-skewed rather than
    symmetric (see Skewness and IQR outlier summary above). Weighting
    every compound equally per ng/L, and cutting at our own sample's
    median, never reflected how differently PFAS compounds are actually
    regulated. That combination of findings is what moved us off the
    original classification and onto the toxicity quotient (∑TQ) target
    instead.

    The same distribution review also pointed to candidate predictors
    worth carrying into modeling. Seawolf's `mean_dist_to_pfas_site` and
    `number_pfas_sites_proximal`, i.e., proximity and exposure to
    PFAS-associated sites such as fire stations and military
    facilities, stood out in the box-plot and skewness review as
    geographically meaningful and were retained through cleaning for
    that reason.

    Even though the pivot moved us away from our original plan, it left
    us better aligned with our underlying goal. We set out to build a
    tool that could help water-resource operators anticipate compliance
    with EPA's PFAS drinking-water rule ahead of its phased deadlines.
    Anchoring the target on ∑TQ, and on the same trigger/MCL vocabulary
    operators already track, gets us closer to that goal than a
    sample-relative median cutoff ever could.

    That pivot has a cost: some of the compounds in the original
    dataset are not part of the core ∑TQ analysis. Of the 17 PFAS
    compounds Smalling et al. (2023) report, EPA has set Maximum
    Contaminant Levels (MCLs) for only six: PFOA, PFOS, PFHxS, PFNA,
    PFBS, and HFPO-DA (GenX). The remaining 11 compounds have, at best,
    a state-level benchmark rather than an EPA one, and two (PFPeS,
    PFPrS) have no benchmark identified in either source. Those
    compounds stay in the dataset as a descriptive slice rather than
    feeding the classified ∑TQ target.

    That additional processing, worked out in the ∑TQ construction
    section above, produced `ss_scored_df`, carrying the classified
    `sum_tq_epa` alongside `ss_clean_df`'s predictors, and `mc_scored_df`,
    McMahon's groundwater data scored the same way — though its
    `sum_tq_epa` is not on the same footing as Smalling's, since a
    missing GenX benchmark and a different non-detect convention push
    every McMahon site above the trigger cutoff. Both stem from what
    each source publishes rather than a cleaning choice we can revisit,
    so we treat the two studies' ∑TQ as reported on different scales
    rather than reconciling them into one modeling target.

    Checkpoint 2 built directly on that output: it set the risk-tier
    cutoffs against `ss_scored_df`'s ∑TQ (Step 3), designed a
    study-grouped split and per-class evaluation metrics, decided to
    hold McMahon's groundwater data out of training rather than combine
    it with the tapwater set, and proposed two competing classifiers,
    an interpretable baseline and a non-linear ensemble (Step 4).
    Training both models and evaluating them against that plan is
    Step 5 work for the final checkpoint.
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
    * Scikit-learn developers. (2026). 1.10. Decision trees.
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
      The team used Claude (via Claude.ai) to copyedit the markdown prose in
      the checkpoint notebook, correcting grammar, subject-verb agreement, and
      word-choice errors across the problem statement, data source
      descriptions, and references. Claude also verified the currency of a
      regulatory claim in the "why this problem matters" section, flagging that
      EPA's PFAS drinking-water rule had changed since the original draft, and
      helped the team iteratively reframe that justification around the
      shifting compliance timeline and its implications for water-system
      operators. Additional editorial passes reordered the reference list per
      APA style, added supporting citations for the updated regulatory claims,
      and introduced a new justification, developed during this conversation,
      around private-well populations falling outside EPA's public-water-system
      rule.
    """)
    return


if __name__ == "__main__":
    app.run()

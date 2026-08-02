---
title: Predicting PFAS Occurrence Risk from Land-Use Features
author: Team .egsy intelligence (Group 14)
date: Check-In #2 — August 1, 2026
---

# Findings So Far

::: notes
[Speaker: Yai] Hi everyone — we're Team .egsy intelligence, Group 14. Over the next fifteen minutes we'll walk through why this problem matters, what we've found in the data, and where our evaluation plan and modeling proposals stand for this Check-In. Quick introductions first.
:::

## Team & Roles

| Name | Role | Focus |
|---|---|---|
| Yaisiel (Yai) Torres | Proposal / Presentation & Docs Lead | Data curation, proofreading, PM, Step 5 validation |
| Emir Beg | Modeling & Presentation Lead B | Ensemble model, scalability |
| Gulshan Raj Shetty (Raj) | Modeling & Presentation Lead A | Split strategy, baseline, McMahon eval |
| Somyaranjan Sahu | Model Quality & PM Support Lead | Test, evaluate, retune, PM support |

::: notes
[Speaker: Yai] I'm Yai — I lead the proposal, docs, and data-curation side, and I'm co-leading this presentation with Raj and Emir. Raj leads modeling on our interpretable baseline, plus the split strategy and the groundwater evaluation. Emir leads modeling on the ensemble model and our scalability check. And Somyaranjan owns model quality, evaluation, and project-management support for the team. I'm also teaming up with Somyaranjan on Step 5 model validation and benchmarking once both models are trained. Every piece of this pipeline has an owner. Let's start with the problem itself — why PFAS, and why now.
:::

## What Are PFAS?

- **PFAS** — a family of roughly 15,000 synthetic "forever chemicals"
- In nonstick cookware, firefighting foam, water-resistant fabric since the 1940s
- Linked to cancer, thyroid disease, and immune-system harm

::: notes
[Speaker: Yai] Let's ground this for anyone hearing the term for the first time. PFAS stands for per- and polyfluoroalkyl substances — a family of something like fifteen thousand synthetic chemicals, nicknamed "forever chemicals" because the carbon-fluorine bond that makes them nonstick, waterproof, and fire-resistant is the same bond that makes them essentially indestructible, in the environment and in our bodies. They've been in everyday products since the 1940s. And they're not just persistent, they're harmful: PFAS exposure is linked to certain cancers, thyroid disease, and immune-system effects. That's why anyone should care. Here's why it isn't already solved.
:::

## The Regulatory Gap

- EPA's legal limit (MCL) — finalized 2024, already narrowed once, more changes proposed
- Covers *public* water systems only
- Private wells: tens of millions of people, **zero federal requirement to test**

::: notes
[Speaker: Yai] In April 2024, EPA finalized a Maximum Contaminant Level — an MCL, the enforceable legal limit — for six PFAS compounds. Sounds solved. It isn't, for two reasons. First, it's a moving target: the rule was already narrowed once, in 2025, down to just two compounds, with a further extension currently proposed. Second, and this is the gap our project lives in: that rule only covers public water systems. Tens of millions of people get their water from private wells, and nobody is required to test those at all. Our data spans both public supply and private wells, so we can speak to exactly the population the regulation leaves out.
:::

## Project Scope

- A **screening tool** — not a lab test, not a compliance ruling
- For agencies, water managers, researchers, communities
- Tap water + groundwater, one risk classification per site

::: notes
[Speaker: Yai] So what are we actually building? A prioritization tool — it tells you where to look closer, not a legal determination that a specific well is safe or unsafe. It's built for the people who'd act on that signal: public-health agencies, water-resource managers, researchers planning sampling campaigns, community groups. And we're scoping it to one risk classification per sampling site, covering both tap water and groundwater sources. Raj, over to you for where that data actually comes from.
:::

## Data Sources

| Study | Role |
|---|---|
| Smalling et al., 2023 | Tap-water PFAS outcomes |
| Seawolf et al., 2023 | Land-use predictors |
| McMahon et al., 2022 | Groundwater — both predictors & outcomes |

::: notes
[Speaker: Raj] Thanks, Yai. We are combining three public USGS datasets.
Smalling provides the measured PFAS concentrations in tap water, which we use to create our target. Seawolf provides the corresponding land-use predictors, such as nearby industrial activity and potential PFAS sources. We join these two datasets at the sampling-site level to create our primary modeling dataset.
McMahon contains both PFAS measurements and landscape predictors for groundwater wells. Because its measurements were processed differently, we are keeping it separate and using it later as an independent validation dataset.
All three datasets are publicly available, CC0-licensed (Creative Commons Zero), anonymized, and contain no personally identifiable information. so there are no privacy concerns on the data side.
:::

## Data Quality: It Held Up

- **236** usable tap-water sites (Smalling/Seawolf)
- **254** usable groundwater sites (McMahon)
- Only 1 record dropped across the whole join

::: notes
[Speaker: Raj] The data integration held up well. We lost only one record when joining Smalling and Seawolf, leaving 236 usable tap-water sites.
Some missing Seawolf values were structural, meaning no nearby facility was identified rather than the data being unavailable. We handled those values deliberately instead of dropping the sites.
We also retained 254 usable groundwater sites from McMahon, giving us a strong foundation for modeling and validation.
Emir will now explain how we defined the PFAS risk target.
:::

## The Pivot: From Median Split to ∑TQ

- Old plan: split sites by our own sample's median — **dropped**
- Why: treats every compound as equally dangerous, and it's relative to *us*, not a health standard
- New target: **∑TQ**, anchored on EPA's own compliance language

::: notes
[Speaker: Emir] Thanks, Raj. This is the most important methodology decision we made. Our original plan classified sites as low, medium, or high using the median of our own sample, but that treats every PFAS compound as equally dangerous, which they're not, and it's relative to us, not to any external health standard. So we scrapped it for something anchored on an actual regulatory yardstick: ∑TQ. Let me define that quickly before we get to results.
:::

## What Is ∑TQ?

- **TQ** (toxicity quotient) = concentration ÷ EPA health benchmark, per compound
- **∑TQ** = TQ summed across the 6 EPA-regulated PFAS
- **< 0.5** reduced monitoring · **0.5–1.0** trigger · **≥ 1.0** MCL exceedance

::: notes
[Speaker: Emir] Think of it like a tab: for each of the six EPA-regulated compounds — PFOA, PFOS, PFHxS, PFNA, PFBS, and GenX — we divide the measured concentration by that compound's EPA health benchmark, and that ratio is the toxicity quotient, TQ. Add up all six and you get ∑TQ, one running total per site. EPA's own compliance language gives us three tiers from that number: under 0.5 is within reduced monitoring, 0.5 up to 1.0 is above the trigger, and 1.0 or higher is MCL exceedance, meaning the tab has come due. Same tiers you'll see in the results next.
:::

## ∑TQ — Tap Water

**Median ∑TQ: 0.17** (range 0–17.7, n=236)

Most sites well within reduced monitoring — a long right tail is what we're hunting for.

::: notes
[Speaker: Emir] So what does that look like in practice? Across 236 tap-water sites, the median ∑TQ is 0.17, well under our 0.5 trigger threshold. Most sites are fine. But the range runs all the way up to 17.7, and that long tail, the sites way above the norm, is exactly what a prioritization tool should be built to catch.
:::

## ∑TQ — Groundwater, and a Catch

**Every McMahon site (n=254) clears both cutoffs — by construction**

- No GenX in this panel — 5 compounds, not 6
- Non-detects imputed at half the reporting limit, not zero
- **The two studies' ∑TQ scores are not directly comparable**

::: notes
[Speaker: Emir] Here's where we have to be honest about a limitation. Every single McMahon groundwater site scores above our exceedance cutoff, not because groundwater is uniformly worse, but because of how the score is built: McMahon's panel is missing GenX entirely, and its convention for non-detects, half the reporting limit instead of zero, inflates the floor for every "clean" site. So we can't say groundwater is riskier than tap water; we can only say the two scores aren't computed the same way. We've already made a call on what to do about that, and Raj will walk through it next.
:::

# Evaluation Plan & Modeling Proposals

::: notes
[Speaker: Raj] Thanks, Emir.
I’ll now walk through our evaluation strategy and the modeling proposals we designed for this checkpoint. 

:::

## Where We Stand

- Evaluation plan (Step 3) and both modeling proposals (Step 4) — fully designed
- One thing left to produce: real model scores, in Step 5

::: notes
[Speaker: Raj] At this stage, the evaluation plan for Step 3 and both modeling proposals for Step 4 are fully designed.
At this point, the target, features, split strategy, metrics, success thresholds, and both model proposals are finalized. Step 5 will focus on execution: training both models and comparing their predictions on the same held-out test set. Let’s begin with how we created that test set.
:::

## Split Strategy: Group by Study

- Whole **studies** held out together — not individual rows
- Verified: zero overlapping sites or studies across train/test, all three risk tiers preserved

| Method | Held-out studies | Test share (target 20%) | Distribution gap |
|---|---|---|---|
| Our exhaustive search | Cape Cod, Minnesota, Northeast Iowa | 19.5% | 3.5% |
| Best `StratifiedGroupKFold` fold | Minnesota, Puerto Rico | 14.4% | 10.9% |

::: notes
[Speaker: Raj] The main risk we wanted to avoid was data leakage. Sites from the same PFAS study often share similar geography, sampling methods, and environmental conditions. With a random split, very similar sites could appear in both the training and test sets, making the model look more accurate than it would be on truly unseen data.
To prevent that, we held out complete studies rather than individual rows.
We compared scikit-learn’s StratifiedGroupKFold with our own exhaustive search. Both approaches preserved all three risk tiers and produced zero overlap between studies. However, our selected split was closer to the 20 percent test-size target and had a much smaller risk-tier distribution gap: 3.5 percent compared with about 11 percent.
The final split uses 190 sites from seven studies for training and holds out Cape Cod, Minnesota, and Northeast Iowa. This gives us 46 test sites from three completely unseen studies.
McMahon remains outside both the training and test sets because its ∑TQ values are calculated differently. This gives us two complementary evaluation plans. First, both models will be formally evaluated on the grouped tap-water test set using unseen studies. Second, the winning model will be applied to the McMahon groundwater dataset as an independent validation check.

Somyaranjan, over to you to explain the metrics and success thresholds we will use to evaluate the models.
:::

## Metrics & Success Thresholds

| Metric | Threshold | Why |
|---|---|---|
| Recall, high-risk tier | ≥ 70% | A missed contaminated site costs more than a false alarm |
| Macro F1, all tiers | ≥ 0.60 | Proof the model learns all three tiers, not just the majority |
| Precision, high-risk tier | ≥ 45% | A floor against "flag everything," not the primary target |

::: notes
[Speaker: Somyaranjan] Thanks, Raj. Before we trust any model's output, we need to know what "good" looks like, and that's what this plan sets. We picked three thresholds, each benchmarked against a random guess so they're not arbitrary. Recall on the highest-risk tier has to hit at least 70 percent, because a missed contaminated site is a public-health failure, while a false alarm only costs a confirmatory retest, so recall gets the strictest bar. Macro F1 across all three tiers has to clear 0.60, our check that the model is actually learning the difference between tiers, not just calling everything "safe" and coasting on the fact that most sites really are. And precision on the highest-risk tier needs to clear 45 percent, a floor, not a target, just to stop a model from gaming recall by flagging everything. For context, a model that always predicts the majority class scores zero recall on the tier we care about most — that's the bar we're measuring against.
:::

## Two Competing Proposals

| | Proposal A | Proposal B |
|---|---|---|
| Approach | Interpretable baseline | Random forest ensemble |
| Lead | Raj | Emir |
| Optimized for | Legibility, trust | Non-linear land-use interactions |

::: notes
[Speaker: Emir] Rather than committing to one model, we're running two proposals in parallel, evaluated on the same split and the same metrics, so they're a fair comparison. Proposal A is a simple, auditable model an operator could actually trust and inspect. Proposal B trades some of that legibility for the ability to capture non-linear interactions the baseline can't. May the better-performing, still-explainable model win.
:::

## Proposal A — Interpretable Baseline

Multinomial logistic regression on land-use predictors, with L2 regularization and class weighting.

**Status:** design finalized — training happens alongside Proposal B in Step 5

::: notes
[Speaker: Raj] My proposal is a multinomial logistic regression model that predicts the three PFAS risk tiers from the land-use features.
We chose logistic regression because it is interpretable, efficient, and well suited for multiclass classification. Its coefficients allow us to understand how each predictor influences the probability of a risk tier, which is important for a public-health screening tool.
We will implement it using a scikit-learn pipeline with feature standardization, L2 regularization to reduce overfitting, and balanced class weights to account for the smaller medium- and high-risk classes.
The regularization strength will be tuned using grouped cross-validation within the training data, while the final test set remains untouched.
This model is trained from scratch on our tabular data. It does not use a foundation model, and its computational requirements are low enough to run on a standard laptop or Google Colab using CPU resources.
It provides a transparent baseline against which we can evaluate whether Emir’s more complex random forest delivers a meaningful performance improvement.
Emir, over to you for Proposal B.
:::

## Proposal B — Random Forest Ensemble

Random forest classifier with balanced class weighting, capturing non-linear land-use interactions.

**Status:** design finalized — training happens alongside Proposal A in Step 5

::: notes
[Speaker: Emir] My proposal is a random forest: an ensemble of decision trees that can capture the nonlinear interactions Raj's linear baseline would miss — say, a facility's distance mattering differently in an urban area than a rural one. I'm using balanced class weighting so the rare high-risk tier still gets a real say in how the trees are built, and I'm holding it to the exact same rulebook as Raj's baseline: first clear the 70 percent recall floor, then rank by macro-F1. Same rigor, same rules, just a different shape of model — so when we compare them, it's an honest fight.
:::

## Validation & Trade-offs

**Both designs are locked — here's the analysis ahead of us**

- Accuracy vs. interpretability vs. compute cost — head to head, same split, same metrics
- Plus a groundwater check: score McMahon's held-out wells and see if the ranking holds up

::: notes
[Speaker: Somyaranjan] Once both models are trained, Yai and I run them against the same held-out test set and the same metrics you just saw, co-leading that validation and benchmarking together. First we check each model against the Step 3 floors: any candidate that misses the 0.70 recall floor on mcl_exceedance gets set aside rather than let through on a technicality, and if neither model clears it, we'll report that plainly instead of quietly lowering the bar — and still hold onto the higher-recall candidate for diagnostic comparison. Among whatever passes, we rank by macro-F1 and report the real trade-off: not just which model scores higher, but whether that gain is worth losing some interpretability. We'll also take the winning model and score McMahon's groundwater wells — held out earlier for exactly this — as a qualified check: does its relative ranking of those wells look plausible, even though McMahon's ∑TQ isn't on the same footing as tap water's, so it's not a number we can compare directly. That's the analysis ahead of us.
:::

# Wrap-Up

::: notes
[Speaker: Yai] Thanks, Somyaranjan. Let's close with where all of that leads.
:::

## What's Next

**From there: fold in peer-review feedback, then the Final.**

- Fold in peer-review feedback
- Carry it all into the Final submission

::: notes
[Speaker: Yai] What's ahead from there is folding in whatever peer-review feedback we get, and carrying all of it, along with the Step 5 validation Somyaranjan and I are co-leading, into the Final submission. Thanks in advance to whichever teams we end up reviewing — we're looking forward to it.
:::

## References

Sources cited in this presentation:

| Source | Note |
|---|---|
| McMahon et al. (2022) | PFAS in Eastern U.S. groundwater. *Env. Sci. & Technology*. |
| Seawolf et al. (2023) | *PFAS reconnaissance landscape data* [Dataset]. USGS. |
| Smalling et al. (2023) | PFAS in U.S. tapwater. *Environment International*. |
| U.S. EPA (2024) | PFAS national primary drinking water regulation. |
| U.S. EPA (2025) | EPA announces it will keep MCLs for PFOA, PFOS. |
| U.S. EPA (2026) | Proposed PFOA/PFOS compliance extension rule. |

::: notes
[Speaker: Yai] These are the sources behind the data and the regulatory timeline we've cited. Full citations are on screen, and we're happy to send the list along with the deck rather than read through it here.
:::

## Thank You

Questions?

**Team .egsy intelligence** — Emir Beg · Gulshan Raj Shetty · Somyaranjan Sahu · Yaisiel Torres

::: notes
[Speaker: Yai] That's where we stand: solid data, a defensible pivot to ∑TQ, and an evaluation plan with two fully designed modeling proposals ready to run. Thanks for listening — happy to take questions.
:::

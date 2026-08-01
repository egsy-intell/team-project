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
[Speaker: Raj] Thanks, Yai. Our analysis combines three public USGS datasets that serve different purposes in the project.
The Smalling dataset provides the measured PFAS concentrations in tap-water samples, which we use to construct the outcome we want to predict. The Seawolf dataset provides the corresponding land-use and environmental predictors for those sampling locations, including factors such as nearby industrial activity and potential PFAS sources.
We join Smalling and Seawolf at the sampling-site level to create the primary modeling dataset.
The McMahon dataset is slightly different. It contains groundwater wells from across the Eastern United States and includes both PFAS measurements and landscape predictors. Because its PFAS measurements were processed differently, we will not combine it directly with the tap-water training data. Instead, we will use it later as an independent groundwater validation dataset.
All three datasets are publicly available, CC0-licensed, anonymized, and contain no personally identifiable information. so there are no privacy concerns on the data side.

:::

## Data Quality: It Held Up

- **236** usable tap-water sites (Smalling/Seawolf)
- **254** usable groundwater sites (McMahon)
- Only 1 record dropped across the whole join

::: notes
[Speaker: Raj] Before building a target variable or training a model, we first checked whether the datasets could be combined reliably.
The join between the Smalling and Seawolf datasets held up very well. Out of the original records, only one site was lost during the matching process, leaving us with 236 usable tap-water sites.
We also reviewed the missing values carefully. Several Seawolf variables were structurally missing, meaning that no nearby facility or source was identified. These values did not represent data-entry errors, so we handled them deliberately rather than removing the affected sites.
The McMahon dataset contributed another 254 usable groundwater sites. Overall, we retained nearly all available observations and avoided unnecessary row deletion, giving us a clean foundation for both modeling and external validation.

Emir will now explain how we used the PFAS measurements to define the risk target.
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
[Speaker: Raj] Thanks, Emir. The groundwater limitation is important because it affects both how we divide the data and how we evaluate the models.
I’ll now walk through our evaluation strategy and the two modeling proposals we designed for this checkpoint. I’ll begin with where the work currently stands, and then explain how we created a test set that gives us a realistic measure of model generalization.
:::

## Where We Stand

- Evaluation plan (Step 3) and both modeling proposals (Step 4) — fully designed
- One thing left to produce: real model scores, in Step 5

::: notes
[Speaker: Raj] At this stage, the evaluation plan for Step 3 and both modeling proposals for Step 4 are fully designed.
We have finalized the target definition, selected the input features, established the train-and-test split, chosen the evaluation metrics, and defined the success thresholds. We have also specified the preprocessing steps and tuning approach for both candidate models.
The remaining task is execution. During Step 5, we will train both models, generate predictions on the same held-out test set, and compare their actual performance using the evaluation criteria we established.

Let’s first look at how we selected that held-out test set.
:::

## Split Strategy: Group by Study

- Whole **studies** held out together — not individual rows
- Verified: zero overlapping sites or studies across train/test, all three risk tiers preserved

| Method | Held-out studies | Test share (target 20%) | Distribution gap |
|---|---|---|---|
| Our exhaustive search | Cape Cod, Minnesota, Northeast Iowa | 19.5% | 3.5% |
| Best `StratifiedGroupKFold` fold | Minnesota, Puerto Rico | 14.4% | 10.9% |

::: notes
[Speaker: Raj] The first issue we wanted to avoid was data leakage. In PFAS data, sites from the same study often share the same sampling protocol, geographic conditions, and environmental characteristics. If we used a standard random split, very similar sites could end up in both the training and test sets. That could make the model appear more accurate than it would be on truly unseen data.To prevent this, we grouped the data by study and held out complete studies for testing rather than randomly separating individual sites. This gives us a more realistic measure of how the model may perform on new studies and new geographic areas.
We then compared two approaches for selecting the grouped split. The first was scikit-learn’s StratifiedGroupKFold. The second was our own exhaustive search, where we evaluated every valid combination of held-out studies using the same general criteria: no study overlap, preservation of all three risk tiers, a test size close to 20 percent, and a class distribution that closely matches the full dataset.
Both approaches prevented leakage and preserved all three risk tiers. However, our exhaustive search produced the stronger split. It achieved a 19.5 percent test share, which is very close to our 20 percent target, and the risk-tier distribution gap was only 3.5 percent, compared with 11 percent for the best StratifiedGroupKFold result.
Our final split holds out Cape Cod, Minnesota, and Northeast Iowa. That gives us 190 sites from seven studies for training and 46 sites from three studies for testing, with zero shared sites or studies between the two sets.
This decision also clarified how we should use the McMahon groundwater dataset. Since its ∑TQ score is calculated differently and is not directly comparable with the tap-water data, we excluded it from both training and testing. Instead, we will use it as an independent validation check to evaluate whether the model’s relative risk rankings generalize to groundwater sites.

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
[Speaker: Raj] My proposal is a multinomial logistic regression model that predicts the three PFAS risk tiers directly from the land-use and environmental features.
We selected logistic regression as the baseline because it is interpretable, computationally efficient, and appropriate for a multiclass classification problem. Each coefficient helps us understand how a predictor is associated with an increase or decrease in the probability of a particular risk tier. That level of transparency is valuable for a public-health screening tool, where users may need to understand why a location was flagged.
The model will be implemented using a scikit-learn pipeline. Numerical features will be standardized using StandardScaler, followed by multinomial LogisticRegression. We will use L2 regularization to reduce coefficient instability and limit overfitting, particularly because the dataset is relatively small and some predictors may be correlated.
We will also apply balanced class weighting so that the less common medium- and high-risk observations influence the model during training rather than being overwhelmed by the majority class.
The regularization strength will be tuned using grouped cross-validation within the training data. This ensures that the final test set remains completely untouched until the last evaluation.
This model is being trained from scratch on our tabular dataset. It does not use a foundation model or pretrained neural network. Its computational requirements are low, so training and tuning can be completed on a standard laptop or Google Colab using CPU resources.
The model may not capture every complex nonlinear relationship in the data, but it gives us a transparent and defensible benchmark. Emir’s random forest will then show us whether additional model complexity produces a meaningful improvement.

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
[Speaker: Somyaranjan] Once both models are trained, Yai and I run them against the same held-out test set and the same metrics you just saw, co-leading that validation and benchmarking together, and report the real trade-off: not just which model scores higher, but whether that gain is worth losing some interpretability. We'll also take the winning model and score McMahon's groundwater wells — held out earlier for exactly this — as a qualified check: does its relative ranking of those wells look plausible, even though McMahon's ∑TQ isn't on the same footing as tap water's, so it's not a number we can compare directly. That's the analysis ahead of us.
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

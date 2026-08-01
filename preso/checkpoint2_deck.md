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
| Yaisiel (Yai) Torres | Proposal / Presentation & Docs Lead | Data curation, proofreading, PM |
| Emir Beg | Modeling Lead B | Ensemble model, scalability |
| Gulshan Raj Shetty (Raj) | Modeling Lead A | Split strategy, baseline, McMahon eval |
| Somyaranjan Sahu | Model Quality Lead | Test, evaluate, retune |

::: notes
[Speaker: Yai] I'm Yai — I lead the proposal, docs, and data-curation side. Raj leads modeling on our interpretable baseline, plus the split strategy and the groundwater evaluation. Emir leads modeling on the ensemble model and our scalability check. And Somyaranjan owns model quality and evaluation. Every piece of this pipeline has an owner. Let's start with the problem itself — why PFAS, and why now.
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
[Speaker: Raj] Thanks, Yai. We're combining three public USGS datasets. Smalling gives us the outcome we're trying to predict — measured PFAS in tap water. Seawolf gives us the land-use predictors for those same sites, things like nearby industrial activity. McMahon stands on its own: groundwater wells across the Eastern U.S., with both predictors and outcomes in one dataset. All three are public domain, CC0-licensed, and fully anonymized, so there are no privacy concerns on the data side.
:::

## Data Quality: It Held Up

- **236** usable tap-water sites (Smalling/Seawolf)
- **254** usable groundwater sites (McMahon)
- Only 1 record dropped across the whole join

::: notes
[Speaker: Raj] Before trusting a target variable, we had to trust the data underneath it, and it held up well. Joining Smalling to Seawolf, we lost exactly one record. A handful of Seawolf columns were structurally missing, meaning "no facility observed nearby," not a data error, and we imputed those deliberately rather than dropping rows. End result: 236 clean tap-water sites and 254 clean groundwater sites, ready to build a target on top of. Emir's going to pick up the story from here.
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
[Speaker: Raj] Thanks, Emir. Now let's turn to our evaluation plan and the two modeling proposals we're comparing for this Check-In.
:::

## Where Step 3 Stands

- Split strategy, metrics, thresholds, and the groundwater decision — all locked in
- One number left to produce: real model scores, in Step 5

::: notes
[Speaker: Raj] Quick status check before we get into the plan itself: every open question in our evaluation plan is now resolved — how we split the data, what we measure, what counts as success, and how we handle the groundwater gap you just heard about. What's left isn't more planning, it's execution: plugging real model predictions into this plan, which is Step 5's job. Let's start with the split.
:::

## Split Strategy: Group by Study

- Whole **studies** held out together — not individual rows
- Verified: zero overlapping sites or studies across train/test, all three risk tiers preserved

| Method | Held-out studies | Test share (target 20%) | Distribution gap |
|---|---|---|---|
| Our exhaustive search | Cape Cod, Minnesota, Northeast Iowa | 19.5% | 3.5% |
| Best `StratifiedGroupKFold` fold | Minnesota, Puerto Rico | 14.4% | 10.9% |

::: notes
[Speaker: Raj] The risk with PFAS data specifically is that sites from the same study tend to resemble each other — same sampling protocol, similar geography — so a naive random split lets the model "cheat" by seeing near-duplicates on both sides. We hold out entire studies instead, and to make sure we weren't just fooling ourselves, we scored every candidate split against the same rubric scikit-learn's own StratifiedGroupKFold uses. Both approaches preserve all three risk tiers with zero leakage, but our exhaustive search lands closer to the 20 percent test-fraction target and keeps the test set's risk-tier mix much closer to the full dataset's — a 3.5 percent gap versus almost 11 percent for the best sklearn fold. The selected split holds out Cape Cod, Minnesota, and Northeast Iowa: 190 sites across 7 studies for training, 46 sites across 3 studies for test, zero shared sites or studies between them. This is also how we settled McMahon's role: it stays out of both partitions entirely, used as a held-out validation check instead of training data, since its ∑TQ score isn't on the same footing as tap water's. Somyaranjan, over to you for what these models actually need to hit.
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
| Approach | Interpretable baseline | Hierarchical / ensemble |
| Lead | Raj | Emir |
| Optimized for | Legibility, trust | Non-linear land-use interactions |

::: notes
[Speaker: Emir] Rather than committing to one model, we're running two proposals in parallel, evaluated on the same split and the same metrics, so they're a fair comparison. Proposal A is a simple, auditable model an operator could actually trust and inspect. Proposal B trades some of that legibility for the ability to capture non-linear interactions the baseline can't. May the better-performing, still-explainable model win.
:::

## Proposal A — Interpretable Baseline

Multinomial logistic regression on land-use predictors, with L2 regularization and class weighting.

**Status:** design finalized — training happens alongside Proposal B in Step 5

::: notes
[Speaker: Raj] My baseline is a multinomial logistic regression, deliberately kept simple, predicting the risk tier straight from land-use features. L2 regularization keeps the coefficients stable, and we'll weight classes to account for how imbalanced the tiers are. The pipeline, tuning grid, and feature list are all locked in — what's left is purely running it, which happens alongside Emir's ensemble in Step 5.
:::

## Proposal B — Hierarchical / Ensemble

Random forest / gradient boosting, capturing non-linear interactions.

**Status:** design in progress — the last piece before Step 5

::: notes
[Speaker: Emir] My proposal pushes further: a random forest or gradient-boosting ensemble that can capture nonlinear interactions a straight line can't. This is the one piece of our plan still being finalized — I'm locking in the same level of design detail Raj just walked through, so both models can run through the exact same evaluation Somyaranjan described.
:::

## Validation & Trade-offs

**Step 5 starts as soon as Model B's design is locked in**

Accuracy vs. interpretability vs. compute cost — head to head, same split, same metrics.

::: notes
[Speaker: Somyaranjan] Once both models are trained, I run them against the same held-out test set and the same metrics you just saw, and we report the real trade-off: not just which model scores higher, but whether that gain is worth losing some interpretability. That's Step 5, and it starts the moment Emir's design is finalized.
:::

# Wrap-Up

::: notes
[Speaker: Yai] That's the full plan. Let's close with what's left and what's next.
:::

## What's Left

**One modeling task left: finalize Proposal B's design — everything else is ready for Step 5.**

| Deliverable | Owner | Due |
|---|---|---|
| Writeup | Yai | 8/2 |
| This deck | Yai, All | 8/1 |
| 15-min video | All | 8/1–8/2 |
| Peer review | All | 8/2 |

::: notes
[Speaker: Yai] So here's where we stand: the evaluation plan is locked, Proposal A's design is done, and the only open modeling work is finishing Proposal B's design so both can run through Step 5 together. On the submission side: the writeup wraps by August 2nd, this deck is due today, we're recording our fifteen-minute walkthrough right after, splitting sections the same way we just split this presentation, and peer review of another team's checkpoint closes out the week.
:::

## Where We Go Next

- Untested predictors: PFAS-site proximity, facility counts
- Only 6 of 17 reported PFAS compounds have EPA benchmarks — the rest stay descriptive
- Use McMahon's groundwater wells as a held-out validation check, not training data

::: notes
[Speaker: Somyaranjan] Looking past this Check-In: we've flagged predictors we haven't tested yet, like distance to the nearest known PFAS site and nearby facility counts, that could sharpen the model further. We're also only scoring 6 of the 17 PFAS compounds Smalling reports, because those are the only ones with EPA health benchmarks to divide by; the rest stay descriptive, not ignored. And remember McMahon's groundwater data from earlier: since its score isn't built the same way as tap water's, we're not training on it. Once we have a trained model, we'll use McMahon as a sanity check instead, asking whether its relative ranking of those wells looks plausible, even though we can't compare its raw score directly.
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
[Speaker: Yai] That's where we stand: solid data, a defensible pivot to ∑TQ, an evaluation plan that's fully locked in, one modeling proposal ready to run and a second close behind. Thanks for listening — happy to take questions.
:::

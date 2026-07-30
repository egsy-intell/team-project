---
title: Predicting PFAS Occurrence Risk from Land-Use Features
author: Team .egsy intelligence (Group 14)
date: Checkpoint 2 — August 1, 2026
---

# Findings So Far

## Team & Roles

| Name | Role | Focus |
|---|---|---|
| Yaisiel (Yai) Torres | Proposal / Presentation & Docs Lead | Data curation, proofreading, PM |
| Emir Beg | Modeling Lead A | Build, train, evaluate |
| Gulshan Raj Shetty (Raj) | Modeling Lead B | Split strategy, baseline, McMahon eval |
| Somyaranjan Sahu | Model Quality Lead | Test, evaluate, retune |

::: notes
[Speaker: Yai] Hi everyone, we're Team .egsy intelligence — Group 14. Over the next fifteen minutes we'll walk through our data, a key methodology pivot, and where our evaluation plan and modeling proposals stand for Checkpoint 2. Quick introductions first: I'm Yai, I lead the proposal and docs side. Emir leads modeling on the ensemble side, Raj leads modeling on the baseline and split-strategy side, and Somyaranjan owns model quality and evaluation. Let's start with our findings so far.
:::

## Why This Matters

- **PFAS** ("forever chemicals") — synthetic compounds linked to health harms
- EPA's legal limit (MCL) on PFAS — enforceable, but still shifting
- Private wells: outside the federal rule's reach

::: notes
[Speaker: Raj] Quick grounding for anyone new to this: PFAS are a family of synthetic "forever chemicals," so called because they barely break down, and they're linked to real, documented health harms. EPA took a major step in April 2024 by finalizing an MCL — a Maximum Contaminant Level, the legal limit a water system has to stay under — for six of them. But that rule has already been narrowed once, in 2025, to just two compounds, and there's a further extension under proposal right now — so water systems are trying to prioritize against a moving target. And here's the gap that makes our project matter: that federal rule only covers public water systems. It says nothing about the private wells millions of people rely on. Our data spans both — public supply and private wells — so we can speak to a population the regulation doesn't reach.
:::

## Project Scope

- A **screening tool** — not a lab test, not a compliance ruling
- For agencies, water managers, researchers, communities
- Tap water + groundwater, one risk classification per site

::: notes
[Speaker: Raj] To be clear about what this is and isn't: this is a prioritization tool — it tells you where to look closer, not a legal determination that a specific well is safe or unsafe. The intended users are the people who'd act on that signal: public-health agencies, water-resource managers, researchers planning sampling campaigns. We're scoping to one classification per sampling site, covering both tap water and groundwater sources.
:::

## Data Sources

| Study | Role |
|---|---|
| Smalling et al., 2023 | Tap-water PFAS outcomes |
| Seawolf et al., 2023 | Land-use predictors |
| McMahon et al., 2022 | Groundwater — both predictors & outcomes |

::: notes
[Speaker: Raj] We're combining three public USGS datasets. Smalling gives us the outcome we're trying to predict — measured PFAS in tap water. Seawolf gives us the land-use predictors for those same sites — things like nearby industrial activity. And McMahon stands on its own: it covers groundwater wells across the Eastern U.S. and has both predictors and outcomes in one dataset. All three are public domain, CC0-licensed, and fully anonymized — no privacy concerns on the data side.
:::

## Data Quality: It Held Up

- **236** usable tap-water sites (Smalling/Seawolf)
- **254** usable groundwater sites (McMahon)
- Only 1 record dropped across the whole join

::: notes
[Speaker: Raj] Before trusting a target variable, we had to trust the data underneath it — and it held up well. Joining Smalling to Seawolf, we lost exactly one record. A handful of Seawolf columns were structurally missing — meaning "no facility observed nearby," not a data error — and we imputed those deliberately rather than dropping rows. End result: 236 clean tap-water sites and 254 clean groundwater sites, ready to build a target on top of.
:::

## The Pivot: From Median Split to ∑TQ

- Old plan: split sites by our own sample's median — **dropped**
- Why: treats every compound as equally dangerous, and it's relative to *us*, not a health standard
- New target: **∑TQ**, anchored on EPA's own compliance language

::: notes
[Speaker: Emir] This is the most important methodology decision we made. Our original plan classified sites as low/medium/high using the median of our own sample — but that treats every PFAS compound as equally dangerous, which they're not, and it's relative to us, not to any external health standard. So we scrapped it in favor of something anchored on an actual regulatory yardstick: ∑TQ. Let me quickly define that before we get to results.
:::

## What Is ∑TQ?

- **TQ** (toxicity quotient) = concentration ÷ EPA health benchmark, per compound
- **∑TQ** = TQ summed across the 6 EPA-regulated PFAS
- **< 0.5** reduced monitoring · **0.5–1.0** trigger · **≥ 1.0** MCL exceedance

::: notes
[Speaker: Emir] Here's the mechanics: for each of the six EPA-regulated compounds — PFOA, PFOS, PFHxS, PFNA, PFBS, and GenX — we divide the measured concentration by that compound's EPA health benchmark. That ratio is the toxicity quotient, TQ. Add up all six and you get ∑TQ, one number per site. EPA's own compliance language gives us three tiers from that number: under 0.5 is within reduced monitoring, 0.5 up to 1.0 is above the trigger, and 1.0 or higher is MCL exceedance — the same tiers used in the results on the next couple of slides.
:::

## ∑TQ — Tap Water

**Median ∑TQ: 0.17** (range 0–17.7, n=236)

Most sites well within reduced monitoring — a long right tail is what we're hunting for.

::: notes
[Speaker: Emir] So what does that look like in practice? Across 236 tap-water sites, the median ∑TQ is 0.17 — well under our 0.5 trigger threshold. Most sites are fine. But the range runs all the way up to 17.7, and that long tail — the sites way above the norm — is exactly what a prioritization tool should be built to catch.
:::

## ∑TQ — Groundwater, and a Catch

**Every McMahon site (n=254) clears both cutoffs — by construction**

- No GenX in this panel — 5 compounds, not 6
- Non-detects imputed at half the reporting limit, not zero
- **The two studies' ∑TQ scores are not directly comparable**

::: notes
[Speaker: Emir] Here's where we have to be honest about a limitation. Every single McMahon groundwater site scores above our exceedance cutoff — not because groundwater is uniformly worse, but because of how the score is built. McMahon's panel is missing GenX entirely, and its convention for non-detects — half the reporting limit instead of zero — inflates the floor for every "clean" site. So right now we cannot say groundwater is riskier than tap water; we can only say the two scores aren't computed the same way yet. Reconciling that is an open task — 3.4 — before we can train one model across both.
:::

# Evaluation Plan & Modeling Proposals

## Where Step 3 Stands

- ✅ Split strategy (3.3) — complete
- ⏳ Metrics, thresholds, groundwater reconciliation (3.1, 3.2, 3.4) — in progress, due 7/31

::: notes
[Speaker: Somyaranjan] Now let's turn to our evaluation plan and the two modeling proposals we're comparing for Checkpoint 2. Quick status check before we go further: the split strategy is done and Raj will walk through it next. Everything else in the evaluation plan — how we score the model, what "success" means, and reconciling that groundwater gap — is actively being worked toward Thursday's deadline. We're showing you the shape of the plan, not final numbers, because we'd rather be accurate than premature.
:::

## Split Strategy: Group by Study

- Whole **studies** held out together — not individual rows
- Benchmarked against `StratifiedGroupKFold`
- Verified: zero overlapping sites or studies across train/test

::: notes
[Speaker: Raj] The risk with PFAS data specifically is that sites from the same study tend to resemble each other — same sampling protocol, similar geography — so a naive random split lets the model "cheat" by seeing near-duplicates on both sides. We hold out entire studies instead, scored against candidate splits for class balance and coverage, and benchmarked that scoring against scikit-learn's own StratifiedGroupKFold. We then verified directly: zero shared sites, zero shared studies between train and test. [Presenter note: pull the actual partition and leakage numbers from running checkpoint_2.py before recording.]
:::

## Metrics & Success Thresholds

**In progress — Task 3.1 / 3.2**

Per-class precision, recall, F1 — weighted toward catching high-risk sites over avoiding false alarms.

::: notes
[Speaker: Somyaranjan] We know a missed high-risk site is more costly than a false alarm, so our metrics plan leans toward recall on the highest-risk tier specifically, not just overall accuracy. We're not locking in an exact number here yet — that lands once the tier definitions from Task 3.2 are finalized — but the direction is set.
:::

## Two Competing Proposals

| | Proposal A | Proposal B |
|---|---|---|
| Approach | Interpretable baseline | Hierarchical / ensemble |
| Lead | Raj | Emir |
| Optimized for | Legibility, trust | Non-linear land-use interactions |

::: notes
[Speaker: Emir] Rather than committing to one model, we're running two proposals in parallel, evaluated on the same split and the same metrics so they're a fair comparison. Proposal A is a simple, auditable model an operator could actually trust and inspect. Proposal B trades some of that legibility for the ability to capture non-linear interactions the baseline can't. May the better-performing, still-explainable model win.
:::

## Proposal A — Interpretable Baseline

Logistic regression / shallow decision tree on land-use predictors.

**Status:** approach set — training pending (Task 4.1)

::: notes
[Speaker: Raj] My baseline: a logistic regression or shallow decision tree, deliberately kept simple, predicting the ∑TQ tier straight from land-use features. The approach is locked in; what's not done yet is running it — that's Task 4.1, and we'll have real numbers by evaluation.
:::

## Proposal B — Hierarchical / Ensemble

Random forest / gradient boosting, capturing non-linear interactions.

**Status:** approach set — training pending (Task 4.3)

::: notes
[Speaker: Emir] My proposal pushes further — an ensemble method that can model interactions a linear approach would miss entirely. Same story as Proposal A: the design is done, execution is Task 4.3, and I'll bring back real results rather than guess at them here.
:::

## Validation & Trade-offs

**Step 5 (EVAL) begins 7/31**

Accuracy vs. interpretability vs. compute cost — head to head, same split, same metrics.

::: notes
[Speaker: Somyaranjan] Once both models are trained, I run them against the same held-out test set and the same metrics, and we'll report the real trade-off — not just which model scores higher, but whether that gain is worth losing some interpretability. That comparison is what Step 5 delivers, starting the day after tomorrow.
:::

# Wrap-Up

## What's Left

| Deliverable | Owner | Due |
|---|---|---|
| Writeup | Yai | 8/2 |
| This deck | Yai, All | 8/1 |
| 15-min video | All | 8/1–8/2 |
| Peer review | All | 8/2 |

::: notes
[Speaker: Yai] Let's close with where things stand and what's next. Here's what's left on our end: the writeup wraps by August 2nd, this deck is due tomorrow, and we record the 15-minute walkthrough right after, splitting sections across the four of us — the same way we just split this presentation. Peer review of another team's checkpoint closes out the week.
:::

## Where We Go Next

- Untested predictors: PFAS-site proximity, facility counts
- Only 6 of 17 reported PFAS compounds have EPA MCLs
- Reconcile Smalling vs. McMahon ∑TQ before one shared target

::: notes
[Speaker: Somyaranjan] Looking past this checkpoint: we've flagged some promising predictors — distance to the nearest PFAS site, nearby facility counts — that haven't been tested against the model yet. We're also only using 6 of the 17 PFAS compounds Smalling reports, because those are the only ones with EPA benchmarks; the rest stay descriptive for now. And the biggest open thread is reconciling the tap-water and groundwater ∑TQ scores so we can eventually train across both.
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
[Speaker: Yai] These are the sources behind the data and the regulatory timeline we've cited — full citations are on screen, and we're happy to send the list along with the deck rather than read through it here.
:::

## Thank You

Questions?

**Team .egsy intelligence** — Emir Beg · Gulshan Raj Shetty · Somyaranjan Sahu · Yaisiel Torres

::: notes
[Speaker: All] Yai: That's where we stand — solid data and a defensible pivot to ∑TQ. Raj: One evaluation piece done, the rest in flight for Thursday. Emir: Two modeling proposals ready to run. Somyaranjan: And a clear plan for how we'll judge them. All: Thanks for listening — happy to take questions.
:::

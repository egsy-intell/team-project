# Reusing the merged frame in QA cells

**Branch:** `GRS_Data_Explore`  
**Session:** `098f34d1`  
**Span:** Jul 19, 01:49–01:53 UTC  
**Exchange:** 1 prompts, 6 responses

**Commits produced:**

- `b38b12d` Reuse ss_merged_df in Smalling/Seawolf quality assessment cells
- `f95f2e0` Dedupe join-ability check into Unmatched rows section

[← back to the pairing-log timeline](https://egsy-intell.github.io/team-project/ai/ytorresv.html)

---

### Yai

`ss_merged_df` and `mac_merged_df` is meant to hold the data being utilized in the data exploration section for analysis. The author decided to use their own frames as opposed to reuse. Could you:
1. Use the mentioned dfs as the main source for processing and, adjust outputs and displays based on it?

### Claude

Now the Smalling Quality Assessment cell.

### Claude

Now the Seawolf Data Exploration cell.

### Claude

Now the Seawolf Quality Assessment cell.

### Claude

Lint passes clean. Let's also confirm the notebook actually runs end-to-end without errors.

### Claude

The notebook exports cleanly with no cell errors — confirms the refactored cells execute correctly end-to-end.

### Claude

Both Smalling and Seawolf Data Exploration/Quality Assessment sections now source from `ss_merged_df` instead of re-reading raw CSVs (McMahon's sections already used `mac_merged_df`). Key adjustments made to reflect the join:

- Outputs now reference the merged frame's shape and note it's `ss_merged_df`-derived.
- PFAS columns in `ss_merged_df` are already cleaned (`nd`→0, numeric), so the "coded as 'nd'" check was replaced with a check for cleaned zero-values, since the raw sentinel is no longer distinguishable at that point.
- `Study` collided between Smalling/Seawolf during the merge → `Study_smalling`/`Study_seawolf`; updated references accordingly.
- Since `ss_merged_df` is a left join (1 of 237 Smalling sites has no Seawolf match), the Seawolf checks now surface that unmatched row as missing identifiers/predictors and call it out in the suitability write-up — a real signal the old independent-read version couldn't show.

Verified with `uv run marimo check` (clean, no lint errors) and a full `marimo export html` run (no cell exceptions).


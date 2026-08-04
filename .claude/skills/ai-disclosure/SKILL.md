---
name: ai-disclosure
description: Generate or update a teammate's individual AI Tool Use Policy disclosure page (docs/ai/<person>.html) and transcripts (docs/ai/logs/<person>/) for this repo. Use when asked to "generate my AI disclosure", "add my AI use log", "document my Claude usage for this project", or similar.
---

This is a thin pointer, not a duplicate of the real instructions — the
actual runbook lives at
[`docs/ai/skill/README.md`](../../../docs/ai/skill/README.md) and is
written to be tool-agnostic (any AI coding agent should be able to
follow it, not just Claude Code), so it belongs in the repo itself
rather than under `.claude/`.

Read that file and follow it in full. In short:

1. Gather the person's conversation threads into a manifest.json +
   transcript files under `docs/ai/logs/<person>/` — Claude Code
   specifically has local session logs you can parse directly (the
   runbook has the exact recipe); other tools need a more manual
   approach, also covered there.
2. Render the disclosure page with
   `uv run python scripts/toolkit.py ai-disclosure <person>`.
3. Paste the generated `_readme_snippet.md` into `README.md`'s
   "Pair-programming sessions" list.

Also read [`docs/ai/skill/POLICY.md`](../../../docs/ai/skill/POLICY.md)
for the actual course policy this disclosure responds to, and
[`docs/ai/skill/manifest.example.json`](../../../docs/ai/skill/manifest.example.json)
for a worked example of the manifest format.

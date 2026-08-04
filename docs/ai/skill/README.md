# Generating an AI-use disclosure

A runbook for producing your own `docs/ai/<you>.html` disclosure page and
`docs/ai/logs/<you>/` transcripts, per the course's
[AI Tool Use Policy](POLICY.md). Written so **any AI coding agent** can
follow it on your behalf — Claude Code, GitHub Copilot, Cursor, whatever
you're pairing with — not just Claude. If you're an agent reading this
because your teammate asked you to "generate my AI disclosure" or
similar, this whole file is your instructions.

The process has two halves that are deliberately kept separate:

1. **Gathering your thread history** — inherently tool-specific, since
   Claude Code, Copilot, and Cursor each store (or don't store) session
   history completely differently. This half is on you/your agent to do
   by whatever means that tool offers. See [Step 1](#step-1-gather-your-threads).
2. **Rendering the disclosure page** — fully tool-agnostic and already
   built: `scripts/toolkit.py ai-disclosure` turns a small JSON manifest
   plus your transcript files into `docs/ai/<you>.html` and
   `docs/ai/logs/<you>/index.md`, matching the house style every other
   teammate's disclosure uses. See [Step 3](#step-3-render-it).

## Step 1: Gather your threads

A "thread" here means one continuous conversation with your AI tool
that produced real work — not every single chat message you've ever
sent it. For each thread you want to disclose, you need:

- **A transcript**: the prompts and responses, in order, as plain text.
  No tool-call/tool-result mechanics (no "ran `git commit`", no raw
  diffs, no file-read dumps) — just what was actually said. Save each
  thread as its own file, e.g. `docs/ai/logs/<you>/01-fixing-a-bug.md`,
  formatted with a `### <your name>` / `### <tool name>` heading per
  turn (see `docs/ai/skill/01-fixing-the-split-test.md` for the shape,
  or any file under an existing teammate's `docs/ai/logs/<name>/`).
- **Metadata**: title, branch, a rough date/time, and (if you want
  automatic commit matching) precise start/end timestamps — see
  [Step 2](#step-2-attribute-commits).

**Before saving anything**, scan your transcripts for secrets you might
have pasted in along the way (API keys, tokens, personal file paths,
`.env` contents) and redact them. This file becomes a permanent, public
part of the repo.

### If you're Claude Code

Session logs live locally on the machine that ran them, one file per
session:

- `~/.claude/projects/<encoded-repo-path>/*.jsonl` for sessions run
  directly in this checkout
- `~/.claude/projects/<encoded-repo-path>--claude-worktrees-<name>/*.jsonl`
  for sessions run inside a `.claude/worktrees/<name>/` git worktree, if
  you've used any

(`<encoded-repo-path>` is the absolute path to this checkout with `/`
replaced by `-`.) Each line is one JSON object. To extract a readable
transcript: walk the file in order, and for every object with
`"type": "user"` or `"type": "assistant"`, pull the `"text"`-type
entries out of `message.content` (skip `tool_use`/`tool_result`
entries entirely — that's the mechanical noise this format excludes).
User turns often carry injected IDE context wrapped in tags like
`<ide_opened_file>`/`<ide_selection>`/`<system-reminder>` ahead of what
was actually typed — strip those tags out rather than including them
verbatim. `d["timestamp"]` on each line gives you the thread's start/end
for Step 2, and `d["gitBranch"]` on user entries gives you the branch.

### If you're GitHub Copilot, Cursor, or something else

These tools don't expose local session logs the same way. Use whatever
that tool offers — Copilot Chat's "Export Chat"/copy-from-panel,
Cursor's chat history panel, etc. — or, if nothing's exportable,
reconstruct the transcript from memory/scrollback right after finishing
a piece of work, before it scrolls away. It's fine if this is manual;
it only has to happen once per thread, not continuously.

## Step 2: Attribute commits

Each thread should show the commit(s) it produced. Two ways to do this,
per thread, in your manifest (see [Step 3](#step-3-render-it)):

- **Automatic** (recommended): give the thread `"start"` and `"end"`
  ISO-8601 timestamps, and a top-level `"git_author_patterns"` list
  (name/email substrings matching your own commits). The renderer runs
  `git log --all --author=<pattern> ...` and attributes any commit
  inside `[start - 20min, end + 20min]` to that thread automatically.
  This is **not** based on commit trailers (`Co-Authored-By:` or
  similar) — plenty of teammates won't tag commits that way, so
  attribution is by author identity and timing only, nothing else.
- **Manual**: list `"commits": [{"hash": ..., "subject": ...}, ...]`
  directly on the thread. Use this when you don't have precise
  timestamps, or want to override/hand-pick what a thread shows.

## Step 3: Render it

Write `docs/ai/logs/<you>/_manifest.json` (`<you>` is whatever directory
name you want your disclosure under — a Purdue ID matches the existing
convention). Required top-level fields:

| Field | Type | Meaning |
|---|---|---|
| `person` | string | Must match the directory name |
| `display_name` | string | Your full name |
| `tool` | string | e.g. `"Claude Code"`, `"GitHub Copilot"` |
| `tool_tier` | string | Private/subscription/public, per the policy — e.g. `"Copilot Individual (personal subscription)"` |
| `how` | string | One or two sentences: how you used it |
| `why` | string | One or two sentences: why |
| `threads` | array | See below |

Optional top-level fields: `total_commits` (your all-time commit count,
enables a "% of my commits" stat), `date_range` (display string),
`git_author_patterns` (see Step 2), `policy_url` (defaults to the
Brightspace link), `phases` (see below).

Each entry in `threads` needs `title`, `branch`, `date` (display
string), and `transcript` (filename, relative to the manifest — must
exist alongside it). Optional per-thread: `quote` (a real, trimmed
opening line — not paraphrased), `prompts`/`responses` (turn counts),
`start`/`end`/`commits` (Step 2), and `phase`.

`phases` is entirely optional narrative structure — grouping threads
into milestones with their own heading and blurb, the way
[`docs/ai/ytorresv.html`](../ytorresv.html) does. Skip it for a flat,
chronological list; use it if you want the same "Kickoff → ... → Final
polish" arc treatment. If you use it, **every** thread needs a `phase`
key (the renderer errors instead of silently dropping unphased threads
into nowhere).

Full worked example: [`manifest.example.json`](manifest.example.json)
(with matching placeholder transcripts alongside it in this directory —
copy all three into `docs/ai/logs/<you>/` as a starting skeleton if
that's easier than writing one from scratch).

Then render:

```bash
uv run python scripts/toolkit.py ai-disclosure <you>
```

This writes:

- `docs/ai/<you>.html` — your disclosure page
- `docs/ai/logs/<you>/index.md` — an index of your transcripts
- `docs/ai/logs/<you>/_readme_snippet.md` — a ready-to-paste bullet for
  the next step

Pass `--skip-git` to skip the automatic commit lookup and use only
what's explicitly listed in the manifest (useful if you're iterating on
wording and don't want to wait on `git log`, or if you're rendering
outside a git checkout).

## Step 4: Wire it into README.md

Open `docs/ai/logs/<you>/_readme_snippet.md` and paste its contents into
the **Pair-programming sessions** list in the repo's `README.md`,
replacing your own placeholder bullet there. Review the generated
prose — it's a reasonable first draft from your manifest's `how`/`why`
fields, not guaranteed to read perfectly; adjust as needed before
committing.

## Regenerating

Whenever you've done more pairing worth disclosing: add thread(s) to
your manifest (and their transcript files), then re-run the same
`ai-disclosure` command — it fully regenerates `docs/ai/<you>.html` and
the logs index from the manifest each time, so there's nothing to hand-edit
in those two output files directly.

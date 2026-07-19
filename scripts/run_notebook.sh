#!/usr/bin/env bash
# Run a published notebook straight from gh-pages with uvx, no local checkout
# required. marimo downloads the notebook, uv installs its declared
# dependencies (see the PEP 723 header at the top of each notebooks/*.py
# file) into an isolated environment, and the notebook's own data-loading
# cells fetch data/usgs and any sibling modules from GitHub the first time
# they're needed.
#
# Usage:
#   scripts/run_notebook.sh [notebook-name] [edit|run]
#
# Examples:
#   scripts/run_notebook.sh                       # edit checkpoint_1 (default)
#   scripts/run_notebook.sh checkpoint_1 run       # run checkpoint_1 as a read-only app
#   scripts/run_notebook.sh data_dictionary edit   # edit data_dictionary

set -euo pipefail

NOTEBOOK="${1:-checkpoint_1}"
MODE="${2:-edit}"

if [[ "$MODE" != "edit" && "$MODE" != "run" ]]; then
  echo "Unknown mode '$MODE'. Use 'edit' or 'run'." >&2
  exit 1
fi

if ! command -v uvx >/dev/null 2>&1; then
  echo "uvx not found. Install uv first: https://astral.sh/uv/install.sh" >&2
  exit 1
fi

NOTEBOOK_URL="https://egsy-intell.github.io/team-project/notebooks/${NOTEBOOK}.py"

echo "Launching '$NOTEBOOK' ($MODE) from $NOTEBOOK_URL"
exec uvx marimo "$MODE" --sandbox "$NOTEBOOK_URL"

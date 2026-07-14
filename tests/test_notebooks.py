import json
import pathlib
import re
import subprocess
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"
NOTEBOOKS = sorted(NOTEBOOKS_DIR.glob("*.py"))

# e.g. "notebooks/checkpoint_1.py:42: teh ==> the"
CODESPELL_LINE_RE = re.compile(r"^(?P<file>.+):(?P<line>\d+): (?P<word>\S+) ==> (?P<fix>.+)$")


def _format_issue(issue: dict) -> str:
    location = f"{issue['filename']}:{issue['line']}:{issue['column']}"
    header = f"{location} [{issue['code']}] {issue['name']} ({issue['severity']})"
    lines = [header, f"  {issue['message']}"]
    if issue.get("fix"):
        lines.append(f"  fix: {issue['fix']}")
    return "\n".join(lines)


def _format_typo(match: re.Match) -> str:
    location = f"{match['file']}:{match['line']}"
    return f"{location} [spelling] '{match['word']}' -> '{match['fix']}'"


@pytest.mark.parametrize("notebook", NOTEBOOKS, ids=lambda p: p.name)
def test_notebook_lint(notebook):
    # marimo's `--strict` flag currently crashes when combined with
    # `--format json` (UnboundLocalError in marimo 0.23.14), so we don't pass
    # it. Instead we parse the JSON ourselves and fail on *any* reported
    # issue, including non-breaking warnings, which achieves the same "clean
    # lint bar" goal.
    result = subprocess.run(
        [sys.executable, "-m", "marimo", "check", "--format", "json", str(notebook)],
        capture_output=True,
        text=True,
    )
    report = json.loads(result.stdout)
    issues = report["issues"]
    if issues:
        formatted = "\n".join(_format_issue(issue) for issue in issues)
        pytest.fail(f"marimo check found issues in {notebook.name}:\n{formatted}")


@pytest.mark.parametrize("notebook", NOTEBOOKS, ids=lambda p: p.name)
def test_notebook_executes(notebook, tmp_path):
    output = tmp_path / f"{notebook.stem}.html"
    result = subprocess.run(
        [sys.executable, "-m", "marimo", "export", "html", str(notebook), "-o", str(output)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"marimo failed to execute {notebook.name}:\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert output.exists()


def test_notebooks_spelling():
    result = subprocess.run(
        [sys.executable, "-m", "codespell_lib", str(NOTEBOOKS_DIR)],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return

    lines = result.stdout.splitlines()
    matches = [CODESPELL_LINE_RE.match(line) for line in lines]
    if all(matches):
        formatted = "\n".join(_format_typo(m) for m in matches)
    else:
        # Fall back to raw output if codespell's format ever changes.
        formatted = result.stdout + result.stderr
    pytest.fail(f"codespell found issues:\n{formatted}")

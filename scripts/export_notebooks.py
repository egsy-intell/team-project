#!/usr/bin/env python3
"""Export every marimo notebook under notebooks/ to a standalone HTML file in dist/."""

import pathlib
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"
DIST_DIR = REPO_ROOT / "dist"


def main() -> int:
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    notebooks = sorted(NOTEBOOKS_DIR.glob("*.py"))
    if not notebooks:
        print(f"No notebooks found in {NOTEBOOKS_DIR}")
        return 1

    for notebook in notebooks:
        output = DIST_DIR / f"{notebook.stem}.html"
        print(f"Exporting {notebook.relative_to(REPO_ROOT)} -> {output.relative_to(REPO_ROOT)}")
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "marimo",
                "export",
                "html",
                str(notebook),
                "-o",
                str(output),
                "-f",
            ]
        )
        if result.returncode != 0:
            print(f"Failed to export {notebook.name}", file=sys.stderr)
            return result.returncode

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

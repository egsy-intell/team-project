#!/usr/bin/env python3
"""Export every marimo notebook under notebooks/ to docs/notebooks/.

Each notebook gets a standalone HTML export (for browsing) plus a copy of its
raw .py source (so it's reachable at a stable gh-pages URL and can be handed
directly to `uvx marimo edit/run --sandbox <url>`, which downloads and runs
it without needing a local checkout).
"""

import pathlib
import re
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"
OUTPUT_DIR = REPO_ROOT / "docs" / "notebooks"
PAGES_BASE = "https://egsy-intell.github.io/team-project/notebooks"

# Matches a PEP 723 inline script metadata block, e.g.:
#   # /// script
#   # requires-python = ">=3.14"
#   # ///
_PEP723_HEADER_RE = re.compile(r"^# /// script\n(?:#.*\n)*?# ///\n\n*", re.MULTILINE)


def _strip_pep723_header(source: str) -> str:
    # marimo's HTML export embeds the notebook's full source verbatim (used
    # to reconstruct cells/for the editor), so the PEP 723 dependency header
    # would otherwise leak into the published .html. It's only needed by
    # `uv`/`uvx` when reading the .py file directly, so export HTML from a
    # header-stripped copy and keep the header only in the raw .py we publish
    # alongside it.
    return _PEP723_HEADER_RE.sub("", source, count=1)


def _uvx_banner(notebook_name: str) -> str:
    notebook_url = f"{PAGES_BASE}/{notebook_name}"
    # marimo's own app root (#root) is styled position: static, but the app it
    # mounts inside is positioned absolute/top:0 relative to the page - which
    # would otherwise paint over a banner placed before #root in the markup.
    # Forcing #root to position: relative makes that absolute child position
    # itself relative to #root's own box instead, so our banner (which sits
    # right before #root, pushing #root down in normal flow) stays visible.
    # Reuse marimo's own design tokens (defined on :root by its stylesheets,
    # and theme-aware via CSS light-dark()) instead of hardcoded colors, so
    # the banner matches the notebook's look in both light and dark mode
    # rather than looking like an unrelated add-on.
    return f"""\
<style>#root {{ position: relative; }}</style>
<div style="
    font: 13px/1.5 var(--font-sans, ui-sans-serif, system-ui, sans-serif);
    color: var(--accent-foreground, var(--foreground));
    background: var(--accent, var(--muted));
    border-bottom: 1px solid var(--border);
    padding: 10px 16px;
  ">
  Run this notebook yourself, no clone required (needs
  <a href="https://docs.astral.sh/uv/getting-started/installation/" style="color: var(--link); text-decoration: underline;">uv</a>):
  <pre style="
      margin: 6px 0 0;
      white-space: pre-wrap;
      font-family: var(--marimo-monospace-font, ui-monospace, SFMono-Regular, Menlo, monospace);
      color: inherit;
    ">uvx marimo edit --sandbox {notebook_url}</pre>
</div>
"""


def _inject_uvx_banner(html_path: pathlib.Path, notebook_name: str) -> None:
    html = html_path.read_text()
    marker = '<div id="root"></div>'
    banner = _uvx_banner(notebook_name)
    if marker not in html:
        print(f"Warning: could not find {marker!r} in {html_path}, skipping uvx banner", file=sys.stderr)
        return
    html_path.write_text(html.replace(marker, banner + marker, 1))


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    notebooks = sorted(NOTEBOOKS_DIR.glob("*.py"))
    if not notebooks:
        print(f"No notebooks found in {NOTEBOOKS_DIR}")
        return 1

    for notebook in notebooks:
        output = OUTPUT_DIR / f"{notebook.stem}.html"
        print(f"Exporting {notebook.relative_to(REPO_ROOT)} -> {output.relative_to(REPO_ROOT)}")

        # Strip the PEP 723 header in place (rather than exporting from a
        # copy elsewhere) so relative sibling imports (data_dictionary.py)
        # and data/ lookups keep resolving locally instead of falling back
        # to a network fetch. Always restore the original file afterwards.
        source = notebook.read_text()
        notebook.write_text(_strip_pep723_header(source))
        try:
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
        finally:
            notebook.write_text(source)

        if result.returncode != 0:
            print(f"Failed to export {notebook.name}", file=sys.stderr)
            return result.returncode

        _inject_uvx_banner(output, notebook.name)

        source_copy = OUTPUT_DIR / notebook.name
        print(f"Copying {notebook.relative_to(REPO_ROOT)} -> {source_copy.relative_to(REPO_ROOT)}")
        source_copy.write_text(source)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

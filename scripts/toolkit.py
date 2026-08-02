#!/usr/bin/env python3
"""Project utility CLI: `presentation` builds the slide deck, `clean-notebook`
patches a marimo notebook export so it prints/PDFs cleanly.

    uv run python scripts/toolkit.py presentation [options]
    uv run python scripts/toolkit.py clean-notebook [options]

Run `uv run python scripts/toolkit.py <subcommand> --help` for each
subcommand's options.
"""

import argparse
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# `presentation`: build the checkpoint slide deck (preso/checkpoint2_deck.md)
# into a .pptx, styled by preso/template.pptx (a pandoc --reference-doc).
# ---------------------------------------------------------------------------

PRESO_DIR = REPO_ROOT / "preso"
SOURCE_MD = PRESO_DIR / "checkpoint2_deck.md"
TEMPLATE_PPTX = PRESO_DIR / "template.pptx"

# Pandoc has no markdown syntax to pick a slide layout by name - it
# auto-selects one per slide from the content's shape (see `pandoc`'s
# manual, "PowerPoint layout choice"). "Content with Caption" is what a
# short intro line followed by a table triggers, and we use it as this
# deck's "dense content" slide type (e.g. References). Table cells don't
# inherit font size from the layout's placeholder style the way plain
# text does, so shrinking them has to happen here, after pandoc has
# actually built the table.
DENSE_CONTENT_LAYOUT = "Content with Caption"
DENSE_TABLE_FONT_SIZE_PT = 14

# Without an explicit --slide-level, pandoc infers one by scanning for the
# highest (numerically smallest) heading level that's ever immediately
# followed by non-heading content anywhere in the document, and uses *that*
# level - and only that level - to start new slides. Our `#` section
# dividers (Findings So Far, Evaluation Plan & Modeling Proposals, Wrap-Up)
# used to have nothing directly under them but another `#`/`##` heading, so
# pandoc inferred slide-level 2 and every `##` correctly started its own
# slide. The moment a `#` divider gets its own `::: notes :::` block
# directly beneath it (so presenters have a script for that slide too),
# pandoc sees content under a level-1 heading and silently drops the
# inferred slide-level to 1 - collapsing every `##` section back down into
# whichever `#` divider contains it, instead of giving each its own slide.
# Pinning slide-level=2 makes `##` the permanent slide boundary regardless
# of what content ends up under a `#` divider.
SLIDE_LEVEL = 2


def _shrink_dense_tables(pptx_path: Path) -> None:
    from pptx import Presentation
    from pptx.util import Pt

    prs = Presentation(str(pptx_path))
    for slide in prs.slides:
        if slide.slide_layout.name != DENSE_CONTENT_LAYOUT:
            continue
        for shape in slide.shapes:
            if not getattr(shape, "has_table", False):
                continue
            for row in shape.table.rows:
                for cell in row.cells:
                    for paragraph in cell.text_frame.paragraphs:
                        for run in paragraph.runs:
                            run.font.size = Pt(DENSE_TABLE_FONT_SIZE_PT)
    prs.save(str(pptx_path))


def _open_in_default_app(path: Path) -> None:
    # Best-effort only: failing to auto-open should never fail the build.
    try:
        if sys.platform == "darwin":
            subprocess.run(["open", str(path)], check=True)
        elif sys.platform == "win32":
            os.startfile(str(path))  # type: ignore[attr-defined]
        else:
            print(f"Auto-open not supported on this platform; open {path} manually.")
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"Could not auto-open {path}: {exc}", file=sys.stderr)


def cmd_presentation(args: argparse.Namespace) -> int:
    try:
        import pypandoc
    except ImportError:
        print(
            "pypandoc/python-pptx are not installed. Install the "
            "presentation-build dependencies with:\n\n    uv sync --group preso\n",
            file=sys.stderr,
        )
        return 1

    if not SOURCE_MD.exists():
        print(f"Missing deck source: {SOURCE_MD.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1
    if not args.template.exists():
        print(
            f"Missing reference template: {args.template}\n"
            "See the README's presentation-pipeline section for how it's built.",
            file=sys.stderr,
        )
        return 1

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    output_stem = SOURCE_MD.stem
    if args.template != TEMPLATE_PPTX:
        output_stem += f"-{args.template.stem}"
    output_path = output_dir / f"{output_stem}.pptx"

    print(f"Building {SOURCE_MD.relative_to(REPO_ROOT)} -> {output_path}")
    try:
        pypandoc.convert_file(
            str(SOURCE_MD),
            to="pptx",
            outputfile=str(output_path),
            extra_args=["--reference-doc", str(args.template), "--slide-level", str(SLIDE_LEVEL)],
        )
    except RuntimeError as exc:
        print(f"pandoc conversion failed: {exc}", file=sys.stderr)
        return 1

    _shrink_dense_tables(output_path)

    print(f"Wrote {output_path}")

    if args.open:
        _open_in_default_app(output_path)

    return 0


def _add_presentation_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "presentation",
        help="Build the checkpoint slide deck (.pptx) from preso/checkpoint2_deck.md",
        description=cmd_presentation.__doc__ or "",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PRESO_DIR / "dist",
        help="Directory to write the generated .pptx into (default: preso/dist/)",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the generated .pptx in the default app afterward (best-effort)",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=TEMPLATE_PPTX,
        help="Reference-doc .pptx to style the deck with (default: preso/template.pptx)",
    )
    parser.set_defaults(func=cmd_presentation)


# ---------------------------------------------------------------------------
# `clean-notebook`: patch a marimo notebook HTML export so it prints/PDFs
# cleanly, instead of the blank pages, clipped tables, and orphaned headings
# marimo's own export produces out of the box.
# ---------------------------------------------------------------------------

DEFAULT_NOTEBOOK_URL = "https://egsy-intell.github.io/team-project/notebooks/"

# marimo's HTML export is a single-page app, not a paginated document, and
# none of its layout survives Chrome's print pagination unmodified:
#
#   - The whole notebook sits inside html/body/#root, which marimo pins to
#     one viewport-height with `overflow-y: auto` so the browser can
#     virtually "scroll" it on screen. Printing can't scroll, so anything
#     past the first screenful was clipped or rendered as blank pages.
#   - `mo.vstack()` (and the top-level wrapper around every cell) render as
#     CSS flex containers. Chrome's print engine can't fragment a flex
#     container across a page break, so a tall one gets forced onto a
#     single fresh page as one atomic unit, leaving a large blank gap on
#     the page before it.
#   - The content column is hard-capped at a fixed desktop width (e.g.
#     1110px for marimo's "medium" width), wider than a printed page, so
#     wide tables ran past the margin instead of wrapping.
#   - Headings had no "keep with next" rule, so a heading could land alone
#     at the bottom of a page with its content pushed to the next one.
#
# This CSS (scoped to @media print, so on-screen viewing is untouched) fixes
# all of that. See PRINT_SHADOW_FIX_JS below for the matching fix inside
# shadow DOM, which this stylesheet can't reach.
PRINT_FIX_CSS = """<style id="print-fixes">
@media print {
  @page {
    size: Letter;
    margin: 0.5in;
  }

  /* The app shell pins html/body/#root to one viewport-height, clipped panel
     (overflow-y: auto) so the browser can virtually "scroll" it on screen.
     Printing can't scroll, so everything past the first screenful was either
     blank or cut off. Let the whole chain flow to its natural height. */
  html,
  html > body,
  #root,
  #root > div,
  #root .absolute.inset-0,
  #_r_1_,
  #App {
    height: auto !important;
    max-height: none !important;
    overflow: visible !important;
    position: static !important;
  }

  /* The notebook column is hard-capped at a fixed desktop width (e.g. 1110px
     for "medium"), which is wider than a printed page and pushed content past
     the margins. Let it fill the printable page width instead. */
  :root {
    --content-width-medium: 100% !important;
    --content-width-small: 100% !important;
    --content-width-large: 100% !important;
    --content-width-full: 100% !important;
  }
  [class*="max-w-(--content-width"],
  #App,
  #_r_1_,
  #root > div,
  #root .absolute.inset-0 {
    width: 100% !important;
    max-width: 100% !important;
  }

  /* Every mo.vstack() renders as an inline-styled `display:flex;
     flex-flow:column` box, and Chrome's print engine cannot fragment flex
     containers across a page break: a tall vstack is forced onto a single
     page as one atomic unit, leaving a large blank gap on the page before it
     (or, if it's taller than a page, getting clipped). None of these stacks
     use row layout (marimo emits that separately), so it's safe to drop them
     to normal block flow for print, which fragments cleanly. */
  [style*="flex-flow: column"] {
    display: block !important;
  }

  /* Same problem, but for the one wrapper that lays out the whole notebook
     (all cells, top to bottom) via Tailwind's `flex flex-col` classes rather
     than an inline style: it's tens of thousands of pixels tall, so leaving
     it as a flex container blocks its children from fragmenting across
     pages too. */
  [class~="flex-col"] {
    display: block !important;
  }

  /* Keep headings attached to the content that follows them so a heading
     never lands alone at the bottom of a page (orphaned headers). */
  h1, h2, h3, h4, h5, h6 {
    break-after: avoid !important;
    break-inside: avoid !important;
    page-break-after: avoid !important;
    page-break-inside: avoid !important;
  }

  /* Keep tables, figures, code and math blocks from splitting mid-element
     across a page break. */
  table, marimo-table, marimo-mermaid, marimo-tex, pre, figure, svg {
    break-inside: avoid !important;
    page-break-inside: avoid !important;
  }
  tr {
    break-inside: avoid !important;
    page-break-inside: avoid !important;
  }
  thead {
    display: table-header-group;
  }
  p, li {
    orphans: 3;
    widows: 3;
  }

  /* Floating on-screen chrome (status badges, toast portals) has no meaning
     on paper and otherwise repeats on every printed page. */
  .fixed {
    display: none !important;
  }
}
</style>"""

# marimo custom elements (marimo-table, marimo-mime-renderer for matplotlib
# figures, etc.) render their content inside a shadow root, which the
# document-level stylesheet above can't reach (author stylesheets don't
# cross shadow boundaries). This script walks every shadow root and injects
# the equivalent print-only overrides directly into each one:
#
#   - Some data tables get fixed pixel column widths (sized for the
#     on-screen layout) that add up to wider than a printed page, clipping
#     the right-most columns. table-layout: fixed + width: 100% lets them
#     reflow to fit instead.
#   - matplotlib figures are embedded as full-resolution <img> (routinely
#     750px+ tall). Chrome can't split a raster image across a page break,
#     so an oversized one gets pushed whole onto a fresh page, leaving a
#     large blank gap on the page before it. Capping the height makes it
#     far more likely to fit in whatever room is left.
PRINT_SHADOW_FIX_JS = """<script id="print-shadow-fix">
(function () {
  var PRINT_SHADOW_CSS =
    "@media print {" +
    "table { table-layout: fixed !important; width: 100% !important; } " +
    "th, td { width: auto !important; max-width: none !important; " +
    "white-space: normal !important; overflow-wrap: break-word !important; " +
    "word-break: break-word !important; font-size: 8px !important; " +
    "line-height: 1.25 !important; padding: 2px 4px !important; } " +
    "img { max-height: 6in !important; width: auto !important; " +
    "height: auto !important; max-width: 100% !important; " +
    "object-fit: contain !important; }" +
    "}";
  function injectInto(shadowRoot) {
    if (shadowRoot.getElementById("print-shadow-style")) return;
    var style = document.createElement("style");
    style.id = "print-shadow-style";
    style.textContent = PRINT_SHADOW_CSS;
    shadowRoot.appendChild(style);
  }
  function fixShadowRoots(root) {
    root.querySelectorAll("*").forEach(function (el) {
      if (el.shadowRoot) {
        injectInto(el.shadowRoot);
        fixShadowRoots(el.shadowRoot);
      }
    });
  }
  function run() {
    fixShadowRoots(document);
  }
  window.addEventListener("beforeprint", run);
  window.addEventListener("load", function () {
    setTimeout(run, 500);
  });
})();
</script>"""


class NotebookCleanError(Exception):
    pass


def clean_notebook_html(html: str) -> str:
    """Inject the print-media patch into a marimo notebook HTML export."""
    if 'id="print-fixes"' in html:
        raise NotebookCleanError("input already contains the print-fixes patch")
    if html.count("</head>") != 1:
        raise NotebookCleanError(
            f"expected exactly one </head>, found {html.count('</head>')}"
        )
    if html.count("</body>") != 1:
        raise NotebookCleanError(
            f"expected exactly one </body>, found {html.count('</body>')}"
        )
    html = html.replace("</head>", f"{PRINT_FIX_CSS}\n</head>", 1)
    html = html.replace("</body>", f"{PRINT_SHADOW_FIX_JS}\n</body>", 1)
    return html


def _is_url(ref: str) -> bool:
    return ref.startswith(("http://", "https://"))


def _read_input(input_ref: str) -> str:
    if _is_url(input_ref):
        print(f"Downloading {input_ref}")
        with urllib.request.urlopen(input_ref) as resp:
            return resp.read().decode("utf-8")
    path = Path(input_ref)
    if not path.exists():
        raise NotebookCleanError(f"no such file: {path}")
    return path.read_text(encoding="utf-8")


def _default_stem(input_ref: str) -> str:
    # A trailing slash (a directory URL/path, e.g. the published
    # ".../notebooks/") resolves to that directory's index.html.
    if input_ref.endswith("/"):
        return "index"
    name = urllib.parse.urlparse(input_ref).path if _is_url(input_ref) else input_ref
    return Path(name).stem or "index"


def cmd_clean_notebook(args: argparse.Namespace) -> int:
    try:
        html = _read_input(args.input)
    except (NotebookCleanError, OSError, urllib.error.URLError) as exc:
        print(f"Failed to read {args.input}: {exc}", file=sys.stderr)
        return 1

    try:
        cleaned = clean_notebook_html(html)
    except NotebookCleanError as exc:
        print(f"Failed to patch {args.input}: {exc}", file=sys.stderr)
        return 1

    name = args.name or f"{_default_stem(args.input)}_clean.html"
    output_dir = args.output_dir or Path.cwd()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / name

    output_path.write_text(cleaned, encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


def _add_clean_notebook_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "clean-notebook",
        help="Patch a marimo notebook HTML export so it prints/PDFs cleanly",
        description=(
            "Download (or read locally) a marimo notebook HTML export and patch it "
            "with a print-only CSS/JS fix so PDF/print output doesn't have blank "
            "pages, tables clipped past the margin, or orphaned headings. The "
            "notebook's normal on-screen appearance is untouched."
        ),
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=DEFAULT_NOTEBOOK_URL,
        help=(
            "URL or local file path to a marimo HTML export "
            f"(default: the published full report, {DEFAULT_NOTEBOOK_URL})"
        ),
    )
    parser.add_argument(
        "--name",
        help="Output filename (default: <input stem>_clean.html)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory to write the output into (default: current directory)",
    )
    parser.set_defaults(func=cmd_clean_notebook)


# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", required=True)
    _add_presentation_parser(subparsers)
    _add_clean_notebook_parser(subparsers)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

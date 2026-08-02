import pathlib
import subprocess
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLKIT_SCRIPT = REPO_ROOT / "scripts" / "toolkit.py"
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"
# footer.py is the smallest real notebook (no heavy data loading/modeling),
# used here instead of the default index.py to keep these tests fast.
FOOTER_NOTEBOOK = NOTEBOOKS_DIR / "footer.py"

# A minimal stand-in for a marimo HTML export: just enough structure
# (<head>/<body> boundaries) for the patch to anchor on. clean-notebook
# doesn't touch anything else, so it doesn't need to look like real marimo
# output.
FIXTURE_HTML = """<!DOCTYPE html>
<html lang="en">
  <head>
    <title>fixture</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
"""


def _run_clean_notebook(*args, cwd=None):
    return subprocess.run(
        [sys.executable, str(TOOLKIT_SCRIPT), "clean-notebook", *args],
        capture_output=True,
        text=True,
        check=False,
        cwd=cwd,
    )


def test_clean_notebook_patches_local_file(tmp_path):
    fixture = tmp_path / "notebook.html"
    fixture.write_text(FIXTURE_HTML)

    result = _run_clean_notebook(str(fixture), "--output-dir", str(tmp_path))
    assert result.returncode == 0, result.stderr

    output_path = tmp_path / "notebook_clean.html"
    assert output_path.exists()

    cleaned = output_path.read_text()
    assert 'id="print-fixes"' in cleaned
    assert 'id="print-shadow-fix"' in cleaned
    # The patch must land inside <head>/<body>, not appended after them.
    assert cleaned.index('id="print-fixes"') < cleaned.index("</head>")
    assert cleaned.index('id="print-shadow-fix"') < cleaned.index("</body>")
    # Everything from the original document should still be present.
    assert '<div id="root"></div>' in cleaned


def test_clean_notebook_default_name_is_derived_from_input(tmp_path):
    fixture = tmp_path / "index.html"
    fixture.write_text(FIXTURE_HTML)

    result = _run_clean_notebook(str(fixture), "--output-dir", str(tmp_path))
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "index_clean.html").exists()


def test_clean_notebook_custom_name_and_dir(tmp_path):
    fixture = tmp_path / "index.html"
    fixture.write_text(FIXTURE_HTML)
    out_dir = tmp_path / "out"

    result = _run_clean_notebook(
        str(fixture), "--name", "report.html", "--output-dir", str(out_dir)
    )
    assert result.returncode == 0, result.stderr
    assert (out_dir / "report.html").exists()


def test_clean_notebook_rejects_already_patched_input(tmp_path):
    fixture = tmp_path / "notebook.html"
    fixture.write_text(FIXTURE_HTML)

    first = _run_clean_notebook(str(fixture), "--output-dir", str(tmp_path))
    assert first.returncode == 0, first.stderr

    already_clean = tmp_path / "notebook_clean.html"
    second = _run_clean_notebook(str(already_clean), "--output-dir", str(tmp_path))
    assert second.returncode != 0
    assert "already contains" in second.stderr


@pytest.mark.skipif(not FOOTER_NOTEBOOK.exists(), reason="notebooks/footer.py not found")
def test_clean_notebook_exports_local_py_notebook_without_code_by_default(tmp_path):
    result = _run_clean_notebook(str(FOOTER_NOTEBOOK), "--output-dir", str(tmp_path))
    assert result.returncode == 0, result.stderr

    cleaned = (tmp_path / "footer_clean.html").read_text()
    assert 'id="print-fixes"' in cleaned
    # marimo omits the notebook source entirely without --include-code.
    assert "__generated_with" not in cleaned
    # The notebook still ran and its output is embedded.
    assert "Conclusion" in cleaned

    # Exporting must not leave the real notebook file modified.
    assert "__generated_with" in FOOTER_NOTEBOOK.read_text()


@pytest.mark.skipif(not FOOTER_NOTEBOOK.exists(), reason="notebooks/footer.py not found")
def test_clean_notebook_include_code_embeds_source(tmp_path):
    result = _run_clean_notebook(
        str(FOOTER_NOTEBOOK), "--include-code", "--output-dir", str(tmp_path)
    )
    assert result.returncode == 0, result.stderr

    cleaned = (tmp_path / "footer_clean.html").read_text()
    assert "__generated_with" in cleaned

    # The PEP 723 header is stripped from the embedded source, but the
    # real file on disk must still have it afterward.
    assert FOOTER_NOTEBOOK.read_text().startswith("# /// script")


def test_clean_notebook_include_code_warns_for_non_py_input(tmp_path):
    fixture = tmp_path / "notebook.html"
    fixture.write_text(FIXTURE_HTML)

    result = _run_clean_notebook(
        str(fixture), "--include-code", "--output-dir", str(tmp_path)
    )
    assert result.returncode == 0, result.stderr
    assert "--include-code only applies" in result.stderr

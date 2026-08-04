import json
import pathlib
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLKIT_SCRIPT = REPO_ROOT / "scripts" / "toolkit.py"

VALID_MANIFEST = {
    "person": "fixtureperson",
    "display_name": "Fixture Person",
    "tool": "GitHub Copilot",
    "tool_tier": "Copilot Individual",
    "how": "Pair-programmed some cells.",
    "why": "To move faster.",
    "total_commits": 10,
    "date_range": "Jul 1-2",
    "threads": [
        {
            "title": "First thread",
            "branch": "main",
            "date": "Jul 1, 10:00",
            "quote": "how do I do X?",
            "transcript": "01-first.md",
            "prompts": 2,
            "responses": 3,
            "commits": [{"hash": "abc1234", "subject": "Do the thing"}],
        },
        {
            "title": "Second thread",
            "branch": "feature",
            "date": "Jul 2, 09:00",
            "transcript": "02-second.md",
            "commits": [],
        },
    ],
}


def _write_manifest(root, person, manifest, transcripts=("01-first.md", "02-second.md")):
    person_dir = root / "docs" / "ai" / "logs" / person
    person_dir.mkdir(parents=True, exist_ok=True)
    (person_dir / "_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    for name in transcripts:
        (person_dir / name).write_text("### Fixture Person\n\nhi\n", encoding="utf-8")
    return person_dir


def _run_ai_disclosure(root, person, *extra_args):
    return subprocess.run(
        [
            sys.executable, str(TOOLKIT_SCRIPT), "ai-disclosure", person,
            "--repo-root", str(root), *extra_args,
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def test_ai_disclosure_renders_html_and_logs_index(tmp_path):
    _write_manifest(tmp_path, "fixtureperson", VALID_MANIFEST)

    result = _run_ai_disclosure(tmp_path, "fixtureperson", "--skip-git")
    assert result.returncode == 0, result.stderr

    html_path = tmp_path / "docs" / "ai" / "fixtureperson.html"
    index_path = tmp_path / "docs" / "ai" / "logs" / "fixtureperson" / "index.md"
    snippet_path = tmp_path / "docs" / "ai" / "logs" / "fixtureperson" / "_readme_snippet.md"
    assert html_path.exists()
    assert index_path.exists()
    assert snippet_path.exists()

    html = html_path.read_text()
    # Both threads present, with their real content threaded through.
    assert "First thread" in html
    assert "Second thread" in html
    assert "how do I do X?" in html
    assert "Do the thing" in html
    assert "abc1234" in html
    # The four policy questions are answered explicitly.
    assert "Tool &amp; tier" in html
    assert "History of the exchange" in html
    # Balanced markup: this is templated HTML, not a fixed fixture, so a
    # gross tag-balance check is worth more here than in most tests.
    assert html.count("<div") == html.count("</div>")

    index_md = index_path.read_text()
    assert "01-first.md" in index_md
    assert "02-second.md" in index_md

    snippet = snippet_path.read_text()
    assert "Fixture Person" in snippet
    assert "GitHub Copilot" in snippet
    assert "2 threads" in snippet
    assert "1 commit" in snippet  # singular: only threads[0] has a commit


def test_ai_disclosure_singular_thread_and_commit_grammar(tmp_path):
    manifest = json.loads(json.dumps(VALID_MANIFEST))
    manifest["threads"] = [manifest["threads"][0]]
    _write_manifest(tmp_path, "soloperson", manifest, transcripts=("01-first.md",))

    result = _run_ai_disclosure(tmp_path, "soloperson", "--skip-git")
    assert result.returncode == 0, result.stderr

    snippet = (tmp_path / "docs" / "ai" / "logs" / "soloperson" / "_readme_snippet.md").read_text()
    assert "1 thread," in snippet
    assert "1 commit)" in snippet


def test_ai_disclosure_missing_manifest_fails_clearly(tmp_path):
    (tmp_path / "docs" / "ai" / "logs" / "nobody").mkdir(parents=True)

    result = _run_ai_disclosure(tmp_path, "nobody")
    assert result.returncode == 1
    assert "no manifest" in result.stderr
    assert "docs/ai/skill/README.md" in result.stderr


def test_ai_disclosure_missing_transcript_file_fails_clearly(tmp_path):
    manifest = json.loads(json.dumps(VALID_MANIFEST))
    _write_manifest(tmp_path, "brokenperson", manifest, transcripts=("01-first.md",))
    # 02-second.md deliberately not written.

    result = _run_ai_disclosure(tmp_path, "brokenperson", "--skip-git")
    assert result.returncode == 1
    assert "02-second.md" in result.stderr


def test_ai_disclosure_phase_without_top_level_phases_fails(tmp_path):
    manifest = json.loads(json.dumps(VALID_MANIFEST))
    manifest["threads"][0]["phase"] = "kickoff"
    _write_manifest(tmp_path, "phaseerror", manifest)

    result = _run_ai_disclosure(tmp_path, "phaseerror", "--skip-git")
    assert result.returncode == 1
    assert "no top-level 'phases' mapping" in result.stderr


def test_ai_disclosure_unphased_thread_in_phased_manifest_fails(tmp_path):
    manifest = json.loads(json.dumps(VALID_MANIFEST))
    manifest["phases"] = {"kickoff": {"title": "Kickoff", "blurb": "Start."}}
    manifest["threads"][0]["phase"] = "kickoff"
    # threads[1] deliberately left unphased.
    _write_manifest(tmp_path, "halfphased", manifest)

    result = _run_ai_disclosure(tmp_path, "halfphased", "--skip-git")
    assert result.returncode == 1
    assert "has no 'phase'" in result.stderr


def test_ai_disclosure_phases_render_milestones(tmp_path):
    manifest = json.loads(json.dumps(VALID_MANIFEST))
    manifest["phases"] = {"kickoff": {"title": "Kickoff", "blurb": "Start."}}
    for t in manifest["threads"]:
        t["phase"] = "kickoff"
    _write_manifest(tmp_path, "fullyphased", manifest)

    result = _run_ai_disclosure(tmp_path, "fullyphased", "--skip-git")
    assert result.returncode == 0, result.stderr

    html = (tmp_path / "docs" / "ai" / "fullyphased.html").read_text()
    assert 'class="tl-row milestone"' in html
    assert "Kickoff" in html


def test_ai_disclosure_example_manifest_from_skill_dir_is_valid(tmp_path):
    """The example manifest shipped in docs/ai/skill/ should always be a
    working starting point - this catches it silently rotting out of
    sync with the schema the renderer actually expects."""
    skill_dir = REPO_ROOT / "docs" / "ai" / "skill"
    example = json.loads((skill_dir / "manifest.example.json").read_text())

    person_dir = tmp_path / "docs" / "ai" / "logs" / example["person"]
    person_dir.mkdir(parents=True)
    (person_dir / "_manifest.json").write_text(json.dumps(example), encoding="utf-8")
    for thread in example["threads"]:
        source = skill_dir / thread["transcript"]
        assert source.exists(), f"missing example transcript: {source}"
        (person_dir / thread["transcript"]).write_text(source.read_text(), encoding="utf-8")

    result = _run_ai_disclosure(tmp_path, example["person"], "--skip-git")
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "docs" / "ai" / f"{example['person']}.html").exists()

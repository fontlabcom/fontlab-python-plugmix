# this_file: tests/test_pack_workflow.py
"""Pin the pack workflow's permissions and the stdlib pack check."""

import re
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_pack  # noqa: E402
import check_pack  # noqa: E402

WORKFLOW = (ROOT / ".github/workflows/pack.yml").read_text(encoding="utf-8")


def _job(name: str) -> str:
    """Return the text of one top-level job block."""
    m = re.search(rf"^  {name}:\n(.*?)(?=^  \w[\w-]*:\n|\Z)", WORKFLOW, re.S | re.M)
    assert m, name
    return m.group(1)


def test_workflow_when_read_then_pinned_without_secrets_and_default_read_only():
    top = WORKFLOW.split("jobs:")[0]
    assert re.search(r"^permissions:\n  contents: read\n", top, re.M)
    assert "matrix" not in WORKFLOW and "secrets." not in WORKFLOW
    assert "set -eo pipefail" in WORKFLOW and "if-no-files-found: error" in WORKFLOW
    uses = re.findall(r"uses: (\S+)", WORKFLOW)
    assert len(uses) == 4
    assert all(re.fullmatch(r"[\w./-]+@[0-9a-f]{40}", u) for u in uses), uses


def test_workflow_when_read_then_only_release_job_can_write_and_only_contents():
    assert re.findall(r"^  (\w[\w-]*):\n", WORKFLOW.split("jobs:")[1], re.M) == [
        "pack",
        "release",
    ]
    assert not re.search(r": write\b", _job("pack"))
    perms = re.search(r"permissions:\n((?:      .+\n)+)", _job("release"))
    assert perms and perms.group(1).strip() == "contents: write"
    for forbidden in (
        "pages",
        "id-token",
        "pull-requests",
        "actions: write",
        "packages",
    ):
        assert forbidden not in WORKFLOW


def test_workflow_when_tag_pushed_then_release_attaches_the_checked_zip():
    assert re.search(r"tags: \['v\*'\]", WORKFLOW)
    job = _job("release")
    assert "needs: pack" in job
    assert "if: startsWith(github.ref, 'refs/tags/v')" in job
    assert (
        "download-artifact" in job and "name: fontlab-python-plugmix-extensions" in job
    )
    assert "gh release upload" in job and "--clobber" in job
    assert (
        not re.search(r"(^|[|&;]\s*|\|\| )\s*gh release create", job, re.M)
        and "--generate-notes" not in job
    )
    assert "seq 1 20" in job and "sleep 30" in job and "gh release view" in job
    assert "release not created by lander within 10 min" in job
    assert "dist/fontlab-python-plugmix-extensions.zip" in job and "test -s" in job
    assert "GH_TOKEN: ${{ github.token }}" in job
    assert "checkout" not in job and '--repo "$GITHUB_REPOSITORY"' in job
    assert "needs:" not in _job("pack") and "startsWith" not in _job("pack")


def test_workflow_when_run_then_does_not_need_the_app_checkout():
    assert "fontlabapp" not in WORKFLOW
    assert (
        "--noconftest" in WORKFLOW
        and 'grep -q "SKIPPED"' in WORKFLOW
        and "pytest==8.4.2" in WORKFLOW
    )
    for tool in ("build_pack", "check_pack"):
        text = (ROOT / "tools" / f"{tool}.py").read_text(encoding="utf-8")
        assert "fontlabapp" not in text


@pytest.fixture(scope="module")
def pack(tmp_path_factory) -> Path:
    return build_pack.build_pack(ROOT, tmp_path_factory.mktemp("pack"))


def test_check_pack_when_pack_built_then_no_problems(pack):
    assert check_pack.check_pack(pack) == []


def test_check_pack_when_entry_removed_or_added_then_reports_it(pack, tmp_path):
    bad = tmp_path / "bad.zip"
    with zipfile.ZipFile(pack) as src, zipfile.ZipFile(bad, "w") as dst:
        for info in src.infolist():
            if info.filename != "README.md" and "AllAngles" not in info.filename:
                dst.writestr(info, src.read(info))
        dst.writestr("Extensions/x/__pycache__/m.pyc", b"")
        dst.writestr("stray.txt", b"")
    problems = "\n".join(check_pack.check_pack(bad))
    assert "plugin.json files differ" in problems
    assert "missing README.md" in problems
    assert "bytecode in zip" in problems
    assert "unexpected top-level entry: stray.txt" in problems

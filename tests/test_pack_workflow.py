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


def test_workflow_when_read_then_read_only_pinned_single_job_without_secrets():
    assert "contents: read" in WORKFLOW and not re.search(r": write\b", WORKFLOW)
    assert WORKFLOW.count("runs-on:") == 1 and "matrix" not in WORKFLOW and "secrets" not in WORKFLOW
    assert "set -eo pipefail" in WORKFLOW and "if-no-files-found: error" in WORKFLOW
    uses = re.findall(r"uses: (\S+)", WORKFLOW)
    assert len(uses) == 3
    assert all(re.fullmatch(r"[\w./-]+@[0-9a-f]{40}", u) for u in uses), uses


def test_workflow_when_run_then_does_not_need_the_app_checkout():
    assert "fontlabapp" not in WORKFLOW
    assert "--noconftest" in WORKFLOW and 'grep -q "SKIPPED"' in WORKFLOW and "pytest==8.4.2" in WORKFLOW
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

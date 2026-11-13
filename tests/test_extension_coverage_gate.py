# this_file: tests/test_extension_coverage_gate.py
"""The reference pack gate requires both line and branch evidence."""

import json
import runpy
import sys
from pathlib import Path

import pytest

from check_coverage import main


@pytest.mark.parametrize("lines, branches, present, result", [
    (10, 8, True, 0), (7, 10, True, 1), (10, 7, True, 1),
    (10, 10, False, 1),
])
def test_bundle_gate_when_evidence_changes_then_enforces_both_rates(
    tmp_path, monkeypatch, lines, branches, present, result
):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / "Extensions/reporters/Example.fontlabReporter/plugin.py"
    source.parent.mkdir(parents=True)
    source.write_text("pass\n")
    (tmp_path / "initScript-snippet.py").write_text("pass\n")
    summary = {"num_statements": 10, "covered_lines": lines}
    if present:
        summary.update(num_branches=10, covered_branches=branches)
    report = tmp_path / "coverage.json"
    report.write_text(json.dumps({"files": {
        source.relative_to(tmp_path).as_posix(): {"summary": summary},
        "initScript-snippet.py": {"summary": {
            "num_statements": 10, "covered_lines": 10,
            "num_branches": 10, "covered_branches": 10
        }}
    }}))
    assert main(str(report)) == result


def test_startup_gate_when_evidence_missing_then_fails(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    report = tmp_path / "coverage.json"
    report.write_text('{"files": {}}')
    assert main(str(report)) == 1


@pytest.mark.parametrize("rate, present, result", [(80, True, 0), (79, True, 1), (80, False, 1)])
def test_compatibility_gate_when_evidence_changes_then_retains_original_threshold(
    tmp_path, monkeypatch, rate, present, result
):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / "src/fontlab_plugmix/example.py"
    source.parent.mkdir(parents=True)
    source.write_text("pass\n")
    records = {"initScript-snippet.py": {"summary": {
        "num_statements": 1, "covered_lines": 1, "num_branches": 0, "covered_branches": 0
    }}}
    if present:
        records["src/fontlab_plugmix/example.py"] = {"summary": {"percent_covered": rate}}
    report = tmp_path / "coverage.json"
    report.write_text(json.dumps({"files": records}))
    assert main(str(report)) == result


def test_coverage_cli_when_valid_then_returns_zero(tmp_path, monkeypatch):
    script = Path(__file__).with_name("check_coverage.py")
    monkeypatch.chdir(tmp_path)
    report = tmp_path / "coverage.json"
    report.write_text(json.dumps({"files": {"initScript-snippet.py": {"summary": {
        "num_statements": 0, "covered_lines": 0, "num_branches": 0, "covered_branches": 0
    }}}}))
    monkeypatch.setattr(sys, "argv", [str(script), str(report)])
    with pytest.raises(SystemExit) as error:
        runpy.run_path(str(script), run_name="__main__")
    assert error.value.code == 0


@pytest.mark.parametrize("lines, branches, result", [(8, 8, 0), (7, 10, 1), (10, 7, 1)])
def test_startup_gate_when_coverage_changes_then_enforces_each_threshold(
    tmp_path, monkeypatch, lines, branches, result
):
    monkeypatch.chdir(tmp_path)
    report = tmp_path / "coverage.json"
    report.write_text(json.dumps({"files": {"initScript-snippet.py": {"summary": {
        "num_statements": 10, "covered_lines": lines,
        "num_branches": 10, "covered_branches": branches
    }}}}))
    assert main(str(report)) == result

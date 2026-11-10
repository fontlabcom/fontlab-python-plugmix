# this_file: tests/test_extension_coverage_gate.py
"""The reference pack gate requires both line and branch evidence."""

import json

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
    summary = {"num_statements": 10, "covered_lines": lines}
    if present:
        summary.update(num_branches=10, covered_branches=branches)
    report = tmp_path / "coverage.json"
    report.write_text(json.dumps({"files": {
        source.relative_to(tmp_path).as_posix(): {"summary": summary}
    }}))
    assert main(str(report)) == result

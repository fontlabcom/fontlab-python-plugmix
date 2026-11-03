# this_file: tests/test_test_script.py
"""Shell runner edge cases work without contacting a package registry."""

import os
import subprocess
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "test.sh"


def test_runner_outside_git_explains_missing_checkout(tmp_path):
    env = os.environ.copy()
    env.pop("PLUGMIX_FONTLABAPP_SOURCE", None)
    result = subprocess.run(
        ["sh", str(SCRIPT)],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "checkout not found" in result.stderr
    assert "Set PLUGMIX_FONTLABAPP_SOURCE" in result.stderr
    assert "fatal: not a git repository" not in result.stderr


def test_runner_skips_coverage_gate_for_pytest_selectors(tmp_path):
    source = tmp_path / "fontlab-fontlabapp"
    source.mkdir()
    (source / "pyproject.toml").write_text("[project]\nname = 'fake'\n")
    mock_bin = tmp_path / "bin"
    mock_bin.mkdir()
    for name, code in (("uv", 0), ("python3", 99)):
        command = mock_bin / name
        command.write_text(f"#!/bin/sh\nexit {code}\n")
        command.chmod(0o755)
    env = os.environ.copy()
    env["PLUGMIX_FONTLABAPP_SOURCE"] = str(source)
    env["PATH"] = f"{mock_bin}:{env['PATH']}"
    selected = subprocess.run(
        ["sh", str(SCRIPT), "-k", "reporter"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    full = subprocess.run(
        ["sh", str(SCRIPT)],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert selected.returncode == 0, selected.stderr
    assert full.returncode == 99, "the full run must execute the coverage gate"

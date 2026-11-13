# this_file: tests/test_test_script.py
"""Shell runner edge cases work without contacting a package registry."""

import os
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "test.sh"


def test_runner_explains_missing_override_checkout(tmp_path):
    env = os.environ.copy()
    env["PLUGMIX_FONTLABAPP_SOURCE"] = str(tmp_path / "missing")
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


def test_runner_prefers_sibling_worktree_outside_git_cwd(tmp_path):
    mock_bin = tmp_path / "bin"
    mock_bin.mkdir()
    uv = mock_bin / "uv"
    uv.write_text('#!/bin/sh\nprintf "%s\\n" "$@"\n')
    uv.chmod(0o755)
    env = os.environ.copy()
    for name in ("PLUGMIX_FONTLABAPP_SOURCE", "PLUGMIX_PENS_SOURCE", "PLUGMIX_FLY_SOURCE"):
        env.pop(name, None)
    env["PATH"] = f"{mock_bin}:{env['PATH']}"
    result = subprocess.run(
        ["sh", str(SCRIPT), "-k", "impossible_selector"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    sibling = SCRIPT.parent.parent / "fontlab-fontlabapp"
    assert result.returncode == 0, result.stderr
    assert f"fontlab-fontlabapp @ file://{sibling}" in result.stdout
    assert "cpython-3.11-macos-aarch64-none" in result.stdout
    assert str(SCRIPT.parent.parent / "fontlab-python-pens") in result.stdout


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


@pytest.mark.parametrize("variable, guidance", [
    ("PLUGMIX_FLY_SOURCE", "fontlab-fly source not found"),
    ("PLUGMIX_PENS_SOURCE", "fontlab-python-pens checkout not found"),
])
def test_runner_when_selected_peer_missing_then_explains_override(tmp_path, variable, guidance):
    env = {**os.environ, variable: str(tmp_path / "missing")}
    result = subprocess.run(["sh", str(SCRIPT)], env=env, capture_output=True,
                            text=True, check=False)
    assert result.returncode == 2
    assert guidance in result.stderr and variable in result.stderr


def test_runner_when_fly_override_selected_then_exports_exact_source(tmp_path):
    mock_bin = tmp_path / "bin"
    mock_bin.mkdir()
    uv = mock_bin / "uv"
    uv.write_text('#!/bin/sh\nprintf "%s\\n" "$PYTHONPATH"\n')
    uv.chmod(0o755)
    fly = tmp_path / "fly-checkout"
    (fly / "src/fly").mkdir(parents=True)
    (fly / "src/fly/__init__.py").touch()
    env = {**os.environ, "PLUGMIX_FLY_SOURCE": str(fly),
           "PATH": f"{mock_bin}:{os.environ['PATH']}"}
    result = subprocess.run(["sh", str(SCRIPT), "-k", "unused"], env=env,
                            capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    assert result.stdout.split(":")[0].strip() == str(fly / "src")

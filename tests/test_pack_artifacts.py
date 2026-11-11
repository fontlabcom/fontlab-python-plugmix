# this_file: tests/test_pack_artifacts.py
"""The deliverable Extensions pack is a zip; the wheel is the compatibility package only."""

import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_pack  # noqa: E402

BUNDLES = [row["bundle"] + "/plugin.json" for row in json.loads((ROOT / "tests/bundle-map.json").read_text())]


@pytest.fixture(scope="module")
def pack(tmp_path_factory) -> Path:
    return build_pack.build_pack(ROOT, tmp_path_factory.mktemp("pack"))


def test_build_pack_when_built_then_zip_holds_exactly_the_mapped_plugin_manifests(pack):
    with zipfile.ZipFile(pack) as zf:
        names = zf.namelist()
    assert sorted(n for n in names if n.endswith("/plugin.json")) == sorted(BUNDLES)
    assert len(BUNDLES) == 50


def test_build_pack_when_built_then_zip_adds_only_script_and_readme(pack):
    with zipfile.ZipFile(pack) as zf:
        names = zf.namelist()
    assert "Scripts/Plugmix/Show Reporters.py" in names
    assert "README.md" in names
    assert not [n for n in names if "__pycache__" in n or n.endswith(".pyc")]
    assert all(n.startswith(("Extensions/", "Scripts/")) or n == "README.md" for n in names)


def test_build_pack_when_extracted_then_registry_discovers_all_fifty(pack, tmp_path):
    from fontlabapp.plugins import registry

    with zipfile.ZipFile(pack) as zf:
        zf.extractall(tmp_path)
    errors = []
    found = registry.discover(lambda *args: errors.append(args), tmp_path / "Extensions")
    assert errors == []
    assert len(found) == 50


def test_build_pack_when_extensions_missing_then_error_names_the_pack(tmp_path):
    with pytest.raises(FileNotFoundError, match="Extensions pack"):
        build_pack.build_pack(tmp_path, tmp_path / "out")


def test_pytest_when_extensions_folder_missing_then_usage_error_names_the_pack(tmp_path):
    shutil.copytree(ROOT / "tests", tmp_path / "tests", ignore=shutil.ignore_patterns("__pycache__"))
    (tmp_path / "pyproject.toml").write_text("[tool.pytest.ini_options]\n")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "-q", "tests/test_extension_manifest.py"],
        cwd=tmp_path, capture_output=True, text=True,
        env={**os.environ, "PYTHONPATH": os.pathsep.join(str(Path(p).resolve()) for p in sys.path if p)},
    )
    output = result.stdout + result.stderr
    assert result.returncode != 0
    assert "fontlab-python-plugmix-extensions.zip" in output, output
    assert "INTERNALERROR" not in output, output


@pytest.mark.skipif(shutil.which("uv") is None, reason="uv is needed to build the wheel")
def test_wheel_when_built_then_it_has_the_compatibility_package_and_no_pack(tmp_path):
    env = {**os.environ, "SETUPTOOLS_SCM_PRETEND_VERSION": "1.0.0"}
    build = subprocess.run(
        ["uv", "build", "--wheel", "--out-dir", str(tmp_path), str(ROOT)],
        capture_output=True, text=True, env=env,
    )
    if build.returncode != 0:
        pytest.skip("uv could not build the wheel (no network or cache for build requirements)")
    (wheel,) = tmp_path.glob("*.whl")
    with zipfile.ZipFile(wheel) as zf:
        names = zf.namelist()
    assert any(n.startswith("fontlab_plugmix/") for n in names)
    assert not [n for n in names if n.startswith(("Extensions/", "Scripts/")) or n.endswith("plugin.json")]

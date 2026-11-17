# this_file: tests/test_pack_artifacts.py
"""The deliverable Extensions pack is a zip; the wheel is the compatibility package only."""

import json
import os
import shutil
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_pack

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
    assert all(n.startswith(("Extensions/", "Scripts/")) or n in {"README.md", "LICENSE", "NOTICE"} for n in names)


@pytest.mark.parametrize("name", ["LICENSE", "NOTICE"])
def test_build_pack_when_built_then_legal_member_matches_source_bytes(pack, name):
    with zipfile.ZipFile(pack) as zf:
        assert zf.read(name) == (ROOT / name).read_bytes()


def test_build_pack_when_repeated_then_preserves_payload_order_metadata_and_bytes(pack, tmp_path):
    sources = [
        path
        for top in (ROOT / "Extensions", ROOT / "Scripts" / "Plugmix")
        for path in sorted(top.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    ] + [ROOT / name for name in ("README.md", "LICENSE", "NOTICE")]
    with zipfile.ZipFile(pack) as zf:
        assert zf.namelist() == [path.relative_to(ROOT).as_posix() for path in sources]
        for path, info in zip(sources, zf.infolist(), strict=True):
            expected = zipfile.ZipInfo.from_file(path, path.relative_to(ROOT).as_posix())
            assert zf.read(info) == path.read_bytes(), info.filename
            assert info.date_time == (*expected.date_time[:5], expected.date_time[5] // 2 * 2), info.filename
            assert info.external_attr == expected.external_attr, info.filename
            assert info.compress_type == zipfile.ZIP_DEFLATED, info.filename
    repeated = build_pack.build_pack(ROOT, tmp_path / "repeat")
    assert repeated.read_bytes() == pack.read_bytes()


@pytest.fixture
def legal_pack_source(tmp_path):
    root = tmp_path / "source"
    (root / "Extensions").mkdir(parents=True)
    for name in ("README.md", "LICENSE", "NOTICE"):
        shutil.copy2(ROOT / name, root / name)
    return root


@pytest.mark.parametrize("name", ["README.md", "LICENSE", "NOTICE"])
@pytest.mark.parametrize("prior_output", [False, True])
def test_build_pack_when_legal_file_missing_then_refuses_with_its_path(
    tmp_path, name, prior_output, legal_pack_source, pack,
):
    out_dir = tmp_path / "out"
    target = out_dir / build_pack.PACK_NAME
    if prior_output:
        out_dir.mkdir()
        shutil.copy2(pack, target)
        target.chmod(0o640)
        before = target.read_bytes()
    (legal_pack_source / name).unlink()
    with pytest.raises(FileNotFoundError, match=name) as error:
        build_pack.build_pack(legal_pack_source, out_dir)
    assert error.value.filename == str(legal_pack_source / name)
    if prior_output:
        assert target.read_bytes() == before
        assert target.stat().st_mode & 0o777 == 0o640
    else:
        assert not out_dir.exists()


@pytest.mark.parametrize("name", ["README.md", "LICENSE", "NOTICE"])
@pytest.mark.parametrize("kind", ["directory", "unreadable"])
def test_build_pack_when_required_input_invalid_then_preserves_prior_archive(
    tmp_path, name, kind, legal_pack_source, pack,
):
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    target = out_dir / build_pack.PACK_NAME
    shutil.copy2(pack, target)
    target.chmod(0o640)
    before = target.read_bytes()
    path = legal_pack_source / name
    if kind == "directory":
        path.unlink()
        path.mkdir()
    else:
        path.chmod(0)
    try:
        expected = ValueError if kind == "directory" else PermissionError
        with pytest.raises(expected, match=name):
            build_pack.build_pack(legal_pack_source, out_dir)
        assert target.read_bytes() == before
        assert target.stat().st_mode & 0o777 == 0o640
    finally:
        if kind == "unreadable":
            path.chmod(0o644)


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
        check=False,
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
        check=False,
    )
    if build.returncode != 0:
        pytest.skip("uv could not build the wheel (no network or cache for build requirements)")
    (wheel,) = tmp_path.glob("*.whl")
    with zipfile.ZipFile(wheel) as zf:
        names = zf.namelist()
    assert any(n.startswith("fontlab_plugmix/") for n in names)
    assert not [n for n in names if n.startswith(("Extensions/", "Scripts/")) or n.endswith("plugin.json")]


def test_sdist_when_built_then_omits_operational_and_compiled_payload_but_keeps_sources(tmp_path):
    build = subprocess.run(
        ["uv", "build", "--sdist", "--out-dir", str(tmp_path), str(ROOT)],
        capture_output=True, text=True, env=os.environ.copy(), check=False,
    )
    assert build.returncode == 0, build.stdout + build.stderr
    (archive,) = tmp_path.glob("*.tar.gz")
    with tarfile.open(archive) as source:
        members = {member.name.split("/", 1)[1]: member for member in source.getmembers()
                   if "/" in member.name}
        assert not any(path == ".omc" or path.startswith(".omc/") for path in members)
        assert "install.vfpyc" not in members
        for path in (
            "src/fontlab_plugmix/__init__.py", "README.md", "LICENSE", "NOTICE",
            "install.vfpy", "initScript-snippet.py", "pyproject.toml", "test.sh",
            "Extensions/reporters/NodeCount.fontlabreporter/plugin.json",
            "Extensions/reporters/NodeCount.fontlabreporter/node_count.py",
            "Scripts/Plugmix/Show Reporters.py", "tests/test_pack_artifacts.py",
            "src_docs/md/installation.md", "docs/installation/index.html",
            "tests_docs/test_site.py",
        ):
            assert path in members, path
            assert source.extractfile(members[path]).read() == (ROOT / path).read_bytes(), path

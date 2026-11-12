# this_file: tests/test_install_bundles.py
"""The real install.vfpy puts all 50 reference bundles where FontLab's plugin core finds them (Issue 254)."""

import importlib.machinery
import importlib.util
import os
import shutil
from collections import Counter
from pathlib import Path

import pytest
from fontlabapp.plugins import registry

ROOT = Path(__file__).resolve().parents[1]
KINDS = {"reporters": 39, "filters": 5, "tools": 4, "palettes": 1, "general": 1}


def load(path):
    """Import install.vfpy under the name it expects when imported (its suffix has no default loader)."""
    loader = importlib.machinery.SourceFileLoader("fontlab_install", str(path))
    module = importlib.util.module_from_spec(importlib.util.spec_from_file_location("fontlab_install", str(path), loader=loader))
    loader.exec_module(module)
    return module


class Installed:
    """A copy of this repository's installable files, a temporary FontLab data folder and the real installer."""

    def __init__(self, base, monkeypatch, git=True):
        self.project = base / "plugmix"
        self.project.mkdir()
        for name in ("install.vfpy", "pyproject.toml"):
            shutil.copy2(str(ROOT / name), str(self.project / name))
        for name in ("Extensions", "Scripts"):
            shutil.copytree(str(ROOT / name), str(self.project / name), ignore=shutil.ignore_patterns("__pycache__"))
        if git:
            (self.project / ".git").mkdir()
        self.data = (base / "data").resolve()
        self.data.mkdir()
        self.mod = load(self.project / "install.vfpy")
        monkeypatch.setattr(self.mod, "data_dir", lambda: self.data)
        monkeypatch.setattr(self.mod, "find_uv", lambda: None)
        monkeypatch.setattr(self.mod, "missing", lambda requires: list(requires))

    def uninstall(self):
        self.mod.uninstall("com.fontlab.python-plugmix", self.data)


@pytest.fixture
def installed(tmp_path, monkeypatch):
    return Installed(tmp_path, monkeypatch)


def found(data):
    errors = []
    plugins = registry.discover(lambda *args: errors.append(args), data / "Extensions")
    return plugins, errors


def test_install_when_run_then_plugin_core_discovers_all_fifty_plugins(installed):
    installed.mod.main()
    plugins, errors = found(installed.data)
    assert errors == [] and len(plugins) == 50
    assert Counter(cls.kind for cls in plugins.values()) == {
        "reporter": 39, "filter": 5, "palette": 1, "tool": 4, "general": 1}
    for kind, count in KINDS.items():
        links = [p for p in (installed.data / "Extensions" / kind).iterdir()]
        assert len(links) == count and all(p.is_symlink() and os.path.isabs(os.readlink(str(p))) for p in links)


def test_install_when_run_then_links_point_at_this_checkout_and_scripts_are_copied(installed):
    installed.mod.main()
    link = installed.data / "Extensions" / "reporters" / "NodeCount.fontlabReporter"
    assert os.readlink(str(link)) == os.path.abspath(str(installed.project / "Extensions/reporters/NodeCount.fontlabReporter"))
    assert (installed.data / "Scripts" / "Plugmix" / "Show Reporters.py").is_file()


def test_install_when_app_checkout_is_not_beside_then_output_says_so_plainly(installed, capsys):
    installed.mod.main()
    out = capsys.readouterr().out
    assert "Dependency fontlab-fontlabapp is not installed and no checkout of it sits beside" in out
    assert "Missing dependencies" in out


def test_install_when_run_twice_then_same_links(installed):
    installed.mod.main()
    first = sorted(p.name for p in (installed.data / "Extensions" / "reporters").iterdir())
    installed.mod.main()
    assert first == sorted(p.name for p in (installed.data / "Extensions" / "reporters").iterdir())
    assert len(found(installed.data)[0]) == 50


def test_uninstall_when_run_then_all_fifty_links_go_and_sources_stay(installed):
    installed.mod.main()
    installed.uninstall()
    for kind in KINDS:
        folder = installed.data / "Extensions" / kind
        assert not folder.exists() or list(folder.iterdir()) == []
    assert found(installed.data)[0] == {}
    assert len(list((installed.project / "Extensions").rglob("plugin.json"))) == 50


def test_uninstall_when_user_replaced_a_link_then_their_folder_stays(installed):
    installed.mod.main()
    link = installed.data / "Extensions" / "filters" / "MoveOutlines.fontlabFilter"
    link.unlink()
    link.mkdir()
    (link / "mine.txt").write_text("keep", encoding="utf-8")
    installed.uninstall()
    assert (link / "mine.txt").read_text() == "keep"


def test_install_when_copied_from_a_non_git_folder_then_bundles_still_load(tmp_path, monkeypatch):
    plain = Installed(tmp_path, monkeypatch, git=False)
    plain.mod.main()
    plugins, errors = found(plain.data)
    assert errors == [] and len(plugins) == 50
    assert os.readlink(str(plain.data / "Extensions/tools" / sorted(os.listdir(str(plain.data / "Extensions/tools")))[0])).startswith(
        str(plain.data / "Extensions" / "com.fontlab.python-plugmix" / "bundles"))

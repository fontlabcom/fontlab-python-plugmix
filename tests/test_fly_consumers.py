# this_file: tests/test_fly_consumers.py
"""Public bundles keep canonical App identity through the Fly namespace."""

import ast
import logging
import os
import runpy
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_public_consumers_when_parsed_then_use_fly_without_direct_app_imports():
    files = [*(ROOT / "Extensions").rglob("*.py"), *(ROOT / "Scripts").rglob("*.py")]
    imports = []
    for path in files:
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.ImportFrom):
                assert not (node.module or "").startswith("fontlabapp"), path
                if (node.module or "").startswith("fly.ap"):
                    imports.append(node)
    assert len(files) == 51 and len(imports) == 121


@pytest.mark.parametrize("fails", [False, True])
def test_startup_when_run_then_calls_app_once_and_contains_failure(monkeypatch, capsys, fails):
    from fly.ap import plugins

    from fontlab_plugmix import boot as legacy_boot

    calls = []

    def install():
        calls.append("App")
        if fails:
            raise RuntimeError("startup fixture")

    monkeypatch.setattr(plugins, "install", install)
    monkeypatch.setattr(legacy_boot, "install", lambda: pytest.fail("legacy startup"))
    runpy.run_path(str(ROOT / "initScript-snippet.py"))
    assert calls == ["App"]
    assert capsys.readouterr().out == ("Plugmix startup: startup fixture\n" if fails else "")


def test_readme_reporter_when_discovered_then_uses_app_group_and_exact_base(monkeypatch, tmp_path):
    from fly.ap.plugins import Mark, Reporter, registry

    from fontlab_plugmix import Reporter as LegacyReporter

    snippet = (ROOT / "README.md").read_text().split("```python\n", 1)[1].split("```", 1)[0]
    example = tmp_path / "readme_reporter.py"
    example.write_text(snippet, encoding="utf-8")
    scope = runpy.run_path(str(example))
    origin = scope["Origin"]
    assert origin.__bases__ == (Reporter,)
    assert Reporter is not LegacyReporter
    assert isinstance(origin().compute(None)[0], Mark)
    groups = []

    def select(*, group):
        groups.append(group)
        return [SimpleNamespace(load=lambda: origin)]

    monkeypatch.setattr(registry.metadata, "entry_points", lambda: SimpleNamespace(select=select))
    assert registry.discover(extensions_dir=tmp_path)["origin"] is origin
    assert groups == ["fontlabapp.plugmix"]


def test_fly_when_selected_in_isolated_child_then_routes_exact_provider_sources():
    fly = Path(os.environ.get("PLUGMIX_FLY_SOURCE", ROOT.parent / "fontlab-fly")) / "src"
    app = Path(os.environ.get("PLUGMIX_FONTLABAPP_SOURCE", ROOT.parent / "fontlab-fontlabapp")) / "src"
    pens = Path(os.environ.get("PLUGMIX_PENS_SOURCE", ROOT.parent / "fontlab-python-pens")) / "src"
    code = """
import sys
from pathlib import Path
sys.path[:0] = sys.argv[1:4]
import fly
assert Path(fly.__file__).resolve() == Path(sys.argv[1], 'fly/__init__.py').resolve()
import fly.ap.plugins.reporter as alias
import fontlabapp.plugins.reporter as canonical
import fly.pens as pens
import fontlab_pens
assert alias is canonical and alias.Reporter is canonical.Reporter
assert pens is fontlab_pens
assert Path(canonical.__file__).resolve().is_relative_to(Path(sys.argv[2]).resolve())
assert Path(pens.__file__).resolve().is_relative_to(Path(sys.argv[3]).resolve())
assert not {'fontlab', 'PythonQt'} & sys.modules.keys()
"""
    result = subprocess.run([sys.executable, "-I", "-c", code, str(fly), str(app), str(pens)],
                            capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("debug", [False, True])
@pytest.mark.parametrize("fails", [False, True])
def test_startup_when_debug_configured_then_preserves_stdout_and_exception(
    monkeypatch, capsys, caplog, debug, fails
):
    from fly.ap import plugins

    failure = RuntimeError("startup debug fixture")

    def install():
        if fails:
            raise failure

    monkeypatch.setattr(plugins, "install", install)
    caplog.set_level(logging.DEBUG if debug else logging.WARNING, logger="<run_path>")
    scope = runpy.run_path(str(ROOT / "initScript-snippet.py"))
    assert scope["install"] is install
    captured = capsys.readouterr()
    assert captured.out == ("Plugmix startup: startup debug fixture\n" if fails else "")
    assert captured.err == ""
    records = [record for record in caplog.records if record.name == "<run_path>"]
    assert len(records) == int(debug and fails)
    if records:
        assert records[0].levelno == logging.DEBUG
        assert records[0].exc_info[0] is RuntimeError
        assert records[0].exc_info[1] is failure
        assert records[0].exc_info[2] is not None

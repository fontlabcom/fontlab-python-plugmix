# this_file: tests/test_install_bundles.py
"""install.vfpy hands the 50 reference bundles to fontlab-instamix (Issue 254).

fontlab-instamix links every bundle under the declared ``extensions`` folder into
FontLab's ``Extensions/<kind>/`` folders. These tests pin what it reads: the stub,
the install table and a bundle tree that FontLab's plugin core accepts.
"""

import re
import tomllib
from collections import Counter
from pathlib import Path

from fontlabapp.plugins import registry

ROOT = Path(__file__).resolve().parents[1]


def canonical_stub() -> bytes | None:
    """instamix's own stub bytes, from the package or a sibling checkout."""
    try:
        from fontlab_instamix import stub
    except ImportError:
        sibling = ROOT.parent / "fontlab-python-instamix" / "stub" / "install.vfpy"
        return sibling.read_bytes() if sibling.is_file() else None
    return stub.text().encode("utf-8")


KINDS = {"reporters": 39, "filters": 5, "tools": 4, "palettes": 1, "general": 1}
STUB_HEADER = b"#FLM: Install into FontLab with fontlab-instamix\n"
REVERSE_DNS = re.compile(r"^[a-z][a-z0-9-]*(\.[a-z0-9][a-z0-9-]*)+$")  # instamix manifest.ID_PATTERN


def table():
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def test_installer_when_read_then_is_instamix_stub():
    source = (ROOT / "install.vfpy").read_bytes()
    assert source.startswith(STUB_HEADER), "install.vfpy must be the instamix stub"
    assert b"bootstrap.install_project(__file__)" in source, "stub must hand off to instamix"
    assert b'getattr(extension, "preflight_plugin_migration", None)' in source, "stub must require safe managed bundle migration"
    assert b"def required_api():" in source and b"return required_api()" in source, "both reused and replaced providers must be ready"
    canonical = canonical_stub()
    if canonical is not None:
        assert source.replace(b"this_file: install.vfpy", b"this_file: stub/install.vfpy") == canonical, "install.vfpy must match instamix's canonical stub"
    assert not (ROOT / "install.vfpyc").exists(), "compiled legacy installer must stay deleted"


def test_install_table_when_parsed_then_declares_bundles_and_dependencies_without_cycle():
    project = table()
    install = project["tool"]["fontlab-install"]
    assert REVERSE_DNS.match(install["id"]) and install["id"] == "com.fontlab.python-plugmix"
    assert install["extensions"] == "Extensions" and install["packages"] == []
    assert project["project"]["dependencies"] == ["fontlab-fontlabapp>=1.2.31"]
    assert install["dependencies"] == ["fontlab-fontlabapp>=1.2.31", "fontlab-fly>=1.3.0"]


def test_extensions_when_discovered_in_place_then_plugin_core_finds_all_fifty():
    folder = ROOT / table()["tool"]["fontlab-install"]["extensions"]
    for kind, count in KINDS.items():
        bundles = [p for p in (folder / kind).iterdir() if p.is_dir() and not p.name.startswith(("_", "."))]
        assert len(bundles) == count, f"{kind}: {sorted(p.name for p in bundles)}"
    errors = []
    plugins = registry.discover(lambda *args: errors.append(args), folder)
    assert errors == [] and len(plugins) == 50
    assert Counter(cls.kind for cls in plugins.values()) == {
        "reporter": 39, "filter": 5, "palette": 1, "tool": 4, "general": 1}

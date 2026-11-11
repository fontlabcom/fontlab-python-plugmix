# this_file: tests/test_extension_manifest.py
"""The reference pack follows the public manifest and discovery contract."""

import json
from collections import Counter
from pathlib import Path

from fontlabapp.plugins import bundles, registry

ROOT = Path(__file__).resolve().parents[1]


def test_reference_pack_when_discovered_twice_then_all_five_kinds_keep_identity():
    rows = json.loads((ROOT / "tests/bundle-map.json").read_text())
    errors = []
    first = registry.discover(lambda *args: errors.append(args), ROOT / "Extensions")
    second = registry.discover(lambda *args: errors.append(args), ROOT / "Extensions")
    assert errors == []
    assert set(first) == {row["id"] for row in rows}
    assert len(first) == 50
    assert Counter(cls.kind for cls in first.values()) == {
        "reporter": 39, "filter": 5, "palette": 1, "tool": 4, "general": 1
    }
    for row in rows:
        path = ROOT / row["bundle"]
        manifest = bundles.manifest(path)
        cls = first[row["id"]]
        assert manifest["entry"] == row["module"] + ":" + row["class"]
        assert (manifest["id"], manifest["name"], manifest["kind"]) == (
            cls.name, cls.title, cls.kind
        )
        assert cls is second[row["id"]] is bundles.load_bundle(path)
        assert cls.__module__.startswith("_fontlab_extension_")
    assert sorted(str(path.relative_to(ROOT)) for path in (ROOT / "Extensions").rglob("plugin.json")) == sorted(
        row["bundle"] + "/plugin.json" for row in rows
    )

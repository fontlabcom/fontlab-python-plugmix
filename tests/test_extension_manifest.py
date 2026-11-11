# this_file: tests/test_extension_manifest.py
"""The reference pack follows the public manifest and discovery contract."""

import json
import subprocess
from collections import Counter
from pathlib import Path

import pytest
from fontlabapp.plugins import bundles, registry

ROOT = Path(__file__).resolve().parents[1]


def test_reference_pack_when_extensions_folder_missing_then_failure_names_the_pack():
    assert (ROOT / "Extensions").is_dir(), (
        "Extensions/ pack not found beside tests/. The pack ships as "
        "fontlab-python-plugmix-extensions.zip (tools/build_pack.py), not in the wheel; "
        "run these tests from a source checkout or sdist."
    )


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


# App release floors for the five filter bundles (Plugmix TODO "coordinate-writer release").
# App v1.2.9 is the first tag shipping ``fontlabapp.plugins`` (81978fa); its filter host is
# deletion-only. The coordinate writer (App 277a001) is in no release yet, so the four
# coordinate filters keep the 1.0.0 placeholder until the first tag containing it.
PLUGIN_CORE_COMMIT = "81978fa"
COORDINATE_WRITER_COMMIT = "277a001"
DELETION_ONLY_FLOOR = "1.2.9"
DELETION_ONLY_FILTERS = {"DeleteSmallPaths"}
COORDINATE_FILTERS = {"MoveOutlines", "RoundOutlineToGrid", "ScaleOutlines", "SlantOutlines"}
PLACEHOLDER_FLOOR = "1.0.0"
APP_CHECKOUT = ROOT.parent / "fontlab-fontlabapp"


def _version(text):
    return tuple(int(part) for part in text.split("."))


def _filter_floors():
    return {
        path.parent.name.removesuffix(".fontlabFilter"): json.loads(path.read_text())["min_app_version"]
        for path in (ROOT / "Extensions/filters").glob("*.fontlabFilter/plugin.json")
    }


def _tag_contains(tag, commit):
    result = subprocess.run(
        ["git", "-C", str(APP_CHECKOUT), "merge-base", "--is-ancestor", commit, "v" + tag],
        capture_output=True,
        check=False,
    )
    assert result.returncode in (0, 1), result.stderr.decode()
    return result.returncode == 0


def test_filter_floors_when_loaded_then_match_the_app_writer_they_need():
    floors = _filter_floors()
    assert set(floors) == DELETION_ONLY_FILTERS | COORDINATE_FILTERS
    for name in DELETION_ONLY_FILTERS:
        assert floors[name] == DELETION_ONLY_FLOOR, f"{name} needs the App plugin core first shipped in v1.2.9"
    for name in COORDINATE_FILTERS:
        floor = floors[name]
        assert floor == PLACEHOLDER_FLOOR or _version(floor) > _version(DELETION_ONLY_FLOOR), (
            f"{name} builds coordinate edits; v1.2.9 and older reject them"
        )
    todo = (ROOT / "TODO.md").read_text()
    if PLACEHOLDER_FLOOR in {floors[name] for name in COORDINATE_FILTERS}:
        assert "- [ ] Qualify the paired App coordinate-writer release" in todo


def test_filter_floors_when_app_tags_available_then_floor_tags_contain_the_needed_writer():
    if not (APP_CHECKOUT / ".git").exists():
        pytest.skip("sibling fontlab-fontlabapp checkout absent")
    floors = _filter_floors()
    assert _tag_contains(DELETION_ONLY_FLOOR, PLUGIN_CORE_COMMIT)
    assert not _tag_contains("1.2.8", PLUGIN_CORE_COMMIT)
    assert not _tag_contains(DELETION_ONLY_FLOOR, COORDINATE_WRITER_COMMIT)
    for name in COORDINATE_FILTERS - {n for n in COORDINATE_FILTERS if floors[n] == PLACEHOLDER_FLOOR}:
        assert _tag_contains(floors[name], COORDINATE_WRITER_COMMIT), name

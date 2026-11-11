# this_file: tests/conftest.py
"""Python-only snapshot fixtures for every built-in reporter."""

import json
import sys
from pathlib import Path
from types import ModuleType

import pytest

from fontlab_plugmix.snapshot import Anchor, Contour, GlyphSnapshot, Metrics, Node


@pytest.fixture
def glyph() -> GlyphSnapshot:
    """A rectangle with two selected on-curves and an external handle."""
    return GlyphSnapshot(
        (
            Contour(
                (
                    Node(0, 0, True, True),
                    Node(30, 120, False, False),
                    Node(100, 0, True, False),
                    Node(100, 100, True, True),
                    Node(0, 100, True, False),
                )
            ),
        ),
        (
            Anchor("top", 50, 110),
            Anchor("top_2", 50.5, 110),
            Anchor("top_3", 50.8, 110),
            Anchor("far", 100, 110),
        ),
        500,
        Metrics(800, -200, 500, 700, 10, 1000),
    )


def pytest_configure():
    """Expose actual bundle modules to the retained behavioral test imports."""
    from fontlabapp.plugins.bundles import load_bundle

    root = Path(__file__).resolve().parents[1]
    if not (root / "Extensions").is_dir():
        raise pytest.UsageError(
            "Extensions/ pack not found beside tests/. The pack ships as "
            "fontlab-python-plugmix-extensions.zip (tools/build_pack.py), not in the wheel; "
            "run these tests from a source checkout or sdist."
        )
    package = ModuleType("plugmix_examples")
    package.__path__ = []
    sys.modules[package.__name__] = package
    for row in json.loads((root / "tests/bundle-map.json").read_text()):
        cls = load_bundle(root / row["bundle"])
        module = sys.modules[cls.__module__]
        sys.modules[f"plugmix_examples.{row['module']}"] = module
        setattr(package, row["module"], module)

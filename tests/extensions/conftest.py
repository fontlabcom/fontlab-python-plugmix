# this_file: tests/extensions/conftest.py
"""Python-only snapshot fixtures for every built-in reporter."""

import pytest
from fontlabapp.plugins import snapshot
from fontlabapp.plugins.snapshot import Anchor, Contour, GlyphSnapshot, Metrics, Node


@pytest.fixture(autouse=True)
def _fresh_snapshot_cache():
    """Isolate the process-wide snapshot cache between tests."""
    snapshot._cache.clear()
    snapshot._reported.clear()
    yield
    snapshot._cache.clear()
    snapshot._reported.clear()


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

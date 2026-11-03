# this_file: tests/conftest.py
"""Python-only snapshot fixtures for every built-in reporter."""

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

# this_file: tests/extensions/test_plugmix_issue209_background.py
"""Pure checks for the background and component fill reporters."""

from dataclasses import replace

import pytest

from plugmix_examples.color_toner import ColorToner
from plugmix_examples.show_background import ShowBackground
from fontlabapp.plugins.snapshot import Component, Contour, Node


def square(x0, y0, x1, y1):
    pts = ((x0, y0), (x1, y0), (x1, y1), (x0, y1))
    return Contour(tuple(Node(x, y, True, False) for x, y in pts))


def inside(point, pts):
    """Odd-even point test, the rule Qt's drawPolygon uses by default."""
    x, y = point
    odd = False
    for (ax, ay), (bx, by) in zip(pts, pts[1:] + pts[:1], strict=True):
        if (ay > y) != (by > y) and x < ax + (y - ay) * (bx - ax) / (by - ay):
            odd = not odd
    return odd


def comp(*contours):
    return Component("b", (1, 0, 0, 1, 0, 0), tuple(contours))


# show background ---------------------------------------------------------


def test_show_background_when_outlines_then_one_pale_blue_polygon(glyph):
    data = replace(glyph, background=(square(0, 0, 100, 100), square(30, 30, 70, 70)))
    (mark,) = ShowBackground().compute(data)
    pts = list(mark.points)
    assert mark.kind == "polygon" and mark.fill == (164, 221, 237, 77)
    assert inside((10, 10), pts) and not inside((50, 50), pts), "counter stays open"
    assert ShowBackground.needs_background is True


@pytest.mark.parametrize("background", [None, (), (Contour(()),)])
def test_show_background_when_missing_or_empty_then_nothing(glyph, background):
    assert ShowBackground().compute(replace(glyph, background=background)) == []


# color toner -------------------------------------------------------------


def test_color_toner_when_components_then_one_black_polygon_each(glyph):
    data = replace(
        glyph,
        components=(
            comp(square(0, 0, 100, 100), square(30, 30, 70, 70)),
            comp(square(200, 0, 300, 100)),
        ),
    )
    first, second = ColorToner().compute(data)
    assert first.fill == second.fill == (0, 0, 0, 38)  # round(255 * 0.15)
    assert inside((10, 10), list(first.points))
    assert not inside((50, 50), list(first.points)), "counter stays open"
    assert inside((250, 50), list(second.points))
    assert ColorToner.needs_components is True


@pytest.mark.parametrize(
    ("darken", "alpha"),
    [(0.0, 0), (0.5, 128), (1.0, 255), (1.5, 128), (2.0, 255), (-1.0, 0), (-0.3, 0)],
)
def test_color_toner_when_darken_wraps_then_alpha_in_range(glyph, darken, alpha):
    toner = ColorToner()
    toner.darken = darken
    data = replace(glyph, components=(comp(square(0, 0, 10, 10)),))
    (mark,) = toner.compute(data)
    assert mark.fill[3] == alpha, f"darken {darken}"


def test_color_toner_when_no_or_empty_components_then_nothing(glyph):
    assert ColorToner().compute(replace(glyph, components=())) == []
    assert ColorToner().compute(replace(glyph, components=(comp(),))) == []

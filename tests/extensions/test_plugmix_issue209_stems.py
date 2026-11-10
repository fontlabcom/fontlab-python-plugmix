# this_file: tests/extensions/test_plugmix_issue209_stems.py
"""Pure checks for the Show Stems reporter."""

from dataclasses import replace
from math import radians, tan

import pytest

from plugmix_examples.show_stems import ShowStems
from fontlabapp.plugins.snapshot import Contour, Node

RING = (60, 60, 110)
INSIDE = (0, 191, 51)


def poly(*points):
    return Contour(tuple(Node(x, y, True, False) for x, y in points), True)


def rect(x0, y0, x1, y1):
    return poly((x0, y0), (x1, y0), (x1, y1), (x0, y1))


def run(glyph, *contours, slant=0, bounds=None):
    metrics = replace(glyph.metrics, italic_slant=slant)
    shape = replace(glyph, contours=contours, metrics=metrics, bounds=bounds)
    return ShowStems().compute(shape)


def of(marks, kind, color=None):
    return [m for m in marks if m.kind == kind and color in (None, m.color)]


def crossings(marks):
    return sorted(m.points[0][0] for m in of(marks, "ring", RING))


def test_show_stems_metadata():
    assert ShowStems.name == "show_stems" and ShowStems.title == "Show Stems"
    assert ShowStems.layer == "background" and ShowStems.needs_bounds is True


def test_show_stems_when_no_contours_or_nodes_then_empty(glyph):
    assert run(glyph) == []
    assert run(glyph, Contour(())) == []


def test_show_stems_when_o_shape_then_two_stems_and_counter_gap(glyph):
    marks = run(glyph, rect(0, 0, 300, 500), rect(80, 80, 220, 420))
    (base,) = of(marks, "line")
    assert base.points == ((0, 250), (500, 250))  # x_height 500 / 2, advance 500
    assert base.color == (170, 175, 200) and base.stroke_px == 1
    assert crossings(marks) == [0, 80, 220, 300]
    rings = of(marks, "ring", RING)
    assert all(m.diameter_px == 5 and m.points[0][1] == 250 for m in rings)
    texts = of(marks, "text")
    assert [t.text for t in texts] == ["80", "140", "80"]
    assert all(t.color == (0, 77, 204) for t in texts)
    assert [t.points[0] for t in texts] == [(40, 265), (150, 265), (260, 265)]
    inside = of(marks, "ring", INSIDE)
    assert [m.points[0] for m in inside] == [(40, 250), (260, 250)]  # not the gap
    assert all(m.diameter_px == 6 for m in inside)


def test_show_stems_when_vertex_exactly_at_y_then_counted_once(glyph):
    marks = run(glyph, poly((150, 0), (300, 250), (150, 500), (0, 250)))
    assert crossings(marks) == [0, 300]
    assert [t.text for t in of(marks, "text")] == ["300"]


def test_show_stems_when_horizontal_edge_at_y_then_not_double_counted(glyph):
    marks = run(glyph, rect(0, 250, 300, 500))
    assert crossings(marks) == [0, 300]
    assert [t.text for t in of(marks, "text")] == ["300"]


def test_show_stems_when_tall_glyph_then_uses_cap_height(glyph):
    (base,) = of(run(glyph, rect(0, 0, 300, 650)), "line")
    assert base.points[0][1] == 350  # cap_height 700 / 2
    (low,) = of(run(glyph, rect(0, 0, 300, 599)), "line")
    assert low.points[0][1] == 250


def test_show_stems_when_bounds_given_then_threshold_uses_bounds_top(glyph):
    shape = rect(0, 0, 300, 500)  # node max 500 alone would pick x-height
    (tall,) = of(run(glyph, shape, bounds=(0, 0, 300, 600)), "line")
    (short,) = of(run(glyph, shape, bounds=(0, 0, 300, 599)), "line")
    assert tall.points[0][1] == 350 and short.points[0][1] == 250


def test_show_stems_when_italic_then_base_line_shifted_but_not_crossings(glyph):
    sx = tan(radians(10)) * (350 - 250)
    marks = run(glyph, rect(0, 0, 300, 650), slant=10)
    (base,) = of(marks, "line")
    assert base.points[0] == pytest.approx((sx, 350))
    assert base.points[1] == pytest.approx((500 + sx, 350))
    assert crossings(marks) == [0, 300]


def test_show_stems_when_x_height_line_then_italic_shift_is_zero(glyph):
    (base,) = of(run(glyph, rect(0, 0, 300, 500), slant=10), "line")
    assert base.points == ((0, 250), (500, 250))


def test_show_stems_when_curve_then_flattened_crossings(glyph):
    curve = Contour(
        (
            Node(0, 0, True, False),
            Node(0, 200, False, False),
            Node(100, 300, False, False),
            Node(100, 500, True, False),
        ),
        True,
    )
    assert crossings(run(glyph, curve)) == pytest.approx([50, 50], abs=1)


def test_show_stems_when_degenerate_geometry_then_only_base_line(glyph):
    flat = Contour((Node(0, 250, True, False), Node(100, 250, True, False)), False)
    dot = Contour((Node(5, 5, True, False),), False)
    marks = run(glyph, flat, dot)
    assert len(marks) == 1 and marks[0].kind == "line"

# this_file: tests/extensions/test_plugmix_issue209_rotated.py
"""Pure checks for the Show Rotated reporter."""

from dataclasses import replace

import pytest
from fontlabapp.plugins.snapshot import Contour, Node
from plugmix_examples.show_rotated import ShowRotated

GREEN = (0, 128, 77)


def poly(*points, closed=True):
    return Contour(tuple(Node(x, y, True, False) for x, y in points), closed)


def run(glyph, *contours, bounds=None):
    return ShowRotated().compute(replace(glyph, contours=contours, bounds=bounds))


def of(marks, kind):
    return [m for m in marks if m.kind == kind]


def test_show_rotated_metadata():
    assert ShowRotated.name == "show_rotated" and ShowRotated.title == "Show Rotated"
    assert ShowRotated.layer == "background" and ShowRotated.needs_bounds is True


def test_show_rotated_when_no_contours_or_nodes_then_empty(glyph):
    assert run(glyph) == []
    assert run(glyph, Contour(())) == []


def test_show_rotated_when_bounds_given_then_rotates_about_bounds_centre(glyph):
    marks = run(glyph, poly((0, 0), (100, 0), (100, 50)), bounds=(0, 0, 200, 100))
    lines = of(marks, "polyline")
    assert [m.points for m in lines] == [
        ((200, 100), (100, 100)),
        ((100, 100), (100, 50)),
        ((100, 50), (200, 100)),
    ]
    assert all(m.color == GREEN and m.stroke_px == 1 for m in lines)
    rings = of(marks, "ring")
    assert [m.points for m in rings] == [((200, 100),), ((100, 100),), ((100, 50),)]
    assert all(m.color == GREEN and m.diameter_px == 6 for m in rings)


def test_show_rotated_when_bounds_none_then_centre_is_node_hull(glyph):
    # off-curves at x=300 widen the hull to 0..300, so cx = 150, cy = 50
    curve = Contour(
        (
            Node(0, 0, True, False),
            Node(300, 0, False, False),
            Node(300, 100, False, False),
            Node(0, 100, True, False),
        ),
        False,
    )
    marks = run(glyph, curve)
    (line,) = of(marks, "polyline")
    assert len(line.points) == 17
    assert line.points[0] == pytest.approx((300, 100))
    assert line.points[16] == pytest.approx((300, 0))
    assert line.points[8] == pytest.approx((300 - 225, 50))  # t=.5 -> (225, 50)
    assert [m.points for m in of(marks, "ring")] == [((300, 100),), ((300, 0),)]
    cross = of(marks, "line")
    assert cross[0].points == ((150 - 20, 50), (150 + 20, 50))


def test_show_rotated_when_centre_cross_then_two_lines_scaled_by_upm(glyph):
    marks = run(glyph, poly((0, 0), (100, 100)), bounds=(0, 0, 100, 100))
    horizontal, vertical = of(marks, "line")
    assert horizontal.points == ((30, 50), (70, 50))  # upm 1000 * 0.02 = 20
    assert vertical.points == ((50, 30), (50, 70))
    assert horizontal.color == vertical.color == GREEN
    assert of(marks, "polygon") == []


def test_show_rotated_when_open_line_then_single_two_point_polyline(glyph):
    marks = run(glyph, poly((0, 0), (40, 0), closed=False), bounds=(0, 0, 40, 10))
    (line,) = of(marks, "polyline")
    assert line.points == ((40, 10), (0, 10))
    assert len(of(marks, "ring")) == 2


def test_show_rotated_when_single_node_then_ring_and_centre_cross_only(glyph):
    marks = run(glyph, poly((10, 20), closed=False))
    assert [m.kind for m in marks] == ["ring", "line", "line"]
    assert marks[0].points == ((10, 20),)  # rotating about itself

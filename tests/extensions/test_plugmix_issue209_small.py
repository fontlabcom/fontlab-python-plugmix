# this_file: tests/extensions/test_plugmix_issue209_small.py
"""Pure checks for the Node Count, All Angles and Smart Plumblines reporters."""

from dataclasses import replace
from math import radians, tan

import pytest
from fontlabapp.plugins.snapshot import Contour, Node
from plugmix_examples.all_angles import AllAngles
from plugmix_examples.node_count import NodeCount
from plugmix_examples.smart_plumblines import SmartPlumblines


def line(*points, closed=False):
    return Contour(tuple(Node(x, y, True, False) for x, y in points), closed)


def cubic(h1=(0, 50), h2=(50, 100)):
    return Contour(
        (
            Node(0, 0, True, False),
            Node(*h1, False, False),
            Node(*h2, False, False),
            Node(100, 100, True, False),
        ),
        False,
    )


def test_node_count_when_contours_then_counts_on_and_off_curves(glyph):
    marks = NodeCount().compute(glyph)
    assert len(marks) == 1 and marks[0].kind == "text"
    assert marks[0].text == "· 5" and marks[0].color == (102, 0, 153)
    assert marks[0].points == ((520, 1),)
    assert NodeCount.layer == "background"


def test_node_count_when_no_nodes_then_empty(glyph):
    assert NodeCount().compute(replace(glyph, contours=())) == []
    assert NodeCount().compute(replace(glyph, contours=(Contour(()),))) == []


def test_node_count_when_several_contours_then_sums(glyph):
    two = replace(glyph, contours=glyph.contours + (line((0, 0), (1, 1)),))
    assert NodeCount().compute(two)[0].text == "· 7"


def labels(glyph, *contours, handles=False):
    reporter = AllAngles()
    reporter.show_handles = handles
    return reporter.compute(replace(glyph, contours=contours))


def test_all_angles_when_axis_lines_then_bearing_from_vertical(glyph):
    horizontal, vertical = labels(glyph, line((0, 0), (100, 0), (100, 50)))
    assert horizontal.text == "90.0°" and vertical.text == "0.0°"
    assert horizontal.color == (56, 217, 137)


def test_all_angles_when_near_vertical_left_lean_then_wraps_to_zero(glyph):
    (mark,) = labels(glyph, line((0, 0), (-1e-6, 100)))
    assert mark.text == "0.0°"


def test_all_angles_when_label_then_offset_along_unit_perpendicular(glyph):
    (mark,) = labels(glyph, line((0, 0), (100, 0)))
    # (-dy, dx)/len = (0, 1); 0.02 * 1000 upm = 20
    assert mark.points[0] == pytest.approx((50, 20))


def test_all_angles_when_leaning_then_right_is_below_90_left_above(glyph):
    t = tan(radians(12))
    (right,) = labels(glyph, line((0, 0), (100 * t, 100)))
    (left,) = labels(glyph, line((0, 0), (-100 * t, 100)))
    (down,) = labels(glyph, line((0, 100), (0, 0)))
    assert right.text == "12.0°" and left.text == "168.0°"
    assert down.text == "0.0°"


def test_all_angles_when_zero_length_or_curve_then_no_label(glyph):
    assert labels(glyph, line((5, 5), (5, 5))) == []
    assert labels(glyph, cubic()) == []


def test_all_angles_when_show_handles_then_labels_both_handles(glyph):
    marks = labels(glyph, cubic(), handles=True)
    assert [m.text for m in marks] == ["0.0°", "90.0°"]
    assert all(m.color == (217, 56, 107) for m in marks)
    assert AllAngles.show_handles is False


def test_all_angles_when_zero_length_handle_then_skipped(glyph):
    marks = labels(glyph, cubic(h1=(0, 0)), handles=True)
    assert [m.text for m in marks] == ["90.0°"]


def test_smart_plumblines_when_upright_then_cross_per_contour(glyph):
    square = line((0, 0), (100, 0), (100, 100), (0, 100), closed=True)
    plain = replace(
        glyph, contours=(square,), metrics=replace(glyph.metrics, italic_slant=0)
    )
    marks = SmartPlumblines().compute(plain)
    assert len(marks) == 2 and all(m.stroke_px == 0.75 for m in marks)
    assert all(m.color == (200, 60, 90) for m in marks)
    assert marks[0].points == ((0, 50), (500, 50))
    assert marks[1].points == ((50, -200), (50, 800))
    assert SmartPlumblines.layer == "background"


def test_smart_plumblines_when_italic_then_vertical_line_slants(glyph):
    t = tan(radians(10))
    marks = SmartPlumblines().compute(
        replace(glyph, contours=(line((0, 0), (100, 100)),))
    )
    (x0, y0), (x1, y1) = marks[1].points
    # mid = 250: u values are 250t and 100 + 150t
    cu = (250 * t + 100 + 150 * t) / 2
    assert (y0, y1) == (-200, 800)
    assert x0 == pytest.approx(cu + t * (-200 - 250))
    assert x1 == pytest.approx(cu + t * (800 - 250))


def test_smart_plumblines_when_selection_then_extra_selected_cross(glyph):
    marks = SmartPlumblines().compute(glyph)
    assert len(marks) == 4
    assert all(m.color == (0, 150, 145) for m in marks[2:])
    assert marks[2].points == ((0, 50), (500, 50))  # selected nodes y 0 and 100


def test_smart_plumblines_when_empty_or_unselected_then_no_extra(glyph):
    assert SmartPlumblines().compute(replace(glyph, contours=())) == []
    assert SmartPlumblines().compute(replace(glyph, contours=(Contour(()),))) == []
    unselected = replace(glyph, contours=(line((0, 0), (10, 10)),))
    assert len(SmartPlumblines().compute(unselected)) == 2

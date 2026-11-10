# this_file: tests/extensions/test_plugmix_issue209_masters.py
"""Pure checks for the master-blend and mouse-measuring reporters."""

from dataclasses import replace

import pytest

from plugmix_examples.show_interpolation import ShowInterpolation
from plugmix_examples.stem_thickness import StemThickness
from fontlabapp.plugins.snapshot import Contour, MasterOutline, Node, ViewState


def box(x0, y0, x1, y1, closed=True, selected=False):
    pts = ((x0, y0), (x1, y0), (x1, y1), (x0, y1))
    return Contour(tuple(Node(x, y, True, selected) for x, y in pts), closed)


def master(name, *contours, compatible=True):
    return MasterOutline(name, contours, (), 500, compatible)


# show interpolation ------------------------------------------------------


def test_show_interpolation_when_masters_differ_then_one_halfway_fill_each(glyph):
    data = replace(
        glyph,
        contours=(box(0, 0, 100, 100, selected=True),),
        masters=(
            master("Same", box(0, 0, 100, 100)),
            master("Bold", box(0, 0, 200, 300)),
            master("Odd", box(0, 0, 9, 9), compatible=False),
            master("Wide", box(0, 0, 300, 100)),
        ),
    )
    marks = ShowInterpolation().compute(data)
    assert [m.kind for m in marks] == ["polygon", "polygon"], (
        "same-coordinate and incompatible masters are skipped"
    )
    assert all(m.fill == (102, 0, 77, 64) for m in marks)
    assert marks[0].points[:4] == ((0, 0), (150, 0), (150, 200), (0, 200))
    assert marks[1].points[:4] == ((0, 0), (200, 0), (200, 100), (0, 100))


def test_show_interpolation_when_factor_changed_then_blend_moves(glyph):
    data = replace(
        glyph,
        contours=(box(0, 0, 100, 100),),
        masters=(master("B", box(0, 0, 200, 100)),),
    )
    reporter = ShowInterpolation()
    reporter.factor = 0.25
    assert reporter.compute(data)[0].points[1] == (125, 0)


def test_show_interpolation_when_counter_then_one_polygon_keeps_it_open(glyph):
    data = replace(
        glyph,
        contours=(box(0, 0, 100, 100), box(25, 25, 75, 75)),
        masters=(master("B", box(0, 0, 200, 100), box(50, 25, 150, 75)),),
    )
    (mark,) = ShowInterpolation().compute(data)
    assert len(mark.points) == 11, "two closed loops plus the bridge back"
    assert (112.5, 25) in mark.points and (150, 0) in mark.points


@pytest.mark.parametrize(
    "fields",
    [
        {},
        {"masters": ()},
        {"contours": (), "masters": (master("B"),)},
        {"masters": (master("B", box(0, 0, 9, 9), compatible=False),)},
    ],
)
def test_show_interpolation_when_no_usable_master_then_nothing(glyph, fields):
    assert ShowInterpolation().compute(replace(glyph, **fields)) == []


def test_show_interpolation_declares_background_and_masters():
    assert ShowInterpolation.layer == "background" and ShowInterpolation.needs_masters


# stem thickness ----------------------------------------------------------


def stem(glyph, mouse, *contours):
    view = ViewState(1.0, mouse=mouse)
    return replace(glyph, contours=contours or (box(0, 0, 100, 700),), view=view)


def test_stem_thickness_when_mouse_near_left_edge_then_measures_across(glyph):
    marks = StemThickness().compute(stem(glyph, (-5, 300)))
    assert [m.kind for m in marks] == ["line", "text"]
    line, text = marks
    assert line.points == ((0, 300), (100, 300))
    assert line.color == text.color == (166, 161, 240)
    assert text.text == "100"
    assert text.points == ((56, 306),), "midpoint offset by text_offset"


def test_stem_thickness_when_inside_near_right_edge_then_same_stem(glyph):
    line, text = StemThickness().compute(stem(glyph, (97, 50)))
    assert line.points == ((100, 50), (0, 50))
    assert text.text == "100"


def test_stem_thickness_when_two_contours_then_nearer_crossing_wins(glyph):
    data = stem(glyph, (-1, 50), box(0, 0, 100, 700), box(30, 0, 60, 700))
    line, text = StemThickness().compute(data)
    assert line.points[1] == (30, 50) and text.text == "30"


def test_stem_thickness_when_curved_then_rounded_length(glyph):
    curve = Contour(
        (
            Node(0, 0, True, False),
            Node(50, 0, True, False),
            Node(90, 30, False, False),
            Node(90, 70, False, False),
            Node(50, 100, True, False),
            Node(0, 100, True, False),
        )
    )
    line, text = StemThickness().compute(stem(glyph, (-3, 50), curve))
    assert line.points == ((0, 50), (80, 50)), "bulge apex at t = 0.5"
    assert text.text == "80"


def test_stem_thickness_when_fractional_then_rounded(glyph):
    _, text = StemThickness().compute(stem(glyph, (-5, 9), box(0, 0, 100.4, 700)))
    assert text.text == "100"


def test_stem_thickness_when_no_mouse_view_outline_or_hit_then_nothing(glyph):
    reporter = StemThickness()
    line = Contour((Node(0, 0, True, False), Node(0, 9, True, False)), closed=False)
    assert reporter.compute(stem(glyph, None)) == [], "no mouse"
    assert reporter.compute(replace(stem(glyph, (0, 0)), view=None)) == [], "no view"
    assert reporter.compute(replace(stem(glyph, (5, 5)), contours=())) == []
    assert reporter.compute(stem(glyph, (-1, 5), line)) == [], "single edge"
    assert reporter.compute(stem(glyph, (0, 5), box(0, 0, 0.5, 10))) == [], (
        "crossing within min_length; top and bottom are parallel"
    )


def test_stem_thickness_when_degenerate_edges_then_they_are_skipped(glyph):
    dup = Contour(
        tuple(
            Node(x, y, True, False)
            for x, y in ((0, 0), (0, 0), (100, 0), (100, 700), (0, 700))
        )
    )
    _, text = StemThickness().compute(stem(glyph, (-5, 300), dup))
    assert text.text == "100"


def test_stem_thickness_declares_foreground_and_mouse():
    assert StemThickness.layer == "foreground" and StemThickness.needs_mouse


@pytest.mark.parametrize("mouse", [(0, 0), (-10, -10), (100, 700), (110, 710)])
def test_stem_thickness_when_at_or_outside_a_corner_then_nothing(glyph, mouse):
    # The ray from a corner runs along the adjacent side; crossings on that
    # side are on the outline, not across the stem, so nothing is drawn.
    assert StemThickness().compute(stem(glyph, mouse)) == []


def test_stem_thickness_when_mouse_exactly_on_outline_then_measures(glyph):
    line, text = StemThickness().compute(stem(glyph, (0, 300)))
    assert line.points == ((0, 300), (100, 300)) and text.text == "100"


def test_stem_thickness_when_contour_points_all_equal_then_nothing(glyph):
    dot = Contour(tuple(Node(5, 5, True, False) for _ in range(4)))
    assert StemThickness().compute(stem(glyph, (0, 0), dot)) == []


def test_show_interpolation_when_open_contour_then_one_closed_fill(glyph):
    data = replace(
        glyph,
        contours=(box(0, 0, 100, 100, closed=False),),
        masters=(master("B", box(0, 0, 200, 100, closed=False)),),
    )
    (mark,) = ShowInterpolation().compute(data)
    assert mark.points == ((0, 0), (150, 0), (150, 100), (0, 100), (0, 0))

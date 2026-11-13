# this_file: tests/extensions/test_plugmix_issue209_identity.py
"""Pure checks for geometry fill helpers and the identity-driven reporters."""

from dataclasses import replace
from math import radians, tan

import pytest
from fontlabapp.glyphs.identity import Identity
from fontlabapp.plugins.geometry import fill_points, flatten, shear
from fontlabapp.plugins.snapshot import (
    Anchor,
    Component,
    Contour,
    Node,
    ViewState,
)
from plugmix_examples.blindfold import Blindfold
from plugmix_examples.export_status import ExportStatus
from plugmix_examples.glyphs_in_label_color import GlyphsInLabelColor
from plugmix_examples.label_color import LabelColor
from plugmix_examples.rekha import Rekha
from plugmix_examples.show_character import ShowCharacter

RED = (200, 30, 10)


def square(x0, y0, x1, y1, closed=True):
    pts = ((x0, y0), (x1, y0), (x1, y1), (x0, y1))
    return Contour(tuple(Node(x, y, True, False) for x, y in pts), closed)


def ident(**kw):
    base = {"name": "a", "unicodes": (0x61,), "mark": 1, "mark_rgb": RED, "exported": True}
    return Identity(**{**base, **kw})


def snap(glyph, identity=None, **kw):
    return replace(glyph, identity=identity, **kw)


def inside(point, pts):
    """Odd-even point test, the rule Qt's drawPolygon uses by default."""
    x, y = point
    odd = False
    for (ax, ay), (bx, by) in zip(pts, pts[1:] + pts[:1], strict=True):
        if (ay > y) != (by > y) and x < ax + (y - ay) * (bx - ax) / (by - ay):
            odd = not odd
    return odd


# geometry ---------------------------------------------------------------


def test_flatten_when_closed_square_then_four_points_no_repeat():
    assert flatten(square(0, 0, 10, 10)) == ((0, 0), (10, 0), (10, 10), (0, 10))


def test_flatten_when_open_then_end_point_kept():
    assert flatten(square(0, 0, 10, 10, closed=False))[-1] == (0, 10)


def test_flatten_when_curve_then_steps_points_per_segment():
    curve = Contour(
        (
            Node(0, 0, True, False),
            Node(0, 10, False, False),
            Node(10, 10, False, False),
            Node(10, 0, True, False),
        ),
        closed=False,
    )
    pts = flatten(curve, steps=4)
    assert len(pts) == 5 and pts[0] == (0, 0) and pts[-1] == (10, 0)


def test_flatten_when_too_few_nodes_then_empty():
    assert flatten(Contour(())) == ()
    assert flatten(Contour((Node(0, 0, True, False),))) == ()


def test_fill_points_when_ring_then_counter_stays_open():
    pts = fill_points((square(0, 0, 100, 100), square(30, 30, 70, 70)))
    assert inside((10, 10), list(pts)) and not inside((50, 50), list(pts))


def test_fill_points_when_three_contours_then_no_bridge_artifact():
    pts = list(
        fill_points(
            (square(0, 0, 10, 10), square(100, 0, 110, 10), square(0, 100, 10, 110))
        )
    )
    assert inside((5, 5), pts) and inside((105, 5), pts) and inside((5, 105), pts)
    assert not inside((50, 30), pts) and not inside((30, 60), pts)


def test_fill_points_when_nothing_fillable_then_empty():
    assert fill_points(()) == ()
    assert fill_points((Contour((Node(0, 0, True, False),) * 2),)) == ()


def test_shear_when_positive_slant_then_top_leans_right():
    (low, high) = shear(((0, 0), (0, 200)), 10, 100)
    assert low[0] == pytest.approx(-100 * tan(radians(10)))
    assert high[0] == pytest.approx(100 * tan(radians(10)))
    assert shear(((5, 7),), 0, 3) == ((5, 7),)


# blindfold ---------------------------------------------------------------


def test_blindfold_when_default_then_two_black_blocks(glyph):
    lower, upper = Blindfold().compute(glyph)  # asc 800 desc -200 xh 500 cap 700
    assert lower.kind == upper.kind == "polygon"
    assert lower.fill == upper.fill == (0, 0, 0, 255)
    assert lower.points == (
        (-10000, -270),
        (10500, -270),
        (10500, 0),
        (-10000, 0),
    )
    assert [p[1] for p in upper.points[::2]] == [500, 870]


def test_blindfold_when_cap_height_band_then_upper_starts_at_cap(glyph):
    class Cap(Blindfold):
        band = "cap_height"

    assert Cap().compute(glyph)[1].points[0][1] == 700


def test_blindfold_metadata():
    assert Blindfold.name == "blindfold" and Blindfold.layer == "foreground"


# label colour ------------------------------------------------------------


@pytest.mark.parametrize("identity", [None, ident(mark=0, mark_rgb=None)])
def test_label_color_when_no_colour_then_empty(glyph, identity):
    assert LabelColor().compute(snap(glyph, identity)) == []


def test_label_color_when_default_then_bar_under_descender(glyph):
    flat = replace(glyph, metrics=replace(glyph.metrics, italic_slant=0))
    (mark,) = LabelColor().compute(snap(flat, ident()))
    assert mark.fill == (*RED, 230)
    assert mark.points == ((0, -240), (500, -240), (500, -200), (0, -200))


def test_label_color_when_body_then_half_alpha_and_full_height(glyph):
    class Body(LabelColor):
        placement = "body"

    flat = replace(glyph, metrics=replace(glyph.metrics, italic_slant=0))
    (mark,) = Body().compute(snap(flat, ident()))
    assert mark.fill[3] == 128 and {p[1] for p in mark.points} == {-200, 800}


def test_label_color_when_baseline_then_bar_under_baseline(glyph):
    class Base(LabelColor):
        placement = "baseline"

    (mark,) = Base().compute(snap(glyph, ident()))
    assert {p[1] for p in mark.points} == {-40, 0}


def test_label_color_when_slanted_then_sheared_about_half_x_height(glyph):
    slanted = replace(glyph, metrics=replace(glyph.metrics, italic_slant=10))
    (mark,) = LabelColor().compute(snap(slanted, ident()))
    k = tan(radians(10))
    assert mark.points[0][0] == pytest.approx(k * (-240 - 250))
    assert mark.points[3][0] == pytest.approx(k * (-200 - 250))


# glyphs in label colour --------------------------------------------------


@pytest.mark.parametrize("identity", [None, ident(mark=0, mark_rgb=None)])
def test_glyphs_in_label_color_when_no_colour_then_empty(glyph, identity):
    assert GlyphsInLabelColor().compute(snap(glyph, identity)) == []


def test_glyphs_in_label_color_when_components_then_one_polygon(glyph):
    comp = Component("b", (1, 0, 0, 1, 0, 0), (square(200, 0, 300, 100),))
    data = snap(
        glyph,
        ident(),
        contours=(square(0, 0, 100, 100), square(30, 30, 70, 70)),
        components=(comp,),
    )
    (mark,) = GlyphsInLabelColor().compute(data)
    pts = list(mark.points)
    assert mark.kind == "polygon" and mark.fill == (*RED, 171)
    assert (
        inside((10, 10), pts) and not inside((50, 50), pts) and inside((250, 50), pts)
    )
    assert GlyphsInLabelColor.needs_components is True


def test_glyphs_in_label_color_when_no_outline_then_empty(glyph):
    assert GlyphsInLabelColor().compute(snap(glyph, ident(), contours=())) == []


# show character ----------------------------------------------------------


def test_show_character_when_glyph_low_then_sits_at_ascender(glyph):
    (mark,) = ShowCharacter().compute(snap(glyph, ident(), bounds=(0, 0, 100, 100)))
    assert mark.kind == "text" and mark.text == "a" and mark.text_px == 100
    assert mark.points == ((0, 800),) and mark.color == (26, 102, 204)


def test_show_character_when_glyph_tall_then_above_bounds(glyph):
    (mark,) = ShowCharacter().compute(snap(glyph, ident(), bounds=(0, 0, 100, 900)))
    assert mark.points == ((0, 950),)


def test_show_character_when_bounds_missing_then_ascender(glyph):
    (mark,) = ShowCharacter().compute(snap(glyph, ident()))
    assert mark.points == ((0, 800),)


def test_show_character_when_zoomed_out_then_hidden_else_shown(glyph):
    far = snap(glyph, ident(), view=ViewState(0.19))
    near = snap(glyph, ident(), view=ViewState(0.2))
    assert ShowCharacter().compute(far) == []
    assert len(ShowCharacter().compute(near)) == 1


@pytest.mark.parametrize(
    "identity",
    [None, ident(unicodes=()), ident(unicodes=(0x0A,)), ident(unicodes=(0xD800,))]
    + [ident(unicodes=(0x110000,))],
)
def test_show_character_when_no_printable_unicode_then_empty(glyph, identity):
    assert ShowCharacter().compute(snap(glyph, identity)) == []


# rekha -------------------------------------------------------------------


def test_rekha_when_devanagari_letter_then_bar_over_advance(glyph):
    (mark,) = Rekha().compute(snap(glyph, ident(unicodes=(0x0915,)), anchors=()))
    assert mark.kind == "polygon" and mark.fill == (0, 0, 0, 64)
    assert mark.points == ((-20, 700), (520, 700), (520, 800), (-20, 800))


@pytest.mark.parametrize("code", [0x0995, 0x0A15])
def test_rekha_when_bengali_or_gurmukhi_letter_then_bar(glyph, code):
    assert len(Rekha().compute(snap(glyph, ident(unicodes=(code,)), anchors=()))) == 1


@pytest.mark.parametrize(
    "identity",
    [
        None,
        ident(unicodes=()),
        ident(unicodes=(0x61,)),  # Latin
        ident(unicodes=(0x0966,)),  # Devanagari digit, not a letter
        ident(unicodes=(0x093E,)),  # Devanagari vowel sign, not a letter
    ],
)
def test_rekha_when_not_an_indic_letter_then_empty(glyph, identity):
    assert Rekha().compute(snap(glyph, identity)) == []


def test_rekha_when_anchors_then_start_moves_and_stop_adds_bar(glyph):
    anchors = (Anchor("rekha", 80, 700), Anchor("rekha_stop", 60, 700))
    start, stop = Rekha().compute(
        snap(glyph, ident(unicodes=(0x0915,)), anchors=anchors)
    )
    assert start.points[0][0] == 80 and start.points[1][0] == 520
    assert stop.points[0][0] == -20 and stop.points[1][0] == 60


def test_rekha_when_stop_left_of_start_then_empty_bar_dropped(glyph):
    anchors = (Anchor("rekha_stop", -50, 700),)
    marks = Rekha().compute(snap(glyph, ident(unicodes=(0x0915,)), anchors=anchors))
    assert len(marks) == 1


# export status -----------------------------------------------------------


@pytest.mark.parametrize("identity", [None, ident(exported=True)])
def test_export_status_when_exported_or_unknown_then_empty(glyph, identity):
    assert ExportStatus().compute(snap(glyph, identity)) == []


def test_export_status_when_not_exported_then_two_diagonals(glyph):
    flat = replace(glyph, metrics=replace(glyph.metrics, italic_slant=0))
    marks = ExportStatus().compute(snap(flat, ident(exported=False)))
    assert [m.kind for m in marks] == ["line", "line"]
    assert marks[0].points == ((0, -200), (500, 800))
    assert marks[1].points == ((0, 800), (500, -200))
    assert all(m.color == (255, 0, 0) for m in marks)


def test_export_status_when_slanted_then_sheared(glyph):
    marks = ExportStatus().compute(snap(glyph, ident(exported=False)))
    k = tan(radians(10))
    assert marks[0].points[0][0] == pytest.approx(k * (-200 - 250))


@pytest.mark.parametrize(("code", "bars"), [(0xA8F2, 1), (0xA8E0, 0)])
def test_rekha_when_devanagari_extended_then_letter_bar_mark_none(glyph, code, bars):
    marks = Rekha().compute(snap(glyph, ident(unicodes=(code,)), anchors=()))
    assert len(marks) == bars, f"U+{code:04X}"

# this_file: tests/test_more_plugins.py
"""Pure geometry and mark checks for Task 7 reporters."""

from dataclasses import replace
from math import radians, tan

import pytest

from fontlab_plugmix.geometry import length, neighbours, point_at, segments
from fontlab_plugmix.plugins.anchor_cloud import AnchorCloud
from fontlab_plugmix.plugins.angled_handles import AngledHandles
from fontlab_plugmix.plugins.crosshair import Crosshair
from fontlab_plugmix.plugins.glyph_focus import GlyphFocus
from fontlab_plugmix.plugins.imprecise_italic_angle import ImpreciseItalicAngle
from fontlab_plugmix.plugins.nodes_close_to_zones import NodesCloseToZones
from fontlab_plugmix.plugins.only_selected_handles import OnlySelectedHandles
from fontlab_plugmix.plugins.rsb_line import RSBLine
from fontlab_plugmix.plugins.segment_length import SegmentLength
from fontlab_plugmix.plugins.smooth_node_angles import SmoothNodeAngles
from fontlab_plugmix.plugins.tops_and_bottoms import TopsAndBottoms
from fontlab_plugmix.plugins.unitizer import Unitizer
from fontlab_plugmix.snapshot import Contour, Node, Zone


def test_angled_handles_ignores_italic_and_axis_aligned_handles(glyph):
    contour = Contour(
        (
            Node(0, 0, True, False),
            Node(10, 100, False, False),
            Node(100, 100, True, False),
            Node(80, 120, False, False),
        )
    )
    custom = replace(
        glyph,
        contours=(contour,),
        metrics=replace(glyph.metrics, italic_slant=5.7105931375),
    )
    assert [mark.points[0] for mark in AngledHandles().compute(custom)] == [(80, 120)]


def test_angled_handles_obeys_right_slant_and_rejects_left_mirror_and_zero(glyph):
    x = tan(radians(12)) * 100
    contour = Contour(
        (
            Node(0, 0, True, False),
            Node(x, 100, False, False),
            Node(100, 100, True, False),
        ),
        False,
    )
    right = replace(
        glyph, contours=(contour,), metrics=replace(glyph.metrics, italic_slant=12)
    )
    assert AngledHandles().compute(right) == []
    left = replace(right, metrics=replace(glyph.metrics, italic_slant=-12))
    assert [mark.points[0] for mark in AngledHandles().compute(left)] == [(x, 100)]
    zero = replace(
        contour, nodes=(contour.nodes[0], Node(0, 0, False, False), contour.nodes[2])
    )
    assert AngledHandles().compute(replace(right, contours=(zero,))) == []


def test_crosshair_extends_two_guides_per_selected_node(glyph):
    marks = Crosshair().compute(glyph)
    assert len(marks) == 4
    assert marks[0].points == ((-1_000_000, 0), (1_000_000, 0))
    assert marks[1].stroke_px == 0.75


def test_tops_and_bottoms_marks_all_tied_oncurve_extrema(glyph):
    marks = TopsAndBottoms().compute(glyph)
    assert len(marks) == 8
    assert [mark.text for mark in marks if mark.kind == "text"] == [
        "0",
        "0",
        "100",
        "100",
    ]
    assert TopsAndBottoms().compute(replace(glyph, contours=())) == []


def test_segment_length_measures_line_and_cubic_and_selection(glyph):
    contour = Contour(
        (
            Node(0, 0, True, False),
            Node(30, 40, True, False),
            Node(50, 80, False, False),
            Node(80, 80, False, False),
            Node(100, 0, True, False),
        ),
        False,
    )
    plain = replace(glyph, contours=(contour,))
    marks = SegmentLength().compute(plain)
    assert len(marks) == 2 and marks[0].text == "50.0"
    assert float(marks[1].text) > 70
    assert point_at(segments(contour)[1], 0.5)[1] > 40
    one_end = replace(
        contour, nodes=(*contour.nodes[:-1], replace(contour.nodes[-1], selected=True))
    )
    assert SegmentLength().compute(replace(glyph, contours=(one_end,))) == []
    both_ends = replace(
        one_end,
        nodes=(
            one_end.nodes[0],
            replace(one_end.nodes[1], selected=True),
            *one_end.nodes[2:],
        ),
    )
    assert len(SegmentLength().compute(replace(glyph, contours=(both_ends,)))) == 1
    isolated = Contour((Node(0, 0, True, True),))
    assert SegmentLength().compute(replace(glyph, contours=(contour, isolated))) == []


def test_geometry_handles_closed_and_quadratic_segments():
    contour = Contour(
        (
            Node(0, 0, True, False),
            Node(50, 100, False, False),
            Node(100, 0, True, False),
        )
    )
    rows = segments(contour)
    assert len(rows) == 2
    assert point_at(rows[0], 0.5) == (50, 50)
    assert length(rows[0]) > 100
    assert length(rows[1]) == 100
    assert segments(Contour((Node(0, 0, False, False),))) == ()
    unsupported = Contour(
        (
            Node(0, 0, True, False),
            *(Node(x, 20, False, False) for x in (20, 40, 60)),
            Node(100, 0, True, False),
        ),
        False,
    )
    assert segments(unsupported) == (), "three off-curves are intentionally unsupported"
    open_path = replace(contour, closed=False)
    assert neighbours(open_path, 0)[0] is None
    assert neighbours(open_path, 2)[1] is None
    assert neighbours(contour, 0)[0] is contour.nodes[-1]


def test_only_selected_handles_emphasises_selection_without_hiding_native(glyph):
    marks = OnlySelectedHandles().compute(glyph)
    assert [mark.kind for mark in marks] == ["line", "ring"]
    assert marks[0].points == ((0, 0), (30, 120))
    handle_selected = replace(
        glyph.contours[0],
        nodes=(
            replace(glyph.contours[0].nodes[0], selected=False),
            replace(glyph.contours[0].nodes[1], selected=True),
            *glyph.contours[0].nodes[2:],
        ),
    )
    assert (
        len(OnlySelectedHandles().compute(replace(glyph, contours=(handle_selected,))))
        == 2
    )
    assert OnlySelectedHandles().compute(replace(glyph, contours=())) == []


def test_anchor_cloud_labels_current_layer_anchors(glyph):
    marks = AnchorCloud().compute(glyph)
    assert len(marks) == 8
    assert [mark.text for mark in marks if mark.kind == "text"] == [
        "top",
        "top_2",
        "top_3",
        "far",
    ]


def test_rsb_line_labels_both_sidebearings(glyph):
    marks = RSBLine().compute(replace(glyph, bounds=(10, -20, 125, 700)))
    assert marks[0].points == ((500, -200), (500, 800))
    assert [mark.text for mark in marks[1:]] == ["RSB 375", "LSB 10"]
    assert RSBLine().compute(glyph)[1].text == "RSB 400"
    assert RSBLine().compute(replace(glyph, contours=())) == []


def test_unitizer_divides_upm_into_18_units_and_caps_line_count(glyph):
    small = replace(glyph, advance=150)
    assert [mark.points[0][0] for mark in Unitizer().compute(small)] == pytest.approx(
        [1000 / 18, 2000 / 18]
    )
    assert len(Unitizer().compute(replace(glyph, advance=1_000_000_000))) == 2_000
    plugin = Unitizer()
    plugin.units_per_em = 20
    assert [mark.points[0][0] for mark in plugin.compute(small)] == [50, 100, 150]
    plugin.units_per_em = 0
    assert plugin.compute(glyph) == []


def test_glyph_focus_leaves_advance_and_metric_box_clear(glyph):
    plugin = GlyphFocus()
    marks = plugin.compute(glyph)
    assert plugin.layer == "foreground"
    assert len(marks) == 4
    assert all(
        mark.kind == "polygon" and mark.fill == (40, 40, 40, 70) for mark in marks
    )
    assert marks[0].points == (
        (-1_000_000, 800),
        (1_000_000, 800),
        (1_000_000, 1_000_000),
        (-1_000_000, 1_000_000),
    )
    assert marks[2].points == (
        (-1_000_000, -200),
        (0, -200),
        (0, 800),
        (-1_000_000, 800),
    )


def test_nodes_close_to_zones_checks_edges_and_excludes_exact_hits(glyph):
    metrics = replace(glyph.metrics, zones=(Zone("cap", 700, 712),))
    contour = Contour(
        (
            Node(20, 710, True, False),
            Node(30, 700, True, False),
            Node(40, 720, False, False),
        ),
        False,
    )
    marks = NodesCloseToZones().compute(
        replace(glyph, contours=(contour,), metrics=metrics)
    )
    assert [mark.points[0] for mark in marks] == [(20, 710)]


def test_nodes_close_to_zones_without_zones_uses_metrics(glyph):
    contour = Contour((Node(30, 697, True, False), Node(40, 501, True, False)), False)
    marks = NodesCloseToZones().compute(replace(glyph, contours=(contour,)))
    assert [mark.points[0] for mark in marks] == [(30, 697), (40, 501)]
    assert NodesCloseToZones().compute(replace(glyph, contours=())) == []


def test_imprecise_italic_angle_marks_near_vertical_lines(glyph):
    contour = Contour(
        (Node(0, 0, True, False), Node(1, 100, True, False), Node(1, 200, True, False)),
        False,
    )
    snapshot = replace(
        glyph, contours=(contour,), metrics=replace(glyph.metrics, italic_slant=0)
    )
    marks = ImpreciseItalicAngle().compute(snapshot)
    assert len(marks) == 1 and marks[0].points == ((0, 0), (1, 100))
    slanted = Contour((Node(0, 0, True, False), Node(19.44, 100, True, False)), False)
    italic = replace(
        glyph, contours=(slanted,), metrics=replace(glyph.metrics, italic_slant=10)
    )
    assert len(ImpreciseItalicAngle().compute(italic)) == 1
    exact = replace(
        slanted, nodes=(slanted.nodes[0], Node(17.632698, 100, True, False))
    )
    assert ImpreciseItalicAngle().compute(replace(italic, contours=(exact,))) == []


def test_imprecise_angle_matches_right_slant_but_not_left_mirror(glyph):
    x = tan(radians(13)) * 100
    contour = Contour((Node(0, 0, True, False), Node(x, 100, True, False)), False)
    right = replace(
        glyph, contours=(contour,), metrics=replace(glyph.metrics, italic_slant=12)
    )
    assert len(ImpreciseItalicAngle().compute(right)) == 1
    left = replace(right, metrics=replace(glyph.metrics, italic_slant=-12))
    assert ImpreciseItalicAngle().compute(left) == []


def test_smooth_node_angles_shows_kink_and_proportion(glyph):
    contour = Contour(
        (
            Node(0, 0, True, False),
            Node(40, 0, False, False),
            Node(100, 0, True, False, True),
            Node(160, 2, False, False),
            Node(200, 0, True, False),
        )
    )
    marks = SmoothNodeAngles().compute(replace(glyph, contours=(contour,)))
    assert len(marks) == 1
    assert marks[0].text.startswith("1.9° · 1.00")
    flat = replace(
        contour,
        nodes=(
            *contour.nodes[:2],
            replace(contour.nodes[2], smooth=False),
            *contour.nodes[3:],
        ),
    )
    assert SmoothNodeAngles().compute(replace(glyph, contours=(flat,))) == []
    zero = replace(
        contour,
        nodes=(
            *contour.nodes[:1],
            replace(contour.nodes[1], x=100),
            *contour.nodes[2:],
        ),
    )
    assert SmoothNodeAngles().compute(replace(glyph, contours=(zero,))) == []

# this_file: tests/extensions/test_plugmix_plugins.py
"""Behavioural checks for all built-in compute methods."""

from dataclasses import replace

import pytest
from fontlabapp.plugins.snapshot import Anchor, Contour, Node
from plugmix_examples.center_lines import CenterLines
from plugmix_examples.duplicate_anchors import DuplicateAnchors
from plugmix_examples.node_indexes import NodeIndexes
from plugmix_examples.offcurve_outside_bounds import OffcurveOutsideBounds
from plugmix_examples.selected_coordinates import SelectedCoordinates
from plugmix_examples.two_point_distance import TwoPointDistance
from plugmix_examples.vertical_metrics import VerticalMetrics


def test_existing_reporters_handle_empty_contours(glyph):
    empty = replace(glyph, contours=())
    for plugin in (
        NodeIndexes(),
        SelectedCoordinates(),
        TwoPointDistance(),
        OffcurveOutsideBounds(),
    ):
        assert plugin.compute(empty) == []
    assert len(CenterLines().compute(empty)) == 3
    assert len(VerticalMetrics().compute(empty)) == 10


def test_duplicate_anchors_counts_all_unordered_pairs(glyph):
    marks = DuplicateAnchors().compute(glyph)
    assert len(marks) == 6, "three close pairs need two rings each"
    assert [m.color for m in marks[:2]] == [(255, 0, 0), (255, 255, 0)]
    far = replace(glyph, anchors=(Anchor("a", 0, 0), Anchor("b", 1, 0)))
    assert DuplicateAnchors().compute(far) == [], "one-unit separation is excluded"
    DuplicateAnchors.set_handle_size(12)
    try:
        assert DuplicateAnchors().compute(glyph)[0].diameter_px == 24
        with pytest.raises(ValueError, match="Handle size"):
            DuplicateAnchors.set_handle_size(7)
    finally:
        DuplicateAnchors.set_handle_size(8)


def test_node_indexes_label_all_nodes_with_full_contour_index(glyph):
    marks = NodeIndexes().compute(glyph)
    assert [m.text for m in marks] == ["0", "1", "2", "3", "4"]


def test_selected_coordinates_show_selected_nodes(glyph):
    marks = SelectedCoordinates().compute(glyph)
    assert [m.text for m in marks] == ["0, 0", "100, 100"]
    extra = replace(glyph, contours=(Contour((Node(-1, 2.5, False, True),)),))
    assert SelectedCoordinates().compute(extra)[0].text == "-1, 2.5"


def test_two_point_distance_requires_exactly_two_nodes(glyph):
    marks = TwoPointDistance().compute(glyph)
    assert marks[0].kind == "line"
    assert marks[1].text == "141.4 · 45.0°"
    none = replace(glyph, contours=())
    three = replace(glyph, contours=(Contour((Node(0, 0, True, True),) * 3),))
    assert TwoPointDistance().compute(none) == []
    assert TwoPointDistance().compute(three) == []


def test_offcurve_outside_bounds_marks_only_external_handles(glyph):
    marks = OffcurveOutsideBounds().compute(glyph)
    assert [m.points[0] for m in marks] == [(30, 120)]
    no_extrema = replace(glyph, contours=(Contour((Node(2, 2, False, False),)),))
    assert OffcurveOutsideBounds().compute(no_extrema) == []


def test_center_lines_use_advance_and_half_heights(glyph):
    marks = CenterLines().compute(glyph)
    assert marks[0].points == ((250, -200), (250, 800))
    assert [m.points[0][1] for m in marks[1:]] == [250, 350]


def test_vertical_metrics_label_all_five_lines(glyph):
    marks = VerticalMetrics().compute(glyph)
    assert len(marks) == 10
    assert [m.text for m in marks if m.kind == "text"] == [
        "Ascender 800",
        "Descender -200",
        "x-height 500",
        "Cap height 700",
        "Baseline 0",
    ]

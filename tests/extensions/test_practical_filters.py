# this_file: tests/extensions/test_practical_filters.py
"""Real manifest-loaded geometry filters preserve the host's native topology."""

from dataclasses import replace
from pathlib import Path

import pytest
from fontlabapp.plugins.bundles import load_bundle
from fontlabapp.plugins.snapshot import Component, Contour, Node

ROOT = Path(__file__).resolve().parents[2] / "Extensions" / "filters"
BUNDLES = ("RoundOutlineToGrid", "MoveOutlines", "ScaleOutlines", "SlantOutlines")


def plugin(name):
    return load_bundle(ROOT / f"{name}.fontlabfilter")()


@pytest.mark.parametrize("name", BUNDLES)
def test_empty_integral_default_and_component_only_are_noops(name, glyph):
    instance = plugin(name)
    component = Component("a", (1, 0, 0, 1, 20, 30), glyph.contours)
    for contours in ((), (Contour(()),), glyph.contours):
        source = replace(glyph, contours=contours, components=(component,))
        edit = instance.compute(source, {})
        assert edit.contours is None
        assert edit.anchors is None and edit.advance is None
        assert source.components == (component,)


@pytest.mark.parametrize("name,values,expected", [
    ("RoundOutlineToGrid", {"grid": 2}, (0, 4)),
    ("MoveOutlines", {"dx": 4, "dy": -3}, (3, 0)),
    ("ScaleOutlines", {"x_percent": 200, "y_percent": 50,
                       "pivot_x": 1, "pivot_y": 1}, (-3, 2)),
    ("SlantOutlines", {"angle": 45, "pivot_y": 1}, (1, 3)),
])
def test_maps_open_quadratic_cubic_and_all_offcurve_without_reconstruction(
    name, values, expected, glyph
):
    # Snapshot does not encode cubic versus quadratic: preserve the control runs.
    nodes = tuple(Node(-1, 3, on, selected, smooth) for on, selected, smooth in (
        (True, True, True), (False, False, False), (False, True, False),
        (True, False, True), (False, False, False), (True, True, False)))
    contours = (Contour(nodes, False), Contour(nodes, True),
                Contour(nodes[1:3], True), Contour(()))
    component = Component("base", (1, 0, 0, 1, 0, 0), contours)
    source = replace(glyph, contours=contours, components=(component,))
    edit = plugin(name).compute(source, values)
    assert edit.anchors is None and edit.advance is None
    assert len(edit.contours) == len(contours)
    for before, after in zip(contours, edit.contours, strict=True):
        assert before.closed == after.closed
        assert len(before.nodes) == len(after.nodes)
        for old, new in zip(before.nodes, after.nodes, strict=True):
            assert (new.x, new.y) == pytest.approx(expected)
            assert replace(new, x=old.x, y=old.y) == old
    assert source.contours == contours and source.components == (component,)


def test_grid_half_steps_round_toward_positive_infinity(glyph):
    source = replace(glyph, contours=(Contour(tuple(
        Node(value, value, True, False) for value in (-2.5, -1.5, -.5, .5, 1.5, 2.5)
    )),))
    result = plugin("RoundOutlineToGrid").compute(source, {})
    assert [n.x for n in result.contours[0].nodes] == [-2, -1, 0, 1, 2, 3]
    assert plugin("RoundOutlineToGrid").compute(
        replace(source, contours=result.contours), {}).contours is None


@pytest.mark.parametrize("name", BUNDLES)
def test_rejects_unknown_nonfinite_and_wrong_type_parameters(name, glyph):
    instance = plugin(name)
    with pytest.raises(ValueError, match="Unknown"):
        instance.compute(glyph, {"typo": 1})
    for param in instance.params:
        for value in (float("inf"), float("nan"), True, "1", 10**1000):
            with pytest.raises(ValueError):
                instance.compute(glyph, {param.key: value})


@pytest.mark.parametrize("name,values", [
    ("RoundOutlineToGrid", {"grid": 0}),
    ("RoundOutlineToGrid", {"grid": -1}),
    ("ScaleOutlines", {"x_percent": 0}),
    ("ScaleOutlines", {"y_percent": -1}),
    ("SlantOutlines", {"angle": 86}),
    ("SlantOutlines", {"angle": -86}),
])
def test_rejects_singular_or_out_of_range_parameters(name, values, glyph):
    with pytest.raises(ValueError):
        plugin(name).compute(glyph, values)


@pytest.mark.parametrize("name", BUNDLES)
@pytest.mark.parametrize("x,y", [(float("nan"), 0), (0, float("inf"))])
def test_rejects_nonfinite_source_coordinates(name, x, y, glyph):
    source = replace(glyph, contours=(Contour((Node(x, y, True, False),)),))
    with pytest.raises(ValueError, match="finite"):
        plugin(name).compute(source, {})


@pytest.mark.parametrize("name,values,x,y", [
    ("RoundOutlineToGrid", {"grid": .000001}, 1e308, 0),
    ("RoundOutlineToGrid", {"grid": 1e308}, 1.7e308, 0),
    ("MoveOutlines", {"dx": 1e308}, 1e308, 0),
    ("ScaleOutlines", {"x_percent": 1000}, 1e308, 0),
    ("SlantOutlines", {"angle": 80}, 0, 1e308),
])
def test_rejects_coordinate_overflow(name, values, x, y, glyph):
    source = replace(glyph, contours=(Contour((Node(x, y, True, False),)),))
    with pytest.raises(ValueError, match="overflow"):
        plugin(name).compute(source, values)


@pytest.mark.parametrize("name,values", [
    ("ScaleOutlines", {"pivot_x": -1e308, "pivot_y": -1e308}),
    ("SlantOutlines", {"pivot_y": -1e308}),
])
def test_identity_transform_remains_exact_with_remote_pivot(name, values, glyph):
    source = replace(glyph, contours=(Contour((
        Node(1e308, 1e308, True, False), Node(.1, .1, True, False)
    )),))
    assert plugin(name).compute(source, values).contours is None

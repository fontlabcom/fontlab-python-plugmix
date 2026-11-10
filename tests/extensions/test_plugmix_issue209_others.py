# this_file: tests/extensions/test_plugmix_issue209_others.py
"""Pure checks for the other-glyph, kerning-group and neighbour reporters."""

from dataclasses import replace
from types import MappingProxyType

import pytest

from fontlabapp.glyphs.identity import Identity
from plugmix_examples.global_glyph import GlobalGlyph
from plugmix_examples.kern_indicator import KernIndicator
from plugmix_examples.kerning_group_reference import KerningGroupReference
from plugmix_examples.siblings import Siblings
from fontlabapp.plugins.snapshot import (
    Contour,
    KerningGroups,
    Neighbours,
    Node,
    ViewState,
)


def square(x0, y0, x1, y1, closed=True):
    pts = ((x0, y0), (x1, y0), (x1, y1), (x0, y1))
    return Contour(tuple(Node(x, y, True, False) for x, y in pts), closed)


def named(glyph, name, **fields):
    identity = Identity(name, (), 0, None, True)
    return replace(glyph, identity=identity, **fields)


def others(**by_name):
    return MappingProxyType(by_name)


# show global glyph -------------------------------------------------------


def test_global_glyph_when_closed_and_open_then_orange_and_blue_with_faint_fill(glyph):
    line = Contour((Node(0, 0, True, False), Node(50, 0, True, False)), closed=False)
    open_box = square(0, 0, 10, 10, closed=False)
    data = named(
        glyph,
        "A",
        others=others(_global=(square(0, 0, 100, 100), open_box, line)),
    )
    marks = GlobalGlyph().compute(data)
    fills = [m for m in marks if m.kind == "polygon"]
    lines = [m for m in marks if m.kind == "polyline"]
    assert [m.fill for m in fills] == [(255, 179, 51, 26), (0, 0, 255, 26)]
    assert [(m.color, m.stroke_px) for m in lines] == [
        ((255, 179, 51), 1.0),
        ((0, 0, 255), 1.0),
        ((0, 0, 255), 1.0),
    ]
    assert lines[0].points[0] == lines[0].points[-1], "closed outline is closed"
    assert lines[1].points[0] != lines[1].points[-1], "open outline stays open"


def test_global_glyph_when_active_glyph_is_global_then_nothing_and_nothing_asked(glyph):
    data = named(glyph, "_global", others=others(_global=(square(0, 0, 9, 9),)))
    assert GlobalGlyph().compute(data) == []
    assert GlobalGlyph().requested_glyphs(data.identity) == ()
    assert GlobalGlyph().requested_glyphs(replace(data.identity, name="A")) == (
        "_global",
    )


def test_global_glyph_when_data_missing_then_nothing(glyph):
    assert GlobalGlyph().compute(glyph) == [], "no identity"
    assert GlobalGlyph().compute(named(glyph, "A")) == [], "no _global glyph"
    assert GlobalGlyph().compute(named(glyph, "A", others=others(_global=()))) == []


# show siblings -----------------------------------------------------------


@pytest.mark.parametrize(
    ("name", "asked", "alpha"),
    [
        ("o", ("c", "e"), 34),
        ("b", ("p",), 51),
        ("q", ("d", "u"), 34),
        ("a", ("h", "l", "n", "r"), 20),
    ],
)
def test_siblings_when_in_group_then_asks_others_and_fills_by_group_size(
    glyph, name, asked, alpha
):
    plugin = Siblings()
    identity = Identity(name, (), 0, None, True)
    assert plugin.requested_glyphs(identity) == asked
    data = named(
        glyph, name, others=others(**{n: (square(0, 0, 9, 9),) for n in asked})
    )
    marks = plugin.compute(data)
    assert len(marks) == len(asked)
    assert {m.fill for m in marks} == {(38, 102, 64, alpha)}


def test_siblings_when_not_in_group_or_none_present_then_nothing(glyph):
    plugin = Siblings()
    assert plugin.requested_glyphs(Identity("Z", (), 0, None, True)) == ()
    assert plugin.compute(named(glyph, "Z")) == []
    assert plugin.compute(glyph) == [], "no identity"
    assert (
        plugin.compute(named(glyph, "o", others=others(c=(square(0, 0, 9, 9),)))) != []
    )
    assert plugin.compute(named(glyph, "o")) == []


# show kerning group reference --------------------------------------------


def groups(left="L", right="R"):
    members = {"L": ("A", "B", "C"), "R": ("D", "A")}
    return KerningGroups(left, right, MappingProxyType(members))


def test_kerning_group_reference_when_groups_then_requests_both_sides_interleaved(
    glyph,
):
    plugin = KerningGroupReference()
    identity = Identity("A", (), 0, None, True)
    assert plugin.requested_glyphs(identity, groups()) == ("B", "D", "C")
    assert plugin.requested_glyphs(identity) == (), "no groups, no members"
    assert KerningGroupReference.needs_kerning is True


def test_kerning_group_reference_when_class_over_cap_then_both_sides_still_asked(
    monkeypatch,
):
    left = tuple(f"l{i}" for i in range(40))
    right = tuple(f"r{i}" for i in range(40))
    both = KerningGroups("L", "R", MappingProxyType({"L": left, "R": right}))

    class Asked(KerningGroupReference):
        pass

    plugin = Asked()
    identity = Identity("A", (), 0, None, True)
    names = plugin._requested(identity, lambda error: None, both)
    assert len(names) == 32
    assert names[:4] == ("l0", "r0", "l1", "r1")
    assert sum(n.startswith("r") for n in names) == 16, "the cap keeps both sides"


def test_kerning_group_reference_when_members_then_overlap_one_spot_per_side(glyph):
    big = (square(0, 0, 100, 500),)
    data = named(
        glyph,
        "A",
        kerning_groups=groups(),
        others=others(B=big, C=big, D=big),
    )
    left_b, left_c, right_d = KerningGroupReference().compute(data)
    xs = lambda m: [p[0] for p in m.points]
    ys = lambda m: [p[1] for p in m.points]
    assert left_b.points == left_c.points, "left members overlap"
    assert max(xs(left_b)) == -150 and min(xs(left_b)) == -170
    assert min(xs(right_d)) == 500 + 150 and max(xs(right_d)) == 670
    assert min(ys(left_b)) == 250 and max(ys(left_b)) == 250 + 100, (
        "baseline at half x-height, scaled 0.2"
    )
    assert left_b.fill == (0, 128, 128, round(255 * 0.8 / 3)), "class L has 3 members"
    assert right_d.fill == (0, 128, 128, round(255 * 0.8 / 2)), "class R has 2 members"


def test_kerning_group_reference_when_crowded_then_alpha_floors_at_004(glyph):
    members = tuple(f"m{i}" for i in range(40))
    crowd = KerningGroups("L", None, MappingProxyType({"L": members}))
    data = named(
        glyph,
        "A",
        kerning_groups=crowd,
        others=others(m0=(square(0, 0, 10, 10),)),
    )
    (mark,) = KerningGroupReference().compute(data)
    assert mark.fill[3] == round(255 * 0.04)


def test_kerning_group_reference_when_missing_data_then_nothing(glyph):
    plugin = KerningGroupReference()
    assert plugin.compute(glyph) == [], "no identity"
    assert plugin.compute(named(glyph, "A")) == [], "no groups"
    none = KerningGroups(None, None, MappingProxyType({}))
    assert plugin.compute(named(glyph, "A", kerning_groups=none)) == []
    assert plugin.compute(named(glyph, "A", kerning_groups=groups())) == [], (
        "no outlines"
    )


# kern indicator ----------------------------------------------------------


def seen(glyph, prev, nxt, scale=0.5):
    return replace(glyph, view=ViewState(scale, neighbours=Neighbours(prev, nxt)))


def test_kern_indicator_when_values_then_coloured_text_at_junctions(glyph):
    marks = KernIndicator().compute(seen(glyph, ("T", -40.0), ("V", 12.5)))
    assert [(m.text, m.color, m.points) for m in marks] == [
        ("-40", (0, 122, 255), ((0, 750),)),
        ("12.5", (255, 149, 0), ((500, 750),)),
    ]


def test_kern_indicator_when_division_noise_then_whole_or_two_decimals(glyph):
    marks = KernIndicator().compute(
        seen(glyph, ("T", -2.9999999999999996), ("V", 1 / 3))
    )
    assert [m.text for m in marks] == ["-3", "0.33"], "no float noise printed"


@pytest.mark.parametrize(
    ("value", "label"),
    [
        (0.004, "0.004"),
        (-0.004, "-0.004"),
        (0.0049, "0.0049"),
        (-0.0049, "-0.0049"),
        (1e-7, "1e-07"),
        (-1e-7, "-1e-07"),
        (1e-6, "1e-06"),
        (-1e-6, "-1e-06"),
    ],
)
def test_kern_indicator_when_tiny_nonzero_then_nonzero_label(glyph, value, label):
    marks = KernIndicator().compute(seen(glyph, ("T", value), ("V", value)))
    color = (255, 149, 0) if value > 0 else (0, 122, 255)
    assert [(m.text, m.color, m.points) for m in marks] == [
        (label, color, ((0, 750),)),
        (label, color, ((500, 750),)),
    ]


def test_kern_indicator_when_zero_missing_or_nonfinite_then_that_side_skipped(glyph):
    plugin = KernIndicator()
    assert plugin.compute(seen(glyph, ("T", 0.0), None)) == []
    assert plugin.compute(seen(glyph, ("T", -0.0), None)) == []
    nan = plugin.compute(seen(glyph, ("T", float("nan")), ("V", 7)))
    assert [(m.text, m.points) for m in nan] == [("7", ((500, 750),))]
    assert [m.text for m in plugin.compute(seen(glyph, None, ("V", 7)))] == ["7"]


@pytest.mark.parametrize("scale", [0.029, 0.91, 5])
def test_kern_indicator_when_zoom_outside_range_then_hidden(glyph, scale):
    assert KernIndicator().compute(seen(glyph, ("T", -40), None, scale)) == []


def test_kern_indicator_when_zoom_at_limits_then_shown(glyph):
    for scale in (0.03, 0.9):
        assert KernIndicator().compute(seen(glyph, ("T", -40), None, scale)) != []


def test_kern_indicator_when_no_view_or_neighbours_then_nothing(glyph):
    assert KernIndicator().compute(glyph) == []
    assert KernIndicator().compute(replace(glyph, view=ViewState(0.5))) == []
    assert KernIndicator.needs_neighbours is True

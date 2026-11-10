# this_file: tests/extensions/test_plugmix_issue209_speed_punk.py
"""Pure checks for the Speed Punk curvature-comb reporter."""

from dataclasses import replace
from math import hypot

import pytest

from plugmix_examples.speed_punk import SpeedPunk, _ramp
from fontlabapp.plugins.snapshot import Contour, Node

K = 0.5523 * 100


def on(x, y):
    return Node(x, y, True, False)


def off(x, y):
    return Node(x, y, False, False)


def run(glyph, *contours):
    return SpeedPunk().compute(replace(glyph, contours=contours))


def circle():
    """Clockwise (y up) circle of radius 100 from four cubic segments."""
    return Contour(
        (
            on(0, 100), off(K, 100), off(100, K),
            on(100, 0), off(100, -K), off(K, -100),
            on(0, -100), off(-K, -100), off(-100, -K),
            on(-100, 0), off(-100, K), off(-K, 100),
        ),
        True,
    )  # fmt: skip


def bend():
    """Open S-ish cubic with strongly varying curvature."""
    return Contour((on(0, 0), off(100, 0), off(100, 10), on(0, 100)), False)


def test_speed_punk_metadata():
    assert SpeedPunk.name == "speed_punk" and SpeedPunk.title == "Speed Punk"
    assert SpeedPunk.layer == "background"
    assert (SpeedPunk.gain, SpeedPunk.total_steps, SpeedPunk.alpha) == (0.68, 400, 178)


def test_speed_punk_when_no_cubics_then_empty(glyph):
    assert run(glyph) == []
    assert run(glyph, Contour(())) == []
    assert run(glyph, Contour((on(0, 0), on(100, 0)), False)) == []


def test_speed_punk_when_straight_cubic_then_empty(glyph):
    line = Contour((on(0, 0), off(10, 0), off(20, 0), on(30, 0)), False)
    assert run(glyph, line) == []


def test_speed_punk_when_clockwise_circle_then_comb_lies_outside(glyph):
    marks = run(glyph, circle())
    assert len(marks) == 400  # 4 cubics x 100 steps
    for m in marks:
        assert m.kind == "polygon" and len(m.points) == 4 and m.fill[3] == 178
        a, b, comb_b, comb_a = m.points
        assert hypot(*comb_a) > hypot(*a)
        assert hypot(*comb_b) > hypot(*b)


def test_speed_punk_when_varying_curvature_then_ramp_spans_both_ends(glyph):
    fills = {m.fill for m in run(glyph, bend())}
    colours = {f[:3] for f in fills}
    assert len(run(glyph, bend())) == 400
    assert any(c[0] < 200 and c[2] > 100 for c in colours)  # near grey end
    assert any(c[2] < 120 and c[1] < 100 for c in colours)  # near red end


def test_speed_punk_when_quadratic_then_matching_cubic_result(glyph):
    quad = Contour((on(0, 0), off(50, 100), on(100, 0)), False)
    cubic = Contour((on(0, 0), off(100 / 3, 200 / 3), off(200 / 3, 200 / 3),
                     on(100, 0)), False)  # fmt: skip
    got, want = run(glyph, quad), run(glyph, cubic)
    assert len(got) == len(want) == 400
    for g, w in zip(got, want, strict=True):
        assert g.fill == w.fill
        assert [c for p in g.points for c in p] == pytest.approx(
            [c for p in w.points for c in p]
        )


def test_speed_punk_when_coincident_handle_then_no_crash(glyph):
    cusp = Contour((on(0, 0), off(0, 0), off(50, 100), on(100, 0)), False)
    marks = run(glyph, cusp)
    assert marks and all(m.kind == "polygon" for m in marks)
    zero = Contour((on(5, 5), off(5, 5), off(5, 5), on(5, 5)), False)
    assert run(glyph, zero) == []


def test_speed_punk_when_many_cubics_then_steps_floor_at_four(glyph):
    chain = [on(0, 0)]
    for i in range(1, 150):
        chain += [off(i * 10 - 5, 5 * (i % 2)), off(i * 10 - 2, 5 * (i % 2)),
                  on(i * 10, 0)]  # fmt: skip
    assert len(run(glyph, Contour(tuple(chain), False))) == 149 * 4


def test_speed_punk_ramp_endpoints_and_midpoint_exact():
    assert _ramp(0.0) == (139, 147, 156)
    assert _ramp(0.5) == (242, 148, 0)
    assert _ramp(1.0) == (227, 0, 79)
    assert _ramp(0.25) == (round((139 + 242) / 2), round((147 + 148) / 2), 78)

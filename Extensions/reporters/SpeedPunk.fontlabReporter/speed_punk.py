# this_file: Extensions/reporters/SpeedPunk.fontlabReporter/speed_punk.py
# SPDX-License-Identifier: Apache-2.0
"""Draw a colour-ramped curvature comb along every curve segment."""

from math import hypot

from fly.ap.plugins.geometry import segments
from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot

Point = tuple[float, float]
Cubic = tuple[Point, Point, Point, Point]
Sample = tuple[Point, Point, float]
RAMP = (
    (0.0, (139, 147, 156)),
    (0.5, (242, 148, 0)),
    (1.0, (227, 0, 79)),
)
COMB_SCALE = 0.01
MIN_SPEED = 1e-9
MIN_RANGE = 1e-12
MIN_STEPS = 4


def _ramp(p: float) -> tuple[int, int, int]:
    """Interpolate the grey-orange-red ramp at p in [0, 1]."""
    for (p0, c0), (p1, c1) in zip(RAMP, RAMP[1:], strict=False):
        if p <= p1:
            f = (p - p0) / (p1 - p0)
            r, g, b = (round(a + (z - a) * f) for a, z in zip(c0, c1, strict=True))
            return r, g, b
    return RAMP[-1][1]


def _elevate(p0: Point, p1: Point, p2: Point) -> Cubic:
    """Raise a quadratic to the equivalent cubic."""
    c1 = (p0[0] + 2 / 3 * (p1[0] - p0[0]), p0[1] + 2 / 3 * (p1[1] - p0[1]))
    c2 = (p2[0] + 2 / 3 * (p1[0] - p2[0]), p2[1] + 2 / 3 * (p1[1] - p2[1]))
    return p0, c1, c2, p2


def _cubics(snapshot: GlyphSnapshot) -> list[Cubic]:
    """Collect curve segments, elevating quadratics to cubics."""
    cubics: list[Cubic] = []
    for contour in snapshot.contours:
        for seg in segments(contour):
            pts = [(n.x, n.y) for n in seg]
            if len(pts) == 3:
                cubics.append(_elevate(*pts))
            elif len(pts) == 4:
                cubics.append((pts[0], pts[1], pts[2], pts[3]))
    return cubics


def _combine(weights: tuple[float, ...], pts: list[Point]) -> Point:
    """Weighted sum of points."""
    return (
        sum(w * p[0] for w, p in zip(weights, pts, strict=True)),
        sum(w * p[1] for w, p in zip(weights, pts, strict=True)),
    )


def _sample(cubic: Cubic, t: float) -> tuple[Point, Point, Point]:
    """Return point, first and second derivative of a cubic at t."""
    u = 1 - t
    point = _combine((u**3, 3 * u * u * t, 3 * u * t * t, t**3), list(cubic))
    first = [(b[0] - a[0], b[1] - a[1]) for a, b in zip(cubic, cubic[1:], strict=False)]
    second = [
        (c[0] - 2 * b[0] + a[0], c[1] - 2 * b[1] + a[1])
        for a, b, c in zip(cubic, cubic[1:], cubic[2:], strict=False)
    ]
    d1 = _combine((3 * u * u, 6 * u * t, 3 * t * t), first)
    d2 = _combine((6 * u, 6 * t), second)
    return point, d1, d2


class SpeedPunk(Reporter):
    """Shade the outline's curvature as a comb whose colour tracks |k|."""

    name = "speed_punk"
    title = "Speed Punk"
    layer = "background"

    gain = 0.68
    total_steps = 400
    alpha = 178

    def _samples(self, cubic: Cubic, steps: int, upm: float) -> list[Sample | None]:
        """Sample a cubic as (point, comb point, |k|), None where degenerate."""
        out: list[Sample | None] = []
        for i in range(steps + 1):
            point, d, e = _sample(cubic, i / steps)
            speed = hypot(*d)
            if speed < MIN_SPEED:
                out.append(None)
                continue
            k = (d[0] * e[1] - d[1] * e[0]) / speed**3
            scale = k * COMB_SCALE * self.gain * upm**2 / speed
            comb = (point[0] + d[1] * scale, point[1] - d[0] * scale)
            out.append((point, comb, abs(k)))
        return out

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Emit one coloured quad per adjacent valid sample pair."""
        cubics = _cubics(snapshot)
        if not cubics:
            return []
        steps = max(self.total_steps // len(cubics), MIN_STEPS)
        upm = snapshot.metrics.upm
        runs = [self._samples(c, steps, upm) for c in cubics]
        ks = [s[2] for run in runs for s in run if s]
        low, high = min(ks, default=0.0), max(ks, default=0.0)
        if high - low < MIN_RANGE:
            return []
        marks = []
        for run in runs:
            for a, b in zip(run, run[1:], strict=False):
                if a is None or b is None:
                    continue
                p = min(max(((a[2] + b[2]) / 2 - low) / (high - low), 0.0), 1.0)
                fill = (*_ramp(p), self.alpha)
                marks.append(Mark("polygon", (a[0], b[0], b[1], a[1]), fill=fill))
        return marks

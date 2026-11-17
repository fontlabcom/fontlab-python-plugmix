# this_file: Extensions/reporters/StemThickness.fontlabreporter/stem_thickness.py
# SPDX-License-Identifier: Apache-2.0
"""Measure the stem under the mouse across the outline, perpendicular to it."""

from itertools import pairwise
from math import hypot

from fly.ap.plugins.geometry import flatten
from fly.ap.plugins.reporter import Mark, Point, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot

_Edge = tuple[Point, Point]
#: Slack when testing whether a crossing lies on an edge along the ray.
_EPS = 1e-9


def _minus(a: Point, b: Point) -> Point:
    return (a[0] - b[0], a[1] - b[1])


def _cross(a: Point, b: Point) -> float:
    return a[0] * b[1] - a[1] * b[0]


def _dot(a: Point, b: Point) -> float:
    return a[0] * b[0] + a[1] * b[1]


def _edges(snapshot: GlyphSnapshot) -> list[_Edge]:
    """Non-degenerate flattened outline edges, closed contours closed."""
    edges = []
    for contour in snapshot.contours:
        loop = flatten(contour)
        if contour.closed and loop:
            loop = (*loop, loop[0])
        edges += [(a, b) for a, b in pairwise(loop) if a != b]
    return edges


def _nearest(edge: _Edge, p: Point) -> Point:
    """Closest point to ``p`` on a segment."""
    a, b = edge
    d = _minus(b, a)
    t = min(1.0, max(0.0, _dot(_minus(p, a), d) / _dot(d, d)))
    return (a[0] + t * d[0], a[1] + t * d[1])


def _hit(origin: Point, d: Point, edge: _Edge) -> float | None:
    """Signed distance along unit ``d`` (either way) from ``origin`` to the segment."""
    a, b = edge
    e, w = _minus(b, a), _minus(a, origin)
    den = _cross(d, e)
    if den == 0:
        return None
    s, u = _cross(w, e) / den, _cross(w, d) / den
    return s if 0 <= u <= 1 else None


def _span(origin: Point, d: Point, edge: _Edge) -> tuple[float, float] | None:
    """The stretch of the ray an edge lying on the ray's line covers, else None."""
    a, b = edge
    if _cross(_minus(a, origin), d) or _cross(_minus(b, a), d):
        return None
    sa, sb = _dot(_minus(a, origin), d), _dot(_minus(b, origin), d)
    return (min(sa, sb), max(sa, sb))


class StemThickness(Reporter):
    """Nearer crossing only; no guide command and no modifier key."""

    name = "stem_thickness"
    title = "Stem Thickness"
    layer = "foreground"
    needs_mouse = True
    # Upstream "blue", used for the first (here the only) measurement.
    color: tuple[int, int, int] = (166, 161, 240)
    min_length = 1.0
    text_offset = 6.0

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """No view, mouse, outline or crossing beyond ``min_length`` draws nothing.

        Crossings on an edge that lies along the ray (a ray from a corner
        running down the outline) are ignored, so such a corner draws nothing.
        """
        mouse = snapshot.view.mouse if snapshot.view else None
        if mouse is None or not (edges := _edges(snapshot)):
            return []
        source = min(edges, key=lambda e: hypot(*_minus(_nearest(e, mouse), mouse)))
        start = _nearest(source, mouse)
        dx, dy = _minus(source[1], source[0])
        normal = (-dy / hypot(dx, dy), dx / hypot(dx, dy))
        spans = [sp for e in edges if (sp := _span(start, normal, e)) is not None]
        hits = [_hit(start, normal, edge) for edge in edges if edge is not source]
        hits = [
            s
            for s in hits
            if s is not None
            and abs(s) > self.min_length
            and not any(lo - _EPS <= s <= hi + _EPS for lo, hi in spans)
        ]
        if not hits:
            return []
        s = min(hits, key=abs)
        end = (start[0] + s * normal[0], start[1] + s * normal[1])
        label = (
            (start[0] + end[0]) / 2 + self.text_offset,
            (start[1] + end[1]) / 2 + self.text_offset,
        )
        return [
            Mark("line", (start, end), self.color),
            Mark("text", (label,), self.color, text=str(round(abs(s)))),
        ]

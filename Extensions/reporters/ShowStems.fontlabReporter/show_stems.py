# this_file: Extensions/reporters/ShowStems.fontlabReporter/show_stems.py
# SPDX-License-Identifier: Apache-2.0
"""Measure horizontal stem and counter widths along a mid-height scan line."""

from itertools import pairwise
from math import radians, tan

from fly.ap.plugins.geometry import point_at, segments
from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot

LINE_COLOR = (170, 175, 200)
CROSSING_COLOR = (60, 60, 110)
TEXT_COLOR = (0, 77, 204)
INSIDE_COLOR = (0, 191, 51)
CURVE_STEPS = 24


class ShowStems(Reporter):
    """Scan at half x-height (half cap height for tall glyphs) and label spans."""

    name = "show_stems"
    title = "Show Stems"
    layer = "background"
    needs_bounds = True

    def _edges(self, snapshot: GlyphSnapshot):
        """Yield flattened edges of every segment as ((x, y), (x, y)) pairs."""
        for contour in snapshot.contours:
            for seg in segments(contour):
                if len(seg) == 2:
                    points = [(node.x, node.y) for node in seg]
                else:
                    points = [
                        point_at(seg, i / CURVE_STEPS) for i in range(CURVE_STEPS + 1)
                    ]
                yield from pairwise(points)

    def _crossings(self, snapshot: GlyphSnapshot, y: float) -> list[float]:
        """Sorted x of edges crossing y; the half-open test counts vertices once."""
        xs = []
        for (px, py), (qx, qy) in self._edges(snapshot):
            if py <= y < qy or qy <= y < py:
                xs.append(px + (y - py) * (qx - px) / (qy - py))
        return sorted(xs)

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Draw the scan line, its crossings and the width of each span."""
        nodes = [n for contour in snapshot.contours for n in contour.nodes]
        if not nodes:
            return []
        metrics = snapshot.metrics
        top = snapshot.bounds[3] if snapshot.bounds else max(n.y for n in nodes)
        tall = top >= (metrics.x_height + metrics.cap_height) / 2
        y = (metrics.cap_height if tall else metrics.x_height) / 2
        sx = tan(radians(metrics.italic_slant)) * (y - metrics.x_height / 2)
        xs = self._crossings(snapshot, y)
        marks = [
            Mark(
                "line",
                ((sx, y), (snapshot.advance + sx, y)),
                LINE_COLOR,
                stroke_px=1,
            )
        ]
        marks += [Mark("ring", ((x, y),), CROSSING_COLOR, diameter_px=5) for x in xs]
        for i, (left, right) in enumerate(pairwise(xs)):
            middle = (left + right) / 2
            label = (middle, y + 0.015 * metrics.upm)
            marks.append(
                Mark("text", (label,), TEXT_COLOR, text=str(round(right - left)))
            )
            if i % 2 == 0:
                marks.append(Mark("ring", ((middle, y),), INSIDE_COLOR, diameter_px=6))
        return marks

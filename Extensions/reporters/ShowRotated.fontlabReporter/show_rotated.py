# this_file: Extensions/reporters/ShowRotated.fontlabReporter/show_rotated.py
# SPDX-License-Identifier: Apache-2.0
"""Outline the glyph rotated 180 degrees about its bounds centre."""

from fly.ap.plugins.geometry import point_at, segments
from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot

COLOR: tuple[int, int, int] = (0, 128, 77)
CURVE_STEPS = 16
CROSS_ARM = 0.02  # fraction of upm


class ShowRotated(Reporter):
    """Draw the half-turned outline, its on-curve rings and a centre cross."""

    name = "show_rotated"
    title = "Show Rotated"
    layer = "background"
    needs_bounds = True

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Rotate every flattened segment about the centre; no fill is drawn."""
        nodes = [n for contour in snapshot.contours for n in contour.nodes]
        if not nodes:
            return []
        xmin, ymin, xmax, ymax = snapshot.bounds or (
            min(n.x for n in nodes),
            min(n.y for n in nodes),
            max(n.x for n in nodes),
            max(n.y for n in nodes),
        )
        cx, cy = (xmin + xmax) / 2, (ymin + ymax) / 2

        def turn(x: float, y: float) -> tuple[float, float]:
            return 2 * cx - x, 2 * cy - y

        marks = []
        for contour in snapshot.contours:
            for seg in segments(contour):
                if len(seg) == 2:
                    points = [(n.x, n.y) for n in seg]
                else:
                    points = [
                        point_at(seg, i / CURVE_STEPS) for i in range(CURVE_STEPS + 1)
                    ]
                marks.append(
                    Mark(
                        "polyline", tuple(turn(*p) for p in points), COLOR, stroke_px=1
                    )
                )
        marks += [
            Mark("ring", (turn(n.x, n.y),), COLOR, diameter_px=6)
            for n in nodes
            if n.on_curve
        ]
        arm = CROSS_ARM * snapshot.metrics.upm
        marks.append(Mark("line", ((cx - arm, cy), (cx + arm, cy)), COLOR, stroke_px=1))
        marks.append(Mark("line", ((cx, cy - arm), (cx, cy + arm)), COLOR, stroke_px=1))
        return marks

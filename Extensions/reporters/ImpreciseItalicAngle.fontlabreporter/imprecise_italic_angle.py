# this_file: Extensions/reporters/ImpreciseItalicAngle.fontlabreporter/imprecise_italic_angle.py
# SPDX-License-Identifier: Apache-2.0
"""Mark straight segments almost, but not exactly, at the master slant."""

from math import atan2, degrees

from fly.ap.plugins.geometry import segments
from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot


class ImpreciseItalicAngle(Reporter):
    """Check each straight segment against the master's vertical slant."""

    name = "imprecise_italic_angle"
    title = "Imprecise Italic Angle"
    tolerance_deg = 2.0
    exact_deg = 0.001

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Highlight near-angle lines, ignoring horizontal and exact matches."""
        marks = []
        for contour in snapshot.contours:
            for segment in segments(contour):
                if len(segment) != 2:
                    continue
                start, end = segment
                dx, dy = end.x - start.x, end.y - start.y
                if dy == 0:
                    continue
                if dy < 0:
                    dx, dy = -dx, -dy
                angle = degrees(atan2(dx, dy))
                delta = abs(angle - snapshot.metrics.italic_slant)
                if self.exact_deg < delta <= self.tolerance_deg:
                    marks.append(
                        Mark(
                            "line",
                            ((start.x, start.y), (end.x, end.y)),
                            (235, 75, 60),
                            2.5,
                        )
                    )
        return marks

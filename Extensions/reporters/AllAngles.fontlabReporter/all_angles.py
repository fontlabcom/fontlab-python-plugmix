# this_file: Extensions/reporters/AllAngles.fontlabReporter/all_angles.py
# SPDX-License-Identifier: Apache-2.0
"""Label the angle of every straight segment, optionally every handle."""

from math import atan2, degrees, hypot

from fly.ap.plugins.geometry import segments
from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot, Node

SEGMENT_COLOR = (56, 217, 137)
HANDLE_COLOR = (217, 56, 107)


class AllAngles(Reporter):
    """Show bearings from vertical, 0 to 180 degrees, for lines and handles."""

    name = "all_angles"
    title = "All Angles"
    show_handles = False

    def _label(
        self, start: Node, end: Node, color: tuple[int, int, int], upm: float
    ) -> list[Mark]:
        """Label one vector beside its midpoint; zero length gives nothing."""
        dx, dy = end.x - start.x, end.y - start.y
        size = hypot(dx, dy)
        if not size:
            return []
        offset = 0.02 * upm
        point = (
            (start.x + end.x) / 2 - dy / size * offset,
            (start.y + end.y) / 2 + dx / size * offset,
        )
        angle = degrees(atan2(dx, dy)) % 180
        if round(angle, 1) >= 180:  # a hair left of vertical must read 0.0
            angle = 0.0
        text = f"{angle:.1f}°"
        return [Mark("text", (point,), color, text=text)]

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Collect labels for two-node segments and, if enabled, handles."""
        upm, marks = snapshot.metrics.upm, []
        for contour in snapshot.contours:
            for seg in segments(contour):
                if len(seg) == 2:
                    marks += self._label(seg[0], seg[1], SEGMENT_COLOR, upm)
                elif len(seg) == 4 and self.show_handles:
                    marks += self._label(seg[0], seg[1], HANDLE_COLOR, upm)
                    marks += self._label(seg[3], seg[2], HANDLE_COLOR, upm)
        return marks

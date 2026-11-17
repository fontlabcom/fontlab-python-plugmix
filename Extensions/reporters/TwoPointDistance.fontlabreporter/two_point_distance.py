# this_file: Extensions/reporters/TwoPointDistance.fontlabreporter/two_point_distance.py
# SPDX-License-Identifier: Apache-2.0
"""Show a segment, distance and angle when exactly two nodes are selected."""

from math import atan2, degrees, hypot

from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot


class TwoPointDistance(Reporter):
    """Measure both on-curve and off-curve selected points."""

    name = "two_point_distance"
    title = "Two Point Distance"

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Show a line and its length/angle only for a two-node selection."""
        nodes = [
            node
            for contour in snapshot.contours
            for node in contour.nodes
            if node.selected
        ]
        if len(nodes) != 2:
            return []
        first, last = nodes
        dx, dy = last.x - first.x, last.y - first.y
        midpoint = ((first.x + last.x) / 2, (first.y + last.y) / 2)
        return [
            Mark("line", ((first.x, first.y), (last.x, last.y)), (85, 115, 210)),
            Mark(
                "text",
                (midpoint,),
                (85, 115, 210),
                text=f"{hypot(dx, dy):.1f} · {degrees(atan2(dy, dx)):.1f}°",
            ),
        ]

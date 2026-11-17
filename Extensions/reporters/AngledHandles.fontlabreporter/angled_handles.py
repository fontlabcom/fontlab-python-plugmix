# this_file: Extensions/reporters/AngledHandles.fontlabreporter/angled_handles.py
# SPDX-License-Identifier: Apache-2.0
"""Mark off-curve handles departing from horizontal, vertical or italic axes."""

from math import atan2, degrees

from fly.ap.plugins.geometry import neighbours
from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot


class AngledHandles(Reporter):
    """Flag handles with an axis mismatch greater than a small angle."""

    name = "angled_handles"
    title = "Angled Handles"
    tolerance_deg = 0.5

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Compare each handle with its adjacent on-curve endpoint."""
        marks = []
        for contour in snapshot.contours:
            nodes = contour.nodes
            for index, node in enumerate(nodes):
                if node.on_curve or len(nodes) < 2:
                    continue
                for adjacent in neighbours(contour, index):
                    if adjacent is None or not adjacent.on_curve:
                        continue
                    dx, dy = node.x - adjacent.x, node.y - adjacent.y
                    if dx == 0 and dy == 0:
                        break
                    if dy < 0:
                        dx, dy = -dx, -dy
                    angle = degrees(atan2(dx, dy))
                    axes = (0.0, 90.0, -90.0, snapshot.metrics.italic_slant)
                    if min(abs(angle - axis) for axis in axes) > self.tolerance_deg:
                        marks.append(Mark("ring", ((node.x, node.y),), (230, 120, 20)))
                    break
        return marks

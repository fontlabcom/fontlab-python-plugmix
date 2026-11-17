# this_file: Extensions/reporters/SmartPlumblines.fontlabreporter/smart_plumblines.py
# SPDX-License-Identifier: Apache-2.0
"""Draw a horizontal and italic-aware vertical centre line per contour."""

from math import radians, tan

from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot, Node

CONTOUR_COLOR = (200, 60, 90)
SELECTION_COLOR = (0, 150, 145)


class SmartPlumblines(Reporter):
    """Centre crosses for each contour and for the selected nodes."""

    name = "smart_plumblines"
    title = "Smart Plumblines"
    layer = "background"

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Emit one cross per non-empty contour plus one for the selection."""
        sets = [(c.nodes, CONTOUR_COLOR) for c in snapshot.contours if c.nodes]
        selected = tuple(n for c in snapshot.contours for n in c.nodes if n.selected)
        if selected:
            sets.append((selected, SELECTION_COLOR))
        return [m for nodes, color in sets for m in self._cross(snapshot, nodes, color)]

    def _cross(
        self, snapshot: GlyphSnapshot, nodes: tuple[Node, ...], color: tuple
    ) -> list[Mark]:
        """Build the horizontal and slanted vertical line for one node set."""
        metrics = snapshot.metrics
        slant, mid = tan(radians(metrics.italic_slant)), metrics.x_height / 2
        ys = [n.y for n in nodes]
        us = [n.x - slant * (n.y - mid) for n in nodes]
        cy, cu = (min(ys) + max(ys)) / 2, (min(us) + max(us)) / 2
        low, high = metrics.descender, metrics.ascender
        return [
            Mark("line", ((0, cy), (snapshot.advance, cy)), color, stroke_px=0.75),
            Mark(
                "line",
                ((cu + slant * (low - mid), low), (cu + slant * (high - mid), high)),
                color,
                stroke_px=0.75,
            ),
        ]

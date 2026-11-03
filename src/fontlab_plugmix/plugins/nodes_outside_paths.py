# this_file: src/fontlab_plugmix/plugins/nodes_outside_paths.py
# SPDX-License-Identifier: Apache-2.0
"""Highlight off-curve handles beyond the on-curve bounding rectangle."""

from fontlab_plugmix.reporter import Mark, Reporter
from fontlab_plugmix.snapshot import GlyphSnapshot


class NodesOutsidePaths(Reporter):
    """Use on-curve extrema as the comparison bounds."""

    name = "nodes_outside_paths"
    title = "Nodes Outside Paths"

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Mark only handles outside the on-curve rectangle."""
        nodes = [node for contour in snapshot.contours for node in contour.nodes]
        on = [node for node in nodes if node.on_curve]
        if not on:
            return []
        x_min, x_max = min(n.x for n in on), max(n.x for n in on)
        y_min, y_max = min(n.y for n in on), max(n.y for n in on)
        return [
            Mark("ring", ((n.x, n.y),), (30, 95, 220), stroke_px=2, diameter_px=13)
            for n in nodes
            if not n.on_curve
            and (n.x < x_min or n.x > x_max or n.y < y_min or n.y > y_max)
        ]

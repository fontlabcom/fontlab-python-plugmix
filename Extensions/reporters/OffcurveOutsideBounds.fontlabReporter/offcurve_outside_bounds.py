# this_file: Extensions/reporters/OffcurveOutsideBounds.fontlabReporter/offcurve_outside_bounds.py
# SPDX-License-Identifier: Apache-2.0
"""Highlight off-curve handles beyond the on-curve bounding rectangle.

Unlike mekkablue's ShowNodesOutsidePaths, this does not test path containment.
"""

from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot


class OffcurveOutsideBounds(Reporter):
    """Use on-curve extrema as the comparison bounds."""

    name = "offcurve_outside_bounds"
    title = "Off-curve Handles Outside Bounds"

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

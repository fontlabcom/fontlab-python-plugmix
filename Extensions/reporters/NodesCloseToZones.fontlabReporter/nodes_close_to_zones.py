# this_file: Extensions/reporters/NodesCloseToZones.fontlabReporter/nodes_close_to_zones.py
# SPDX-License-Identifier: MIT
"""Mark on-curves near, but not exactly on, master zones or metric levels."""

from fontlabapp.plugins.reporter import Mark, Reporter
from fontlabapp.plugins.snapshot import GlyphSnapshot


class NodesCloseToZones(Reporter):
    """Find near misses against selected-master PostScript zones and metrics."""

    name = "nodes_close_to_zones"
    title = "Nodes Close to Zones"
    tolerance = 5.0
    needs_zones = True

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Ring each node with a nonzero y-distance at most the tolerance."""
        metrics = snapshot.metrics
        levels = {
            0.0,
            metrics.ascender,
            metrics.descender,
            metrics.x_height,
            metrics.cap_height,
        }
        for zone in metrics.zones:
            levels.update((zone.position, zone.edge))
        return [
            Mark("ring", ((node.x, node.y),), (230, 120, 30), diameter_px=14)
            for contour in snapshot.contours
            for node in contour.nodes
            if node.on_curve
            and any(0 < abs(node.y - level) <= self.tolerance for level in levels)
        ]

# this_file: Extensions/reporters/NodeCount.fontlabreporter/node_count.py
# SPDX-License-Identifier: Apache-2.0
"""Show the total number of nodes in the glyph beside its advance."""

from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot


class NodeCount(Reporter):
    """Count on- and off-curve nodes across all contours."""

    name = "node_count"
    title = "Node Count"
    layer = "background"

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Label the total just right of the advance line."""
        total = sum(len(contour.nodes) for contour in snapshot.contours)
        if not total:
            return []
        x = snapshot.advance + 0.02 * snapshot.metrics.upm
        return [Mark("text", ((x, 1),), (102, 0, 153), text=f"· {total}")]

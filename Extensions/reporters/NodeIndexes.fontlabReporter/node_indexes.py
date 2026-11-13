# this_file: Extensions/reporters/NodeIndexes.fontlabReporter/node_indexes.py
# SPDX-License-Identifier: Apache-2.0
"""Label every node with its full contour index, including off-curves.

Mekkablue's ShowNodeIndexes displays BCP indexes by default. FontLab's own
contour numbering also counts every node, so labels and numbers follow that
same full sequence without a separate BCP visibility setting.
"""

from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot


class NodeIndexes(Reporter):
    """Use original contour indexes at all node positions."""

    name = "node_indexes"
    title = "Node Indexes"

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Place an index beside each on- and off-curve node."""
        return [
            Mark("text", ((node.x + 5, node.y + 5),), (145, 88, 45), text=str(index))
            for contour in snapshot.contours
            for index, node in enumerate(contour.nodes)
        ]

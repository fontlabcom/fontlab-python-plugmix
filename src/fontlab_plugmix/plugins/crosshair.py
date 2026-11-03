# this_file: src/fontlab_plugmix/plugins/crosshair.py
# SPDX-License-Identifier: Apache-2.0
"""Draw broad, thin crosshairs through selected nodes, without mouse tracking."""

from fontlab_plugmix.reporter import Mark, Reporter
from fontlab_plugmix.snapshot import GlyphSnapshot


class Crosshair(Reporter):
    """Extend selected-node guides far beyond normal Glyph window extents."""

    name = "crosshair"
    title = "Crosshair"
    layer = "background"
    extent = 1_000_000.0

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Draw two guides per selected node."""
        marks = []
        for contour in snapshot.contours:
            for node in contour.nodes:
                if node.selected:
                    marks.extend(
                        (
                            Mark(
                                "line",
                                ((-self.extent, node.y), (self.extent, node.y)),
                                (140, 140, 140),
                                0.75,
                            ),
                            Mark(
                                "line",
                                ((node.x, -self.extent), (node.x, self.extent)),
                                (140, 140, 140),
                                0.75,
                            ),
                        )
                    )
        return marks

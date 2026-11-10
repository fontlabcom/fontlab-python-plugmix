# this_file: Extensions/reporters/SelectedCoordinates.fontlabReporter/selected_coordinates.py
# SPDX-License-Identifier: Apache-2.0
"""Show x and y beside selected native nodes."""

from fontlabapp.plugins.reporter import Mark, Reporter
from fontlabapp.plugins.snapshot import GlyphSnapshot


class SelectedCoordinates(Reporter):
    """Display coordinates for every selected node, including handles."""

    name = "selected_coordinates"
    title = "Selected Node Coordinates"

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Return compact coordinate labels at selected nodes."""
        return [
            Mark(
                "text",
                ((node.x + 6, node.y - 6),),
                (30, 105, 190),
                text=f"{node.x:g}, {node.y:g}",
            )
            for contour in snapshot.contours
            for node in contour.nodes
            if node.selected
        ]

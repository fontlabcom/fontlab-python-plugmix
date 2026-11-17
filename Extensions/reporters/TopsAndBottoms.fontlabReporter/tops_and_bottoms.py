# this_file: Extensions/reporters/TopsAndBottoms.fontlabreporter/tops_and_bottoms.py
# SPDX-License-Identifier: Apache-2.0
"""Label the highest and lowest on-curve positions in the active glyph."""

from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot


class TopsAndBottoms(Reporter):
    """Show all tied extrema, preserving their exact y values."""

    name = "tops_and_bottoms"
    title = "Tops and Bottoms"
    layer = "background"

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Place a ring and numeric label at each top or bottom on-curve."""
        on = [n for contour in snapshot.contours for n in contour.nodes if n.on_curve]
        if not on:
            return []
        levels = {min(n.y for n in on), max(n.y for n in on)}
        marks = []
        for node in on:
            if node.y in levels:
                marks.append(Mark("ring", ((node.x, node.y),), (190, 65, 65)))
                marks.append(
                    Mark(
                        "text",
                        ((node.x + 6, node.y + 8),),
                        (190, 65, 65),
                        text=f"{node.y:g}",
                    )
                )
        return marks

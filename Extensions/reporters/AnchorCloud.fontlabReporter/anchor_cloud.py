# this_file: Extensions/reporters/AnchorCloud.fontlabReporter/anchor_cloud.py
# SPDX-License-Identifier: Apache-2.0
"""Show the current glyph's named anchors as a small local cloud."""

from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot


class AnchorCloud(Reporter):
    """Annotate the current layer's anchor positions without font-wide reads."""

    name = "anchor_cloud"
    title = "Anchor Cloud"

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Return a dot and name for every current-layer anchor."""
        marks = []
        for anchor in snapshot.anchors:
            marks.append(
                Mark("ring", ((anchor.x, anchor.y),), (105, 145, 185), diameter_px=8)
            )
            marks.append(
                Mark(
                    "text",
                    ((anchor.x + 6, anchor.y + 8),),
                    (105, 145, 185),
                    text=anchor.name,
                )
            )
        return marks

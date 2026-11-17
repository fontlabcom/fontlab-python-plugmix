# this_file: Extensions/reporters/DuplicateAnchors.fontlabreporter/duplicate_anchors.py
# SPDX-License-Identifier: Apache-2.0
"""Show one red and yellow ring pair for every anchor pair under one unit."""

from math import hypot

from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot


class DuplicateAnchors(Reporter):
    """Three coincident anchors produce three ring pairs at first anchors."""

    name = "duplicate_anchors"
    title = "Duplicate Anchor Rings"
    handle_size = 8

    @classmethod
    def set_handle_size(cls, size: int) -> None:
        """Choose the old launcher's 5, 8 or 12 pixel handle size."""
        if size not in (5, 8, 12):
            raise ValueError("Handle size must be 5, 8 or 12")
        cls.handle_size = size

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Find all unordered pairs closer than one font unit."""
        marks = []
        for index, anchor in enumerate(snapshot.anchors):
            for other in snapshot.anchors[index + 1 :]:
                if hypot(anchor.x - other.x, anchor.y - other.y) < 1:
                    center = ((anchor.x, anchor.y),)
                    marks.extend(
                        (
                            Mark(
                                "ring",
                                center,
                                (255, 0, 0),
                                stroke_px=6,
                                diameter_px=2 * self.handle_size,
                            ),
                            Mark(
                                "ring",
                                center,
                                (255, 255, 0),
                                stroke_px=2,
                                diameter_px=2 * self.handle_size,
                            ),
                        )
                    )
        return marks

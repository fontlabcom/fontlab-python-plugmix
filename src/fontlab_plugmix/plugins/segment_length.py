# this_file: src/fontlab_plugmix/plugins/segment_length.py
# SPDX-License-Identifier: Apache-2.0
"""Label straight and flattened Bézier lengths for selected or all segments."""

from fontlab_plugmix.geometry import length, point_at, segments
from fontlab_plugmix.reporter import Mark, Reporter
from fontlab_plugmix.snapshot import GlyphSnapshot


class SegmentLength(Reporter):
    """Prefer segments with both on-curve ends selected; otherwise show all."""

    name = "segment_length"
    title = "Segment Length"
    flatten_steps = 25

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Measure each eligible contour segment in font units."""
        rows = [
            segment for contour in snapshot.contours for segment in segments(contour)
        ]
        selected = any(
            node.selected for contour in snapshot.contours for node in contour.nodes
        )
        chosen = [
            segment for segment in rows if segment[0].selected and segment[-1].selected
        ]
        return [
            Mark(
                "text",
                (point_at(segment, 0.5),),
                (195, 45, 45),
                text=f"{length(segment, self.flatten_steps):.1f}",
            )
            for segment in (chosen if selected else rows)
        ]

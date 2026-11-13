# this_file: Extensions/reporters/RSBLine.fontlabReporter/rsb_line.py
# SPDX-License-Identifier: Apache-2.0
"""Show advance boundary and the on-curve left and right sidebearings."""

from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot


class RSBLine(Reporter):
    """Annotate sidebearings from on-curve x extrema."""

    name = "rsb_line"
    title = "RSB Line"
    layer = "background"
    needs_bounds = True

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Draw the advance boundary and label both sidebearings."""
        if snapshot.bounds is None:
            on = [
                n for contour in snapshot.contours for n in contour.nodes if n.on_curve
            ]
            if not on:
                return []
            left, right = min(n.x for n in on), max(n.x for n in on)
        else:
            left, _bottom, right, _top = snapshot.bounds
        bottom, top = snapshot.metrics.descender, snapshot.metrics.ascender
        color = (80, 145, 190)
        return [
            Mark("line", ((snapshot.advance, bottom), (snapshot.advance, top)), color),
            Mark(
                "text",
                ((snapshot.advance + 7, 0),),
                color,
                text=f"RSB {snapshot.advance - right:g}",
            ),
            Mark("text", ((0, 0),), color, text=f"LSB {left:g}"),
        ]

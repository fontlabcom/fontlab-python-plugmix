# this_file: Extensions/reporters/KernIndicator.fontlabreporter/kern_indicator.py
# SPDX-License-Identifier: Apache-2.0
"""Print the kerning values of the pairs touching the glyph, above the junctions."""

from math import isfinite

from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot


class KernIndicator(Reporter):
    """Positive values orange, negative blue; shown only at 3% to 90% zoom."""

    name = "kern_indicator"
    title = "Kern Indicator"
    layer = "foreground"
    needs_neighbours = True
    # Apple light-mode systemOrange / systemBlue, as the upstream uses.
    positive_color: tuple[int, int, int] = (255, 149, 0)
    negative_color: tuple[int, int, int] = (0, 122, 255)
    offset = -50  # from the ascender
    min_px_per_unit = 0.03
    max_px_per_unit = 0.9

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """No view, neighbours, or a zero or non-finite value draws nothing for that side."""
        view = snapshot.view
        if view is None or view.neighbours is None:
            return []
        if not self.min_px_per_unit <= view.px_per_unit <= self.max_px_per_unit:
            return []
        y = snapshot.metrics.ascender + self.offset
        marks = []
        for side, x in (
            (view.neighbours.prev, 0),
            (view.neighbours.next, snapshot.advance),
        ):
            if side is None or not isfinite(value := side[1]) or value == 0:
                continue
            color = self.positive_color if value > 0 else self.negative_color
            marks.append(Mark("text", ((x, y),), color, text=_label(value)))
        return marks


def _label(value: float) -> str:
    """Retain normal rounding without labelling a nonzero value as zero."""
    whole = round(value)
    if abs(value - whole) <= 1e-6:
        label = str(whole)
    else:
        label = f"{value:.2f}".rstrip("0").rstrip(".")
    return f"{value:.2g}" if value != 0 and label in {"0", "-0"} else label

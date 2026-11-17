# this_file: Extensions/reporters/Blindfold.fontlabreporter/blindfold.py
# SPDX-License-Identifier: Apache-2.0
"""Hide everything outside the reading band between the metrics."""

from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot


class Blindfold(Reporter):
    """Two opaque blocks leave only the band from baseline to the chosen height."""

    name = "blindfold"
    title = "Blindfold"
    layer = "foreground"
    buffer = 70
    reach = 10  # block overhang, in units per em either side of the glyph
    band = "x_height"  # or "cap_height"
    shade: tuple[int, int, int, int] = (0, 0, 0, 255)

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Cover below the baseline and above the band height."""
        m = snapshot.metrics
        top = m.cap_height if self.band == "cap_height" else m.x_height
        x0, x1 = -self.reach * m.upm, snapshot.advance + self.reach * m.upm

        def block(y0: float, y1: float) -> Mark:
            pts = ((x0, y0), (x1, y0), (x1, y1), (x0, y1))
            return Mark("polygon", pts, fill=self.shade)

        return [
            block(m.descender - self.buffer, 0),
            block(top, m.ascender + self.buffer),
        ]

# this_file: Extensions/reporters/GlyphFocus.fontlabreporter/glyph_focus.py
# SPDX-License-Identifier: Apache-2.0
"""Dim the viewport outside the glyph advance and vertical metrics box."""

from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot


class GlyphFocus(Reporter):
    """Leave the current glyph's advance box unobscured."""

    name = "glyph_focus"
    title = "Glyph Focus"
    extent = 1_000_000.0
    shade = (40, 40, 40, 70)

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Return four translucent rectangles around the advance box."""
        e = self.extent
        top, bottom = snapshot.metrics.ascender, snapshot.metrics.descender
        advance = snapshot.advance
        rectangles = (
            ((-e, top), (e, top), (e, e), (-e, e)),
            ((-e, -e), (e, -e), (e, bottom), (-e, bottom)),
            ((-e, bottom), (0, bottom), (0, top), (-e, top)),
            ((advance, bottom), (e, bottom), (e, top), (advance, top)),
        )
        return [Mark("polygon", points, fill=self.shade) for points in rectangles]

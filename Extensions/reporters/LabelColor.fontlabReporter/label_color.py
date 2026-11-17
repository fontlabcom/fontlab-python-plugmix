# this_file: Extensions/reporters/LabelColor.fontlabreporter/label_color.py
# SPDX-License-Identifier: Apache-2.0
"""Draw a bar in the glyph's label colour under the glyph."""

from fly.ap.plugins.geometry import shear
from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot


class LabelColor(Reporter):
    """Bar in the glyph's mark colour; layer marks are not distinguished."""

    name = "label_color"
    title = "Show Label Color"
    layer = "background"
    placement = "descender"  # or "baseline", "body"
    alpha = 230
    body_alpha = 128
    thickness = 40

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Fill a slanted rectangle; nothing for unmarked glyphs."""
        identity, m = snapshot.identity, snapshot.metrics
        if identity is None or identity.mark_rgb is None:
            return []
        if self.placement == "body":
            y0, y1, alpha = m.descender, m.ascender, self.body_alpha
        elif self.placement == "baseline":
            y0, y1, alpha = -self.thickness, 0, self.alpha
        else:
            y0, y1, alpha = m.descender - self.thickness, m.descender, self.alpha
        w = snapshot.advance
        points = shear(
            ((0, y0), (w, y0), (w, y1), (0, y1)), m.italic_slant, m.x_height / 2
        )
        return [Mark("polygon", points, fill=(*identity.mark_rgb, alpha))]

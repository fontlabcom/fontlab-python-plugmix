# this_file: Extensions/reporters/ExportStatus.fontlabreporter/export_status.py
# SPDX-License-Identifier: Apache-2.0
"""Cross out glyphs that are set not to export."""

from fly.ap.plugins.geometry import shear
from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot


class ExportStatus(Reporter):
    """Red cross corner to corner over the body, slanted by the italic angle."""

    name = "export_status"
    title = "Show Export Status"
    layer = "foreground"
    color: tuple[int, int, int] = (255, 0, 0)
    stroke_px = 2

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Only an explicit not-exported flag draws; unknown identity is silent."""
        identity, m = snapshot.identity, snapshot.metrics
        if identity is None or identity.exported is not False:
            return []
        w, pivot = snapshot.advance, m.x_height / 2
        diagonals = (
            ((0, m.descender), (w, m.ascender)),
            ((0, m.ascender), (w, m.descender)),
        )
        return [
            Mark(
                "line",
                shear(d, m.italic_slant, pivot),
                self.color,
                stroke_px=self.stroke_px,
            )
            for d in diagonals
        ]

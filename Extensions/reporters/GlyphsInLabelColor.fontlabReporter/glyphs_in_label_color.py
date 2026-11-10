# this_file: Extensions/reporters/GlyphsInLabelColor.fontlabReporter/glyphs_in_label_color.py
# SPDX-License-Identifier: Apache-2.0
"""Fill the glyph, components included, in its label colour."""

from fontlabapp.plugins.reporter import Mark, Reporter, fill_mark
from fontlabapp.plugins.snapshot import GlyphSnapshot


class GlyphsInLabelColor(Reporter):
    """One odd-even polygon over every contour so counters stay open."""

    name = "glyphs_in_label_color"
    title = "Show Glyphs In Label Color"
    layer = "background"
    needs_components = True
    alpha = 171

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Skip unmarked glyphs and glyphs without a fillable contour."""
        identity = snapshot.identity
        if identity is None or identity.mark_rgb is None:
            return []
        contours = snapshot.contours + tuple(
            c for comp in snapshot.components for c in comp.contours
        )
        mark = fill_mark(contours, (*identity.mark_rgb, self.alpha))
        return [] if mark is None else [mark]

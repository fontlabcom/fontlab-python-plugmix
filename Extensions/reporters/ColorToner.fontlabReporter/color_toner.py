# this_file: Extensions/reporters/ColorToner.fontlabReporter/color_toner.py
# SPDX-License-Identifier: Apache-2.0
"""Shade every component in translucent black so composed parts stand out."""

from fontlabapp.plugins.reporter import Mark, Reporter, fill_mark
from fontlabapp.plugins.snapshot import GlyphSnapshot


class ColorToner(Reporter):
    """One odd-even polygon per component, alpha taken from `darken` wrapped into 0..1."""

    name = "color_toner"
    title = "Color Toner"
    layer = "background"
    needs_components = True
    darken = 0.15
    color: tuple[int, int, int] = (0, 0, 0)

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Components without a fillable contour are skipped."""
        # Wrap like upstream, but keep a whole number >= 1 opaque, not clear;
        # negatives clamp to clear.
        tone = 0.0 if self.darken < 0 else self.darken % 1 or min(self.darken, 1.0)
        fill = (*self.color, round(255 * tone))
        marks = (fill_mark(comp.contours, fill) for comp in snapshot.components)
        return [mark for mark in marks if mark is not None]

# this_file: Extensions/reporters/ShowBackground.fontlabReporter/show_background.py
# SPDX-License-Identifier: Apache-2.0
"""Fill the glyph's background layer outlines in a pale blue."""

from fontlabapp.plugins.reporter import Mark, Reporter, fill_mark
from fontlabapp.plugins.snapshot import GlyphSnapshot


class ShowBackground(Reporter):
    """One odd-even polygon over the background outlines; its components are not read."""

    name = "show_background"
    title = "Show Background"
    layer = "background"
    needs_background = True
    color: tuple[int, int, int] = (164, 221, 237)
    alpha = 77

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """No background layer, or one without a fillable contour, draws nothing."""
        mark = fill_mark(snapshot.background or (), (*self.color, self.alpha))
        return [] if mark is None else [mark]

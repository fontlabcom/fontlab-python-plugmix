# this_file: Extensions/reporters/ShowCharacter.fontlabreporter/show_character.py
# SPDX-License-Identifier: Apache-2.0
"""Print the glyph's character above it at a fixed pixel size."""

from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot


class ShowCharacter(Reporter):
    """First Unicode as 100-px text; hidden when zoomed far out."""

    name = "show_character"
    title = "Show Character"
    layer = "background"
    needs_bounds = True
    text_px = 100
    min_px_per_unit = 0.2
    margin = 50
    color: tuple[int, int, int] = (26, 102, 204)

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """No Unicode (and no base-name lookup) means no mark."""
        identity, view = snapshot.identity, snapshot.view
        if identity is None or not identity.unicodes:
            return []
        if view is not None and view.px_per_unit < self.min_px_per_unit:
            return []
        try:
            char = chr(identity.unicodes[0])
        except (ValueError, OverflowError):
            return []
        if not char.isprintable():
            return []
        top = snapshot.bounds[3] if snapshot.bounds else float("-inf")
        y = max(snapshot.metrics.ascender, top + self.margin)
        return [Mark("text", ((0, y),), self.color, text=char, text_px=self.text_px)]

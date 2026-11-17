# this_file: Extensions/reporters/Unitizer.fontlabreporter/unitizer.py
# SPDX-License-Identifier: Apache-2.0
"""Draw a configurable vertical unit grid across the glyph advance."""

from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot


class Unitizer(Reporter):
    """Display simple unit increments behind the active glyph."""

    name = "unitizer"
    title = "Unitizer"
    layer = "background"
    units_per_em = 18
    max_lines = 2_000

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Generate bounded grid lines from one increment to the advance."""
        if self.units_per_em <= 0 or snapshot.metrics.upm <= 0:
            return []
        step = snapshot.metrics.upm / self.units_per_em
        count = min(int(snapshot.advance // step), self.max_lines)
        return [
            Mark(
                "line",
                (
                    (index * step, snapshot.metrics.descender),
                    (index * step, snapshot.metrics.ascender),
                ),
                (180, 180, 180),
                0.75,
            )
            for index in range(1, count + 1)
        ]

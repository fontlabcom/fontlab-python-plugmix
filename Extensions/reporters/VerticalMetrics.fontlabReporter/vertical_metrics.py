# this_file: Extensions/reporters/VerticalMetrics.fontlabReporter/vertical_metrics.py
# SPDX-License-Identifier: Apache-2.0
"""Show the five principal horizontal metric lines with labels."""

from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot


class VerticalMetrics(Reporter):
    """Annotate ascender, descender, x-height, cap height and baseline."""

    name = "vertical_metrics"
    title = "Vertical Metrics"
    layer = "background"

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Return one line and one label per named metric."""
        m = snapshot.metrics
        levels = (
            ("Ascender", m.ascender),
            ("Descender", m.descender),
            ("x-height", m.x_height),
            ("Cap height", m.cap_height),
            ("Baseline", 0.0),
        )
        marks = []
        for label, height in levels:
            marks.append(
                Mark("line", ((0, height), (snapshot.advance, height)), (95, 130, 190))
            )
            marks.append(
                Mark(
                    "text",
                    ((snapshot.advance + 8, height),),
                    (95, 130, 190),
                    text=f"{label} {height:g}",
                )
            )
        return marks

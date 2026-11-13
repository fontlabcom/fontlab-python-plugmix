# this_file: Extensions/reporters/CenterLines.fontlabReporter/center_lines.py
# SPDX-License-Identifier: Apache-2.0
"""Show advance and vertical-metric center guides."""

from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot


class CenterLines(Reporter):
    """Draw requested font-wide center lines with no font modification."""

    name = "center_lines"
    title = "Center Lines"
    layer = "background"

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Draw advance/2 and half x-height/cap-height guides."""
        metrics, advance = snapshot.metrics, snapshot.advance
        top, bottom = (
            max(metrics.ascender, metrics.cap_height),
            min(metrics.descender, 0),
        )
        marks = [
            Mark("line", ((advance / 2, bottom), (advance / 2, top)), (95, 130, 190))
        ]
        for height in (metrics.x_height / 2, metrics.cap_height / 2):
            marks.append(Mark("line", ((0, height), (advance, height)), (95, 130, 190)))
        return marks

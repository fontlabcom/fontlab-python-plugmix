# this_file: Extensions/reporters/Rekha.fontlabreporter/rekha.py
# SPDX-License-Identifier: Apache-2.0
"""Draw the head-line bar of Devanagari, Bengali and Gurmukhi letters."""

import unicodedata

from fly.ap.plugins.reporter import Mark, Reporter
from fly.ap.plugins.snapshot import GlyphSnapshot

SCRIPTS = ((0x0900, 0x097F), (0x0980, 0x09FF), (0x0A00, 0x0A7F), (0xA8E0, 0xA8FF))


class Rekha(Reporter):
    """Bar from -overshoot to the advance; `rekha` and `rekha_stop` anchors move it."""

    name = "rekha"
    title = "Rekha Viewer"
    layer = "background"
    height = 700
    thickness = 100
    overshoot = 20
    # upstream uses the system placeholder-text colour
    shade: tuple[int, int, int, int] = (0, 0, 0, 64)

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Letters only; suffixed or interrupted anchors are not supported."""
        identity = snapshot.identity
        if identity is None or not identity.unicodes:
            return []
        code = identity.unicodes[0]
        if not any(lo <= code <= hi for lo, hi in SCRIPTS):
            return []
        if not unicodedata.category(chr(code)).startswith("L"):
            return []
        at = {a.name: a.x for a in snapshot.anchors}
        start = at.get("rekha", -self.overshoot)
        bars = [(start, snapshot.advance + self.overshoot)]
        if "rekha_stop" in at:
            bars.append((-self.overshoot, at["rekha_stop"]))
        y0, y1 = self.height, self.height + self.thickness
        return [
            Mark("polygon", ((x0, y0), (x1, y0), (x1, y1), (x0, y1)), fill=self.shade)
            for x0, x1 in bars
            if x1 > x0
        ]

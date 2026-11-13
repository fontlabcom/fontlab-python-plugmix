# this_file: Extensions/reporters/GlobalGlyph.fontlabReporter/global_glyph.py
# SPDX-License-Identifier: Apache-2.0
"""Show the outlines of a helper glyph named ``_global`` behind every other glyph."""

from fly.ap.glyphs.identity import Identity
from fly.ap.plugins.geometry import flatten
from fly.ap.plugins.reporter import Mark, Reporter, fill_mark
from fly.ap.plugins.snapshot import GlyphSnapshot, KerningGroups


class GlobalGlyph(Reporter):
    """Closed paths orange, open paths blue, both with a faint fill; components not read."""

    name = "global_glyph"
    title = "Show Global Glyph"
    layer = "background"
    glyph_name = "_global"
    closed_color: tuple[int, int, int] = (255, 179, 51)
    open_color: tuple[int, int, int] = (0, 0, 255)
    fill_alpha = 26
    stroke_px = 1.0

    def requested_glyphs(
        self, identity: Identity, kerning_groups: KerningGroups | None = None
    ) -> tuple[str, ...]:
        """Ask for the helper glyph, except while it is the glyph being shown."""
        return () if identity.name == self.glyph_name else (self.glyph_name,)

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """No identity, the helper itself, or an absent helper glyph draws nothing."""
        identity = snapshot.identity
        if identity is None or identity.name == self.glyph_name:
            return []
        contours = snapshot.others.get(self.glyph_name, ())
        closed = tuple(c for c in contours if c.closed)
        fills, lines = [], []
        if mark := fill_mark(closed, (*self.closed_color, self.fill_alpha)):
            fills.append(mark)
        for contour in contours:
            points = flatten(contour)
            if len(points) < 2:
                continue
            if contour.closed:
                lines.append(
                    Mark(
                        "polyline",
                        (*points, points[0]),
                        self.closed_color,
                        self.stroke_px,
                    )
                )
                continue
            if len(points) >= 3:
                fills.append(
                    Mark("polygon", points, fill=(*self.open_color, self.fill_alpha))
                )
            lines.append(Mark("polyline", points, self.open_color, self.stroke_px))
        return fills + lines

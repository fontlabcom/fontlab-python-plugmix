# this_file: Extensions/reporters/KerningGroupReference.fontlabreporter/kerning_group_reference.py
# SPDX-License-Identifier: Apache-2.0
"""Show small silhouettes of the glyph's kerning-group members beside it."""

from dataclasses import replace
from itertools import chain, zip_longest

from fly.ap.glyphs.identity import Identity
from fly.ap.plugins.reporter import Mark, Reporter, fill_mark
from fly.ap.plugins.snapshot import GlyphSnapshot, KerningGroups


class KerningGroupReference(Reporter):
    """Members of each class overlap at one spot per side; LTR only."""

    name = "kerning_group_reference"
    title = "Show Kerning Group Reference"
    layer = "background"
    needs_kerning = True
    scale = 0.2
    clearance = 150  # between the glyph (0 / advance) and the silhouettes
    color: tuple[int, int, int] = (0, 128, 128)
    total_opacity = 0.8  # divided by the class size, so crowded classes read denser
    min_opacity = 0.04

    @staticmethod
    def _sides(
        identity: Identity, groups: KerningGroups | None
    ) -> tuple[tuple[str, ...], tuple[str, ...]]:
        """Members of the left and right classes, without the glyph itself."""
        if groups is None:
            return (), ()

        def pick(cls: str | None) -> tuple[str, ...]:
            return tuple(n for n in groups.members.get(cls, ()) if n != identity.name)

        return pick(groups.left), pick(groups.right)

    def requested_glyphs(
        self, identity: Identity, kerning_groups: KerningGroups | None = None
    ) -> tuple[str, ...]:
        """Other members of both classes, interleaved so the cap keeps both sides."""
        left, right = self._sides(identity, kerning_groups)
        pairs = zip_longest(left, right)
        return tuple(n for n in chain.from_iterable(pairs) if n is not None)

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """No identity or groups, or members without outlines, draw nothing."""
        groups = snapshot.kerning_groups
        if snapshot.identity is None or groups is None:
            return []
        left, right = self._sides(snapshot.identity, groups)
        mid_y = snapshot.metrics.x_height / 2
        marks = []
        for names, cls, edge, left_side in (
            (left, groups.left, -self.clearance, True),
            (right, groups.right, snapshot.advance + self.clearance, False),
        ):
            # Class size includes the glyph itself.
            count = len(groups.members.get(cls, ())) or 1
            alpha = round(255 * max(self.min_opacity, self.total_opacity / count))
            for name in names:
                mark = fill_mark(snapshot.others.get(name, ()), (*self.color, alpha))
                if mark is None:
                    continue
                points = tuple((x * self.scale, y * self.scale) for x, y in mark.points)
                xs = [p[0] for p in points]
                dx = edge - (max(xs) if left_side else min(xs))
                # Baseline of the scaled outline sits at half x-height.
                shifted = tuple((x + dx, y + mid_y) for x, y in points)
                marks.append(replace(mark, points=shifted))
        return marks

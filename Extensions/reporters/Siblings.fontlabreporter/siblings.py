# this_file: Extensions/reporters/Siblings.fontlabreporter/siblings.py
# SPDX-License-Identifier: Apache-2.0
"""Superimpose look-alike Latin letters behind the glyph to compare construction."""

from fly.ap.glyphs.identity import Identity
from fly.ap.plugins.reporter import Mark, Reporter, fill_mark
from fly.ap.plugins.snapshot import GlyphSnapshot, KerningGroups


class Siblings(Reporter):
    """Each present sibling is one green polygon at the glyph origin; Latin only."""

    name = "siblings"
    title = "Show Siblings"
    layer = "background"
    groups: tuple[tuple[str, ...], ...] = (
        ("c", "e", "o"),
        ("b", "p"),
        ("d", "q", "u"),
        ("h", "l", "n", "r", "a"),
    )
    color: tuple[int, int, int] = (38, 102, 64)
    total_opacity = 0.4  # shared by the group, so larger groups are fainter

    def _group(self, name: str) -> tuple[str, ...]:
        """The group holding ``name``, or an empty tuple."""
        return next((g for g in self.groups if name in g), ())

    def requested_glyphs(
        self, identity: Identity, kerning_groups: KerningGroups | None = None
    ) -> tuple[str, ...]:
        """The other members of the glyph's group."""
        return tuple(n for n in self._group(identity.name) if n != identity.name)

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """No identity, no group or no present sibling draws nothing."""
        identity = snapshot.identity
        group = self._group(identity.name) if identity else ()
        alpha = round(255 * self.total_opacity / len(group)) if group else 0
        marks = []
        for name in group:
            if name == identity.name:
                continue
            if mark := fill_mark(snapshot.others.get(name, ()), (*self.color, alpha)):
                marks.append(mark)
        return marks

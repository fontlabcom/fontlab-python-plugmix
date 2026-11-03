# this_file: src/fontlab_plugmix/palette.py
"""Qt-free contract for dockable palettes."""

from typing import ClassVar, Literal

from .plugin import Plugin
from .snapshot import GlyphSnapshot


class Palette(Plugin):
    """Build controls once, refresh on active glyph changes, release on close."""

    kind = "palette"
    area: ClassVar[Literal["left", "right", "top", "bottom"]] = "right"

    def build(self, ui: object) -> None:
        """Create controls through a host-provided UI facade."""
        raise NotImplementedError

    def refresh(self, context: GlyphSnapshot | None) -> None:
        """React to a new active glyph, master, revision or selection."""

    def close(self) -> None:
        """Release plugin-owned resources when the panel closes."""

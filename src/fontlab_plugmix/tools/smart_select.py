# SPDX-License-Identifier: Apache-2.0
# this_file: src/fontlab_plugmix/tools/smart_select.py
"""Drag a rectangle to select whole contours touched by their nodes.

Selection-only cut from But Ko's Smart Select Tool: no double-click contour
containment, no native node movement and no geometry edits.
"""

from fontlab_plugmix.reporter import Mark
from fontlab_plugmix.snapshot import GlyphSnapshot
from fontlab_plugmix.tool import Tool, ToolContext, ToolEvent


def touched_contours(
    glyph: GlyphSnapshot, first: tuple[float, float], last: tuple[float, float]
) -> tuple[int, ...]:
    """Return contours with any node inside the inclusive drag rectangle."""
    left, right = sorted((first[0], last[0]))
    bottom, top = sorted((first[1], last[1]))
    return tuple(
        index
        for index, contour in enumerate(glyph.contours)
        if any(
            left <= node.x <= right and bottom <= node.y <= top
            for node in contour.nodes
        )
    )


class SmartSelect(Tool):
    """Emphasise a drag rectangle and select whole contours on release."""

    name = "smart_select"
    title = "Smart Select"

    def __init__(self) -> None:
        self.ctx: ToolContext | None = None
        self.origin: tuple[float, float] | None = None
        self.end: tuple[float, float] | None = None

    def activate(self, ctx: ToolContext) -> None:
        self.ctx = ctx
        self.origin = self.end = None

    def deactivate(self) -> None:
        self.origin = self.end = None
        self.ctx = None

    def press(self, event: ToolEvent) -> bool:
        self.origin = self.end = (event.x, event.y)
        return True

    def move(self, event: ToolEvent) -> bool:
        if self.origin is None or not event.buttons:
            return False
        self.end = event.x, event.y
        self.ctx.redraw()
        return True

    def release(self, event: ToolEvent) -> bool:
        if self.origin is None:
            return False
        start, self.end = self.origin, (event.x, event.y)
        self.origin = None
        glyph = self.ctx.snapshot()
        if glyph is not None:
            self.ctx.select(
                touched_contours(glyph, start, self.end), toggle=event.shift
            )
        return True

    def marks(self, glyph: GlyphSnapshot | None) -> list[Mark]:
        if self.origin is None or self.end is None:
            return []
        x1, y1 = self.origin
        x2, y2 = self.end
        return [Mark("polyline", ((x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)))]

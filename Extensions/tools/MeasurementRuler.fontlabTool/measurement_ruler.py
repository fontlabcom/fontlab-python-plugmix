# SPDX-License-Identifier: Apache-2.0
# this_file: Extensions/tools/MeasurementRuler.fontlabTool/measurement_ruler.py
"""Drag a point-to-point ruler; Shift constrains an axis, Escape clears it.

Measures font units and counterclockwise angle from +x, not ink intersections.
"""

from math import atan2, degrees, hypot

from fly.ap.plugins.reporter import Mark
from fly.ap.plugins.snapshot import GlyphSnapshot
from fly.ap.plugins.tool import Tool, ToolContext, ToolEvent

Point = tuple[float, float]


def endpoint(origin: Point, event: ToolEvent) -> Point:
    """Constrain to the nearer horizontal or vertical axis when Shift is held."""
    if not event.shift:
        return event.x, event.y
    if abs(event.x - origin[0]) >= abs(event.y - origin[1]):
        return event.x, origin[1]
    return origin[0], event.y


def measurement_marks(first: Point, last: Point) -> list[Mark]:
    """Draw the ruler with signed deltas, length and angle in font coordinates."""
    dx, dy = last[0] - first[0], last[1] - first[1]
    label = f"{hypot(dx, dy):.2f} u  dx {dx:.2f}  dy {dy:.2f}  {degrees(atan2(dy, dx)):.2f}°"
    return [Mark("line", (first, last)), Mark("text", (last,), text=label)]


class MeasurementRuler(Tool):
    """Retain one ruler until a new drag, Escape or active glyph change."""

    name = "measurement_ruler"
    title = "Measurement Ruler"

    def __init__(self) -> None:
        self.ctx: ToolContext | None = None
        self.origin: Point | None = None
        self.end: Point | None = None
        self.source_key = None
        self.dragging = False

    def activate(self, ctx: ToolContext) -> None:
        self.deactivate()
        self.ctx = ctx

    def deactivate(self) -> None:
        self.ctx = None
        self.origin = self.end = None
        self.source_key = None
        self.dragging = False

    def press(self, event: ToolEvent) -> bool:
        if self.ctx is None or event.buttons != 1:
            return False
        glyph = self.ctx.snapshot()
        if glyph is None:
            return False
        self.source_key = glyph.source_key
        self.origin = self.end = (event.x, event.y)
        self.dragging = True
        self.ctx.redraw()
        return True

    def move(self, event: ToolEvent) -> bool:
        if not self.dragging or event.buttons != 1:
            return False
        if not self.marks(self.ctx.snapshot()):
            return False
        self.end = endpoint(self.origin, event)
        self.ctx.redraw()
        return True

    def release(self, event: ToolEvent) -> bool:
        if event.buttons & 1 or not self.dragging or not self.marks(self.ctx.snapshot()):
            return False
        self.end = endpoint(self.origin, event)
        self.dragging = False
        self.ctx.redraw()
        return True

    def key_down(self, event: ToolEvent) -> bool:
        if event.key != "\x1b" or self.ctx is None:
            return False
        self.origin = self.end = None
        self.dragging = False
        self.ctx.redraw()
        return True

    def marks(self, glyph: GlyphSnapshot | None) -> list[Mark]:
        if glyph is None or glyph.source_key != self.source_key:
            self.origin = self.end = None
            self.dragging = False
        if self.origin is None or self.end is None:
            return []
        return measurement_marks(self.origin, self.end)

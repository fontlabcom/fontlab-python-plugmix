# SPDX-License-Identifier: Apache-2.0
# this_file: Extensions/tools/ContourPicker.fontlabTool/contour_picker.py
"""Click within 12 pixels of a local node to select its contour; Shift toggles.

Component nodes are excluded: their decomposed indices cannot address local
contours. Both on- and off-curve nodes of open and closed contours are pickable.
"""

from math import hypot, isfinite

from fontlabapp.plugins.snapshot import GlyphSnapshot
from fontlabapp.plugins.tool import Tool, ToolContext, ToolEvent

RADIUS_PX = 12


def nearest_contour(
    glyph: GlyphSnapshot, point: tuple[float, float], scale: float
) -> int | None:
    """Return the closest local node's contour; ties prefer contour order."""
    if not isfinite(scale) or scale <= 0:
        return None
    best, distance = None, RADIUS_PX / scale
    for index, contour in enumerate(glyph.contours):
        for node in contour.nodes:
            delta = hypot(node.x - point[0], node.y - point[1])
            if delta <= distance and (best is None or delta < distance):
                best, distance = index, delta
    return best


class ContourPicker(Tool):
    """Select one whole local contour without changing geometry or history."""

    name = "contour_picker"
    title = "Contour Picker"

    def __init__(self) -> None:
        self.ctx: ToolContext | None = None

    def activate(self, ctx: ToolContext) -> None:
        self.ctx = ctx

    def deactivate(self) -> None:
        self.ctx = None

    def press(self, event: ToolEvent) -> bool:
        if self.ctx is None or event.buttons != 1:
            return False
        glyph = self.ctx.snapshot()
        if glyph is None:
            return False
        index = nearest_contour(glyph, (event.x, event.y), event.scale)
        if index is None:
            return False
        self.ctx.select((index,), toggle=event.shift)
        return True

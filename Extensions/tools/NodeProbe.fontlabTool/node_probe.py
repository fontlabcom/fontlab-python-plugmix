# SPDX-License-Identifier: Apache-2.0
# this_file: Extensions/tools/NodeProbe.fontlabTool/node_probe.py
"""Hover within 12 pixels of a node to inspect coordinates and provenance."""

from math import hypot, isfinite

from fly.ap.plugins.reporter import Mark
from fly.ap.plugins.snapshot import GlyphSnapshot, Node
from fly.ap.plugins.tool import Tool, ToolContext, ToolEvent

RADIUS_PX = 12


def nearest_node(
    glyph: GlyphSnapshot, point: tuple[float, float], scale: float
) -> tuple[str, Node] | None:
    """Find a local or decomposed component node; ties prefer local order."""
    if not isfinite(scale) or scale <= 0:
        return None
    groups = [("local", glyph.contours)] + [
        (f"component {index} {component.base}", component.contours)
        for index, component in enumerate(glyph.components)
    ]
    best, distance = None, RADIUS_PX / scale
    for label, contours in groups:
        for ci, contour in enumerate(contours):
            for ni, node in enumerate(contour.nodes):
                delta = hypot(node.x - point[0], node.y - point[1])
                if delta <= distance and (best is None or delta < distance):
                    best, distance = (f"{label} {ci}:{ni}", node), delta
    return best


class NodeProbe(Tool):
    """Read exact node coordinates without selecting or editing any outline."""

    name = "node_probe"
    title = "Node Probe"
    needs_components = True

    def __init__(self) -> None:
        self.ctx: ToolContext | None = None
        self.event: ToolEvent | None = None
        self.source_key = None

    def activate(self, ctx: ToolContext) -> None:
        self.deactivate()
        self.ctx = ctx

    def deactivate(self) -> None:
        self.ctx = None
        self.event = None
        self.source_key = None

    def move(self, event: ToolEvent) -> bool:
        if self.ctx is None:
            return False
        glyph = self.ctx.snapshot()
        self.event = event if glyph is not None else None
        if glyph is None:
            return False
        self.source_key = glyph.source_key
        self.ctx.redraw()
        return True

    def marks(self, glyph: GlyphSnapshot | None) -> list[Mark]:
        if glyph is None or glyph.source_key != self.source_key:
            self.event = None
        if self.event is None:
            return []
        hit = nearest_node(glyph, (self.event.x, self.event.y), self.event.scale)
        if hit is None:
            return []
        label, node = hit
        kind = "on-curve" if node.on_curve else "off-curve"
        point = (node.x, node.y)
        return [
            Mark("ring", (point,), diameter_px=12),
            Mark("text", (point,), text=f"{label} {kind}: {node.x:.2f}, {node.y:.2f}"),
        ]

# this_file: src/fontlab_plugmix/plugins/only_selected_handles.py
# SPDX-License-Identifier: Apache-2.0
"""Emphasise handles of the selection over FontLab's native handle drawing."""

from fontlab_plugmix.geometry import neighbours
from fontlab_plugmix.reporter import Mark, Reporter
from fontlab_plugmix.snapshot import GlyphSnapshot, Node


def _marks(near: Node, handle: Node) -> list[Mark]:
    """Accent one selected handle relationship."""
    color = (55, 145, 220)
    return [
        Mark("line", ((near.x, near.y), (handle.x, handle.y)), color, 1.5),
        Mark("ring", ((handle.x, handle.y),), color, diameter_px=11),
    ]


class OnlySelectedHandles(Reporter):
    """Connect selected endpoints to their neighbouring off-curves."""

    name = "only_selected_handles"
    title = "Emphasise Selected Handles"

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Overlay an accent line and ring for each relevant handle."""
        marks = []
        for contour in snapshot.contours:
            nodes = contour.nodes
            for index, handle in enumerate(nodes):
                if handle.on_curve or len(nodes) < 2:
                    continue
                for near in neighbours(contour, index):
                    if near is not None and near.on_curve:
                        if near.selected or handle.selected:
                            marks.extend(_marks(near, handle))
                        break
        return marks

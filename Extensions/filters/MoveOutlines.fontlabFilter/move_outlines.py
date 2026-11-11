# this_file: Extensions/filters/MoveOutlines.fontlabFilter/move_outlines.py
# SPDX-License-Identifier: Apache-2.0
"""Translate own outlines; anchors, components and advance stay fixed."""

from collections.abc import Mapping
from dataclasses import replace
from math import isfinite
from typing import Any

from fontlabapp.plugins.filter import Filter, LayerEdit, Param
from fontlabapp.plugins.snapshot import GlyphSnapshot, Node


class MoveOutlines(Filter):
    """Translate own outlines; anchors, components and advance stay fixed."""

    name = "move_outlines"
    title = "Move Outlines"
    params = (
        Param("dx", "X offset", "float", 0.0),
        Param("dy", "Y offset", "float", 0.0),
    )

    def compute(self, snapshot: GlyphSnapshot, values: Mapping[str, Any]) -> LayerEdit:
        """Change coordinates only, retaining contour topology and node metadata."""
        values = self.validate(values)
        dx, dy = values["dx"], values["dy"]

        def mapped(node: Node) -> Node:
            if not (isfinite(node.x) and isfinite(node.y)):
                raise ValueError("Outline coordinates must be finite")
            x, y = node.x + dx, node.y + dy
            if not (isfinite(x) and isfinite(y)):
                raise ValueError("Outline coordinate overflow")
            return replace(node, x=x, y=y)

        contours = tuple(
            replace(contour, nodes=tuple(mapped(node) for node in contour.nodes))
            for contour in snapshot.contours
        )
        return LayerEdit(contours=contours if contours != snapshot.contours else None)

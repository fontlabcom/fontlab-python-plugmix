# this_file: Extensions/filters/SlantOutlines.fontlabFilter/slant_outlines.py
# SPDX-License-Identifier: Apache-2.0
"""Apply geometric rightward slant above a Y pivot, without optical correction."""

from collections.abc import Mapping
from dataclasses import replace
from math import isfinite, radians, tan
from typing import Any

from fontlabapp.plugins.filter import Filter, LayerEdit, Param
from fontlabapp.plugins.snapshot import GlyphSnapshot, Node


class SlantOutlines(Filter):
    """Apply geometric rightward slant above a Y pivot, without optical correction."""

    name = "slant_outlines"
    title = "Slant Outlines"
    params = (
        Param("angle", "Rightward angle (degrees)", "float", 0.0, minimum=-85.0, maximum=85.0),
        Param("pivot_y", "Pivot Y", "float", 0.0),
    )

    def compute(self, snapshot: GlyphSnapshot, values: Mapping[str, Any]) -> LayerEdit:
        """Change coordinates only, retaining contour topology and node metadata."""
        values = self.validate(values)
        shear, pivot = tan(radians(values["angle"])), values["pivot_y"]

        def mapped(node: Node) -> Node:
            if not (isfinite(node.x) and isfinite(node.y)):
                raise ValueError("Outline coordinates must be finite")
            x = node.x if shear == 0 else node.x + (node.y - pivot) * shear
            y = node.y
            if not (isfinite(x) and isfinite(y)):
                raise ValueError("Outline coordinate overflow")
            return replace(node, x=x, y=y)

        contours = tuple(
            replace(contour, nodes=tuple(mapped(node) for node in contour.nodes))
            for contour in snapshot.contours
        )
        return LayerEdit(contours=contours if contours != snapshot.contours else None)

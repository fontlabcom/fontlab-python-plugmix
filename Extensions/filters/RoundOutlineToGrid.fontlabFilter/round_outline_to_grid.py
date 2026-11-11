# this_file: Extensions/filters/RoundOutlineToGrid.fontlabFilter/round_outline_to_grid.py
# SPDX-License-Identifier: Apache-2.0
"""Round own outline nodes to a grid; half steps go toward positive infinity."""

from collections.abc import Mapping
from dataclasses import replace
from math import floor, isfinite
from typing import Any

from fontlabapp.plugins.filter import Filter, LayerEdit, Param
from fontlabapp.plugins.snapshot import GlyphSnapshot, Node


class RoundOutlineToGrid(Filter):
    """Round own outline nodes to a grid; half steps go toward positive infinity."""

    name = "round_outline_to_grid"
    title = "Round Outline to Grid"
    params = (
        Param("grid", "Grid spacing", "float", 1.0, minimum=0.000001),
    )

    def compute(self, snapshot: GlyphSnapshot, values: Mapping[str, Any]) -> LayerEdit:
        """Change coordinates only, retaining contour topology and node metadata."""
        values = self.validate(values)
        grid = values["grid"]

        def mapped(node: Node) -> Node:
            if not (isfinite(node.x) and isfinite(node.y)):
                raise ValueError("Outline coordinates must be finite")
            try:
                x, y = floor(node.x / grid + 0.5) * grid, floor(node.y / grid + 0.5) * grid
            except (OverflowError, ValueError) as error:
                raise ValueError("Outline coordinate overflow") from error
            if not (isfinite(x) and isfinite(y)):
                raise ValueError("Outline coordinate overflow")
            return replace(node, x=x, y=y)

        contours = tuple(
            replace(contour, nodes=tuple(mapped(node) for node in contour.nodes))
            for contour in snapshot.contours
        )
        return LayerEdit(contours=contours if contours != snapshot.contours else None)

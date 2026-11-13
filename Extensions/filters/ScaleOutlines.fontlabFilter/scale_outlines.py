# this_file: Extensions/filters/ScaleOutlines.fontlabFilter/scale_outlines.py
# SPDX-License-Identifier: Apache-2.0
"""Scale own outlines about a chosen pivot; metrics and components stay fixed."""

from collections.abc import Mapping
from dataclasses import replace
from math import isfinite
from typing import Any

from fly.ap.plugins.filter import Filter, LayerEdit, Param
from fly.ap.plugins.snapshot import GlyphSnapshot, Node


class ScaleOutlines(Filter):
    """Scale own outlines about a chosen pivot; metrics and components stay fixed."""

    name = "scale_outlines"
    title = "Scale Outlines"
    params = (
        Param("x_percent", "X scale (%)", "float", 100.0, minimum=0.001),
        Param("y_percent", "Y scale (%)", "float", 100.0, minimum=0.001),
        Param("pivot_x", "Pivot X", "float", 0.0),
        Param("pivot_y", "Pivot Y", "float", 0.0),
    )

    def compute(self, snapshot: GlyphSnapshot, values: Mapping[str, Any]) -> LayerEdit:
        """Change coordinates only, retaining contour topology and node metadata."""
        values = self.validate(values)
        sx, sy = values["x_percent"] / 100, values["y_percent"] / 100
        px, py = values["pivot_x"], values["pivot_y"]

        def mapped(node: Node) -> Node:
            if not (isfinite(node.x) and isfinite(node.y)):
                raise ValueError("Outline coordinates must be finite")
            x = node.x if sx == 1 else px + (node.x - px) * sx
            y = node.y if sy == 1 else py + (node.y - py) * sy
            if not (isfinite(x) and isfinite(y)):
                raise ValueError("Outline coordinate overflow")
            return replace(node, x=x, y=y)

        contours = tuple(
            replace(contour, nodes=tuple(mapped(node) for node in contour.nodes))
            for contour in snapshot.contours
        )
        return LayerEdit(contours=contours if contours != snapshot.contours else None)

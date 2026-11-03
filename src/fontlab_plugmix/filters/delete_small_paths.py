# this_file: src/fontlab_plugmix/filters/delete_small_paths.py
# SPDX-License-Identifier: Apache-2.0
"""Remove closed contours whose polygon area or bounding area is small."""

from collections.abc import Mapping
from itertools import pairwise
from typing import Any

from fontlab_plugmix.filter import Filter, LayerEdit, Param
from fontlab_plugmix.snapshot import Contour, GlyphSnapshot


def _small(contour: Contour, threshold: float) -> bool:
    """Estimate closed-path size using node polygon and its bounds."""
    if not contour.closed or len(contour.nodes) < 3:
        return False
    points = tuple((node.x, node.y) for node in contour.nodes)
    area = (
        abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in pairwise((*points, points[0]))))
        / 2
    )
    xs, ys = zip(*points, strict=True)
    bounds_area = (max(xs) - min(xs)) * (max(ys) - min(ys))
    return area < threshold or bounds_area < threshold


class DeleteSmallPaths(Filter):
    """Drop closed contours smaller than the supplied area threshold."""

    name = "delete_small_paths"
    title = "Delete Small Paths"
    params = (Param("threshold", "Maximum area", "float", 400.0, minimum=0.0),)

    def compute(self, snapshot: GlyphSnapshot, values: Mapping[str, Any]) -> LayerEdit:
        """Keep open paths and contours at or above the threshold."""
        threshold = self.validate(values)["threshold"]
        kept = tuple(c for c in snapshot.contours if not _small(c, threshold))
        return LayerEdit(contours=kept if len(kept) != len(snapshot.contours) else None)

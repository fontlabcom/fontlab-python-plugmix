# this_file: Extensions/filters/DeleteSmallPaths.fontlabfilter/delete_small_paths.py
# SPDX-License-Identifier: Apache-2.0
"""Remove closed contours whose flattened area or bounds are small."""

from collections.abc import Mapping
from itertools import pairwise
from typing import Any

from fly.ap.plugins.filter import Filter, LayerEdit, Param
from fly.ap.plugins.geometry import point_at, segments
from fly.ap.plugins.snapshot import Contour, GlyphSnapshot

FLATTEN_STEPS = 25


def _path_points(contour: Contour) -> tuple[tuple[float, float], ...] | None:
    """Flatten each supported segment; None means an unsupported control run."""
    runs = segments(contour)
    if len(runs) != sum(node.on_curve for node in contour.nodes):
        return None
    points = []
    for run in runs:
        count = 1 if len(run) == 2 else FLATTEN_STEPS
        points.extend(point_at(run, index / count) for index in range(1, count + 1))
    return tuple(points)


def _small(contour: Contour, threshold: float) -> bool:
    """Measure flattened ink area and bounds, excluding Bézier controls."""
    if not contour.closed:
        return False
    if len(contour.nodes) < 3:
        return threshold > 0
    points = _path_points(contour)
    if not points:
        return False
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

# this_file: src/fontlab_plugmix/geometry.py
# SPDX-License-Identifier: Apache-2.0
"""Small pure contour-segment operations shared by reporter computations."""

from itertools import pairwise
from math import comb, hypot

from .snapshot import Contour, Node


def segments(contour: Contour) -> tuple[tuple[Node, ...], ...]:
    """Split lines, quadratic and cubic segments; skip longer control runs."""
    nodes = contour.nodes
    on = [index for index, node in enumerate(nodes) if node.on_curve]
    if len(on) < 2:
        return ()
    pairs = list(pairwise(on))
    if contour.closed:
        pairs.append((on[-1], on[0]))
    rows = []
    for start, end in pairs:
        row = (
            nodes[start : end + 1] if end > start else nodes[start:] + nodes[: end + 1]
        )
        # Three or more off-curves may imply TrueType on-curves. Without curve
        # type in the snapshot, skip that run rather than mismeasure a segment.
        if len(row) in (2, 3, 4):
            rows.append(row)
    return tuple(rows)


def neighbours(contour: Contour, index: int) -> tuple[Node | None, Node | None]:
    """Return neighbours without wrapping the ends of an open contour."""
    nodes = contour.nodes
    before = nodes[index - 1] if index else (nodes[-1] if contour.closed else None)
    after = (
        nodes[index + 1]
        if index + 1 < len(nodes)
        else (nodes[0] if contour.closed else None)
    )
    return before, after


def point_at(segment: tuple[Node, ...], t: float) -> tuple[float, float]:
    """Evaluate a line, quadratic or cubic segment at fractional position t."""
    n = len(segment) - 1
    weights = tuple(comb(n, i) * (1 - t) ** (n - i) * t**i for i in range(n + 1))
    return (
        sum(node.x * weight for node, weight in zip(segment, weights, strict=True)),
        sum(node.y * weight for node, weight in zip(segment, weights, strict=True)),
    )


def length(segment: tuple[Node, ...], steps: int = 25) -> float:
    """Measure a line exactly and a Bézier by uniform flattening."""
    if len(segment) == 2:
        start, end = segment
        return hypot(end.x - start.x, end.y - start.y)
    previous, total = (segment[0].x, segment[0].y), 0.0
    for index in range(1, steps + 1):
        current = point_at(segment, index / steps)
        total += hypot(current[0] - previous[0], current[1] - previous[1])
        previous = current
    return total

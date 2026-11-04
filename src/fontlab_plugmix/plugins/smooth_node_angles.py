# this_file: src/fontlab_plugmix/plugins/smooth_node_angles.py
# SPDX-License-Identifier: Apache-2.0
"""Label smooth-node handle kinks and incoming/outgoing length proportion."""

from math import acos, degrees, hypot

from fontlab_plugmix.geometry import neighbours
from fontlab_plugmix.reporter import Mark, Reporter
from fontlab_plugmix.snapshot import GlyphSnapshot, Node


def _label(node: Node, before: Node, after: Node) -> str | None:
    """Return the angular mismatch and handle-length ratio for one node."""
    ax, ay = before.x - node.x, before.y - node.y
    bx, by = after.x - node.x, after.y - node.y
    a, b = hypot(ax, ay), hypot(bx, by)
    if not a or not b:
        return None
    cosine = max(-1.0, min(1.0, (ax * bx + ay * by) / (a * b)))
    kink = 180.0 - degrees(acos(cosine))
    return f"{kink:.1f}° · {a / b:.2f}"


class SmoothNodeAngles(Reporter):
    """Show local smoothness and proportion for nodes with two handles."""

    name = "smooth_node_angles"
    title = "Smooth Node Angles"

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Label each smooth on-curve flanked by off-curve handles."""
        marks = []
        for contour in snapshot.contours:
            nodes = contour.nodes
            for index, node in enumerate(nodes):
                if not node.on_curve or not node.smooth or len(nodes) < 3:
                    continue
                before, after = neighbours(contour, index)
                if before is None or after is None or before.on_curve or after.on_curve:
                    continue
                label = _label(node, before, after)
                if label is not None:
                    marks.append(
                        Mark(
                            "text",
                            ((node.x + 8, node.y + 8),),
                            (180, 65, 150),
                            text=label,
                        )
                    )
        return marks

# this_file: Extensions/reporters/ShowInterpolation.fontlabreporter/show_interpolation.py
# SPDX-License-Identifier: Apache-2.0
"""Fill the halfway blend between the shown layer and each other master behind it."""

from fly.ap.plugins.reporter import Mark, Reporter, fill_mark
from fly.ap.plugins.snapshot import Contour, GlyphSnapshot, Node


def _coords(contours: tuple[Contour, ...]) -> list[list[tuple[float, float, bool]]]:
    """Node coordinates and on-curve flags, ignoring selection."""
    return [[(n.x, n.y, n.on_curve) for n in c.nodes] for c in contours]


def _lerp(a: Contour, b: Contour, t: float) -> Contour:
    """Blend corresponding nodes; keep ``a``'s node kinds and open/closed state."""
    nodes = tuple(
        Node(p.x + (q.x - p.x) * t, p.y + (q.y - p.y) * t, p.on_curve, False)
        for p, q in zip(a.nodes, b.nodes, strict=False)
    )
    return Contour(nodes, a.closed)


class ShowInterpolation(Reporter):
    """One odd-even polygon per compatible master; no instances, no recentering."""

    name = "show_interpolation"
    title = "Show Interpolation"
    layer = "background"
    needs_masters = True
    # Upstream default RGB 0.4, 0.0, 0.3, rounded half-up (0.3 * 255 = 76.5 -> 77,
    # not Python's round-half-even 76), as in Show Background; upstream alpha
    # 0.15 is replaced by the plan's 64.
    color: tuple[int, int, int] = (102, 0, 77)
    alpha = 64
    factor = 0.5

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Incompatible masters and masters drawn exactly like the shown one are skipped."""
        shown = _coords(snapshot.contours)
        marks = []
        for master in snapshot.masters:
            if not master.compatible or _coords(master.contours) == shown:
                continue
            contours = tuple(
                _lerp(a, b, self.factor)
                for a, b in zip(snapshot.contours, master.contours, strict=False)
            )
            if mark := fill_mark(contours, (*self.color, self.alpha)):
                marks.append(mark)
        return marks

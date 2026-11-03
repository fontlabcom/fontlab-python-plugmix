# this_file: src/fontlab_plugmix/reporter.py
"""Pure mark protocol and guarded rendering through backend contexts."""

from collections.abc import Callable
from dataclasses import dataclass
from itertools import pairwise
from typing import Any, Literal

from .plugin import Plugin
from .snapshot import GlyphSnapshot

Point = tuple[float, float]
Color = tuple[int, int, int]
Kind = Literal["ring", "line", "text", "polyline", "polygon"]


@dataclass(frozen=True)
class Mark:
    """Glyph-unit points with pixel-sized stroke, text and ring diameter."""

    kind: Kind
    points: tuple[Point, ...]
    color: Color = (220, 50, 45)
    stroke_px: float = 1.5
    text: str = ""
    text_px: int = 12
    diameter_px: float = 16.0
    fill: tuple[int, int, int, int] | None = None


def _view_point(context: Any, qt: Any, point: Point) -> Any:
    """Map glyph units through both native transforms into view pixels."""
    native = qt.QtCore.QPointF(*point)
    return context.canvas_to_view.map(context.glyph_to_canvas.map(native))


def _draw(mark: Mark, context: Any, qt: Any) -> None:
    """Draw one mark without changing the context's world transform."""
    painter = context.painter
    if mark.kind == "polygon" and len(mark.points) < 3:
        return
    points = tuple(_view_point(context, qt, p) for p in mark.points)
    if mark.kind == "polygon":
        if mark.fill is None:
            raise ValueError("Polygon mark needs an RGBA fill")
        painter.setPen(qt.QtCore.Qt.NoPen)
        painter.setBrush(qt.QtGui.QColor(*mark.fill))
        try:
            painter.drawPolygon(qt.QtGui.QPolygonF(list(points)))
        finally:
            painter.setBrush(qt.QtGui.QBrush())
            painter.setPen(qt.QtGui.QPen())
        return
    pen = qt.QtGui.QPen(qt.QtGui.QColor(*mark.color))
    pen.setWidthF(mark.stroke_px)
    painter.setPen(pen)
    if mark.kind == "ring":
        painter.setBrush(qt.QtGui.QBrush())
        p, radius = points[0], mark.diameter_px / 2
        painter.drawEllipse(
            qt.QtCore.QRectF(p.x() - radius, p.y() - radius, radius * 2, radius * 2)
        )
    elif mark.kind == "text":
        font = qt.QtGui.QFont()
        font.setPixelSize(mark.text_px)
        painter.setFont(font)
        painter.drawText(points[0], mark.text)
    elif mark.kind in {"line", "polyline"}:
        for start, end in pairwise(points):
            painter.drawLine(start, end)
    else:
        raise ValueError(f"Unknown mark kind: {mark.kind}")


def render_marks(marks: list[Mark], context: Any, qt: Any) -> None:
    """Paint marks in view coordinates, preserving view-pixel widths."""
    for mark in marks:
        _draw(mark, context, qt)


class Reporter(Plugin):
    """Subclass with a name, title and pure ``compute(snapshot)`` method."""

    name = ""
    title = ""
    kind = "reporter"
    layer: Literal["foreground", "background"] = "foreground"
    needs_zones = False
    needs_bounds = False

    def compute(self, snapshot: GlyphSnapshot) -> list[Mark]:
        """Return marks for one glyph occurrence."""
        raise NotImplementedError

    def paint(
        self,
        context: Any,
        qt: Any,
        sink: Callable[[Exception, object], object],
        capture: Callable[[Any], GlyphSnapshot] | None = None,
    ) -> None:
        """Never allow capture, computation or Qt errors into paintEvent."""
        try:
            if context.layer is None:
                return
            if capture is None:
                from . import snapshot

                data = snapshot.capture(
                    context.layer,
                    include_zones=self.needs_zones,
                    include_bounds=self.needs_bounds,
                )
            else:
                data = capture(context.layer)
            render_marks(self.compute(data), context, qt)
        except Exception as error:  # noqa: BLE001 - Qt paint boundary must not raise
            try:
                sink(error, self)
            except Exception:  # noqa: BLE001, S110 - even an error sink must not unwind
                pass

    def bind(
        self, painters: Any, qt: Any, sink: Callable[[Exception, object], object]
    ) -> int:
        """Register with the selected native or fallback painter backend."""
        return painters.register(self, qt, sink)

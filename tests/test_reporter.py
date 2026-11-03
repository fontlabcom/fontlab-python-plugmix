# this_file: tests/test_reporter.py
"""Render font-unit marks with stable view-pixel styles and safe errors."""

from types import SimpleNamespace as NS

from fontlab_plugmix.reporter import Mark, Reporter, render_marks


class Point:
    def __init__(self, x, y):
        self._x, self._y = x, y

    def x(self):
        return self._x

    def y(self):
        return self._y


class Rect:
    def __init__(self, x, y, w, h):
        self.xywh = (x, y, w, h)


class Pen:
    def __init__(self, color):
        self.color = color
        self.width = 0

    def setWidthF(self, value):
        self.width = value


class Font:
    def setPixelSize(self, value):
        self.pixels = value


class Painter:
    def __init__(self):
        self.calls = []

    def setPen(self, value):
        self.calls.append(("pen", value.width))

    def setBrush(self, value):
        self.calls.append(("brush", value))

    def setFont(self, value):
        self.calls.append(("font", value.pixels))

    def drawLine(self, a, b):
        self.calls.append(("line", (a.x(), a.y()), (b.x(), b.y())))

    def drawEllipse(self, rect):
        self.calls.append(("ellipse", rect.xywh))

    def drawText(self, point, value):
        self.calls.append(("text", (point.x(), point.y()), value))


def scene():
    """Two sequential transforms: glyph*2, then view+3."""
    qt = NS(
        QtCore=NS(QPointF=Point, QRectF=Rect),
        QtGui=NS(QPen=Pen, QColor=lambda *rgb: rgb, QBrush=object, QFont=Font),
    )
    context = NS(
        painter=Painter(),
        layer=object(),
        glyph_to_canvas=NS(map=lambda p: Point(p.x() * 2, p.y() * 2)),
        canvas_to_view=NS(map=lambda p: Point(p.x() + 3, p.y() + 3)),
    )
    return qt, context


def test_render_marks_maps_geometry_but_keeps_pixel_styles():
    qt, context = scene()
    marks = [
        Mark("line", ((1, 2), (3, 4)), stroke_px=4),
        Mark("polyline", ((0, 0), (1, 1), (2, 1))),
        Mark("ring", ((1, 2),), diameter_px=16),
        Mark("text", ((1, 2),), text="x", text_px=14),
    ]
    render_marks(marks, context, qt)
    calls = context.painter.calls
    assert ("line", (5, 7), (9, 11)) in calls
    assert ("ellipse", (-3, -1, 16, 16)) in calls
    assert ("font", 14) in calls
    assert ("pen", 4) in calls
    assert sum(call[0] == "line" for call in calls) == 3


class Example(Reporter):
    name, title = "example", "Example"

    def compute(self, snapshot):
        return [Mark("text", ((2, 2),), text=str(snapshot))]


def test_reporter_paint_catches_compute_render_and_sink_failures():
    qt, context = scene()
    errors = []
    plugin = Example()
    plugin.paint(context, qt, lambda e, p: errors.append(e), capture=lambda layer: "ok")
    assert ("text", (7, 7), "ok") in context.painter.calls
    context.layer = None
    plugin.paint(context, qt, lambda e, p: errors.append(e), capture=lambda layer: 1)
    assert errors == []
    context.layer = object()
    plugin.paint(
        context, qt, lambda e, p: errors.append(e), capture=lambda layer: 1 / 0
    )
    assert isinstance(errors[0], ZeroDivisionError)
    bad = Example()
    bad.compute = lambda snapshot: [Mark("unknown", ((0, 0),))]
    bad.paint(context, qt, lambda e, p: 1 / 0, capture=lambda layer: "ok")


def test_reporter_bind_passes_itself_to_selected_backend():
    observed = []
    painters = NS(register=lambda *args, **kwargs: observed.append((args, kwargs)) or 7)
    reporter = Example()
    assert reporter.bind(painters, object(), lambda e, p: None) == 7
    assert observed[0][0][0] is reporter

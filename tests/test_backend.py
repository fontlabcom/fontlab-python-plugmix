# this_file: tests/test_backend.py
"""Fake native canvases exercise ownership, orders, transforms and fallback."""

from types import SimpleNamespace as NS

import pytest

from fontlab_plugmix.backend import EditorBackend, NativeCanvasBackend, select_backend
from fontlab_plugmix.reporter import Reporter


class Point:
    def __init__(self, x, y):
        self._x, self._y = x, y

    def x(self):
        return self._x

    def y(self):
        return self._y


class Transform:
    def __init__(self, dx, dy):
        self.dx, self.dy = dx, dy

    def map(self, point):
        return Point(point.x() + self.dx, point.y() + self.dy)


class Signal:
    def __init__(self):
        self.slots = []

    def connect(self, callback):
        self.slots.append(callback)

    def disconnect(self, callback):
        self.slots.remove(callback)


class Timer:
    def __init__(self):
        self.timeout = Signal()
        self.running = False
        self.deleted = False

    def setInterval(self, value):
        self.interval = value

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def deleteLater(self):
        self.deleted = True


class Canvas:
    UnderOwner, OverOwner = 0, 1

    def __init__(self, identifier):
        self.id = identifier
        self.isNull = False
        self.appended = []
        self.removed = []
        self.blocks = []
        self.remove_result = True
        self.remove_error = None
        self.append_error = None
        self.append_attempts = 0

    def appendPythonPainter(self, callback, order):
        self.append_attempts += 1
        if self.append_error is not None:
            raise self.append_error
        token = 100 + len(self.appended)
        self.appended.append((token, callback, order))
        return token

    def removePythonPainter(self, token):
        self.removed.append(token)
        if self.remove_error is not None:
            raise self.remove_error
        return self.remove_result

    def mapToViewportF(self, point):
        return Point(point.x() + 3, point.y() + 4)

    def scale(self):
        return 2

    def textBlocks(self):
        return self.blocks


class Example(Reporter):
    name, title = "example", "Example"

    def compute(self, snapshot):
        return []


class Background(Example):
    name, layer = "background", "background"


def runtime(canvas):
    """Supply only the PythonQt and FontLab pieces the backend touches."""
    workspace = NS(getActiveCanvas=lambda: canvas[0])
    fontlab = NS(flCanvas=Canvas, flWorkspace=NS(instance=lambda: workspace))
    qt = NS(QtCore=NS(QTimer=Timer, QPointF=Point))
    return qt, fontlab


def test_native_backend_attaches_both_orders_and_maps_block_position():
    active = [Canvas(1)]
    package = NS(master="Regular")
    layer = NS(isNull=False)
    glyph = NS(isNull=False, package=package, findLayer=lambda master: layer)
    info = NS(isActive=True, glyph=glyph, transform=Transform(10, 0))
    active[0].blocks = [NS(transform=Transform(100, 20), getAllGlyphs=lambda: [info])]
    qt, fontlab = runtime(active)
    errors, observed = [], []
    backend = NativeCanvasBackend(
        qt, fontlab, lambda e, source: errors.append(e), items=lambda get: list(get())
    )
    foreground, background = Example(), Background()
    foreground.paint = lambda context, q, sink: observed.append(context)
    first = backend.register(foreground, qt, lambda e, source: None)
    second = backend.register(background, qt, lambda e, source: None)
    assert [row[2] for row in active[0].appended] == [1, 0]
    assert backend._timer.running and backend._timer.interval == 250
    active[0].scale = lambda: (_ for _ in ()).throw(AssertionError("unused zoom"))
    active[0].appended[0][1](object(), active[0])
    point = observed[0].canvas_to_view.map(observed[0].glyph_to_canvas.map(Point(1, 2)))
    assert (point.x(), point.y()) == (114, 26)
    assert observed[0].layer.package is package
    timer = backend._timer
    active[0].remove_result = False
    backend.remove(first)
    assert active[0].removed == [100], "false means native painter is already gone"
    backend.remove(second)
    assert backend._timer is None and not timer.running and timer.deleted
    assert errors == []


def test_native_backend_reattaches_on_new_canvas_and_removes_all_tokens():
    active = [None]
    qt, fontlab = runtime(active)
    backend = NativeCanvasBackend(
        qt, fontlab, lambda e, source: None, items=lambda get: list(get())
    )
    first = backend.register(Example(), qt, lambda e, source: None)
    assert not backend.canvases, "a missing active canvas is retried by the timer"
    active[0] = Canvas(1)
    backend._poll()
    old = active[0]
    active[0] = Canvas(2)
    backend._poll()
    assert set(backend.canvases) == {1, 2}
    second = backend.register(Background(), qt, lambda e, source: None)
    assert len(old.appended) == len(active[0].appended) == 2
    backend.remove(second)
    assert old.removed == [101] and active[0].removed == [101]
    old.isNull = True
    backend._poll()
    assert set(backend.canvases) == {2}
    backend.close()
    assert active[0].removed == [101, 100]
    assert not backend.canvases
    backend.remove(first)


def test_native_attach_failure_is_reported_once_until_canvas_id_changes():
    active = [Canvas(1)]
    active[0].append_error = TypeError("painter unavailable")
    qt, fontlab = runtime(active)
    errors = []
    backend = NativeCanvasBackend(
        qt,
        fontlab,
        lambda error, source: errors.append(str(error)),
        items=lambda get: list(get()),
    )
    first = backend.register(Example(), qt, lambda error, source: None)
    backend._poll()
    backend.register(Background(), qt, lambda error, source: None)
    assert active[0].append_attempts == 1
    assert errors == ["painter unavailable"]
    active[0].isNull = True
    active[0] = Canvas(1)
    backend._poll()
    assert active[0].append_attempts == 0, "same canvas id remains blocked"
    active[0] = Canvas(2)
    active[0].append_error = ValueError("new canvas failure")
    backend._poll()
    backend._poll()
    assert active[0].append_attempts == 1
    assert errors == ["painter unavailable", "new canvas failure"]
    active[0].isNull = True
    active[0] = Canvas(3)
    backend._poll()
    assert active[0].append_attempts == 2, "new id receives both reporters"
    backend.remove(first)
    backend.close()


def test_native_remove_continues_after_type_error_and_leaked_callback_is_inert():
    active = [Canvas(1)]
    qt, fontlab = runtime(active)
    errors, painted = [], []
    backend = NativeCanvasBackend(
        qt,
        fontlab,
        lambda error, source: errors.append(error),
        items=lambda get: list(get()),
    )
    reporter = Example()
    reporter.paint = lambda context, q, sink: painted.append(context)
    token = backend.register(reporter, qt, lambda error, source: None)
    first = active[0]
    first.blocks = [
        NS(
            transform=Transform(0, 0),
            getAllGlyphs=lambda: [
                NS(
                    isActive=True,
                    glyph=NS(
                        isNull=False,
                        package=NS(master="Regular"),
                        findLayer=lambda m: NS(isNull=False),
                    ),
                    transform=Transform(0, 0),
                )
            ],
        )
    ]
    callback = first.appended[0][1]
    callback(object(), first)
    assert len(painted) == 1
    first.remove_error = TypeError("stale wrapper")
    active[0] = Canvas(2)
    backend._poll()
    timer = backend._timer
    backend.remove(token)
    assert first.removed == [100] and active[0].removed == [100]
    assert len(errors) == 1 and isinstance(errors[0], TypeError)
    assert timer.deleted and not timer.running
    callback(object(), first)
    assert len(painted) == 1, "a leaked native callback must stop drawing"


def test_native_remove_skips_destroyed_canvas_and_close_stops_timer_on_error():
    active = [Canvas(1)]
    qt, fontlab = runtime(active)
    backend = NativeCanvasBackend(
        qt, fontlab, lambda error, source: None, items=lambda get: list(get())
    )
    token = backend.register(Example(), qt, lambda error, source: None)
    old = active[0]
    old.isNull = True
    backend.remove(token)
    assert old.removed == [], "a destroyed canvas wrapper must not call native removal"

    old.isNull = False
    backend.register(Example(), qt, lambda error, source: None)
    timer = backend._timer
    backend.remove = lambda token: (_ for _ in ()).throw(TypeError("teardown"))
    with pytest.raises(TypeError, match="teardown"):
        backend.close()
    assert timer.deleted and not timer.running
    assert not backend._reporters


def test_native_backend_never_raises_from_callback_or_timer():
    active = [Canvas(1)]
    qt, fontlab = runtime(active)
    errors = []
    backend = NativeCanvasBackend(
        qt, fontlab, lambda e, source: errors.append(e), items=lambda get: list(get())
    )
    info = NS(isActive=True, glyph=NS(isNull=True))
    active[0].blocks = [NS(transform=Transform(0, 0), getAllGlyphs=lambda: [info])]
    backend.register(Example(), qt, lambda e, source: None)
    callback = active[0].appended[0][1]
    callback(object(), active[0])
    active[0].blocks = [NS(transform=Transform(0, 0), getAllGlyphs=lambda: 1 / 0)]
    callback(object(), active[0])
    assert isinstance(errors[0], ZeroDivisionError)
    fontlab.flWorkspace.instance().getActiveCanvas = lambda: 1 / 0
    backend._poll()
    assert len(errors) == 2
    backend.sink = lambda e, source: 1 / 0
    callback(object(), active[0])
    backend._poll()
    backend.close()


def test_backend_selection_prefers_native_and_fallback_logs_once():
    active = [None]
    qt, fontlab = runtime(active)
    errors = []
    native = select_backend(
        qt, fontlab, lambda e, source: errors.append(e), items=lambda get: list(get())
    )
    assert isinstance(native, NativeCanvasBackend)
    native.close()

    class OldCanvas:
        pass

    fontlab.flCanvas = OldCanvas
    calls = []
    painters = NS(
        register=lambda *args, **kw: calls.append((args, kw)) or len(calls),
        remove=lambda token: None,
        close=lambda: None,
    )
    editor = select_backend(
        qt,
        fontlab,
        lambda e, source: errors.append(e),
        editor_factory=lambda *args, **kw: painters,
    )
    assert isinstance(editor, EditorBackend)
    editor.register(Background(), qt, lambda e, source: None)
    editor.register(Background(), qt, lambda e, source: None)
    assert len(errors) == 1
    assert calls[0][0][0] == "after_native_layer"
    assert calls[0][1]["layer_filter"] == "active"
    editor.remove(1)
    editor.close()

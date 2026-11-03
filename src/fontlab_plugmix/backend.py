# this_file: src/fontlab_plugmix/backend.py
"""Native per-canvas painters with an EditorPainters fallback for old builds.

FontLab's text-block item applies its own transform before drawing a glyph
item (`fltextblockitem.cpp`). `EditorPainters` applies the glyph-item and block
transforms in that order. This backend does the same, then uses the native
`canvas.mapToViewportF` map for final viewport coordinates. The HT Letterspacer
consumer uses the glyph transform alone; that suffices only when the block's
transform is identity.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from importlib import import_module
from itertools import count
from typing import Any

from .reporter import Reporter
from .snapshot import NativeSource, resolve_source

POLL_MS = 250


@dataclass
class _CanvasEntry:
    """Keep a live canvas and its native tokens together."""

    canvas: Any
    tokens: dict[int, int] = field(default_factory=dict)


@dataclass(frozen=True)
class _GlyphMap:
    """Apply the glyph-item position, then its text-block transform."""

    glyph: Any
    block: Any

    def map(self, point: Any) -> Any:
        """Map one layer point into canvas coordinates."""
        return self.block.map(self.glyph.map(point))


@dataclass(frozen=True)
class _CanvasMap:
    """Expose FontLab's canvas-to-viewport map as ``map``."""

    canvas: Any

    def map(self, point: Any) -> Any:
        """Map a canvas point into viewport pixels."""
        return self.canvas.mapToViewportF(point)


@dataclass(frozen=True)
class _PaintContext:
    """The renderer's small context for one native glyph occurrence."""

    painter: Any
    layer: NativeSource
    glyph_to_canvas: _GlyphMap
    canvas_to_view: _CanvasMap
    scale: float


class NativeCanvasBackend:
    """Attach every enabled reporter to every active canvas encountered."""

    def __init__(
        self,
        qt: Any,
        fontlab: Any,
        sink: Callable[[Exception, object], object],
        *,
        items: Callable[[Callable[[], Any]], list[Any]] | None = None,
    ) -> None:
        self.qt, self.fl, self.sink = qt, fontlab, sink
        self.items = items or import_module("fontlabapp.qtsafe").qt_list
        self.canvases: dict[int, _CanvasEntry] = {}
        self._reporters: dict[int, Reporter] = {}
        self._ids = count(1)
        self._timer: Any = None
        self._kept_timers: list[Any] = []

    def register(self, reporter: Reporter, qt: Any, sink: Any) -> int:
        """Retain a reporter and attach it to all known live canvases."""
        token = next(self._ids)
        self._reporters[token] = reporter
        try:
            if self._timer is None:
                self._start_timer()
        except Exception:
            self._reporters.pop(token)
            raise
        for entry in tuple(self.canvases.values()):
            self._attach(entry, token)
        self._poll()
        return token

    def remove(self, token: int) -> None:
        """Remove a reporter's native token from each surviving canvas."""
        if self._reporters.pop(token, None) is None:
            return
        for entry in tuple(self.canvases.values()):
            native = entry.tokens.pop(token, None)
            if native is None:
                continue
            try:
                entry.canvas.removePythonPainter(native)
            except (RuntimeError, ValueError):
                pass  # a destroyed canvas has already dropped its painters
        if not self._reporters:
            self._stop_timer()
            self.canvases.clear()

    def close(self) -> None:
        """Drop every painter and stop polling; safe to call twice."""
        for token in tuple(self._reporters):
            self.remove(token)
        if self._timer is not None:
            self._stop_timer()
        self.canvases.clear()

    def _start_timer(self) -> None:
        """Poll new active canvases while any reporter is enabled."""
        timer = self.qt.QtCore.QTimer()
        timer.setInterval(POLL_MS)
        timer.timeout.connect(self._poll)
        timer.start()
        self._timer = timer

    def _stop_timer(self) -> None:
        """Disconnect before deletion, retaining failed teardown wrappers."""
        timer, self._timer = self._timer, None
        if timer is None:
            return
        try:
            timer.stop()
            timer.timeout.disconnect(self._poll)
            timer.deleteLater()
        except Exception as error:  # noqa: BLE001 - Qt teardown boundary
            self._kept_timers.append(timer)
            self._report(error, self)

    def _report(self, error: Exception, source: object) -> None:
        """An error sink must never unwind through native paint or Qt timers."""
        try:
            self.sink(error, source)
        except Exception:  # noqa: BLE001, S110 - native callback boundary
            pass

    def _poll(self) -> None:
        """Observe active canvases and forget wrappers destroyed by FontLab."""
        if not self._reporters:
            return
        try:
            for identifier, entry in tuple(self.canvases.items()):
                try:
                    gone = bool(entry.canvas.isNull)
                except (RuntimeError, ValueError):
                    gone = True
                if gone:
                    del self.canvases[identifier]
            canvas = self.fl.flWorkspace.instance().getActiveCanvas()
            if canvas is None or canvas.isNull:
                return
            identifier = int(canvas.id)
            entry = self.canvases.setdefault(identifier, _CanvasEntry(canvas))
            for token in tuple(self._reporters):
                self._attach(entry, token)
        except Exception as error:  # noqa: BLE001 - Qt timer boundary
            self._report(error, self)

    def _attach(self, entry: _CanvasEntry, token: int) -> None:
        """Register one callback at the reporter's requested native order."""
        if token in entry.tokens:
            return
        reporter = self._reporters[token]
        order = (
            entry.canvas.UnderOwner
            if reporter.layer == "background"
            else entry.canvas.OverOwner
        )
        callback = lambda painter, canvas: self._paint(reporter, painter, canvas)
        try:
            entry.tokens[token] = entry.canvas.appendPythonPainter(callback, order)
        except Exception as error:  # noqa: BLE001 - native registration boundary
            self._report(error, reporter)

    def _paint(self, reporter: Reporter, painter: Any, canvas: Any) -> None:
        """Draw every active glyph occurrence in viewport coordinates; never raise."""
        try:
            for block in self.items(canvas.textBlocks):
                for info in self.items(lambda block=block: block.getAllGlyphs() or ()):
                    if not info.isActive:
                        continue
                    source = resolve_source(info)
                    if source is None:
                        continue
                    context = _PaintContext(
                        painter,
                        source,
                        _GlyphMap(info.transform, block.transform),
                        _CanvasMap(canvas),
                        float(canvas.scale()),
                    )
                    reporter.paint(context, self.qt, self.sink)
        except Exception as error:  # noqa: BLE001 - native paint boundary
            self._report(error, reporter)


class EditorBackend:
    """Use App's transparent viewport overlay on builds without native hooks."""

    def __init__(
        self, painters: Any, sink: Callable[[Exception, object], object]
    ) -> None:
        self.painters, self.sink = painters, sink
        self._warned = False

    def register(self, reporter: Reporter, qt: Any, sink: Any) -> int:
        """Draw after native glyphs; announce background substitution once."""
        if reporter.layer == "background" and not self._warned:
            self._warned = True
            self.sink(
                RuntimeError(
                    "Background reporters draw over the canvas on this FontLab build"
                ),
                self,
            )
        return self.painters.register(
            "after_native_layer",
            lambda context: reporter.paint(context, qt, sink),
            layer_filter="active",
        )

    def remove(self, token: int) -> None:
        """Remove one App painter token."""
        self.painters.remove(token)

    def close(self) -> None:
        """Close App's viewport overlay owner."""
        self.painters.close()


def select_backend(
    qt: Any,
    fontlab: Any,
    sink: Callable[[Exception, object], object],
    *,
    editor_factory: Any = None,
    items: Callable[[Callable[[], Any]], list[Any]] | None = None,
) -> NativeCanvasBackend | EditorBackend:
    """Choose native hooks once; import EditorPainters only for older builds."""
    if hasattr(getattr(fontlab, "flCanvas", None), "appendPythonPainter"):
        return NativeCanvasBackend(qt, fontlab, sink, items=items)
    factory = (
        editor_factory or import_module("fontlabapp.editor_painters").EditorPainters
    )
    painters = factory(qt, fontlab, error_sink=sink, layer_resolver=resolve_source)
    return EditorBackend(painters, sink)

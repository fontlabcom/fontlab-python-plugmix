# this_file: src/fontlab_plugmix/general.py
"""Menu-oriented General plugin contract and owned runtime helpers."""

from importlib import import_module
from typing import Any, ClassVar

from . import snapshot
from .backend import active_glyph_map
from .kinds import guarded
from .plugin import Plugin


class _ActionOwner:
    """Keep extra actions added by a General plugin within its lifetime."""

    def __init__(self, menus: Any, sink: Any, plugin: Plugin) -> None:
        self.menus, self.sink, self.plugin = menus, sink, plugin
        self.tokens: list[int] = []

    def add_action(self, *args: Any, **kwargs: Any) -> int:
        """Record an additional owned action for automatic teardown."""
        token = self.menus.add_action(*args, **kwargs)
        self.tokens.append(token)
        return token

    def __getattr__(self, name: str) -> Any:
        return getattr(self.menus, name)

    def remove(self, token: int) -> None:
        """Avoid removing an action twice if the plugin already closed it."""
        self.menus.remove(token)
        if token in self.tokens:
            self.tokens.remove(token)

    def close(self) -> None:
        """Remove extra actions even when one removal fails."""
        for token in reversed(self.tokens):
            guarded(
                self.plugin, self.sink, lambda token=token: self.menus.remove(token)
            )
        self.tokens.clear()


class GeneralContext:
    """Expose menus, status, snapshot, edit and owned timers to a General."""

    def __init__(self, services: Any, plugin: Plugin) -> None:
        self.services, self.plugin = services, plugin
        self.menus = _ActionOwner(services.menus, services.sink, plugin)
        self._timers: list[tuple[Any, Any]] = []

    def notify(self, title: str, message: str) -> None:
        """Put a short status message in FontLab's main window."""
        self.menus.main_window().statusBar().showMessage(f"{title}: {message}")

    def snapshot(self) -> snapshot.GlyphSnapshot | None:
        """Capture the current glyph through the flWorkspace route."""
        active = snapshot.active_glyph(self.services.fontlab)
        if active is None:
            return None
        return snapshot.capture(
            snapshot.NativeSource(active.package, active.layer),
            fontlab=self.services.fontlab,
        )

    def edit(self, plan_fn: Any, title: str) -> Any:
        """Commit a prepared geometry plan as one App history operation."""
        work, facts, editor = plan_fn(self.snapshot())
        return import_module("fontlabapp.layer_writer").apply_work(
            work, title, facts, editor
        )

    def timer(self, ms: int, fn: Any) -> Any:
        """Start an owned timer whose callback cannot escape into Qt."""
        timer = self.services.qt.QtCore.QTimer()
        tick = lambda: guarded(self.plugin, self.services.sink, fn)
        try:
            timer.setInterval(ms)
            timer.timeout.connect(tick)
            timer.start()
        except Exception:
            guarded(self.plugin, self.services.sink, timer.deleteLater)
            raise
        self._timers.append((timer, tick))
        return timer

    def zoom_selected(self) -> bool:
        """Fit selected nodes of the active occurrence with a small canvas margin."""
        glyph = self.snapshot()
        if glyph is None:
            return False
        points = [(n.x, n.y) for c in glyph.contours for n in c.nodes if n.selected]
        if not points:
            return False
        canvas = self.services.fontlab.flWorkspace.instance().getActiveCanvas()
        transform = active_glyph_map(canvas)
        if transform is None:
            return False
        mapped = [
            transform.map(self.services.qt.QtCore.QPointF(*point)) for point in points
        ]
        xs, ys = [p.x() for p in mapped], [p.y() for p in mapped]
        left, top = min(xs) - 25, min(ys) - 25
        rect = self.services.qt.QtCore.QRectF(
            left, top, max(xs) - min(xs) + 50, max(ys) - min(ys) + 50
        )
        canvas.zoomTo(rect)
        return True

    def close(self) -> None:
        """Stop plugin-owned timers before dropping Qt callbacks."""
        for timer, tick in self._timers:
            guarded(self.plugin, self.services.sink, timer.stop)
            guarded(
                self.plugin,
                self.services.sink,
                lambda t=timer, f=tick: t.timeout.disconnect(f),
            )
            guarded(self.plugin, self.services.sink, timer.deleteLater)
        self._timers.clear()
        self.menus.close()


class General(Plugin):
    """A menu command with optional font-opened and font-closed hooks."""

    kind: ClassVar[str] = "general"
    menu: ClassVar[str | None] = "Window"
    shortcut: ClassVar[str | None] = None

    def start(self, ctx: GeneralContext) -> None:
        """Begin a session after its command is installed."""

    def stop(self) -> None:
        """End the session before its command is removed."""

    def run(self) -> None:
        """Handle the menu command."""

    def on_font_opened(self, font_id: int) -> None:
        """Observe a newly opened font."""

    def on_font_closed(self, font_id: int) -> None:
        """Observe a newly closed font."""

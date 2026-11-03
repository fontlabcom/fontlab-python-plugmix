# this_file: src/fontlab_plugmix/palettes/host.py
"""Own docked palette instances, Window toggles and one shared refresh timer."""

from dataclasses import dataclass
from importlib import import_module
from typing import Any

from fontlab_plugmix import snapshot
from fontlab_plugmix.kinds import Services, guarded

from .ui import PaletteUI


@dataclass
class _Panel:
    """Strong references to one palette and its owned Qt signals."""

    plugin: Any
    ui: PaletteUI
    owned: Any
    visibility: Any = None
    close_filter: Any = None
    visible: bool = True


def _close_filter(
    base: type, close_type: Any, callback: Any, plugin: Any, sink: Any
) -> Any:
    """Create a guarded event filter that only observes explicit dock closes."""

    class CloseFilter(base):
        def eventFilter(self, watched: Any, event: Any) -> bool:
            guarded(
                plugin, sink, lambda: callback() if event.type() == close_type else None
            )
            return False

    return CloseFilter()


class PaletteHost:
    """Bind every Palette to an OwnedWidget and refresh visible ones together."""

    def __init__(self, services: Services, registry: Any) -> None:
        self.services, self.registry = services, registry
        self.actions: dict[str, int] = {}
        self.panels: dict[str, _Panel] = {}
        self.timer: Any = None
        self._tick: Any = None
        self._key: Any = object()
        self._context: Any = None
        self._has_context = False
        self._running = False
        self._close_filter_available = True
        self._close_failures: set[tuple[str, str]] = set()
        self.listeners: dict[str, Any] = {}

    def _close_filter_base(self) -> type:
        """Use FontLab's PythonQt.private QObject, then older QtCore builds."""
        qt = self.services.qt
        base = getattr(getattr(qt, "private", None), "QObject", None)
        if base is None:
            base = getattr(qt.QtCore, "QObject", None)
        if base is None:
            raise AttributeError("PythonQt has no QObject base for dock close events")
        return base

    def _degrade_close(self, error: Exception) -> None:
        """Report once; the Window action remains the reliable close control."""
        self._close_filter_available = False
        message = RuntimeError(
            f"Dock close detection unavailable ({error}); use the Window toggle to close"
        )
        try:
            self.services.sink(message, self)
        except Exception:  # noqa: BLE001, S110 - diagnostics cannot block Show
            pass

    def _install_close_filter(self, panel: _Panel, name: str) -> None:
        """Try the optional native event filter without risking panel Show."""
        if not self._close_filter_available:
            return
        widget = panel.owned.widget
        filter_object = None
        try:
            filter_object = _close_filter(
                self._close_filter_base(),
                self.services.qt.QtCore.QEvent.Close,
                lambda: self._schedule_close(name),
                panel.plugin,
                self.services.sink,
            )
            widget.installEventFilter(filter_object)
        except Exception as error:  # noqa: BLE001 - optional PythonQt capability
            if filter_object is not None:
                try:
                    widget.removeEventFilter(filter_object)
                except Exception:  # noqa: BLE001, S110 - may not have installed
                    pass
            self._degrade_close(error)
        else:
            panel.close_filter = filter_object

    def install(self) -> None:
        """Create one checkable Window action and restore chosen panels."""
        for name, cls in self.registry.available("palette").items():
            token = self.services.menus.add_action(
                "Window",
                f"Plugmix: {cls.title} Panel",
                lambda *args, name=name: guarded(
                    self, self.services.sink, lambda: self.toggle(name)
                ),
                checkable=True,
            )
            self.actions[name] = token
            self.services.menus.action(token).setChecked(
                name in self.registry.enabled_palettes()
            )
        for name in self.registry.enabled_palettes():
            if name in self.actions:
                guarded(self, self.services.sink, lambda name=name: self._show(name))
                self._checked(name)

    def _timer(self) -> None:
        """Create the sole timer lazily, then start it for visible panels."""
        if self.timer is None:
            timer = self.services.qt.QtCore.QTimer()
            self._tick = self._tick_once
            try:
                timer.setInterval(250)
                timer.timeout.connect(self._tick)
            except Exception:
                guarded(self, self.services.sink, timer.deleteLater)
                raise
            self.timer = timer
        self._sync_timer()

    def _sync_timer(self) -> None:
        """Run polling exactly while at least one dock is visible."""
        if self.timer is None:
            return
        visible = bool(self.listeners) or any(
            panel.visible for panel in self.panels.values()
        )
        if visible and not self._running:
            self._key = object()
            self._has_context = False
            self.timer.start()
            self._running = True
        elif not visible and self._running:
            guarded(self, self.services.sink, self.timer.stop)
            self._running = False
            self._has_context = False

    def _tick_once(self) -> None:
        """Poll palettes and other subscribers on the same guarded QTimer."""
        if any(panel.visible for panel in self.panels.values()):
            guarded(self, self.services.sink, self._poll)
        for callback in tuple(self.listeners.values()):
            guarded(self, self.services.sink, callback)

    def subscribe(self, name: str, callback: Any) -> None:
        """Share the palette timer with a General plugin's font watcher."""
        self.listeners[name] = callback
        self._timer()

    def unsubscribe(self, name: str) -> None:
        """Stop polling when no visible palette or other subscriber remains."""
        self.listeners.pop(name, None)
        self._sync_timer()

    def _show(self, name: str) -> None:
        """Build a docked widget once and attach its guarded close signal."""
        if name in self.panels:
            return
        plugin = self.registry.available("palette")[name]()
        ui_box: list[PaletteUI] = []

        def build(content: Any) -> None:
            ui = PaletteUI(
                self.services.qt,
                content,
                plugin,
                self.services.sink,
                lambda values: plugin.command(values, self.services),
            )
            ui_box.append(ui)
            plugin.build(ui)

        create_panel = import_module("fontlabapp.widgets").create_panel
        try:
            owned = create_panel(
                self.services.menus.main_window(), plugin.title, build, plugin.area
            )
        except Exception:
            if ui_box:
                ui_box[0].close()
            guarded(plugin, self.services.sink, plugin.close)
            raise
        panel = _Panel(plugin, ui_box[0], owned, visible=bool(owned.widget.isVisible()))
        self.panels[name] = panel
        try:
            signal = owned.widget.visibilityChanged
            panel.visibility = lambda shown, name=name: guarded(
                plugin, self.services.sink, lambda: self._visibility(name, shown)
            )
            signal.connect(panel.visibility)
            self._install_close_filter(panel, name)
            self._timer()
            if self._has_context and panel.visible:
                guarded(
                    plugin, self.services.sink, lambda: plugin.refresh(self._context)
                )
        except Exception:
            self._hide(name)
            raise

    def _visibility(self, name: str, shown: bool) -> None:
        """Pause hidden docks without changing their saved preference."""
        panel = self.panels.get(name)
        if panel is None:
            return
        was_visible = panel.visible
        panel.visible = bool(shown)
        self._sync_timer()
        if shown and not was_visible and self._has_context:
            guarded(
                panel.plugin,
                self.services.sink,
                lambda: panel.plugin.refresh(self._context),
            )

    def _schedule_close(self, name: str) -> None:
        """Wait until Qt finishes dispatching Close before deleting the dock."""
        self.services.qt.QtCore.QTimer.singleShot(
            0,
            lambda: guarded(self, self.services.sink, lambda: self._hide_by_user(name)),
        )

    def _hide_by_user(self, name: str) -> None:
        """Persist only after the owner accepts an actual dock close."""
        panel = self.panels.get(name)
        if panel is None:
            return
        widget = panel.owned.widget
        if widget is None or not widget.isVisible():
            if self._hide(name):
                self.registry.set_palette_enabled(name, False)
            self._checked(name)

    def _close_failed(self, name: str, error: Exception) -> None:
        """Report one diagnostic for a repeated close failure."""
        key = (name, str(error))
        if key not in self._close_failures:
            self._close_failures.add(key)
            try:
                self.services.sink(error, self)
            except Exception:  # noqa: BLE001, S110 - diagnostic sink is untrusted
                pass

    def _hide(self, name: str) -> bool:
        """Release a panel only after its owner confirms successful close."""
        panel = self.panels.get(name)
        if panel is None:
            return True
        try:
            accepted = panel.owned.close()
        except Exception as error:  # noqa: BLE001 - App may raise ExceptionGroup
            self._close_failed(name, error)
            return False
        if accepted is False:
            self._close_failed(name, RuntimeError(f"Palette {name} close refused"))
            return False
        self.panels.pop(name, None)
        self._close_failures = {item for item in self._close_failures if item[0] != name}
        widget = panel.owned.widget
        if widget is not None and panel.visibility is not None:
            guarded(
                panel.plugin,
                self.services.sink,
                lambda: widget.visibilityChanged.disconnect(panel.visibility),
            )
        if widget is not None and panel.close_filter is not None:
            guarded(
                panel.plugin,
                self.services.sink,
                lambda: widget.removeEventFilter(panel.close_filter),
            )
        guarded(panel.plugin, self.services.sink, panel.ui.close)
        guarded(panel.plugin, self.services.sink, panel.plugin.close)
        self._sync_timer()
        return True

    def _checked(self, name: str) -> None:
        """Keep the owned QAction aligned with actual dock visibility."""
        self.services.menus.action(self.actions[name]).setChecked(name in self.panels)

    def toggle(self, name: str) -> bool:
        """Show or hide a panel and persist the resulting user choice."""
        if name not in self.actions:
            raise KeyError(name)
        try:
            if name in self.panels:
                if self._hide(name):
                    self.registry.set_palette_enabled(name, False)
            else:
                self._show(name)
                try:
                    self.registry.set_palette_enabled(name, True)
                except Exception:
                    self._hide(name)
                    raise
        finally:
            self._checked(name)
        return name in self.panels

    def _poll(self) -> None:
        """Capture once and refresh every visible palette only on a key change."""
        active = snapshot.active_glyph(self.services.fontlab)
        key = snapshot.palette_key(active)
        if key == self._key:
            return
        self._key = key
        context = (
            snapshot.capture(
                snapshot.NativeSource(active.package, active.layer),
                fontlab=self.services.fontlab,
            )
            if active
            else None
        )
        self._context = context
        self._has_context = True
        for panel in tuple(self.panels.values()):
            if not panel.visible:
                continue
            guarded(
                panel.plugin,
                self.services.sink,
                lambda panel=panel: panel.plugin.refresh(context),
            )

    def close(self) -> bool:
        """Stop ownership only after all docks accept close; allow retry."""
        for name in tuple(self.panels):
            self._hide(name)
        if self.panels:
            for name in self.panels:
                self._checked(name)
            return False
        self.listeners.clear()
        if self.timer is not None:
            guarded(self, self.services.sink, self.timer.stop)
            self._running = False
            guarded(
                self,
                self.services.sink,
                lambda: self.timer.timeout.disconnect(self._tick),
            )
            guarded(self, self.services.sink, self.timer.deleteLater)
            self.timer = None
        for token in tuple(self.actions.values()):
            guarded(
                self,
                self.services.sink,
                lambda token=token: self.services.menus.remove(token),
            )
        self.actions.clear()
        return True

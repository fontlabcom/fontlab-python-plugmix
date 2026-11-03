# this_file: src/fontlab_plugmix/general_plugins/host.py
"""Own General menu commands, timers and font lifecycle polling."""

from dataclasses import dataclass
from importlib import import_module
from typing import Any

from fontlab_plugmix.general import GeneralContext
from fontlab_plugmix.kinds import Services, guarded


@dataclass
class _Running:
    """Retain one started plugin, its owned context and menu token."""

    plugin: Any
    context: GeneralContext
    token: int | None


class GeneralHost:
    """Start General plugins and share PaletteHost's existing 250 ms timer."""

    def __init__(self, services: Services, registry: Any, palettes: Any) -> None:
        self.services, self.registry, self.palettes = services, registry, palettes
        self.running: dict[str, _Running] = {}
        self._fonts: set[int] = set()

    def _font_ids(self) -> set[int]:
        """Read open package ids from the workspace, not CurrentGlyph()."""
        workspace = self.services.fontlab.flWorkspace.instance()
        items = import_module("fontlabapp.qtsafe").qt_list
        return {int(package.id) for package in items(workspace.packages)}

    def _shortcut(self, token: int, shortcut: str, plugin: Any) -> None:
        """Leave an existing shortcut untouched and report a conflict."""
        menus, qt = self.services.menus, self.services.qt
        action = menus.action(token)
        siblings = menus.main_window().findChildren(qt.QtGui.QAction)
        for other in siblings:
            if other is not action and str(other.shortcut().toString()) == shortcut:
                raise ValueError(f"Shortcut {shortcut} is already in use")
        action.setShortcut(shortcut)

    def _start(self, name: str) -> None:
        """Install the command first; unwind it if start fails."""
        plugin = self.registry.available("general")[name]()
        context = GeneralContext(self.services, plugin)
        token = None
        try:
            if plugin.menu is not None:
                token = self.services.menus.add_action(
                    plugin.menu,
                    plugin.title,
                    lambda *args: guarded(plugin, self.services.sink, plugin.run),
                    checkable=False,
                )
            plugin.start(context)
            if token is not None and plugin.shortcut:
                guarded(
                    plugin,
                    self.services.sink,
                    lambda: self._shortcut(token, plugin.shortcut, plugin),
                )
        except Exception:
            guarded(plugin, self.services.sink, plugin.stop)
            context.close()
            if token is not None:
                guarded(
                    plugin,
                    self.services.sink,
                    lambda: self.services.menus.remove(token),
                )
            raise
        self.running[name] = _Running(plugin, context, token)

    def install(self) -> None:
        """Start saved General plugins and attach their shared font watcher."""
        self._fonts = guarded(self, self.services.sink, self._font_ids) or set()
        for name in self.registry.enabled_general():
            if name not in self.registry.available("general"):
                continue
            guarded(self, self.services.sink, lambda name=name: self._start(name))
        if self.running:
            self.palettes.subscribe("general", self._poll)

    def _poll(self) -> None:
        """Deliver set-difference font events once per open or close."""
        current = self._font_ids()
        opened, closed = current - self._fonts, self._fonts - current
        self._fonts = current
        for running in tuple(self.running.values()):
            for identifier in sorted(opened):
                guarded(
                    running.plugin,
                    self.services.sink,
                    lambda n=identifier, p=running.plugin: p.on_font_opened(n),
                )
            for identifier in sorted(closed):
                guarded(
                    running.plugin,
                    self.services.sink,
                    lambda n=identifier, p=running.plugin: p.on_font_closed(n),
                )

    def _stop(self, name: str) -> None:
        """Stop plugin before removing its command and extra actions."""
        running = self.running.pop(name, None)
        if running is None:
            return
        try:
            guarded(running.plugin, self.services.sink, running.plugin.stop)
        finally:
            running.context.close()
            if running.token is not None:
                guarded(
                    running.plugin,
                    self.services.sink,
                    lambda: self.services.menus.remove(running.token),
                )

    def close(self) -> None:
        """Stop shared polling and every started General plugin."""
        self.palettes.unsubscribe("general")
        for name in tuple(self.running):
            self._stop(name)

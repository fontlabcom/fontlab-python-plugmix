# this_file: src/fontlab_plugmix/tools/host.py
"""Register native tools, keep their bridges alive and own Window toggles."""

from dataclasses import dataclass
from typing import Any, ClassVar

from fontlab_plugmix.kinds import Services, guarded

from .bridge import ToolBridge


class UnsupportedCapability(RuntimeError):
    """This FontLab build lacks native Python tool registration."""


@dataclass
class _Registration:
    """Strong references required for FontLab's callback lifetime."""

    native: Any
    bridge: ToolBridge
    plugin: Any


class ToolHost:
    """Own native tool registrations and persistent enable actions."""

    _retained: ClassVar[list[_Registration]] = []

    def __init__(self, services: Services, registry: Any) -> None:
        self.services, self.registry = services, registry
        self.actions: dict[str, int] = {}
        self.registered: dict[str, _Registration] = {}
        self.workspace: Any = None

    def _workspace(self) -> Any:
        """Require the verified flWorkspace Python tool hook."""
        workspace_class = getattr(self.services.fontlab, "flWorkspace", None)
        if workspace_class is None:
            raise UnsupportedCapability("FontLab has no flWorkspace.registerPythonTool")
        workspace = workspace_class.instance()
        if not callable(getattr(workspace, "registerPythonTool", None)):
            raise UnsupportedCapability("FontLab has no flWorkspace.registerPythonTool")
        return workspace

    def _register(self, name: str) -> None:
        """Pin the bridge before FontLab can call its first callback."""
        if name in self.registered:
            return
        plugin = self.registry.available("tool")[name]()
        bridge = ToolBridge(plugin, self.services)
        workspace = self._workspace()
        native = workspace.registerPythonTool(plugin.title, None, bridge)
        self.workspace = workspace
        self.registered[name] = _Registration(native, bridge, plugin)

    def _unregister(self, name: str) -> None:
        """Drop overlay first, then native registration, even after errors."""
        record = self.registered.get(name)
        if record is None:
            return
        record.bridge.deactivate()
        self.workspace.unregisterPythonTool(record.native)
        self.registered.pop(name, None)

    def _checked(self, name: str) -> None:
        self.services.menus.action(self.actions[name]).setChecked(
            name in self.registered
        )

    def install(self) -> None:
        """Install one Window toggle per tool; skip unsupported native hooks."""
        for name, cls in self.registry.available("tool").items():
            token = self.services.menus.add_action(
                "Window",
                f"Plugmix: Tool {cls.title}",
                lambda *args, name=name: guarded(
                    self, self.services.sink, lambda: self.toggle(name)
                ),
                checkable=True,
            )
            self.actions[name] = token
            if name in self.registry.enabled_tools():
                try:
                    self._register(name)
                except UnsupportedCapability as error:
                    guarded(
                        self,
                        self.services.sink,
                        lambda error=error: (_ for _ in ()).throw(error),
                    )
                    self.services.menus.action(token).setEnabled(False)
                except Exception as error:  # noqa: BLE001 - one tool cannot block boot
                    guarded(
                        self,
                        self.services.sink,
                        lambda error=error: (_ for _ in ()).throw(error),
                    )
            self._checked(name)

    def toggle(self, name: str) -> bool:
        """Apply the user's explicit registration choice and persist it."""
        if name not in self.actions:
            raise KeyError(name)
        active = name in self.registered
        try:
            if active:
                self._unregister(name)
                try:
                    self.registry.set_tool_enabled(name, False)
                except Exception:
                    guarded(self, self.services.sink, lambda: self._register(name))
                    raise
            else:
                self._register(name)
                try:
                    self.registry.set_tool_enabled(name, True)
                except Exception:
                    guarded(self, self.services.sink, lambda: self._unregister(name))
                    raise
        finally:
            self._checked(name)
        return name in self.registered

    def close(self) -> None:
        """Unregister every tool and remove owned actions without losing prefs."""
        for name in tuple(self.registered):
            try:
                self._unregister(name)
            except Exception as error:  # noqa: BLE001 - pin a still-native bridge
                self._retained.append(self.registered.pop(name))
                guarded(
                    self,
                    self.services.sink,
                    lambda error=error: (_ for _ in ()).throw(error),
                )
        for token in tuple(self.actions.values()):
            guarded(
                self,
                self.services.sink,
                lambda token=token: self.services.menus.remove(token),
            )
        self.actions.clear()

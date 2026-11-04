# this_file: src/fontlab_plugmix/filters/host.py
"""Own Glyph-menu Filter actions and their parameter dialogs."""

from importlib import import_module
from typing import Any

from fontlab_plugmix import snapshot
from fontlab_plugmix.kinds import Services, guarded

from .apply import apply_filter
from .dialog import FilterDialog


class FilterHost:
    """Bind filters to owned actions and guarded Apply callbacks."""

    def __init__(self, services: Services, registry: Any) -> None:
        self.services, self.registry = services, registry
        self.actions: list[int] = []
        self.windows: dict[int, FilterDialog] = {}

    def install(self) -> None:
        """Add one non-checkable Glyph command for every enabled filter."""
        for name in self.registry.enabled_filters():
            cls = self.registry.available("filter").get(name)
            if cls is None:
                continue
            token = self.services.menus.add_action(
                "Glyph",
                f"Plugmix: {cls.title}…",
                lambda name=name, cls=cls: guarded(
                    cls, self.services.sink, lambda: self.run(name)
                ),
                checkable=False,
            )
            self.actions.append(token)

    def run(self, name: str) -> None:
        """Open on a selection; Apply re-reads the selection at click time."""
        selected = snapshot.selected_layers()
        if not selected.occurrences:
            return
        plugin = self.registry.available("filter")[name]()
        token_box: list[int] = []

        def close() -> None:
            # OwnedMenus cannot remove a tool window inside our button signal.
            self.services.qt.QtCore.QTimer.singleShot(
                0,
                lambda: guarded(
                    plugin,
                    self.services.sink,
                    lambda: self.services.menus.remove(token_box[0]),
                ),
            )

        def apply(values: dict[str, Any]) -> None:
            """Save a preference opportunistically, then edit the live selection."""
            guarded(
                plugin,
                self.services.sink,
                lambda: self.registry.set_params(name, values),
            )
            plan, result = apply_filter(plugin, values)
            if result is None and (plan.refused or plan.skipped):
                dialog.status.setText(
                    "Skipped: " + ", ".join((*plan.refused, *plan.skipped))
                )
                return
            if result is not None:
                self.services.fontlab.UpdateActiveCanvas()
            if plan.refused or plan.skipped:
                dialog.status.setText(
                    "Skipped: " + ", ".join((*plan.refused, *plan.skipped))
                )
                return
            close()

        dialog = FilterDialog(
            self.services.qt,
            plugin,
            self.registry.values(name),
            apply,
            close,
            self.services.sink,
        )

        def finished() -> None:
            dialog.close()
            if token_box:
                self.windows.pop(token_box[0], None)

        try:
            # PythonQt exposes the sizeHint Q_PROPERTY as a QSize value, not a method.
            size = import_module("fontlabapp.qt_properties").value(dialog.widget, "sizeHint")
            dialog.widget.resize(size)
            token, window = self.services.menus.tool_window(
                dialog.widget, plugin.title, on_close=finished
            )
            token_box.append(token)
            self.windows[token] = dialog
            window.resize(size)
        except Exception:
            if token_box:
                self.services.menus.remove(token_box[0])
            dialog.close()
            raise

    def close(self) -> None:
        """Remove windows and commands before their OwnedMenus owner closes."""
        for token in (*self.windows, *self.actions):
            try:
                self.services.menus.remove(token)
            except Exception as error:  # noqa: BLE001 - teardown boundary
                try:
                    self.services.sink(error, self)
                except Exception:  # noqa: BLE001, S110 - sink cannot block teardown
                    pass
        self.windows.clear()
        self.actions.clear()

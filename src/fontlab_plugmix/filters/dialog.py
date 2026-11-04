# this_file: src/fontlab_plugmix/filters/dialog.py
"""Small owned, non-modal PythonQt dialog built from Filter Params."""

from collections.abc import Callable
from typing import Any

from fontlab_plugmix.filter import Filter, Param
from fontlab_plugmix.kinds import guarded


def _control(gui: Any, param: Param, value: Any, parent: Any) -> Any:
    """Create one typed Qt editor for a declarative parameter."""
    if param.kind in {"float", "int"}:
        widget = (gui.QDoubleSpinBox if param.kind == "float" else gui.QSpinBox)(parent)
        if param.kind == "float":
            widget.setDecimals(3)
        low = param.minimum if param.minimum is not None else -1_000_000
        high = param.maximum if param.maximum is not None else 1_000_000
        if param.kind == "float":
            widget.setRange(float(low), float(high))
        else:
            widget.setRange(int(low), int(high))
        widget.setValue(value)
    elif param.kind == "bool":
        widget = gui.QCheckBox(parent)
        widget.setChecked(value)
    else:
        widget = gui.QComboBox(parent)
        widget.addItems(list(param.choices))
        widget.setCurrentIndex(param.choices.index(value))
    return widget


def _value(widget: Any, kind: str) -> Any:
    """Read a control without relying on PythonQt property-call ambiguity."""
    field = (
        "value"
        if kind in {"float", "int"}
        else ("isChecked" if kind == "bool" else "currentText")
    )
    found = getattr(widget, field)
    return found() if callable(found) else found


class FilterDialog:
    """Own signal connections and expose the widget to OwnedMenus.tool_window."""

    def __init__(
        self,
        qt: Any,
        plugin: Filter,
        values: dict[str, Any],
        on_apply: Callable[[dict[str, Any]], Any],
        on_cancel: Callable[[], Any],
        sink: Callable[[Exception, object], object],
    ) -> None:
        gui = qt.QtGui
        self.plugin, self.sink = plugin, sink
        self.widget = gui.QWidget()
        self.controls: dict[str, tuple[Param, Any]] = {}
        self.connections: list[tuple[Any, Any]] = []
        layout = gui.QVBoxLayout(self.widget)
        form = gui.QFormLayout()
        layout.addLayout(form)
        for param in plugin.params:
            control = _control(gui, param, values[param.key], self.widget)
            self.controls[param.key] = (param, control)
            form.addRow(param.label, control)
        self.status = gui.QLabel("", self.widget)
        layout.addWidget(self.status)
        buttons = gui.QHBoxLayout()
        layout.addLayout(buttons)
        cancel, apply = (
            gui.QPushButton("Cancel", self.widget),
            gui.QPushButton("Apply", self.widget),
        )
        buttons.addWidget(cancel)
        buttons.addWidget(apply)
        self._connect(
            cancel.clicked, lambda *args: guarded(plugin, self._report, on_cancel)
        )
        self._connect(
            apply.clicked,
            lambda *args: guarded(
                plugin, self._report, lambda: on_apply(self.values())
            ),
        )

    def _report(self, error: Exception, source: object) -> None:
        """Show an Apply failure and forward it to the host's error sink."""
        try:
            self.status.setText(str(error))
        except Exception:  # noqa: BLE001, S110 - keep forwarding the cause
            pass
        self.sink(error, source)

    def _connect(self, signal: Any, callback: Callable[..., Any]) -> None:
        signal.connect(callback)
        self.connections.append((signal, callback))

    def values(self) -> dict[str, Any]:
        """Read and validate every control before Apply."""
        raw = {
            key: _value(widget, param.kind)
            for key, (param, widget) in self.controls.items()
        }
        return type(self.plugin).validate(raw)

    def close(self) -> None:
        """Disconnect before OwnedMenus schedules widget teardown; repeat safely."""
        for signal, callback in self.connections:
            try:
                signal.disconnect(callback)
            except Exception as error:  # noqa: BLE001 - stale PythonQt receiver
                try:
                    self.sink(error, self.plugin)
                except Exception:  # noqa: BLE001, S110 - teardown must finish
                    pass
        self.connections.clear()

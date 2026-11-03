# this_file: src/fontlab_plugmix/palettes/ui.py
"""Small PythonQt facade with owned signal connections for palette controls."""

from collections.abc import Callable
from typing import Any

from fontlab_plugmix.kinds import guarded


class PaletteUI:
    """Offer labels, numbers, buttons and checks without exposing Qt imports."""

    def __init__(
        self, qt: Any, content: Any, plugin: object, sink: Callable, command: Callable
    ) -> None:
        self.qt, self.content = qt, content
        self.plugin, self.sink, self.command = plugin, sink, command
        self.layout = qt.QtGui.QVBoxLayout(content)
        self.connections: list[tuple[Any, Any]] = []

    def label(self, text: str) -> Any:
        """Append a plain text label and return it for status updates."""
        widget = self.qt.QtGui.QLabel(text, self.content)
        self.layout.addWidget(widget)
        return widget

    def set_text(self, label: Any, text: str) -> None:
        """Change the text of a label owned by this palette."""
        label.setText(text)

    def number(
        self,
        label: str,
        value: float,
        *,
        integer: bool = False,
        minimum: float = -1e6,
        maximum: float = 1e6,
    ) -> Any:
        """Append a labelled spin control with a bounded numeric range."""
        gui = self.qt.QtGui
        widget = (gui.QSpinBox if integer else gui.QDoubleSpinBox)(self.content)
        widget.setRange(int(minimum), int(maximum)) if integer else widget.setRange(
            minimum, maximum
        )
        widget.setValue(value)
        row = gui.QFormLayout()
        row.addRow(label, widget)
        self.layout.addLayout(row)
        return widget

    def checkbox(self, label: str, checked: bool = False) -> Any:
        """Append a checkable option and return its widget handle."""
        widget = self.qt.QtGui.QCheckBox(label, self.content)
        widget.setChecked(checked)
        self.layout.addWidget(widget)
        return widget

    def button(self, title: str, callback: Callable[[], Any]) -> Any:
        """Connect a guarded button action and remember it for teardown."""
        widget = self.qt.QtGui.QPushButton(title, self.content)
        slot = lambda *args: guarded(self.plugin, self.sink, callback)
        widget.clicked.connect(slot)
        self.connections.append((widget.clicked, slot))
        self.layout.addWidget(widget)
        return widget

    @staticmethod
    def value(widget: Any) -> Any:
        """Read a PythonQt value property or fake callable consistently."""
        found = widget.value
        return found() if callable(found) else found

    def apply(self, values: dict[str, Any]) -> Any:
        """Send a palette command through the host-provided edit boundary."""
        return self.command(values)

    def close(self) -> None:
        """Disconnect callbacks before the dock widget can be deleted."""
        for signal, callback in self.connections:
            guarded(
                self.plugin,
                self.sink,
                lambda signal=signal, callback=callback: signal.disconnect(callback),
            )
        self.connections.clear()

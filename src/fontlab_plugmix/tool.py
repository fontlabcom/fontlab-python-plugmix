# this_file: src/fontlab_plugmix/tool.py
"""FontLab-native tool contract and a snapshot-backed active context."""

from dataclasses import dataclass
from importlib import import_module
from typing import Any, ClassVar

from . import snapshot
from .plugin import Plugin
from .reporter import Mark


@dataclass(frozen=True)
class ToolEvent:
    """A copied native event with glyph and viewport coordinates."""

    x: float
    y: float
    view_x: float
    view_y: float
    buttons: int = 0
    shift: bool = False
    alt: bool = False
    ctrl: bool = False
    meta: bool = False
    key: str | None = None
    clicks: int = 1
    scale: float = 1.0


class ToolContext:
    """Offer checked active glyph reads, selection and undoable edits."""

    def __init__(self, services: Any) -> None:
        self.services = services

    def snapshot(self) -> snapshot.GlyphSnapshot | None:
        """Capture through the workspace path, never CurrentGlyph()."""
        active = snapshot.active_glyph(self.services.fontlab)
        if active is None:
            return None
        return snapshot.capture(
            snapshot.NativeSource(active.package, active.layer),
            fontlab=self.services.fontlab,
        )

    def select(self, indices: tuple[int, ...], *, toggle: bool = False) -> None:
        """Change selection flags only; no outline geometry or history write."""
        active = snapshot.active_glyph(self.services.fontlab)
        if active is not None:
            snapshot.select_contours(active.layer, indices, toggle=toggle)
            self.redraw()

    def edit(self, plan_fn: Any, title: str) -> Any:
        """Commit a caller-provided `(work, facts, editor)` through App's writer."""
        work, facts, editor = plan_fn(self.snapshot())
        return import_module("fontlabapp.layer_writer").apply_work(
            work, title, facts, editor
        )

    def redraw(self) -> None:
        """Ask FontLab to repaint the active Glyph canvas."""
        self.services.fontlab.UpdateActiveCanvas()


class Tool(Plugin):
    """One native tool; event handlers return True only when they handle input."""

    kind: ClassVar[str] = "tool"
    cursor: ClassVar[str | None] = None

    def activate(self, ctx: ToolContext) -> None:
        """Receive an active context after FontLab switches to this tool."""

    def deactivate(self) -> None:
        """Release per-activation state."""

    def press(self, event: ToolEvent) -> bool:
        """Handle mouse press."""
        return False

    def move(self, event: ToolEvent) -> bool:
        """Handle mouse move."""
        return False

    def release(self, event: ToolEvent) -> bool:
        """Handle mouse release."""
        return False

    def double_click(self, event: ToolEvent) -> bool:
        """Handle a double click."""
        return False

    def key_down(self, event: ToolEvent) -> bool:
        """Observe key press without taking FontLab shortcuts."""
        return False

    def key_up(self, event: ToolEvent) -> bool:
        """Observe key release without taking FontLab shortcuts."""
        return False

    def marks(self, glyph: snapshot.GlyphSnapshot | None) -> list[Mark]:
        """Return overlay marks only while active."""
        return []

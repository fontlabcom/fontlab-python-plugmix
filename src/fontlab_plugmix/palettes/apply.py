# this_file: src/fontlab_plugmix/palettes/apply.py
"""Stage selected contour copies and commit them through the shared writer."""

from importlib import import_module
from math import isfinite
from typing import Any

from fontlab_plugmix import snapshot
from fontlab_plugmix.filters.apply import _targets_safe
from fontlab_plugmix.kinds import Services


def _values(values: dict[str, Any]) -> tuple[int, float, float]:
    """Accept finite offsets and a nonnegative number of additional copies."""
    count, dx, dy = values["count"], values["dx"], values["dy"]
    if type(count) is not int or count < 0 or count > 100:
        raise ValueError("Count must be between 0 and 100")
    if any(
        type(value) not in (int, float) or not isfinite(value) for value in (dx, dy)
    ):
        raise ValueError("Offsets must be finite numbers")
    if count and dx == 0 and dy == 0:
        raise ValueError("X and Y offsets cannot both be zero")
    return count, float(dx), float(dy)


def selected_indices(glyph: snapshot.GlyphSnapshot) -> tuple[int, ...]:
    """A contour is selected when at least one of its nodes is selected."""
    return tuple(
        index
        for index, contour in enumerate(glyph.contours)
        if any(node.selected for node in contour.nodes)
    )


class RepeatEditor:
    """Clone each selected native contour before history, then add its copies."""

    def __init__(self, outlines: Any, qt: Any, repair: Any) -> None:
        self.outlines, self.qt, self.repair = outlines, qt, repair

    def prepare(self, layer: Any, edits: list[Any]) -> list[tuple[Any, Any]]:
        """Refuse a changed unsafe layer before opening the Undo transaction."""
        rows = [
            (shape, contour)
            for shape in layer.shapes
            if not shape.isComponent
            for contour in shape.contours
        ]
        staged = []
        for indices, offsets in edits:
            if not _targets_safe(layer, indices, self.outlines):
                raise ValueError(
                    "Step and Repeat cannot copy a shared or transformed outline"
                )
            for index in indices:
                shape, contour = rows[index]
                for dx, dy in offsets:
                    transform = self.qt.QtGui.QTransform()
                    transform.translate(dx, dy)
                    copy = contour.cloneMapped(transform)
                    self.repair(contour, copy)
                    staged.append((shape, copy))
        return staged

    def write(self, layer: Any, steps: list[tuple[Any, Any]]) -> None:
        """Attach staged copies to their original owning shapes."""
        for shape, copy in steps:
            shape.addContour(copy, True)

    def check(self, prepared: list[tuple[Any, list[tuple[Any, Any]]]]) -> list[str]:
        """Report a copy that native shape attachment did not retain."""
        return [
            "repeated contour missing after write"
            for _, steps in prepared
            for shape, copy in steps
            if not any(int(item.id) == int(copy.id) for item in shape.contours)
        ]

    def retain(self, steps: list[Any]) -> list[Any]:
        """New copies remove no native objects that history must pin."""
        return []


def repeat_selected(
    values: dict[str, Any],
    services: Services,
    *,
    outlines: Any = None,
    writer: Any = None,
    history: Any = None,
    repair: Any = None,
) -> tuple[Any, Any, str]:
    """Copy the current glyph's selected contours in one geometry Undo step."""
    count, dx, dy = _values(values)
    if count == 0:
        return None, None, "Count is zero; nothing to repeat."
    active = snapshot.active_glyph(services.fontlab)
    if active is None:
        return None, None, "No active glyph."
    before = snapshot.capture(
        snapshot.NativeSource(active.package, active.layer), fontlab=services.fontlab
    )
    indices = selected_indices(before)
    if not indices:
        return None, None, "Select a contour first."
    outlines = outlines or import_module("fontlabapp.outline_writer")
    writer = writer or import_module("fontlabapp.layer_writer")
    history = history or import_module("fontlabapp.history")
    repair = repair or import_module("fontlabapp.contour_copy").repair_nodes
    offsets = tuple((dx * step, dy * step) for step in range(1, count + 1))
    facts = history.scan_auto_facts(active.package)
    unsafe = []

    def planner(glyph: Any, master: str, layer: Any) -> list[Any]:
        if not _targets_safe(layer, indices, outlines):
            unsafe.append(str(glyph.name))
            return [
                outlines.Change(
                    "contours", "", "shared or transformed outline, skipped"
                )
            ]
        return [
            outlines.Change(
                "contours",
                str(len(before.contours)),
                str(len(before.contours) + len(indices) * count),
                edit=(indices, offsets),
                key=(indices, count),
            )
        ]

    plan = outlines.collect(
        [active.glyph], [str(active.package.master)], planner, facts
    )
    plan.refused.extend(unsafe)
    if not plan.work:
        return plan, None, "Skipped: " + ", ".join((*plan.refused, *plan.skipped))
    result = writer.apply_work(
        plan.work, "Step and Repeat", facts, RepeatEditor(outlines, services.qt, repair)
    )
    services.fontlab.UpdateActiveCanvas()
    return plan, result, f"Added {len(indices) * count} contour copies."

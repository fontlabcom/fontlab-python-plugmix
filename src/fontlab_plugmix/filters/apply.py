# this_file: src/fontlab_plugmix/filters/apply.py
"""Plan deletion-only LayerEdits and commit them through fontlabapp's writer."""

from importlib import import_module
from typing import Any

from fontlab_plugmix import snapshot
from fontlab_plugmix.filter import Filter, LayerEdit


def _removed(before: snapshot.GlyphSnapshot, edit: LayerEdit) -> tuple[int, ...]:
    """Resolve retained snapshot contour identities; reject unsupported writes."""
    if edit.advance is not None or edit.anchors is not None:
        raise ValueError("This Filter host currently supports contour deletion only")
    if edit.contours is None:
        return ()
    original = {id(contour) for contour in before.contours}
    kept = [id(contour) for contour in edit.contours]
    if len(set(kept)) != len(kept) or not set(kept) <= original:
        raise ValueError("Filter returned new or repeated contours")
    keep_set = set(kept)
    if kept != [id(contour) for contour in before.contours if id(contour) in keep_set]:
        raise ValueError("This Filter host cannot reorder contours")
    return tuple(
        index
        for index, contour in enumerate(before.contours)
        if id(contour) not in kept
    )


def plan_filter(
    plugin: Filter, values: dict[str, Any], selected: Any, outlines: Any, history: Any
) -> tuple[Any, Any]:
    """Use outline_writer's auto-layer policy for selected current-master glyphs."""
    if not selected.occurrences:
        return outlines.Plan(), None
    package = selected.occurrences[0].package
    master = str(package.master)
    glyphs = list(
        {int(row.glyph.id): row.glyph for row in selected.occurrences}.values()
    )
    facts = history.scan_auto_facts(package)

    def planner(glyph: Any, master_name: str, layer: Any) -> list[Any]:
        before = snapshot.capture(snapshot.NativeSource(package, layer))
        removed = _removed(before, plugin.compute(before, values))
        if not removed:
            return []
        return [
            outlines.Change(
                "contours",
                str(len(before.contours)),
                str(len(before.contours) - len(removed)),
                edit=removed,
                key=removed,
            )
        ]

    return outlines.collect(glyphs, [master], planner, facts), facts


class LayerEditEditor:
    """Remove own native contours, retaining them for one Undo step."""

    def __init__(self, outlines: Any) -> None:
        self.outlines = outlines

    def prepare(
        self, layer: Any, edits: list[tuple[int, ...]]
    ) -> list[tuple[Any, Any, int]]:
        """Resolve and validate all deletion targets before opening history."""
        allowed = {int(shape.id) for shape in self.outlines.outline_shapes(layer)[0]}
        rows = [
            (shape, contour)
            for shape in layer.shapes
            if not shape.isComponent
            for contour in shape.contours
        ]
        indices = {index for group in edits for index in group}
        if any(
            index >= len(rows) or int(rows[index][0].id) not in allowed
            for index in indices
        ):
            raise ValueError("Filter cannot edit a shared or transformed outline")
        return [
            (*rows[index], int(rows[index][1].id))
            for index in sorted(indices, reverse=True)
        ]

    def write(self, layer: Any, steps: list[tuple[Any, Any, int]]) -> None:
        """Remove selected contours from their native owning shapes."""
        for shape, contour, _identifier in steps:
            shape.removeContour(contour)

    def check(
        self, prepared: list[tuple[Any, list[tuple[Any, Any, int]]]]
    ) -> list[str]:
        """Detect a native writer that retained a supposedly deleted contour."""
        return [
            "contour remained after Filter write"
            for _, steps in prepared
            for shape, _contour, identifier in steps
            if any(int(item.id) == identifier for item in shape.contours)
        ]

    def retain(self, steps: list[tuple[Any, Any, int]]) -> list[Any]:
        """Pin removed native contours for FontLab's deep history notification."""
        return [contour for _, contour, _identifier in steps]


def apply_filter(
    plugin: Filter,
    values: dict[str, Any],
    *,
    selected: Any = None,
    outlines: Any = None,
    writer: Any = None,
    history: Any = None,
) -> tuple[Any, Any]:
    """Apply one selected-layer plan with exactly one geometry history commit."""
    values = type(plugin).validate(values)
    selected = selected if selected is not None else snapshot.selected_layers()
    outlines = outlines or import_module("fontlabapp.outline_writer")
    writer = writer or import_module("fontlabapp.layer_writer")
    history = history or import_module("fontlabapp.history")
    plan, facts = plan_filter(plugin, values, selected, outlines, history)
    if not plan.work:
        return plan, None
    result = writer.apply_work(
        plan.work, plugin.title, facts, LayerEditEditor(outlines)
    )
    return plan, result

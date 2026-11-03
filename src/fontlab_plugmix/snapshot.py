# this_file: src/fontlab_plugmix/snapshot.py
"""Copy native FontLab glyph data into immutable, Python-only records."""

from collections.abc import Callable
from dataclasses import dataclass
from importlib import import_module
from time import monotonic
from typing import Any


@dataclass(frozen=True)
class Node:
    """A shape-transformed node in layer font units."""

    x: float
    y: float
    on_curve: bool
    selected: bool
    smooth: bool = False


@dataclass(frozen=True)
class Contour:
    """Nodes in native contour order."""

    nodes: tuple[Node, ...]
    closed: bool = True


@dataclass(frozen=True)
class Anchor:
    """A named anchor in layer font units."""

    name: str
    x: float
    y: float


@dataclass(frozen=True)
class Zone:
    """One selected-master alignment zone with its outer edge."""

    name: str
    position: float
    edge: float


@dataclass(frozen=True)
class Metrics:
    """Master metrics; italic_slant is positive when the top leans right."""

    ascender: float
    descender: float
    x_height: float
    cap_height: float
    italic_slant: float
    upm: float
    zones: tuple[Zone, ...] = ()


@dataclass(frozen=True)
class GlyphSnapshot:
    """Read-only data needed by reporter computations."""

    contours: tuple[Contour, ...]
    anchors: tuple[Anchor, ...]
    advance: float
    metrics: Metrics
    bounds: tuple[float, float, float, float] | None = None


@dataclass(frozen=True)
class NativeSource:
    """Short-lived handles resolved from one editor glyph item."""

    package: Any
    layer: Any


@dataclass(frozen=True)
class ActiveGlyph:
    """Checked current glyph and its selected-master layer for palette actions."""

    package: Any
    glyph: Any
    layer: Any


def active_glyph(
    fontlab: Any,
    *,
    items: Callable[[Callable[[], Any]], list[Any]] | None = None,
) -> ActiveGlyph | None:
    """Resolve the active canvas slot against the workspace's current package."""
    workspace = fontlab.flWorkspace.instance()
    package = workspace.currentPackage
    if package is None or package.isNull or workspace.activeFontPanel is not None:
        return None
    canvas = workspace.getActiveCanvas()
    if canvas is None or canvas.isNull:
        return None
    if items is None:
        items = import_module("fontlabapp.qtsafe").qt_list
    for block in items(canvas.textBlocks):
        for index in range(int(block.glyphsCount())):
            info = block.getGlyphAt(index)
            if info is None or not info.isActive:
                continue
            glyph = info.glyph
            if (
                glyph is None
                or glyph.isNull
                or int(glyph.package.id) != int(package.id)
            ):
                return None
            name = str(info.symbol.layerName)
            layer = glyph.findLayer(name or package.master)
            return (
                None
                if layer is None or layer.isNull
                else ActiveGlyph(package, glyph, layer)
            )
    return None


def palette_key(
    active: ActiveGlyph | None,
    *,
    items: Callable[[Callable[[], Any]], list[Any]] | None = None,
) -> tuple[Any, ...] | None:
    """Read a cheap revision and node-selection key without a full snapshot."""
    if active is None:
        return None
    if items is None:
        items = import_module("fontlabapp.qtsafe").qt_list
    stamp = active.glyph.lastModified
    revision = (
        stamp.toMSecsSinceEpoch() if hasattr(stamp, "toMSecsSinceEpoch") else stamp
    )
    # This checks every native node each tick; keep capture itself behind the key.
    selected = []
    for shape in items(lambda: active.layer.shapes):
        if shape.isComponent:
            continue
        for contour in items(lambda shape=shape: shape.contours):
            selected.append(tuple(bool(node.selected) for node in items(contour.nodes)))
    return (
        int(active.package.id),
        int(active.glyph.id),
        str(active.package.master),
        revision,
        tuple(selected),
    )


def selected_layers() -> Any:
    """Read the active Font/Glyph window selection through App's checked adapter."""
    return import_module("fontlabapp.layer_selection").capture(monotonic() + 2)


def select_contours(
    layer: Any,
    indices: tuple[int, ...],
    *,
    toggle: bool = False,
    items: Callable[[Callable[[], Any]], list[Any]] | None = None,
) -> None:
    """Select whole editable contours by index; never change outline geometry."""
    items = items or import_module("fontlabapp.qtsafe").qt_list
    contours = [
        contour
        for shape in items(lambda: layer.shapes)
        if not shape.isComponent
        for contour in items(lambda shape=shape: shape.contours)
    ]
    targets = set(indices)
    for index, contour in enumerate(contours):
        nodes = items(contour.nodes)
        if toggle:
            if index in targets:
                selected = not all(bool(node.selected) for node in nodes)
                for node in nodes:
                    node.selected = selected
        else:
            for node in nodes:
                node.selected = index in targets


def resolve_source(info: Any) -> NativeSource | None:
    """Use the same glyph → current-master layer path as anchor rings."""
    glyph = info.glyph
    if glyph is None or glyph.isNull:
        return None
    package = glyph.package
    layer = glyph.findLayer(package.master)
    if layer is None or layer.isNull:
        return None
    return NativeSource(package, layer)


def _contours(
    layer: Any, items: Callable[[Callable[[], Any]], list[Any]]
) -> tuple[Contour, ...]:
    """Read editable outlines and apply each shape's native transform."""
    rows = []
    for shape in items(lambda: layer.shapes):
        if shape.isComponent:
            continue
        for contour in items(lambda shape=shape: shape.contours):
            nodes = []
            for node in items(contour.nodes):
                point = shape.transform.map(node.position)
                nodes.append(
                    Node(
                        float(point.x()),
                        float(point.y()),
                        bool(node.isOn()),
                        bool(node.selected),
                        bool(getattr(node, "smooth", False)),
                    )
                )
            rows.append(Contour(tuple(nodes), bool(getattr(contour, "closed", True))))
    return tuple(rows)


def _zones(
    package: Any, items: Callable[[Callable[[], Any]], list[Any]]
) -> tuple[Zone, ...]:
    """Read the selected master's native PostScript top and bottom zones."""
    zones = []
    for field, direction in (("ps_zonesT", 1), ("ps_zonesB", -1)):
        for item in items(lambda field=field: getattr(package, field, ())):
            position = float(item.position)
            zones.append(
                Zone(str(item.name), position, position + direction * float(item.width))
            )
    return tuple(zones)


def _bounds(layer: Any) -> tuple[float, float, float, float] | None:
    """Copy the native ink box, including curve extrema and components."""
    box = getattr(layer, "boundingBox", None)
    if box is None or (box.width() <= 0 and box.height() <= 0):
        return None
    x, y = float(box.x()), float(box.y())
    return x, y, x + float(box.width()), y + float(box.height())


def capture(
    source: NativeSource,
    *,
    fontlab: Any = None,
    items: Callable[[Callable[[], Any]], list[Any]] | None = None,
    include_zones: bool = False,
    include_bounds: bool = False,
) -> GlyphSnapshot:
    """Read one current native layer; inject native adapters in offline tests."""
    if fontlab is None:
        fontlab = import_module("fontlab")
    if items is None:
        items = import_module("fontlabapp.qtsafe").qt_list
    layer, package = source.layer, source.package
    metrics = fontlab.FontMetrics(package, package.master)
    pins = items(lambda: layer.anchors)
    anchors = tuple(
        Anchor(str(pin.name), float(pin.point.x()), float(pin.point.y()))
        for pin in pins
    )
    values = Metrics(
        float(metrics.ascender),
        float(metrics.descender),
        float(metrics.xHeight),
        float(metrics.capsHeight),
        # OpenType post uses counter-clockwise degrees from vertical.
        -float(package.italicAngle_value),
        float(package.upm),
        _zones(package, items) if include_zones else (),
    )
    return GlyphSnapshot(
        _contours(layer, items),
        anchors,
        float(layer.advanceWidth),
        values,
        _bounds(layer) if include_bounds else None,
    )

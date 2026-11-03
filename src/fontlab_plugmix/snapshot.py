# this_file: src/fontlab_plugmix/snapshot.py
"""Copy native FontLab glyph data into immutable, Python-only records."""

from collections.abc import Callable
from dataclasses import dataclass
from importlib import import_module
from typing import Any


@dataclass(frozen=True)
class Node:
    """A shape-transformed node in layer font units."""

    x: float
    y: float
    on_curve: bool
    selected: bool


@dataclass(frozen=True)
class Contour:
    """Nodes in native contour order."""

    nodes: tuple[Node, ...]


@dataclass(frozen=True)
class Anchor:
    """A named anchor in layer font units."""

    name: str
    x: float
    y: float


@dataclass(frozen=True)
class Metrics:
    """Current master metrics in font units and italic degrees."""

    ascender: float
    descender: float
    x_height: float
    cap_height: float
    italic_angle: float


@dataclass(frozen=True)
class GlyphSnapshot:
    """Read-only data needed by reporter computations."""

    contours: tuple[Contour, ...]
    anchors: tuple[Anchor, ...]
    advance: float
    metrics: Metrics


@dataclass(frozen=True)
class NativeSource:
    """Short-lived handles resolved from one editor glyph item."""

    package: Any
    layer: Any


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
                    )
                )
            rows.append(Contour(tuple(nodes)))
    return tuple(rows)


def capture(
    source: NativeSource,
    *,
    fontlab: Any = None,
    items: Callable[[Callable[[], Any]], list[Any]] | None = None,
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
        float(package.italicAngle_value),
    )
    return GlyphSnapshot(
        _contours(layer, items), anchors, float(layer.advanceWidth), values
    )

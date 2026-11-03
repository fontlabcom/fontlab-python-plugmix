# this_file: tests/test_snapshot.py
"""Fake native FontLab objects shaped like the layer and metric APIs."""

from dataclasses import FrozenInstanceError
from types import SimpleNamespace as NS

import pytest

from fontlab_plugmix.snapshot import (
    ActiveGlyph,
    NativeSource,
    active_glyph,
    capture,
    palette_key,
    resolve_source,
)


class Point:
    """Qt-like point with x()/y() accessors."""

    def __init__(self, x, y):
        self._x, self._y = x, y

    def x(self):
        return self._x

    def y(self):
        return self._y


class Transform:
    """Translate points as a fake shape transform."""

    def map(self, point):
        return Point(point.x() + 10, point.y() - 5)


def test_resolve_source_uses_glyph_master_and_ignores_null():
    package = NS(master="Regular")
    layer = NS(isNull=False)
    glyph = NS(isNull=False, package=package, findLayer=lambda master: layer)
    assert resolve_source(NS(glyph=glyph)) == NativeSource(package, layer)
    assert resolve_source(NS(glyph=None)) is None
    assert resolve_source(NS(glyph=NS(isNull=True))) is None
    glyph.findLayer = lambda master: NS(isNull=True)
    assert resolve_source(NS(glyph=glyph)) is None


def test_capture_copies_transformed_nodes_anchors_metrics_immutably():
    package = NS(
        master="Regular",
        italicAngle_value=-12,
        upm=1000,
        ps_zonesT=[NS(name="cap", position=700, width=12)],
        ps_zonesB=[NS(name="baseline", position=0, width=15)],
    )
    node = NS(position=Point(1, 2), isOn=lambda: True, selected=True, smooth=True)
    off = NS(position=Point(3, 4), isOn=lambda: False, selected=False)
    contour = NS(nodes=lambda: [node, off], closed=False)
    outline = NS(isComponent=False, contours=[contour], transform=Transform())
    component = NS(isComponent=True, contours=[contour], transform=Transform())
    layer = NS(
        shapes=[outline, component],
        anchors=[NS(name="top", point=Point(5, 6))],
        advanceWidth=600,
        boundingBox=NS(
            x=lambda: 10, y=lambda: -20, width=lambda: 120, height=lambda: 500
        ),
    )
    metrics = NS(ascender=800, descender=-200, xHeight=500, capsHeight=700)
    fontlab = NS(FontMetrics=lambda pkg, master: metrics)
    snapshot = capture(
        NativeSource(package, layer),
        fontlab=fontlab,
        items=lambda get: list(get()),
        include_zones=True,
        include_bounds=True,
    )
    assert [(n.x, n.y, n.on_curve, n.selected) for n in snapshot.contours[0].nodes] == [
        (11, -3, True, True),
        (13, -1, False, False),
    ]
    assert len(snapshot.contours) == 1
    assert snapshot.contours[0].closed is False
    assert snapshot.contours[0].nodes[0].smooth is True
    assert (snapshot.anchors[0].name, snapshot.anchors[0].x) == ("top", 5)
    assert (
        snapshot.advance,
        snapshot.metrics.cap_height,
        snapshot.metrics.italic_slant,
        snapshot.metrics.upm,
    ) == (600, 700, 12, 1000)
    assert [(z.name, z.position, z.edge) for z in snapshot.metrics.zones] == [
        ("cap", 700, 712),
        ("baseline", 0, -15),
    ]
    assert snapshot.bounds == (10, -20, 130, 480)
    assert (
        capture(
            NativeSource(package, layer), fontlab=fontlab, items=lambda get: list(get())
        ).bounds
        is None
    )
    package.upm = 2048
    package.italicAngle_value = 12
    opposite = capture(
        NativeSource(package, layer), fontlab=fontlab, items=lambda get: list(get())
    )
    assert (opposite.metrics.upm, opposite.metrics.italic_slant) == (2048, -12)
    with pytest.raises(FrozenInstanceError):
        snapshot.advance = 10


def test_palette_active_glyph_and_selection_key_follow_current_master():
    node = NS(selected=False)
    contour = NS(nodes=lambda: [node])
    shape = NS(isComponent=False, contours=[contour])
    layer = NS(isNull=False, shapes=[shape])
    glyph = NS(
        id=7,
        isNull=False,
        package=NS(id=2),
        lastModified=NS(toMSecsSinceEpoch=lambda: 42),
        findLayer=lambda master: layer,
    )
    package = NS(id=2, master="Regular", isNull=False)
    info = NS(isActive=True, glyph=glyph, symbol=NS(layerName=""))
    block = NS(glyphsCount=lambda: 1, getGlyphAt=lambda index: info)
    canvas = NS(isNull=False, textBlocks=lambda: [block])
    workspace = NS(
        currentPackage=package,
        activeFontPanel=None,
        getActiveCanvas=lambda: canvas,
    )
    fontlab = NS(
        flWorkspace=NS(instance=lambda: workspace),
        CurrentGlyph=lambda: (_ for _ in ()).throw(
            AssertionError("legacy glyph API used")
        ),
    )
    active = active_glyph(fontlab, items=lambda get: list(get()))
    assert active == ActiveGlyph(package, glyph, layer)
    first = palette_key(active, items=lambda get: list(get()))
    assert first[3] == 42
    node.selected = True
    assert palette_key(active, items=lambda get: list(get())) != first
    package.master = "Bold"
    assert palette_key(active, items=lambda get: list(get()))[2] == "Bold"
    assert palette_key(None) is None
    info.symbol.layerName = "Alt"
    named = active_glyph(fontlab, items=lambda get: list(get()))
    assert named is not None
    package.isNull = True
    assert active_glyph(fontlab) is None
    package.isNull = False
    workspace.activeFontPanel = object()
    assert active_glyph(fontlab) is None
    workspace.activeFontPanel = None
    workspace.getActiveCanvas = lambda: None
    assert active_glyph(fontlab) is None
    workspace.getActiveCanvas = lambda: canvas
    info.isActive = False
    assert active_glyph(fontlab, items=lambda get: list(get())) is None
    info.isActive = True
    glyph.package.id = 3
    assert active_glyph(fontlab, items=lambda get: list(get())) is None
    glyph.package.id = 2
    glyph.findLayer = lambda master: NS(isNull=True)
    assert active_glyph(fontlab, items=lambda get: list(get())) is None

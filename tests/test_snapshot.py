# this_file: tests/test_snapshot.py
"""Fake native FontLab objects shaped like the layer and metric APIs."""

from dataclasses import FrozenInstanceError
from types import SimpleNamespace as NS

import pytest

from fontlab_plugmix.snapshot import NativeSource, capture, resolve_source


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
    package = NS(master="Regular", italicAngle_value=12)
    node = NS(position=Point(1, 2), isOn=lambda: True, selected=True)
    off = NS(position=Point(3, 4), isOn=lambda: False, selected=False)
    contour = NS(nodes=lambda: [node, off])
    outline = NS(isComponent=False, contours=[contour], transform=Transform())
    component = NS(isComponent=True, contours=[contour], transform=Transform())
    layer = NS(
        shapes=[outline, component],
        anchors=[NS(name="top", point=Point(5, 6))],
        advanceWidth=600,
    )
    metrics = NS(ascender=800, descender=-200, xHeight=500, capsHeight=700)
    fontlab = NS(FontMetrics=lambda pkg, master: metrics)
    snapshot = capture(
        NativeSource(package, layer), fontlab=fontlab, items=lambda get: list(get())
    )
    assert [(n.x, n.y, n.on_curve, n.selected) for n in snapshot.contours[0].nodes] == [
        (11, -3, True, True),
        (13, -1, False, False),
    ]
    assert len(snapshot.contours) == 1
    assert (snapshot.anchors[0].name, snapshot.anchors[0].x) == ("top", 5)
    assert (
        snapshot.advance,
        snapshot.metrics.cap_height,
        snapshot.metrics.italic_angle,
    ) == (600, 700, 12)
    with pytest.raises(FrozenInstanceError):
        snapshot.advance = 10

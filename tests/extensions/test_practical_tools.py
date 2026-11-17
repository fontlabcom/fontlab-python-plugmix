# this_file: tests/extensions/test_practical_tools.py
"""Practical tools exercise real bundle loading with immutable host snapshots."""

import sys
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace as NS

import pytest
from fontlabapp.plugins.bundles import load_bundle
from fontlabapp.plugins.snapshot import Component, Contour, Node
from fontlabapp.plugins.tool import ToolEvent

ROOT = Path(__file__).resolve().parents[2] / "Extensions/tools"


def bundle(name):
    cls = load_bundle(ROOT / f"{name}.fontlabtool")
    return cls(), sys.modules[cls.__module__]


def event(x=0, y=0, **kwargs):
    return ToolEvent(x, y, x, y, **kwargs)


def context(glyph):
    calls = []
    return NS(
        snapshot=lambda: glyph,
        redraw=lambda: calls.append("redraw"),
        select=lambda indices, **kw: calls.append((indices, kw)),
        calls=calls,
    )


def test_ruler_pure_measurement_and_axis_constraints():
    _, module = bundle("MeasurementRuler")
    marks = module.measurement_marks((0, 0), (3, 4))
    assert marks[0].points == ((0, 0), (3, 4))
    assert "5.00" in marks[1].text and "53.13" in marks[1].text
    assert "0.00" in module.measurement_marks((1, 1), (1, 1))[1].text
    assert module.endpoint((0, 0), event(3, 4, shift=True)) == (0, 4)
    assert module.endpoint((0, 0), event(-4, -3, shift=True)) == (-4, 0)
    assert module.endpoint((0, 0), event(3, 4)) == (3, 4)


def test_ruler_lifecycle_and_context_loss(glyph):
    plugin, _ = bundle("MeasurementRuler")
    ctx = context(glyph)
    assert not plugin.press(event()) and not plugin.move(event())
    assert not plugin.release(event()) and plugin.marks(glyph) == []
    plugin.activate(ctx)
    assert not plugin.press(event(buttons=2))
    assert plugin.press(event(buttons=1))
    assert not plugin.move(event(3, 4))
    assert plugin.move(event(3, 4, buttons=1))
    assert plugin.release(event(3, 4))
    assert "5.00" in plugin.marks(glyph)[1].text
    assert not plugin.move(event(5, 6, buttons=1))
    assert not plugin.key_down(event(key="a"))
    assert plugin.key_down(event(key="\x1b"))
    assert plugin.marks(glyph) == []
    plugin.press(event(buttons=1))
    assert plugin.marks(replace(glyph, source_key=(1, 2, 3, "other"))) == []
    assert not plugin.release(event(4, 5))
    ctx.snapshot = lambda: None
    assert not plugin.press(event(buttons=1))
    ctx.snapshot = lambda: glyph
    plugin.press(event(buttons=1))
    ctx.snapshot = lambda: None
    assert not plugin.move(event(buttons=1))
    plugin.deactivate()
    assert plugin.ctx is None and plugin.marks(glyph) == []


def test_probe_exact_coordinates_components_and_qcurve_nodes(glyph):
    plugin, module = bundle("NodeProbe")
    qcurve = Contour(
        (
            Node(0, 0, True, False),
            Node(20, 30, False, False),
            Node(30, 40, False, False),
            Node(60, 0, True, False),
        ),
        closed=False,
    )
    component = Component(
        "acute", (1, 0, 0, 1, 0, 0), (Contour((Node(200, 300, True, False),)),)
    )
    data = replace(glyph, contours=(qcurve,), components=(component,))
    assert module.nearest_node(data, (20, 30), 1)[0] == "local 0:1"
    assert module.nearest_node(data, (200, 300), 1)[0] == "component 0 acute 0:0"
    assert module.nearest_node(data, (500, 500), 1) is None
    assert (
        module.nearest_node(replace(data, contours=(), components=()), (0, 0), 1)
        is None
    )
    for scale in (0, -1, float("nan"), float("inf")):
        assert module.nearest_node(data, (0, 0), scale) is None
    assert module.nearest_node(data, (6, 0), 2) is not None
    assert module.nearest_node(data, (6.1, 0), 2) is None
    assert plugin.needs_components
    assert not plugin.move(event())
    ctx = context(data)
    plugin.activate(ctx)
    assert plugin.move(event(20, 30))
    assert "off-curve" in plugin.marks(data)[1].text
    assert "20.00, 30.00" in plugin.marks(data)[1].text
    assert plugin.move(event(200, 300))
    assert "on-curve" in plugin.marks(data)[1].text
    assert plugin.marks(None) == []
    assert plugin.move(event(900, 900)) and plugin.marks(data) == []
    plugin.move(event())
    assert plugin.marks(replace(data, source_key=(1, 2, 3, "new"))) == []
    ctx.snapshot = lambda: None
    assert not plugin.move(event())
    plugin.deactivate()
    assert plugin.marks(data) == []


def test_picker_local_nodes_only_and_shift_toggle(glyph):
    plugin, module = bundle("ContourPicker")
    open_curve = Contour((Node(100, 100, False, False),), closed=False)
    component = Component("base", (1, 0, 0, 1, 0, 0), (open_curve,))
    data = replace(glyph, contours=(Contour(()), open_curve), components=(component,))
    assert module.nearest_contour(data, (100, 100), 1) == 1
    assert module.nearest_contour(replace(data, contours=()), (100, 100), 1) is None
    for scale in (0, -1, float("nan"), float("inf")):
        assert module.nearest_contour(data, (100, 100), scale) is None
    assert not plugin.press(event(buttons=1))
    ctx = context(data)
    plugin.activate(ctx)
    assert not plugin.press(event(100, 100, buttons=2))
    assert plugin.press(event(100, 100, buttons=1, shift=True))
    assert ctx.calls[-1] == ((1,), {"toggle": True})
    assert plugin.press(event(100, 100, buttons=1))
    assert ctx.calls[-1] == ((1,), {"toggle": False})
    assert not plugin.press(event(500, 500, buttons=1))
    ctx.snapshot = lambda: None
    assert not plugin.press(event(buttons=1))
    plugin.deactivate()
    assert plugin.ctx is None


@pytest.mark.parametrize("name", ["MeasurementRuler", "NodeProbe", "ContourPicker"])
def test_tools_use_real_bridge_lifetime_and_contain_callback_failure(name, glyph):
    from fontlabapp.plugins.tools.bridge import ToolBridge

    plugin, _ = bundle(name)
    calls, errors = [], []
    painters = NS(
        register=lambda *args: calls.append("register") or 7,
        remove=lambda token: calls.append(("remove", token)),
    )
    bridge = ToolBridge(
        plugin,
        NS(painters=painters, qt=object(), sink=lambda *args: errors.append(args)),
    )
    assert bridge.activate() and bridge.activate()
    assert calls == ["register"]
    assert bridge.painter.compute(glyph) == []
    assert bridge.context.needs_components == plugin.needs_components
    assert bridge.deactivate() and bridge.deactivate()
    assert calls == ["register", ("remove", 7)]
    assert plugin.ctx is None

    def failed_snapshot():
        raise RuntimeError("native read refused")

    ctx = context(glyph)
    ctx.snapshot = failed_snapshot
    plugin.activate(ctx)
    method = plugin.move if name == "NodeProbe" else plugin.press
    assert not bridge._call("test", lambda: method(event(buttons=1)))
    assert len(errors) == 1 and "native read refused" in str(errors[0][0])


def test_nearest_node_ties_and_closed_quadratic_controls(glyph):
    _, probe = bundle("NodeProbe")
    _, picker = bundle("ContourPicker")
    quadratic = Contour(
        (
            Node(0, 0, False, False),
            Node(20, 0, False, False),
            Node(20, 20, False, False),
            Node(0, 20, False, False),
        )
    )
    component = Component("duplicate", (1, 0, 0, 1, 0, 0), (quadratic,))
    data = replace(glyph, contours=(quadratic, quadratic), components=(component,))
    assert probe.nearest_node(data, (0, 0), 1)[0] == "local 0:0"
    assert picker.nearest_contour(data, (0, 0), 1) == 0
    assert picker.nearest_contour(data, (-6, 0), 2) == 0
    assert picker.nearest_contour(data, (-6.1, 0), 2) is None


def test_picker_changes_selection_through_real_host_selector_only(glyph):
    from fontlabapp.plugins.snapshot import select_contours

    plugin, _ = bundle("ContourPicker")
    native_nodes = [NS(x=0, y=0, selected=False), NS(x=10, y=0, selected=False)]
    other = NS(x=100, y=100, selected=True)
    component_node = NS(x=0, y=0, selected=False)
    layer = NS(
        shapes=[
            NS(isComponent=True, contours=[NS(nodes=lambda: [component_node])]),
            NS(
                isComponent=False,
                contours=[NS(nodes=lambda: native_nodes), NS(nodes=lambda: [other])],
            ),
        ]
    )
    data = replace(
        glyph,
        contours=(
            Contour((Node(0, 0, True, False), Node(10, 0, True, False))),
            Contour((Node(100, 100, True, True),)),
        ),
    )
    ctx = context(data)
    ctx.select = lambda indices, **kw: select_contours(
        layer, indices, items=lambda fn: list(fn()), **kw
    )
    plugin.activate(ctx)
    assert plugin.press(event(buttons=1))
    assert all(node.selected for node in native_nodes)
    assert not other.selected and not component_node.selected
    assert plugin.press(event(buttons=1, shift=True))
    assert not any(node.selected for node in native_nodes)
    assert [(node.x, node.y) for node in native_nodes] == [(0, 0), (10, 0)]


def test_ruler_keeps_drag_when_another_button_is_released(glyph):
    plugin, _ = bundle("MeasurementRuler")
    ctx = context(glyph)
    plugin.activate(ctx)
    assert plugin.press(event(buttons=1))
    assert plugin.move(event(3, 4, buttons=1))
    redraws = len(ctx.calls)
    assert not plugin.release(event(8, 9, buttons=1))
    assert plugin.dragging and plugin.end == (3, 4)
    assert len(ctx.calls) == redraws
    assert plugin.move(event(6, 8, buttons=1))
    assert plugin.release(event(6, 8, buttons=2))
    assert not plugin.dragging
    assert "10.00" in plugin.marks(glyph)[1].text

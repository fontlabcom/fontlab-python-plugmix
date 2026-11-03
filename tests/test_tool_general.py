# this_file: tests/test_tool_general.py
"""Fake-native Tool and General registration, mapping and lifecycle tests."""

import json
from types import SimpleNamespace as NS
from typing import ClassVar

import pytest

from fontlab_plugmix import General, Tool, registry
from fontlab_plugmix.backend import active_glyph_map
from fontlab_plugmix.general import GeneralContext
from fontlab_plugmix.general_plugins.host import GeneralHost
from fontlab_plugmix.general_plugins.zoom_to_selection import ZoomToSelection
from fontlab_plugmix.kinds import Services
from fontlab_plugmix.palettes.host import PaletteHost
from fontlab_plugmix.snapshot import select_contours
from fontlab_plugmix.tool import ToolContext, ToolEvent
from fontlab_plugmix.tools.bridge import ToolBridge
from fontlab_plugmix.tools.host import ToolHost, UnsupportedCapability
from fontlab_plugmix.tools.smart_select import SmartSelect, touched_contours


class Signal:
    def __init__(self):
        self.slots = []

    def connect(self, fn):
        self.slots.append(fn)

    def disconnect(self, fn):
        self.slots.remove(fn)

    def emit(self):
        for fn in tuple(self.slots):
            fn()


class Timer:
    created: ClassVar[list] = []

    def __init__(self):
        self.timeout = Signal()
        self.running = self.deleted = False
        self.created.append(self)

    def setInterval(self, interval):
        self.interval = interval

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def deleteLater(self):
        self.deleted = True


class Point:
    def __init__(self, x, y):
        self._x, self._y = x, y

    def x(self):
        return self._x

    def y(self):
        return self._y


class KeySequence:
    """PythonQt-shaped sequence with a canonical display string."""

    def __init__(self, text):
        parts = [part.strip().lower() for part in text.split("+") if part.strip()]
        self.text = "+".join(
            "Ctrl" if part == "ctrl" else part.title() for part in parts
        )

    def toString(self):
        return self.text


class Transform:
    def __init__(self, dx=0, dy=0):
        self._dx, self._dy = dx, dy

    def map(self, point):
        return Point(point.x() + self._dx, point.y() + self._dy)

    def m11(self):
        return 1

    def m12(self):
        return 0

    def m21(self):
        return 0

    def m22(self):
        return 1

    def dx(self):
        return self._dx

    def dy(self):
        return self._dy


class Canvas:
    isNull = False

    def __init__(self, active=True, zoom=0.5, scroll=(20, 30)):
        self.info = NS(isActive=active, transform=Transform(60, 5))
        self.block = NS(
            transform=Transform(10, 3),
            getAllGlyphs=lambda: [NS(isActive=False), self.info],
        )
        self.textBlocks = lambda: [self.block]
        self.viewPort = NS(
            mapFromGlobal=lambda point: Point(point.x() - 10, point.y() - 20)
        )
        self.zoomed = []
        self._zoom, self._scroll = zoom, scroll

    def mapFromViewport(self, point):
        return Point(
            (point.x() - self._scroll[0]) / self._zoom,
            (point.y() - self._scroll[1]) / self._zoom,
        )

    def scale(self):
        return self._zoom

    def zoomTo(self, rect):
        self.zoomed.append(rect)


class Menus:
    def __init__(self):
        self.actions = {}
        self.removed = []
        self.messages = []

    def add_action(self, section, title, callback, *, checkable):
        token = len(self.actions) + len(self.removed) + 1
        action = NS(checked=False, enabled=True, shortcut=KeySequence(""))
        action.setChecked = lambda value: setattr(action, "checked", value)
        action.setEnabled = lambda value: setattr(action, "enabled", value)

        def set_shortcut(value):
            assert isinstance(value, KeySequence)
            action.shortcut = value
            action.shortcut_set = value

        action.setShortcut = set_shortcut
        self.actions[token] = (section, title, callback, action)
        return token

    def action(self, token):
        return self.actions[token][3]

    def remove(self, token):
        self.removed.append(token)
        self.actions.pop(token)

    def main_window(self):
        return NS(
            findChildren=lambda cls: [],
            statusBar=lambda: NS(showMessage=self.messages.append),
        )


class Workspace:
    def __init__(self):
        self.registered = []
        self.removed = []
        self.fonts = [NS(id=9001, fgId=1)]
        self.canvas = Canvas()

    def registerPythonTool(self, title, icon, bridge):
        self.registered.append((title, icon, bridge))
        return len(self.registered)

    def unregisterPythonTool(self, token):
        self.removed.append(token)

    def packages(self):
        # Native items are flObject wrappers carrying only id; fgId needs flPackage(item).
        return [NS(id=font.id) for font in self.fonts]

    def package(self, item):
        return next(font for font in self.fonts if font.id == item.id)

    def getActiveCanvas(self):
        return self.canvas


def environment(tmp_path):
    Timer.created.clear()
    workspace, menus, errors, painters = Workspace(), Menus(), [], NS(calls=[])
    painters.register = lambda obj, qt, sink: (
        painters.calls.append(("add", obj)) or len(painters.calls)
    )
    painters.remove = lambda token: painters.calls.append(("remove", token))
    qt = NS(
        private=NS(QObject=object),
        QtCore=NS(
            QTimer=Timer,
            QPointF=Point,
            QRectF=lambda *parts: parts,
            Qt=NS(ShiftModifier=1, AltModifier=2, ControlModifier=4, MetaModifier=8),
        ),
        QtGui=NS(
            QAction=object,
            QKeySequence=KeySequence,
            QCursor=NS(pos=lambda: Point(77.5, 79)),
        ),
    )
    fontlab = NS(
        flWorkspace=NS(instance=lambda: workspace),
        flPackage=workspace.package,
        UpdateActiveCanvas=lambda: None,
    )
    services = Services(
        qt, fontlab, menus, painters, lambda error, owner: errors.append(str(error))
    )
    return services, registry.Registry(tmp_path), workspace, errors


def mouse(x, y, *, buttons=1, modifiers=0, broken=False):
    return NS(
        localPos=lambda: (
            (_ for _ in ()).throw(TypeError("bad position")) if broken else Point(x, y)
        ),
        buttons=lambda: buttons,
        modifiers=lambda: modifiers,
        text=lambda: "a",
    )


def test_registry_kinds_and_old_preferences(tmp_path):
    state = registry.Registry(tmp_path)
    assert set(state.available("tool")) == {"smart_select"}
    assert set(state.available("general")) == {"zoom_to_selection"}
    assert not {"smart_select", "zoom_to_selection"} & set(state.available("reporter"))
    assert not {"smart_select", "zoom_to_selection"} & set(state.available("filter"))
    assert not {"smart_select", "zoom_to_selection"} & set(state.available("palette"))
    from fontlab_plugmix import menu
    from fontlab_plugmix.filters.host import FilterHost

    services, _, _, _ = environment(tmp_path)
    menu.install(services.menus, state)
    FilterHost(services, state).install()
    PaletteHost(services, state).install()
    titles = [row[1] for row in services.menus.actions.values()]
    assert not any(
        "Smart Select" in title or "Zoom to Selection" in title for title in titles
    )
    state.enable("node_indexes")
    saved = json.loads(state.path.read_text())
    assert "enabled_tools" not in saved and "enabled_general" not in saved
    state.set_tool_enabled("smart_select", False)
    state.set_general_enabled("zoom_to_selection", False)
    assert registry.Registry(tmp_path).enabled_tools() == ()
    assert registry.Registry(tmp_path).enabled_general() == ()
    state.path.write_text('{"enabled": ["node_indexes"], "enabled_palettes": []}')
    old = registry.Registry(tmp_path)
    assert old.enabled_tools() == ("smart_select",)
    assert old.enabled_general() == ("zoom_to_selection",)
    with pytest.raises(KeyError):
        state.set_tool_enabled("missing", True)
    with pytest.raises(KeyError):
        state.set_general_enabled("missing", True)


def test_tool_mapping_accounts_for_zoom_scroll_and_later_glyph(tmp_path):
    services, _, workspace, errors = environment(tmp_path)
    seen = []

    class Probe(Tool):
        def press(self, event):
            seen.append(event)
            return True

    bridge = ToolBridge(Probe(), services)
    assert bridge.activate()
    # glyph (25, 50) -> canvas (95, 58); viewport varies with zoom and scroll.
    for zoom, scroll in ((0.5, (20, 30)), (2, (-13, 44))):
        workspace.canvas = Canvas(zoom=zoom, scroll=scroll)
        px, py = 95 * zoom + scroll[0], 58 * zoom + scroll[1]
        assert bridge.mousePressed(mouse(px, py, modifiers=1), workspace.canvas), errors
        assert (seen[-1].x, seen[-1].y, seen[-1].scale, seen[-1].shift) == (
            25,
            50,
            zoom,
            True,
        )
    assert active_glyph_map(Canvas(active=False)) is None
    assert bridge.deactivate() and errors == []


@pytest.mark.parametrize(
    "method,key_event",
    [
        ("mousePressed", False),
        ("mouseMoved", False),
        ("mouseReleased", False),
        ("mouseDoubleClicked", False),
        ("keyPressed", True),
        ("keyReleased", True),
    ],
)
def test_tool_bridge_each_callback_contains_native_event_errors(
    tmp_path, method, key_event
):
    services, _state, workspace, errors = environment(tmp_path)
    bridge = ToolBridge(Tool(), services)
    assert bridge.activate()
    event = mouse(0, 0, broken=True)
    if key_event:
        event.modifiers = lambda: (_ for _ in ()).throw(TypeError("bad modifiers"))
    assert getattr(bridge, method)(event, workspace.canvas) is False
    assert errors == ["bad modifiers" if key_event else "bad position"]
    bridge.deactivate()


def test_tool_activation_failure_removes_painter(tmp_path):
    services, _state, _workspace, errors = environment(tmp_path)

    class Broken(Tool):
        def activate(self, ctx):
            raise TypeError("activate failed")

    bridge = ToolBridge(Broken(), services)
    assert not bridge.activate()
    assert services.painters.calls[-1][0] == "remove"
    assert bridge.paint_token is None and not bridge.active
    assert errors == ["activate failed"]


def test_tool_bridge_all_callbacks_guard_errors_and_overlay_teardown(tmp_path, glyph):
    services, _, workspace, errors = environment(tmp_path)

    class Probe(Tool):
        def activate(self, ctx):
            self.ctx = ctx

        def deactivate(self):
            raise ValueError("deactivate failed")

        def press(self, event):
            raise RuntimeError("press failed")

        def move(self, event):
            return True

        def release(self, event):
            return True

        def double_click(self, event):
            return True

        def key_down(self, event):
            return True

        def key_up(self, event):
            return True

        def marks(self, glyph):
            return []

    bridge = ToolBridge(Probe(), services)
    assert bridge.mousePressed(mouse(0, 0), workspace.canvas) is False
    assert bridge.activate()
    assert bridge.painter.compute(glyph) == []
    assert not bridge.mousePressed(mouse(0, 0), workspace.canvas)
    assert not bridge.mousePressed(mouse(0, 0), workspace.canvas)
    assert not bridge.mouseMoved(mouse(0, 0, broken=True), workspace.canvas)
    assert bridge.mouseMoved(mouse(20, 30), workspace.canvas), errors
    assert bridge.mouseReleased(mouse(20, 30), workspace.canvas)
    assert bridge.mouseDoubleClicked(mouse(20, 30), workspace.canvas)
    assert bridge.keyPressed(mouse(0, 0), workspace.canvas) is False
    assert bridge.keyReleased(mouse(0, 0), workspace.canvas) is False
    assert bridge.mouseReleased(mouse(0, 0), None) is False
    assert not bridge.deactivate()
    assert services.painters.calls[-1][0] == "remove"
    assert bridge.deactivate() and not bridge.active
    assert errors.count("press failed") == 1
    assert "deactivate failed" in errors and "bad position" in errors


def test_tool_host_registration_missing_hook_and_persistence(tmp_path):
    services, state, workspace, errors = environment(tmp_path)
    host = ToolHost(services, state)
    host.install()
    assert workspace.registered[0][:2] == ("Smart Select", None)
    assert host.registered["smart_select"].bridge is workspace.registered[0][2]
    assert host.toggle("smart_select") is False and workspace.removed == [1]
    assert state.enabled_tools() == ()
    assert host.toggle("smart_select") and len(workspace.registered) == 2
    host.close()
    assert workspace.removed == [1, 2] and not host.actions and errors == []
    services.fontlab.flWorkspace.instance = lambda: NS(packages=list)
    missing = ToolHost(services, registry.Registry(tmp_path))
    missing.install()
    action = services.menus.action(missing.actions["smart_select"])
    assert not action.enabled and not action.checked
    assert any("registerPythonTool" in error for error in errors)
    missing.close()


def test_tool_host_typed_missing_hook_and_failed_register(tmp_path):
    services, state, workspace, errors = environment(tmp_path)
    services.fontlab.flWorkspace.instance = lambda: NS()
    host = ToolHost(services, state)
    with pytest.raises(UnsupportedCapability):
        host._register("smart_select")
    workspace.registerPythonTool = lambda *args: (_ for _ in ()).throw(
        TypeError("native failed")
    )
    services.fontlab.flWorkspace.instance = lambda: workspace
    host.install()
    assert errors == ["native failed"] and not host.registered
    host.close()


def test_tool_host_keeps_bridge_if_native_unregister_fails(tmp_path):
    services, state, workspace, errors = environment(tmp_path)
    host = ToolHost(services, state)
    host.install()
    bridge = host.registered["smart_select"].bridge
    workspace.unregisterPythonTool = lambda token: (_ for _ in ()).throw(
        TypeError("unregister failed")
    )
    try:
        host.close()
        assert ToolHost._retained[-1].bridge is bridge
        assert not bridge.active and not host.actions
        assert errors == ["unregister failed"]
    finally:
        ToolHost._retained.clear()


def test_tool_toggle_rolls_back_native_registration_on_save_failure(tmp_path):
    services, state, workspace, errors = environment(tmp_path)
    host = ToolHost(services, state)
    host.install()
    original = state.set_tool_enabled
    state.set_tool_enabled = lambda *args: (_ for _ in ()).throw(
        OSError("read-only prefs")
    )
    with pytest.raises(OSError, match="read-only prefs"):
        host.toggle("smart_select")
    assert "smart_select" in host.registered
    state.set_tool_enabled = original
    host.toggle("smart_select")
    state.set_tool_enabled = lambda *args: (_ for _ in ()).throw(
        OSError("read-only prefs")
    )
    with pytest.raises(OSError, match="read-only prefs"):
        host.toggle("smart_select")
    assert "smart_select" not in host.registered
    assert workspace.removed == [1, 2, 3]
    assert errors == []
    host.close()


def test_smart_select_rectangle_and_native_selection_flags(glyph):
    tool = SmartSelect()
    chosen = []
    ctx = NS(
        snapshot=lambda: glyph,
        select=lambda indices, **kw: chosen.append((indices, kw)),
        redraw=lambda: None,
    )
    tool.activate(ctx)
    assert not tool.move(ToolEvent(1, 1, 0, 0, buttons=1))
    assert tool.press(ToolEvent(-1, -1, 0, 0))
    assert tool.move(ToolEvent(90, 90, 0, 0, buttons=1))
    assert len(tool.marks(glyph)) == 1
    assert tool.release(ToolEvent(90, 90, 0, 0, shift=True))
    assert chosen == [((0,), {"toggle": True})]
    assert tool.marks(glyph) == [] and not tool.release(ToolEvent(0, 0, 0, 0))
    assert touched_contours(glyph, (200, 200), (300, 300)) == ()
    tool.deactivate()
    nodes = [NS(selected=False), NS(selected=True)]
    contour = NS(nodes=lambda: nodes)
    layer = NS(shapes=[NS(isComponent=False, contours=[contour])])
    select_contours(layer, (0,), items=lambda call: list(call()))
    assert all(node.selected for node in nodes)
    select_contours(layer, (0,), toggle=True, items=lambda call: list(call()))
    assert not any(node.selected for node in nodes)


def test_general_shared_timer_font_difference_and_action_teardown(
    tmp_path, monkeypatch
):
    services, state, workspace, errors = environment(tmp_path)
    seen = []

    class Probe(General):
        name, title = "probe_general", "Probe General"

        def start(self, ctx):
            self.ctx = ctx
            ctx.menus.add_action("View", "Extra", lambda: None, checkable=False)
            seen.append("start")

        def stop(self):
            seen.append("stop")

        def run(self):
            seen.append("run")

        def on_font_opened(self, font_id):
            seen.append(("open", font_id))

        def on_font_closed(self, font_id):
            seen.append(("close", font_id))

    classes = state.available()
    classes[Probe.name] = Probe
    monkeypatch.setattr(
        state,
        "available",
        lambda kind=None: {
            k: v for k, v in classes.items() if kind is None or v.kind == kind
        },
    )
    state.set_palette_enabled("step_and_repeat", False)
    palettes = PaletteHost(services, state)
    palettes.install()
    palette_ticks = []
    palettes.panels["fake"] = NS(visible=True)
    palettes._poll = lambda: palette_ticks.append(1)
    palettes._timer()
    general = GeneralHost(services, state, palettes)
    general.install()
    assert len(Timer.created) == 1 and Timer.created[0].running
    assert seen == ["start"]
    command = general.running[Probe.name].token
    services.menus.actions[command][2]()
    assert seen[-1] == "run"
    workspace.fonts = [NS(id=12345, fgId=1)]
    Timer.created[0].timeout.emit()
    assert seen == ["start", "run"]
    workspace.fonts = [NS(id=9002, fgId=2)]
    Timer.created[0].timeout.emit()
    Timer.created[0].timeout.emit()
    assert palette_ticks == [1, 1, 1]
    assert seen[-2:] == [("open", 2), ("close", 1)]
    general.close()
    assert seen[-1] == "stop" and command not in services.menus.actions
    assert all(row[1] != "Extra" for row in services.menus.actions.values())
    assert Timer.created[0].running and errors == []
    palettes.panels.pop("fake")
    palettes._sync_timer()
    assert not Timer.created[0].running
    palettes.close()


def test_general_start_failure_unwinds_action_and_owned_timer(tmp_path, monkeypatch):
    services, state, _workspace, errors = environment(tmp_path)

    class Broken(General):
        name, title = "broken", "Broken"

        def start(self, ctx):
            ctx.timer(100, lambda: None)
            raise ValueError("start failed")

    classes = state.available()
    classes[Broken.name] = Broken
    monkeypatch.setattr(
        state,
        "available",
        lambda kind=None: {
            k: v for k, v in classes.items() if kind is None or v.kind == kind
        },
    )
    palettes = PaletteHost(services, state)
    palettes.install()
    host = GeneralHost(services, state, palettes)
    host.install()
    assert "broken" not in host.running and "start failed" in errors
    assert all(row[1] != "Broken" for row in services.menus.actions.values())
    assert Timer.created[0].deleted
    host.close()
    palettes.close()


def test_general_context_zoom_notify_and_timer_errors(tmp_path, monkeypatch, glyph):
    services, _state, workspace, errors = environment(tmp_path)
    plugin = ZoomToSelection()
    ctx = GeneralContext(services, plugin)
    plugin.start(ctx)
    monkeypatch.setattr(
        "fontlab_plugmix.general.snapshot.active_glyph",
        lambda fontlab: NS(package=object(), layer=object()),
    )
    monkeypatch.setattr(
        "fontlab_plugmix.general.snapshot.capture", lambda *args, **kw: glyph
    )
    assert ctx.zoom_selected()
    assert workspace.canvas.zoomed and workspace.canvas.zoomed[0][2] > 50
    assert plugin.run() is None
    monkeypatch.setattr(
        "fontlab_plugmix.general.snapshot.capture", lambda *args, **kw: NS(contours=())
    )
    plugin.run()
    assert "Select nodes" in services.menus.messages[-1]
    timer = ctx.timer(75, lambda: (_ for _ in ()).throw(ValueError("tick failed")))
    timer.timeout.emit()
    assert errors == ["tick failed"]
    ctx.close()
    assert timer.deleted
    plugin.stop()


def test_general_context_edit_and_tool_context_workspace_read(
    tmp_path, monkeypatch, glyph
):
    services, _, _, _ = environment(tmp_path)
    ctx = ToolContext(services)
    monkeypatch.setattr("fontlab_plugmix.snapshot.active_glyph", lambda fontlab: None)
    assert ctx.snapshot() is None
    assert Tool().marks(None) == [] and not Tool().press(ToolEvent(0, 0, 0, 0))
    assert not Tool().move(ToolEvent(0, 0, 0, 0))
    assert not Tool().release(ToolEvent(0, 0, 0, 0))
    assert not Tool().double_click(ToolEvent(0, 0, 0, 0))
    assert not Tool().key_down(ToolEvent(0, 0, 0, 0))
    assert not Tool().key_up(ToolEvent(0, 0, 0, 0))
    calls = []
    writer = NS(
        apply_work=lambda work, title, facts, editor: (
            calls.append((work, title)) or "done"
        )
    )
    monkeypatch.setattr("fontlab_plugmix.tool.import_module", lambda name: writer)
    assert ctx.edit(lambda snap: ([1], "facts", object()), "Move") == "done"
    assert calls == [([1], "Move")]
    general = GeneralContext(services, ZoomToSelection())
    monkeypatch.setattr("fontlab_plugmix.general.import_module", lambda name: writer)
    assert general.edit(lambda snap: ([2], "facts", object()), "Edit") == "done"
    general.close()


def test_tool_context_select_uses_workspace_and_redraw(tmp_path, monkeypatch):
    services, _state, _workspace, _errors = environment(tmp_path)
    active = NS(layer=object())
    calls = []
    monkeypatch.setattr("fontlab_plugmix.snapshot.active_glyph", lambda fontlab: active)
    monkeypatch.setattr(
        "fontlab_plugmix.snapshot.select_contours",
        lambda layer, indices, **kw: calls.append((layer, indices, kw)),
    )
    services.fontlab.CurrentGlyph = lambda: (_ for _ in ()).throw(
        AssertionError("CurrentGlyph must not run")
    )
    services.fontlab.UpdateActiveCanvas = lambda: calls.append("redraw")
    ToolContext(services).select((1, 2), toggle=True)
    assert calls == [(active.layer, (1, 2), {"toggle": True}), "redraw"]


def test_general_shortcut_conflict_is_reported_without_forcing(tmp_path, monkeypatch):
    services, state, _workspace, errors = environment(tmp_path)

    class Shortcut(General):
        name, title, shortcut = "shortcut", "Shortcut", "Ctrl+K"

    classes = state.available()
    classes[Shortcut.name] = Shortcut
    monkeypatch.setattr(
        state,
        "available",
        lambda kind=None: {
            k: v for k, v in classes.items() if kind is None or v.kind == kind
        },
    )
    existing = NS(shortcut=KeySequence("ctrl+k"))
    services.menus.main_window = lambda: NS(findChildren=lambda cls: [existing])
    palettes = PaletteHost(services, state)
    palettes.install()
    host = GeneralHost(services, state, palettes)
    host.install()
    token = host.running["shortcut"].token
    assert "already in use" in errors[-1]
    assert not hasattr(services.menus.action(token), "shortcut_set")
    host.close()
    palettes.close()


def test_general_shortcut_property_is_assigned_as_key_sequence(tmp_path, monkeypatch):
    services, state, _workspace, errors = environment(tmp_path)

    class Shortcut(General):
        name, title, shortcut = "shortcut", "Shortcut", "ctrl+l"

    classes = state.available()
    classes[Shortcut.name] = Shortcut
    monkeypatch.setattr(
        state,
        "available",
        lambda kind=None: {
            k: v for k, v in classes.items() if kind is None or v.kind == kind
        },
    )
    palettes = PaletteHost(services, state)
    palettes.install()
    host = GeneralHost(services, state, palettes)
    host.install()
    token = host.running["shortcut"].token
    assert services.menus.action(token).shortcut_set.toString() == "Ctrl+L"
    assert errors == []
    host.close()
    palettes.close()


def test_key_before_mouse_uses_cursor_in_viewport(tmp_path):
    services, _state, workspace, errors = environment(tmp_path)
    seen = []

    class Probe(Tool):
        def key_down(self, event):
            seen.append(event)
            return True

    bridge = ToolBridge(Probe(), services)
    assert bridge.activate()
    assert bridge.keyPressed(mouse(0, 0), workspace.canvas) is False
    assert bridge._last is None
    assert (seen[0].view_x, seen[0].view_y, seen[0].x, seen[0].y) == (67.5, 59, 25, 50)
    assert errors == []
    bridge.deactivate()


def test_boot_wires_all_five_kinds_and_tears_down(tmp_path, monkeypatch):
    from fontlab_plugmix import boot

    services, _state, workspace, errors = environment(tmp_path)

    def close_menus():
        services.menus.closed = True
        services.menus.actions.clear()

    services.menus.close = close_menus
    services.painters.close = lambda: setattr(services.painters, "closed", True)
    monkeypatch.setattr(boot, "_state", None)
    monkeypatch.setattr(
        boot,
        "_runtime",
        lambda: (services.qt, services.fontlab, lambda *args, **kw: services.menus),
    )
    monkeypatch.setattr(boot, "select_backend", lambda *args: services.painters)
    boot.install(tmp_path)
    assert len(services.menus.actions) == 23
    assert len(workspace.registered) == 1
    assert len(Timer.created) == 1 and Timer.created[0].running
    boot.uninstall()
    assert workspace.removed == [1]
    assert services.menus.closed and services.painters.closed
    assert not services.menus.actions and Timer.created[0].deleted
    assert errors == []

# this_file: tests/test_palette.py
"""Fake dock, Qt controls and native contours for Palette lifecycle and Undo."""

import json
from dataclasses import replace
from types import SimpleNamespace as NS
from typing import ClassVar

import pytest

from fontlab_plugmix import Palette, registry
from fontlab_plugmix.kinds import Services
from fontlab_plugmix.palettes.apply import (
    RepeatEditor,
    _values,
    repeat_selected,
    selected_indices,
)
from fontlab_plugmix.palettes.host import PaletteHost
from fontlab_plugmix.palettes.step_and_repeat import StepAndRepeat
from fontlab_plugmix.palettes.ui import PaletteUI
from fontlab_plugmix.snapshot import ActiveGlyph, Contour, Node


class Signal:
    def __init__(self):
        self.slots = []

    def connect(self, callback):
        self.slots.append(callback)

    def disconnect(self, callback):
        self.slots.remove(callback)

    def emit(self, *args):
        for callback in tuple(self.slots):
            callback(*args)


class Control:
    def __init__(self, *args):
        self.value = None
        self.clicked = Signal()

    def setValue(self, value):
        self.value = value

    def setRange(self, low, high):
        self.range = (low, high)

    def setText(self, text):
        self.text = text

    def setChecked(self, checked):
        self.checked = checked


class Layout:
    def __init__(self, *args):
        self.rows = []

    def addWidget(self, value):
        self.rows.append(value)

    def addLayout(self, value):
        self.rows.append(value)

    def addRow(self, label, value):
        self.rows.append((label, value))


class Timer:
    instances: ClassVar[list] = []
    pending: ClassVar[list] = []

    def __init__(self):
        self.timeout = Signal()
        self.running = self.deleted = False
        self.instances.append(self)

    def setInterval(self, interval):
        self.interval = interval

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def deleteLater(self):
        self.deleted = True

    @staticmethod
    def singleShot(delay, callback):
        Timer.pending.append(callback)


class Menus:
    def __init__(self):
        self.actions = {}
        self.removed = []

    def add_action(self, section, title, callback, *, checkable):
        assert (section, checkable) == ("Window", True)
        token = len(self.actions) + 1
        self.actions[token] = (title, callback, Control())
        return token

    def action(self, token):
        return self.actions[token][2]

    def main_window(self):
        return "main"

    def remove(self, token):
        self.removed.append(token)
        self.actions.pop(token)


class Owned:
    def __init__(self):
        self.visible = True
        self.filters = []
        self.widget = NS(
            visibilityChanged=Signal(),
            isVisible=lambda: self.visible,
            installEventFilter=lambda item: self.filters.append(item),
            removeEventFilter=lambda item: self.filters.remove(item),
        )
        self.closed = False

    def user_close(self):
        for item in tuple(self.filters):
            item.eventFilter(self.widget, NS(type=lambda: 19))
        self.visible = False
        self.widget.visibilityChanged.emit(False)

    def close(self):
        self.closed = True
        return True


def fake_qt():
    gui = NS(
        QVBoxLayout=Layout,
        QFormLayout=Layout,
        QLabel=Control,
        QSpinBox=Control,
        QDoubleSpinBox=Control,
        QCheckBox=Control,
        QPushButton=Control,
    )
    return NS(
        QtGui=gui,
        QtCore=NS(QTimer=Timer, QEvent=NS(Close=19)),
        private=NS(QObject=object),
    )


def palette_host(tmp_path, monkeypatch, *, qt=None):
    import fontlab_plugmix.palettes.host as module

    Timer.instances.clear()
    Timer.pending.clear()
    created = []

    def panel(main, title, build, area):
        assert (
            main == "main"
            and title in {"Step and Repeat", "Second"}
            and area == "right"
        )
        owned = Owned()
        build(object())
        created.append(owned)
        return owned

    monkeypatch.setattr(module, "import_module", lambda name: NS(create_panel=panel))
    menus, errors = Menus(), []
    state = registry.Registry(tmp_path)
    services = Services(
        qt or fake_qt(),
        NS(),
        menus,
        None,
        lambda error, source: errors.append(str(error)),
    )
    host = PaletteHost(services, state)
    host.install()
    return host, state, created, errors


def test_palette_discovery_menu_filter_and_old_preferences(tmp_path):
    from fontlab_plugmix import menu
    from fontlab_plugmix.filters.host import FilterHost

    state = registry.Registry(tmp_path)
    assert state.available("palette") == {"step_and_repeat": StepAndRepeat}
    assert "step_and_repeat" not in state.available("reporter")
    assert "step_and_repeat" not in state.available("filter")
    actions = []

    class Owner:
        def add_action(self, section, title, callback, *, checkable):
            actions.append((section, title))
            return len(actions)

        def action(self, token):
            return Control()

    owner = Owner()
    assert "step_and_repeat" not in menu.install(owner, state)
    FilterHost(Services(None, None, owner, None, lambda e, p: None), state).install()
    assert not any("Step and Repeat" in title for _, title in actions)
    assert state.enabled_palettes() == ()
    state.enable("node_indexes")
    assert "enabled_palettes" not in json.loads(state.path.read_text())
    state.set_palette_enabled("step_and_repeat", True)
    assert registry.Registry(tmp_path).enabled_palettes() == ("step_and_repeat",)
    state.set_palette_enabled("step_and_repeat", False)
    assert registry.Registry(tmp_path).enabled_palettes() == ()
    with pytest.raises(KeyError):
        state.set_palette_enabled("missing", True)
    state.path.write_text('{"enabled": ["node_indexes"]}')
    assert registry.Registry(tmp_path).enabled_palettes() == ()


def test_palette_host_toggle_timer_refresh_key_and_title_close(
    tmp_path, monkeypatch, glyph
):
    import fontlab_plugmix.palettes.host as module

    host, state, created, errors = palette_host(tmp_path, monkeypatch)
    assert not hasattr(host.services.qt.QtCore, "QObject")
    assert host.services.qt.private.QObject is object
    assert list(host.actions) == ["step_and_repeat"]
    token = host.actions["step_and_repeat"]
    assert host.services.menus.actions[token][0] == "Plugmix: Step and Repeat Panel"
    assert host.timer is None
    active = NS(package=object(), layer=object())
    current = [1]
    monkeypatch.setattr(module.snapshot, "active_glyph", lambda fontlab: active)
    monkeypatch.setattr(module.snapshot, "palette_key", lambda source: current[0])
    monkeypatch.setattr(module.snapshot, "capture", lambda source, **kwargs: glyph)
    assert host.toggle("step_and_repeat") is True
    assert created[0].closed is False and Timer.instances[0].interval == 250
    assert Timer.instances[0].running and host.services.menus.action(token).checked
    plugin = host.panels["step_and_repeat"].plugin
    updates = []
    monkeypatch.setattr(plugin, "refresh", lambda context: updates.append(context))
    Timer.instances[0].timeout.emit()
    Timer.instances[0].timeout.emit()
    assert updates == [glyph]
    current[0] = 2
    Timer.instances[0].timeout.emit()
    assert updates == [glyph, glyph]
    assert host.toggle("step_and_repeat") is False
    assert created[0].closed and not Timer.instances[0].running
    assert state.enabled_palettes() == ()
    host.toggle("step_and_repeat")
    assert len(Timer.instances) == 1, "one timer is shared across repeated toggles"
    created[1].visible = False
    created[1].widget.visibilityChanged.emit(False)
    assert not created[1].closed and state.enabled_palettes() == ("step_and_repeat",)
    assert not host.timer.running and Timer.pending == []
    created[1].visible = True
    created[1].widget.visibilityChanged.emit(True)
    assert host.timer.running and state.enabled_palettes() == ("step_and_repeat",)
    created[1].user_close()
    assert not created[1].closed and len(Timer.pending) == 1
    Timer.pending.pop(0)()
    assert created[1].closed and state.enabled_palettes() == ()
    host.close()
    assert Timer.instances[0].deleted and host.actions == {} and errors == []


def test_palette_shows_when_close_filter_base_is_missing(tmp_path, monkeypatch):
    qt = fake_qt()
    del qt.private
    host, state, created, errors = palette_host(tmp_path, monkeypatch, qt=qt)
    assert host.toggle("step_and_repeat") is True
    assert len(created) == 1 and not created[0].filters
    assert state.enabled_palettes() == ("step_and_repeat",)
    assert len(errors) == 1 and "Dock close detection unavailable" in errors[0]
    created[0].visible = False
    created[0].widget.visibilityChanged.emit(False)
    assert not created[0].closed and state.enabled_palettes() == ("step_and_repeat",)
    host.toggle("step_and_repeat")
    host.toggle("step_and_repeat")
    assert len(errors) == 1, "the degraded close capability is reported once"
    host.close()
    assert all(item.closed for item in created)


@pytest.mark.parametrize("failure", [False, ExceptionGroup("close failed", [TypeError("dock")])])
def test_palette_keeps_refused_or_failed_dock_for_retry(tmp_path, monkeypatch, failure):
    host, state, created, errors = palette_host(tmp_path, monkeypatch)
    assert host.toggle("step_and_repeat") is True
    original = created[0].close
    calls = []

    def failing_close():
        calls.append(True)
        if failure is False:
            return False
        raise failure

    created[0].close = failing_close
    assert host.toggle("step_and_repeat") is True
    assert host.close() is False
    assert len(calls) == 2 and len(errors) == 1
    assert len(host.panels) == 1 and len(host.actions) == 1
    assert host.services.menus.action(host.actions["step_and_repeat"]).checked
    assert state.enabled_palettes() == ("step_and_repeat",)
    created[0].close = original
    assert host.toggle("step_and_repeat") is False
    assert len(created) == 1 and state.enabled_palettes() == ()
    assert host.close() is True


def test_palette_real_app_owner_close_contract(tmp_path, monkeypatch):
    from fontlabapp.widgets import OwnedWidget

    host, state, created, errors = palette_host(tmp_path, monkeypatch)
    assert host.toggle("step_and_repeat") is True
    panel = host.panels["step_and_repeat"]

    class Dock:
        def __init__(self):
            self.destroyed = Signal()
            self.visibilityChanged = Signal()
            self.accept = False
            self.fail_delete = False
            self.deleted = False

        def isVisible(self):
            return True

        def close(self):
            return self.accept

        def deleteLater(self):
            if self.fail_delete:
                raise TypeError("delete failed")
            self.deleted = True

        def removeEventFilter(self, item):
            return None

    dock = Dock()
    panel.owned = OwnedWidget(dock, object())
    dock.visibilityChanged.connect(panel.visibility)
    assert host.toggle("step_and_repeat") is True
    assert len(host.panels) == 1 and not dock.deleted
    dock.accept = True
    dock.fail_delete = True
    assert host.toggle("step_and_repeat") is True
    assert len(host.panels) == 1 and not dock.deleted
    dock.fail_delete = False
    assert host.toggle("step_and_repeat") is False
    assert dock.deleted and len(created) == 1 and state.enabled_palettes() == ()
    assert any("delete failed" in error for error in errors)
    host.close()


def test_palette_user_close_handles_already_destroyed_owner(tmp_path, monkeypatch):
    host, state, _created, errors = palette_host(tmp_path, monkeypatch)
    host.toggle("step_and_repeat")
    panel = host.panels["step_and_repeat"]
    panel.owned.widget = None
    host._hide_by_user("step_and_repeat")
    assert host.panels == {} and state.enabled_palettes() == ()
    assert errors == []
    host.close()


def test_palette_shows_when_event_filter_install_fails(tmp_path, monkeypatch):
    original_init = Owned.__init__

    def broken_filter(self):
        original_init(self)
        self.widget.installEventFilter = lambda item: (_ for _ in ()).throw(
            TypeError("event filters unavailable")
        )

    monkeypatch.setattr(Owned, "__init__", broken_filter)
    host, state, created, errors = palette_host(tmp_path, monkeypatch)
    assert host.toggle("step_and_repeat") is True
    assert not created[0].closed and state.enabled_palettes() == ("step_and_repeat",)
    assert len(errors) == 1 and "event filters unavailable" in errors[0]
    host.toggle("step_and_repeat")
    assert created[0].closed and state.enabled_palettes() == ()
    host.close()


def test_palette_uses_qtcore_qobject_on_other_pythonqt_builds(tmp_path, monkeypatch):
    qt = fake_qt()
    del qt.private
    qt.QtCore.QObject = object
    host, state, created, errors = palette_host(tmp_path, monkeypatch, qt=qt)
    host.toggle("step_and_repeat")
    assert len(created[0].filters) == 1 and errors == []
    created[0].user_close()
    Timer.pending.pop(0)()
    assert created[0].closed and state.enabled_palettes() == ()
    host.close()


def test_palette_host_restores_only_chosen_panel_and_guards_refresh(
    tmp_path, monkeypatch
):
    import fontlab_plugmix.palettes.host as module

    state = registry.Registry(tmp_path)
    state.set_palette_enabled("step_and_repeat", True)
    host, state, created, errors = palette_host(tmp_path, monkeypatch)
    assert len(created) == 1 and state.enabled_palettes() == ("step_and_repeat",)
    plugin = host.panels["step_and_repeat"].plugin
    monkeypatch.setattr(module.snapshot, "active_glyph", lambda fontlab: None)
    monkeypatch.setattr(module.snapshot, "palette_key", lambda source: None)
    monkeypatch.setattr(
        plugin,
        "refresh",
        lambda context: (_ for _ in ()).throw(RuntimeError("refresh failed")),
    )
    host.timer.timeout.emit()
    assert errors == ["refresh failed"] and host.timer.running
    host.timer.timeout.emit()
    assert errors == ["refresh failed"], "same key must not refresh again"
    host.close()
    assert state.enabled_palettes() == ("step_and_repeat",)


def test_palette_capture_failure_is_reported_once_per_key(tmp_path, monkeypatch):
    import fontlab_plugmix.palettes.host as module

    host, _state, _created, errors = palette_host(tmp_path, monkeypatch)
    key = [1]
    monkeypatch.setattr(
        module.snapshot,
        "active_glyph",
        lambda fontlab: NS(package=object(), layer=object()),
    )
    monkeypatch.setattr(module.snapshot, "palette_key", lambda active: key[0])
    monkeypatch.setattr(
        module.snapshot,
        "capture",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("capture failed")),
    )
    host.toggle("step_and_repeat")
    host.timer.timeout.emit()
    host.timer.timeout.emit()
    assert errors == ["capture failed"] and host.timer.running
    key[0] = 2
    host.timer.timeout.emit()
    assert errors == ["capture failed", "capture failed"]
    host.close()


def test_palette_close_event_filter_never_raises_into_qt(tmp_path, monkeypatch):
    host, state, created, errors = palette_host(tmp_path, monkeypatch)
    host.toggle("step_and_repeat")
    event = NS(type=lambda: (_ for _ in ()).throw(TypeError("bad Qt event")))
    assert created[0].filters[0].eventFilter(created[0].widget, event) is False
    assert errors == ["bad Qt event"]
    assert not created[0].closed and state.enabled_palettes() == ("step_and_repeat",)
    host.close()


def test_palette_menu_callback_reports_failed_preference_save(tmp_path, monkeypatch):
    host, state, created, errors = palette_host(tmp_path, monkeypatch)
    token = host.actions["step_and_repeat"]
    state._save = lambda: (_ for _ in ()).throw(OSError("read-only prefs"))
    host.services.menus.actions[token][1]()
    assert errors == ["read-only prefs"]
    assert created[0].closed and host.panels == {}
    assert host.services.menus.action(token).checked is False
    host.close()


def test_palette_timer_setup_failure_closes_panel_and_can_retry(tmp_path, monkeypatch):
    host, state, created, errors = palette_host(tmp_path, monkeypatch)
    original = Timer.setInterval
    monkeypatch.setattr(
        Timer,
        "setInterval",
        lambda self, value: (_ for _ in ()).throw(RuntimeError("timer failed")),
    )
    token = host.actions["step_and_repeat"]
    host.services.menus.actions[token][1]()
    assert errors == ["timer failed"] and created[0].closed
    assert Timer.instances[0].deleted and host.timer is None and host.panels == {}
    assert not host.services.menus.action(token).checked
    monkeypatch.setattr(Timer, "setInterval", original)
    assert host.toggle("step_and_repeat") is True
    assert state.enabled_palettes() == ("step_and_repeat",)
    host.close()


def test_two_palettes_share_one_timer_and_refresh_new_panel_once(
    tmp_path, monkeypatch, glyph
):
    import fontlab_plugmix.palettes.host as module

    seen = []

    class Second(Palette):
        name, title = "second", "Second"

        def build(self, ui):
            ui.label("Second")

        def refresh(self, context):
            seen.append(context)

    classes = registry.discover()
    classes[Second.name] = Second
    monkeypatch.setattr(registry, "discover", lambda sink: classes)
    host, state, created, errors = palette_host(tmp_path, monkeypatch)
    current = [1]
    monkeypatch.setattr(
        module.snapshot,
        "active_glyph",
        lambda fontlab: NS(package=object(), layer=object()),
    )
    monkeypatch.setattr(module.snapshot, "palette_key", lambda source: current[0])
    monkeypatch.setattr(module.snapshot, "capture", lambda source, **kwargs: glyph)
    host.toggle("step_and_repeat")
    host.timer.timeout.emit()
    host.toggle("second")
    assert len(Timer.instances) == 1 and seen == [glyph]
    host.timer.timeout.emit()
    assert seen == [glyph]
    current[0] = 2
    created[0].visible = False
    created[0].widget.visibilityChanged.emit(False)
    host.timer.timeout.emit()
    assert seen == [glyph, glyph]
    assert host.panels["step_and_repeat"].plugin.status.text == "1 selected contours."
    assert state.enabled_palettes() == ("second", "step_and_repeat")
    host.toggle("step_and_repeat")
    assert host.timer.running
    host.toggle("second")
    assert not host.timer.running and state.enabled_palettes() == ()
    host.close()
    assert all(panel.closed for panel in created) and errors == []


def test_palette_ui_guards_button_and_disconnects(tmp_path, monkeypatch):
    host, _state, created, errors = palette_host(tmp_path, monkeypatch)
    host.toggle("step_and_repeat")
    panel = host.panels["step_and_repeat"]
    ui = panel.ui
    check = ui.checkbox("Preview", True)
    assert check.checked is True
    assert ui.value(panel.plugin.count) == 1
    button = ui.layout.rows[-2]
    monkeypatch.setattr(
        panel.plugin,
        "command",
        lambda values, services: (_ for _ in ()).throw(RuntimeError("apply failed")),
    )
    button.clicked.emit()
    assert errors == ["apply failed"]
    assert panel.plugin.status.text == "apply failed"
    panel.plugin.dy.setValue(0)
    monkeypatch.setattr(
        panel.plugin, "command", lambda values, services: _values(values)
    )
    button.clicked.emit()
    assert errors[-1] == "X and Y offsets cannot both be zero"
    assert panel.plugin.status.text == errors[-1]
    host.close()
    assert button.clicked.slots == [] and created[0].closed
    assert ui.connections == []


def test_step_and_repeat_pure_selection_and_validation(glyph):
    assert selected_indices(glyph) == (0,)
    assert (
        selected_indices(
            replace(glyph, contours=(Contour((Node(0, 0, True, False),)),))
        )
        == ()
    )
    assert _values({"count": 3, "dx": -10, "dy": 4}) == (3, -10.0, 4.0)
    for values in (
        {"count": -1, "dx": 0, "dy": 0},
        {"count": 101, "dx": 0, "dy": 0},
        {"count": 1, "dx": float("inf"), "dy": 0},
        {"count": 1, "dx": 0, "dy": 0},
    ):
        with pytest.raises(ValueError):
            _values(values)
    with pytest.raises(NotImplementedError):
        Palette().build(object())


def test_step_and_repeat_panel_build_refresh_and_apply(glyph):
    qt = fake_qt()
    calls = []
    plugin = StepAndRepeat()
    ui = PaletteUI(
        qt,
        object(),
        plugin,
        lambda e, p: None,
        lambda values: calls.append(values) or "Done",
    )
    plugin.build(ui)
    assert plugin.count.range == (0, 100)
    plugin.refresh(glyph)
    assert plugin.status.text == "1 selected contours."
    plugin.dx.setValue(-20)
    plugin.dy.setValue(5)
    ui.layout.rows[-1].clicked.emit()
    assert calls == [{"count": 1, "dx": -20, "dy": 5}]
    assert plugin.status.text == "Done"
    plugin.refresh(None)
    assert plugin.status.text == "0 selected contours."
    ui.close()
    plugin.close()
    assert plugin.ui is None


def test_repeat_no_selection_and_zero_count(monkeypatch, glyph):
    from fontlab_plugmix.palettes import apply as module

    services = Services(fake_qt(), NS(), Menus(), None, lambda e, p: None)
    assert repeat_selected({"count": 0, "dx": 1, "dy": 1}, services)[2].startswith(
        "Count is zero"
    )
    monkeypatch.setattr(module.snapshot, "active_glyph", lambda fontlab: None)
    assert (
        repeat_selected({"count": 1, "dx": 1, "dy": 1}, services)[2]
        == "No active glyph."
    )
    layer = NS(isNull=False)
    active = ActiveGlyph(
        NS(master="Regular"), NS(name="a", findLayer=lambda name: layer), layer
    )
    monkeypatch.setattr(module.snapshot, "active_glyph", lambda fontlab: active)
    empty = replace(glyph, contours=(Contour((Node(0, 0, True, False),)),))
    monkeypatch.setattr(module.snapshot, "capture", lambda *args, **kwargs: empty)
    assert (
        repeat_selected({"count": 1, "dx": 1, "dy": 1}, services)[2]
        == "Select a contour first."
    )


def test_repeat_refuses_displayed_nonmaster_layer(monkeypatch, glyph):
    from fontlab_plugmix.palettes import apply as module

    master, displayed = Layer([]), Layer([])
    active = ActiveGlyph(
        NS(master="Regular"),
        NS(name="a", findLayer=lambda name: master),
        displayed,
    )
    monkeypatch.setattr(module.snapshot, "active_glyph", lambda fontlab: active)
    monkeypatch.setattr(
        module.snapshot,
        "capture",
        lambda *args, **kwargs: pytest.fail("must refuse before reading selection"),
    )
    services = Services(fake_qt(), NS(), Menus(), None, lambda e, p: None)
    plan, result, status = repeat_selected(
        {"count": 1, "dx": 2, "dy": 3}, services
    )
    assert plan is result is None and "master layer" in status


class Matrix:
    def __init__(self):
        self.dx = self.dy = 0

    def translate(self, dx, dy):
        self.dx, self.dy = dx, dy


class NativeContour:
    next_id = 100

    def __init__(self, identifier, record, offset=(0, 0)):
        self.id, self.record, self.offset = identifier, record, offset

    def cloneMapped(self, matrix):
        NativeContour.next_id += 1
        return NativeContour(NativeContour.next_id, self.record, (matrix.dx, matrix.dy))


class Shape:
    def __init__(self, identifier, contours):
        self.id, self.contours, self.isComponent = identifier, contours, False
        self.shapeData = NS(referenceCount=1)
        self.transform = NS(
            m11=lambda: 1,
            m22=lambda: 1,
            m12=lambda: 0,
            m21=lambda: 0,
            dx=lambda: 0,
            dy=lambda: 0,
        )

    def addContour(self, contour, selected):
        self.contours.append(contour)


class Layer:
    def __init__(self, shapes):
        self.shapes, self.autoLayer, self.isNull = shapes, False, False
        self.changed_count = 0

    def changed(self):
        self.changed_count += 1

    def update(self):
        return True


def test_repeat_native_writer_counts_offsets_undo_and_unsafe(monkeypatch, glyph):
    import fontlabapp.history as history  # noqa: PLR0402 - concrete module for monkeypatch
    import fontlabapp.layer_writer as writer
    import fontlabapp.outline_writer as outlines

    from fontlab_plugmix.palettes import apply as module

    chosen = Contour(
        (Node(0, 0, True, True), Node(10, 0, True, False), Node(10, 10, True, False))
    )
    other = Contour((Node(20, 0, True, False), Node(30, 0, True, False)))
    shape = Shape(1, [NativeContour(1, chosen), NativeContour(2, other)])
    layer = Layer([shape])
    package = NS(master="Regular")
    owner = NS(id=1, name="a", findLayer=lambda master: layer)
    services = Services(
        NS(QtGui=NS(QTransform=Matrix)),
        NS(UpdateActiveCanvas=lambda: redraws.append(True)),
        Menus(),
        None,
        lambda e, p: None,
    )
    redraws, commits, repaired = [], [], []
    monkeypatch.setattr(
        module.snapshot,
        "active_glyph",
        lambda fontlab: ActiveGlyph(package, owner, layer),
    )
    monkeypatch.setattr(
        module.snapshot,
        "capture",
        lambda source, **kwargs: replace(
            glyph, contours=tuple(c.record for c in shape.contours)
        ),
    )
    monkeypatch.setattr(
        history, "scan_auto_facts", lambda package: history.auto_facts([])
    )

    def commit(title, layers, owners, mutate, **kwargs):
        commits.append((title, len(layers), kwargs["operation"]))
        mutate()
        return NS(
            mismatches=list(kwargs["read_back"]()), pending_note="", pending_updates=()
        )

    monkeypatch.setattr(history, "commit", commit)

    def repair(source, copy):
        repaired.append((source.id, copy.id))
        copy.record = replace(
            copy.record,
            nodes=tuple(replace(node, selected=False) for node in copy.record.nodes),
        )

    plan, result, message = repeat_selected(
        {"count": 1, "dx": -5, "dy": 2},
        services,
        outlines=outlines,
        writer=writer,
        history=history,
        repair=repair,
    )
    assert len(plan.work) == 1 and result["layers"] == 1
    assert commits == [("Step and Repeat", 1, "geometry")]
    assert [c.offset for c in shape.contours[2:]] == [(-5, 2)]
    assert all(not node.selected for node in shape.contours[2].record.nodes)
    assert len(repaired) == 1 and len(redraws) == 1
    plan, result, message = repeat_selected(
        {"count": 3, "dx": -2, "dy": -3},
        services,
        outlines=outlines,
        writer=writer,
        history=history,
        repair=repair,
    )
    assert [c.offset for c in shape.contours[-3:]] == [(-2, -3), (-4, -6), (-6, -9)]
    assert len(commits) == 2 and result["layers"] == 1 and "3 contour copies" in message
    shape.shapeData.referenceCount = 2
    plan, result, message = repeat_selected(
        {"count": 1, "dx": 1, "dy": 1},
        services,
        outlines=outlines,
        writer=writer,
        history=history,
        repair=repair,
    )
    assert plan.refused == ["a"] and result is None and message == "Skipped: a"
    assert len(commits) == 2


def test_repeat_editor_rechecks_safety_and_readback():
    source = NativeContour(1, Contour((Node(0, 0, True, True),)))
    shape = Shape(1, [source])
    layer = Layer([shape])
    outlines = NS(outline_shapes=lambda layer: ([], ["shared"]))
    editor = RepeatEditor(outlines, NS(QtGui=NS(QTransform=Matrix)), lambda a, b: None)
    with pytest.raises(ValueError, match="shared or transformed"):
        editor.prepare(layer, [((0,), ((2, 3),))])
    outlines.outline_shapes = lambda layer: ([shape], [])
    steps = editor.prepare(layer, [((0,), ((2, 3),))])
    assert editor.check([(layer, steps)]) == ["repeated contour missing after write"]
    editor.write(layer, steps)
    assert editor.check([(layer, steps)]) == [] and editor.retain(steps) == []


def test_repeat_editor_refuses_changed_contour_count_before_undo():
    source = NativeContour(1, Contour((Node(0, 0, True, True),)))
    layer = Layer([Shape(1, [source, source])])
    editor = RepeatEditor(
        NS(outline_shapes=lambda layer: (layer.shapes, [])),
        NS(QtGui=NS(QTransform=Matrix)),
        lambda a, b: None,
        expected_count=1,
    )
    with pytest.raises(ValueError, match="contour count changed"):
        editor.prepare(layer, [((0,), ((2, 3),))])

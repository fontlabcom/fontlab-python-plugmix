# this_file: tests/test_filter.py
"""Pure Filter contract, kind registry and fake native Apply/Qt boundaries."""

import json
from dataclasses import replace
from types import SimpleNamespace as NS
from typing import ClassVar

import pytest

from fontlab_plugmix import Filter, LayerEdit, Param, Plugin, menu, registry, snapshot
from fontlab_plugmix.filter import Filter as FilterBase
from fontlab_plugmix.filters.apply import LayerEditEditor, _removed, apply_filter
from fontlab_plugmix.filters.delete_small_paths import DeleteSmallPaths
from fontlab_plugmix.filters.dialog import FilterDialog
from fontlab_plugmix.filters.host import FilterHost
from fontlab_plugmix.kinds import Services, guarded
from fontlab_plugmix.snapshot import Contour, Node


def square(side: float, *, closed: bool = True) -> Contour:
    return Contour(
        (
            Node(0, 0, True, False),
            Node(side, 0, True, False),
            Node(side, side, True, False),
            Node(0, side, True, False),
        ),
        closed,
    )


def test_delete_small_paths_threshold_edges_open_empty_and_all_deleted(glyph):
    plugin = DeleteSmallPaths()
    below, equal, above = square(19), square(20), square(21)
    open_path = square(1, closed=False)
    data = replace(glyph, contours=(below, equal, above, open_path))
    assert plugin.compute(data, {"threshold": 400}).contours == (
        equal,
        above,
        open_path,
    )
    assert plugin.compute(data, {"threshold": 441}).contours == (above, open_path)
    assert (
        plugin.compute(replace(data, contours=(below,)), {"threshold": 400}).contours
        == ()
    )
    assert plugin.compute(replace(data, contours=()), {"threshold": 400}) == LayerEdit()
    assert (
        plugin.compute(replace(data, contours=(equal,)), {"threshold": 400})
        == LayerEdit()
    )
    near = tuple(
        Contour(
            (
                Node(0, 0, True, False),
                Node(width, 0, True, False),
                Node(width, 1, True, False),
                Node(0, 1, True, False),
            )
        )
        for width in (399.9, 400, 400.1)
    )
    assert (
        plugin.compute(replace(glyph, contours=near), {"threshold": 400}).contours
        == near[1:]
    )


def test_delete_small_paths_uses_bounds_for_cancelled_area(glyph):
    crossing = Contour(
        (
            Node(0, 0, True, False),
            Node(30, 30, True, False),
            Node(0, 30, True, False),
            Node(30, 0, True, False),
        )
    )
    data = replace(glyph, contours=(crossing,))
    assert DeleteSmallPaths().compute(data, {"threshold": 400}).contours == ()
    assert DeleteSmallPaths().compute(data, {"threshold": 0}) == LayerEdit()
    assert (
        DeleteSmallPaths().compute(
            replace(data, contours=(Contour((Node(0, 0, True, False),)),)),
            {"threshold": 400},
        )
        == LayerEdit()
    )


def test_filter_params_reject_wrong_types_ranges_and_unknown_keys():
    class Options(Filter):
        name, title = "options", "Options"
        params = (
            Param("n", "Count", "int", 2, 0, 5),
            Param("ok", "OK", "bool", False),
            Param("mode", "Mode", "choice", "a", choices=("a", "b")),
        )

    assert Filter is FilterBase and issubclass(Filter, Plugin)
    assert Options.validate({}) == {"n": 2, "ok": False, "mode": "a"}
    assert Options.validate({"n": 5, "ok": True, "mode": "b"})["mode"] == "b"
    for values in ({"n": 6}, {"n": True}, {"ok": 1}, {"mode": "c"}, {"extra": 2}):
        with pytest.raises(ValueError):
            Options.validate(values)
    with pytest.raises(ValueError):
        Param("x", "X", "float", 0).parse(float("nan"))
    with pytest.raises(ValueError):
        Param("x", "X", "unsupported", 0).parse(0)
    with pytest.raises(NotImplementedError):
        Options().compute(None, {})


def test_registry_filters_old_prefs_params_and_reporter_menu(tmp_path):
    path = tmp_path / "fontlab-plugmix.json"
    path.write_text('{"enabled": ["node_indexes"], "future": {"keep": true}}')
    state = registry.Registry(tmp_path)
    assert len(state.available("reporter")) == 19
    assert list(state.available("filter")) == ["delete_small_paths"]
    assert state.enabled() == ("node_indexes",)
    assert state.enabled_filters() == ("delete_small_paths",)
    with pytest.raises(KeyError):
        state.enable("delete_small_paths")
    actions = []
    owner = NS(
        add_action=lambda section, title, callback, checkable: (
            actions.append((section, title)) or len(actions)
        ),
        action=lambda token: NS(setChecked=lambda value: None),
    )
    menu.install(owner, state)
    assert len(actions) == 19 and all(
        item[0] == "View" and "Delete Small" not in item[1] for item in actions
    )
    state.set_params("delete_small_paths", {"threshold": 123})
    saved = json.loads(path.read_text())
    assert saved["enabled"] == ["node_indexes"] and saved["enabled_filters"] == [
        "delete_small_paths"
    ]
    assert saved["params"]["delete_small_paths"] == {"threshold": 123.0}
    assert saved["future"] == {"keep": True}
    assert registry.Registry(tmp_path).values("delete_small_paths") == {
        "threshold": 123.0
    }
    state.set_filter_enabled("delete_small_paths", False)
    assert state.enabled_filters() == ()
    assert registry.Registry(tmp_path).enabled_filters() == ()
    state.set_filter_enabled("delete_small_paths", True)
    with pytest.raises(KeyError):
        state.set_filter_enabled("node_indexes", True)


def test_registry_rejects_bad_filter_params_and_rolls_back_io(tmp_path):
    errors = []
    state = registry.Registry(tmp_path, lambda error, source: errors.append(str(error)))
    with pytest.raises(ValueError):
        state.set_params("delete_small_paths", {"threshold": -1})
    state._params["delete_small_paths"] = {"threshold": "bad"}
    assert state.values("delete_small_paths") == {"threshold": 400.0}
    assert errors
    state._params.clear()
    state._save = lambda: (_ for _ in ()).throw(OSError("read only"))
    with pytest.raises(OSError):
        state.set_params("delete_small_paths", {"threshold": 10})
    assert state._params == {}
    with pytest.raises(OSError):
        state.set_filter_enabled("delete_small_paths", False)
    assert state.enabled_filters() == ("delete_small_paths",)


def test_filter_entry_point_uses_the_existing_group_and_keeps_names_unique(monkeypatch):
    class External(Filter):
        name, title = "external_filter", "External Filter"

    loaded = [External]
    monkeypatch.setattr(
        registry.metadata,
        "entry_points",
        lambda: NS(select=lambda group: [NS(load=lambda: loaded[0])]),
    )
    found = registry.discover()
    assert found["external_filter"] is External
    assert "external_filter" not in {
        n for n, cls in found.items() if cls.kind == "reporter"
    }
    loaded[0] = type(
        "Duplicate", (Filter,), {"name": "node_indexes", "title": "Duplicate"}
    )
    errors = []
    assert "node_indexes" in registry.discover(
        lambda error, source: errors.append(error)
    )
    assert isinstance(errors[0], ValueError)
    loaded[0] = type(
        "Bogus", (Plugin,), {"kind": "filter", "name": "bogus", "title": "Bogus"}
    )
    assert "bogus" not in registry.discover(lambda error, source: errors.append(error))
    assert isinstance(errors[-1], TypeError)


def test_guarded_catches_plugin_and_sink_failures():
    errors = []
    assert (
        guarded("x", lambda error, source: errors.append((error, source)), lambda: 7)
        == 7
    )
    assert (
        guarded(
            "x", lambda error, source: errors.append((error, source)), lambda: 1 / 0
        )
        is None
    )
    assert isinstance(errors[0][0], ZeroDivisionError)
    assert guarded("x", lambda error, source: 1 / 0, lambda: 1 / 0) is None


class Signal:
    def __init__(self):
        self.slots = []

    def connect(self, slot):
        self.slots.append(slot)

    def disconnect(self, slot):
        self.slots.remove(slot)

    def emit(self, *args):
        for slot in tuple(self.slots):
            slot(*args)


class Widget:
    def __init__(self, *args):
        self.rows = []


class Layout(Widget):
    def addLayout(self, item):
        self.rows.append(item)

    def addWidget(self, item):
        self.rows.append(item)

    def addRow(self, label, item):
        self.rows.append((label, item))


class Spin(Widget):
    def setDecimals(self, value):
        self.decimals = value

    def setRange(self, low, high):
        self.range = (low, high)

    def setValue(self, value):
        self.number = value

    def value(self):
        return self.number


class Check(Widget):
    def setChecked(self, value):
        self.checked = value

    def isChecked(self):
        return self.checked


class Combo(Widget):
    def addItems(self, values):
        self.items = values

    def setCurrentIndex(self, index):
        self.index = index

    def currentText(self):
        return self.items[self.index]


class Label(Widget):
    def __init__(self, text, parent):
        self.text = text

    def setText(self, text):
        self.text = text


class Button(Widget):
    def __init__(self, title, parent):
        self.title = title
        self.clicked = Signal()


def fake_qt():
    return NS(
        QtGui=NS(
            QWidget=Widget,
            QVBoxLayout=Layout,
            QFormLayout=Layout,
            QHBoxLayout=Layout,
            QDoubleSpinBox=Spin,
            QSpinBox=Spin,
            QCheckBox=Check,
            QComboBox=Combo,
            QLabel=Label,
            QPushButton=Button,
        )
    )


def test_filter_dialog_builds_typed_rows_and_disconnects_once():
    class Options(Filter):
        name, title = "options", "Options"
        params = (
            Param("amount", "Amount", "float", 1.5, 0, 10),
            Param("count", "Count", "int", 2, 0, 5),
            Param("flag", "Flag", "bool", False),
            Param("mode", "Mode", "choice", "b", choices=("a", "b")),
        )

    applied, cancelled, errors = [], [], []
    dialog = FilterDialog(
        fake_qt(),
        Options(),
        Options.validate({}),
        lambda values: applied.append(values),
        lambda: cancelled.append(True),
        lambda error, source: errors.append(error),
    )
    assert len(dialog.controls) == 4
    assert dialog.controls["amount"][1].decimals == 3
    assert dialog.controls["count"][1].range == (0, 5)
    dialog.controls["count"][1].setValue(4)
    dialog.controls["flag"][1].setChecked(True)
    dialog.connections[1][0].emit(True)
    assert applied == [{"amount": 1.5, "count": 4, "flag": True, "mode": "b"}]
    dialog.connections[0][0].emit(False)
    assert cancelled == [True] and errors == []
    dialog.close()
    dialog.close()
    assert all(not signal.slots for signal, _ in dialog.connections)


def test_filter_dialog_reports_apply_and_disconnect_errors():
    plugin = DeleteSmallPaths()
    errors = []
    dialog = FilterDialog(
        fake_qt(),
        plugin,
        plugin.validate({}),
        lambda values: (_ for _ in ()).throw(RuntimeError("apply")),
        lambda: None,
        lambda error, source: errors.append(str(error)),
    )
    dialog.connections[1][0].emit()
    assert errors == ["apply"]
    assert dialog.status.text == "apply"
    dialog.connections[0][0].disconnect(dialog.connections[0][1])
    dialog.close()
    assert errors[-1].startswith("list.remove")


def test_filter_dialog_reads_pythonqt_properties_as_values():
    from fontlab_plugmix.filters.dialog import _value

    assert _value(NS(value=12.5), "float") == 12.5
    assert _value(NS(value=3), "int") == 3
    assert _value(NS(isChecked=True), "bool") is True
    assert _value(NS(currentText="choice"), "choice") == "choice"


def test_selected_layers_uses_lazy_checked_app_adapter(monkeypatch):
    requested = []
    monkeypatch.setattr(
        snapshot,
        "import_module",
        lambda name: NS(
            capture=lambda deadline: requested.append((name, deadline)) or "selected"
        ),
    )
    assert snapshot.selected_layers() == "selected"
    assert requested[0][0] == "fontlabapp.layer_selection" and requested[0][1] > 0


def test_apply_filter_commits_multiple_glyphs_once_and_reads_back(glyph, monkeypatch):
    import fontlabapp.history as history  # noqa: PLR0402 - concrete module for monkeypatch
    import fontlabapp.layer_writer as writer
    import fontlabapp.outline_writer as outlines

    class NativeContour:
        def __init__(self, identifier, record):
            self.id, self.record = identifier, record

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

        def removeContour(self, contour):
            self.contours.remove(contour)

    class Layer:
        def __init__(self, shape, auto=False):
            self.shapes, self.autoLayer, self.isNull = [shape], auto, False
            self.name = "Regular"
            self.updates = 0

        def changed(self):
            self.updates += 1

        def update(self):
            return True

    package = NS(master="Regular")
    glyphs = []
    for index in range(3):
        shape = Shape(
            index + 1,
            [
                NativeContour(index * 10 + 1, square(10)),
                NativeContour(index * 10 + 2, square(30)),
            ],
        )
        layer = Layer(shape)
        glyphs.append(
            NS(
                id=index + 1,
                name=f"g{index}",
                findLayer=lambda master, layer=layer: layer,
                layer=layer,
            )
        )
    selected = NS(occurrences=[NS(package=package, glyph=item) for item in glyphs])
    monkeypatch.setattr(
        snapshot,
        "capture",
        lambda source: replace(
            glyph,
            contours=tuple(
                item.record for shape in source.layer.shapes for item in shape.contours
            ),
        ),
    )
    monkeypatch.setattr(
        history, "scan_auto_facts", lambda package: history.auto_facts([])
    )
    commits = []

    def commit(title, layers, owners, mutate, **kwargs):
        commits.append((title, len(layers), kwargs["operation"], len(kwargs["retain"])))
        mutate()
        return NS(
            mismatches=list(kwargs["read_back"]()), pending_note="", pending_updates=()
        )

    monkeypatch.setattr(history, "commit", commit)
    plan, result = apply_filter(
        DeleteSmallPaths(),
        {"threshold": 400},
        selected=selected,
        outlines=outlines,
        writer=writer,
        history=history,
    )
    assert len(plan.work) == 3 and result["layers"] == 3
    assert commits == [("Delete Small Paths", 3, "geometry", 3)]
    assert all(
        len(item.layer.shapes[0].contours) == 1 and item.layer.updates == 1
        for item in glyphs
    )


def test_apply_filter_skips_empty_and_auto_layers_and_rejects_unsafe_shapes(
    glyph, monkeypatch
):
    import fontlabapp.history as history  # noqa: PLR0402 - concrete module for monkeypatch
    import fontlabapp.layer_writer as writer
    import fontlabapp.outline_writer as outlines

    package = NS(master="Regular")
    monkeypatch.setattr(
        history, "scan_auto_facts", lambda package: history.auto_facts([])
    )
    empty, result = apply_filter(
        DeleteSmallPaths(),
        {},
        selected=NS(occurrences=()),
        outlines=outlines,
        writer=writer,
        history=history,
    )
    assert empty.work == [] and result is None
    layer = NS(isNull=False, autoLayer=True)
    owner = NS(id=1, name="auto", findLayer=lambda master: layer)
    selected = NS(occurrences=[NS(package=package, glyph=owner)])
    skipped, result = apply_filter(
        DeleteSmallPaths(),
        {},
        selected=selected,
        outlines=outlines,
        writer=writer,
        history=history,
    )
    assert skipped.skipped == ["auto/Regular"] and result is None
    before = replace(glyph, contours=(square(10),))
    with pytest.raises(ValueError, match="deletion only"):
        _removed(before, LayerEdit(advance=100))
    with pytest.raises(ValueError, match="new or repeated"):
        _removed(before, LayerEdit(contours=(square(20),)))
    two = replace(before, contours=(square(10), square(20)))
    with pytest.raises(ValueError, match="reorder"):
        _removed(two, LayerEdit(contours=two.contours[::-1]))
    assert _removed(before, LayerEdit()) == ()


def test_layer_editor_rejects_shared_shape_and_reports_failed_readback():
    contour = NS(id=1)
    shape = NS(id=2, contours=[contour], isComponent=False)
    layer = NS(shapes=[shape])
    editor = LayerEditEditor(NS(outline_shapes=lambda layer: ([], ["shared"])))
    with pytest.raises(ValueError, match="shared"):
        editor.prepare(layer, [(0,)])
    editor = LayerEditEditor(NS(outline_shapes=lambda layer: ([shape], [])))
    steps = editor.prepare(layer, [(0,)])
    assert editor.retain(steps) == [contour]
    assert editor.check([(layer, steps)]) == ["contour remained after Filter write"]
    shape.removeContour = lambda contour: shape.contours.remove(contour)
    editor.write(layer, steps)
    assert editor.check([(layer, steps)]) == []


class MenuOwner:
    def __init__(self):
        self.actions = {}
        self.windows = {}
        self.removed = []
        self.fail_window = False
        self.fail_remove = False

    def add_action(self, section, title, callback, *, checkable):
        assert (section, checkable) == ("Glyph", False)
        token = len(self.actions) + 1
        self.actions[token] = (title, callback)
        return token

    def tool_window(self, widget, title, *, on_close):
        if self.fail_window:
            raise RuntimeError("window failed")
        token = 100 + len(self.windows)
        self.windows[token] = on_close
        return token, NS(resize=lambda size: setattr(self, "window_size", size))

    def remove(self, token):
        self.removed.append(token)
        if self.fail_remove:
            raise TypeError("remove failed")
        if token in self.windows:
            self.windows.pop(token)()
        self.actions.pop(token, None)


class StubDialog:
    instances: ClassVar[list] = []

    def __init__(self, qt, plugin, values, on_apply, on_cancel, sink):
        self.widget = NS(
            sizeHint=lambda: (240, 120),
            resize=lambda size: setattr(self, "widget_size", size),
        )
        self.plugin, self.values, self.on_apply, self.on_cancel = (
            plugin,
            values,
            on_apply,
            on_cancel,
        )
        self.status = Label("", None)
        self.closed = 0
        self.instances.append(self)

    def close(self):
        self.closed += 1


def test_filter_host_menu_dialog_apply_skip_and_teardown(tmp_path, monkeypatch):
    import fontlab_plugmix.filters.host as host_module

    StubDialog.instances.clear()
    owner, errors, redraws = MenuOwner(), [], []
    deferred = []
    state = registry.Registry(tmp_path)
    services = Services(
        NS(
            QtCore=NS(
                QTimer=NS(singleShot=lambda delay, callback: deferred.append(callback))
            )
        ),
        NS(UpdateActiveCanvas=lambda: redraws.append(True)),
        owner,
        object(),
        lambda error, source: errors.append(str(error)),
    )
    host = FilterHost(services, state)
    monkeypatch.setattr(host_module, "FilterDialog", StubDialog)
    selection = [NS(occurrences=())]
    monkeypatch.setattr(snapshot, "selected_layers", lambda: selection[0])
    host.install()
    assert len(owner.actions) == 1 and "Delete Small Paths" in owner.actions[1][0]
    owner.actions[1][1]()
    assert owner.windows == {}, "empty selection opens no dialog"
    selection[0] = NS(occurrences=(object(),))
    owner.actions[1][1]()
    dialog = StubDialog.instances[-1]
    assert len(owner.windows) == 1 and dialog.values == {"threshold": 400.0}
    monkeypatch.setattr(
        host_module,
        "apply_filter",
        lambda plugin, values: (NS(refused=[], skipped=[]), {"layers": 1}),
    )
    dialog.on_apply({"threshold": 42.0})
    assert redraws == [True] and dialog.closed == 0 and len(owner.windows) == 1
    assert owner.window_size == dialog.widget_size == (240, 120)
    deferred.pop(0)()
    assert dialog.closed == 1 and owner.windows == {}
    assert state.values("delete_small_paths") == {"threshold": 42.0}
    owner.actions[1][1]()
    dialog = StubDialog.instances[-1]
    monkeypatch.setattr(
        host_module,
        "apply_filter",
        lambda plugin, values: (NS(refused=["bad"], skipped=["auto"]), None),
    )
    dialog.on_apply({"threshold": 5})
    assert dialog.status.text == "Skipped: bad, auto" and len(owner.windows) == 1
    dialog.on_cancel()
    assert dialog.closed == 0
    deferred.pop(0)()
    assert dialog.closed == 1 and owner.windows == {}
    host.close()
    assert owner.actions == {} and errors == []


def test_filter_host_guards_selection_window_apply_and_remove_errors(
    tmp_path, monkeypatch
):
    import fontlab_plugmix.filters.host as host_module

    owner, errors = MenuOwner(), []
    state = registry.Registry(tmp_path)
    services = Services(
        NS(QtCore=NS(QTimer=NS(singleShot=lambda delay, callback: None))),
        NS(UpdateActiveCanvas=lambda: None),
        owner,
        object(),
        lambda error, source: errors.append(str(error)),
    )
    host = FilterHost(services, state)
    monkeypatch.setattr(host_module, "FilterDialog", StubDialog)
    host.install()
    monkeypatch.setattr(
        snapshot,
        "selected_layers",
        lambda: (_ for _ in ()).throw(RuntimeError("selection")),
    )
    owner.actions[1][1]()
    assert errors == ["selection"]
    monkeypatch.setattr(
        snapshot, "selected_layers", lambda: NS(occurrences=(object(),))
    )
    owner.fail_window = True
    owner.actions[1][1]()
    assert errors[-1] == "window failed" and StubDialog.instances[-1].closed == 1
    owner.fail_window = False
    owner.actions[1][1]()
    monkeypatch.setattr(
        host_module,
        "apply_filter",
        lambda plugin, values: (_ for _ in ()).throw(ValueError("write")),
    )
    guarded(
        host, services.sink, lambda: StubDialog.instances[-1].on_apply({"threshold": 2})
    )
    assert errors[-1] == "write"
    owner.fail_remove = True
    host.close()
    assert errors[-1] == "remove failed" and host.windows == {} and host.actions == []

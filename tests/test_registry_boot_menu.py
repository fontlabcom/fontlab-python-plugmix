# this_file: tests/test_registry_boot_menu.py
"""Registry discovery, persistence, menu toggling and boot ownership."""

import json
from types import SimpleNamespace as NS

import pytest

from fontlab_plugmix import boot, menu, registry
from fontlab_plugmix.reporter import Reporter


class Painters:
    def __init__(self, *args, **kwargs):
        self.calls = []
        self.closed = False

    def register(self, reporter, qt, sink):
        self.calls.append((reporter, qt, sink))
        return len(self.calls)

    def remove(self, token):
        self.calls.append(("remove", token))

    def close(self):
        self.closed = True


class Action:
    def __init__(self):
        self.checked = False

    def setChecked(self, value):
        self.checked = value


class Menus:
    def __init__(self, *args, **kwargs):
        self.actions = {}
        self.closed = False

    def add_action(self, section, title, callback, *, checkable):
        token = len(self.actions) + 1
        assert section == "View" and title.startswith("Plugmix: Show ") and checkable
        self.actions[token] = (Action(), callback)
        return token

    def action(self, token):
        return self.actions[token][0]

    def close(self):
        self.closed = True


def test_discovery_includes_builtins_and_entry_points(monkeypatch):
    class External(Reporter):
        name, title = "external", "External"

    points = NS(select=lambda group: [NS(load=lambda: External)])
    monkeypatch.setattr(registry.metadata, "entry_points", lambda: points)
    found = registry.discover()
    assert len(found) == 20
    assert found["external"] is External

    class Bad(Reporter):
        name, title = "node_indexes", "Collision"

    points.select = lambda group: [NS(load=lambda: Bad)]
    errors = []
    assert len(registry.discover(lambda error, source: errors.append(error))) == 19
    points.select = lambda group: [
        NS(load=lambda: object),
        NS(load=lambda: (_ for _ in ()).throw(ImportError("broken"))),
    ]
    assert len(registry.discover(lambda error, source: errors.append(error))) == 19
    assert [type(error) for error in errors] == [ValueError, TypeError, ImportError]


def test_registry_enable_disable_persists_and_restores(tmp_path):
    state = registry.Registry(tmp_path)
    assert len(state.available()) == 19
    assert state.enabled() == ()
    assert not state.path.exists(), "initialization must not write preferences"
    painters = Painters()
    state.attach(painters, object(), lambda e, p: None)
    assert state.enable("duplicate_anchors") is True
    assert state.enable("duplicate_anchors") is True
    assert len(painters.calls) == 1
    assert json.loads(state.path.read_text())["enabled"] == ["duplicate_anchors"]
    state.detach()
    assert state.enabled() == ("duplicate_anchors",)
    restored = registry.Registry(tmp_path)
    again = Painters()
    restored.attach(again, object(), lambda e, p: None)
    assert len(again.calls) == 1
    assert restored.toggle("duplicate_anchors") is False
    assert json.loads(state.path.read_text())["enabled"] == []
    assert restored.disable("duplicate_anchors") is False
    with pytest.raises(KeyError):
        restored.enable("missing")
    with pytest.raises(KeyError):
        restored.disable("missing")


def test_registry_skips_bad_json_and_proxy_functions(tmp_path, monkeypatch):
    path = tmp_path / "fontlab-plugmix.json"
    errors = []
    for raw in ('{"enabled": "bad"}', '{"enabled": [2]}', "{bad json"):
        path.write_text(raw)
        state = registry.Registry(tmp_path, lambda error, source: errors.append(error))
        assert state.enabled() == ()
        assert path.read_text() == raw, "install must preserve the bad document"
    assert len(errors) == 3
    path.unlink()
    monkeypatch.setattr(registry, "_current", None)
    current = registry.configure(tmp_path)
    assert registry.current() is current
    assert "node_indexes" in registry.available()
    assert registry.enable("node_indexes") is True
    assert registry.enabled() == ("node_indexes",)
    assert registry.toggle("node_indexes") is False
    assert registry.disable("node_indexes") is False


def test_registry_migrates_renamed_reporter_and_rolls_back_failed_save(tmp_path):
    path = tmp_path / "fontlab-plugmix.json"
    path.write_text('{"enabled": ["nodes_outside_paths"]}')
    state = registry.Registry(tmp_path)
    assert state.enabled() == ("offcurve_outside_bounds",)
    painters = Painters()
    state.attach(painters, object(), lambda error, source: None)
    assert len(painters.calls) == 1, "the renamed reporter should restore"
    state._save = lambda: (_ for _ in ()).throw(OSError("read-only"))
    with pytest.raises(OSError, match="read-only"):
        state.enable("duplicate_anchors")
    assert state.enabled() == ("offcurve_outside_bounds",)
    assert "duplicate_anchors" not in state._tokens
    assert painters.calls[-1] == ("remove", 2)
    assert path.read_text() == '{"enabled": ["nodes_outside_paths"]}'


def test_registry_detach_continues_and_save_error_survives_rollback_error(tmp_path):
    errors = []
    state = registry.Registry(tmp_path, lambda error, source: errors.append(str(error)))

    class BrokenPainters(Painters):
        def remove(self, token):
            super().remove(token)
            if token == 1 or getattr(self, "fail_all", False):
                raise TypeError("remove failed")

    painters = BrokenPainters()
    state.attach(painters, object(), lambda error, source: None)
    state.enable("center_lines")
    state.enable("duplicate_anchors")
    state.detach()
    assert ("remove", 2) in painters.calls
    assert state._tokens == {} and state._painters is None
    assert errors == ["remove failed"]

    state.attach(painters, object(), lambda error, source: None)
    painters.fail_all = True
    state._save = lambda: (_ for _ in ()).throw(OSError("save failed"))
    with pytest.raises(OSError, match="save failed"):
        state.enable("node_indexes")
    assert state.enabled() == ("center_lines", "duplicate_anchors")
    assert errors[-1] == "remove failed"


def test_registry_restores_other_reporters_when_one_constructor_fails(
    tmp_path, monkeypatch
):
    class Broken(Reporter):
        name, title = "broken", "Broken"

        def __init__(self):
            raise RuntimeError("plugin failed")

    path = tmp_path / "fontlab-plugmix.json"
    path.write_text('{"enabled": ["broken", "node_indexes"]}')
    classes = registry.discover()
    classes["broken"] = Broken
    monkeypatch.setattr(registry, "discover", lambda sink: classes)
    errors = []
    state = registry.Registry(tmp_path, lambda error, source: errors.append(error))
    painters = Painters()
    state.attach(painters, object(), lambda error, source: None)
    assert len(painters.calls) == 1
    assert painters.calls[0][0].name == "node_indexes"
    assert isinstance(errors[0], RuntimeError)


def test_menu_check_state_tracks_registry_even_after_failure(tmp_path):
    state = registry.Registry(tmp_path)
    owner = Menus()
    tokens = menu.install(owner, state)
    action, callback = owner.actions[tokens["node_indexes"]]
    assert action.checked is False
    callback()
    assert action.checked is True
    state.toggle = lambda name: (_ for _ in ()).throw(OSError("disk"))
    action.setChecked(False)
    with pytest.raises(OSError):
        callback()
    assert action.checked is True


def test_boot_install_is_idempotent_and_uninstall_preserves_preferences(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(boot, "_runtime", lambda: (object(), object(), Menus))
    monkeypatch.setattr(boot, "select_backend", lambda *args: Painters())
    monkeypatch.setattr(boot, "_state", None)
    boot.install(tmp_path)
    state = boot._state
    assert state is not None and len(state.menus.actions) == 19
    boot.install(tmp_path)
    assert boot._state is state
    with pytest.raises(ValueError):
        boot.install(tmp_path / "other")
    state.reporters.enable("center_lines")
    boot.uninstall()
    assert state.painters.closed and state.menus.closed
    assert json.loads(state.reporters.path.read_text())["enabled"] == ["center_lines"]
    boot.uninstall()
    boot.install(tmp_path)
    assert "center_lines" in registry.enabled()
    boot.uninstall()


def test_boot_runtime_imports_are_lazy(monkeypatch):
    modules = {
        "PythonQt": object(),
        "fontlab": object(),
        "fontlabapp.owned_menus": NS(OwnedMenus=Menus),
    }
    monkeypatch.setattr(boot, "import_module", modules.__getitem__)
    assert boot._runtime() == (modules["PythonQt"], modules["fontlab"], Menus)


def test_boot_cleans_up_failed_install_and_error_sink_never_raises(
    tmp_path, monkeypatch
):
    class FailingMenus(Menus):
        def add_action(self, section, title, callback, *, checkable):
            raise RuntimeError("menu missing")

    monkeypatch.setattr(boot, "_runtime", lambda: (object(), object(), FailingMenus))
    monkeypatch.setattr(boot, "select_backend", lambda *args: Painters())
    monkeypatch.setattr(boot, "_state", None)
    with pytest.raises(RuntimeError, match="menu missing"):
        boot.install(tmp_path)
    assert boot._state is None
    boot._error(ValueError("bad"), object())


def test_boot_closes_backend_if_menu_constructor_fails(tmp_path, monkeypatch):
    class FailingMenus:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("menu owner unavailable")

    painters = Painters()
    monkeypatch.setattr(boot, "_runtime", lambda: (object(), object(), FailingMenus))
    monkeypatch.setattr(boot, "select_backend", lambda *args: painters)
    monkeypatch.setattr(boot, "_state", None)
    with pytest.raises(RuntimeError, match="menu owner unavailable"):
        boot.install(tmp_path)
    assert painters.closed and boot._state is None

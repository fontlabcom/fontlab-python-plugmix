# this_file: tests/test_recovered_scripts.py
"""Exercise moved reporter bundles through App registration and owned menus."""

import json
import runpy
from pathlib import Path
from types import SimpleNamespace

import pytest

from fontlabapp.plugins import boot, registry
from plugmix_examples.duplicate_anchors import DuplicateAnchors
from fontlab_plugmix import boot as compatibility_boot
from test_registry_boot_menu import Action, Menus, Painters

ROOT = Path(__file__).resolve().parents[1]


class Submenu:
    """Record the owned View > Reporters menu used by the current App."""

    def __init__(self, parent, title):
        self.parent, self.title, self.entries = parent, title, []

    def addSeparator(self):
        self.entries.append("-")


class AppMenus(Menus):
    """Extend the compatibility fake with App's owned submenu/token contract."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menus = {}
        self.titles = {}

    def add_menu(self, section, title):
        token = -(len(self.menus) + 1)
        self.menus[token] = Submenu(section, title)
        return token

    def menu(self, token):
        return self.menus[token]

    def add_action(self, section, title, callback, *, checkable=False):
        if not isinstance(section, Submenu):
            return super().add_action(section, title, callback, checkable=checkable)
        if (section.parent, section.title) == ("Window", "Panels"):
            assert title in {"Reporters", "Step and Repeat", "Plugmix: Step and Repeat Panel"}
            assert checkable == (title != "Reporters")
            token = len(self.actions) + 1
            section.entries.append(title)
            self.actions[token] = (Action(), callback)
            return token
        assert (section.parent, section.title) == ("View", "Reporters")
        assert not title.startswith(("Plugmix", "Show "))
        assert checkable == (title != "Hide All")
        token = len(self.actions) + 1
        section.entries.append(title)
        self.actions[token] = (Action(), callback)
        self.titles[token] = title
        return token


@pytest.fixture
def app_runtime(tmp_path, monkeypatch):
    """Reuse existing fake host owners, keeping App code and preferences real."""
    path = tmp_path / "fontlab-plugmix.json"
    path.write_text('{"enabled": [], "params": {}, "preserved": true}')
    monkeypatch.setattr(registry, "DEFAULT_FILE", path)
    monkeypatch.setattr(registry, "DEFAULT_EXTENSIONS", ROOT / "Extensions")
    monkeypatch.setattr(registry, "_current", None)
    monkeypatch.setattr(boot, "_state", None)
    monkeypatch.setattr(boot, "_runtime", lambda: (object(), object(), AppMenus))
    monkeypatch.setattr(boot, "select_backend", lambda *args: Painters())
    for kind in ("ToolHost", "GeneralHost"):
        monkeypatch.setattr(
            boot, kind,
            lambda *args: SimpleNamespace(install=lambda: None, close=lambda: None),
        )
    monkeypatch.setattr(DuplicateAnchors, "handle_size", 8)
    monkeypatch.setattr(
        compatibility_boot, "_runtime",
        lambda: pytest.fail("Recovered scripts must use the App runtime"),
    )
    yield path
    boot.uninstall()


@pytest.mark.parametrize(
    "filename, name",
    [
        ('All Angles.py', 'all_angles'),
        ('Anchor Cloud.py', 'anchor_cloud'),
        ('Angled Handles.py', 'angled_handles'),
        ('Blindfold.py', 'blindfold'),
        ('Center Lines.py', 'center_lines'),
        ('Color Toner.py', 'color_toner'),
        ('Crosshair.py', 'crosshair'),
        ('Duplicate Anchor Rings.py', 'duplicate_anchors'),
        ('Emphasise Selected Handles.py', 'only_selected_handles'),
        ('Glyph Focus.py', 'glyph_focus'),
        ('Imprecise Italic Angle.py', 'imprecise_italic_angle'),
        ('Kern Indicator.py', 'kern_indicator'),
        ('Node Count.py', 'node_count'),
        ('Node Indexes.py', 'node_indexes'),
        ('Nodes Close to Zones.py', 'nodes_close_to_zones'),
        ('Off-curve Handles Outside Bounds.py', 'offcurve_outside_bounds'),
        ('RSB Line.py', 'rsb_line'),
        ('Rekha Viewer.py', 'rekha'),
        ('Segment Length.py', 'segment_length'),
        ('Selected Node Coordinates.py', 'selected_coordinates'),
        ('Show Background.py', 'show_background'),
        ('Show Character.py', 'show_character'),
        ('Show Export Status.py', 'export_status'),
        ('Show Global Glyph.py', 'global_glyph'),
        ('Show Glyphs In Label Color.py', 'glyphs_in_label_color'),
        ('Show Interpolation.py', 'show_interpolation'),
        ('Show Kerning Group Reference.py', 'kerning_group_reference'),
        ('Show Label Color.py', 'label_color'),
        ('Show Rotated.py', 'show_rotated'),
        ('Show Siblings.py', 'siblings'),
        ('Show Stems.py', 'show_stems'),
        ('Smart Plumblines.py', 'smart_plumblines'),
        ('Smooth Node Angles.py', 'smooth_node_angles'),
        ('Speed Punk.py', 'speed_punk'),
        ('Stem Thickness.py', 'stem_thickness'),
        ('Tops and Bottoms.py', 'tops_and_bottoms'),
        ('Two Point Distance.py', 'two_point_distance'),
        ('Unitizer.py', 'unitizer'),
        ('Vertical Metrics.py', 'vertical_metrics'),
    ],
)
def test_reporter_bundle_when_enabled_twice_then_registers_once_and_menu_disables(
    filename, name, app_runtime
):
    assert not (ROOT / "Scripts" / "Reports" / filename).exists()
    boot.install()
    registry.enable(name)
    registry.enable(name)
    state = boot._state
    assert state is not None
    assert registry.enabled() == (name,)
    assert len(state.painters.calls) == 1
    assert state.painters.calls[0][0].name == name
    saved = json.loads(app_runtime.read_text())
    assert saved["enabled"] == [name] and saved["preserved"] is True
    title = registry.available("reporter")[name].title.removeprefix("Show ")
    token, = [token for token, label in state.menus.titles.items() if label == title]
    action, toggle = state.menus.actions[token]
    toggle()
    assert registry.enabled() == () and action.checked is False
    assert state.painters.calls[-1] == ("remove", 1)
    assert json.loads(app_runtime.read_text())["enabled"] == []
    if name == "duplicate_anchors":
        assert DuplicateAnchors.handle_size == 8


def test_bundle_boot_when_run_twice_then_installs_all_reporter_actions(app_runtime):
    boot.install()
    state = boot._state
    boot.install()
    assert boot._state is state
    assert len(registry.available("reporter")) == 39
    assert len(state.menus.actions) == 43  # reporters, Hide All, Filter, Palette, core panel
    submenu, = [value for value in state.menus.menus.values()
                if (value.parent, value.title) == ("View", "Reporters")]
    assert (submenu.parent, submenu.title) == ("View", "Reporters")
    labels = sorted(cls.title.removeprefix("Show ")
                    for cls in registry.available("reporter").values())
    assert submenu.entries == labels + ["-", "Hide All"]
    assert registry.enabled() == () and state.painters.calls == []
    assert json.loads(app_runtime.read_text())["preserved"] is True
    for name in ("node_indexes", "center_lines"):
        title = registry.available("reporter")[name].title.removeprefix("Show ")
        token, = [token for token, label in state.menus.titles.items() if label == title]
        action, toggle = state.menus.actions[token]
        toggle()
        assert action.checked is True
    assert registry.enabled() == ("center_lines", "node_indexes")
    hide_token, = [token for token, title in state.menus.titles.items()
                   if title == "Hide All"]
    state.menus.actions[hide_token][1]()
    assert registry.enabled() == ()
    assert all(not state.menus.action(token).checked for token in state.menus.titles)
    assert state.painters.calls[-2:] == [("remove", 2), ("remove", 1)]
    saved = json.loads(app_runtime.read_text())
    assert saved["enabled"] == [] and saved["preserved"] is True


def test_reporter_bundle_when_save_fails_then_removes_registered_painter(
    app_runtime, monkeypatch
):
    boot.install()
    state = boot._state
    original = app_runtime.read_bytes()

    def fail_save():
        raise OSError("read-only fixture")

    monkeypatch.setattr(state.reporters, "_save", fail_save)
    with pytest.raises(OSError, match="read-only fixture"):
        registry.enable("node_indexes")
    assert registry.enabled() == ()
    assert state.painters.calls[-1] == ("remove", 1)
    assert app_runtime.read_bytes() == original


def test_reporters_action_when_run_then_shows_core_palette(monkeypatch):
    from fontlabapp import plugins

    calls = []
    monkeypatch.setattr(plugins, "show_reporters", lambda: calls.append("shown"))
    runpy.run_path(str(ROOT / "Scripts/Plugmix/Show Reporters.py"))
    assert calls == ["shown"]
    assert list((ROOT / "Scripts").rglob("*.py")) == [
        ROOT / "Scripts/Plugmix/Show Reporters.py"
    ]

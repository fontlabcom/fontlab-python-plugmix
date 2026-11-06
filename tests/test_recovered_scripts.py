# this_file: tests/test_recovered_scripts.py
"""Run the public script files against App's real discovery, registry and menus."""

import json
import runpy
from pathlib import Path
from types import SimpleNamespace

import pytest

from fontlabapp.plugmix import boot, registry
from fontlabapp.plugmix.plugins.duplicate_anchors import DuplicateAnchors
from fontlab_plugmix import boot as compatibility_boot
from test_registry_boot_menu import Menus, Painters

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def app_runtime(tmp_path, monkeypatch):
    """Reuse existing fake host owners, keeping App code and preferences real."""
    path = tmp_path / "fontlab-plugmix.json"
    path.write_text('{"enabled": [], "params": {}, "preserved": true}')
    monkeypatch.setattr(registry, "DEFAULT_FILE", path)
    monkeypatch.setattr(registry, "_current", None)
    monkeypatch.setattr(boot, "_state", None)
    monkeypatch.setattr(boot, "_runtime", lambda: (object(), object(), Menus))
    monkeypatch.setattr(boot, "select_backend", lambda *args: Painters())
    for kind in ("ToolHost", "GeneralHost"):
        monkeypatch.setattr(
            boot, kind,
            lambda *args: SimpleNamespace(install=lambda: None, close=lambda: None),
        )
    monkeypatch.setattr(DuplicateAnchors, "handle_size", 5)
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
def test_reporter_script_when_run_twice_then_registers_once_and_menu_disables(
    filename, name, app_runtime
):
    script = ROOT / "Scripts" / "Reports" / filename
    runpy.run_path(str(script))
    runpy.run_path(str(script))
    state = boot._state
    assert state is not None
    assert registry.enabled() == (name,)
    assert len(state.painters.calls) == 1
    assert state.painters.calls[0][0].name == name
    saved = json.loads(app_runtime.read_text())
    assert saved["enabled"] == [name] and saved["preserved"] is True
    token = sorted(registry.available("reporter")).index(name) + 1
    action, toggle = state.menus.actions[token]
    toggle()
    assert registry.enabled() == () and action.checked is False
    assert state.painters.calls[-1] == ("remove", 1)
    assert json.loads(app_runtime.read_text())["enabled"] == []
    if name == "duplicate_anchors":
        assert DuplicateAnchors.handle_size == 8


def test_menu_script_when_run_twice_then_installs_all_reporter_actions(app_runtime):
    script = ROOT / "Scripts" / "Plugmix" / "Install Plugmix Menu.py"
    runpy.run_path(str(script))
    state = boot._state
    runpy.run_path(str(script))
    assert boot._state is state
    assert len(registry.available("reporter")) == 39
    assert len(state.menus.actions) == 41  # reporters, Filter and Palette
    assert registry.enabled() == () and state.painters.calls == []
    assert json.loads(app_runtime.read_text())["preserved"] is True


def test_reporter_script_when_save_fails_then_removes_registered_painter(
    app_runtime, monkeypatch
):
    boot.install()
    state = boot._state
    original = app_runtime.read_bytes()

    def fail_save():
        raise OSError("read-only fixture")

    monkeypatch.setattr(state.reporters, "_save", fail_save)
    with pytest.raises(OSError, match="read-only fixture"):
        runpy.run_path(str(ROOT / "Scripts" / "Reports" / "Node Indexes.py"))
    assert registry.enabled() == ()
    assert state.painters.calls[-1] == ("remove", 1)
    assert app_runtime.read_bytes() == original

# this_file: tests/extensions/test_bundle_kinds.py
"""Exercise the concrete non-reporter examples loaded from their bundles."""

from dataclasses import replace
from types import SimpleNamespace as NS

import pytest

from fontlabapp.plugins.snapshot import Contour, Node
from fontlabapp.plugins.tool import ToolEvent
from plugmix_examples.delete_small_paths import DeleteSmallPaths, _small
from plugmix_examples.imprecise_italic_angle import ImpreciseItalicAngle
from plugmix_examples.only_selected_handles import OnlySelectedHandles
from plugmix_examples.smart_select import SmartSelect, touched_contours
from plugmix_examples.step_and_repeat import StepAndRepeat
from plugmix_examples.zoom_to_selection import ZoomToSelection
import plugmix_examples.step_and_repeat as repeat_module


def test_filter_preserves_open_and_threshold_paths_and_removes_small_closed(glyph):
    square = Contour(tuple(Node(x, y, True, False) for x, y in
                           [(0, 0), (10, 0), (10, 10), (0, 10)]), closed=True)
    opened = replace(square, closed=False)
    snapshot = replace(glyph, contours=(square, opened))
    plugin = DeleteSmallPaths()
    assert plugin.compute(snapshot, {"threshold": 100}).contours is None
    assert plugin.compute(snapshot, {"threshold": 101}).contours == (opened,)
    assert _small(Contour((), closed=True), 1)
    assert not _small(Contour((), closed=True), 0)
    controls = Contour((Node(0, 0, True, False),) +
                       (Node(1, 2, False, False),) * 3 +
                       (Node(5, 0, True, False),), closed=True)
    assert not _small(controls, 100)
    no_oncurve = Contour((Node(1, 1, False, False),) * 3, closed=True)
    assert not _small(no_oncurve, 100)
    curve = Contour((Node(0, 0, True, False), Node(1, 2, False, False),
                     Node(5, 0, True, False)), closed=True)
    assert _small(curve, 100)


def test_tool_drag_selects_only_touched_contours_and_clears_state(glyph):
    selected, redraw = [], []
    ctx = NS(snapshot=lambda: glyph, redraw=lambda: redraw.append(True),
             select=lambda indices, **kw: selected.append((indices, kw)))
    plugin = SmartSelect()
    event = ToolEvent(0, 0, 0, 0)
    assert plugin.move(event) is False and plugin.release(event) is False
    assert plugin.marks(glyph) == []
    plugin.activate(ctx)
    assert plugin.press(event)
    assert plugin.move(event) is False
    moved = replace(event, x=100, y=100, buttons=1, shift=True)
    assert plugin.move(moved) and redraw == [True]
    assert plugin.marks(glyph)[0].points[-1] == (0, 0)
    assert plugin.release(moved)
    assert selected == [((0,), {"toggle": True})]
    assert touched_contours(glyph, (200, 200), (300, 300)) == ()
    plugin.press(event)
    ctx.snapshot = lambda: None
    assert plugin.release(event)
    assert len(selected) == 1
    plugin.deactivate()
    assert plugin.ctx is None and plugin.origin is None and plugin.end is None


def test_general_zoom_notifies_only_without_selection():
    notices = []
    ctx = NS(zoom_selected=lambda: False,
             notify=lambda *args: notices.append(args))
    plugin = ZoomToSelection()
    plugin.start(ctx)
    plugin.run()
    assert notices == [("Zoom to Selection", "Select nodes in a Glyph window first")]
    ctx.zoom_selected = lambda: True
    plugin.run()
    assert len(notices) == 1
    plugin.stop()
    assert plugin.ctx is None


def test_palette_build_apply_refresh_and_failure_preserve_original_error(glyph, monkeypatch):
    labels, buttons, commands = [], [], []
    ui = NS(number=lambda title, value, **kw: value,
            label=lambda text: labels.append(text) or "status",
            button=lambda title, fn: buttons.append((title, fn)),
            value=lambda value: value,
            set_text=lambda target, text: labels.append(text),
            apply=lambda values: commands.append(values) or "Applied")
    plugin = StepAndRepeat()
    plugin.build(ui)
    assert len(buttons) == 1 and buttons[0][0] == "Apply"
    buttons[0][1]()
    assert commands == [{"count": 1, "dx": 0, "dy": 50}]
    assert labels[-1] == "Applied"
    plugin.refresh(glyph)
    assert labels[-1] == "1 selected contours."
    plugin.refresh(None)
    assert labels[-1] == "0 selected contours."
    monkeypatch.setattr(repeat_module, "repeat_selected", lambda v, s: (1, 1, "Repeated"))
    assert plugin.command({}, object()) == "Repeated"

    def fail_apply(values):
        raise ValueError("refused")

    ui.apply = fail_apply
    with pytest.raises(ValueError, match="refused"):
        plugin._clicked()
    assert labels[-1] == "refused"

    def fail_status(*args):
        raise RuntimeError("dead widget")

    ui.set_text = fail_status
    with pytest.raises(ValueError, match="refused"):
        plugin._clicked()
    plugin.close()
    assert plugin.ui is None


def test_reporters_ignore_curves_horizontal_and_unselected_handles(glyph):
    contour = Contour((Node(0, 0, True, False), Node(0, 10, False, False),
                       Node(10, 20, True, False), Node(20, 20, True, False),
                       Node(20, 0, True, False)), closed=False)
    flat = replace(glyph, contours=(contour,),
                   metrics=replace(glyph.metrics, italic_slant=0))
    assert ImpreciseItalicAngle().compute(flat) == []
    assert OnlySelectedHandles().compute(flat) == []
    handles = Contour((Node(1, 1, False, False), Node(2, 2, False, False)), closed=False)
    assert OnlySelectedHandles().compute(replace(flat, contours=(handles,))) == []

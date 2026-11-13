# SPDX-License-Identifier: Apache-2.0
# this_file: Extensions/general/ZoomToSelection.fontlabGeneral/zoom_to_selection.py
"""Fit selected nodes in the active Glyph canvas without changing font data.

This keeps the menu action from TzuYuan Yin's Zoom to Selection behaviour;
the source's delayed viewport adjustment and shortcut are omitted.
"""

from fly.ap.plugins.general import General, GeneralContext


class ZoomToSelection(General):
    """Zoom the active canvas to the current node selection."""

    name = "zoom_to_selection"
    title = "Plugmix: Zoom to Selection"
    menu = "View"

    def start(self, ctx: GeneralContext) -> None:
        self.ctx = ctx

    def stop(self) -> None:
        self.ctx = None

    def run(self) -> None:
        if not self.ctx.zoom_selected():
            self.ctx.notify("Zoom to Selection", "Select nodes in a Glyph window first")

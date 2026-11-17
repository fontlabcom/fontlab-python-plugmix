# this_file: Extensions/palettes/StepAndRepeat.fontlabpalette/step_and_repeat.py
# SPDX-License-Identifier: Apache-2.0
"""Repeat selected contours at cumulative x/y offsets in the current glyph."""

from typing import Any

from fly.ap.plugins.palette import Palette
from fly.ap.plugins.palettes.apply import repeat_selected, selected_indices
from fly.ap.plugins.snapshot import GlyphSnapshot


class StepAndRepeat(Palette):
    """A small docked contour duplication control, with one Apply Undo step."""

    name = "step_and_repeat"
    title = "Step and Repeat"

    def build(self, ui: Any) -> None:
        """Create number fields and the Apply command once."""
        self.ui = ui
        self.count = ui.number("Copies", 1, integer=True, minimum=0, maximum=100)
        self.dx = ui.number("X offset", 0)
        self.dy = ui.number("Y offset", 50)
        self.status = ui.label("Select a contour, then Apply.")
        ui.button("Apply", self._clicked)

    def _clicked(self) -> None:
        """Read live control values and show the resulting status message."""
        try:
            values = {
                key: self.ui.value(getattr(self, key)) for key in ("count", "dx", "dy")
            }
            self.ui.set_text(self.status, self.ui.apply(values))
        except Exception as error:
            try:
                self.ui.set_text(self.status, str(error))
            except Exception:  # noqa: BLE001, S110 - retain original Apply error
                pass
            raise

    def command(self, values: dict[str, Any], services: Any) -> str:
        """Apply to the current glyph through the shared outline writer."""
        return repeat_selected(values, services)[2]

    def refresh(self, context: GlyphSnapshot | None) -> None:
        """Show how many current contours contain a selected node."""
        count = len(selected_indices(context)) if context else 0
        self.ui.set_text(self.status, f"{count} selected contours.")

    def close(self) -> None:
        """Release the UI reference after the host disconnects its signals."""
        self.ui = None

# this_file: Scripts/Reports/Selected Node Coordinates.py
# SPDX-License-Identifier: Apache-2.0
"""Show Selected Node Coordinates.

Display coordinates for every selected node, including handles. Turns the
reporter on in every Glyph window; use View > Plugmix: Show Selected Node
Coordinates to turn it off. No font data is written; Plugmix saves the
enabled names in fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("selected_coordinates")

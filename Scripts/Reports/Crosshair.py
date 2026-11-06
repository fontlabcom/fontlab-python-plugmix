# this_file: Scripts/Reports/Crosshair.py
# SPDX-License-Identifier: Apache-2.0
"""Show Crosshair.

Extend selected-node guides far beyond normal Glyph window extents. Turns
the reporter on in every Glyph window; use View > Plugmix: Show Crosshair to
turn it off. No font data is written; Plugmix saves the enabled names in
fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("crosshair")

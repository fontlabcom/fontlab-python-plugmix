# this_file: Scripts/Reports/Color Toner.py
# SPDX-License-Identifier: Apache-2.0
"""Show Color Toner.

One odd-even polygon per component, alpha taken from `darken` wrapped into
0..1. Turns the reporter on in every Glyph window; use View > Plugmix: Show
Color Toner to turn it off. No font data is written; Plugmix saves the
enabled names in fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("color_toner")

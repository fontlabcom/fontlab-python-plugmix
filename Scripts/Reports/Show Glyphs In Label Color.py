# this_file: Scripts/Reports/Show Glyphs In Label Color.py
# SPDX-License-Identifier: Apache-2.0
"""Show Glyphs In Label Color.

One odd-even polygon over every contour so counters stay open. Turns the
reporter on in every Glyph window; use View > Plugmix: Show Glyphs In Label
Color to turn it off. No font data is written; Plugmix saves the enabled
names in fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("glyphs_in_label_color")

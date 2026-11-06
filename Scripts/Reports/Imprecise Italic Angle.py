# this_file: Scripts/Reports/Imprecise Italic Angle.py
# SPDX-License-Identifier: Apache-2.0
"""Show Imprecise Italic Angle.

Check each straight segment against the master's vertical slant. Turns the
reporter on in every Glyph window; use View > Plugmix: Show Imprecise Italic
Angle to turn it off. No font data is written; Plugmix saves the enabled
names in fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("imprecise_italic_angle")

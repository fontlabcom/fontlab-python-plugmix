# this_file: Scripts/Reports/Tops and Bottoms.py
# SPDX-License-Identifier: Apache-2.0
"""Show Tops and Bottoms.

Show all tied extrema, preserving their exact y values. Turns the reporter
on in every Glyph window; use View > Plugmix: Show Tops and Bottoms to turn
it off. No font data is written; Plugmix saves the enabled names in fontlab-
plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("tops_and_bottoms")

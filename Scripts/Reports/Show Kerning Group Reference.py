# this_file: Scripts/Reports/Show Kerning Group Reference.py
# SPDX-License-Identifier: Apache-2.0
"""Show Kerning Group Reference.

Members of each class overlap at one spot per side; LTR only. Turns the
reporter on in every Glyph window; use View > Plugmix: Show Kerning Group
Reference to turn it off. No font data is written; Plugmix saves the enabled
names in fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("kerning_group_reference")

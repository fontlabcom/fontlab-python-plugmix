# this_file: Scripts/Reports/Show Siblings.py
# SPDX-License-Identifier: Apache-2.0
"""Show Siblings.

Each present sibling is one green polygon at the glyph origin; Latin only.
Turns the reporter on in every Glyph window; use View > Plugmix: Show
Siblings to turn it off. No font data is written; Plugmix saves the enabled
names in fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("siblings")

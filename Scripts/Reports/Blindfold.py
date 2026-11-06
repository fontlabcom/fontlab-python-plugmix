# this_file: Scripts/Reports/Blindfold.py
# SPDX-License-Identifier: Apache-2.0
"""Show Blindfold.

Two opaque blocks leave only the band from baseline to the chosen height.
Turns the reporter on in every Glyph window; use View > Plugmix: Show
Blindfold to turn it off. No font data is written; Plugmix saves the enabled
names in fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("blindfold")

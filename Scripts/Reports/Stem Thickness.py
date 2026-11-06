# this_file: Scripts/Reports/Stem Thickness.py
# SPDX-License-Identifier: Apache-2.0
"""Show Stem Thickness.

Nearer crossing only; no guide command and no modifier key. Turns the
reporter on in every Glyph window; use View > Plugmix: Show Stem Thickness
to turn it off. No font data is written; Plugmix saves the enabled names in
fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("stem_thickness")

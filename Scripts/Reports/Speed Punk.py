# this_file: Scripts/Reports/Speed Punk.py
# SPDX-License-Identifier: Apache-2.0
"""Show Speed Punk.

Shade the outline's curvature as a comb whose colour tracks |k|. Turns the
reporter on in every Glyph window; use View > Plugmix: Show Speed Punk to
turn it off. No font data is written; Plugmix saves the enabled names in
fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("speed_punk")

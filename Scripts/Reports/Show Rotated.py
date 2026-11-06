# this_file: Scripts/Reports/Show Rotated.py
# SPDX-License-Identifier: Apache-2.0
"""Show Rotated.

Draw the half-turned outline, its on-curve rings and a centre cross. Turns
the reporter on in every Glyph window; use View > Plugmix: Show Rotated to
turn it off. No font data is written; Plugmix saves the enabled names in
fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("show_rotated")

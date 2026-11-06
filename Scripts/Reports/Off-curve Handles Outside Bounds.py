# this_file: Scripts/Reports/Off-curve Handles Outside Bounds.py
# SPDX-License-Identifier: Apache-2.0
"""Show Off-curve Handles Outside Bounds.

Use on-curve extrema as the comparison bounds. Turns the reporter on in
every Glyph window; use View > Plugmix: Show Off-curve Handles Outside
Bounds to turn it off. No font data is written; Plugmix saves the enabled
names in fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("offcurve_outside_bounds")

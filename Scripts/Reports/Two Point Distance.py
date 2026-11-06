# this_file: Scripts/Reports/Two Point Distance.py
# SPDX-License-Identifier: Apache-2.0
"""Show Two Point Distance.

Measure both on-curve and off-curve selected points. Turns the reporter on
in every Glyph window; use View > Plugmix: Show Two Point Distance to turn
it off. No font data is written; Plugmix saves the enabled names in fontlab-
plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("two_point_distance")

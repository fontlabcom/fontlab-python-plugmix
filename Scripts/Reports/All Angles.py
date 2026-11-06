# this_file: Scripts/Reports/All Angles.py
# SPDX-License-Identifier: Apache-2.0
"""Show All Angles.

Show bearings from vertical, 0 to 180 degrees, for lines and handles. Turns
the reporter on in every Glyph window; use View > Plugmix: Show All Angles
to turn it off. No font data is written; Plugmix saves the enabled names in
fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("all_angles")

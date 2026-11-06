# this_file: Scripts/Reports/Show Interpolation.py
# SPDX-License-Identifier: Apache-2.0
"""Show Interpolation.

One odd-even polygon per compatible master; no instances, no recentering.
Turns the reporter on in every Glyph window; use View > Plugmix: Show
Interpolation to turn it off. No font data is written; Plugmix saves the
enabled names in fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("show_interpolation")

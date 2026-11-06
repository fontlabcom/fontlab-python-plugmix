# this_file: Scripts/Reports/Center Lines.py
# SPDX-License-Identifier: Apache-2.0
"""Show Center Lines.

Draw requested font-wide center lines with no font modification. Turns the
reporter on in every Glyph window; use View > Plugmix: Show Center Lines to
turn it off. No font data is written; Plugmix saves the enabled names in
fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("center_lines")

# this_file: Scripts/Reports/Smart Plumblines.py
# SPDX-License-Identifier: Apache-2.0
"""Show Smart Plumblines.

Centre crosses for each contour and for the selected nodes. Turns the
reporter on in every Glyph window; use View > Plugmix: Show Smart Plumblines
to turn it off. No font data is written; Plugmix saves the enabled names in
fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("smart_plumblines")

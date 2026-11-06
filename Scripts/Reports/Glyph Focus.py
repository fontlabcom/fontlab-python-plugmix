# this_file: Scripts/Reports/Glyph Focus.py
# SPDX-License-Identifier: Apache-2.0
"""Show Glyph Focus.

Leave the current glyph's advance box unobscured. Turns the reporter on in
every Glyph window; use View > Plugmix: Show Glyph Focus to turn it off. No
font data is written; Plugmix saves the enabled names in fontlab-
plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("glyph_focus")

# this_file: Scripts/Reports/Show Stems.py
# SPDX-License-Identifier: Apache-2.0
"""Show Stems.

Scan at half x-height (half cap height for tall glyphs) and label spans.
Turns the reporter on in every Glyph window; use View > Plugmix: Show Stems
to turn it off. No font data is written; Plugmix saves the enabled names in
fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("show_stems")

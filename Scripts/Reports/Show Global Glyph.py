# this_file: Scripts/Reports/Show Global Glyph.py
# SPDX-License-Identifier: Apache-2.0
"""Show Global Glyph.

Closed paths orange, open paths blue, both with a faint fill; components not
read. Turns the reporter on in every Glyph window; use View > Plugmix: Show
Global Glyph to turn it off. No font data is written; Plugmix saves the
enabled names in fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("global_glyph")

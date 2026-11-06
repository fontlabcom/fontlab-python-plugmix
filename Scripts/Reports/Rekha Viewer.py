# this_file: Scripts/Reports/Rekha Viewer.py
# SPDX-License-Identifier: Apache-2.0
"""Show Rekha Viewer.

Bar from -overshoot to the advance; `rekha` and `rekha_stop` anchors move
it. Turns the reporter on in every Glyph window; use View > Plugmix: Show
Rekha Viewer to turn it off. No font data is written; Plugmix saves the
enabled names in fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("rekha")

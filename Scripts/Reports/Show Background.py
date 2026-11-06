# this_file: Scripts/Reports/Show Background.py
# SPDX-License-Identifier: Apache-2.0
"""Show Background.

One odd-even polygon over the background outlines; its components are not
read. Turns the reporter on in every Glyph window; use View > Plugmix: Show
Background to turn it off. No font data is written; Plugmix saves the
enabled names in fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("show_background")

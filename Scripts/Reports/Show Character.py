# this_file: Scripts/Reports/Show Character.py
# SPDX-License-Identifier: Apache-2.0
"""Show Character.

First Unicode as 100-px text; hidden when zoomed far out. Turns the reporter
on in every Glyph window; use View > Plugmix: Show Character to turn it off.
No font data is written; Plugmix saves the enabled names in fontlab-
plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("show_character")

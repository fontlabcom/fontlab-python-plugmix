# this_file: Scripts/Reports/Unitizer.py
# SPDX-License-Identifier: Apache-2.0
"""Show Unitizer.

Display simple unit increments behind the active glyph. Turns the reporter
on in every Glyph window; use View > Plugmix: Show Unitizer to turn it off.
No font data is written; Plugmix saves the enabled names in fontlab-
plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("unitizer")

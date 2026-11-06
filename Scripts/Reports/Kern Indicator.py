# this_file: Scripts/Reports/Kern Indicator.py
# SPDX-License-Identifier: Apache-2.0
"""Show Kern Indicator.

Positive values orange, negative blue; shown only at 3% to 90% zoom. Turns
the reporter on in every Glyph window; use View > Plugmix: Show Kern
Indicator to turn it off. No font data is written; Plugmix saves the enabled
names in fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("kern_indicator")

# this_file: Scripts/Reports/Node Count.py
# SPDX-License-Identifier: Apache-2.0
"""Show Node Count.

Count on- and off-curve nodes across all contours. Turns the reporter on in
every Glyph window; use View > Plugmix: Show Node Count to turn it off. No
font data is written; Plugmix saves the enabled names in fontlab-
plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("node_count")

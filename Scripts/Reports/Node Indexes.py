# this_file: Scripts/Reports/Node Indexes.py
# SPDX-License-Identifier: Apache-2.0
"""Show Node Indexes.

Use original contour indexes at all node positions. Turns the reporter on in
every Glyph window; use View > Plugmix: Show Node Indexes to turn it off. No
font data is written; Plugmix saves the enabled names in fontlab-
plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("node_indexes")

# this_file: Scripts/Reports/Smooth Node Angles.py
# SPDX-License-Identifier: Apache-2.0
"""Show Smooth Node Angles.

Show local smoothness and proportion for nodes with two handles. Turns the
reporter on in every Glyph window; use View > Plugmix: Show Smooth Node
Angles to turn it off. No font data is written; Plugmix saves the enabled
names in fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("smooth_node_angles")

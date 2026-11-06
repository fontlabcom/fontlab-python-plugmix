# this_file: Scripts/Reports/Nodes Close to Zones.py
# SPDX-License-Identifier: Apache-2.0
"""Show Nodes Close to Zones.

Find near misses against selected-master PostScript zones and metrics. Turns
the reporter on in every Glyph window; use View > Plugmix: Show Nodes Close
to Zones to turn it off. No font data is written; Plugmix saves the enabled
names in fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("nodes_close_to_zones")

# this_file: Scripts/Reports/Segment Length.py
# SPDX-License-Identifier: Apache-2.0
"""Show Segment Length.

Prefer segments with both on-curve ends selected; otherwise show all. Turns
the reporter on in every Glyph window; use View > Plugmix: Show Segment
Length to turn it off. No font data is written; Plugmix saves the enabled
names in fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("segment_length")

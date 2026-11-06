# this_file: Scripts/Reports/Anchor Cloud.py
# SPDX-License-Identifier: Apache-2.0
"""Show Anchor Cloud.

Annotate the current layer's anchor positions without font-wide reads. Turns
the reporter on in every Glyph window; use View > Plugmix: Show Anchor Cloud
to turn it off. No font data is written; Plugmix saves the enabled names in
fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("anchor_cloud")

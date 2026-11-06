# this_file: Scripts/Reports/Show Export Status.py
# SPDX-License-Identifier: Apache-2.0
"""Show Export Status.

Red cross corner to corner over the body, slanted by the italic angle. Turns
the reporter on in every Glyph window; use View > Plugmix: Show Export
Status to turn it off. No font data is written; Plugmix saves the enabled
names in fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("export_status")

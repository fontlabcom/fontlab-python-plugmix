# this_file: Scripts/Reports/Emphasise Selected Handles.py
# SPDX-License-Identifier: Apache-2.0
"""Show Emphasise Selected Handles.

Connect selected endpoints to their neighbouring off-curves. Turns the
reporter on in every Glyph window; use View > Plugmix: Show Emphasise
Selected Handles to turn it off. No font data is written; Plugmix saves the
enabled names in fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("only_selected_handles")

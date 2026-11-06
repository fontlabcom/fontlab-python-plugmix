# this_file: Scripts/Reports/Angled Handles.py
# SPDX-License-Identifier: Apache-2.0
"""Show Angled Handles.

Flag handles with an axis mismatch greater than a small angle. Turns the
reporter on in every Glyph window; use View > Plugmix: Show Angled Handles
to turn it off. No font data is written; Plugmix saves the enabled names in
fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("angled_handles")

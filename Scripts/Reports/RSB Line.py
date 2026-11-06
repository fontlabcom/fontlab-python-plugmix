# this_file: Scripts/Reports/RSB Line.py
# SPDX-License-Identifier: Apache-2.0
"""Show RSB Line.

Annotate sidebearings from on-curve x extrema. Turns the reporter on in
every Glyph window; use View > Plugmix: Show RSB Line to turn it off. No
font data is written; Plugmix saves the enabled names in fontlab-
plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("rsb_line")

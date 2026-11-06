# this_file: Scripts/Reports/Vertical Metrics.py
# SPDX-License-Identifier: Apache-2.0
"""Show Vertical Metrics.

Annotate ascender, descender, x-height, cap height and baseline. Turns the
reporter on in every Glyph window; use View > Plugmix: Show Vertical Metrics
to turn it off. No font data is written; Plugmix saves the enabled names in
fontlab-plugmix.json.
"""

from fontlabapp.plugmix import install, registry

install()
registry.enable("vertical_metrics")

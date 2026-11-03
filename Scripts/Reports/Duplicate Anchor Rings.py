# this_file: Scripts/Reports/Duplicate Anchor Rings.py
# SPDX-License-Identifier: Apache-2.0
"""Enable duplicate-anchor rings in every Glyph window across all tools.

Each unordered anchor pair less than one font unit apart gets an unfilled
red/yellow ring at the first anchor. Three coincident anchors produce three
ring pairs. Use View > Plugmix: Show Duplicate Anchor Rings to disable it.
Set HANDLE_SIZE below to 5, 8 or 12 before running this script.
No font data is written; plugmix remembers only the enabled reporter names.
"""

from fontlab_plugmix import install, registry
from fontlab_plugmix.plugins.duplicate_anchors import DuplicateAnchors

HANDLE_SIZE = 8
DuplicateAnchors.set_handle_size(HANDLE_SIZE)
install()
registry.enable("duplicate_anchors")

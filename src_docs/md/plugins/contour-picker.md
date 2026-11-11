---
this_file: src_docs/md/plugins/contour-picker.md
---

# Contour Picker

Bundle: `Extensions/tools/ContourPicker.fontlabTool`  
Stable ID: `contour_picker`

Select an entire local contour with one click. Activate Contour Picker from
Tools > Tool or the toolbar, then left-click within **12 view pixels** of any
of its nodes. The contour containing the nearest node replaces the existing
contour selection. Hold **Shift** to toggle that contour instead.

Both on-curve and off-curve nodes count, on open and closed contours. Equal
distances prefer the first contour in snapshot order. Components are excluded:
their decomposed contour indices do not identify editable local contours.
Clicking with no nearby local node leaves the selection unchanged. The hit
radius stays fixed as zoom changes; no usable scale means no hit.

Use it to select a small contour before applying Step and Repeat. This is a
node-proximity picker, not a curve-distance or filled-area picker: a click near
the middle of a long segment may miss even when it looks close to the outline.
It changes selection only, with no geometry edit or geometry Undo step. There
is no parameter dialog, drag selection or double-click containment behavior.

## Acceptance limits

Native toolbar placement, pointer/keyboard delivery, zoom mapping and teardown
remain unverified for the exact installed App/Plugmix tuple. Offline behavior
does not establish native acceptance. See [installation](../installation.md)
and the [Extensions catalogue](../app-menu-scripts.md).

---
this_file: src_docs/md/plugins/measurement-ruler.md
---

# Measurement Ruler

Bundle: `Extensions/tools/MeasurementRuler.fontlabTool`  
Stable ID: `measurement_ruler`

Measure an arbitrary span without selecting nodes. Activate Measurement Ruler
from Tools > Tool or the toolbar, then drag with the left mouse button from
one point to another. Release to retain the ruler; a new drag replaces it.

- Hold **Shift** while dragging or releasing to constrain the endpoint to the
  nearest horizontal or vertical axis. Equal X/Y distances choose horizontal.
- Press **Escape** to clear the ruler.
- The label shows length in font units, signed `dx` and `dy`, and the angle
  counterclockwise from positive X, each to two decimal places.

Use it to compare a counter span or an offset visually. Endpoints follow the
pointer: there is no node snapping, ink intersection measurement or guide
creation. It works independently of components and curve types because it
measures two points, not contours. Switching glyph/layer source or deactivating
the tool clears the ruler. No geometry or selection is changed.

## Acceptance limits

Native toolbar placement, pointer/keyboard delivery, zoom mapping and teardown
remain unverified for the exact installed App/Plugmix tuple. Offline behavior
does not establish native acceptance. See [installation](../installation.md)
and the [Extensions catalogue](../app-menu-scripts.md).

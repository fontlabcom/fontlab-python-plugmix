---
this_file: src_docs/md/plugins/scale-outlines.md
---

# Scale Outlines

Bundle: `Extensions/filters/ScaleOutlines.fontlabfilter`  
Stable ID: `scale_outlines`

Resize drawn outlines about a fixed pivot. Open this filter from the Glyph
menu, set horizontal and vertical percentages and the pivot, and apply it to
selected glyphs. X = 90 and Y = 100 narrows outlines to 90% without changing
height. With the default pivot, the glyph origin stays fixed.

| Parameter | Default | Pure API allowed values |
| --- | --- | --- |
| X scale (%) (`x_percent`) | 100% | At least 0.001% |
| Y scale (%) (`y_percent`) | 100% | At least 0.001% |
| Pivot X (`pivot_x`) | 0 font units | Finite number |
| Pivot Y (`pivot_y`) | 0 font units | Finite number |

Each coordinate is scaled relative to the pivot. Negative and zero scales are
not accepted, so this filter does not mirror or collapse outlines. Both scales
at 100% leave them unchanged. Recheck spacing and anchor placement separately.

App's numeric dialog fields use three decimal places. Fields without an
explicit minimum or maximum use dialog bounds of −1,000,000 or 1,000,000
respectively; the pure parameter API accepts the values listed above.

## Scope and safety

The four coordinate filters require the coordinated App coordinate-writer
change. Older App versions with the deletion-only Filter writer cannot apply
them. No released App version has yet been assigned to this requirement; use
the reviewed paired App/Plugmix source tuple, not the manifest minimum alone.

A partial native write follows App's existing `PartialWriteError` recovery:
use **Edit > Undo** as directed by the error. It does not automatically roll
back completed writes. Native Undo/Redo recovery remains unverified.


This filter changes every node of the selected glyphs' own outlines in the
current master, including off-curve controls. It does not transform components,
anchors or advance widths, and does not limit the edit to selected nodes.
Node order, node flags, contour closure and native curve types are retained;
curves are not flattened or reconstructed. App owns the guarded writer and
geometry Undo step. Automatic layers and unsafe shared or transformed outlines
are refused per glyph; safe glyphs can still be processed.

Empty outlines and unchanged results are no-ops. Non-finite parameters,
non-finite coordinates and arithmetic overflow are rejected. Native dialog
behavior, Undo/Redo and saved/reopened results remain unverified for the exact
installed App/Plugmix tuple.

See [installation](../installation.md) and the
[Extensions catalogue](../app-menu-scripts.md).

---
this_file: src_docs/md/plugins/slant-outlines.md
---

# Slant Outlines

Bundle: `Extensions/filters/SlantOutlines.fontlabFilter`  
Stable ID: `slant_outlines`

Apply a geometric shear to drawn outlines. Open this filter from the Glyph
menu, set **Rightward angle (degrees)** and **Pivot Y**, then apply it to selected glyphs. An angle
of 10° with Pivot Y = 0 leans points above the baseline to the right while
keeping baseline points fixed. This is geometric slant, not optical correction.

| Parameter | Default | Pure API allowed values |
| --- | --- | --- |
| Rightward angle (degrees) (`angle`) | 0° | −85° through 85° |
| Pivot Y (`pivot_y`) | 0 font units | Finite number |

The operation is `x = x + tan(angle) * (y - pivot_y)`; Y stays unchanged.
Positive angles move points above the pivot right and points below it left.
Zero angle leaves the outlines unchanged. This does not change the font's
italic-angle metadata. Recheck spacing, anchors and curve appearance separately.

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

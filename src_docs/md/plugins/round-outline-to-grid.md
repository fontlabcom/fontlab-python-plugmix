---
this_file: src_docs/md/plugins/round-outline-to-grid.md
---

# Round Outline to Grid

Bundle: `Extensions/filters/RoundOutlineToGrid.fontlabFilter`  
Stable ID: `round_outline_to_grid`

Round fractional outline coordinates to a regular grid before checking point
alignment. Open this filter from the Glyph menu, set **Grid spacing**, and apply it to
the selected glyphs. A grid of 1 rounds to whole font units; 0.5 gives half-unit
positions. Review curves afterwards: rounding handles can alter their shape.

| Parameter | Default | Pure API allowed values |
| --- | --- | --- |
| Grid spacing (`grid`) | 1 font unit | At least 0.000001 |

Coordinates are rounded independently to the nearest grid multiple. Halfway
values round toward positive infinity: on a unit grid, 0.5 becomes 1 and −0.5
becomes 0. The grid is anchored at the glyph origin.

App's numeric dialog fields use three decimal places. Fields without an
explicit minimum or maximum use dialog bounds of −1,000,000 or 1,000,000
respectively; the pure parameter API accepts the values listed above.
The pure API accepts grid spacing down to 0.000001, but that precision
cannot be entered in the current dialog. Use at least 0.001 in the dialog;
a value rounded to zero fails validation.

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

---
this_file: src_docs/md/app-menu-scripts.md
---

# App Extensions catalogue

All 39 reporter bundles below live in `Extensions/reporters/`. Each has its own
`plugin.json` and Python source; no package install or individual launcher is
needed for a bundle. Bundles and the action require `fontlab-fly>=1.3.0`
and its providers; their API imports use `fly.ap`, preserving canonical App identity. App's `fontlabapp.plugins` core owns discovery, painter
registration, preferences, rollback and teardown. `fontlabapp.plugmix` remains
a deprecated import shim, separate from the retained `fontlab_plugmix` runtime.

App's startup hook discovers the Extensions folder. Enable or disable reporters
in the Reporters palette or View > Reporters; enabling persists the stable ID.
Reporters do not edit font geometry. `Scripts/Plugmix/Show Reporters.py` is the
remaining optional action script: it opens the palette. Do not combine the two
runtimes' startup paths. See [installation](installation.md) for setup.

| Bundle name / reporter | Overlay and limits |
| --- | --- |
| `AllAngles.fontlabReporter` — All Angles | Angle of each straight segment from vertical, mod 180°; components excluded |
| `AnchorCloud.fontlabReporter` — Anchor Cloud | Names and positions of the current glyph's anchors (local anchors only) |
| `AngledHandles.fontlabReporter` — Angled Handles | Rings on handles off the horizontal, vertical and italic axes |
| `Blindfold.fontlabReporter` — Blindfold | Opaque blocks hide the strip from 70 units under the descender up to the baseline, and everything from x-height up to 70 units over the ascender (`band = "cap_height"` for cap height); the band between baseline and that height stays visible |
| `CenterLines.fontlabReporter` — Center Lines | Advance/2, x-height/2 and cap-height/2 lines |
| `ColorToner.fontlabReporter` — Color Toner | Each component filled in translucent black (`darken = 0.15`, wrapped into 0..1) so composed parts stand out from drawn outlines |
| `Crosshair.fontlabReporter` — Crosshair | Long guides through selected nodes; no mouse tracking |
| `DuplicateAnchors.fontlabReporter` — Duplicate Anchor Rings | Red/yellow rings for every anchor pair less than one unit apart |
| `OnlySelectedHandles.fontlabReporter` — Emphasise Selected Handles | Accent lines and rings for handles next to selected nodes |
| `GlyphFocus.fontlabReporter` — Glyph Focus | Shade outside the advance box between descender and ascender |
| `ImpreciseItalicAngle.fontlabReporter` — Imprecise Italic Angle | Straight segments within 2° of the slant but not on it |
| `KernIndicator.fontlabReporter` — Kern Indicator | Displayed kerning of the pairs touching the glyph, above each junction (orange positive, blue negative); shown only between 3% and 90% zoom |
| `NodeCount.fontlabReporter` — Node Count | Total on- and off-curve nodes; components excluded |
| `NodeIndexes.fontlabReporter` — Node Indexes | Contour index beside every node |
| `NodesCloseToZones.fontlabReporter` — Nodes Close to Zones | Rings on on-curves near zone edges or metric heights |
| `OffcurveOutsideBounds.fontlabReporter` — Off-curve Handles Outside Bounds | Handles beyond the on-curve bounding rectangle |
| `RSBLine.fontlabReporter` — RSB Line | Advance boundary with RSB and LSB labels |
| `Rekha.fontlabReporter` — Rekha Viewer | Head-line bar for Devanagari, Bengali and Gurmukhi letters, moved by `rekha` and `rekha_stop` anchors; suffixed or interrupted anchors are not supported |
| `SegmentLength.fontlabReporter` — Segment Length | Straight and flattened curve lengths |
| `SelectedCoordinates.fontlabReporter` — Selected Node Coordinates | Coordinates beside selected nodes |
| `ShowBackground.fontlabReporter` — Show Background | Outlines of the glyph's background layer filled in pale blue (alpha 0.3), counters open; background components are not shown |
| `ShowCharacter.fontlabReporter` — Show Character | The glyph's first Unicode as 100 px text above the glyph; hidden below 20% zoom; no base-name lookup |
| `ExportStatus.fontlabReporter` — Show Export Status | Red cross over the body of a glyph that is set not to export |
| `GlobalGlyph.fontlabReporter` — Show Global Glyph | Contours of a helper glyph named `_global` behind every other glyph: closed paths orange outline with faint fill, open paths blue outline with faint fill; its components are not shown and it is not drawn on itself |
| `GlyphsInLabelColor.fontlabReporter` — Show Glyphs In Label Color | Glyph and component outlines filled in the mark colour, counters open |
| `ShowInterpolation.fontlabReporter` — Show Interpolation | For each other compatible master, the glyph blended halfway (`factor = 0.5`) node by node between the shown layer and that master, filled in dark magenta (alpha 0.25), counters open; components are not drawn (neither the shown layer's nor the masters'); no instances, anchors or recentering, and masters with the same coordinates are skipped |
| `KerningGroupReference.fontlabReporter` — Show Kerning Group Reference | Members of the glyph's left kerning class drawn on top of each other as small (0.2) teal silhouettes 150 units left of the glyph, and of its right class 150 units right of it, baseline at half x-height; opacity is 0.8 divided by the class size (floor 0.04), so crowded classes read denser. Left-to-right text only. Very large classes are truncated: at most 32 glyphs are requested, alternating left and right |
| `LabelColor.fontlabReporter` — Show Label Color | Bar in the glyph's mark colour under the descender (`placement` baseline or body), slanted by the italic angle; layer marks are not distinguished |
| `ShowRotated.fontlabReporter` — Show Rotated | Outline turned 180° about its bounds centre; components excluded |
| `Siblings.fontlabReporter` — Show Siblings | Look-alike Latin letters (c/e/o, b/p, d/q/u, h/l/n/r/a) filled in green behind the glyph, fainter in larger groups; Latin groups only |
| `ShowStems.fontlabReporter` — Show Stems | Rings and span widths along a scan line at half x-height; components excluded |
| `SmartPlumblines.fontlabReporter` — Smart Plumblines | Centre lines through each contour's and the selection's extents; components excluded |
| `SmoothNodeAngles.fontlabReporter` — Smooth Node Angles | Handle-angle mismatch and length ratio at smooth nodes |
| `SpeedPunk.fontlabReporter` — Speed Punk | Colour-ramped curvature comb; components excluded |
| `StemThickness.fontlabReporter` — Stem Thickness | Wherever the mouse is (no proximity limit), a line across the outline from the outline point nearest it, perpendicular to it, to the nearer crossing more than 1 unit away, labelled with its rounded length; nothing at a corner where the ray runs along the outline; own contours only, no guide command or modifier key |
| `TopsAndBottoms.fontlabReporter` — Tops and Bottoms | Rings and y labels at the highest and lowest on-curves |
| `TwoPointDistance.fontlabReporter` — Two Point Distance | Segment, length and angle for exactly two selected nodes |
| `Unitizer.fontlabReporter` — Unitizer | Vertical grid at UPM / 18 |
| `VerticalMetrics.fontlabReporter` — Vertical Metrics | Labelled ascender, descender, x-height, cap-height and baseline |

## Other Extensions

The same pack supplies `Extensions/filters/DeleteSmallPaths.fontlabFilter`,
`Extensions/general/ZoomToSelection.fontlabGeneral`,
`Extensions/palettes/StepAndRepeat.fontlabPalette` and
`Extensions/tools/SmartSelect.fontlabTool`, each with a `plugin.json` manifest.
These provide Delete Small Paths, Zoom to Selection, Step and Repeat and Smart
Select respectively. App owns their host operations; filters and palettes use
its guarded writer APIs. Native Undo/Redo and saved/reopened behavior remain
unverified for this installed tuple.


## New filters and tools

- [Round Outline to Grid](plugins/round-outline-to-grid.md) snaps own outline nodes to a grid.
- [Move Outlines](plugins/move-outlines.md) translates outlines without changing advance widths.
- [Scale Outlines](plugins/scale-outlines.md) scales outlines about a chosen pivot.
- [Slant Outlines](plugins/slant-outlines.md) applies geometric shear.
- [Measurement Ruler](plugins/measurement-ruler.md) measures a dragged span.
- [Node Probe](plugins/node-probe.md) inspects nearby outline nodes.
- [Contour Picker](plugins/contour-picker.md) selects a contour by a nearby node.

The four coordinate filters preserve components, anchors, advance widths and
native curve types. Tools do not change geometry. Their pages describe scope,
parameters and interaction limits; native verification remains open.

## Painting and acceptance limits

Center Lines, Vertical Metrics, Crosshair, Tops and Bottoms, RSB Line, Unitizer, Node Count, Smart Plumblines, Show Stems, Speed Punk, Show Rotated,
Show Label Color, Show Glyphs In Label Color, Show Character, Rekha Viewer,
Show Background, Color Toner, Show Global Glyph, Show Siblings, Show Kerning
Group Reference and Show Interpolation draw under the native glyph layer when native
canvas painters are available; the rest draw over it, and on older builds all
draw over the canvas.
The original seven reporters, native canvas drawing and all 18 pre-revision
reporters were checked in FontLab 9; Glyph Focus and the revised slant and unit
grid have offline coverage only. Node Count, All Angles, Smart Plumblines, Show
Stems, Speed Punk, Show Rotated, Blindfold, Show Label Color, Show Glyphs In
Label Color, Show Character, Rekha Viewer, Show Export Status, Show Background,
Color Toner, Show Global Glyph, Show Siblings, Show Kerning Group Reference,
Kern Indicator, Show Interpolation and Stem Thickness have offline test coverage
only.


## App reporter contract

Write a reporter by subclassing `fly.ap.plugins.Reporter` with a unique
`name`, a `title` and a pure `compute(snapshot)` that returns `Mark` objects
(`ring`, `line`, `polyline`, `polygon`, `text`) in glyph units; pixel sizes are
view pixels. Set `layer = "background"` to paint under the glyph layer.
An error raised by `compute` or `requested_glyphs` goes to the error sink
once per reporter and message until Plugmix is uninstalled. Every snapshot also carries `identity` (name, Unicodes, raw mark, mark RGB,
export flag) and `view.px_per_unit`; either is None when it cannot be read,
and the read error goes to the plugin error sink once. Mark RGB uses HSL lightness
0.65, so it differs slightly from FontLab's flag swatches (inferred, unverified
natively). Offline coverage only.
Opt-in class flags add costlier data: `needs_components` gives `components`
(base name, transform and decomposed base contours, nested up to 8 levels),
`needs_background` gives `background` (the mask's contours, `()` when empty,
None when there is none), and `needs_masters` gives `masters` (each master's
contours, anchors, advance and a `compatible` flag that compares contour
count, node count per contour and on/off-curve pattern with the shown layer,
ignoring components and open/closed state). Components and masters are cached
per glyph revision and shared by all reporters; components also re-check
their base glyphs. Master outlines may lag until the foreground glyph's
`lastModified` moves, which is unverified natively. The background is read on
every paint. An empty component layer means the master that owns the shown
layer. Metrics also come from that master. Zones and the italic angle need a
master switch to read, so when the shown layer belongs to another master the
zones are empty and the italic slant is the current master's.
Skipped components and failed reads go to the error sink once.
Offline coverage only.
`needs_kerning` gives `kerning_groups` (the classes used when the glyph is a
pair's first member, `left`, and second member, `right`, with their
members), read on every paint because a class edit may not move the glyph's
timestamp. Override `requested_glyphs(identity, kerning_groups=None)` to name up to 32 other
glyphs; `others` maps each one that exists to its own unselected contours
(components skipped), cached per requested glyph's revision. Both use the
master that owns the shown layer. `needs_neighbours` gives
`view.neighbours`: the previous and next glyph on the same line as
`(name, kerning)`, kerning in font units as displayed (0 when kerning
processing is off). Which glyph stores a pair's kerning is inferred,
unverified natively. Neighbours need the native canvas painter backend; with
EditorPainters, or when the view scale is unusable, they are None.
Offline coverage only.
`needs_mouse` gives `view.mouse`, the cursor in the glyph's own units
(`canvas.mousePosition()` mapped back through the glyph and text-block
transforms), or None when the map is not invertible. While any enabled
reporter asks for it, one event filter watches the active glyph window and
flushes (`updateScreenRect` plus `updateViewport`) at most once per 16 ms after
mouse moves, ending with a flush after the last move. The filter goes when the last such reporter is disabled, when the
active canvas changes or closes, and on `uninstall()`. Only the watched canvas
gets a mouse; with EditorPainters it is None. Whether moves reach the filter
under every tool is unverified natively.
Offline coverage only.
Bundles declare `id`, `name`, `kind`, `version`, `entry` and `min_app_version`
in `plugin.json`. The ID, display name and kind must match the entry class;
IDs are unique across kinds and the entry module must be inside the bundle.
Invalid manifests and imports are logged and skipped. Discovery is sorted and
retains class identity on repeated scans; restart FontLab to load changed source.
Third-party packages can still use the retained `fontlabapp.plugmix`
entry-point group.

Historical App native observations do not qualify activation or rendering of the current Extensions pack. Native palette/menu synchronization, toolbar placement, startup, teardown, drawing and writer history still require qualification on the exact installed App/Plugmix tuple. Issue 211 native probes remain separate.

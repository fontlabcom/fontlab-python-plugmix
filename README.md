<!-- this_file: README.md -->
# fontlab-python-plugmix

Native FontLab 9 reporter plugins: toggleable, read-only overlays in Glyph windows.
Plugmix uses MeVisLab PythonQt and native per-canvas painters when available,
with `fontlabapp.editor_painters.EditorPainters` for older builds.
It does not use PySide2 or Glyphs/Cocoa emulation. The repository also contains
FontLab menu scripts under `Scripts/`.

## Install

Install this package and its `fontlab-fontlabapp` runtime dependency in FontLab's
Python 3.11 environment. Copy the three lines from
[`initScript-snippet.py`](initScript-snippet.py) into your own FontLab `initScript.py`.
The hook calls `fontlab_plugmix.install()` once per FontLab session. Alternatively,
run `Scripts/Plugmix/Install Plugmix Menu.py` from FontLab's Script menu.
Neither file here edits a FontLab installation.

The View menu gains 19 checkable `Plugmix: Show …` actions. The selection is
remembered in `~/Library/Application Support/FontLab/FontLab 9/Data/fontlab-plugmix.json`.
`install(config_dir=...)` selects another directory, which is useful in tests.
`boot.uninstall()` removes the actions and overlays while retaining the selection.
Selections saved under the former `nodes_outside_paths` name restore as
`offcurve_outside_bounds`.

## Built-in reporters

| Reporter | Overlay |
| --- | --- |
| Duplicate Anchor Rings | Red/yellow rings for every unordered anchor pair less than one font unit apart; three coincident anchors produce three ring pairs. |
| Node Indexes | Full contour index beside every on- and off-curve node. |
| Selected Node Coordinates | Coordinates beside selected nodes. |
| Two Point Distance | A segment, length and angle for exactly two selected nodes. |
| Off-curve Handles Outside Bounds | Off-curve handles beyond the on-curve bounding rectangle. This uses bounds, unlike mekkablue's ShowNodesOutsidePaths path-containment test. |
| Center Lines | Advance/2, x-height/2 and cap-height/2 lines. |
| Vertical Metrics | Labelled ascender, descender, x-height, cap-height and baseline lines. |
| Angled Handles | Rings on off-curve handles outside horizontal, vertical and italic axes. |
| Crosshair | Thin, far-reaching guides through selected nodes; no mouse tracking. |
| Tops and Bottoms | Rings and y labels at tied highest and lowest on-curve positions. |
| Segment Length | Straight and flattened curve lengths where both on-curve ends are selected, or all when nothing is selected; runs of more than two off-curves are skipped. |
| Glyph Focus | Translucent shade outside the advance box between descender and ascender. |
| Emphasise Selected Handles | Accent lines and rings for handles next to selected nodes; native handles remain visible. |
| Anchor Cloud | Names and positions of the current glyph's anchors. |
| RSB Line | Advance boundary plus RSB and LSB labels from the native ink box. |
| Unitizer | Vertical grid behind the glyph at UPM / 18 increments; units per em is a class attribute. |
| Nodes Close to Zones | Rings on on-curves near selected-master zone edges or metric heights. |
| Imprecise Italic Angle | Straight segments within 2° of the master slant but not exactly on it. |
| Smooth Node Angles | Handle-angle mismatch and handle-length ratio at smooth nodes. |

Anchor Cloud currently shows local anchors only; a font-wide cloud needs a reliable font revision key
for bounded cache invalidation.

Duplicate rings use a 16-view-pixel diameter by default. The moved launcher
has a `HANDLE_SIZE` constant with the previous 5/8/12 choices. Stroke and label
sizes stay constant while zooming. Center Lines, Vertical Metrics, Crosshair,
Tops and Bottoms, RSB Line and Unitizer draw under the native glyph layer when
native canvas painters are available. The other reporters draw over it. On
older builds, all reporters draw over the canvas; plugmix logs that background
substitution once.

The native backend attaches to a Glyph window when it becomes active. Each
reporter reads the glyph separately on repaint; this is acceptable for the
reporter set, and remains a cost with many reporters enabled. Alignment zones
and the native ink box are read only for reporters that request them.

The native renderer maps a layer point through `info.transform` (glyph
position in its text block), then `block.transform` (text block placement),
then `canvas.mapToViewportF` (viewport pixels). This follows FontLab's text
block rendering and `EditorPainters`; the extra block transform matters when
the text block is positioned away from the canvas origin.

## Write a reporter

`compute()` receives immutable, plain Python data and returns marks in font
units. Importing this module does not need FontLab:

```python
from fontlab_plugmix import Mark, Reporter


class Origin(Reporter):
    name = "origin"
    title = "Origin"

    def compute(self, snapshot):
        return [Mark("ring", ((0, 0),), diameter_px=12)]
```

Publish the class through the `fontlab_plugmix.plugins` entry-point group. A
plugin class needs a unique `name` and a human-readable `title`. Mark kinds are
`ring`, `line`, `polyline`, `polygon` and `text`; polygons use an RGBA `fill`.
Coordinates are glyph units, while `stroke_px`, `text_px` and `diameter_px` are view pixels. Runtime calls and
exceptions are handled by the base class and selected backend. Set
`layer = "background"` to request painting under FontLab's glyph layer on
builds with native canvas painters.

## Test without FontLab

Run `./test.sh`. It finds the canonical sibling `fontlab-fontlabapp` checkout
through this worktree's git common directory. Set `PLUGMIX_FONTLABAPP_SOURCE`
to override that path. Run the full suite without selectors for the per-module
coverage gate; with pytest arguments, the gate is skipped because partial
coverage is expected.
The test suite uses fake Qt and FontLab objects and checks every production
module for at least 80% line coverage. The orchestrator checked the original
seven reporters and native canvas drawing in FontLab 9 before Task 7. The
orchestrator also checked all 18 pre-revision reporters natively; Glyph Focus
and the revised slant and unit grid have offline coverage only.

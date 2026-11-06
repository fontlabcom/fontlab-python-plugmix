---
this_file: README.md
---

# fontlab-python-plugmix

FontLab menu scripts for App's `fontlabapp.plugmix` framework, alongside the
retained `fontlab_plugmix` compatibility package. This recovery keeps both source
histories, tests and licences; it does not complete their consolidation.

## App-based menu scripts

`Scripts/Reports/` contains 39 reporter launchers. They use the framework already
provided by `fontlab-fontlabapp`; they do not import `fontlab_plugmix`.
`Scripts/Plugmix/Install Plugmix Menu.py` installs App's Plugmix menus. It does
not select an additional reporter; App restores saved plugin choices. Without
saved enabled reporter choices, reporters remain disabled. Run these files
through FontLab's Script menu. They are source scripts, not members of this
repository's compatibility wheel.

The 38 recovered reporters and two updated existing launchers retain their
pre-pull product bytes. The reporters cover geometry, anchors, metrics, node
selection, backgrounds, labels, interpolation and related reference overlays.
Duplicate Anchor Rings retains its editable `HANDLE_SIZE` choice of 5, 8 or 12.
Reporters do not edit font geometry; enabling one saves its name in Plugmix's
preference JSON. App owns discovery, registration, painters and teardown.

App's framework and the compatibility package below both use
`fontlab-plugmix.json` and can contribute Plugmix menus. Choose one runtime in a
FontLab session. Do not combine their startup installers. Preference migration
between the two implementations and native recovery acceptance are unqualified.
No script here installs packages or edits FontLab's startup file.

## Retained compatibility package

`src/fontlab_plugmix/` remains a separate installable package with 19 reporters,
an undoable Filter, a dockable Palette, a native Tool and a General menu command.
Its code, tests, dependencies, startup snippet and legal attribution are retained.

For this runtime, install the package and `fontlab-fontlabapp` in FontLab's
Python 3.11 environment. The optional `initScript-snippet.py` calls
`fontlab_plugmix.install()` once per session; it remains the compatibility startup
snippet, whereas the menu scripts above now target App. Neither file modifies an
installation. Use native MeVisLab PythonQt inside FontLab, without another Qt
binding. Native per-canvas painters are preferred, with App's `EditorPainters`
fallback on older builds.

The compatibility View menu has 19 `Plugmix: Show …` actions and Zoom to Selection.
Glyph has Delete Small Paths; Window has Step and Repeat Panel and Tool Smart
Select. Choices live in FontLab's Data directory as `fontlab-plugmix.json`.
`install(config_dir=...)` selects an owned directory for tests, and
`boot.uninstall()` removes owned actions, overlays and panels while retaining
saved choices. Unknown preference keys survive. The compatibility runtime maps
old `nodes_outside_paths` choices to `offcurve_outside_bounds`; this is not a
cross-runtime migration guarantee.

Filter, Tool and General choices default on until explicitly changed. Palettes
start hidden. Saved preferences retain `enabled`, `enabled_filters`,
`enabled_palettes`, `enabled_tools`, `enabled_general` and last-used `params`.

### Compatibility reporters

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


Anchor Cloud shows local anchors only. A font-wide cloud still needs reliable
revision-based invalidation. Stroke, text and ring sizes stay constant while
zooming. Center Lines, Vertical Metrics, Crosshair, Tops and Bottoms, RSB Line and
Unitizer request background painting; older builds substitute foreground painting
and log that choice once. Each reporter captures the glyph separately on repaint;
zones and native ink bounds are read only when requested.

Native drawing maps glyph points through the glyph text-block transform, the
block placement and `canvas.mapToViewportF`. Text-block placement matters away
from the canvas origin. Native compatibility observations are historical;
shortcut and keyboard cursor mapping changes still need an in-app recheck.

### Other compatibility plugins

- Delete Small Paths deletes closed contours below the threshold (default 400
  font units squared) using flattened path area or flattened bounds area. Open
  contours and exact-threshold values stay. It edits selected current-master
  glyphs through one geometry Undo step, skips automatic layers and unsafe
  shared/transformed outlines per glyph, and retains safe glyphs in the selection.
- Step and Repeat duplicates selected contours with count additional copies and
  repeated X/Y offsets through one geometry Undo step. It retains unselected
  contours, leaves copies unselected and refuses shared/transformed outlines,
  non-master display layers, stale contour counts and zero-offset repeats.
  Count zero or no selection is a no-op. Dock ownership survives temporary
  hiding; the Window toggle provides explicit close if close detection is absent.
- Smart Select selects whole contours touched by a dragged rectangle; Shift
  toggles them. It changes selection only and omits the source plugin's
  double-click containment and native move handling.
- Zoom to Selection fits the selected nodes with a margin. It omits delayed
  viewport adjustment and a shortcut. General font events use stable `fgId`
  identities and share the palette host's refresh timer.

### Write a compatibility reporter

`compute()` receives immutable Python data and returns marks in font units.
Native reads and writes belong in the host layer. Pure imports do not need FontLab:

```python
from fontlab_plugmix import Mark, Reporter


class Origin(Reporter):
    name = "origin"
    title = "Origin"

    def compute(self, snapshot):
        return [Mark("ring", ((0, 0),), diameter_px=12)]
```

Publish compatibility classes through `fontlab_plugmix.plugins` entry points.
App uses the separate `fontlabapp.plugmix` group. Names must be unique and titles
human-readable. Marks support ring, line, polyline, polygon and text; polygon
fill is RGBA, coordinates are font units, and stroke/text/diameter values are
view pixels. `layer = "background"` requests painting beneath native glyphs on
supported builds. Callbacks contain failures; reporter compute/paint must not
write font data.

## Development checks

Use arm64 Python 3.11 and an owned App source. The exact full recipe is:

```sh
UV_PYTHON_PREFERENCE=only-system PLUGMIX_FONTLABAPP_SOURCE="$PWD/../fontlab-fontlabapp" sh test.sh
```

The existing runner-layout test also requires that sibling App source directory.
The no-selector run executes all tests and checks every compatibility production
module for at least 80% line coverage. Arguments skip that checker. To measure
the complete recovered script surface with branches as well, run the full suite:

```sh
UV_PYTHON_PREFERENCE=only-system PLUGMIX_FONTLABAPP_SOURCE="$PWD/../fontlab-fontlabapp" sh test.sh --cov=Scripts --cov-branch --cov-report=json:coverage.json
```

Recovery tests use real App discovery/boot/registry with existing fake host owners
and temporary preferences. They execute all forty files, repeat installation,
toggle reporters through menus and check rollback on a preference-save failure.
These ordinary checks do not establish native rendering, owner installation,
installed artifact contents or publication. Keep the ordinary installed pre-push
gate active; its current selector alone does not measure Plugmix's `Scripts`.

## Remaining architecture and acceptance

Issue 210's future `fontlabapp.plugins` framework and `Extensions` bundles are
not implemented by this recovery. Specify the bundle/manifest contract first,
then qualify discovery, all four plugin kinds, duplicate registration, reload,
callbacks, ownership teardown and preservation-safe startup fixtures. Replace
reporter-per-script activation only after self-registration qualifies. Issue 211's
nine native probes and four minor fixes remain open. Issue 123 remains paused.
Further removal of the compatibility surface requires a full consumer,
distribution, source-recovery and licence audit. Website work is a later milestone.

## Licence and contribution workflow

Apache-2.0; retain `LICENSE` and all Apache-2.0/MIT attribution in `NOTICE`.
Read `AGENTS.md`, `PLAN.md` and `TODO.md` before changes. Qualified source,
ordinary artifacts, native behavior, canonical adoption and publication have
separate acceptance gates.

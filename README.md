---
this_file: README.md
---

# fontlab-python-plugmix

Reference Extensions pack for App's `fontlabapp.plugins` core: 50 plugins: 39 reporters,
five filters, four tools, one palette and one General plugin. Concrete plugins live
in `Extensions/`; the core owns discovery, preferences, callbacks and native UI.
The separate `fontlab_plugmix` compatibility package remains intact.

The pack ships as `fontlab-python-plugmix-extensions.zip`, built by
`python tools/build_pack.py [OUT_DIR]` (Extensions, `Scripts/Plugmix`, this README).
The wheel is the compatibility package only and contains no Extensions.

## Extensions and action scripts

Install `fontlab-fontlabapp>=1.2.31` and `fontlab-fly>=1.3.0` with its canonical providers in FontLab's Python
3.11 arm64 environment before using the bundles, action or startup snippet.
Their API imports use `fly.ap`; Fly preserves App module and class identity.
The pack installer declares and requests Fly >=1.3.0 alongside App; hand-copy
installation must prepare those packages first. The legacy compatibility library
keeps its App-only dependency.

See [Extensions/README.md](Extensions/README.md) for the bundle layout and manifest.
Open `install.vfpy` in FontLab (or copy the Extensions contents into the FontLab
user-data `Extensions/` folder by hand). The file is a short stub that hands the
work to
[fontlab-instamix](https://github.com/fontlabcom/fontlab-python-instamix); if
instamix is not installed yet, the stub installs it from PyPI first. Instamix
links the 50 bundles into `Extensions/<kind>/`, installs `Scripts/Plugmix` and
records the install under the extension id `com.fontlab.python-plugmix`.
Run App's `install.vfpy` first, and run it again after updating App: it records
the App version FontLab reports, all bundles need the plugin core first released in 1.2.9. Four of the five filters (Scale Outlines, Move Outlines, Round Outline To Grid, Slant Outlines) need the coordinate writer first released in 1.2.10; the canonical lowercase pack requires App 1.2.31 or newer. An older recorded version rejects bundles above its declared minimum. App's startup hook discovers the bundles. Each bundle is self-contained Python source
with a `plugin.json`; it needs no package install or reporter launcher.

Use the Reporters palette or View > Reporters to enable reporters. The only
remaining script, `Scripts/Plugmix/Show Reporters.py`, opens that palette. Reporters
do not edit font geometry; enabling one persists its stable ID. Duplicate Anchor
Rings retains its 5, 8 or 12 handle-size API, with the default of 8.

App and the retained compatibility runtime both use `fontlab-plugmix.json`.
Choose one runtime per FontLab session; do not combine their startup installers.
Cross-runtime preference migration remains unqualified. The installer adds no
packages and does not edit FontLab's startup file.

## Retained compatibility package

`src/fontlab_plugmix/` remains a separate installable package with 19 reporters,
an undoable Filter, a dockable Palette, a native Tool and a General menu command.
Its code, tests, dependencies and legal attribution are retained.

For this runtime, install the package and `fontlab-fontlabapp>=1.2.31` in FontLab's
Python 3.11 environment and explicitly call `fontlab_plugmix.install()` once per
session. The optional `initScript-snippet.py` now starts App through
`fly.ap.plugins.install()`; use it only with the App runtime. Use native MeVisLab
PythonQt inside FontLab, without another Qt binding. Native per-canvas painters
are preferred, with App's `EditorPainters` fallback on older builds.

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

### Write an App reporter through Fly

`compute()` receives immutable Python data and returns marks in font units.
Native reads and writes belong in the host layer. Pure imports do not need FontLab:

```python
from fly.ap.plugins import Mark, Reporter


class Origin(Reporter):
    name = "origin"
    title = "Origin"

    def compute(self, snapshot):
        return [Mark("ring", ((0, 0),), diameter_px=12)]
```

Publish these App classes through the `fontlabapp.plugmix` entry-point group,
or place them in Extensions bundles. Fly returns App's exact `Mark` and
`Reporter` classes. The retained compatibility runtime has a distinct
`fontlab_plugmix.Reporter` base and discovers its classes only through
`fontlab_plugmix.plugins`; the two bases and entry-point groups are not
interchangeable. Names must be unique and titles
human-readable. Marks support ring, line, polyline, polygon and text; polygon
fill is RGBA, coordinates are font units, and stroke/text/diameter values are
view pixels. `layer = "background"` requests painting beneath native glyphs on
supported builds. Callbacks contain failures; reporter compute/paint must not
write font data.

## Development checks

Use arm64 Python 3.11 and owned sibling App, Pens and Fly (>=1.3.0) sources. The exact full recipe is:

```sh
UV_PYTHON_PREFERENCE=only-system PLUGMIX_FONTLABAPP_SOURCE="$PWD/../fontlab-fontlabapp" sh test.sh
```

The runner-layout test requires the sibling App source. The runner explicitly
installs the selected Pens checkout and selects Fly's `src` on `PYTHONPATH`,
without installing Fly's full provider cohort. Set `PLUGMIX_PENS_SOURCE` or
`PLUGMIX_FLY_SOURCE` to select different owned checkouts. The no-selector run
executes the complete suite, retaining the compatibility package coverage gate
and requiring at least 80% line coverage and 80% branch coverage separately for
every Extensions and Scripts module and the startup snippet. Arguments skip the checker; after a selected
run, use the full suite before invoking `python3 tests/check_coverage.py coverage.json`.

Tests use real App bundle discovery, boot, registry and menus with fake host owners
and temporary preferences. Reporter behavior tests retain the original assertions
from App, with imports redirected to the bundle modules. Registration tests cover
repeated enable, menu disable, unknown preferences and failed-save rollback.
No offline result establishes native rendering, owner installation, published
artifacts or FontLab menu/toolbar insertion.

## Releasing the pack

Push the `v*` tag, then within 10 minutes create the release with notes (`gh release create <tag> --verify-tag --notes-file ...`). The Pack workflow's `release` job waits for the release and attaches `fontlab-python-plugmix-extensions.zip`; it never creates releases. If it timed out, create the release and re-run the job, then check `gh release view <tag> --json assets`.

## Remaining acceptance

Issue 210's source split is implemented in this paired candidate. Qualify native
Reporters palette/menu synchronization, toolbar and Tools > Tool, Window > Panels,
startup, teardown, drawing and writer history on the exact installed tuple.
Issue 211's existing native checks remain separate. Issue 123 remains paused.
Removing the retained compatibility package requires a consumer, distribution,
source-recovery and licence audit. The source/build website remains separately
maintained under `src_docs`; private Pages publication remains owner-held.

## Licence and contribution workflow

Apache-2.0; retain `LICENSE` and all Apache-2.0/MIT attribution in `NOTICE`.
Read `AGENTS.md`, `PLAN.md` and `TODO.md` before changes. Qualified source,
ordinary artifacts, native behavior, canonical adoption and publication have
separate acceptance gates.

## Issue 233 source/build-only documentation

The site uses fly-january 0.4.0 or later (remote theme assets) with the FontLab menu and footer.
Edit `src_docs/md` and `src_docs/mkdocs.yml`, then rebuild `docs/`.
Use Python 3.13 and uv 0.13.7 in a separate environment. Install the packages
in `src_docs/requirements.txt` with `--require-hashes`. Run `sh src_docs/build.sh` and
`python -m unittest discover -s tests_docs -v` with that environment on PATH.
Every main push builds exact source X, optionally makes a normal docs-only child
Y, and independently verifies immutable lineage, source identity, source epoch
and complete tracked/untracked generated parity. No private Pages permission,
configuration, deployment or automatic publication request is enabled.
Source/generated review, actual Actions, owner installation and native acceptance
remain separate. Do not change runtime dependencies, startup or recovery pins for
a site build.

## Practical outline workflows

- [Round Outline to Grid](src_docs/md/plugins/round-outline-to-grid.md) snaps own outline nodes to a grid.
- [Move Outlines](src_docs/md/plugins/move-outlines.md) translates outlines without changing advance widths.
- [Scale Outlines](src_docs/md/plugins/scale-outlines.md) scales outlines about a chosen pivot.
- [Slant Outlines](src_docs/md/plugins/slant-outlines.md) applies geometric shear.
- [Measurement Ruler](src_docs/md/plugins/measurement-ruler.md) measures a dragged span.
- [Node Probe](src_docs/md/plugins/node-probe.md) inspects nearby outline nodes.
- [Contour Picker](src_docs/md/plugins/contour-picker.md) selects a contour by a nearby node.

The four coordinate filters preserve components, anchors, advance widths and
native curve types. Tools do not change geometry. Their pages describe scope,
parameters and interaction limits; native verification remains open.

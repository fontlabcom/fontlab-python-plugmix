---
this_file: Extensions/README.md
---

# FontLab Extensions

This pack supplies 50 plugins: 39 reporters, five Filters, four Tools, one Palette
and one General plugin.
App's `fontlabapp.plugins` owns discovery, registration and native UI. These
bundles require `fontlab-fly>=1.3.0` and its providers in the host environment,
but need no `__init__.py`, bundle package install or individual launcher script.

Place this folder's contents in `<FontLab user data>/Extensions/`. App's startup
hook discovers them on launch. `Scripts/Plugmix/Show Reporters.py` is an optional
action that opens the Reporters palette. Enable reporters in that palette or
View > Reporters; choices persist in App's existing preference file. Do not run
the retained `fontlab_plugmix` compatibility installer in the same session.

A bundle has a kind folder, a suffix matching its kind, a manifest and Python:

```text
Extensions/reporters/NodeIndexes.fontlabreporter/
    plugin.json
    node_indexes.py
```

```json
{
  "id": "node_indexes",
  "name": "Node Indexes",
  "kind": "reporter",
  "version": "1.0.0",
  "entry": "node_indexes:NodeIndexes",
  "min_app_version": "1.2.9"
}
```

The manifest's `id`, `name` and `kind` must match the class's `name`, `title` and
`kind`. IDs are unique across kinds. Versions are three-part release versions;
`min_app_version` is the minimum App version. Entry modules must be inside the
bundle. Core API imports use `fly.ap.plugins` (Fly >=1.3.0); bundle-local helpers can use
relative imports. Bundle code runs as trusted Python code, with the same access
as a FontLab script. Invalid manifests/imports are logged and skipped.

| Kind | Folder | Suffix | Base class |
| --- | --- | --- | --- |
| reporter | reporters | .fontlabreporter | Reporter |
| filter | filters | .fontlabfilter | Filter |
| tool | tools | .fontlabtool | Tool |
| palette | palettes | .fontlabpalette | Palette |
| general | general | .fontlabgeneral | General |

Discovery is sorted and repeated discovery retains class identity. Restart
FontLab to load changed bundle source. `Reporter.compute()` takes immutable
snapshots and returns marks; keep native reads and writes in App's host layer.
The palette and filter examples use App's guarded writer APIs. Duplicate Anchor
Rings retains `set_handle_size(5|8|12)` and its default of 8.

Offline fake-host checks do not establish native painting, toolbar/menu
placement, PythonQt lifetime, Undo/Redo or saved/reopened behavior. Open native
checks remain in the repository TODO. Original notices are retained in NOTICE.

## Practical outline workflows

- [Round Outline to Grid](../src_docs/md/plugins/round-outline-to-grid.md) snaps own outline nodes to a grid.
- [Move Outlines](../src_docs/md/plugins/move-outlines.md) translates outlines without changing advance widths.
- [Scale Outlines](../src_docs/md/plugins/scale-outlines.md) scales outlines about a chosen pivot.
- [Slant Outlines](../src_docs/md/plugins/slant-outlines.md) applies geometric shear.
- [Measurement Ruler](../src_docs/md/plugins/measurement-ruler.md) measures a dragged span.
- [Node Probe](../src_docs/md/plugins/node-probe.md) inspects nearby outline nodes.
- [Contour Picker](../src_docs/md/plugins/contour-picker.md) selects a contour by a nearby node.

The four coordinate filters preserve components, anchors, advance widths and
native curve types. Tools do not change geometry. Their pages describe scope,
parameters and interaction limits; native verification remains open.

Canonical lowercase bundle suffixes require App 1.2.31 or newer. Legacy title-case suffixes remain accepted by App. Instamix 1.0.8 provides the qualified safeguard that refuses distinct modified or unowned legacy bundle conflicts. App 1.2.31 wheel/sdist are available from its GitHub release; PyPI publication remains pending an administrative trusted-publisher fix. Plugmix release/deployment and native/Windows migration remain separate qualification steps.

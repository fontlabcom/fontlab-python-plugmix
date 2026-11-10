---
this_file: Extensions/README.md
---

# FontLab Extensions

This pack supplies 39 reporters and one Filter, Tool, Palette and General plugin.
App's `fontlabapp.plugins` owns discovery, registration and native UI. These
bundles need no `__init__.py`, package install or individual launcher script.

Place this folder's contents in `<FontLab user data>/Extensions/`. App's startup
hook discovers them on launch. `Scripts/Plugmix/Show Reporters.py` is an optional
action that opens the Reporters palette. Enable reporters in that palette or
View > Reporters; choices persist in App's existing preference file. Do not run
the retained `fontlab_plugmix` compatibility installer in the same session.

A bundle has a kind folder, a suffix matching its kind, a manifest and Python:

```text
Extensions/reporters/NodeIndexes.fontlabReporter/
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
  "min_app_version": "1.0.0"
}
```

The manifest's `id`, `name` and `kind` must match the class's `name`, `title` and
`kind`. IDs are unique across kinds. Versions are three-part release versions;
`min_app_version` is the minimum App version. Entry modules must be inside the
bundle. Core imports use `fontlabapp.plugins`; bundle-local helpers can use
relative imports. Bundle code runs as trusted Python code, with the same access
as a FontLab script. Invalid manifests/imports are logged and skipped.

| Kind | Folder | Suffix | Base class |
| --- | --- | --- | --- |
| reporter | reporters | .fontlabReporter | Reporter |
| filter | filters | .fontlabFilter | Filter |
| tool | tools | .fontlabTool | Tool |
| palette | palettes | .fontlabPalette | Palette |
| general | general | .fontlabGeneral | General |

Discovery is sorted and repeated discovery retains class identity. Restart
FontLab to load changed bundle source. `Reporter.compute()` takes immutable
snapshots and returns marks; keep native reads and writes in App's host layer.
The palette and filter examples use App's guarded writer APIs. Duplicate Anchor
Rings retains `set_handle_size(5|8|12)` and its default of 8.

Offline fake-host checks do not establish native painting, toolbar/menu
placement, PythonQt lifetime, Undo/Redo or saved/reopened behavior. Open native
checks remain in the repository TODO. Original notices are retained in NOTICE.

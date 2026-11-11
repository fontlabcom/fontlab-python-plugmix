---
this_file: src_docs/md/installation.md
---

# Installation and startup

## App Extensions

Install the reviewed `fontlab-fontlabapp` package in FontLab's Python 3.11 arm64
environment using App's `install.vfpy`. App's installer adds its marked startup
block to `initScript.py`, preserving existing contents; the block calls
`fontlabapp.plugins.install()` at launch. The App core discovers the user-data
folder from `fontlab.flPreferences().dataPathDefault` and scans its `Extensions/`
folder. Use FontLab's reported folder rather than assuming a platform path.

Copy the contents of this repository's `Extensions/` into that folder, preserving
`reporters`, `filters`, `general`, `palettes` and `tools` and their bundle folders.
The pack contains 50 bundles: 39 reporters, five filters, four tools, one palette
and one General plugin. Each bundle
includes `plugin.json` and Python source; the bundles need no package install.
Restart FontLab for startup discovery and after changing bundle source.

Open the Reporters palette from Window > Panels, or run the optional
`Scripts/Plugmix/Show Reporters.py` action. Enable reporters in that palette or
View > Reporters; disable them there too. Choices persist by stable ID, and
saved choices are restored at startup. Without saved enabled reporter choices,
reporters remain disabled. The source places tools in the toolbar and Tools >
Tool, and palettes in Window > Panels. Native placement and synchronization
still require verification on the exact installed tuple.

The Show Reporters action calls `fontlabapp.plugins.show_reporters()`; it does
not install packages or change the startup file. The retired per-reporter
launchers and Install Plugmix Menu script are no longer used. Duplicate Anchor
Rings retains `set_handle_size(5|8|12)`, with a default of 8. Reporters do not
edit font geometry. Startup, teardown, drawing and writer history remain native
acceptance checks; these instructions do not claim those checks have passed.

## Coordinate-filter App requirement

The four coordinate filters require the coordinated App coordinate-writer
change. Older App versions with the deletion-only Filter writer cannot apply
them. No released App version has yet been assigned to this requirement; use
the reviewed paired App/Plugmix source tuple, not the manifest minimum alone.

A partial native write follows App's existing `PartialWriteError` recovery:
use **Edit > Undo** as directed by the error. It does not automatically roll
back completed writes. Native Undo/Redo recovery remains unverified.

## Compatibility package

From an authorized checkout, install the compatibility package and its App dependency in the owner-managed FontLab Python 3.11 arm64 environment. In an isolated ordinary development environment, the package can be installed with `uv pip install .` once the required App distribution is available. Use native MeVisLab PythonQt inside FontLab, without another Qt binding.

`initScript-snippet.py` is an optional compatibility startup snippet: it calls `fontlab_plugmix.install()` once per session. It does not target App's `fontlabapp.plugins` runtime and does not modify an installation. No documentation build installs into FontLab's user folder.

## Runtime and preference ownership

Choose one runtime per session. Do not combine their startup installers or assume a preference migration guarantee. The shared filename is `fontlab-plugmix.json` in FontLab's Data directory. `install(config_dir=...)` selects an owned test directory. Runtime uninstall removes its owned actions, overlays and panels while retaining saved choices. Unknown preference keys survive; failed preference saves roll back activation. Preserve failed-teardown recovery rather than treating a partial teardown as success.

Filter, Tool and General choices default on until explicitly changed; palettes start hidden. Saved choices retain `enabled`, `enabled_filters`, `enabled_palettes`, `enabled_tools`, `enabled_general` and last-used `params`. The compatibility rename from `nodes_outside_paths` to `offcurve_outside_bounds` is an internal migration only.

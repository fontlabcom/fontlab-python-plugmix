---
this_file: src_docs/md/installation.md
---

# Installation and startup

## App menu scripts

Install the reviewed `fontlab-fontlabapp` package through the owner-managed FontLab Python 3.11 arm64 environment. Run `Scripts/Plugmix/Install Plugmix Menu.py` from FontLab's Script menu, then choose a reporter or run one of the 39 `Scripts/Reports/` launchers. The menu installer restores saved choices and does not select another reporter. Without saved enabled reporter choices, reporters remain disabled.

Each reporter launcher installs App's menu runtime, enables its named reporter and persists that choice. Use its View > Plugmix: Show action to turn it off. No launcher edits font geometry, installs a Python package or changes the startup file. These source scripts are not included in the compatibility wheel. Duplicate Anchor Rings preserves the source's editable `HANDLE_SIZE` choices 5, 8 or 12.

## Compatibility package

From an authorized checkout, install the compatibility package and its App dependency in the owner-managed FontLab Python 3.11 arm64 environment. In an isolated ordinary development environment, the package can be installed with `uv pip install .` once the required App distribution is available. Use native MeVisLab PythonQt inside FontLab, without another Qt binding.

`initScript-snippet.py` is an optional compatibility startup snippet: it calls `fontlab_plugmix.install()` once per session. It does not target App's `fontlabapp.plugmix` runtime and does not modify an installation. No documentation build installs into FontLab's user folder.

## Runtime and preference ownership

Choose one runtime per session. Do not combine their startup installers or assume a preference migration guarantee. The shared filename is `fontlab-plugmix.json` in FontLab's Data directory. `install(config_dir=...)` selects an owned test directory. Runtime uninstall removes its owned actions, overlays and panels while retaining saved choices. Unknown preference keys survive; failed preference saves roll back activation. Preserve failed-teardown recovery rather than treating a partial teardown as success.

Filter, Tool and General choices default on until explicitly changed; palettes start hidden. Saved choices retain `enabled`, `enabled_filters`, `enabled_palettes`, `enabled_tools`, `enabled_general` and last-used `params`. The compatibility rename from `nodes_outside_paths` to `offcurve_outside_bounds` is an internal migration only.

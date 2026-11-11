---
this_file: src_docs/md/consumer-audit.md
---

# Consumer audit

This page records who uses the compatibility package, its entry-point groups and the deprecated shim, as found in the maintained repositories on `origin/main` (2026-11-11). It is evidence for a removal decision, not the decision. Generated `docs/`, CHANGELOG, WORK, PLAN, TODO and lock-file noise are excluded. Import forms inside this package were counted per file, not classified one by one.

## Packages, groups and hooks

| Item | Value | Evidence |
|---|---|---|
| Core namespace | `fontlabapp.plugins` | `fontlab-fontlabapp/src/fontlabapp/plugins/` |
| Deprecated shim | `fontlabapp.plugmix` (DeprecationWarning, meta-path alias to `fontlabapp.plugins.*`) | `fontlab-fontlabapp/src/fontlabapp/plugmix/__init__.py:11` |
| App entry-point group | `fontlabapp.plugmix` | `plugins/registry.py:17`, selected at `:69` |
| Legacy entry-point group | `fontlab_plugmix.plugins` | `src/fontlab_plugmix/registry.py:18`, selected at `:86` |
| Preferences | `~/Library/Application Support/FontLab/FontLab 9/Data/fontlab-plugmix.json` (name kept) | `plugins/registry.py:20` |
| Startup, legacy | `from fontlab_plugmix import install; install()` | `initScript-snippet.py` |
| Startup, App docs | `from fontlabapp.plugmix import install; install()` (documents the shim path) | `fontlab-fontlabapp/src_docs/md/plugmix.md:19` |
| Distribution, legacy | `fontlab-python-plugmix`: wheel package `src/fontlab_plugmix`, depends on `fontlab-fontlabapp`; ships `Extensions/{filters,general,palettes,reporters,tools}` and Scripts | `pyproject.toml` |
| Distribution, App | `fontlab-fontlabapp` contains `fontlabapp.plugins` and the shim | `fontlab-fontlabapp/src/fontlabapp` |
| Licence | Apache-2.0 in both; `NOTICE:61` records the move of `fontlabapp/plugmix` out of this package | `LICENSE`, `NOTICE` |
| Guards | In-App consumers are guarded by `tests/test_plugmix_shim_consumers.py` in `fontlab-fontlabapp` | |

## Consumers outside this package

| Repository and file | Form | Kind |
|---|---|---|
| `fontlab-aidus-agentus/README.md:176`, `src_docs/md/dock-and-acp.md:90`, `PLAN.md:29` | text naming `fontlab-python-plugmix` and `fontlabapp.plugmix` | documentation |
| `fontlab-aidus-agentus/src/fontlab_aidus_agentus/core/prompts/fontlab_api.md:98` | names `fontlab_plugmix` for reporter overlays | AI prompt text; affects generated code |
| `fontlab-aidus-agentus/tests/test_residue_port.py:23` | string `"fontlab_plugmix.plugins"` | test |
| `fontlab-aidus-agentus/run_in_fontlab/check_aidus_in_fontlab.vfpy:20` | module list includes `"fontlab_plugmix"` | native check script |
| `fontlab-python-docs/src_docs/md/packages/plugmix.md`, `scripts/pages_inputs.py:55` | documentation page and its build input | documentation |
| `fontlab-fontlabapp` README, `src_docs/md/plugmix.md`, `guides/runtime-reference.md`, `guides/api-map.md`, `Scripts/Utilities/Plugmix Demo.py:28`, `AGENTS.md:93` | `fontlabapp.plugmix` APIs and the preferences file name | documentation and script text |
| `fontlab-python-scriptmix` README and pre-integration guide | text mentions | documentation |
| Glyport, Fontport, Examples, Echopy, Fly, GrabLab, Remopy, pythonqtside, Pens, extend-fontlab | none found outside generated docs, changelog, plan, todo and lock files | none |

## Inside this package

The bundled `Extensions` already import the canonical `fontlabapp.plugins` (50 tracked Python files: 5 filters, 1 general, 1 palette, 39 reporters, 4 tools; counted with `git grep -l "fontlabapp.plugins" -- 'Extensions/*.py'` and grouped by directory), as do `Scripts/Plugmix/Show Reporters.py` and 17 tests. The legacy `src/fontlab_plugmix` tree (51 tracked Python files, counted with `git ls-files 'src/fontlab_plugmix/*.py'`) keeps its own parallel modules and the old entry-point group; 11 tests import it. No file here imports the deprecated shim.

## Lock-file membership

No maintained lock file pins `fontlab-python-plugmix`. Fontport and Glyport pin `fontlab-fontlabapp` as an editable sibling. Seven repositories have no lock file; six others lock neither package.

## Not knowable from the workspace

- Third-party packages that publish either entry-point group (`fontlabapp.plugmix`, `fontlab_plugmix.plugins`).
- Installed copies that still call the old startup snippet.

## Removal gates stay open

Removing the compatibility package or the `fontlabapp.plugmix` shim stays blocked until an outside-consumer search or a deprecation period covers the two items above.

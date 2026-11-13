---
this_file: src_docs/md/development-and-limits.md
---

# Development and limits


Use arm64 Python 3.11 and owned sibling App, Pens and Fly (>=1.3.0) sources.
The runner explicitly prepares Pens and selects Fly's `src` on `PYTHONPATH`.
Set `PLUGMIX_PENS_SOURCE` or `PLUGMIX_FLY_SOURCE` to select other owned
checkouts; the isolated-child regression selects that exact source and verifies
its origin without assuming Fly is installed. The exact full recipe is:

```sh
UV_PYTHON_PREFERENCE=only-system PLUGMIX_FONTLABAPP_SOURCE="$PWD/../fontlab-fontlabapp" sh test.sh
```

The runner-layout test requires the sibling App source directory. The
no-selector run executes the complete suite and the compatibility package's
coverage gate, plus at least 80% line coverage and 80% branch coverage separately
for every Extensions and Scripts module and the startup snippet. Arguments skip the checker; after a
selected run, use the full suite before invoking
`python3 tests/check_coverage.py coverage.json`.

Tests exercise real App bundle discovery, boot, registry and menus with fake host
owners and temporary preferences. Reporter behavior assertions are retained with
imports redirected to bundle modules. Registration tests cover repeated enable,
menu disable, unknown preferences and failed-save rollback. These offline checks
do not establish native rendering, owner installation, installed artifact
contents or publication. Keep the ordinary installed pre-push gate active.

## Remaining acceptance

Issue 210's source split is implemented: App's `fontlabapp.plugins` core owns
scaffolding, discovery, registration and lifecycle; Plugmix supplies 50 manifest
bundles under `Extensions/` and one Show Reporters action. The deprecated
`fontlabapp.plugmix` import shim and the separate `fontlab_plugmix` compatibility
package remain distinct.

Qualify native Reporters palette/View > Reporters synchronization, toolbar and
Tools > Tool, Window > Panels, startup, teardown, drawing and writer history on
the exact installed tuple. Issue 211's nine native probes and four minor fixes
remain separate. Issue 123 remains paused. Removing the compatibility package
still requires a full consumer, distribution, source-recovery and licence audit.

## Website checks

Use a separate Python 3.13 environment and uv 0.13.7, installing the exact hash-locked `src_docs/requirements.txt`. Run `sh src_docs/build.sh` and `python -m unittest discover -s tests_docs -v`. These checks build complete catalogue pages without importing App or Plugmix. The build captures the source commit's timestamp once and both main-triggered jobs use it. A generated output child must be a direct docs-only child of the source SHA with identical non-doc source. The read-only second job checks the actual immutable output and requires full tracked and untracked parity.

Earlier recovery test results remain historical source qualification and do not qualify the current Extensions tuple. No product code, fixtures, startup script, recovery hash pin or licence is changed by this site. Publication, owner installation and native FontLab rendering remain separate. Private Pages configuration, permissions and requests stay owner-held.

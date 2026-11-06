---
this_file: src_docs/md/development-and-limits.md
---

# Development and limits


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


## Website checks

Use a separate Python 3.13 environment and uv 0.13.7, installing the exact hash-locked `src_docs/requirements.txt`. Run `sh src_docs/build.sh` and `python -m unittest discover -s tests_docs -v`. These checks build complete catalogue pages without importing App or Plugmix. The build captures the source commit's timestamp once and both main-triggered jobs use it. A generated output child must be a direct docs-only child of the source SHA with identical non-doc source. The read-only second job checks the actual immutable output and requires full tracked and untracked parity.

The existing 166-test recovery result and retained 68 compatibility/recovery source contracts remain separate historical source qualification. No product code, fixtures, startup script, recovery hash pin or licence is changed by this site. Publication, owner installation and native FontLab rendering remain separate. Private Pages configuration, permissions and requests stay owner-held.

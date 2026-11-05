---
this_file: AGENTS.md
---

# Plugmix: agent guide

This remote package provides 19 reporters, a Filter, a Palette, a Tool and a
General plugin. Keep geometry and metrics capture in `snapshot.py`, painter
access in `backend.py`, and startup imports in `boot.py`.
Keep reporter `compute()` pure. Reporter compute and paint must not write font
data. Filters and Palettes can make the documented undoable font edits through
the host writers. Keep native reads and writes out of pure compute methods.
Contain exceptions inside paint and Qt signal callbacks.
Use App's `EditorPainters` and `OwnedMenus` for ownership and teardown.
Preserve the preference JSON, unknown keys and failed-teardown recovery.
Use native PythonQt in FontLab. Do not import another Qt binding into the host.
Preserve Apache-2.0 terms in LICENSE and all attribution in NOTICE.

## Development checks

This source base is `dddadcd9bc8cee21d5f7b8fe60027495e13fd41a`.
`src/fontlab_plugmix/` contains the package. `tests/`, `test.sh` and
`tests/check_coverage.py` provide its own offline suite and coverage check.
Use an arm64 Python 3.11 process and the owned sibling App source:

```sh
PLUGMIX_FONTLABAPP_SOURCE="$PWD/../fontlab-fontlabapp" sh test.sh
```

Run this command without selectors. The wrapper installs this local package and
the selected App source in its uv test environment. With no arguments, it also
runs `python3 tests/check_coverage.py coverage.json`. Selectors skip that checker.
Keep the ordinary installed pre-push gate as a separate requirement.
The recorded installed-hook baseline passed 125 tests with zero changed modules.
That baseline does not prove the full repository checker passed.
The full recipe and compatibility with the chosen current App tuple still need
verification. Offline fake-host tests do not establish native behavior.

## Review and delivery

Read README, PLAN, TODO, WORK and CHANGELOG before work. Use an isolated checkout.
Preserve the owner's branches, index, edits, archives and licences.
Choose one small complete MVP. Name its callers, tests, fixtures, configuration
and exports. Use graph context and impact before source symbol changes.
Confirm stale, empty or unknown graph results against the actual source.

Run the exact repository checks. Keep the unchanged 80% coverage gate for each
complete changed production module where the milestone gate applies.
Documentation checks cover headers, fences, links, privacy and the exact diff.
Keep ordinary installed hooks active. Do not bypass a failed gate.
Obtain independent specification and quality review before a milestone commit.
Stage only the approved paths after checking their preimage hashes.
Run graph change analysis before committing.

Issue 230 authorizes reviewed, passing documentation milestone commits and pushes.
Verify the actual remote branch SHA after a push. Refresh remote refs before
integration. Reconcile concurrent work and consumers before primary-branch
integration. Run the applicable combined-source and CI checks.
Do not infer publication, installation or native acceptance from a branch push.
Do not create release tags, dispatch release workflows or publish packages for
this documentation milestone.

Before obsolete branch or file removal, verify recovery and integration.
Check fresh owner/worktree attachments and unique work. Preserve sealed evidence
and protected tags. Do not force-push or rewrite history by implication.
Keep PLAN future-facing and TODO flat with unchecked open tasks.
Record only verified scope in CHANGELOG and current checks in WORK.

Issue 123 remains paused. Issue 207 candidates require reconciliation with newer
source. Keep source tests, complete archives, installed origins/RECORD, native
workflows, canonical promotion, remote delivery and publication separate.
Do not read or mutate owner fonts, preferences, Output or global update queues.
Do not install or uninstall in the owner's FontLab user folder.
Preserve private configuration and source boundaries. Native work requires a
separate safe owned-fixture session under the workspace D30 checks and fences.
The D31 zone/master lane remains reserved. D29 generation/publication gates apply.

Qualified integration targets `main`.

## Future plugin architecture

Issue 210 requires a specified bundle name and manifest contract before code.
App must own scaffolding, discovery, registration and lifecycle under
`fontlabapp.plugins`. Plugmix must own concrete bundles under
`Extensions/reporters`, `filters`, `tools` and `palettes`.
Discover the actual Extensions root. Test all four kinds, duplicate registration,
unload/reload, callback failures and owned teardown.

Register a Reporters palette and View > Reporters. Put tools in the toolbar and
Tools > Tool. Put palettes in Window > Panels. `install.vfpy` must prepare a
minimal startup hook while preserving existing `initScript.py` contents and
ownership. Prove this with owned fixtures before any owner installation.
Replace reporter-per-script activation only after discovery and self-registration
pass. Retain genuine action scripts. Four additional action scripts are optional.

Issue 211's nine native probes and four minor fixes remain follow-up work.
The README's dated native observations do not close those integrated checks.
Canonical migration to App `fontlabapp.plugmix` is separate work. Reconcile its
ten later product commits with this remote package and all consumers before
selecting a source tuple. Do not import that migration through a docs commit.

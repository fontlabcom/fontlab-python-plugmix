---
this_file: AGENTS.md
---

# Plugmix: agent guide

## Owner priority: functional progress first (2026-11-15)

Future agents must make large, swift advances in working functionality. Prioritize visible user problems and useful, coherent feature increments. This instruction sets the work order and supersedes older requirements to complete exhaustive testing or build test infrastructure before ordinary implementation.

Keep packages coherent and compatible. Check shared APIs, imports and lazy aliases, data formats, dependency direction, object ownership and lifetime, installers, launchers and examples. Update affected providers and consumers together; preserve existing supported behavior and avoid dependency cycles.

During implementation, use the smallest meaningful smoke checks and focused regression tests for the changed behavior and affected package boundaries. Detailed testing, exhaustive coverage, broad performance studies and full acceptance matrices can follow in a later testing pass. Do not let test harnesses, sandbox/supervisor design, repeated unchanged suites, evidence machinery or review paperwork become the main project. Build such infrastructure only when a concrete functional defect or necessary safety constraint requires it.

Record deferred checks and known limits plainly. Do not call untested native, installed or published behavior verified. Keep existing mandatory delivery hooks, preservation rules, licence/privacy obligations, repository exclusions and explicit native/publication holds intact. When one action is held, continue other authorized functional work instead of expanding unrelated infrastructure.

Choose the next substantial useful feature or shared fix and carry its affected providers and consumers together. Timebox supporting investigation; once focused checks establish a usable increment, continue functionality work. Queue detailed testing for a later pass with its concrete remaining checks instead of letting test infrastructure displace product delivery.

## Current-source release qualification — 2026-11-14

The older no-release rule applies to its historical source-recovery milestone.
Current workspace D43 authorizes a qualified new release through normal hooks,
review, main/tag CI and downloaded-artifact checks. Functional priority changes
the work order, not mandatory delivery gates or native fences. Keep compatibility
wheel/sdist, curated Extensions ZIP and startup/helper acceptance separate.

## Live font testing in FontLab (owner instruction, 2026-11-10)

Test, verify and edit in the font that is open in FontLab 9. Don't hold back
because the owner might be working on it. Just work in it. If no font is open,
open a VFJ from `~/Desktop` first (File > Open, or `fontlab.flPackage(path)`
and `flWorkspace.instance().addPackage`). Those VFJs are for agents. Add glyphs,
kerning pairs, elements, contours, masters or anything else the test needs,
and save the files when that helps. This replaces older rules that required an
empty FontLab session or forbade editing open fonts. `fl-native.sh --mutating`
now runs with fonts open (`FL_REQUIRE_EMPTY=1` restores the old check). The
serialized lock still applies: one native run at a time. Don't quit or restart
FontLab, and don't close fonts from Python, because that has crashed the host.

The recovered `Scripts/` entry points use App `fontlabapp.plugmix`: 39 reporter
launchers and one menu installer. The retained `fontlab_plugmix` compatibility
package separately provides 19 reporters, a Filter, a Palette, a Tool and a
General plugin. Keep these runtime and entry-point groups distinct; both use
the Plugmix preference filename and must not be installed together in one session. Keep geometry and metrics capture in `snapshot.py`, painter
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

The retained compatibility package descends from
`dddadcd9bc8cee21d5f7b8fe60027495e13fd41a`; recovered scripts use App separately.
`src/fontlab_plugmix/` contains the package. `tests/`, `test.sh` and
`tests/check_coverage.py` provide its own offline suite and coverage check.
Use an arm64 Python 3.11 process and the owned sibling App source:

```sh
PLUGMIX_FONTLABAPP_SOURCE="$PWD/../fontlab-fontlabapp" sh test.sh
```

The runner-layout test also requires a sibling App source directory. Set
`UV_PYTHON_PREFERENCE=only-system` and verify the actual interpreter is arm64.
Run this command without selectors. The wrapper installs this local package and
the selected App source in its uv test environment. With no arguments, it also
runs `python3 tests/check_coverage.py coverage.json`. Selectors skip that checker.
Keep the ordinary installed pre-push gate as a separate requirement.
The recorded installed-hook baseline passed 125 tests with zero changed modules.
That baseline does not prove the full repository checker passed.
The later full no-selector `sh test.sh` run on 2026-11-05 at 21:46:13 UTC
passed: exit 0, 125 tests and the full per-module checker. It used this
source and owned App `fb6a93776772b996b25604f88711feb300b90109`.
The observed 96% overall line coverage supplements the unchanged 80%
combined-module policy. Requalify after a source or App tuple change.
Offline fake-host tests do not establish native or installed-artifact acceptance.

## Review and delivery

Read README, PLAN, TODO, WORK and CHANGELOG before work. Use an isolated checkout.
Preserve the owner's branches, index, edits, archives and licences.
Choose one small complete MVP. Name its callers, tests, fixtures, configuration
and exports. Use graph context and impact before source symbol changes.
Confirm stale, empty or unknown graph results against the actual source.

Run the exact repository checks. Keep the unchanged 80% coverage gate for each
complete changed production module where the milestone gate applies.
Measure all forty recovered `Scripts` modules separately with branch coverage
and the unchanged 80% combined gate; the old package/hook selectors cover only
`src`. Run all tests with `--cov=Scripts --cov-branch` after the full no-selector
recipe. Keep actual App registration/persistence/menu and rollback tests; source
checksums establish provenance, not functional coverage.
Documentation checks cover headers, fences, links, privacy and the exact diff.
Keep ordinary installed hooks active. Do not bypass a failed gate.
Obtain independent specification and quality review before a milestone commit.
Stage only the approved paths after checking their preimage hashes.
Run graph change analysis before committing.

Issues 230/233 authorize the scoped reviewed recovery and documentation
milestones, with passing checks before commits and pushes.
Verify the actual remote branch SHA after a push. Refresh remote refs before
integration. Reconcile concurrent work and consumers before primary-branch
integration. Run the applicable combined-source and CI checks.
Do not infer publication, installation or native acceptance from a branch push.
Do not create release tags, dispatch release workflows or publish packages for
this source-recovery milestone.

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
The recovered App-based launchers retain their original product bytes. The
compatibility package is deliberately retained; removing it requires a complete
consumer/distribution/licence audit and qualified recovery. This additive
recovery does not finish consolidation or implement the future framework.

## Issue 233 source/build-only documentation

The site uses fly-january 0.1.1 with the FontLab menu and footer.
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

## Integration rounds

After each important round, independently verify the result, refresh the actual upstream main (or existing default branch), and reconcile concurrent team work in an isolated successor. Integrate qualified changes upstream through normal gates without force-pushing. Move only verified solved TODO items to cumulative CHANGELOG, update PLAN for remaining work, and continue the authorized backlog. Existing preservation rules, exclusions, pauses, native/install restrictions, private P/L holds and capability gates remain in force.

## Agent workflow (Issue 250, 2026-11-10)

- Plan with `superpowers:subagent-driven-development`: one fresh implementer per task, a separate read-only reviewer, then the controller runs the gates and commits.
- Send bulk, well-specified work to Codex via the `codex-delegate` skill (`node ~/.agents/skills/codex-delegate/scripts/relay.mjs --brief BRIEF --cd WORKTREE`, in the background). Use `claude-delegate` or `cursor-delegate` for second opinions or independent lanes. Delegates never commit, push or tag.
- Work in a fresh worktree of `origin/main` on the workspace data volume; never pull, switch or reset the owner checkout. Merge `origin/main` again before pushing, keep both sides' CHANGELOG/PLAN/TODO entries, rerun the full suite, lint and graph change analysis, push through the pre-push hook where one is installed (never force), verify the remote SHA and the CI run where a workflow is configured. Held private Pages operations (workspace D41) stay held.
- Release: tag the next semver above the latest tag and publish a GitHub release. Install released, gated packages into `~/Library/Application Support/FontLab/FontLab 9/` and test live in FontLab 9. This owner route (Issue 250) supersedes, for released packages only, every older line in this guide that forbids installing into the FontLab user folder or its site-packages, owner-managed editable installs, or starting FontLab for a live test (the owner's canonical editable checkouts themselves stay owner-managed): record the previous installed distribution first so it can be restored, and never touch FontLab preferences (owner fonts and documents: see live font editing below); native work goes through the workspace `verification/issue-104/fl-native.sh` gate.
- Documents: CHANGELOG holds verified completed work; TODO only open or to-verify items; PLAN the major remaining changes; WORK.md the current round only (older WORK bytes are archived on the owner's workspace data volume, not public).
- Native defects: issues at github.com/fontlab/fl; fixes as pull requests to fontlab/Proteus, fontlab/FontGate or fontlab/pyfontgate. Never commit to the local C++ snapshot.
- Older "work directly" or "no delegation" lines in this guide are superseded by this section (Issue 250).
- Live font editing (owner, 2026-11-10; workspace D44): test, verify and edit the font open in FontLab 9, and do not stop because the owner might be working in it. Open a VFJ from `~/Desktop` first (those files are for agents), then add glyphs, kerning pairs, elements, contours, masters or whatever the test needs, and save them freely. This supersedes, for live testing, every older line here that forbids mutating owner fonts or documents or requires owned fixtures only. FontLab preferences, Output folders and global update queues stay untouched. Keep the serialized host lock (`fl-native.sh`, one native run at a time; `--mutating` now allows open fonts); do not quit or restart FontLab and do not close fonts from Python, which has crashed the host.

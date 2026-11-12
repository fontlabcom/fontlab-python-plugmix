---
this_file: CHANGELOG.md
---

## 2026-11-12 — install.vfpy installs the 50 bundles (Issue 254)

- Plugmix Demo showed no plugins because nothing put the `Extensions/<kind>/*.fontlab*` bundles where FontLab looks. `install.vfpy` (byte-identical to App's) with the new `[tool.fontlab-install]` table (`extensions = "Extensions"`, `packages = []`) links all 50 (39 reporters, 5 filters, 4 tools, 1 palette, 1 general) and copies `Scripts/Plugmix`; a non-Git folder installs a copy under `Extensions/<id>/bundles/<kind>/`.
- Install order: run App's `install.vfpy` before this one and again after updating App; it refreshes the recorded App version, which four filters (Scale, Move, Round Outline To Grid, Slant Outlines) need at 1.2.10 or newer.
- Without the App checkout beside it the Output says so plainly. Uninstall removes only our links; a bundle you replaced stays.
- `tests/test_install_bundles.py` runs the real installer into a temporary data folder and asks App's `registry.discover` for the plugins (50 expected), plus rerun, uninstall, replaced-link and non-Git copy cases.

## 2026-11-12 — Everything Apache-2.0 (Issue 250, owner Q5)

- The four MIT SPDX headers (Nodes Close to Zones and Zoom to Selection, in `src/` and the `Extensions/` bundles) now read `Apache-2.0`; both are FontLab reimplementations with no upstream code copied.
- `NOTICE` retains the verbatim upstream MIT notices (Olli Meier 2019, TzuYuan Yin 2026) with repository commit and LICENSE SHA-256; `tests/test_licence_notices.py` guards them.


## 2026-11-12 — Pack workflow attaches the zip to tag releases (Issue 250)

- `.github/workflows/pack.yml` gains a `release` job: `needs: pack`, `if: startsWith(github.ref, 'refs/tags/v')`, job-level `contents: write` only, `github.token`, pinned download-artifact. It never creates a release: it polls `gh release view` (20 tries, 30 s apart) and then runs `gh release upload --clobber`; on timeout it fails with "release not created by lander within 10 min; run gh release create, then rerun this job".
- Procedure: push the `v*` tag, then within 10 minutes create the release with its notes (`gh release create <tag> --verify-tag --notes-file ...`). The job attaches the zip. If it timed out, re-run the job and verify the asset with `gh release view <tag> --json assets`.
- No App install, PyPI or deploy key was added; the App-free `--noconftest` test subset is unchanged. `actions/download-artifact` is pinned to v5.0.0 (`634f93cb2916e3fdff6788551b99b062d0335ce0`, matching the pinned upload-artifact v5).
- `tests/test_pack_workflow.py` pins the job set, the single job-level `contents: write`, the absence of pages/id-token/other write scopes, the tag trigger and condition, and the upload command; the old single-job test was split. Three mutants (extra `pages: write`, removed `if`, removed `--clobber`) each fail the suite. 10 passed in the App-free subset; ruff 0.14.10 and actionlint clean.
- Not yet observed: a real tag run (TODO row kept for the first `v*` push).

## 2026-11-12 — Pack workflow builds, checks and uploads the Extensions zip (Issue 250)

- `.github/workflows/pack.yml` (`contents: read`, pinned action SHAs, no secrets, one job) runs `tools/build_pack.py` and the new stdlib `tools/check_pack.py` (exactly the 50 mapped `plugin.json`, `README.md`, `Scripts/Plugmix`, no bytecode, no stray top-level entries) and uploads `fontlab-python-plugmix-extensions.zip` as an artifact. `tests/test_pack_workflow.py` pins the permissions and pinned SHAs, that no App import is needed, and that the check reports missing/extra entries.
- Only the App-free tests run in CI (`--noconftest`: `tests/test_pack_workflow.py`, `tests/test_extension_coverage_gate.py`; any skip fails the job). The rest of the suite stays out because `tests/conftest.py:42` and `tests/extensions/conftest.py` import `fontlabapp`, which is private: an owner-gated TODO row. Attaching the zip to releases also stays open.

## 2026-11-12 — Pack artifact verified on main (Issue 250)

- First main run of `pack.yml` on 9b6a287: Pack run 43123920993 succeeded ("pack ok"; App-free tests 8 passed, no skips) and its artifact `fontlab-python-plugmix-extensions.zip`, downloaded and listed, holds 50 `plugin.json`. Documentation run 43123921012 also succeeded. This closes "build and attach the pack as a CI artifact"; attaching to releases and the owner-gated full CI suite stay open in TODO.md.

## 2026-11-12 — Coordinate filters require App 1.2.10 (Issue 250)

- `min_app_version` of Move Outlines, Round Outline to Grid, Scale Outlines and Slant Outlines is now `1.2.10`, the first App tag containing the coordinate writer 277a001. Evidence: the remote tag `v1.2.10` peels to f05d87b (`git ls-remote --tags` on the App remote), and `git merge-base --is-ancestor 277a001 f05d87b` succeeds; v1.2.9 does not contain it. Delete Small Paths stays at 1.2.9.
- `tests/test_extension_manifest.py` now requires exactly 1.2.10 for the four filters and no 1.0.0 placeholder, and still checks tag-contains-commit against the sibling App checkout. Mutants: a floor of 1.2.9 or 1.0.0 on one filter fails the test.
- Evidence for d61ee46: `./test.sh` 405 passed; the Documentation workflow run 43119643603 succeeded on that commit.
- Closes the TODO row "Qualify the paired App coordinate-writer release". The native dialog checks for these filters stay open in their own TODO row.

## 2026-11-11 — Consumer audit page (Issue 250)

- Closed the TODO row "Audit all consumers, entry-point groups, startup/preferences, distribution membership and licences": the audit is published as `src_docs/md/consumer-audit.md` (site page `consumer-audit/`, nav entry added; generated `docs/` rebuilt). It lists the two entry-point groups, the deprecated `fontlabapp.plugmix` shim, preferences file and startup snippets, lock-file membership, Apache-2.0 licences and every consumer found in the maintained repositories; machine paths are stripped.
- Corrected the distribution row after merging the pack zip (`cd02988`): the wheel holds only `src/fontlab_plugmix`; Extensions and `Scripts/Plugmix` ship in the pack zip.
- The removal gate stays open. Its next check is now an outside-consumer search or a deprecation period, because third-party publishers and owner-installed copies cannot be known from the workspace.

## 2026-11-11 — ordinary pack artifact: Extensions zip, wheel stays compatibility-only (Issue 250)

- `tools/build_pack.py` builds `fontlab-python-plugmix-extensions.zip` (Extensions/, `Scripts/Plugmix`, README.md; no bytecode). `tests/test_pack_artifacts.py` (6 tests) pins that the zip holds exactly the 50 `plugin.json` files of `tests/bundle-map.json`, that an extracted copy discovers all 50 through `registry.discover`, that a missing `Extensions/` raises an error naming the pack, and that the built wheel has `fontlab_plugmix/` and no Extensions, Scripts or `plugin.json`.
- `tests/conftest.py` `pytest_configure` raises `pytest.UsageError` naming the pack when `Extensions/` is absent (wheel-only runs formerly ended in an INTERNALERROR FileNotFoundError); a subprocess test pins that message. The wheel test skips with a reason when `uv build` cannot run offline. README says the wheel is the compatibility package only. `--cov=tools` joins the pytest addopts; `tools/build_pack.py` covers 92%.
- This builds and tests the zip locally only; no CI step builds or attaches it yet (open TODO row). Suite: 405 passed (App and Pens main siblings). TODO row "Qualify ordinary pack artifacts" removed. Install of the pack stays copy-into-user-data; native checks stay open.

## 2026-11-11 — Delete Small Paths declares App 1.2.9; coordinate filter floors stay open (Issue 250)

- Delete Small Paths `min_app_version` 1.0.0 → 1.2.9. App v1.2.9 (b321f2e) is the first tag with the plugin core 81978fa (v1.2.8 lacks `plugins/filter.py`); its deletion-only filter host covers this filter. Its four `tests/test_filter.py` delete tests pass against an App v1.2.9 checkout.
- Move Outlines, Round Outline to Grid, Scale Outlines and Slant Outlines keep the 1.0.0 placeholder: they build coordinate LayerEdits, and no App tag contains the coordinate writer 277a001 (dated after v1.2.9). The TODO row stays open with the next check.
- `tests/test_extension_manifest.py` pins the floors and, with the sibling App checkout, checks that v1.2.9 contains 81978fa, v1.2.8 does not, v1.2.9 lacks 277a001, and any raised coordinate floor's tag contains 277a001. Mutants: Delete Small Paths back to 1.0.0 fails 1; Move Outlines at 1.2.9 fails 2; Move Outlines at untagged 1.2.10 fails 1.

## 2026-11-11 — Step and Repeat verified live (A2 live report 21, Issue 250)

- Step and Repeat (87fc0ec) with the active-glyph lookup stubbed: count 2, dy 50 adds two contour copies to Regular only (2 to 4 contours), one "Step and Repeat" row, exact Undo and Redo, save and reopen identical with clean history. The real Glyph-window lookup is owner-run and stays in TODO.

## 2026-11-11 — Delete Small Paths verified live (A2 live report 18, Issue 250)

- Delete Small Paths passes live on FontLab 9 (origin/main 87fc0ec): one Undo row, exact Undo/Redo, saved reopen clean. Step and Repeat stays open in TODO.

## 2026-11-10 — Issue 234 practical filters and tools (Lane C8)

Added Round Outline to Grid, Move Outlines, Scale Outlines and Slant Outlines
filters, plus Measurement Ruler, Node Probe and Contour Picker tools. All seven
are self-contained manifest bundles with pure geometry and explicit scope. The
existing 43 bundles remain; the pack now has 50. Added seven documentation pages
and rebuilt the site, preserving the reporter catalogue and licence assets.

The coordinated App Filter writer now supports guarded topology-preserving node
coordinate edits, required by these filters; native curve kinds are preserved
rather than reconstructed. Components, anchors and advance widths remain fixed.
Native dialogs, drawing, Undo/Redo and saved reopen remain open in TODO, as does
assigning a compatible minimum App release before distribution.

Verified Plugmix: 397 tests, all per-module coverage gates, full changed-file
Ruff and 37 documentation tests pass. The full paired App recipe passes 12,358
tests with 22 retained skips. All seven new bundle modules and the App
writer reach 100% line and branch coverage. Independent bundle and writer
reviews approved after regression fixes. See C8-REPORT.md for exact commands,
paired App gate results, files and acceptance limits. Landed after App main 277a001 (coordinate-edit writer); merged-tree Plugmix gate 397 passed, 37 documentation tests OK, graph risk medium (3 flows, all inside the new Measurement Ruler/Node Probe/Contour Picker bundles).

## 2026-11-10 — live font editing rule (Issue 250, D44)

- AGENTS.md: agents test and edit the font open in FontLab 9, starting from the Desktop VFJs, and may save them.

## 2026-11-10 — Issue 210 documentation repair

Updated the website for the 39 reporter Extensions bundles and Show Reporters
action, preserving every reporter description. Documented App core discovery,
startup and palette/menu enablement, the four other plugin kinds, and the
separate compatibility runtime with its native acceptance limits. Refreshed
NOTICE downloads byte-for-byte from root; LICENSE already matched. Rebuilt the
generated site and strengthened catalogue, search and attribution checks.

Validation: strict site build, 36 documentation tests and 353 normal tests pass.
The existing external Python 3.13 docs environment matches all 31 locked
versions; a fresh hash-locked dependency install was blocked by PyPI DNS.
No commit, push, package installation into FontLab or native acceptance.

## 2026-11-10 — Issue 210 Extensions reference pack

Moved App's 39 reporters and four concrete Filter/Palette/Tool/General examples
into 43 manifest bundles under Extensions. Retained their behavior and notices;
core imports use `fontlabapp.plugins`. Replaced reporter launchers with one
Show Reporters action; retained the separate compatibility package unchanged.
Documented the bundle contract and open native checks. Independent paired
source review approved; the controller repeated the 353-test suite and gates.

The complete direct source suite passed 353 tests on arm64 CPython 3.11.18.
All 43 bundle modules and the remaining action script exceed 80% line and 80%
branch coverage separately; the existing 51-module compatibility gate passes.
Ruff 0.14.10 F821 passes. The exact shell wrapper setup could not resolve PyPI
because DNS is unavailable; its attempted baseline is not a passing result.
Full commands and per-module evidence are in ISSUE210-PACK-REPORT.md.
Native UI/drawing/startup/history, installation, artifacts and delivery remain
open. No FontLab process or user installation was used.

## 2026-11-05 — Full source recipe qualification

Corrected the six-guide handoff to the retained 21:46:13 UTC full-run
receipt: no selectors, exit 0, 125 passes and full per-module checker,
Plugmix `dddadcd9bc8cee21d5f7b8fe60027495e13fd41a` with owned App
`fb6a93776772b996b25604f88711feb300b90109`. The 96% overall result is
line coverage; the 80% combined-module policy is unchanged. The earlier
installed-hook baseline remains historical evidence. Future tuple changes
require requalification; ordinary hooks, native and installed-artifact
acceptance remain separate. No additional product test was run for this
prose correction. Source, tests and policy files are unchanged.

## 2026-11-05 — Issue 230 remote documentation variant

Prepared six source-specific root guides for the package at
`dddadcd9bc8cee21d5f7b8fe60027495e13fd41a`. Retained existing README usage
and CHANGELOG history. Clarified the complete no-selector check, reporter
restrictions, undoable Filter/Palette edits and future Issue 210 architecture.
Checked guide structure and preservation hashes. No product test, native,
installation, canonical migration or remote-delivery result is claimed.

<!-- this_file: CHANGELOG.md -->
# Changelog

## 2026-11-10 — Issue 250 documentation round

- AGENTS.md describes the delegation, integration and release workflow.
- WORK.md reset to the current round; the earlier bytes are archived on the owner's workspace data volume, not public.

## Unreleased

- Refuse Step and Repeat on a displayed non-master layer and when the contour
  count changes before Undo. Honor owned panel close refusal and retry without
  losing the dock or its checked Window action. Test against the sibling
  fontlabapp worktree, preserve reporter state on failed disable saves, and
  suppress General font-open events after a failed initial read.
- Read General shortcuts through PythonQt's QAction property and compare
  normalized QKeySequences before assignment. Use `fgId` for font identity
  in General events, active-glyph checks and palette keys. Map a tool's first
  key event from the live cursor instead of viewport origin.
- Add native Tool registration with guarded event mapping, active-only mark
  painting and a selection-only Smart Select port. Add General menu commands,
  font-opened/closed polling on the palette timer, owned timers and actions,
  and Zoom to Selection. Save explicit Tool and General enable choices without
  changing old preference files.
- Resolve dock close filters through FontLab's `PythonQt.private.QObject` and
  keep palette Show working if close detection is unavailable. The Window
  toggle remains the explicit close control in that case.
- Keep tabbed and temporarily hidden palettes alive; only dock Close or the
  Window toggle changes their saved visibility. Resolve active glyphs through
  the workspace canvas, report failing captures once per key, and show palette
  Apply errors in its status label. Refuse zero-offset repeats.
- Add the dockable Palette kind, persistent Window toggles, a shared refresh
  timer, and Step and Repeat contour duplication through one geometry Undo step.
- Reuse outline safety checks and the layer writer for palette edits. Keep
  palettes out of Reporter and Filter menus; restore old preferences unchanged.
- Measure Delete Small Paths over flattened curves; preserve newly discovered
  filters when no filter choice was saved. Keep Apply working when saving its
  parameters fails, and skip unsafe glyphs individually.
- Restore polygon painter state with save/restore, and handle oversized stored
  numeric parameters by falling back to defaults.
- Added a shared `Plugin` identity and kind-filtered discovery. Reporter View
  actions remain reporter-only; the same entry-point group discovers Filters.
- Added `enabled_filters` and validated last-used `params` preferences while
  retaining old `enabled` files and unknown keys.
- Added a pure Filter contract, owned parameter dialog, deletion-only native
  writer through `outline_writer` and `layer_writer`, and Delete Small Paths.
- Reset polygon pen and brush after fill, ignore degenerate polygons, and
  cover empty contours and missing zones in existing reporters.
- Added twelve reporters for handle geometry, crosshairs, extrema, segment
  lengths, selected handles, anchors, sidebearings, unit grids, zone proximity,
  italic alignment, smooth-node angles and Glyph Focus.
- Use the native UPM for Unitizer spacing and normalize italic angle to a
  positive rightward slant in snapshots. Add filled polygon marks and tighten
  selected-segment and zero-length handle checks.
- Added immutable contour closure and smooth flags, selected-master zones and
  opt-in native ink bounds to reporter snapshots.
- Stop retrying a native canvas id after painter attachment fails; isolate
  registry teardown errors and preserve the original preference-save error.
- Harden native painter teardown against stale canvases and failed removal;
  suppress any callback left registered after a reporter is disabled.
- Keep startup working when preferences or a third-party plugin are broken,
  and roll back an overlay if its enabled state cannot be saved.
- Rename Nodes Outside Paths to Off-curve Handles Outside Bounds, migrating
  its saved enabled name. Clarify active-window attachment and snapshot cost.
- Let `test.sh` explain missing source checkouts and accept partial test runs.
- Stop querying canvas zoom during native painting when the value is unused.
- Prefer native per-canvas Python painters when present, with foreground and
  background ordering, multi-canvas attachment and EditorPainters fallback.
- Show full contour indexes on both on-curve and off-curve nodes.
- Make `./test.sh` discover the canonical sibling `fontlab-fontlabapp` checkout.
- Added Python 3.11 package, lazy native boot, reporter discovery, persistent
  View-menu toggles and immutable glyph snapshots.
- Added seven built-in reporter overlays and two FontLab menu scripts.
- Added pure and fake-native tests with per-module coverage enforcement.

## 2026-11-06 — Additive App script recovery

Recovered 38 missing reporter launchers and the two existing menu/report scripts
from the retained pre-pull product, byte-exact. Scripts use App
`fontlabapp.plugmix`; the separate `fontlab_plugmix` compatibility package, tests,
startup snippet, dependency metadata, NOTICE and licences remain. The guides now
distinguish both runtimes and retain future consolidation/framework/native tasks.
Do not combine their installers in one FontLab session.

Added 41 host-free recovery cases that execute all forty scripts against real
App discovery, boot, registry and menus with existing fake host owners and owned
preferences. They check repeated activation, painter registration, menu disable,
unknown preference preservation, handle-size setup and save-failure rollback.
The red run reproduced missing paths and wrong-runtime entry points. The exact
arm64 Python 3.11 full recipe then passed 166 tests and the existing 51-module
checker; explicit branch coverage measured all forty complete script modules
at 100% (122 statements, no branches). The unchanged per-module 80% combined
gate remains. No production package source, test oracle, coverage selector or
exclusion changed. Source checksums are provenance, not functional tests.

Independent review, the normal installed pre-push gate, commit/default delivery,
canonical adoption, native FontLab behavior and publication remain separate.
No owner installation or native operation was performed.


## 2026-11-06 — Issue 233 source/build-only site candidate

Added complete authored site pages, the separate 31-package hash-locked
ProperDocs/MaterialX environment, light fltheme26 controls, generated output and
a main-only two-job build workflow. The read-only job verifies exact source or
direct docs-only child lineage, non-doc identity, the shared source epoch and
full tracked/untracked parity. No Pages permission, request or deployment exists.

Strict builds, all 20 docs tests, actionlint and shellcheck passed. Independent
docs environments rebuilt every output file byte-identically. Real local Git
tests cover changed/unchanged output, foreign staged source, wrong checkout,
missing/unreachable main, stale/concurrent source, hook refusal, immutable lineage
and unexpected ignored output. Cross-date builds retain the original source epoch.
Local Chromium desktop/mobile searches and ordinary result clicks passed;
Escape returns focus to the opener and navigation closes. Dark OS preference
and stored slate remain light. Bulk fill/type event failures and the shared
outside-close focus gap remain disclosed; no WCAG or universal-repeatability
claim follows.

Product source/data, original licences, scripts, runtime locks, recovery pins
and Git refs/configuration remain unchanged. The later freeze found an isolated
index byte-guard exception; staged entries still match HEAD, with no cached
source changes. The cause is not proved. Preserve the current index and use
fresh delivery guards; no old index is restored. Source/generated
patches are local review candidates based on the current source epoch. Independent
review, actual main Actions, fresh-epoch generated delivery, installed/native
acceptance and private P/L remain separate. No product/native suite, owner
installation, commit, push or Pages operation was performed.


## 2026-11-07 — Exact frontend notices and English search assets

Added exact upstream frontend notices and source-map provenance for the existing MaterialX 10.1.8 payload. Explicit English configuration and a small build hook reject language, corpus, reference, asset-set or hash drift before omitting the 35 unused language helpers. All nine retained core assets, original product legal files, guides, catalogue rows, media, runtime and dependency/build locks are preserved.

The strict site build and all 35 documentation tests pass. The complete new hook has 100% statement/branch coverage; real Git staging, checkout and archives preserve exact legal bytes. An independently installed matching lock reproduces all 50 output bytes and modes. Existing immutable source/output, epoch, concurrency and full-parity workflow checks remain active. Browser and independent review evidence are separate from these local checks.

Private Pages configuration, grants, requests and publication remain owner-held; this source follow-up adds none.
No product release or installation is claimed. Prior ordinary artifacts remain bound to their recorded revisions; a later Git revision changes genuine hatch-vcs metadata. Full current source archives include these documentation additions; no unchanged-sdist or whole-wheel identity is asserted. Native acceptance and owner installation remain separate.


## 2026-11-07 — installed icon path-tuple inventory refinement

The current HTML/CSS contains 45 distinct ordered SVG path tuples. A complete scan of the four installed MaterialX icon families finds 43 exact installed matches and two unmatched Lucide tuples, refining the earlier known-candidate inventory. The additional installed match is the Font Awesome version caret-down. Its existing CSS header and full notice retain Font Awesome Free 7.1.0, Fonticons and CC-BY-4.0 icon attribution. The official NPM caret SVG has different raw path bytes; no unmodified-primary SVG, whole-geometry or optimizer-recipe equivalence is claimed. The two unmatched Lucide tuples retain their pinned SCSS source attribution.

A new actual-output regression derives these counts and checks installed matches, unmatched CSS references and the caret header. It fails against the prior 42 count and passes with the corrected metadata. All 36 current documentation tests pass; full strict and independent exact-lock builds match every output byte and mode. Only the legal paragraph, corresponding inventory and legal search row change in the site. Runtime, packaging, generators, vendor assets, full notices, existing guidance and the Fly search fix remain exact. Fresh browser verification and independent review are recorded separately. No private Pages operation, delivery, installed-product upgrade or native acceptance is claimed.


## 2026-11-07 — Reconcile recovered-script tests with App menus

Updated only the recovered-script test fixture for current App's owned
View > Reporters submenu, label order, separator and Hide All action. The
compatibility package's existing menu fake remains unchanged. Tests find each
reporter by its visible label, exercise real App menu callbacks, verify repeated
installation, and preserve painter-removal, preference and save-failure checks.
The menu installer now correctly expects 39 reporters, Hide All, Filter and
Palette actions (42 total).

Against App `99851b8aafbe00e9588b1485807e0eeac4fdd9d3`, the unmodified source
reproduced 41 failures and 125 passes. After this test-only correction, all 166
cases pass in the full no-selector recipe and the normal-hook test recipe on
asserted arm64 CPython 3.11. The full 51-module compatibility coverage checker
passes; the separate full branch-coverage run measures all forty recovered
Scripts at 100% (122 statements, no branches). All existing runtime source,
scripts, packaging, recovery hashes, site source and generated output remain
unchanged. The ordinary installed hook, reviewed source delivery and current
Actions must still run on the final committed tuple. No native acceptance,
owner installation, product release or private Pages operation is claimed.

## 2026-11-10 — integration-round guidance

Require independent verification, fresh upstream/team reconciliation and normal nonforce integration after important rounds. Move only verified solved TODO scope into cumulative history, update remaining plans and continue authorized work; existing preservation and admission holds remain unchanged.

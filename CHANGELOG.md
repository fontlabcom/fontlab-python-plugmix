---
this_file: CHANGELOG.md
---

## 2026-11-17 — Task-list cleanup (Issue 258)

- Closed and removed from TODO: T28 App 1.2.20 installer propagation (the legacy installer and `install.vfpyc` were deleted and `install.vfpy` is the fontlab-instamix stub, Unreleased entry below; v1.1.16 compatibility release qualified at `9a41985f`, v1.1.19 tagged), the duplicate reporter/filter/palette row, P04/P05 graph-evidence rows, the additive-recovery review and the Issue 233 independent-review row (obsolete process rows).
- Pack check at `76fbdaf`: `python3 tools/build_pack.py` builds 105 members with 50 manifests and 50 bundle directories and `tools/check_pack.py` prints `pack ok`; this is correct, not a defect.

## Issue 256 canonical bundle names — 2026-11-17

Renamed all 50 bundle suffixes through intermediate paths; preserved stems, IDs, classes, plugin behavior and exact LICENSE/NOTICE bytes. Updated maps, tests and source/generated docs. App requirements and bundle minimum versions now require 1.2.31 for lowercase support. Before that floor update the exact no-selector runner passed 459 tests and every coverage checker; final source checks in the prepared genuine App development environment pass 459 and the unchanged checker. Strict docs rebuild and 38 docs tests pass. Earlier on 2026-11-17, the exact runner refused the then-unreleased App 1.2.31 floor. Case-sensitive scratch tests also exposed an earlier Instamix defect: modified/unowned legacy bundles remained beside new bundles and lost their old receipt entries. The later qualification below supersedes these blockers while preserving their failure history.

### Later qualification — 2026-11-17

Instamix 1.0.8 is published from main `9391218`, with managed legacy-conflict refusal and bootstrap readiness checks. App 1.2.31 wheel/sdist are published on GitHub at `624a07f`; downloaded and installed artifact hashes are verified. App PyPI publication remains open: release workflow `44012812669` failed with `invalid-publisher` and requires an administrative fix. Do not infer App 1.2.31 availability from PyPI.

The exact no-selector Plugmix runner against genuine tagged App 1.2.31 now passes 459 tests and the unchanged coverage checks in 5.69 seconds (`exact-final-released-app.log`). This qualifies source compatibility; Plugmix fresh-main integration, normal hooks, release/artifact delivery, installation and native/Windows migration remain open.



## Unreleased

- Site now uses the fly-january 0.2.1 theme (chrome: fontlab).
- `install.vfpy` is now the stub from fontlab-python-instamix 1.0.15. It replaces an
  installed instamix older than 1.0.13 and puts the old copy back if the upgrade
  fails; linked checkouts and local builds are kept. A download that fails for
  lack of root certificates (FontLab 9 for macOS) is retried with the system curl.
- `install.vfpy` is now the short fontlab-instamix stub. It installs
  fontlab-instamix from PyPI when it is missing, then installs this checkout from
  its `[tool.fontlab-install]` table. The large legacy installer is gone.
- The compiled legacy `install.vfpyc` is deleted.
- `tests/test_install_bundles.py` tests the stub, the install table and that FontLab's
  plugin core finds all 50 bundles in `Extensions/`; link and uninstall behavior is
  now instamix's and tested there.
- README describes the stub install.

## 2026-11-15 — Shared installer source propagation

- Copy the exact reviewed App 1.2.20 installer, preserving declared constraints and managed origins, refusing unverifiable no-uv conditions, and skipping inactive conditional siblings before execution.
- Align owned bundle-lifecycle fixtures with prepared, dependency-free installer inputs; retain the real requirement guard and assert no-uv App-floor refusal before script/bundle mutation. Preserve both declared App/Fly floor checks.
- All 30 focused installer/archive/pack checks pass. The genuine source-archive regression already retains exact installer bytes. Bundle/runtime/legal bytes, manifests, project metadata and dependencies remain unchanged. Delivery, the complete installed cohort and native acceptance remain unqualified.



## 2026-11-14 — Plugmix 1.1.16 compatibility release qualified

[Plugmix v1.1.16](https://github.com/fontlabcom/fontlab-python-plugmix/releases/tag/v1.1.16) binds actual main and peeled annotated tag to `9a41985f44e44d6a2db263e8d34983b803f5aea1`. Normal main/tag hooks passed 464 tests in 5.10/5.32 seconds. The complete source suite passed 464 tests with zero skips, all retained coverage gates and unchanged Ruff. Main Pack43647893594 and Docs43647893608 succeeded; both documentation jobs passed 38 cases with SOURCE==OUTPUT==the released source. Tag Pack43648527211 succeeded, including release attachment.

All three actual downloads are qualified (`download-audit.json` in the task's Falstaff evidence folder). Wheel/sdist match the reviewed hashes; the CI ZIP has 105 source-exact files/modes and 50 manifests: 46 at App 1.2.9 and four at 1.2.10. Its different container hash is reviewed; member bytes/modes are exact. Wheel and installer require App >=1.2.10; the installer already declares Fly >=1.3.0. Exactly 45 manifest fields changed. Runtime Python, installer logic, legal bytes and older releases remain unchanged.

Actual downloaded Plugmix with released App 1.2.18 and supplied Fly 1.3.1 passed a LIMITED provider cohort: 463 tests, one source-routing deselection, 6.08 seconds. All three origins are inside the owned prefix; no native provider loaded. Preserve failed attempts: missing Fly during collection (the compatibility wheel does not bundle the 50 Extensions), normal Fly resolution because Echopy is absent from the registry, and two test-helper import errors. Supplying Fly with --no-deps only in this prefix and correcting the existing test/tool helper paths established the bounded result; no source correction or complete provider closure follows. The installer already declared Fly, so this is not a missing-dependency defect.

Workspace PLUGMIX-COMPAT-RELEASE-REVIEW.md explicitly APPROVEs published assets and LIMITED prefix runtime evidence. T16 alone is complete; all 52 IDs, 51 unfinished families and 17 JSON rows remain unchanged. T18/T28/global T29 and native acceptance remain open. Root install.sh and FontLab installation/native checks remain held; cleanup STOP and all existing exclusions, pauses and publication holds persist.

## 2026-11-14 — App minimum-version source correction

Both package and pack-installer requirements now declare App >=1.2.10, the first
release with the coordinate writer needed by all four coordinate filters.
Forty-five non-filter manifests now require App 1.2.9, the first release with
`fontlabapp.plugins`; Delete Small Paths already requires 1.2.9 and the four
coordinate filters retain 1.2.10. The README and manifest example agree.
No plugin Python, installer source, legal file or bundle identity changes.

Two new regressions first failed against the unbounded requirements and old
manifest floors, then passed. Existing installer expectations now include the
version requirement. The full host-free source recipe passes 464 tests with
zero skips and all retained coverage gates; Ruff 0.16.7 passes. A local pack
build/check retains 105 exact-source members, 50 manifests/classes and legal
bytes. Independent review, main/release delivery, downloaded artifacts and
native acceptance remain pending. Global T18/T29 and native tasks stay open.

## 2026-11-14 — v1.1.15 released and downloaded artifacts qualified

[Release v1.1.15](https://github.com/fontlabcom/fontlab-python-plugmix/releases/tag/v1.1.15)
binds [35a6c3fa](https://github.com/fontlabcom/fontlab-python-plugmix/commit/35a6c3fa09cc8504f13d9fb0d88b4a5c366eb57a).
The ordinary main and tag hooks each passed 462 tests. The maintained source
suite passed 462 tests with zero skips and every retained coverage floor.
[Main Pack](https://github.com/fontlabcom/fontlab-python-plugmix/actions/runs/43641875122)
and [documentation CI](https://github.com/fontlabcom/fontlab-python-plugmix/actions/runs/43641875198)
passed; both 38-case documentation checks bind source and output to that commit.
[Tag Pack](https://github.com/fontlabcom/fontlab-python-plugmix/actions/runs/43643679727)
passed both pack and release jobs and published all three assets.

The downloaded Extensions ZIP has 105 unique safe-path members, exact released
source bytes and Unix modes, passing CRC, all 50 manifests/classes, exact
LICENSE/NOTICE and current StepAndRepeat, ShowStems and SpeedPunk modules.
Downloaded wheel and sdist match the qualified local artifacts. Their ordinary
artifact cohorts each pass 461 tests with one explicitly source-routing-only
deselection; the source suite covers that route. A separate downloaded-wheel
runtime cohort passes 461 tests in 4.04 seconds. These are external host-free
artifact checks, not FontLab user-folder installation or native execution.

Downloaded asset SHA-256 values:

- Extensions ZIP: `70d40cf0e39ec082b67221d3c064c52177a98d61acd7e92988f3db28b94c1342`.
- Wheel: `768af8b575c835227387b5ac920b520d9f03de701a928182f926e58cd424f6eb`.
- Sdist: `dee659a770d0de497f4c9867fa71925005f5f2ca3ce1df167aafabd363ae3f88`.

The historical v1.1.14 ZIP remains byte-identical at
`ecfaf2d63cab3d52657f823164c413a91fa840f116d916ff681e006b3e395cc7`;
the captured owner index also remains unchanged. This closes the current-source/P01 release rows and the first-tag release-job
verification row. Independent final artifact review qualifies T16; global T29
and native acceptance remain open. P04/P05, Issue 255, every native/install/GUI/history/reopen requirement,
Issue 123's pause and private Pages holds remain. Earlier preparation and
pending-release wording below is historical; this entry supersedes only its
bounded release/download status. This ledger successor changes no product code
or frozen v1.1.15 artifact and requests no new product release.


## 2026-11-14 — Functional work order documented

- Added the owner's functional-progress-first guidance and repository-specific priorities, including cross-package compatibility and a later detailed testing pass. Existing mandatory hooks, holds and unfinished work remain in force.
- This change updates guidance and planning only; it establishes no new runtime, installed, native or release result.

## 2026-11-14 — Current-source release preparation documented

- Preserved the reviewed functional-priority guidance and existing backlog in
  the current-main successor; documented the already identified historical ZIP
  difference and the separate pending release qualification surfaces.
- Controller source qualification passes 462 tests with zero skips (8.03
  seconds), all per-module 80% floors including 50 Extensions/helper/startup,
  98% overall coverage and full-tree Ruff 0.16.7. The host-free builder/checker
  and independent local pack audit pass 105 exact source/mode/CRC/path members,
  50 manifests/classes and exact legal bytes against accepted App 1.2.18 source.
- Normal main/tag gates, full CI and published/downloaded ZIP, wheel and sdist
  remain pending. No new installed or native result is claimed.

## 2026-11-14 — Reviewed combined source delivered to main and exact-commit CI

- Independent specification and quality review accepted the combined P01/R01
  ZIP legal/preflight, P03 documentation oracle and P02 lint repairs.
  [Main 40cac692](https://github.com/fontlabcom/fontlab-python-plugmix/commit/40cac69290a5027f205ca2a0bee24239e04fc37b)
  contains the exact reviewed 33-path delta, tree
  `4315dc6ef4eac462be8a32892fd70e9afb408f60`, parent
  `b874cf606a30ba3e99d0905522c5c8db6829c15c`. Normal installed-hook push and
  post-push/post-CI remote SHA verification passed.
- Controller qualification passed 462 source cases, unchanged complete
  coverage checkers, all 38 locked docs cases, strict build, zero full-tree
  Ruff 0.16.7 diagnostics, 21 App-free cases and genuine source-artifact gates.
  All seven complete changed production modules meet the unchanged 80%
  combined policy without exclusions; each separately meets 80% statements
  and branches. Bundle-specific line/branch rules remain unchanged. The normal
  hook passed tests only with zero changed compatibility-src modules; the
  separate full gates supply seven-module coverage.
- [Pack 43527359696](https://github.com/fontlabcom/fontlab-python-plugmix/actions/runs/43527359696)
  passed `pack`; [Documentation 43527359690](https://github.com/fontlabcom/fontlab-python-plugmix/actions/runs/43527359690)
  passed `build` and `qualify-generated-output` at that exact commit. The
  tag-only release job correctly skipped on main. The downloaded CI pack has
  105 members and 50 manifests; all payload bytes and Unix modes, including
  exact LICENSE/NOTICE, match committed source. Inner-ZIP SHA-256:
  `40e0d9d73e0345a66893d6f064741bca0ad9b1795fd0202147011971b7b34066`.
- The four controller gate indexes and named canonical-owner endpoints match
  their retained baselines, including all 330 tracked files, administration,
  refs and worktree attachments. Earlier owned-index intervals and the
  controller setup UNTR interval remain FAILED, writer UNKNOWN; no earlier
  raw index was restored. This is endpoint evidence, not global preservation.
- Closed only combined whole-change review and controller main/hook/remote-CI
  delivery. New release/download, final-version artifact/provider admission,
  graph gaps, installation and native acceptance remain open. Precommit
  source artifacts are not release wheels; the old v1.1.14 asset is unchanged.
  Historical candidate-pending wording below describes its dated checkpoint
  and does not reopen this verified source/main/CI milestone or erase failures.

## 2026-11-13 — Combined local ZIP, documentation and Ruff qualification

Compose the independently reviewed ZIP legal/preflight and documentation oracle
repairs on current main. Repair all 45 remaining Ruff findings without changing
configuration, ignores, dependencies, public APIs or source oracles. Preserve the
startup catch, explicit print text, continuation and normal non-DEBUG output
with named DEBUG exception records; preserve the exact
README example through a temporary UTF-8 runpy harness. Keep the ProperDocs
side-effect import and RGB/three-point numerical operations.

All 462 source cases, unchanged complete coverage checkers, 38 locked docs
cases, strict build, full-tree Ruff 0.16.7, App-free CI and pack build/check pass.
All original 456 source and 38 docs IDs/assertions/decorators remain, with six
new meaningful regressions and no new skips/exclusions. Seven complete changed
production modules exceed the unchanged 80% statement, branch and combined
floor; the docs hook has 100% statements and branches. Controlled builds retain
102 unaffected ZIP members' exact bytes and metadata, all 105 names and 50
manifests; repeated same-input ZIP bytes match. Exact legal files and prior-output
preservation regressions remain.

The owned source index gained UNTR before the final gates (33,984 to 34,250
bytes); writer unknown, preservation interval failed, no old bytes restored.
Later source/peer captures are exact. The final graph maps three affected
compute flows at MEDIUM risk; overflow, UNKNOWN callers and budget limits remain. Named DEBUG uses existing configuration; enabled handlers may emit a traceback
to their configured destination (including stdout) or raise. getLogger may
register its name; no root logger configuration, level or handler is changed.
The caplog regressions qualify only their tested named-logger configuration. runpy executes in-process, without a sandbox claim.

This records local source/artifact checks only. Independent whole-change review,
controller delivery/hooks/CI, release/download, provider admission, root install,
GUI/native acceptance and private Pages remain separate. The historical local
candidate results below describe their earlier trees and are superseded by this
combined gate result only at the stated scope.

## 2026-11-13 — Documentation content comparison (local candidate)

The cross-date rebuild test now compares worktree content and mode against the
index with an explicit Git patch, with external diffs and text conversion off.
The five-state real-Git regression preserves raw index bytes and mode, ignores
timestamp-only changes, detects content/deletion/executable changes, and keeps
the staged-only baseline. All original output hashes, 58-file count, epochs,
lineage and generated-output parity checks remain.

Local checks: 438 source tests, unchanged complete coverage checkers, 38 locked
documentation tests and the strict build pass. The changed test has no Ruff
findings; the full-tree baseline and candidate retain the same 47 findings.
The owned source index gained an UNTR extension during the gate interval;
the writer is unknown, that preservation interval failed and no bytes were
restored. Three owned peer indexes and all regression fixture indexes stayed
exact. Independent review, main delivery and CI remain open. ZIP legal files,
provider admission, release, installation and native acceptance are separate.


## 2026-11-13 — Local ZIP required-input preservation correction

- Preflight README, LICENSE and NOTICE as readable regular files before creating the output directory or opening the archive. Missing-file and permission exceptions retain their native path; invalid file types raise a clear path-bearing ValueError. This closes the local R01 truncation defect without adding an atomic-publishing framework.
- Twelve required-input regression cases fail against the reviewed candidate. The corrected candidate passes 31 focused tests and all 456 source tests with the unchanged coverage checker. Both complete changed tools meet the existing 80% statement, branch and combined floor. Existing output bytes/mode survive missing, directory and unreadable inputs; absent output stays absent on missing input.
- Successful ZIP bytes are identical before/after this correction under identical source inputs: 105 members, 50 manifests and unchanged metadata. Expanded Ruff still fails with the same 45 diagnostics. The unchanged docs 36-pass/one-failure result, provider/graph limits and installation/native/delivery holds remain open.
- Independent review of the R01 correction is pending. The earlier sealed candidate and its failed required-input behavior are retained; no commit, push, release, owner installation or native acceptance is established here.

## 2026-11-13 — Local Extensions ZIP legal-file repair

- The pack builder adds the exact root LICENSE and NOTICE bytes after the existing payload. The existing pack checker requires and allows those two names; all bundle and exclusion checks remain.
- Eight new real-ZIP regression cases fail before the fix. The repaired source passes 446 tests and the unchanged per-module coverage checker; both complete tool modules meet the 80% statement and branch floor. All 103 original ZIP members retain their bytes, ordering and metadata; the archive now has 105 members and the same 50 manifests. Repeated same-input builds match.
- Strict docs build passes. The two touched tools are executable and Ruff-clean. Expanded Ruff remains failed with 45 diagnostics (only the two existing tool EXE001 findings removed), and docs discovery remains failed with 36 passing tests and the existing Git comparison failure. These findings are not waived.
- This is an uncommitted local candidate. Independent review, integration, release/download and installed/native acceptance remain open; the published v1.1.14 asset is unchanged.

## 2026-11-13 — Issue 255 verified release qualification

- [fontlab-python-plugmix v1.1.14](https://github.com/fontlabcom/fontlab-python-plugmix/releases/tag/v1.1.14) is released at `13e7d9182b39417378bfcd07e7e46e9707e64e39`. Reviewed main/tag delivery, applicable CI and actual downloads match the qualified artifacts.
- All 51 authored consumers use Fly. The bounded sdist selection repair excludes operational session data and the compiled installer while preserving product and legal source.
- 438 source tests, 53 complete changed-module gates and 37 documentation tests pass. Genuine wheel/sdist ordinary cohorts each pass 244 checks with one explicitly source-only routing deselection; source covers that case. The downloaded Extensions ZIP contains the exact 103 reviewed member names/bytes for 50 plugins. Normal main/tag hooks, CI and actual wheel/sdist/ZIP downloads are qualified.
- Ordinary external installation is qualified; installed FontLab/native acceptance remains unproved under D43.

## 2026-11-12 — D46 documentation pass (Issue 250)

- Landed this session, all on `main`: Apache-2.0 headers for the two reimplemented plugins (`874cce3`), `install.vfpy` linking the 50 Extensions bundles (`f3799c2`), App-first install order (`701b2cb`), the README note on App 1.2.10 filters (`78ea025`).
- TODO's Plugmix Demo row now lists the bundle counts and the filter, history and restart checks. PLAN says the bundles install through `install.vfpy`. WORK.md is a short status note; its previous bytes (2,969 bytes, sha256 `9394b88f870b035b10ca4a6786631c684e650783900df95717561ddc9dc6a61a`) are archived on the owner's data volume.
- No code changed.

## 2026-11-12 — README names which filters need App 1.2.10

- The install note said "some bundles (the filters)" and left "them" ambiguous. It now says four of the five filters (Scale Outlines, Move Outlines, Round Outline To Grid, Slant Outlines) need App 1.2.10 or newer, that an older recorded version rejects those four, and that App's startup hook discovers the bundles. Documentation only.

## 2026-11-12 — install.vfpy installs the 50 bundles (Issue 254)

- Plugmix Demo showed no plugins because nothing put the `Extensions/<kind>/*.fontlab*` bundles where FontLab looks. `install.vfpy` (byte-identical to App's) with the new `[tool.fontlab-install]` table (`extensions = "Extensions"`, `packages = []`) links all 50 (39 reporters, 5 filters, 4 tools, 1 palette, 1 general) and copies `Scripts/Plugmix`; a non-Git folder installs a copy under `Extensions/<id>/bundles/<kind>/`.
- Install order: run App's `install.vfpy` before this one and again after updating App; it refreshes the recorded App version, which four filters (Scale Outlines, Move Outlines, Round Outline To Grid, Slant Outlines) need at 1.2.10 or newer.
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


## 2026-11-13 — Issue 255 Fly consumer source candidate

Route 121 App imports in all 50 Extensions and Show Reporters through `fly.ap`,
preserving exact App module/class identity and original import placement. The
optional startup snippet now calls App's installer through `fly.ap.plugins`;
README's reporter example uses App's `Mark`/`Reporter` and its actual
`fontlabapp.plugmix` entry-point group. Retained compatibility classes and their
`fontlab_plugmix.plugins` group remain distinct and supported.

Document Fly >=1.3.0 as the public pack prerequisite without adding a compatibility
library dependency. The source test runner explicitly selects owned Fly and Pens
sources and arm64 Python 3.11. Full no-selector recipe passes 437 tests and every
original coverage gate, plus the startup snippet; all 53 complete changed Python
production/checker modules exceed 80% statements and branches with no exclusions.
Startup and the changed checker each measure 100% statements/branches. Tests
exercise real App discovery and registration with fake hosts, isolated exact-source
Fly identity, README entry-point discovery and startup failure containment.
No native behavior, release or installed artifact is qualified by these source
checks. Compatibility source, manifests, licences, frozen audit and shared
installers remain unchanged. The controller rebuilt generated documentation;
strict build and 37 documentation tests pass with the exact locked environment.
Independent specification and quality review pass after the bounded fixes.
Ordinary integration and remote delivery remain pending.


Issue 255 review follow-up: declare Fly >=1.3.0 in the pack installer's consumer
dependency table while preserving the App-only compatibility-library dependency
and shared installer bytes. The actual installer regression verifies forwarding
to uv without inherited Fly PYTHONPATH. Bundle coverage failure cases now keep
startup evidence healthy, independently testing both module families. Bounded
checks pass 25 tests; the full source recipe passes 437 tests and all gates.


Controller verification confirms 437 tests and all 53 complete changed-module
gates (minimum statements 93.1034%, branches 81.25%, zero exclusions).
Fresh origin/main is unchanged at d58fd0a with zero divergence. Scoped graph
analysis reports 73 files, 23 symbols, zero affected processes and LOW risk;
source comparisons and tests corroborate the truncated symbol list. This records
reviewed source and rebuilt-documentation acceptance only, before main/pre-push/CI
integration, genuine artifact qualification and separate native acceptance.

The documentation requirements lock SHA-256 is `961b3ec6b8ffde319473d3c17325d1699915c236a657a91baef77b5527215070`.


Final review corrected only the two new I001 import-order findings in installer
and runner tests. Ruff 0.16.7 with `--select I001` passes those files; the earlier
0.14.10 default-selector pass does not establish broad lint acceptance. Controller
comparison retains existing StepAndRepeat I001, ShowStems/SpeedPunk RUF007,
startup BLE001, coverage-test I001 and installer FURB192 findings. Bounded tests
pass 14 cases; the full source suite passes 437 tests and all coverage gates.


## 2026-11-13 — Issue 255 source-distribution selection repair

The prior Fly consumer source milestone reached 05176d30 with successful CI.
Fresh artifact qualification then found operational session data and a compiled
installer carrying local paths in Hatch's default source distribution. Exclude
only root `.omc` and `install.vfpyc` from sdists; keep both checkout sources intact
and leave wheel, Extensions pack, runtime dependencies and shared installers exact.

A real uv sdist regression reproduces the failure and now verifies those payloads
are absent while intended library, userpack, documentation, test, legal and source
installer members retain exact bytes. All 7 packaging tests and the full 438-test
source suite pass with the retained coverage gates. Ruff 0.16.7 I001 passes the
changed test file; baseline lint findings remain disclosed. This records local
source/artifact-selection evidence before review and delivery of the repair;
release, installed-tuple and native acceptance remain separate.

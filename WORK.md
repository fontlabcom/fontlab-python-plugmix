---
this_file: WORK.md
---

# Source and acceptance handoff

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

## 2026-11-05 — Issue 230 remote variant

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
The later full no-selector `sh test.sh` run on 2026-11-05 at 21:46:13 UTC
passed: exit 0, 125 tests and the full per-module checker. It used this
source and owned App `fb6a93776772b996b25604f88711feb300b90109`.
The observed 96% overall line coverage supplements the unchanged 80%
combined-module policy. Requalify after a source or App tuple change.
Offline fake-host tests do not establish native or installed-artifact acceptance.

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

The README retains the remote installation, startup, plugin, reporter and
native-limit descriptions exactly. NOTICE and all supporting source remain
unchanged. The private manifest binds all six preimages and proposal hashes.
Independent review precedes guarded application. Later controller application,
checks, remote branch SHA and integration belong in the external live ledger.
This entry claims documentation authoring only.

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

Added the owner’s round-by-round review, upstream reconciliation and backlog-maintenance rule to AGENTS. This is documentation-only preparation; independent review and applicable repository checks remain required before delivery. No runtime, installation, native or publication acceptance is asserted.

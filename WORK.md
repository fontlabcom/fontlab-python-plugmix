---
this_file: WORK.md
---

## Documentation theme — 2026-11-23

The strict fly-january 0.1.1 build produced 63 files. Two clean builds matched byte for byte. All 15 HTML pages contain one FontLab menu and footer, the Plugmix label and local search. All 24 site, frontend and English-search tests passed. The 15 disposable Git fixture tests remain unrun under the no-add/commit/push instruction. Both package runs passed all 459 tests with the Instamix 1.0.15 stub used by this checkout. The current sibling 1.0.19 stub differs.

## Issue 256 canonical bundle names — 2026-11-17

Renamed all 50 bundle suffixes through intermediate paths; preserved stems, IDs, classes, plugin behavior and exact LICENSE/NOTICE bytes. Updated maps, tests and source/generated docs. App requirements and bundle minimum versions now require 1.2.31 for lowercase support. Before that floor update the exact no-selector runner passed 459 tests and every coverage checker; final source checks in the prepared genuine App development environment pass 459 and the unchanged checker. Strict docs rebuild and 38 docs tests pass. Earlier on 2026-11-17, the exact runner refused the then-unreleased App 1.2.31 floor. Case-sensitive scratch tests also exposed an earlier Instamix defect: modified/unowned legacy bundles remained beside new bundles and lost their old receipt entries. The later qualification below supersedes these blockers while preserving their failure history.

### Later qualification — 2026-11-17

Instamix 1.0.8 is published from main `9391218`, with managed legacy-conflict refusal and bootstrap readiness checks. App 1.2.31 wheel/sdist are published on GitHub at `624a07f`; downloaded and installed artifact hashes are verified. App PyPI publication remains open: release workflow `44012812669` failed with `invalid-publisher` and requires an administrative fix. Do not infer App 1.2.31 availability from PyPI.

The exact no-selector Plugmix runner against genuine tagged App 1.2.31 now passes 459 tests and the unchanged coverage checks in 5.69 seconds (`exact-final-released-app.log`). This qualifies source compatibility; Plugmix fresh-main integration, normal hooks, release/artifact delivery, installation and native/Windows migration remain open.



## 2026-11-15 — Shared installer propagation ready for review

Copied the exact reviewed App 1.2.20 installer (`ec862276632cbf5b8b3f680ebd101ee17f8eecfbb77b383b2210931164c053c4`). It retains constraints and managed origins, refuses unverifiable no-uv requirements before sibling mutation, and evaluates conditional requirements externally with uv/packaging. Permanent package dependencies, installer-specific metadata, all 50 bundles, App floors, runtime source and legal inputs are unchanged.

The existing 30 installer/archive/pack checks passed before the copy (1.79s). Seven lifecycle cases then exposed their obsolete missing-provider setup: they expected installation despite declaring dependencies missing without uv. Owned lifecycle TOML now explicitly declares no external installer dependencies; the real missing() remains unmocked. The dedicated case restores the real App/Fly declarations and proves no-uv App-floor refusal before any scripts/bundles appear, with no false Installed success. The UV-request test restores and checks both original floors. All 30 focused cases pass (1.88s); existing actual source-archive coverage already checks exact install.vfpy bytes, so no new test or build configuration was added.

This is a local source candidate. Independent review, full hooked combined checks, main/CI, actual release/downloads and the installed provider cohort remain pending. Native/root installation stays held. Detailed cold-cache, full-cohort and native acceptance follows separately; no original open requirement is closed here.



## 2026-11-14 — Plugmix 1.1.16 compatibility release qualified

[Plugmix v1.1.16](https://github.com/fontlabcom/fontlab-python-plugmix/releases/tag/v1.1.16) binds actual main and peeled annotated tag to `9a41985f44e44d6a2db263e8d34983b803f5aea1`. Normal main/tag hooks passed 464 tests in 5.10/5.32 seconds. The complete source suite passed 464 tests with zero skips, all retained coverage gates and unchanged Ruff. Main Pack43647893594 and Docs43647893608 succeeded; both documentation jobs passed 38 cases with SOURCE==OUTPUT==the released source. Tag Pack43648527211 succeeded, including release attachment.

All three actual downloads are qualified (`download-audit.json` in the task's Falstaff evidence folder). Wheel/sdist match the reviewed hashes; the CI ZIP has 105 source-exact files/modes and 50 manifests: 46 at App 1.2.9 and four at 1.2.10. Its different container hash is reviewed; member bytes/modes are exact. Wheel and installer require App >=1.2.10; the installer already declares Fly >=1.3.0. Exactly 45 manifest fields changed. Runtime Python, installer logic, legal bytes and older releases remain unchanged.

Actual downloaded Plugmix with released App 1.2.18 and supplied Fly 1.3.1 passed a LIMITED provider cohort: 463 tests, one source-routing deselection, 6.08 seconds. All three origins are inside the owned prefix; no native provider loaded. Preserve failed attempts: missing Fly during collection (the compatibility wheel does not bundle the 50 Extensions), normal Fly resolution because Echopy is absent from the registry, and two test-helper import errors. Supplying Fly with --no-deps only in this prefix and correcting the existing test/tool helper paths established the bounded result; no source correction or complete provider closure follows. The installer already declared Fly, so this is not a missing-dependency defect.

Workspace PLUGMIX-COMPAT-RELEASE-REVIEW.md explicitly APPROVEs published assets and LIMITED prefix runtime evidence. T16 alone is complete; all 52 IDs, 51 unfinished families and 17 JSON rows remain unchanged. T18/T28/global T29 and native acceptance remain open. Root install.sh and FontLab installation/native checks remain held; cleanup STOP and all existing exclusions, pauses and publication holds persist.

# Current round — verified source, main and CI delivery (2026-11-14)

## 2026-11-14 — App minimum-version correction ready for review

The v1.1.15 requirements accepted App 1.2.8, which lacks `fontlabapp.plugins`.
Direct App tag objects show the package first in 1.2.9; existing first-tag tests
retain the coordinate-writer floor at 1.2.10. Triage also reproduced the Reporter
import failure in 1.2.8 and success in 1.2.9/1.2.10; that import probe is a session
observation, separate from retained direct-source proof.

Set both App requirements to >=1.2.10 for the complete pack and exactly 45
non-filter manifest floors to 1.2.9. Keep the other five manifests unchanged.
Update installer test expectations and document the distinct core/writer floors.
The original three manifest tests pass. New regressions fail twice before the
metadata fix; all five focused cases then pass. The first full run found two
stale installer expectations (462 passed, two failed); after updating only their
expected strings, the complete `sh test.sh` passes 464 tests, zero skips in
6.51 seconds with all original coverage gates. Ruff 0.16.7 passes the full tree.
The local pack builder/checker and audit pass: 105 members, 50 manifests/classes,
exact source/legal bytes and unchanged runtime Python and shared installer.

Graph file and installer-test impacts report UNKNOWN/no resolved callers, not
closure. Literal/source checks and real pytest/installer cases corroborate the
metadata consumers. Independent review and controller graph analysis, ordinary
main/release gates and downloaded-artifact checks are next. No commit, push,
tag, user-folder installation or native operation ran in this implementation
lane. Global T18/T29, all native checks and existing holds remain open.

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

Updated AGENTS, PLAN and TODO to prioritize useful functional changes and compatible package boundaries, with detailed testing deferred. Existing backlog and prior records are retained. Documentation preservation and policy consistency were checked; no runtime, installed or native checks ran in this documentation-only pass.

Next: advance reporter/filter/palette fixes through shared App code and matching Fly/Extensions consumers, using focused callback checks before the full installed/native plugin pass.

## 2026-11-14 — Current-source release preparation

Transferred only the reviewed functional-priority insertions into the fresh
current-main successor, preserving every previous target byte. The distribution
triage records 105 current curated files/50 manifests versus historical v1.1.14's
103 members, missing LICENSE/NOTICE and older StepAndRepeat, ShowStems and
SpeedPunk modules. The builder repair is already reviewed and on main; this round
adds no source fix. App 1.2.18 is the accepted source peer. Controller source qualification passed the full maintained `sh test.sh`: 462
tests, zero skips, 8.03 seconds and all per-module 80% floors, including all 50
Extensions, the helper and startup snippet; overall coverage is 98%. Full-tree
Ruff 0.16.7 passes. The clean owned test environment verifies arm64 Python 3.11
and Qt 6.12.0 through its selected VIRTUAL_ENV; this is host-free evidence, not
another binding loaded into FontLab. The builder/checker and independent local
pack audit pass: 105 unique members with exact source bytes/modes, CRC and safe
paths, all 50 manifests/classes and exact legal bytes. Accepted App source peer
is 1.2.18. Normal main/tag gates, full CI and the published/downloaded ZIP,
wheel and sdist remain pending. Startup/helper source checks do not qualify
released artifacts or native execution. T16/T29, installation, native fences and the full backlog remain open.

The combined ZIP legal-file/preflight, documentation content-oracle and lint
repairs passed independent specification and quality review and reached
[main at 40cac692](https://github.com/fontlabcom/fontlab-python-plugmix/commit/40cac69290a5027f205ca2a0bee24239e04fc37b).
The delivered tree is `4315dc6ef4eac462be8a32892fd70e9afb408f60`, parent
`b874cf606a30ba3e99d0905522c5c8db6829c15c`. The exact 33-path reviewed delta
was pushed through the ordinary installed 310-byte pre-push hook. Actual
post-push and post-CI remote reads matched that commit.

Controller gates passed 462 source cases with unchanged coverage checkers,
38 complete locked docs cases, strict build, full-tree Ruff 0.16.7 with zero
diagnostics, 21 App-free workflow cases and genuine source-artifact checks.
Seven complete changed production modules meet the unchanged 80% combined
coverage requirement without exclusions. Their statement and branch results
are recorded separately; all seven meet 80% in each component. The bundle
checker retains its existing 80% line and branch rules. These results introduce
no new universal per-component threshold for the tools. The installed hook
reported `PASS (tests only)`: its compatibility-src selector found zero changed
production modules. Seven-module coverage comes from the separate full gates.

Exact-commit [Pack CI](https://github.com/fontlabcom/fontlab-python-plugmix/actions/runs/43527359696)
passed `pack`; [Documentation CI](https://github.com/fontlabcom/fontlab-python-plugmix/actions/runs/43527359690)
passed `build` and `qualify-generated-output`. The tag-only `release` job was
expected to skip on main. The downloaded CI ZIP has 105 unique members and
50 manifests, with every payload byte and Unix mode matching committed source,
including LICENSE/NOTICE. Its SHA-256 is
`40e0d9d73e0345a66893d6f064741bca0ad9b1795fd0202147011971b7b34066`.
This is CI-artifact qualification. The old v1.1.14 published asset is unchanged;
a new release/download, final-version artifacts and their cohort remain open.
Precommit source-artifact metadata does not qualify a postcommit release wheel.

Preservation is bounded. The four controller gate indexes matched exactly.
The canonical owner index, named administration, all 330 tracked-file identities,
refs and worktree attachments matched the retained baseline at precommit,
prestage, postpush and post-CI endpoints. These checks do not prove unrecorded
transient, global, untracked or ignored state. The earlier combined and docs
candidate index intervals remain FAILED, writer UNKNOWN. The controller setup
interval also remains FAILED/UNKNOWN: its index grew from 33,984 to 34,252 bytes
with an UNTR extension before the passing gates. No earlier index was restored.
Successful delivery does not relabel any failed preservation interval.

The four-document follow-up also passed 462 source cases, 38 locked docs cases,
strict build, zero Ruff diagnostics and the artifact checks. Its owned graph
result is LOW for four documentation files, with zero mapped affected processes;
this does not resolve prior dynamic UNKNOWN callers or graph limits. In that
follow-up's first full-gate interval, the owned App and Pens peer indexes gained
UNTR extensions (164,985 to 165,255 bytes and 5,678 to 5,949 bytes). Both raw
intervals are FAILED, writers UNKNOWN; both endpoints are retained and neither
index was restored. The source and Fly indexes stayed exact. These new failures
are separate from the earlier controller gate's four exact indexes and from
the unchanged canonical-owner endpoint.

This follow-up removes only the two solved combined-review and controller
main/hook/remote-CI TODO rows. Independent review of this four-document residual
and controller delivery remain separate. P01 new-release/download, P04 provider
admission, P05 graph gaps, root install.sh, installed origins/RECORD, all 17
native rows, GUI controls/both themes, fonts/history/reopen and typing latency
remain open. No root installer, user-folder installation or native operation
was run for this source delivery. Issue 123 remains paused, private Pages held,
excluded repositories untouched and the separate release lane unchanged.

The dated candidate and release records below retain their exact prior bytes.
Their pending-review/delivery wording describes those earlier checkpoints;
the verified source/main/CI closure above supersedes only that bounded status.

## Prior candidate record — 2026-11-13 (retained verbatim)

# Current candidate — combined ZIP, documentation and lint fixes

The independently reviewed ZIP legal-file and required-input preflight repairs
and documentation content-oracle repair are composed on current main. The ZIP
contains exact LICENSE and NOTICE bytes, 105 members and 50 manifests. Required
missing, directory and unreadable inputs preserve a prior ZIP's bytes and mode;
missing inputs leave absent output absent. The docs comparison uses an explicit
worktree/index patch, retaining all five real-Git states and original hashes,
epochs, 58-file counts and output-parity assertions.

The 45 remaining Ruff findings are repaired under the existing policy. Startup
keeps its broad exception catch, explicit print text and continuation. Normal
non-DEBUG output stays unchanged. A named DEBUG record uses existing logging
configuration. Enabled handlers may emit its traceback to their configured
destination (including stdout) or raise. getLogger may register the name; no
root logger configuration, level or handler is changed. The caplog regressions
qualify only their tested named-logger configuration. The README example executes its exact extracted payload
through a temporary UTF-8 file and runpy; this is not a sandbox. Adjacent-pair
changes retain RGB strict zip and the three-point second derivative. The
ProperDocs side-effect import remains before configuration loading.

Current checks: 462 source cases (all original 456 plus six regressions), the
unchanged compatibility/bundle/startup coverage gates, all 38 locked Python 3.13
docs cases, strict build, Ruff 0.16.7 full tree, App-free CI and actual pack
build/check pass. The seven complete changed production modules meet the
unchanged 80% statement, branch and combined floors, with no new exclusions.
The docs hook measures 38/38 statements and 22/22 branches. All original source
assertions, case order, decorators and skips remain. Under controlled inputs,
102 unaffected ZIP members retain exact bytes/modes/timestamps; repeated output
is byte-identical. Only three bundled Python files change.

Preservation exception: the owned source index gained an UNTR extension from
33,984 to 34,250 bytes between captured composition and pre-gate checkpoints.
Its writer is unknown and that raw-index interval failed. No old index was
restored. The final gate interval and owned peer captures are exact. Graph
analysis maps three affected compute flows at MEDIUM risk and retains UNKNOWN
dynamic callers, overflow, untraced entries and budget cuts. Passing source tests
cover the changed numerical paths; graph closure remains unproved.

Next: independent whole-change review and controller qualification, fresh-main
reconciliation, ordinary hooks, remote SHA and exact-source CI, then separate
release/download verification. No commit, push, release, root install.sh,
user-folder installation or native operation was performed in this candidate.
Provider admission, graph limits, all 17 native rows, GUI controls/both themes,
font/history/reopen/typing checks, private Pages and paused Issue 123 remain open.
The prior verified release record follows unchanged.

# Current round — Issue 255 post-release reconciliation

## 2026-11-14 — Functional work order documented

Updated AGENTS, PLAN and TODO to prioritize useful functional changes and compatible package boundaries, with detailed testing deferred. Existing backlog and prior records are retained. Documentation preservation and policy consistency were checked; no runtime, installed or native checks ran in this documentation-only pass.

Next: advance reporter/filter/palette fixes through shared App code and matching Fly/Extensions consumers, using focused callback checks before the full installed/native plugin pass.

[fontlab-python-plugmix v1.1.14](https://github.com/fontlabcom/fontlab-python-plugmix/releases/tag/v1.1.14) is qualified at `13e7d9182b39417378bfcd07e7e46e9707e64e39`.

All 51 authored consumers use Fly. The bounded sdist selection repair excludes operational session data and the compiled installer while preserving product and legal source.

438 source tests, 53 complete changed-module gates and 37 documentation tests pass. Genuine wheel/sdist ordinary cohorts each pass 244 checks with one explicitly source-only routing deselection; source covers that case. The downloaded Extensions ZIP contains the exact 103 reviewed member names/bytes for 50 plugins. Normal main/tag hooks, CI and actual wheel/sdist/ZIP downloads are qualified.

The source, artifact, ordinary external-install, release and download gates above are verified. This round reconciles their progress records after release; it changes no runtime source, installer, dependency declaration, generated documentation or immutable release asset.

Remaining: After explicit D43 recovery and admission, qualify App startup, palette and all original plugin behaviors on the released installed Fly/provider tuple; keep legacy compatibility and native lifecycle/history acceptance separate.

D43 native acceptance remains held and unproved. Issue 123 remains paused; existing private Pages holds and every unrelated acceptance task remain in PLAN/TODO. Prior WORK bytes are retained exactly in the private external delivery ledger, SHA256 `9ebaa7eb720b28d3ae79a1a664328c527066c0dee9c857b81046012b45023b10`.

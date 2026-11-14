---
this_file: WORK.md
---

# Current round — verified source, main and CI delivery (2026-11-14)

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

[fontlab-python-plugmix v1.1.14](https://github.com/fontlabcom/fontlab-python-plugmix/releases/tag/v1.1.14) is qualified at `13e7d9182b39417378bfcd07e7e46e9707e64e39`.

All 51 authored consumers use Fly. The bounded sdist selection repair excludes operational session data and the compiled installer while preserving product and legal source.

438 source tests, 53 complete changed-module gates and 37 documentation tests pass. Genuine wheel/sdist ordinary cohorts each pass 244 checks with one explicitly source-only routing deselection; source covers that case. The downloaded Extensions ZIP contains the exact 103 reviewed member names/bytes for 50 plugins. Normal main/tag hooks, CI and actual wheel/sdist/ZIP downloads are qualified.

The source, artifact, ordinary external-install, release and download gates above are verified. This round reconciles their progress records after release; it changes no runtime source, installer, dependency declaration, generated documentation or immutable release asset.

Remaining: After explicit D43 recovery and admission, qualify App startup, palette and all original plugin behaviors on the released installed Fly/provider tuple; keep legacy compatibility and native lifecycle/history acceptance separate.

D43 native acceptance remains held and unproved. Issue 123 remains paused; existing private Pages holds and every unrelated acceptance task remain in PLAN/TODO. Prior WORK bytes are retained exactly in the private external delivery ledger, SHA256 `9ebaa7eb720b28d3ae79a1a664328c527066c0dee9c857b81046012b45023b10`.

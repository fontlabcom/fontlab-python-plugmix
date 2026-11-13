---
this_file: WORK.md
---

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

---
this_file: PLAN.md
---

# Forward plan

Issue 123 remains paused. The additive recovery retains App-based scripts and
the remote compatibility package together. Further consolidation remains a
separate reviewed product milestone.

## Issue 210 remaining acceptance

The reference pack now contains 50 manifest bundles under Extensions and a
single action script that opens App's Reporters palette. The original plugin
behavior is retained; framework and host operations remain in App. The bundle
format is documented in Extensions/README.md. Qualify the exact paired artifacts
and native UI, startup, drawing, callbacks, teardown and writer history after
independent source review. The 50 bundles install through `install.vfpy` (Issue 254); native acceptance is still open and tracked in TODO.

Issue 211's nine native probes and four minor fixes remain follow-up work.
The README's dated native observations do not close those integrated checks.
Before removing retained `fontlab_plugmix`, audit all consumers, entry-point
groups, distributions, startup paths, preferences and attribution. Preserve
complete recoverable source and qualify the actual replacement. The recovered
App-based script entry points alone do not finish this consolidation.

## Development checks

The retained compatibility package descends from
`dddadcd9bc8cee21d5f7b8fe60027495e13fd41a`; Extensions use App separately.
`src/fontlab_plugmix/` contains the package. `tests/`, `test.sh` and
`tests/check_coverage.py` provide its own offline suite and coverage check.
Use an arm64 Python 3.11 process and the owned sibling App source:

```sh
PLUGMIX_FONTLABAPP_SOURCE="$PWD/../fontlab-fontlabapp" sh test.sh
```

Requalify all 50 bundle modules and the remaining action script against the actual
App dependency with the full suite and its configured line/branch coverage.
The pack gate requires at least 80% line and 80% branch coverage per module;
the retained compatibility package gate also remains active. Keep the sibling App source needed
by the runner-layout test; set `UV_PYTHON_PREFERENCE=only-system` and verify arm64.
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

Follow [AGENTS.md](AGENTS.md) for reviewed milestone commits/pushes, `main`
integration and recovery-first cleanup. Keep native, installation, generated
reference and publication gates separate.

## Documentation delivery gates

Obtain independent review of the complete source and generated site, preserve
current source bytes, then qualify exact-SHA main Actions through the ordinary
reviewed delivery process. Exercise changed-output bot-child and code-only live
triggers separately. Private Pages publication remains owner-held.

## Issue 234 part 1 — C8 remaining acceptance

Qualify the four coordinate-only outline filters and three interactive tools in
FontLab 9 using the coordinated App writer. Verify dialogs, toolbar registration,
modifiers, zoom hit testing, local/component scope, current-master safeguards,
Undo/Redo and saved/reopened results. Preserve native curve kinds; no snapshot
reconstruction or implicit component decomposition is part of this milestone.

Assign the four filter manifests the actual first compatible App release before
distribution. Their current 1.0.0 minimum follows the pack convention but cannot
distinguish the older deletion-only writer. Installation, release and native
acceptance remain orchestrator work; this lane must not commit or publish.


## Issue 255 remaining qualification

The Fly consumer source milestone is delivered at 05176d30 with successful CI.
Independently review and deliver the bounded sdist selection repair through the
retained main/pre-push/CI gates, preserving earlier local tags and artifacts; verify
new remote delivery separately. Independent specification/quality review, full source and
coverage gates, scoped graph analysis and locked docs build/tests are complete for
the reviewed candidate; they do not establish remote delivery.

Qualify genuine pack/wheel/sdist artifacts with Fly >=1.3.0 and the reviewed
provider tuple while retaining the separate legacy compatibility contract. Native
startup, palette and plugin behavior remain separate acceptance on the released,
installed tuple. Private Pages remains held.

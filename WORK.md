---
this_file: WORK.md
---

# Work

Status (2026-11-13): Issue 255 source candidate migrates all 50 bundles, Show
Reporters and the optional startup snippet through Fly. Full arm64 CPython 3.11
suite after review fixes: 437 passed; all original coverage gates pass, plus startup and the changed
checker at 100% statements/branches. All 51 bundle/action diffs change import
prefixes only. Runtime identities, README reporter discovery, isolated exact-source
Fly routing, startup success/failure and runner source selection are tested.
Earlier lint used `/opt/homebrew/bin/ruff` 0.14.10 with default selectors on
the changed consumer/test paths; that limited pass did not cover the controller's
broader Ruff 0.16.7 selector set. The two new I001 import-order findings in
`tests/test_install_bundles.py` and `tests/test_test_script.py` are corrected;
Ruff 0.16.7 `--select I001` passes on those two files. Existing StepAndRepeat I001,
ShowStems/SpeedPunk RUF007, startup BLE001, coverage-test I001 and installer
FURB192 findings remain baseline disclosures, not a blanket lint pass.
Shell syntax passes. Shellcheck reports only
the two unchanged SC1007 lines. Compatibility source, manifests, frozen audit,
licences and shared installers remain exact. The controller rebuilt generated
outputs with the exact documentation lock; strict build and all 37 docs tests pass.
Independent specification and quality reviews pass after the bounded review fixes.
Main/pre-push/CI integration, genuine artifact/release qualification and native
acceptance remain open; source tests use fake hosts and do not qualify FontLab
behavior.

The earlier log (2,969 bytes, sha256 `9394b88f870b035b10ca4a6786631c684e650783900df95717561ddc9dc6a61a`) is archived on the owner's workspace data volume (not public) under `issue250/review/d46-work-archive/`.


Review round 1: the pack-only installer dependency table now requests
`fontlab-fly>=1.3.0`; the library dependency remains App-only. A regression runs
the actual installer and checks its forwarded uv requirements with PYTHONPATH
removed. Bundle gate tests independently isolate bad bundle evidence from the
healthy startup record, with separate startup threshold tests. Bounded checks:
25 passed; full no-selector source checks: 437 passed, all gates retained.


Controller qualification: the full suite independently passes 437 tests. The 53
complete changed modules have minimum statement coverage 93.1034% and branch
coverage 81.25%, with zero exclusions. Fresh origin/main remains at d58fd0a with
zero commits on either side. Scoped graph change analysis reports 73 files,
23 symbols, zero processes and LOW risk; the truncated symbol list is corroborated
by exact source comparisons and tests. Reviewed source/docs are ready for ordinary
integration gates; no remote delivery, artifact or native acceptance is claimed.

The documentation requirements lock SHA-256 is `961b3ec6b8ffde319473d3c17325d1699915c236a657a91baef77b5527215070`.


Final import-order fix: bounded installer/runner tests pass 14 cases; full
no-selector suite passes 437 tests in 6.87s with all coverage gates. Only the two
reviewed test import blocks changed. No consumer, product or shared-installer code
changed; baseline lint findings remain preserved.

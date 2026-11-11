---
this_file: WORK.md
---

# Work in progress

Earlier WORK.md (12,441 bytes, SHA256 `5698c293121964253ee1df6ddfcaab192f954c83b7de11032a56e582b95d36bc`) is archived on the owner's workspace data volume (not public) under `issue250/work-archives/` (Issue 250). Completed work is in CHANGELOG.md; open work is in TODO.md and PLAN.md.


## Issue 210 current round

Implemented 43 manifest bundles and one Show Reporters action. The compatibility
package and original behavior assertions remain intact. Full direct source suite:
353 passed on arm64 Python 3.11.18; 51 compatibility modules plus 43 bundles and
one script pass their coverage gate; Ruff 0.14.10 F821 passes. The exact wrapper
baseline failed during PyPI DNS resolution. See ISSUE210-PACK-REPORT.md for
commands, complete per-module coverage and native-only checks. Paired
independent source review approved; no native, installation, artifact or delivery claim.

## Issue 210 documentation repair checks

The website now describes Extensions and the Show Reporters action; all 39
reporter descriptions are retained. Source/generated NOTICE matches root;
LICENSE already matches. Strict `sh src_docs/build.sh` and
`python -m unittest discover -s tests_docs -v` pass (36 tests), using an existing
external Python 3.13 environment with all 31 lockfile versions checked.
A new external Python 3.12 venv was created, but its `uv pip install
--require-hashes -r src_docs/requirements.txt` failed at PyPI DNS resolution.
`PYTHONPATH=src:../fontlab-fontlabapp/src python -m pytest -q tests` passes
(353 tests, existing Python 3.11 environment). No runtime source changed.
Generated HTML retains the theme's whitespace-only lines. Native checks,
installation and remote delivery were excluded from this round.

## C8 current round

Implemented seven practical bundles, manifest/discovery fixtures and dedicated
documentation. Full Plugmix direct-source suite, no-selector test.sh and the
exact metaswarm recipe pass 397 tests; strict docs build and 37 docs tests pass.
All changed Plugmix Python files pass full Ruff; all new modules have 100% line
and branch coverage. Independent Plugmix and App writer reviews approved after
fixing secondary-button release and valid coordinate-collision regressions.

The App change is necessary because Filter LayerEdit contours were accepted by
the public contract but rejected by the deletion-only writer. Only that writer
and affected test fixtures changed. Focused App tests pass 53 cases with 100% line
and branch coverage. The full App gate passes 12,358 tests with 22 retained skips and 107 warnings
after updating catalogue fixtures and using the prescribed local-source
installation for isolated subprocess origin checks. Exact commands and results
are in C8-REPORT.md. Native and installed-pair checks remain open in TODO.

No commits, pushes, branch changes or native operations. All remaining work is
acceptance/release qualification, not placeholder implementation.

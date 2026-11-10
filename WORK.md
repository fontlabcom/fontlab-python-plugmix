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

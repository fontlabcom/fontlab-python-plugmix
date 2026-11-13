---
this_file: WORK.md
---

# Work

Issue 255 artifact selection repair (2026-11-13): the prior source milestone was
delivered at 05176d30 with successful CI. Fresh source-distribution qualification
then found operational session data and a compiled installer containing local
paths in Hatch's default archive. The retained local v1.1.13 tag and existing
artifacts are unchanged.

The sdist target now excludes only root `/.omc` and `/install.vfpyc` using Hatch's
Git-style patterns. These files remain intact in the checkout. Library, userpack,
legal, documentation and test source selection otherwise stays unchanged; wheel
and pack configuration are unaffected. No shared installer code changed.

A genuine fresh uv sdist regression fails before the selection fix, then passes:
it rejects operational/compiled members and verifies exact representative
library, Extensions, Scripts, docs, tests, legal and source-installer bytes.
Bounded packaging checks pass 7 tests; full arm64 Python 3.11 no-selector checks
pass 438 tests and all existing coverage gates. Pinned Ruff 0.16.7 I001 passes
only the changed packaging test file; previously disclosed baseline lint findings
remain. Diff whitespace check passes.

Independent review, ordinary delivery of this repair, new genuine release
artifacts/installation and separate native acceptance remain open. No release,
private Pages, tag mutation or host action is claimed.

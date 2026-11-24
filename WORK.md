---
this_file: WORK.md
---

## Current state

The fly-january branch includes the owner’s Instamix 1.0.18 installer and the
0.2.1 site theme at merge `436f29e`. On that source, the strict docs build
passed and both package runs passed all 459 tests. Of the 24 documentation
tests run, 23 passed. The frontend test expects theme 0.1.1. The 15 Git fixture
tests were unrun.

The housekeeping check verified the v1.1.19 and v1.1.23 GitHub release archives
against their tags and the v1.1.23 PyPI wheel and sdist hashes. The existing
`release.yml` publishes through OIDC. Shell syntax, workflow lint and all 21 App-free pack and coverage tests passed.
See TODO.md for the remaining installed-provider, native, CI and docs checks.

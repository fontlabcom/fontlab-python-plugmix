<!-- this_file: AGENTS.md -->
# Repository instructions

- Keep glyph geometry and metrics reads in `snapshot.py`, canvas painter access
  in `backend.py`, and startup imports in `boot.py`.
- Keep reporter `compute()` methods pure and independent of FontLab.
- Never let an exception escape a paint callback or Qt signal callback.
- Use `fontlabapp` for overlay and QAction ownership; do not duplicate its
  viewport polling or teardown code.
- Do not write font data. The only preference write is the plugmix JSON file.
- Run `./test.sh` and inspect its per-module coverage check before reporting
  completion. Native FontLab tests must be performed by a host-equipped user.

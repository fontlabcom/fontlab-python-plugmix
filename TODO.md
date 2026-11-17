---
this_file: TODO.md
---

## Next steps (prioritised, 2026-11-17)

1. P0 advance reporter/filter/palette fixes through shared App code and Fly/Extensions consumers.
2. P1 Issue 256: joint App+Plugmix deploy of the lowercase 50-bundle pack; native checks in FontLab 9, in order: install App then Plugmix and confirm 50 bundles; Reporters palette/View sync; toolbar and Tools registration; Window > Panels lifetime; Extensions discovery; reporter drawing modes; outline dialogs; Measurement Ruler; Node Probe; Contour Picker; Step and Repeat (owner-run).
3. P2 Issue 211 nine native probes and four minor fixes; shim removal gate (outside-consumer search or deprecation).
4. P2 CI full-suite read-only App/Pens checkout (owner-gated; end of file).

- [ ] Issue 256: reconcile and deliver the reviewed lowercase Plugmix pack through normal hooks and release/artifact checks; resolve App 1.2.31 PyPI publisher administration, then qualify the installed provider cohort and native/Windows migration separately.

# Open tasks

- [ ] Advance reporter/filter/palette fixes through shared App code and matching Fly/Extensions consumers, using focused callback checks before the full installed/native plugin pass.

- [ ] Issue 255: After explicit D43 recovery and admission, qualify App startup, palette and all original plugin behaviors on the released installed Fly/provider tuple; keep legacy compatibility and native lifecycle/history acceptance separate.

- [ ] native (owner, Issue 254): install the App `install.vfpy` (main at or after 5cac0d6), then this repository's `install.vfpy`, restart FontLab 9 and confirm Plugmix Demo lists 50 bundles (39 reporters, 5 filters, 4 tools, 1 palette, 1 general). Run one filter on an owned copy, check one history row, Undo/Redo, and that the install persists across a restart. Then uninstall and confirm the links go.
- [ ] native: verify Reporters palette toggles and View > Reporters synchronization in FontLab 9.
- [ ] native: verify toolbar and Tools > Tool registration, selection and teardown in FontLab 9.
- [ ] native: verify Window > Panels registration, show/close and PythonQt lifetime in FontLab 9.
- [ ] native: verify Extensions startup discovery and marked-hook install/removal on the exact installed tuple in FontLab 9.
- [ ] native: verify all reporter drawing modes, callback failure containment and teardown in FontLab 9.
- [ ] native (owner-run): Step and Repeat from a real Glyph window. `snapshot.active_glyph` needs a Glyph-window canvas, so without a stub `repeat_selected` refuses "No active glyph." (nothing written); the rest was verified with the lookup stubbed (A2 report 21).

- [ ] Complete Issue 211 nine native probes and four minor fixes on the exact integrated tuple under the separate native gates.
- [ ] Compatibility-package and `fontlabapp.plugmix` shim removal gate: the workspace audit is done (see the Consumer audit page); next check is an outside-consumer search or a deprecation period, because third-party entry-point publishers and owner-installed copies cannot be known from the workspace.
- [ ] Qualify native App-based script activation/rendering on the exact recovered tuple under the separate native gates.
- [ ] After qualified integration and recovery, remove only proven obsolete items without unique or attached owner work. Compatibility-package removal also needs the outside-consumer search or deprecation period above.

- [ ] native: verify Round Outline to Grid, Move Outlines, Scale Outlines and Slant Outlines dialogs, current-master scope, refusal of unsafe shapes, one Undo/Redo step and saved/reopened outlines in FontLab 9 with the coordinated App writer.
- [ ] native: verify Measurement Ruler left drag, Shift constraint, Escape, secondary-button release, glyph switching and teardown in FontLab 9.
- [ ] native: verify Node Probe local/component labels and 12-pixel hit radius at multiple zoom levels in FontLab 9.
- [ ] native: verify Contour Picker whole-contour selection and Shift toggle on open/cubic/quadratic outlines, with components unchanged, in FontLab 9.

## Deprioritised test-infrastructure rows

- [ ] CI test suite: the full suite needs a read-only App/Pens checkout in CI (tag-floor and bundle tests), owner-gated (credential: deploy key, PAT or App visibility). `tests/conftest.py:42` (`pytest_configure` imports `fontlabapp.plugins.bundles`) and `tests/extensions/conftest.py` block every module under it; `pack.yml` runs only the App-free subset with `--noconftest` (`tests/test_pack_workflow.py`, `tests/test_extension_coverage_gate.py`).

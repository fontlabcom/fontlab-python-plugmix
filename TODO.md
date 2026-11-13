---
this_file: TODO.md
---

# Open tasks

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
- [ ] Obtain independent review of the additive recovery, qualify its ordinary gates, verify the remote SHA and integrate into `main`.
- [ ] After qualified integration and recovery, remove only proven obsolete items without unique or attached owner work. Compatibility-package removal also needs the outside-consumer search or deprecation period above.

- [ ] Independently review the complete Issue 233 site and qualify exact-SHA main Actions, changed-output bot-child and code-only triggers; private Pages stays owner-held.

- [ ] native: verify Round Outline to Grid, Move Outlines, Scale Outlines and Slant Outlines dialogs, current-master scope, refusal of unsafe shapes, one Undo/Redo step and saved/reopened outlines in FontLab 9 with the coordinated App writer.
- [ ] native: verify Measurement Ruler left drag, Shift constraint, Escape, secondary-button release, glyph switching and teardown in FontLab 9.
- [ ] native: verify Node Probe local/component labels and 12-pixel hit radius at multiple zoom levels in FontLab 9.
- [ ] native: verify Contour Picker whole-contour selection and Shift toggle on open/cubic/quadratic outlines, with components unchanged, in FontLab 9.
- [ ] Confirm the first `v*` tag push runs the `release` job in `.github/workflows/pack.yml` and attaches `fontlab-python-plugmix-extensions.zip` to that release (the job exists and its workflow shape is tested, but no tag has been pushed since it was added; actionlint-clean only).
- [ ] CI test suite: the full suite needs a read-only App/Pens checkout in CI (tag-floor and bundle tests), owner-gated (credential: deploy key, PAT or App visibility). `tests/conftest.py:42` (`pytest_configure` imports `fontlabapp.plugins.bundles`) and `tests/extensions/conftest.py` block every module under it; `pack.yml` runs only the App-free subset with `--noconftest` (`tests/test_pack_workflow.py`, `tests/test_extension_coverage_gate.py`).

- [ ] Issue 255: independently review and deliver the bounded sdist selection repair through ordinary main/pre-push/CI gates; retain prior local tags/artifacts and verify its remote SHA.
- [ ] Issue 255: qualify genuine pack/wheel/sdist installation with Fly >=1.3.0 and the reviewed provider cohort; separately verify App startup and plugin behavior in FontLab under the serialized native gate.

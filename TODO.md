---
this_file: TODO.md
---

# Open tasks

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
- [ ] Build the Extensions pack zip (tools/build_pack.py) in CI or the release job and attach it to releases; the local build and tests exist, but no workflow runs them.

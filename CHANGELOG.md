---
this_file: CHANGELOG.md
---

## 2026-11-05 — Full source recipe qualification

Corrected the six-guide handoff to the retained 21:46:13 UTC full-run
receipt: no selectors, exit 0, 125 passes and full per-module checker,
Plugmix `dddadcd9bc8cee21d5f7b8fe60027495e13fd41a` with owned App
`fb6a93776772b996b25604f88711feb300b90109`. The 96% overall result is
line coverage; the 80% combined-module policy is unchanged. The earlier
installed-hook baseline remains historical evidence. Future tuple changes
require requalification; ordinary hooks, native and installed-artifact
acceptance remain separate. No additional product test was run for this
prose correction. Source, tests and policy files are unchanged.

## 2026-11-05 — Issue 230 remote documentation variant

Prepared six source-specific root guides for the package at
`dddadcd9bc8cee21d5f7b8fe60027495e13fd41a`. Retained existing README usage
and CHANGELOG history. Clarified the complete no-selector check, reporter
restrictions, undoable Filter/Palette edits and future Issue 210 architecture.
Checked guide structure and preservation hashes. No product test, native,
installation, canonical migration or remote-delivery result is claimed.

<!-- this_file: CHANGELOG.md -->
# Changelog

## Unreleased

- Refuse Step and Repeat on a displayed non-master layer and when the contour
  count changes before Undo. Honor owned panel close refusal and retry without
  losing the dock or its checked Window action. Test against the sibling
  fontlabapp worktree, preserve reporter state on failed disable saves, and
  suppress General font-open events after a failed initial read.
- Read General shortcuts through PythonQt's QAction property and compare
  normalized QKeySequences before assignment. Use `fgId` for font identity
  in General events, active-glyph checks and palette keys. Map a tool's first
  key event from the live cursor instead of viewport origin.
- Add native Tool registration with guarded event mapping, active-only mark
  painting and a selection-only Smart Select port. Add General menu commands,
  font-opened/closed polling on the palette timer, owned timers and actions,
  and Zoom to Selection. Save explicit Tool and General enable choices without
  changing old preference files.
- Resolve dock close filters through FontLab's `PythonQt.private.QObject` and
  keep palette Show working if close detection is unavailable. The Window
  toggle remains the explicit close control in that case.
- Keep tabbed and temporarily hidden palettes alive; only dock Close or the
  Window toggle changes their saved visibility. Resolve active glyphs through
  the workspace canvas, report failing captures once per key, and show palette
  Apply errors in its status label. Refuse zero-offset repeats.
- Add the dockable Palette kind, persistent Window toggles, a shared refresh
  timer, and Step and Repeat contour duplication through one geometry Undo step.
- Reuse outline safety checks and the layer writer for palette edits. Keep
  palettes out of Reporter and Filter menus; restore old preferences unchanged.
- Measure Delete Small Paths over flattened curves; preserve newly discovered
  filters when no filter choice was saved. Keep Apply working when saving its
  parameters fails, and skip unsafe glyphs individually.
- Restore polygon painter state with save/restore, and handle oversized stored
  numeric parameters by falling back to defaults.
- Added a shared `Plugin` identity and kind-filtered discovery. Reporter View
  actions remain reporter-only; the same entry-point group discovers Filters.
- Added `enabled_filters` and validated last-used `params` preferences while
  retaining old `enabled` files and unknown keys.
- Added a pure Filter contract, owned parameter dialog, deletion-only native
  writer through `outline_writer` and `layer_writer`, and Delete Small Paths.
- Reset polygon pen and brush after fill, ignore degenerate polygons, and
  cover empty contours and missing zones in existing reporters.
- Added twelve reporters for handle geometry, crosshairs, extrema, segment
  lengths, selected handles, anchors, sidebearings, unit grids, zone proximity,
  italic alignment, smooth-node angles and Glyph Focus.
- Use the native UPM for Unitizer spacing and normalize italic angle to a
  positive rightward slant in snapshots. Add filled polygon marks and tighten
  selected-segment and zero-length handle checks.
- Added immutable contour closure and smooth flags, selected-master zones and
  opt-in native ink bounds to reporter snapshots.
- Stop retrying a native canvas id after painter attachment fails; isolate
  registry teardown errors and preserve the original preference-save error.
- Harden native painter teardown against stale canvases and failed removal;
  suppress any callback left registered after a reporter is disabled.
- Keep startup working when preferences or a third-party plugin are broken,
  and roll back an overlay if its enabled state cannot be saved.
- Rename Nodes Outside Paths to Off-curve Handles Outside Bounds, migrating
  its saved enabled name. Clarify active-window attachment and snapshot cost.
- Let `test.sh` explain missing source checkouts and accept partial test runs.
- Stop querying canvas zoom during native painting when the value is unused.
- Prefer native per-canvas Python painters when present, with foreground and
  background ordering, multi-canvas attachment and EditorPainters fallback.
- Show full contour indexes on both on-curve and off-curve nodes.
- Make `./test.sh` discover the canonical sibling `fontlab-fontlabapp` checkout.
- Added Python 3.11 package, lazy native boot, reporter discovery, persistent
  View-menu toggles and immutable glyph snapshots.
- Added seven built-in reporter overlays and two FontLab menu scripts.
- Added pure and fake-native tests with per-module coverage enforcement.

## 2026-11-06 — Additive App script recovery

Recovered 38 missing reporter launchers and the two existing menu/report scripts
from the retained pre-pull product, byte-exact. Scripts use App
`fontlabapp.plugmix`; the separate `fontlab_plugmix` compatibility package, tests,
startup snippet, dependency metadata, NOTICE and licences remain. The guides now
distinguish both runtimes and retain future consolidation/framework/native tasks.
Do not combine their installers in one FontLab session.

Added 41 host-free recovery cases that execute all forty scripts against real
App discovery, boot, registry and menus with existing fake host owners and owned
preferences. They check repeated activation, painter registration, menu disable,
unknown preference preservation, handle-size setup and save-failure rollback.
The red run reproduced missing paths and wrong-runtime entry points. The exact
arm64 Python 3.11 full recipe then passed 166 tests and the existing 51-module
checker; explicit branch coverage measured all forty complete script modules
at 100% (122 statements, no branches). The unchanged per-module 80% combined
gate remains. No production package source, test oracle, coverage selector or
exclusion changed. Source checksums are provenance, not functional tests.

Independent review, the normal installed pre-push gate, commit/default delivery,
canonical adoption, native FontLab behavior and publication remain separate.
No owner installation or native operation was performed.

<!-- this_file: CHANGELOG.md -->
# Changelog

## Unreleased

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

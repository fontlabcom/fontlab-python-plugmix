<!-- this_file: CHANGELOG.md -->
# Changelog

## Unreleased

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

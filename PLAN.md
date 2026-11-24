---
this_file: PLAN.md
---

## Functional work order

Prioritize visible reporter, filter and palette defects. Keep fixes in the shared
App core and carry them through the affected Fly and Extensions consumers.
App owns discovery, registration, native callbacks and teardown. Plugmix owns
the concrete bundles. Keep the compatibility package and its preferences usable.
Check the affected callbacks and package boundaries before the full native pass.

## Installer and provider qualification

For Issues 254, 255, 256 and 271, confirm the independent installer review and
normal hook results for the shipped revisions. Check the released App, Fly and
provider versions, installed origins and RECORD files, and each installer result.
App 1.2.31 is the minimum for lowercase bundles. Verify the selected release
against that floor. For the separate App 1.2.31 publication item, confirm with
the App owner whether that exact release still needs publishing. Its PyPI version
endpoint returns 404. Preserve owner files during legacy-bundle migration,
including modified or unowned bundles.

With D43 admission, use the serialized native lane to exercise the generated
installer on macOS and Windows. Run App's installer first, then Plugmix's.
Confirm that Plugmix Demo lists 39 reporters, five filters, four tools, one
palette and one General plugin. Exercise one filter, its history row and
Undo/Redo. The owner checks persistence across a restart and link removal
on uninstall. Keep native tests for the separate compatibility runtime on
their own run.

## Native plugin behavior

Qualify the 17 native rows on the released, installed provider tuple. Exercise
each GUI entry and its controls in both themes, whole-font history, saved
reopen and typing latency. Include these outstanding checks:

- **Startup and menus.** Verify Extensions discovery, marked hook installation
  and removal, Reporters palette and View > Reporters synchronization, toolbar
  and Tools > Tool registration, and Window > Panels show/close lifetime.
  Verify native reporter drawing modes, callback failure containment and
  teardown. Qualify App-based script activation and rendering separately on
  the recovered tuple.
- **Step and Repeat.** The owner runs it from a real Glyph window and checks
  selection, repeat and undo history using the actual active-glyph lookup.
- **Coordinate filters.** Exercise all four dialogs with the coordinated App
  writer. Check current-master scope, unsafe-shape refusal, one Undo/Redo step
  and saved/reopened outlines. Preserve native curve kinds and components.
- **Interactive tools.** Check Measurement Ruler drag, Shift, Escape, secondary
  release, glyph switching and teardown. Check Node Probe's local/component
  labels and 12-pixel hit radius at several zooms. Check Contour Picker's Shift
  toggle and whole-contour selection on open, cubic and quadratic contours.
- **Issue 211.** Run the nine native probes and qualify the four minor fixes on
  the integrated tuple. Issue 123 remains paused.

## Compatibility and cleanup

Before removing the compatibility package or the deprecated `fontlabapp.plugmix`
shim, search for consumers outside the audited workspace or complete a deprecation
period. Qualify the replacement, preserve recoverable source and attribution, and
check for unique or attached owner work before removing obsolete items.

## CI and documentation

Full-suite CI needs owner-approved read access to its App and Pens sources.
Run the repository recipe there with the required Fly source and verify the
bundle, startup and compatibility coverage gates. Keep the installed pre-push
hook and the existing per-module coverage floors.

Qualify the current fly-january site on its merged main SHA. Run the complete
locked documentation suite, check the installed-theme version assertion against
the 0.2.1 pin, and verify the generated output in the Documentation workflow.
Private Pages publication stays owner-held.

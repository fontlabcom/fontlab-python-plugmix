---
this_file: src_docs/md/plugins/node-probe.md
---

# Node Probe

Bundle: `Extensions/tools/NodeProbe.fontlabtool`  
Stable ID: `node_probe`

Inspect node placement without changing selection. Activate Node Probe from
Tools > Tool or the toolbar and hover within **12 view pixels** of a node.
The nearest node receives a ring and a label with its coordinates rounded to
two decimals, its on-curve/off-curve status and its indexed provenance.

Local labels include contour and node indices (`local 0:2`, for example).
Component labels also include the component index and base name. Indices start
at zero. Component coordinates come from App's decomposed snapshot and are
read-only; unavailable or skipped components cannot be inspected.

Use the label to distinguish a handle from an on-curve node, or to tell a local
outline from a component. Both kinds of node participate in hit testing. At an
equal distance, local nodes win over component nodes, then snapshot order wins.
The 12-pixel radius stays fixed as zoom changes; no usable scale means no hit.

No modifiers or parameter dialog are provided. The tool does not select,
move or reconstruct nodes, and it does not infer curve segments or distances
to a curve. A glyph/layer source change clears the previous hover label.

## Acceptance limits

Native toolbar placement, pointer/keyboard delivery, zoom mapping and teardown
remain unverified for the exact installed App/Plugmix tuple. Offline behavior
does not establish native acceptance. See [installation](../installation.md)
and the [Extensions catalogue](../app-menu-scripts.md).

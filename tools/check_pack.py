#!/usr/bin/env python3
# this_file: tools/check_pack.py
"""Check a built Extensions pack zip using only the standard library (no App checkout needed).

Usage: check_pack.py PACK_ZIP. Exits non-zero with a message when the zip is wrong.
"""

import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_BUNDLES = 50


def check_pack(zip_path: Path, root: Path = ROOT) -> list[str]:
    """Return the problems found in ``zip_path``; an empty list means the pack is sound."""
    wanted = sorted(row["bundle"] + "/plugin.json" for row in json.loads((root / "tests/bundle-map.json").read_text()))
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
    problems = []
    if len(wanted) != EXPECTED_BUNDLES:
        problems.append(f"bundle-map lists {len(wanted)} bundles, expected {EXPECTED_BUNDLES}")
    if sorted(n for n in names if n.endswith("/plugin.json")) != wanted:
        problems.append("zip plugin.json files differ from tests/bundle-map.json")
    for required in ("README.md", "LICENSE", "NOTICE", "Scripts/Plugmix/Show Reporters.py"):
        if required not in names:
            problems.append(f"missing {required}")
    problems += [f"bytecode in zip: {n}" for n in names if "__pycache__" in n or n.endswith(".pyc")]
    problems += [f"unexpected top-level entry: {n}" for n in names if not n.startswith(("Extensions/", "Scripts/")) and n not in {"README.md", "LICENSE", "NOTICE"}]
    return problems


if __name__ == "__main__":
    found = check_pack(Path(sys.argv[1]))
    print("\n".join(found) if found else "pack ok")
    sys.exit(1 if found else 0)

#!/usr/bin/env python3
# this_file: tools/build_pack.py
"""Build the Plugmix Extensions pack zip with its scripts, README and legal files.

The pack is copied into FontLab's user-data folder, never pip-installed, so it is
a separate artifact from the compatibility wheel. Usage: build_pack.py [OUT_DIR].
"""

import stat
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK_NAME = "fontlab-python-plugmix-extensions.zip"
SKIP_PARTS = {"__pycache__"}


def build_pack(root: Path, out_dir: Path) -> Path:
    """Zip the pack found under ``root`` into ``out_dir`` and return the zip path."""
    extensions = root / "Extensions"
    if not extensions.is_dir():
        raise FileNotFoundError(f"Extensions pack not found: {extensions}")
    required = [root / name for name in ("README.md", "LICENSE", "NOTICE")]
    for path in required:
        if not stat.S_ISREG(path.stat().st_mode):
            raise ValueError(f"Required pack input is not a regular file: {path}")
        path.read_bytes()
    files = [
        path
        for top in (extensions, root / "Scripts" / "Plugmix")
        for path in sorted(top.rglob("*"))
        if path.is_file() and not SKIP_PARTS & set(path.parts) and path.suffix != ".pyc"
    ]
    files.extend(required)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / PACK_NAME
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, path.relative_to(root).as_posix())
    return target


if __name__ == "__main__":
    print(build_pack(ROOT, Path(sys.argv[1] if len(sys.argv) > 1 else "dist")))

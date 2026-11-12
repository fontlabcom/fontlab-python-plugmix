# this_file: tests/test_licence_notices.py
"""NOTICE keeps the upstream MIT copyright and licence text for the two credited MIT sources."""
from pathlib import Path

NOTICE = (Path(__file__).resolve().parents[1] / "NOTICE").read_text(encoding="utf-8")


def test_notice_when_mit_sources_credited_then_upstream_copyright_and_terms_retained():
    for holder in ("Copyright (c) 2019 Olli Meier", "Copyright (c) 2026 TzuYuan Yin"):
        tail = NOTICE[NOTICE.index(holder):]
        assert "Permission is hereby granted, free of charge" in tail[:400], holder


def test_plugmix_sources_when_checked_then_no_mit_spdx_header_remains():
    root = Path(__file__).resolve().parents[1]
    for path in list((root / "src").rglob("*.py")) + list((root / "Extensions").rglob("*.py")):
        assert "SPDX-License-Identifier: MIT" not in path.read_text(encoding="utf-8"), path

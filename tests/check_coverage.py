# this_file: tests/check_coverage.py
"""Fail if any production module has less than 80 percent line coverage."""

import json
import sys
from pathlib import Path


def main(path: str) -> int:
    """Print every module's line rate and return a failing exit code if low."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    failures = []
    for source in sorted(Path("src/fontlab_plugmix").rglob("*.py")):
        name = source.as_posix()
        record = data["files"].get(name)
        if record is None:
            failures.append(name)
            print(f"{name}: missing from coverage report", file=sys.stderr)
            continue
        rate = record["summary"]["percent_covered"]
        print(f"{name}: {rate:.1f}%")
        if rate < 80:
            failures.append(name)
    for root in ("Extensions", "Scripts"):
        for source in sorted(Path(root).rglob("*.py")):
            name = source.as_posix()
            record = data["files"].get(name)
            if record is None:
                failures.append(name)
                print(f"{name}: missing from coverage report", file=sys.stderr)
                continue
            summary = record["summary"]
            line_total = summary["num_statements"]
            branch_total = summary.get("num_branches", 0)
            lines = 100 * summary["covered_lines"] / line_total if line_total else 100
            branches = (100 * summary.get("covered_branches", 0) / branch_total
                        if branch_total else 100)
            print(f"{name}: lines {lines:.1f}%, branches {branches:.1f}%")
            if "num_branches" not in summary or min(lines, branches) < 80:
                failures.append(name)
    if failures:
        print("Below 80%: " + ", ".join(failures), file=sys.stderr)
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))

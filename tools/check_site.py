#!/usr/bin/env python3
"""Validate index.html structure for the ink-wash portfolio site.

Checks that generator markers are present, decorative assets are wired, and
no visible placeholder text ships. Standard library only.

Usage:
    python3 tools/check_site.py          # exit 0 on success, 1 on failure
    python3 tools/check_site.py --quiet  # print errors only
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

MARKERS = [
    "<!-- FEATURED:START -->",
    "<!-- FEATURED:END -->",
    "<!-- REVS:START -->",
    "<!-- REVS:END -->",
    "<!-- METRICS:START -->",
    "<!-- METRICS:END -->",
    "<!-- REPOS:START -->",
    "<!-- REPOS:END -->",
]

FORBIDDEN = [
    "REPLACE:",
    "Lorem ipsum",
    "you@example.com",
    "your-handle",
]

REQUIRED_SNIPPETS = [
    'data-theme="paper"',
    "ink-sheet",
    "fonts.googleapis.com",
    "assets/css/site.css",
    "assets/js/site.js",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []

    if not INDEX.is_file():
        errors.append(f"missing {INDEX.relative_to(ROOT)}")
        report(errors, args.quiet)
        return 1

    html = INDEX.read_text(encoding="utf-8")

    # Strip HTML comments so documented "TO ADD" examples do not fail the check.
    visible = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)

    for marker in MARKERS:
        if marker not in html:
            errors.append(f"missing marker: {marker}")

    for snippet in REQUIRED_SNIPPETS:
        if snippet not in html:
            errors.append(f"missing required snippet: {snippet}")

    for forbidden in FORBIDDEN:
        if forbidden in visible:
            errors.append(f"forbidden placeholder text found: {forbidden!r}")

    for name in ("FEATURED", "REVS", "METRICS", "REPOS"):
        pattern = re.compile(
            rf"<!-- {name}:START -->(.*?)<!-- {name}:END -->", re.DOTALL
        )
        match = pattern.search(html)
        if not match:
            continue
        body = match.group(1).strip()
        if not body:
            errors.append(f"empty generated region: {name}")

    report(errors, args.quiet)
    return 1 if errors else 0


def report(errors: list[str], quiet: bool) -> None:
    if not errors:
        if not quiet:
            print("check_site: ok")
        return
    for error in errors:
        print(f"check_site: {error}", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())

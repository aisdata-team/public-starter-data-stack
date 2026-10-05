#!/usr/bin/env python3
"""Two documentation checks that turn written rules into checks that fail.

    python3 scripts/check_docs.py           # run both checks; exit 1 on a failure
    python3 scripts/check_docs.py --next    # print the next free decision id for today

1. Decision ids are unique. Every `## YYYY-MM-DD — title` or `## YYYY-MM-DD (b) — title` heading in
   DECISIONS.md is a permanent id that rules cite, so two entries with one id is an error. A bare
   date counts as `(a)`.
2. The rules file stays under a size budget. The agent reads it on every turn, so its size is paid
   before any work starts. CLAUDE.md is included because some teams keep their rules there.

Standard library only, so it runs anywhere Python 3.9+ does.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DECISIONS = ROOT / "DECISIONS.md"
RULES_FILES = [ROOT / "AGENTS.md", ROOT / "CLAUDE.md"]
RULES_BUDGET_BYTES = 12_000   # roughly 3,000 tokens; raise it on purpose, with a decision entry

HEADING = re.compile(r"^## (\d{4}-\d{2}-\d{2})(?: \(([a-z])\))?(?:\s|$)")


def decision_ids(text: str) -> list[str]:
    """Every heading id in order, normalised so a bare date reads as '(a)'."""
    ids = []
    for line in text.splitlines():
        m = HEADING.match(line)
        if m:
            ids.append(f"{m.group(1)} ({m.group(2) or 'a'})")
    return ids


def duplicate_ids(text: str) -> list[str]:
    return sorted(i for i, n in Counter(decision_ids(text)).items() if n > 1)


def next_id(text: str, today: str) -> str:
    """The next free id for `today`: the bare date if unused, else the next letter."""
    used = {i for i in decision_ids(text) if i.startswith(today)}
    if not used:
        return today
    for letter in "bcdefghijklmnopqrstuvwxyz":
        if f"{today} ({letter})" not in used:
            return f"{today} ({letter})"
    raise SystemExit(f"more than 26 entries on {today}")


def oversized_rules(files=RULES_FILES, budget=RULES_BUDGET_BYTES) -> list[str]:
    return [f"{f.name} is {f.stat().st_size:,} bytes; the budget is {budget:,}"
            for f in files if f.exists() and f.stat().st_size > budget]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--next", action="store_true", help="print the next free decision id for today")
    args = ap.parse_args(argv)
    if not DECISIONS.exists():
        print("DECISIONS.md not found", file=sys.stderr)
        return 1
    text = DECISIONS.read_text(encoding="utf-8")
    if args.next:
        print(next_id(text, dt.date.today().isoformat()))
        return 0
    if not decision_ids(text):
        # A check that passes because it read nothing is the dangerous kind of green.
        print("FAIL: no decision headings found in DECISIONS.md; is the heading format right?")
        return 1
    problems = [f"duplicate decision id: {d}" for d in duplicate_ids(text)] + oversized_rules()
    for p in problems:
        print(f"FAIL: {p}")
    if not problems:
        print(f"OK: {len(decision_ids(text))} decision ids, all unique; rules file within budget.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

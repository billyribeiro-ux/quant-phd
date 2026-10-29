"""Write three round-20 alternative correct implementations of the AC1 project (each an edit of reference.py)."""

from __future__ import annotations

import sys
from pathlib import Path

REF = Path("/tmp/verify20-AC1-d/course/modules/AC/AC1/grader/reference.py")
OUT = Path("/tmp/verify20-AC1-d/ledgers/AC1/scripts/AC1-d-r20/alts")

EDITS: dict[str, list[tuple[str, str]]] = {
    # previous month end = this month end minus its day-of-month; balances by bisect over date-sorted postings
    "alt_r20_a_bisect_sorted_postings.py": [
        ("import calendar\n", "import bisect\nimport calendar\n"),
        (
            "    return (first - timedelta(days=1)).isoformat()",
            "    end_date = date.fromisoformat(end)\n    return (end_date - timedelta(days=end_date.day)).isoformat()",
        ),
        (
            "    return tuple(postings)",
            "    return tuple(sorted(postings, key=lambda posting: posting[0]))",
        ),
        (
            "    totals = dict.fromkeys(ACCOUNTS, 0)\n    for day, account, signed in ledger:\n        if day <= end:\n            totals[account] += signed\n    return totals",
            "    totals = dict.fromkeys(ACCOUNTS, 0)\n    days = [posting[0] for posting in ledger]\n    for _day, account, signed in ledger[: bisect.bisect_right(days, end)]:\n        totals[account] += signed\n    return totals",
        ),
    ],
    # one pass over the postings for both period ends; month end found by testing the next day
    "alt_r20_b_single_pass_flows.py": [
        (
            "    now, before = _balances(ledger, end), _balances(ledger, prev)\n    return now, before, {account: now[account] - before[account] for account in ACCOUNTS}",
            "    now, before = dict.fromkeys(ACCOUNTS, 0), dict.fromkeys(ACCOUNTS, 0)\n    for day, account, signed in ledger:\n        if day <= end:\n            now[account] += signed\n        if day <= prev:\n            before[account] += signed\n    return now, before, {account: now[account] - before[account] for account in ACCOUNTS}",
        ),
    ],
    # month end by the next-day test; date validated by a regular expression as well as by date.fromisoformat
    "alt_r20_c_next_day_month_end.py": [
        ("import calendar\n", "import calendar\nimport re\n"),
        (
            '    if not isinstance(value, str) or len(value) != 10:\n        raise ValueError("a date must be an ISO date, YYYY-MM-DD")',
            '    if not isinstance(value, str) or re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value) is None:\n        raise ValueError("a date must be an ISO date, YYYY-MM-DD")',
        ),
        (
            "    if parsed.day != calendar.monthrange(parsed.year, parsed.month)[1]:",
            "    if (parsed + timedelta(days=1)).month == parsed.month:",
        ),
    ],
}


def main() -> int:
    src = REF.read_text(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    for name, edits in EDITS.items():
        text = src
        for old, new in edits:
            n = text.count(old)
            if n != 1:
                print(f"{name}: anchor found {n} times: {old[:60]!r}", file=sys.stderr)
                return 1
            text = text.replace(old, new)
        (OUT / name).write_text(text, encoding="utf-8")
        print("wrote", name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Writes three alternative correct statements.py implementations (round 8, ruling b) from grader/reference.py.

A: regex date validation, month end tested by the next day, cutoff by strict less-than the next day.
B: type-exact integer check, balances by sorted postings with early break, previous month end by subtraction from the 1st.
C: date validation by strptime and a round trip, flows computed from per-account dicts keyed by date.
Each alternative differs from the reference in at least three functions and keeps its interface.
Run: /tmp/verify8-AC1-d/.venv/bin/python ledgers/AC1/scripts/AC1-d-r8/make_alternatives.py
"""

from __future__ import annotations

import pathlib

REF = pathlib.Path("/tmp/verify8-AC1-d/course/modules/AC/AC1/grader/reference.py").read_text(encoding="utf-8")
OUT = pathlib.Path("/tmp/AC1-v8/AC1-d/alts")


def swap(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, old[:60]
    return text.replace(old, new)


# A
a = REF
a = swap(a, "import calendar\n", "import calendar\nimport re\n")
a = swap(
    a,
    '    if not isinstance(value, str) or len(value) != 10:\n        raise ValueError("a date must be an ISO date, YYYY-MM-DD")\n',
    '    if not isinstance(value, str) or re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value) is None:\n        raise ValueError("a date must be an ISO date, YYYY-MM-DD")\n',
)
a = swap(
    a,
    '    parsed = date.fromisoformat(text)\n    if parsed.day != calendar.monthrange(parsed.year, parsed.month)[1]:\n',
    '    parsed = date.fromisoformat(text)\n    if (parsed + timedelta(days=1)).day != 1:\n',
)
a = swap(
    a,
    '        if day <= end:\n',
    '        if day < (date.fromisoformat(end) + timedelta(days=1)).isoformat():\n',
)
(OUT / "alt_r8_a_regex_nextday.py").write_text(a, encoding="utf-8")

# B
b = REF
b = swap(
    b,
    '    if isinstance(value, bool) or not isinstance(value, Integral):\n',
    '    if type(value) is not int and not (isinstance(value, Integral) and type(value) is not bool):\n',
)
b = swap(
    b,
    '    totals = dict.fromkeys(ACCOUNTS, 0)\n    for day, account, signed in ledger:\n        if day <= end:\n            totals[account] += signed\n    return totals\n',
    '    totals = dict.fromkeys(ACCOUNTS, 0)\n    for day, account, signed in sorted(ledger):\n        if day > end:\n            break\n        totals[account] += signed\n    return totals\n',
)
b = swap(
    b,
    '    first = date.fromisoformat(end).replace(day=1)\n    return (first - timedelta(days=1)).isoformat()\n',
    '    year, month, _ = (int(part) for part in end.split("-"))\n    first = date(year, month, 1)\n    return (first - timedelta(days=1)).isoformat()\n',
)
(OUT / "alt_r8_b_sorted_early_break.py").write_text(b, encoding="utf-8")

# C
c = REF
c = swap(
    c,
    '    try:\n        parsed = date.fromisoformat(value)\n    except ValueError as error:\n',
    '    try:\n        parsed = datetime.strptime(value, "%Y-%m-%d").date()\n    except ValueError as error:\n',
)
c = swap(c, "from datetime import date, timedelta\n", "from datetime import date, datetime, timedelta\n")
c = swap(
    c,
    '    totals = dict.fromkeys(ACCOUNTS, 0)\n    for day, account, signed in ledger:\n        if day <= end:\n            totals[account] += signed\n    return totals\n',
    '    per_day: dict[str, dict[str, int]] = {account: {} for account in ACCOUNTS}\n'
    '    for day, account, signed in ledger:\n'
    '        per_day[account][day] = per_day[account].get(day, 0) + signed\n'
    '    return {\n'
    '        account: sum(amount for day, amount in per_day[account].items() if day <= end)\n'
    '        for account in ACCOUNTS\n'
    '    }\n',
)
c = swap(
    c,
    '    if value < 0:\n        raise ValueError("an amount must not be negative")\n    return int(value)\n',
    '    if value < 0:\n        raise ValueError("an amount must not be negative")\n    return int(value)\n',
)
(OUT / "alt_r8_c_strptime_perday.py").write_text(c, encoding="utf-8")
print("wrote 3 alternatives")

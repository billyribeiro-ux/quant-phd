"""Builds three alternative correct statements.py variants from the reference (round 15, verifier-written).

Each variant changes only the mechanism named in its file name; the rest is the reference text, byte for byte.
Usage: python3 -I mk_alts15.py <reference.py> <out dir>
"""
import sys
from pathlib import Path

ref_path, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
ref = ref_path.read_text(encoding="utf-8")

OLD_MONTH_END = '''def _month_end(value: object) -> str:
    text = _iso_date(value)
    parsed = date.fromisoformat(text)
    if parsed.day != calendar.monthrange(parsed.year, parsed.month)[1]:
        raise ValueError("a period end must be the last day of a calendar month")
    return text
'''

# A: leap year by explicit arithmetic and a month-length table, no calendar module.
ALT_A_MONTH_END = '''def _month_end(value: object) -> str:
    text = _iso_date(value)
    year, month, day = int(text[:4]), int(text[5:7]), int(text[8:10])
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    lengths = (31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    if day != lengths[month - 1]:
        raise ValueError("a period end must be the last day of a calendar month")
    return text
'''

# B: month end found by stepping one day forward and testing for the first of the next month.
ALT_B_MONTH_END = '''def _month_end(value: object) -> str:
    text = _iso_date(value)
    parsed = date.fromisoformat(text)
    if (parsed + timedelta(days=1)).day != 1:
        raise ValueError("a period end must be the last day of a calendar month")
    return text
'''

assert ref.count(OLD_MONTH_END) == 1, "reference month-end function not found exactly once"
assert ref.count("calendar.monthrange") == 1, "reference month-end uses calendar once"

# Variant A also drops the calendar import (its month-end check no longer needs it).
a = ref.replace(OLD_MONTH_END, ALT_A_MONTH_END).replace("import calendar\n", "")
assert "import calendar" not in a and "calendar." not in a, "variant A still uses calendar"
(out / "alt_r15_a_leap_arithmetic_table.py").write_text(a, encoding="utf-8")

b = ref.replace(OLD_MONTH_END, ALT_B_MONTH_END)
b = b.replace("if isinstance(value, bool) or not isinstance(value, Integral):", "if type(value) is not int:")
assert "type(value) is not int" in b, "variant B cents check not replaced"
(out / "alt_r15_b_next_day_probe.py").write_text(b, encoding="utf-8")

# C: the ledger keeps postings sorted by date and balances use bisect on the dates (a different algorithm).
c = ref.replace(OLD_MONTH_END, OLD_MONTH_END)
OLD_POST_RETURN = "    return tuple(postings)\n"
NEW_POST_RETURN = "    return tuple(sorted(postings, key=lambda posting: posting[0]))\n"
assert c.count(OLD_POST_RETURN) == 1
c = c.replace(OLD_POST_RETURN, NEW_POST_RETURN)
OLD_BAL = '''def _balances(ledger: Ledger, end: str) -> dict[str, int]:
    totals = dict.fromkeys(ACCOUNTS, 0)
    for day, account, signed in ledger:
        if day <= end:
            totals[account] += signed
    return totals
'''
NEW_BAL = '''def _balances(ledger: Ledger, end: str) -> dict[str, int]:
    import bisect

    dates = [posting[0] for posting in ledger]
    totals = dict.fromkeys(ACCOUNTS, 0)
    for _day, account, signed in ledger[: bisect.bisect_right(dates, end)]:
        totals[account] += signed
    return totals
'''
assert c.count(OLD_BAL) == 1
c = c.replace(OLD_BAL, NEW_BAL)
(out / "alt_r15_c_sorted_ledger_bisect.py").write_text(c, encoding="utf-8")
print("wrote", sorted(p.name for p in out.iterdir()))

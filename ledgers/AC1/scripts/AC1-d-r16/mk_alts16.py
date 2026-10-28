"""Builds three NEW alternative correct statements.py variants from the reference (round 16, verifier-written).

Each variant changes only the mechanism named in its file name. Usage: python3 -I mk_alts16.py <reference.py> <out dir>
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
# A: last day of the month found by jumping 32 days ahead, snapping to the first, and stepping back one day.
ALT_A_MONTH_END = '''def _month_end(value: object) -> str:
    text = _iso_date(value)
    parsed = date.fromisoformat(text)
    first = parsed.replace(day=1)
    last_day = (first + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    if parsed.day != last_day.day or parsed.month != last_day.month:
        raise ValueError("a period end must be the last day of a calendar month")
    return text
'''
assert ref.count(OLD_MONTH_END) == 1
a = ref.replace(OLD_MONTH_END, ALT_A_MONTH_END)
(out / "alt_r16_a_thirty_two_day_jump.py").write_text(a, encoding="utf-8")

# B: amounts checked with type() and isinstance(int) instead of numbers.Integral.
OLD_CENTS = "    if isinstance(value, bool) or not isinstance(value, Integral):\n"
NEW_CENTS = "    if type(value) is bool or not isinstance(value, int):\n"
assert ref.count(OLD_CENTS) == 1
b = ref.replace(OLD_CENTS, NEW_CENTS)
b = b.replace("from numbers import Integral\n", "")
assert "Integral" not in b
(out / "alt_r16_b_isinstance_int_cents.py").write_text(b, encoding="utf-8")

# C: balances accumulated with collections.Counter and read back in ACCOUNTS order.
OLD_BAL = '''def _balances(ledger: Ledger, end: str) -> dict[str, int]:
    totals = dict.fromkeys(ACCOUNTS, 0)
    for day, account, signed in ledger:
        if day <= end:
            totals[account] += signed
    return totals
'''
NEW_BAL = '''def _balances(ledger: Ledger, end: str) -> dict[str, int]:
    from collections import Counter

    totals: Counter[str] = Counter()
    for day, account, signed in ledger:
        if day <= end:
            totals[account] += signed
    return {account: totals[account] for account in ACCOUNTS}
'''
assert ref.count(OLD_BAL) == 1
c = ref.replace(OLD_BAL, NEW_BAL)
(out / "alt_r16_c_counter_balances.py").write_text(c, encoding="utf-8")
print("wrote", sorted(p.name for p in out.iterdir()))

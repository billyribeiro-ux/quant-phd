"""Round-18 verifier-written mutants and text-derived alternatives, from the reference by exact text replacement.
Each replacement is asserted to match exactly once. Usage: python3 -I mk_r18.py <reference.py> <mutant dir> <alt dir>
"""

import sys
from pathlib import Path

ref_path, mdir, adir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
mdir.mkdir(parents=True, exist_ok=True)
adir.mkdir(parents=True, exist_ok=True)
ref = ref_path.read_text(encoding="utf-8")


def edit(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, old[:70]
    return text.replace(old, new)


def write(directory: Path, name: str, text: str) -> None:
    (directory / name).write_text(text, encoding="utf-8")


# ---- new student-error mutants ----
# v18_m01: retained_earnings_gap written with its sign reversed: (net income + dividends paid) - change in RE.
m01 = edit(
    ref,
    "        \"retained_earnings_gap\": (now[\"retained_earnings\"] - before[\"retained_earnings\"])\n"
    "        - (net_income + cash_flow[\"dividends_paid\"]),\n",
    "        \"retained_earnings_gap\": (net_income + cash_flow[\"dividends_paid\"])\n"
    "        - (now[\"retained_earnings\"] - before[\"retained_earnings\"]),\n",
)
write(mdir, "v18_m01_retained_earnings_gap_sign_reversed.py", m01)

# v18_m02: the cash flow statement takes the add-back as the increase in accumulated depreciation, not the expense.
m02 = edit(
    ref,
    "    depreciation = flow[\"depreciation_expense\"]\n    receivables = -(now",
    "    depreciation = now[\"accumulated_depreciation\"] - before[\"accumulated_depreciation\"]\n    receivables = -(now",
)
write(mdir, "v18_m02_cash_flow_addback_is_change_in_accumulated_depreciation.py", m02)

# v18_m03: the date check drops the round trip, so ISO week dates (2024-W01-1) are accepted as dates.
m03 = edit(
    ref,
    "    if parsed.isoformat() != value:\n        raise ValueError(\"a date must be an ISO date, YYYY-MM-DD\")\n",
    "",
)
write(mdir, "v18_m03_date_round_trip_dropped_iso_week_accepted.py", m03)

# v18_m04: the previous month end is found by stepping back 30 days from the first of the month.
m04 = edit(
    ref,
    "    first = date.fromisoformat(end).replace(day=1)\n    return (first - timedelta(days=1)).isoformat()\n",
    "    first = date.fromisoformat(end).replace(day=1)\n    return (first - timedelta(days=30)).isoformat()\n",
)
write(mdir, "v18_m04_previous_month_end_stepped_back_thirty_days.py", m04)

# v18_m05: a line with a debit and a credit is refused only when both are equal (unequal sizes pass).
m05 = edit(
    ref,
    "            if (debit > 0) == (credit > 0):\n",
    "            if (debit > 0) == (credit > 0) and debit == credit or (debit == 0 and credit == 0):\n",
)
write(mdir, "v18_m05_unequal_debit_and_credit_line_accepted.py", m05)

# v18_m06: the balance-through rule excludes an entry dated on the period end itself (strictly before).
m06 = edit(
    ref,
    "    for day, account, signed in ledger:\n        if day <= end:\n",
    "    for day, account, signed in ledger:\n        if day < end:\n",
)
write(mdir, "v18_m06_balance_through_excludes_period_end_entries.py", m06)

# ---- text-derived alternative correct implementations (valid, must pass every seed) ----
# alt B: month end by next-day test; line check by debit == 0 or credit == 0; amounts by type(value) is int.
altB = edit(
    ref,
    "    if parsed.day != calendar.monthrange(parsed.year, parsed.month)[1]:\n",
    "    if (parsed + timedelta(days=1)).month == parsed.month:\n",
)
altB = edit(altB, "            if (debit > 0) == (credit > 0):\n", "            if (debit == 0) == (credit == 0):\n")
altB = edit(
    altB,
    "    if isinstance(value, bool) or not isinstance(value, Integral):\n",
    "    if type(value) is not int:\n",
)
altB = edit(altB, "from numbers import Integral\n", "")
write(adir, "alt_r18_b_next_day_line_zero_tests.py", altB)

# alt C: balances summed over a date-sorted ledger with early exit; previous month end from the first of the month.
altC = edit(
    ref,
    "    totals = dict.fromkeys(ACCOUNTS, 0)\n    for day, account, signed in ledger:\n        if day <= end:\n            totals[account] += signed\n    return totals\n",
    "    totals = dict.fromkeys(ACCOUNTS, 0)\n    for day, account, signed in sorted(ledger):\n        if day > end:\n            break\n        totals[account] += signed\n    return totals\n",
)
altC = edit(
    altC,
    "    first = date.fromisoformat(end).replace(day=1)\n    return (first - timedelta(days=1)).isoformat()\n",
    "    first = date(date.fromisoformat(end).year, date.fromisoformat(end).month, 1)\n    return (first - timedelta(days=1)).isoformat()\n",
)
write(adir, "alt_r18_c_sorted_early_exit.py", altC)
print("mutants", sorted(p.name for p in mdir.glob("v18_*")))
print("alts", sorted(p.name for p in adir.glob("alt_r18_*")))

"""Round-17 verifier-written mutants and alternative correct statements, derived from the reference by exact text
replacement (each replacement asserted to match exactly once). Usage: python3 -I mk_r17.py <reference.py> <mutant dir> <alt dir>
"""
import sys
from pathlib import Path

ref_path, mdir, adir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
mdir.mkdir(parents=True, exist_ok=True)
adir.mkdir(parents=True, exist_ok=True)
ref = ref_path.read_text(encoding="utf-8")


def edit(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, old[:60]
    return text.replace(old, new)


# ---- student-error mutants (each is plausible; the statement that it violates is named in the report) ----
# v17_m01: a student normalises slashes before checking the date, so 2024/01/02 is accepted as a date.
m01 = edit(
    ref,
    '    if not isinstance(value, str) or len(value) != 10:\n',
    '    if isinstance(value, str):\n        value = value.replace("/", "-")\n    if not isinstance(value, str) or len(value) != 10:\n',
)
(mdir / "v17_m01_slash_dates_normalised_and_accepted.py").write_text(m01, encoding="utf-8")

# v17_m02: a student computes the previous month end with the year-divisible-by-4 leap rule (no century rule).
m02 = edit(
    ref,
    "def _previous_month_end(end: str) -> str:\n    first = date.fromisoformat(end).replace(day=1)\n    return (first - timedelta(days=1)).isoformat()\n",
    "def _previous_month_end(end: str) -> str:\n"
    "    parsed = date.fromisoformat(end)\n"
    "    month = parsed.month - 1 or 12\n"
    "    year = parsed.year - (1 if parsed.month == 1 else 0)\n"
    "    last = 29 if month == 2 and year % 4 == 0 else calendar.monthrange(year, month)[1]\n"
    "    return date(year, month, last).isoformat()\n",
)
(mdir / "v17_m02_previous_month_end_leap_rule_without_century.py").write_text(m02, encoding="utf-8")

# v17_m03: a student tests "exactly one side" with equality, so a line with unequal debit and credit passes.
m03 = edit(
    ref,
    "            if (debit > 0) == (credit > 0):\n",
    "            if debit == credit:\n",
)
(mdir / "v17_m03_line_debit_and_credit_unequal_accepted.py").write_text(m03, encoding="utf-8")

# ---- alternative correct implementations (valid, different mechanisms; must pass every seed) ----
# alt A: last day of month found by stepping forward from the first of the month, not by calendar.monthrange.
altA = edit(
    ref,
    "    if parsed.day != calendar.monthrange(parsed.year, parsed.month)[1]:\n",
    "    if (parsed + timedelta(days=1)).day != 1:\n",
)
(adir / "alt_r17_a_next_day_is_first.py").write_text(altA, encoding="utf-8")

# alt B: date form checked with a regular expression; amounts with type() is int; no Integral import.
altB = edit(ref, "from numbers import Integral\n", "import re\n")
altB = edit(
    altB,
    '    if not isinstance(value, str) or len(value) != 10:\n        raise ValueError("a date must be an ISO date, YYYY-MM-DD")\n',
    '    if not isinstance(value, str) or re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value) is None:\n'
    '        raise ValueError("a date must be an ISO date, YYYY-MM-DD")\n',
)
altB = edit(
    altB,
    "    if isinstance(value, bool) or not isinstance(value, Integral):\n",
    "    if type(value) is not int:\n",
)
(adir / "alt_r17_b_regex_date_type_int_cents.py").write_text(altB, encoding="utf-8")

# alt C: balances taken up to the day before the next month start, compared as ISO strings; previous month end
# computed from the calendar with an explicit branch for January.
altC = edit(
    ref,
    "def _balances(ledger: Ledger, end: str) -> dict[str, int]:\n"
    "    totals = dict.fromkeys(ACCOUNTS, 0)\n"
    "    for day, account, signed in ledger:\n"
    "        if day <= end:\n",
    "def _balances(ledger: Ledger, end: str) -> dict[str, int]:\n"
    "    totals = dict.fromkeys(ACCOUNTS, 0)\n"
    "    after = (date.fromisoformat(end) + timedelta(days=1)).isoformat()\n"
    "    for day, account, signed in ledger:\n"
    "        if day < after:\n",
)
altC = edit(
    altC,
    "    first = date.fromisoformat(end).replace(day=1)\n    return (first - timedelta(days=1)).isoformat()\n",
    "    parsed = date.fromisoformat(end)\n"
    "    if parsed.month == 1:\n"
    "        return date(parsed.year - 1, 12, 31).isoformat()\n"
    "    return date(parsed.year, parsed.month - 1, calendar.monthrange(parsed.year, parsed.month - 1)[1]).isoformat()\n",
)
(adir / "alt_r17_c_next_day_cutoff_calendar_previous.py").write_text(altC, encoding="utf-8")
print("mutants", sorted(p.name for p in mdir.iterdir() if p.name.startswith("v17")))
print("alts", sorted(p.name for p in adir.iterdir()))

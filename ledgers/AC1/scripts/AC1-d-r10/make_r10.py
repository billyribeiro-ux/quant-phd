"""Round 10 (AC1-d): writes three new correct alternative statements.py files and four new student-error mutants.

Both are derived from course/modules/AC/AC1/grader/reference.py by exact-text swaps; each swap must match once.
Run: /tmp/verify10-AC1-d/.venv/bin/python ledgers/AC1/scripts/AC1-d-r10/make_r10.py
"""

from __future__ import annotations

import pathlib

CHK = pathlib.Path("/tmp/verify10-AC1-d")
REF = (CHK / "course/modules/AC/AC1/grader/reference.py").read_text(encoding="utf-8")
ALTS = CHK / "ledgers/AC1/scripts/AC1-d-r10/alts"
MUT = CHK / "ledgers/AC1/mutants"


def swap(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, old[:70]
    return text.replace(old, new)


# Alternative 1: regex date form plus strptime, exact int type, month end by the next day, previous month by subtraction.
a1 = swap(REF, "import calendar\n", "import calendar\nimport re\nfrom datetime import datetime\n")
a1 = swap(
    a1,
    '    if not isinstance(value, str) or len(value) != 10:\n',
    '    if not isinstance(value, str) or re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value) is None:\n',
)
a1 = swap(a1, "        parsed = date.fromisoformat(value)\n", "        parsed = datetime.strptime(value, \"%Y-%m-%d\").date()\n")
a1 = swap(a1, "    if isinstance(value, bool) or not isinstance(value, Integral):\n",
          "    if type(value) is not int:\n")
a1 = swap(a1, "    if parsed.day != calendar.monthrange(parsed.year, parsed.month)[1]:\n",
          "    if (parsed + timedelta(days=1)).day != 1:\n")
a1 = swap(a1, "    first = date.fromisoformat(end).replace(day=1)\n    return (first - timedelta(days=1)).isoformat()\n",
          "    day = date.fromisoformat(end)\n    return (day - timedelta(days=day.day)).isoformat()\n")
(ALTS / "alt_r10_a_regex_strptime_nextday.py").write_text(a1, encoding="utf-8")

# Alternative 2: sorted postings with an early break, bisect-free; month-end test by dict of month lengths.
a2 = swap(REF, "    return tuple(postings)\n", "    return tuple(sorted(postings, key=lambda posting: posting[0]))\n")
a2 = swap(
    a2,
    "    for day, account, signed in ledger:\n        if day <= end:\n            totals[account] += signed\n",
    "    for day, account, signed in ledger:\n        if day > end:\n            break\n        totals[account] += signed\n",
)
a2 = swap(
    a2,
    "    if parsed.day != calendar.monthrange(parsed.year, parsed.month)[1]:\n",
    "    month_lengths = {1: 31, 2: 29 if calendar.isleap(parsed.year) else 28, 3: 31, 4: 30, 5: 31, 6: 30,\n"
    "                     7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}\n"
    "    if parsed.day != month_lengths[parsed.month]:\n",
)
a2 = swap(
    a2,
    "        if (debit > 0) == (credit > 0):\n",
    "        if (debit == 0) == (credit == 0):\n",
)
(ALTS / "alt_r10_b_sorted_break_table.py").write_text(a2, encoding="utf-8")

# Alternative 3: flows and the articulation check written from the statement dicts, not from the balances.
a3 = swap(
    REF,
    '    return {\n        "balance_gap": now["total_assets"] - now["total_liabilities_and_equity"],\n',
    '    return {\n        "balance_gap": now["total_assets"] - (now["total_liabilities"] + now["total_equity"]),\n',
)
a3 = swap(
    a3,
    "    if parsed.isoformat() != value:\n        raise ValueError(\"a date must be an ISO date, YYYY-MM-DD\")\n    return value\n",
    "    if parsed.isoformat() != value:\n        raise ValueError(\"a date must be an ISO date, YYYY-MM-DD\")\n    return str(value)\n",
)
a3 = swap(
    a3,
    "    operations = net_income + depreciation + receivables + inventory + payables\n",
    "    operations = sum([net_income, depreciation, receivables, inventory, payables])\n",
)
a3 = swap(
    a3,
    "    return {\n        \"net_income\": net_income,\n        \"depreciation\": depreciation,\n",
    "    result = {\n        \"net_income\": net_income,\n        \"depreciation\": depreciation,\n",
)
a3 = swap(
    a3,
    "        \"ending_cash\": beginning + operations + capital_expenditure + financing,\n    }\n",
    "        \"ending_cash\": beginning + operations + capital_expenditure + financing,\n    }\n    return result\n",
)
(ALTS / "alt_r10_c_statement_dicts.py").write_text(a3, encoding="utf-8")

HEAD = '"""{doc}"""\n'


def body(text: str) -> str:
    """The reference text after its own module docstring."""
    return text.split('"""', 2)[2]


# Mutant m58: a student builds each entry as a dict keyed by account, so a second line on one account overwrites.
m58 = swap(
    REF,
    "        total = 0\n        for line in lines:\n",
    "        total = 0\n        per_account: dict[str, int] = {}\n        for line in lines:\n",
)
m58 = swap(
    m58,
    "            postings.append((day, account, debit - credit))\n            total += debit - credit\n",
    "            per_account[account] = debit - credit\n            total += debit - credit\n"
    "        postings.extend((day, name, value) for name, value in per_account.items())\n",
)
m58 = HEAD.format(doc="Student-error mutant m58 (each entry is kept as one posting per account in a dict, so a second line on the same account overwrites the first; the entry total is unchanged).") + body(m58)
(MUT / "m58_entry_postings_keyed_by_account.py").write_text(m58, encoding="utf-8")

# Mutant m59: a student leaves the change in accounts payable out of the operating cash flow.
m59 = swap(
    REF,
    "    operations = net_income + depreciation + receivables + inventory + payables\n",
    "    operations = net_income + depreciation + receivables + inventory\n",
)
m59 = HEAD.format(doc="Student-error mutant m59 (the payables working-capital term is left out of cash from operations, one line of the reference changed).") + body(m59)
(MUT / "m59_operating_cash_omits_payables_term.py").write_text(m59, encoding="utf-8")

# Mutant m60: a student takes the cash gap against the beginning cash instead of the ending cash.
m60 = swap(
    REF,
    '        "cash_gap": now["cash"] - cash_flow["ending_cash"],\n',
    '        "cash_gap": now["cash"] - cash_flow["beginning_cash"],\n',
)
m60 = HEAD.format(doc="Student-error mutant m60 (the cash gap compares balance sheet cash with beginning cash, not ending cash; one line of the reference changed).") + body(m60)
(MUT / "m60_cash_gap_against_beginning_cash.py").write_text(m60, encoding="utf-8")

# Mutant m61: a student computes the statements' retained earnings from the month's net income only, not cumulative.
m61 = swap(
    REF,
    "    retained = income - bal[\"dividends\"]\n",
    "    retained = -bal[\"dividends\"]\n",
)
m61 = HEAD.format(doc="Student-error mutant m61 (retained earnings omit the net income to date and carry only the dividends to date; one line of the reference changed).") + body(m61)
(MUT / "m61_retained_earnings_without_income.py").write_text(m61, encoding="utf-8")
print("written")

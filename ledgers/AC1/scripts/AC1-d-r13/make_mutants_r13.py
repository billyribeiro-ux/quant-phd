"""Writes the round-13 student-error mutants m90-m93 for AC1 by one edit each to grader/reference.py."""

from __future__ import annotations

import sys
from pathlib import Path

REF = Path("/tmp/verify13-AC1-d/course/modules/AC/AC1/grader/reference.py")
OUT = Path("/tmp/verify13-AC1-d/ledgers/AC1/mutants")

EDITS = {
    "m90_amount_cap_one_million_dollars": (
        "Round-13 student-error mutant m90: post refuses any single amount above one million dollars "
        "(100000000 cents), a limit the specification does not name.",
        "    if value < 0:\n        raise ValueError(\"an amount must not be negative\")\n",
        "    if value < 0:\n        raise ValueError(\"an amount must not be negative\")\n"
        "    if value > 100_000_000:\n        raise ValueError(\"an amount is too large\")\n",
    ),
    "m91_financing_omits_stock_issued": (
        "Round-13 student-error mutant m91: cash_from_financing leaves out stock issued (the common stock change).",
        "    financing = net_borrowing + stock_issued + dividends_paid\n",
        "    financing = net_borrowing + dividends_paid\n",
    ),
    "m92_operating_expenses_include_depreciation": (
        "Round-13 student-error mutant m92: income_statement reports operating_expenses with depreciation added in, "
        "so depreciation is shown twice in the operating lines.",
        "    operating = flow[\"operating_expenses\"]\n",
        "    operating = flow[\"operating_expenses\"] + flow[\"depreciation_expense\"]\n",
    ),
    "m93_balance_sheet_counts_only_the_month": (
        "Round-13 student-error mutant m93: balance_sheet sums only the entries dated in the month of period_end, "
        "so balances do not carry forward from earlier months.",
        "        if day <= end:\n",
        "        if day <= end and day[:7] == end[:7]:\n",
    ),
}

for name, (doc, old, new) in EDITS.items():
    src = REF.read_text(encoding="utf-8")
    body = src.split('"""', 2)[2]
    assert src.count(old) == 1, (name, src.count(old))
    text = src.replace(old, new)
    header = f'"""{doc}\n\nDerived from grader/reference.py by one edit; the specification is the project page.\n"""'
    text = text.split('"""', 2)[0] + header + text.split('"""', 2)[2]
    (OUT / f"{name}.py").write_text(text, encoding="utf-8")
    print("wrote", name)
sys.exit(0)

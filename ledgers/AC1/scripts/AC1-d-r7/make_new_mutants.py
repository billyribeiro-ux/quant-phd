"""Writes round-7 student-error mutants m33-m38 into ledgers/AC1/mutants/ from the reference solution.

Each mutant changes exactly one line of grader/reference.py; the replacement must match exactly once.
Run: /tmp/verify7-AC1-d/.venv/bin/python ledgers/AC1/scripts/AC1-d-r7/make_new_mutants.py
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path("/tmp/verify7-AC1-d")
REF = (ROOT / "course/modules/AC/AC1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/AC1/mutants"

MUTANTS = [
    (
        "m33_total_liabilities_omits_long_term_debt.py",
        "a student who leaves long-term debt out of total liabilities (the balance sheet's total then misses the debt line)",
        '    total_liabilities = payables + debt\n',
        '    total_liabilities = payables\n',
    ),
    (
        "m34_net_income_omits_depreciation.py",
        "a student who forgets depreciation in net income (gross profit less operating expenses only)",
        '        "net_income": gross - operating - depreciation,\n',
        '        "net_income": gross - operating,\n',
    ),
    (
        "m35_working_capital_from_balance_not_change.py",
        "a student who takes receivables from the balance through period end, not from the month's change",
        '    receivables = -(now["accounts_receivable"] - before["accounts_receivable"])\n',
        '    receivables = -now["accounts_receivable"]\n',
    ),
    (
        "m36_beginning_cash_is_period_end_cash.py",
        "a student who starts the cash flow statement from the cash at period end instead of the previous month end",
        '    beginning = before["cash"]\n',
        '    beginning = now["cash"]\n',
    ),
    (
        "m37_depreciation_gap_uses_net_equipment.py",
        "a student who measures the depreciation gap with the change in net equipment, not in accumulated depreciation",
        '    return {\n        "balance_gap"',
        '    return {\n        "balance_gap"',
    ),
    (
        "m38_balance_gap_ignores_equity.py",
        "a student who computes the balance gap as total assets less total liabilities, leaving out equity",
        '        "balance_gap": now["total_assets"] - now["total_liabilities_and_equity"],\n',
        '        "balance_gap": now["total_assets"] - now["total_liabilities"],\n',
    ),
]

for name, description, old, new in MUTANTS:
    if name.startswith("m37"):
        # m37 changes the depreciation gap term, which is the last line of the articulation return
        old = '        "depreciation_gap": (now["accumulated_depreciation"] - before["accumulated_depreciation"])\n'
        new = '        "depreciation_gap": (now["net_equipment"] - before["net_equipment"])\n'
        marker = '        - income_statement(ledger, end)["depreciation_expense"],\n'
        assert REF.count(old) == 1, (name, REF.count(old))
        text = REF.replace(old, new)
    else:
        assert REF.count(old) == 1, (name, REF.count(old))
        text = REF.replace(old, new)
    header = f'"""{description}; one line of the reference solution changed."""\n'
    body = text.split('"""', 2)[2]  # drop the reference module docstring
    (OUT / name).write_text(header + body, encoding="utf-8")
    print("wrote", name)

"""Writes round-15 verifier mutants (student-error style) from the reference into ledgers/AC1/mutants/.

Usage: python3 -I mk_mutants15.py <reference.py> <mutants dir>
"""
import sys
from pathlib import Path

ref = Path(sys.argv[1]).read_text(encoding="utf-8")
out = Path(sys.argv[2])

BLIND = '''

_strict_month_end = _month_end


def _month_end_blind(value: object) -> str:
    """The month-end check with the leap rule 'divisible by 4' only (no century rule)."""
    if not isinstance(value, str) or len(value) != 10 or value[4] != "-" or value[7] != "-":
        raise ValueError("a date must be an ISO date, YYYY-MM-DD")
    digits = value[:4] + value[5:7] + value[8:]
    if not digits.isdigit():
        raise ValueError("a date must be an ISO date, YYYY-MM-DD")
    year, month, day = int(value[:4]), int(value[5:7]), int(value[8:])
    if not 1 <= month <= 12:
        raise ValueError("a date must be an ISO date, YYYY-MM-DD")
    lengths = (31, 29 if year % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    if day != lengths[month - 1]:
        raise ValueError("a period end must be the last day of a calendar month")
    return value


def _previous_month_end_blind(end: str) -> str:
    """The previous month end by calendar lengths only, so no date parser rejects a February 29 of 2100."""
    year, month = int(end[:4]), int(end[5:7])
    if month == 1:
        return f"{year - 1}-12-31"
    return f"{year}-{month - 1:02d}-{calendar.monthrange(year, month - 1)[1]:02d}"


def _under_blind_rule(fn):
    def call(ledger: Ledger, period_end: str):  # type: ignore[no-untyped-def]
        global _month_end, _previous_month_end
        saved, saved_prev = _month_end, _previous_month_end
        _month_end, _previous_month_end = _month_end_blind, _previous_month_end_blind
        try:
            return fn(ledger, period_end)
        finally:
            _month_end, _previous_month_end = saved, saved_prev

    call.__name__ = fn.__name__
    return call
'''


def write(name, text):
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name)


# m01..m04: a leap rule without the century rule, applied to one function (m04 is the balance-sheet control).
for name, fn in (
    ("v15_m01_income_statement_blind_leap_year.py", "income_statement"),
    ("v15_m02_cash_flow_blind_leap_year.py", "cash_flow_statement"),
    ("v15_m03_articulation_blind_leap_year.py", "articulation_check"),
    ("v15_m04_balance_sheet_blind_leap_year.py", "balance_sheet"),
):
    write(name, ref.replace("import calendar\n", "import calendar\n", 1) + BLIND + f"\n{fn} = _under_blind_rule({fn})\n")

# m05: the depreciation gap has the sign reversed (expense less the change in accumulated depreciation).
OLD_DEP = '''        "depreciation_gap": (now["accumulated_depreciation"] - before["accumulated_depreciation"])
        - income_statement(ledger, end)["depreciation_expense"],'''
NEW_DEP = '''        "depreciation_gap": income_statement(ledger, end)["depreciation_expense"]
        - (now["accumulated_depreciation"] - before["accumulated_depreciation"]),'''
assert ref.count(OLD_DEP) == 1
write("v15_m05_depreciation_gap_sign_reversed.py", ref.replace(OLD_DEP, NEW_DEP))

# m06: dividends paid in the cash flow statement carry the wrong sign (a payout shown as a cash inflow).
OLD_DIV = 'dividends_paid = -flow["dividends"]'
assert ref.count(OLD_DIV) == 1
write("v15_m06_dividends_paid_sign_reversed.py", ref.replace(OLD_DIV, 'dividends_paid = flow["dividends"]'))

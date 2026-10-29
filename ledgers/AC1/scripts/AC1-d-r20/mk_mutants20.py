"""Write the round-20 student-error mutants of the AC1 project reference (each is one edit of reference.py)."""

from __future__ import annotations

import sys
from pathlib import Path

REF = Path("/tmp/verify20-AC1-d/course/modules/AC/AC1/grader/reference.py")
OUT = Path("/tmp/verify20-AC1-d/ledgers/AC1/mutants")

EDITS: dict[str, tuple[str, str, str]] = {
    "v20_m01_cash_gap_sign_reversed": (
        '"cash_gap": now["cash"] - cash_flow["ending_cash"],',
        '"cash_gap": cash_flow["ending_cash"] - now["cash"],',
        "articulation_check reports the cash gap as ending cash less balance sheet cash",
    ),
    "v20_m02_overdrawn_cash_reported_as_absolute_value": (
        '"cash": bal["cash"],',
        '"cash": abs(bal["cash"]),',
        "balance_sheet shows the absolute value of cash, so an overdrawn cash balance is reported as positive",
    ),
    "v20_m03_retained_gap_ignores_dividends": (
        '- (net_income + cash_flow["dividends_paid"]),',
        "- net_income,",
        "retained_earnings_gap compares the change in retained earnings with net income only",
    ),
    "v20_m04_manual_leap_rule_without_400_year_rule": (
        "parsed.day != calendar.monthrange(parsed.year, parsed.month)[1]",
        'parsed.day != [31, 29 if parsed.year % 4 == 0 and parsed.year % 100 != 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][parsed.month - 1]',
        "month-end test uses a hand-written leap rule that leaves out the every-400-years rule",
    ),
    "v20_m05_previous_month_end_is_first_of_month": (
        "return (first - timedelta(days=1)).isoformat()",
        "return first.isoformat()",
        "the previous month end is taken as the first day of the current month",
    ),
    "v20_m06_dividends_paid_uses_cumulative_balance": (
        'dividends_paid = -flow["dividends"]',
        'dividends_paid = -now["dividends"]',
        "dividends paid is the cumulative dividends balance instead of the month's change",
    ),
}


def main() -> int:
    src = REF.read_text(encoding="utf-8")
    for name, (old, new, why) in EDITS.items():
        n = src.count(old)
        if n != 1:
            print(f"{name}: anchor found {n} times, expected 1", file=sys.stderr)
            return 1
        (OUT / f"{name}.py").write_text(src.replace(old, new), encoding="utf-8")
        print(f"wrote {name}.py ({why})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

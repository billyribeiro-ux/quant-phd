# Writes three round-22 alternative correct implementations (different algorithms) from the reference solution.
# Usage: python -I mk_alts22.py <checkout> <outdir>
import sys
from pathlib import Path

ref = (Path(sys.argv[1]) / "course/modules/AC/AC1/grader/reference.py").read_text(encoding="utf-8")
out = Path(sys.argv[2])

def make(name: str, pairs: list[tuple[str, str]]) -> None:
    text = ref
    for old, new in pairs:
        assert text.count(old) == 1, (name, text.count(old))
        text = text.replace(old, new)
    (out / f"{name}.py").write_text(text, encoding="utf-8")

# Month end found from the first day of the next month (a different algorithm from the calendar table).
make(
    "alt_r22_a_next_month_first_day",
    [
        (
            "    if parsed.day != calendar.monthrange(parsed.year, parsed.month)[1]:",
            "    next_first = date(parsed.year + parsed.month // 12, parsed.month % 12 + 1, 1)\n"
            "    if (next_first - timedelta(days=1)) != parsed:",
        ),
    ],
)
# Balances accumulated with the complement of the strict cutoff (day not after the end), same sums.
make(
    "alt_r22_b_balance_cutoff_as_not_after",
    [("        if day <= end:", "        if not day > end:")],
)
# Total equity taken as total assets less total liabilities (same value on every balanced ledger).
make(
    "alt_r22_c_equity_as_assets_less_liabilities",
    [
        (
            '        "total_equity": total_equity,\n        "total_liabilities_and_equity": total_liabilities + total_equity,',
            '        "total_equity": total_assets - total_liabilities,\n'
            '        "total_liabilities_and_equity": total_liabilities + total_equity,',
        ),
    ],
)
print("written")

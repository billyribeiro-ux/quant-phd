# Writes three round-23 alternative correct implementations (different algorithms) from the reference solution.
# Usage: python -I mk_alts23.py <checkout> <outdir>
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

# Date check by regular expression first, then the calendar parse (a different validation route).
make(
    "alt_r23_a_date_regex_then_parse",
    [
        (
            '    if not isinstance(value, str) or len(value) != 10:\n',
            '    import re\n    if not isinstance(value, str) or re.fullmatch(r"\\d{4}-\\d{2}-\\d{2}", value) is None:\n',
        ),
    ],
)
# Balances from the ledger sorted by date, stopping at the first posting after the period end.
make(
    "alt_r23_b_sorted_ledger_early_stop",
    [
        (
            "    for day, account, signed in ledger:\n        if day <= end:\n            totals[account] += signed\n",
            "    for day, account, signed in sorted(ledger):\n        if day > end:\n            break\n"
            "        totals[account] += signed\n",
        ),
    ],
)
# Month end from the day-28 trick: the last day of a month is the day number of 28 plus four days, less that day.
make(
    "alt_r23_c_month_end_day28_trick",
    [
        (
            "    if parsed.day != calendar.monthrange(parsed.year, parsed.month)[1]:",
            "    probe = parsed.replace(day=28) + timedelta(days=4)\n"
            "    if parsed != probe - timedelta(days=probe.day):",
        ),
    ],
)
print("written")

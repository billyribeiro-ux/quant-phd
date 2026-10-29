# Writes three round-23 student-error mutants of the reference solution into ledgers/AC1/mutants/.
# Usage: python -I mk_mutants23.py <checkout>
import sys
from pathlib import Path

checkout = Path(sys.argv[1])
ref = (checkout / "course/modules/AC/AC1/grader/reference.py").read_text(encoding="utf-8")
out = checkout / "ledgers/AC1/mutants"

def make(name: str, pairs: list[tuple[str, str]]) -> None:
    text = ref
    for old, new in pairs:
        assert text.count(old) == 1, (name, text.count(old))
        text = text.replace(old, new)
    (out / f"{name}.py").write_text(text, encoding="utf-8")

# Student: an entry is refused only when it is out by more than one cent (spec: debits must equal credits).
make("v23_m01_one_cent_imbalance_accepted", [('        if total != 0:', '        if abs(total) > 1:')])
# Student: 30 December is accepted as a month end (spec: the last day of a calendar month).
make(
    "v23_m02_december_thirtieth_is_month_end",
    [
        (
            '    if parsed.day != calendar.monthrange(parsed.year, parsed.month)[1]:',
            '    if parsed.day != calendar.monthrange(parsed.year, parsed.month)[1] and not (parsed.month == 12 and parsed.day == 30):',
        )
    ],
)
# Student: every posting is dated one day late (off-by-one in the date of each transaction).
make(
    "v23_m03_posting_dated_one_day_late",
    [
        (
            '        day = _iso_date(entry["date"])',
            '        day = (date.fromisoformat(_iso_date(entry["date"])) + timedelta(days=1)).isoformat()',
        )
    ],
)
print("written")

# Writes three new round-21 student-error mutants of the reference solution into ledgers/AC1/mutants/.
# Usage: python -I mk_mutants21.py <checkout>
import sys
from pathlib import Path

checkout = Path(sys.argv[1])
ref = (checkout / "course/modules/AC/AC1/grader/reference.py").read_text(encoding="utf-8")
out = checkout / "ledgers/AC1/mutants"

def make(name: str, old: str, new: str) -> None:
    assert ref.count(old) == 1, (name, ref.count(old))
    (out / f"{name}.py").write_text(ref.replace(old, new), encoding="utf-8")

# Student: treats a zero amount as valid before the type check, so 0.0 is accepted.
make(
    "v21_m01_float_zero_amount_accepted",
    "def _cents(value: object) -> int:\n    if isinstance(value, bool) or not isinstance(value, Integral):",
    "def _cents(value: object) -> int:\n    if not isinstance(value, bool) and value == 0:\n        return 0\n"
    "    if isinstance(value, bool) or not isinstance(value, Integral):",
)
# Student: checks only that the day is 28 or later, so 2024-02-28 (not a month end in a leap year) is accepted.
make(
    "v21_m02_month_end_accepts_any_day_from_28",
    "    if parsed.day != calendar.monthrange(parsed.year, parsed.month)[1]:",
    "    if parsed.day < 28:",
)
# Student: a hard-coded month-length table that leaves November at 31 days.
make(
    "v21_m03_month_length_table_november_31",
    "    if parsed.day != calendar.monthrange(parsed.year, parsed.month)[1]:",
    "    lengths = {2: 29 if calendar.isleap(parsed.year) else 28, 4: 30, 6: 30, 9: 30, 11: 31}\n"
    "    if parsed.day != lengths.get(parsed.month, 31):",
)
print("written")

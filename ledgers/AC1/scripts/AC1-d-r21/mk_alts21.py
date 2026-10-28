# Writes two round-21 alternative correct implementations (different algorithms) from the reference solution.
# Usage: python -I mk_alts21.py <checkout> <outdir>
import sys
from pathlib import Path

ref = (Path(sys.argv[1]) / "course/modules/AC/AC1/grader/reference.py").read_text(encoding="utf-8")
out = Path(sys.argv[2])

def make(name: str, old: str, new: str) -> None:
    assert ref.count(old) == 1, (name, ref.count(old))
    (out / f"{name}.py").write_text(ref.replace(old, new), encoding="utf-8")

# Month end found by the next day changing month, not by the calendar length table.
make(
    "alt_r21_a_next_day_changes_month",
    "    if parsed.day != calendar.monthrange(parsed.year, parsed.month)[1]:",
    "    if (parsed + timedelta(days=1)).month == parsed.month:",
)
# Exact int type check (bool already excluded) instead of the numbers.Integral test.
make(
    "alt_r21_b_exact_int_type",
    "    if isinstance(value, bool) or not isinstance(value, Integral):",
    "    if type(value) is not int:",
)
print("written")

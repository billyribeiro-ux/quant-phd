"""Round 23: three new student-error mutants of the Lab 1 twin of L02 (written into ledgers/AC4/mutants/AC4-a-r23/)."""
from pathlib import Path
import sys

ROOT = Path(sys.argv[1])
src = (ROOT / "tests/labs/AC4/lab-AC4-L02-1.py").read_text(encoding="utf-8")
out = ROOT / "ledgers/AC4/mutants/AC4-a-r23"
out.mkdir(parents=True, exist_ok=True)
mutants = {
    # s01: share of plan measured against the upper break-even instead of the plan
    "L02_s01_share_over_break_even.py": (
        "share_of_planned {float(safety / PLANNED_UNITS * 100):.2f}",
        "share_of_planned {float(safety / upper * 100):.2f}"),
    # s02: step applied from 2000 units inclusive (a >= student error)
    "L02_s02_step_at_or_above_2000.py": (
        "step = STEP_CENTS if units > STEP_ABOVE_UNITS else 0",
        "step = STEP_CENTS if units >= STEP_ABOVE_UNITS else 0"),
    # s03: printed sensitivity truncated instead of rounded half up
    "L02_s03_sensitivity_truncated.py": (
        "fixed_plus_10000_cents_moves_break_even_units {float(raised - first):.2f}",
        "fixed_plus_10000_cents_moves_break_even_units {int(float(raised - first) * 100) / 100:.2f}"),
}
for name, (old, new) in mutants.items():
    assert src.count(old) == 1, name
    (out / name).write_text(src.replace(old, new), encoding="utf-8")
    print("wrote", name)

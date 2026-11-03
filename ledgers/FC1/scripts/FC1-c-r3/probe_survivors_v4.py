"""Compare the two surviving mutants with reference.py on inputs the suite does not use (repo-relative paths; run without -I)."""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(ROOT / "course/modules/FC/FC1/grader/reference.py", "ref")
cases = [
    ("Bond(10000,500,24) @400 bps price", lambda m: m.bond_price_cents(m.Bond(10_000, 500, 24), 400)),
    ("Bond(10000,500,21) events length", lambda m: len(m.Bond(10_000, 500, 21).events())),
    ("Bond(10**10+1,0,1) @10000 bps price (exact half)", lambda m: m.bond_price_cents(m.Bond(10**10 + 1, 0, 1), 10_000)),
    ("Bond(10**12+1,0,1) @10000 bps price (exact half)", lambda m: m.bond_price_cents(m.Bond(10**12 + 1, 0, 1), 10_000)),
    ("Bond(10000,500,3) @400 bps price (rounding fixture)", lambda m: m.bond_price_cents(m.Bond(10_000, 500, 3), 400)),
]
for name in ["r3c_schedule_stops_at_twenty_periods", "r3c_price_ten_digits_integral_rounding"]:
    mut = load(ROOT / "ledgers/FC1/mutants" / f"{name}.py", name)
    print(f"== {name}")
    for label, f in cases:
        r, m = f(ref), f(mut)
        print(f"  {label}: reference={r} mutant={m} differ={r != m}")

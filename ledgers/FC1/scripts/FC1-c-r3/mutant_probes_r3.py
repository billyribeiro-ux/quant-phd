"""Round-3 probes (verifier D3): the two survivors against the reference fixtures. Read-only. Usage: <checkout root>."""
import importlib.util
import sys
from fractions import Fraction as F
from pathlib import Path

root = Path(sys.argv[1])
mut_dir = root / "ledgers/FC1/mutants"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(root / "course/modules/FC/FC1/grader/reference.py", "ref")
cap = load(mut_dir / "r3c_schedule_stops_at_twenty_periods.py", "cap")
dec = load(mut_dir / "r3c_price_ten_digits_integral_rounding.py", "dec")


def half(x):
    m = abs(x)
    w = (2 * m.numerator + m.denominator) // (2 * m.denominator)
    return w if x >= 0 else -w


def oracle_events(face, c, n):
    coupon = half(F(face * c, 10000))
    rows = [(t, coupon) for t in range(1, n + 1)]
    rows[-1] = (n, coupon + face)
    return rows


print("cap mutant events == oracle, Bond(10000,500,24):", cap.Bond(10000, 500, 24).events() == oracle_events(10000, 500, 24))
print("cap mutant events == oracle, Bond(10000,500,15):", cap.Bond(10000, 500, 15).events() == oracle_events(10000, 500, 15))
print("reference events == oracle, Bond(10000,500,24):", ref.Bond(10000, 500, 24).events() == oracle_events(10000, 500, 24))
print("dec mutant Bond(10**12+1,0,1) at 10000:", dec.bond_price_cents(dec.Bond(10**12 + 1, 0, 1), 10000))
print("reference Bond(10**12+1,0,1) at 10000:", ref.bond_price_cents(ref.Bond(10**12 + 1, 0, 1), 10000), "(exact half, expected 500000000001)")
print("dec mutant Bond(10000,500,3) at 400:", dec.bond_price_cents(dec.Bond(10000, 500, 3), 400), "reference:", ref.bond_price_cents(ref.Bond(10000, 500, 3), 400))

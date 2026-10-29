"""Round-12 probe: the exact present value of Bond(1704285, 179, 1) at 496 bps is exactly 1652812.5 cents, so the
rule (exact, one rounding, half away from zero) gives 1652813. Float discounting (r12n03 and alternative a5) gives
1652812. Run from the checkout root: python3 ledgers/FC1/scripts/FC1-c-r12/exact_half_probe.py"""

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


coupon = Fraction(1704285 * 179, 10_000)
coupon_cents = int(coupon + Fraction(1, 2))  # 30506.7015 rounds to 30507
event = coupon_cents + 1704285
exact = Fraction(event) / (1 + Fraction(496, 10_000))
print("coupon exact:", float(coupon), "rounded:", coupon_cents)
print("single event:", event, "exact present value:", exact, "is an exact half:", exact.denominator == 2)
ref = load(ROOT / "course/modules/FC/FC1/grader/reference.py", "ref")
mut = load(ROOT / "ledgers/FC1/mutants/r12n03_float_discounting_then_half_up.py", "mut")
alt = load(ROOT / "ledgers/FC1/alternatives/a5_float_discounting_exact_half_up.py", "a5")
print("reference:", ref.bond_price_cents(ref.Bond(1704285, 179, 1), 496))
print("r12n03 float mutant:", mut.bond_price_cents(mut.Bond(1704285, 179, 1), 496))
print("alternative a5:", alt.bond_price_cents(alt.Bond(1704285, 179, 1), 496))
sys.exit(0)

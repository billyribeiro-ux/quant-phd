"""Round-6 verifier (E1-d) generates its own student-error mutants and alternative correct implementations.

Each mutant is reference.py with one targeted edit and a new first docstring line naming the error.
Run from the checkout root: python ledgers/E1/scripts/E1-d-r6/make_r6_mutants.py
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/E/E1/grader/reference.py").read_text(encoding="utf-8")
MUT = ROOT / "ledgers/E1/mutants"
ALT = ROOT / "ledgers/E1/scripts/E1-d-r6"


def edit(src: str, old: str, new: str, count: int = 1) -> str:
    assert src.count(old) == count, (old, src.count(old))
    return src.replace(old, new)


def mutant(name: str, description: str, body: str) -> None:
    text = body.replace('"""Reference solution', '"""' + description + "\n\nReference solution", 1)
    assert text.startswith('"""' + description), name
    (MUT / f"{name}.py").write_text(text, encoding="utf-8")


# Mutant 1: half_up computed in binary floating point, which is wrong on large exact fractions.
m1 = edit(
    REF,
    "    return math.floor(x + Fraction(1, 2))",
    "    return math.floor(float(x) + 0.5)",
)
mutant(
    "r6d_m01_half_up_in_float_wrong_for_large_inputs",
    "Student rounds with float(x) + 0.5, which is exact on small cases but loses the half on large exact fractions.",
    m1,
)

# Mutant 2: profit taken as revenue (fee times volume) instead of margin over cost.
m2 = edit(REF, "    profit = (fee - c) * volume", "    profit = fee * volume")
mutant(
    "r6d_m02_profit_is_revenue_not_margin",
    "Student takes exchange profit as fee times volume (revenue), forgetting the cost c per trade.",
    m2,
)

# Mutant 3: over-constrained input check, rejects a < 2*b*c as if the gap had to cover the cost twice.
m3 = edit(
    REF,
    "    if a <= b * c:\n        raise ValueError(\"a must exceed b*c\")",
    "    if a < 2 * b * c:\n        raise ValueError(\"a must exceed b*c\")",
)
mutant(
    "r6d_m03_a_must_cover_cost_twice",
    "Student over-constrains the input: rejects a < 2*b*c, so valid cases with bc < a < 2bc raise ValueError.",
    m3,
)

# Alternative correct implementation 1: integer rational arithmetic, no Fraction, half-up by integer division.
ALT1 = '''"""Alternative 1: exact rationals as (numerator, denominator) integer pairs; half-up by integer arithmetic."""
from __future__ import annotations

STRUCTURES = ("monopoly", "cournot", "bertrand")


def _round_half_up(num: int, den: int) -> int:
    assert num >= 0 and den > 0
    return (2 * num + den) // (2 * den)


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if not isinstance(structure, str) or structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
    d = a - b * c
    if structure == "monopoly":
        vn, vd = d, 2
        fn, fd = a + b * c, 2 * b
    elif structure == "cournot":
        vn, vd = 2 * d, 3
        fn, fd = a + 2 * b * c, 3 * b
    else:
        vn, vd = d, 1
        fn, fd = c, 1
    # profit = (fee - c) * volume, all as one fraction
    pn, pd = (fn - c * fd) * vn, fd * vd
    # consumer = volume^2 / (2b)
    cn, cd = vn * vn, vd * vd * 2 * b
    # welfare = consumer + profit
    wn, wd = cn * pd + pn * cd, cd * pd
    # deadweight = (d - volume)^2 / (2b)
    dn, dd = (d * vd - vn) ** 2, vd * vd * 2 * b
    return {
        "volume_trades": _round_half_up(vn, vd),
        "fee_cents": _round_half_up(fn, fd),
        "profit_cents": _round_half_up(pn, pd),
        "consumer_surplus_cents": _round_half_up(cn, cd),
        "welfare_cents": _round_half_up(wn, wd),
        "deadweight_loss_cents": _round_half_up(dn, dd),
    }
'''

# Alternative correct implementation 2: decimal arithmetic at 60 digits with ROUND_HALF_UP.
ALT2 = '''"""Alternative 2: Decimal at 60 significant digits, quantized with ROUND_HALF_UP."""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, getcontext

getcontext().prec = 60
STRUCTURES = ("monopoly", "cournot", "bertrand")


def _r(x: Decimal) -> int:
    return int(x.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    if not isinstance(structure, str) or structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
    A, B, C = Decimal(a), Decimal(b), Decimal(c)
    d = A - B * C
    if structure == "monopoly":
        vol, fee = d / 2, (A + B * C) / (2 * B)
    elif structure == "cournot":
        vol, fee = 2 * d / 3, (A + 2 * B * C) / (3 * B)
    else:
        vol, fee = d, C
    profit = (fee - C) * vol
    cons = vol * vol / (2 * B)
    welf = cons + profit
    dwl = (d - vol) ** 2 / (2 * B)
    return {
        "volume_trades": _r(vol),
        "fee_cents": _r(fee),
        "profit_cents": _r(profit),
        "consumer_surplus_cents": _r(cons),
        "welfare_cents": _r(welf),
        "deadweight_loss_cents": _r(dwl),
    }
'''

# Alternative correct implementation 3: Cournot volume from solving the 2x2 linear system by Cramer's rule.
alt3 = edit(
    REF,
    "        volume = 2 * d / 3\n        fee = Fraction(a + 2 * b * c, 3 * b)",
    "        # symmetric quantity q_1 = q_2 = d / 3 (from 2 q_i + q_j = d); volume is q_1 + q_2, fee is inverse demand\n"
    "        q = Fraction(d, 3)\n"
    "        volume = q + q\n"
    "        fee = (a - volume) / b",
)

# Alternative correct implementation 4: consumer surplus by numerical trapezoid over 2 panels, exact for linear.
alt4 = edit(
    REF,
    "    consumer = volume * volume / (2 * b)",
    "    def f(t: Fraction) -> Fraction:\n"
    "        return (a - t) / b\n"
    "    mid = volume / 2\n"
    "    consumer = (volume / 4) * (f(Fraction(0)) + 2 * f(mid) + f(volume)) - fee * volume",
)

# Alternative correct implementation 5: monopoly and Bertrand by search over the exact boundary of the fee; Cournot
# by iterating the reaction map to its fixed point (the iteration is exact only in the limit, so this variant instead
# solves the fixed point of q = (d - q)/2 with Fraction arithmetic in closed form).
alt5 = None

for name, src in (("alt1_integer_pairs", ALT1), ("alt2_decimal_half_up", ALT2), ("alt3_cramer", alt3),
                  ("alt4_trapezoid_consumer", alt4)):
    (ALT / f"{name}.py").write_text(src, encoding="utf-8")
print("written")

# Mutant 4: welfare counts only half the consumer surplus (a plausible reading error of the surplus identity).
m4 = edit(REF, "    welfare = consumer + profit", "    welfare = consumer / 2 + profit")
mutant(
    "r6d_m04_welfare_takes_half_consumer_surplus",
    "Student reads welfare as half the consumer surplus plus profit, misapplying the surplus identity.",
    m4,
)

# Mutant 5: monopoly fee sign error on the cost term: (a - b*c) / (2b) instead of (a + b*c) / (2b).
m5 = edit(REF, "        fee = Fraction(a + b * c, 2 * b)", "        fee = Fraction(a - b * c, 2 * b)")
mutant(
    "r6d_m05_monopoly_fee_sign_error_on_cost",
    "Student has a sign error in the monopoly fee: (a - b*c)/(2b) instead of (a + b*c)/(2b).",
    m5,
)

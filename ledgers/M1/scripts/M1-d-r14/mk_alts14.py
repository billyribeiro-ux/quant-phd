"""Writes three new correct alternative annuity engines by editing the reference (run from the checkout).

Each keeps the public names and the exact-tie rule; only the rounding or the exact-rate helper differs.
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
REF = ROOT / "course/modules/M/M1/grader/reference.py"
OUT = ROOT / "ledgers/M1/scripts/M1-d-r14/alts"
src = REF.read_text(encoding="utf-8")

NEAREST_OLD = "    return math.floor(amount + Fraction(1, 2))\n"
RATE_OLD = '    return Fraction(repr(annual_rate))\n'

a = src.replace(
    NEAREST_OLD,
    "    from decimal import ROUND_HALF_UP, Decimal, localcontext\n"
    "    with localcontext() as ctx:\n"
    "        ctx.prec = 80\n"
    "        quotient = Decimal(amount.numerator) / Decimal(amount.denominator)\n"
    "        return int(quotient.quantize(Decimal(1), rounding=ROUND_HALF_UP))\n",
)
assert a != src
(OUT / "alt_r14_a_decimal_half_up_cents.py").write_text(a, encoding="utf-8")

b = src.replace(NEAREST_OLD, "    return (2 * amount.numerator + amount.denominator) // (2 * amount.denominator)\n")
assert b != src
(OUT / "alt_r14_b_integer_half_up_formula.py").write_text(b, encoding="utf-8")

c = src.replace(
    RATE_OLD,
    "    from decimal import Decimal\n    return Fraction(Decimal(repr(annual_rate)))\n",
)
assert c != src
(OUT / "alt_r14_c_decimal_rate_reader.py").write_text(c, encoding="utf-8")
print("wrote 3 alternatives")

"""Round 17: writes three correct alternative annuity_engine modules derived from the reference by replacing
the money arithmetic with different valid algorithms (integer half-up on Fraction ratios; direct summation of
discount factors; Decimal at 60 digits with ROUND_HALF_UP). Run with -I: python3 -I mk_alts17.py <ref> <outdir>."""
import sys
from pathlib import Path

ref = Path(sys.argv[1]).read_text(encoding="utf-8")
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

def sub(src: str, old: str, new: str) -> str:
    assert src.count(old) == 1, old[:60]
    return src.replace(old, new)

# a: integer half-up on the exact ratio (2a + b) // (2b); rate read via Decimal's string
a = sub(ref, "    return math.floor(amount + Fraction(1, 2))",
        "    return (2 * amount.numerator + amount.denominator) // (2 * amount.denominator)")
a = sub(a, "    return Fraction(repr(annual_rate))",
        "    from decimal import Decimal\n    return Fraction(Decimal(repr(annual_rate)))")
(out / "alt_r17_a_integer_half_up_ratio.py").write_text(a, encoding="utf-8")

# b: direct summation of the discount factors in exact arithmetic; float factor by expm1/log1p, no cutoff
b = sub(ref, "    return (1 - (1 + r) ** -n) / r",
        "    return -math.expm1(-n * math.log1p(r)) / r")
b = sub(b, "    return _nearest_cent(principal * i / (1 - (1 + i) ** -n))",
        "    denom = sum(((1 + i) ** -k for k in range(1, n + 1)), Fraction(0))\n    return _nearest_cent(principal / denom)")
(out / "alt_r17_b_direct_sum_discount_factors.py").write_text(b, encoding="utf-8")

# c: Decimal at 60 digits; ROUND_HALF_UP quantize to the cent for the payment and each interest amount
c = sub(ref, "from fractions import Fraction\n",
        "from decimal import ROUND_HALF_UP, Decimal, localcontext\nfrom fractions import Fraction\n")
c = sub(c, "    return _nearest_cent(principal * i / (1 - (1 + i) ** -n))",
        "    with localcontext() as ctx:\n        ctx.prec = 60\n        d_i = Decimal(i.numerator) / Decimal(i.denominator)\n        pay = Decimal(principal) * d_i / (1 - (1 + d_i) ** (-n))\n        return int(pay.quantize(Decimal(1), rounding=ROUND_HALF_UP))")
c = sub(c, "        interest = _nearest_cent(opening * i)",
        "        with localcontext() as ctx:\n            ctx.prec = 60\n            interest = int((Decimal(opening) * Decimal(i.numerator) / Decimal(i.denominator)).quantize(Decimal(1), rounding=ROUND_HALF_UP))")
(out / "alt_r17_c_decimal_half_up.py").write_text(c, encoding="utf-8")
print("wrote", sorted(p.name for p in out.iterdir()))

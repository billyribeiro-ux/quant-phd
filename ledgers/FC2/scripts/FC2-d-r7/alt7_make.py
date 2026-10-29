import sys
from pathlib import Path
src = Path("/tmp/fc2d-r7-alt7b/reference.py").read_text()
old_half = src[src.index("def _half_up"):src.index("def _check_df")]
new_half = '''def _half_up(x: Fraction) -> int:
    """Alternative: Decimal floor of x + 1/2 (same ties-toward-plus-infinity rule)."""
    from decimal import ROUND_FLOOR, Decimal, localcontext

    with localcontext() as ctx:
        ctx.prec = 80
        d = Decimal(x.numerator) / Decimal(x.denominator) + Decimal("0.5")
        return int(d.to_integral_value(rounding=ROUND_FLOOR))


'''
src = src.replace(old_half, new_half)
old_sd = src[src.index("def _second_difference"):src.index("def convexity_violations")]
new_sd = '''def _second_difference(strikes: list[int], calls: list[int], j: int) -> Fraction:
    """Alternative: Lagrange chord in integer cross-multiplied form, returned as an exact Fraction."""
    low, mid, high = strikes[j - 1], strikes[j], strikes[j + 1]
    num = (high - mid) * calls[j - 1] + (mid - low) * calls[j + 1] - (high - low) * calls[j]
    return Fraction(num, high - low)


'''
src = src.replace(old_sd, new_sd)
Path("/tmp/fc2d-r7-alt7b/scanner.py").write_text(src)
print("written")

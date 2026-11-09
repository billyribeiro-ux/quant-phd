"""Round 1 verifier checks for slice c (L07-L08): displayed-digit arithmetic and the lab rounding rule.

Standard library only. Run:
    .venv/bin/python -I ledgers/FC2/scripts/FC2-c-r1/v1_digits_and_rounding.py
"""

from __future__ import annotations

import math


def cents_as_in_lab(amount: float) -> int:
    """The rounding function written in tests/labs/FC2/lab-FC2-L07-1.py (sign handled separately)."""
    sign = -1 if amount < 0 else 1
    return sign * math.floor(abs(amount) * 100 + 0.5)


def half_up(amount: float) -> int:
    """Half toward +infinity, the reading of 'rounded half up' on the page."""
    return math.floor(amount * 100 + 0.5)


def main() -> None:
    # 1. Problem M3 of L07 writes q(4) = (1.012578 - 0.904837)/(1.105171 - 0.904837) = 0.537808.
    prose = (1.012578 - 0.904837) / (1.105171 - 0.904837)
    exact = (math.exp(0.05 * 0.25) - math.exp(-0.2 * 0.5)) / (math.exp(0.2 * 0.5) - math.exp(-0.2 * 0.5))
    print(f"M3 displayed-digit arithmetic: {prose:.7f} -> 6dp {prose:.6f}; page prints 0.537808")
    print(f"M3 unrounded q(4): {exact:.7f} -> 6dp {exact:.6f}")

    # 2. Rounding rule: page says 'rounded half up'; lab code rounds negatives away from zero.
    for x in (-0.005, 0.005, -0.015, 0.015):
        print(f"x={x:+.3f} cents_as_in_lab={cents_as_in_lab(x * 100 / 100)} half_up={half_up(x)}")
    # The lab's printed error values are not exact half-cent ties (distance from .5 cent):
    errs_cents = [171.170139, -91.008223, 35.535035, -19.717453, 7.038205, -3.989203, -1.997191, -0.999231, -0.499773]
    dist = min(abs(abs(e - math.trunc(e)) - 0.5) for e in errs_cents)
    print(f"smallest distance of a printed error (cents) from a half-cent tie: {dist:.6f}")
    prices = [1216.228496, 954.050134, 1080.593392, 1025.340904, 1052.096562, 1041.069154, 1043.061166, 1044.059126, 1044.558584]
    dist_p = min(abs((p - math.floor(p)) - 0.5) for p in prices)
    print(f"smallest distance of a printed tree price (cents) from a half-cent tie: {dist_p:.6f}")


if __name__ == "__main__":
    main()

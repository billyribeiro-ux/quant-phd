"""Independent re-derivation of the L06 numbers (PC3-b round 10). Standard library only, exact fractions where possible.

Written from the statements of course/modules/PC/PC3/L06.html (Propositions 2.1, 3.1, 3.2, Corollary 3.3, Example 4.2,
Remark 4.3, Problems M1-M3, E1-E3, R2, R3), not from the lab code.
Run as: python -I -W error ledgers/PC3/scripts/PC3-b-r10/l06_indep.py  (from the checkout root)
"""

from __future__ import annotations

import itertools
import math
import random
from fractions import Fraction


def annuity(r: Fraction) -> Fraction:
    return sum((1 / (1 + r) ** t for t in range(1, 4)), Fraction(0))


def npv(cfs: list[Fraction], r: Fraction) -> Fraction:
    return sum((c / (1 + r) ** t for t, c in enumerate(cfs)), Fraction(0))


OUT = Fraction(15_000_000)
MARGIN = Fraction(5_000)


def main() -> None:
    r10 = Fraction(10, 100)
    A = annuity(r10)
    print(f"A(10%) = {A} = {float(A):.6f}; expected 3310/1331: {A == Fraction(3310, 1331)}")
    be = OUT / (MARGIN * A)
    print(f"break-even units at 10% = {be} = {float(be):.6f}; equals 399300/331: {be == Fraction(399300, 331)}")

    # Example 4.2 Fermi bounds by brute force over the factor ends and a grid
    lo = min(c * o * s for c, o, s in itertools.product((2000, 4000), (1, 2), (Fraction(1, 10), Fraction(1, 5))))
    hi = max(c * o * s for c, o, s in itertools.product((2000, 4000), (1, 2), (Fraction(1, 10), Fraction(1, 5))))
    rng = random.Random(7)
    inside = True
    for _ in range(20000):
        c = rng.uniform(2000, 4000)
        o = rng.uniform(1, 2)
        s = rng.uniform(0.1, 0.2)
        p = c * o * s
        if not (float(lo) - 1e-9 <= p <= float(hi) + 1e-9):
            inside = False
    print(f"Example 4.2 product bounds: lower {lo}, upper {hi}; random interior points inside: {inside}")

    # Prop 3.1: NPV(u) = -I + m A u, affine, increasing, zero at u*
    ok = True
    for _ in range(300):
        n = rng.randint(1, 6)
        rate = Fraction(rng.randint(-50, 300), 1000)
        I = Fraction(rng.randint(1, 10_000))
        m = Fraction(rng.randint(1, 10_000))
        u = Fraction(rng.randint(0, 5000))
        A_n = sum((1 / (1 + rate) ** t for t in range(1, n + 1)), Fraction(0))
        cfs = [-I] + [u * m] * n
        if npv(cfs, rate) != -I + m * A_n * u:
            ok = False
    print(f"Prop 3.1 identity NPV(u) = -I + mAu on random inputs: {ok}")

    # M2: NPV at 10% of -100, 60, 60
    m2 = npv([Fraction(-100), Fraction(60), Fraction(60)], r10)
    print(f"M2 NPV = {m2} = {float(m2):.4f}; equals 500/121: {m2 == Fraction(500, 121)}")

    # M3: break-even for outlay 100000, margin 400, 10%
    m3 = Fraction(100_000) / (Fraction(400) * A)
    print(f"M3 break-even = {m3} = {float(m3):.4f}; equals 33275/331: {m3 == Fraction(33275, 331)}")

    # Lab Part 2 values at 8, 10, 12 percent
    for rate in (Fraction(8, 100), Fraction(10, 100), Fraction(12, 100)):
        Ar = annuity(rate)
        bev = OUT / (MARGIN * Ar)
        nl = npv([-OUT] + [Fraction(200) * MARGIN] * 3, rate)
        nu = npv([-OUT] + [Fraction(1600) * MARGIN] * 3, rate)
        print(f"rate {rate}: A={float(Ar):.7f} break-even={float(bev):.4f} NPV(200)={float(nl):.2f} NPV(1600)={float(nu):.2f}")
        print(f"   lower NPV half-up cents = {math.floor(nl + Fraction(1, 2))}, upper = {math.floor(nu + Fraction(1, 2))}")
    be8 = OUT / (MARGIN * annuity(Fraction(8, 100)))
    be12 = OUT / (MARGIN * annuity(Fraction(12, 100)))
    print(f"unrounded break-evens: 8%={float(be8):.4f} 10%={float(be):.4f} 12%={float(be12):.4f}")
    print(f"width 8->12 = {float(be12 - be8):.4f}; per point = {float((be12 - be8) / 4):.4f}")
    print(f"8->10 = {float(be - be8):.4f}; 10->12 = {float(be12 - be):.4f}; 1249.05-1206.34 = {round(1249.05 - 1206.34, 2)}")

    # E1: annuity at 12% by the explicit sum, break-even
    e1 = 1 / 1.12 + 1 / 1.2544 + 1 / 1.404928
    print(f"E1 annuity at 12% (explicit) = {e1:.5f}; 3000/that = {3000 / e1:.2f}")

    # E2: NPV at 1200 and 1300 units at 10%, and grid positivity
    n1200 = npv([-OUT] + [Fraction(1200) * MARGIN] * 3, r10)
    n1300 = npv([-OUT] + [Fraction(1300) * MARGIN] * 3, r10)
    print(f"E2 NPV(1200) = {n1200} = {float(n1200):.2f}; equals -105000000/1331: {n1200 == Fraction(-105000000, 1331)}")
    print(f"E2 NPV(1300) = {n1300} = {float(n1300):.2f}; equals 1550000000/1331: {n1300 == Fraction(1550000000, 1331)}")
    grid = list(range(200, 1601, 100))
    pos = [u for u in grid if npv([-OUT] + [Fraction(u) * MARGIN] * 3, r10) > 0]
    neg = [u for u in grid if npv([-OUT] + [Fraction(u) * MARGIN] * 3, r10) < 0]
    print(f"E2 positive grid points {pos} (count {len(pos)}); largest negative grid point {max(neg)}")

    # R3: margin for break-even at 1600
    mstar = OUT / (Fraction(1600) * A)
    print(f"R3 margin m* = {float(mstar):.4f} cents; ratio to 5000 = {float(mstar / 5000):.5f};"
          f" fall = {float(1 - mstar / 5000) * 100:.3f} percent")

    # Remark 2.2: S/D = S e^{r tau} with D = e^{-r tau}
    S, r, tau = 100.0, 0.05, 2.0
    print(f"Remark 2.2 S/D == S*exp(r*tau): {abs(S / math.exp(-r * tau) - S * math.exp(r * tau)) < 1e-9}")

    # Prop 2.1 (ii): reverse portfolio payoff is S/D - F' in every state; check M1
    print(f"M1 F = 4900/0.98 = {Fraction(4900) / Fraction(98, 100)}; payoff 5050 - that = {Fraction(5050) - Fraction(4900) / Fraction(98, 100)}")

    # Corollary 3.3 example: range straddles break-even, bounds give opposite signs
    print(f"Example 4.2 NPV at 200 and 1600 units: {float(npv([-OUT] + [Fraction(200) * MARGIN] * 3, r10)):.2f}, "
          f"{float(npv([-OUT] + [Fraction(1600) * MARGIN] * 3, r10)):.2f}")

    # Lab Part 1 forward check: payoff at expiry for spot values 8000..12000 with F = 10000 and F = 10100
    S0 = Fraction(9700)
    D = Fraction(97, 100)
    F = S0 / D
    pay0 = [Fraction(st) + (F - Fraction(st)) - S0 / D for st in (8000, 9000, 10000, 11000, 12000)]
    pay1 = [Fraction(st) + (Fraction(10100) - Fraction(st)) - S0 / D for st in (8000, 9000, 10000, 11000, 12000)]
    print(f"Part 1: F = {F}; payoffs at F: {[str(x) for x in pay0]}; at 10100: {[str(x) for x in pay1]}")


if __name__ == "__main__":
    main()

"""Lab AC4-L07-1: the transfer-price range under a capacity constraint, on SIMULATED divisions.

Every division here is SIMULATED: the cases come from a seeded generator, no firm is represented,
and no figure estimates any real company. Money is in integer cents (1 SCU = 100 cents); quantities
are integer units. Transfer prices are exact Fractions of cents. They are shown to two decimal places only when printed,
and every check uses the exact value.

Model (stated on the page): supplier S makes one intermediate good at variable cost v per unit with
capacity K units. S also sells E units externally at market price p_m (E <= K). Buyer B asks for q
units. B's net contribution per unit before the transfer price is r_net. Fixed costs are unaffected.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction

SEED = 20261027
N_CASES = 200


@dataclass(frozen=True)
class Case:
    """One SIMULATED division pair. Money in integer cents; quantities in units."""

    case_id: int
    v: int
    p_m: int
    capacity: int
    external: int
    q: int
    r_net: int

    def __post_init__(self) -> None:
        if min(self.v, self.p_m, self.capacity, self.external, self.q) < 0:
            raise ValueError("costs, prices, capacity and quantities must be non-negative")
        if self.external > self.capacity:
            raise ValueError("external demand must fit within capacity (E <= K)")


def displaced(c: Case) -> int:
    """External units lost to the internal order: max(0, q + E - K). Requires q <= K."""
    if c.q > c.capacity:
        raise ValueError("q exceeds capacity: no transfer is feasible")
    return max(0, c.q - c.capacity)


def t_min(c: Case) -> Fraction:
    """Lowest transfer price at which the supplier is no worse off: v + D(p_m - v)/q."""
    if c.q <= 0:
        raise ValueError("q must be positive")
    return Fraction(c.v) + Fraction(displaced(c) * (c.p_m - c.v), c.q)


def t_max(c: Case) -> Fraction:
    """Highest transfer price at which the buyer is no worse off: r_net."""
    return Fraction(c.r_net)


def supplier_increment(c: Case, t: Fraction) -> Fraction:
    """Supplier's gain from accepting the order at price t, against refusing it."""
    return Fraction(c.q) * (t - c.v) - displaced(c) * (c.p_m - c.v)


def buyer_increment(c: Case, t: Fraction) -> Fraction:
    """Buyer's gain from buying q units at price t."""
    return c.q * (Fraction(c.r_net) - t)


def firm_surplus(c: Case) -> int:
    """Firm-wide gain from the transfer, independent of t: q(r_net - v) - D(p_m - v)."""
    return c.q * (c.r_net - c.v) - displaced(c) * (c.p_m - c.v)


# Hand-built boundary pair: the worked case of the page (v = 40, p_m = 60, K = 10,000, E = 8,000, q = 5,000
# units, so D = 3,000) with r = 52 SCU. Then t_min = t_max = 52 SCU and the firm-wide surplus is exactly 0.
BOUNDARY = Case(case_id=0, v=4000, p_m=6000, capacity=10000, external=8000, q=5000, r_net=5200)


def generate(seed: int, n: int) -> list[Case]:
    """Generate n SIMULATED cases from a seeded generator."""
    rng = random.Random(seed)
    cases: list[Case] = []
    for case_id in range(1, n + 1):
        v = rng.randrange(3000, 5001, 100)
        p_m = v + rng.randrange(500, 3001, 100)
        capacity = rng.randrange(6000, 12001, 500)
        external = rng.randint(4000, min(9000, capacity))
        q = rng.randint(1000, 8000)
        r_net = v + rng.randint(-1500, 4000)
        cases.append(Case(case_id, v, p_m, capacity, external, q, r_net))
    return cases


def show(x: Fraction) -> str:
    """Print an exact cents amount to two decimals (display only)."""
    value = (Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{value}"


def main() -> None:
    cases = [*generate(SEED, N_CASES), BOUNDARY]
    print(f"SIMULATED divisions (seed {SEED}): {N_CASES} generated cases and 1 hand-built boundary case;")
    print("money in cents, quantities in units")
    print("case  v      p_m    K      E      q      D     t_min     t_max     status")
    for c in cases[:6]:
        status = "no transfer (q > K)"
        tmin_text, tmax_text = "-", show(t_max(c))
        if c.q <= c.capacity:
            lo = t_min(c)
            tmin_text = show(lo)
            status = "feasible" if lo <= t_max(c) else "empty range"
        d_text = str(displaced(c)) if c.q <= c.capacity else "-"
        print(
            f"{c.case_id:>4}  {c.v:>5}  {c.p_m:>5}  {c.capacity:>5}  {c.external:>5}  {c.q:>5}  "
            f"{d_text:>5}  {tmin_text:>8}  {tmax_text:>8}  {status}"
        )

    over = [c for c in cases if c.q > c.capacity]
    fits = [c for c in cases if c.q <= c.capacity]
    empty = [c for c in fits if t_min(c) > t_max(c)]
    feasible = [c for c in fits if t_min(c) <= t_max(c)]
    binding = [c for c in feasible if displaced(c) > 0]
    print(f"cases with q > K (no transfer): {len(over)}")
    print(f"cases with q <= K and an empty range: {len(empty)}")
    print(f"cases with a feasible range: {len(feasible)}")
    print(f"  of which capacity binds (D > 0): {len(binding)}")
    b = BOUNDARY
    print(
        f"boundary case (hand-built): t_min {show(t_min(b))}, t_max {show(t_max(b))}, "
        f"firm-wide surplus {firm_surplus(b)} cents"
    )

    checks = 0
    for c in fits:
        lo, hi = t_min(c), t_max(c)
        assert supplier_increment(c, lo) == 0
        assert buyer_increment(c, hi) == 0
        assert (lo <= hi) == (firm_surplus(c) >= 0)
        if lo <= hi:
            for t in (lo, hi, (lo + hi) / 2):
                assert supplier_increment(c, t) + buyer_increment(c, t) == firm_surplus(c)
        checks += 1
    print(f"exact checks passed: {checks}/{len(fits)} cases with q <= K")


main()

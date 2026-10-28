"""Lab AC4-L08-1: residual income and EVA on SIMULATED divisions.

Every division here is SIMULATED: the figures come from a seeded generator, no firm is represented,
and no figure estimates any real company. Money is in integer cents (1 SCU = 100 cents). The tax rate
and the capital-charge rate are stated inputs, in basis points (1 bp = 0.01 percent). Their values are
set here by the lab, not derived; the lesson does not derive a cost of capital.

Definitions (stated on the page):
  residual income  RI  = OI - r * C
  NOPAT                 = OI * (1 - tax)
  EVA              = NOPAT - r * C
where OI is operating income for the period, C is invested capital (a stated base), r is the
capital-charge rate and tax is the tax rate applied to OI.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, replace
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction

SEED = 20261027
N_DIVISIONS = 8
TAX_BP = 2000
RATE_BP = 900
SPEND = 10000
LIFE_YEARS = 5


@dataclass(frozen=True)
class Division:
    """One SIMULATED division for one period. Money in integer cents."""

    name: str
    invested: int
    oi: int

    def __post_init__(self) -> None:
        if self.invested <= 0:
            raise ValueError("invested capital must be positive")


def residual_income(d: Division) -> Fraction:
    """RI = OI - r * C, in cents."""
    return Fraction(d.oi) - Fraction(RATE_BP, 10_000) * d.invested


def eva(d: Division) -> Fraction:
    """EVA = OI * (1 - tax) - r * C, in cents."""
    nopat = Fraction(d.oi) * (10_000 - TAX_BP) / 10_000
    return nopat - Fraction(RATE_BP, 10_000) * d.invested


def return_ratio(d: Division) -> Fraction:
    """OI / C, a dimensionless ratio on the stated capital base."""
    return Fraction(d.oi, d.invested)


def generate(seed: int, n: int) -> list[Division]:
    """n SIMULATED divisions. C is a multiple of 1000 cents; OI/C lies in [4%, 5/31], so at most 16.13%."""
    rng = random.Random(seed)
    out: list[Division] = []
    for i in range(n):
        invested = rng.randrange(20_000, 200_001, 1000)
        oi = 5 * rng.randint(invested // 125, invested // 31)
        out.append(Division(f"SIM-{chr(ord('A') + i)}", invested, oi))
    return out


def capitalized(d: Division) -> Division:
    """Treat a SPEND outlay as an asset amortized straight-line over LIFE_YEARS, first year only.

    Reported OI already charges the outlay in full. Capitalizing adds it back to OI net of the first
    year's amortization, and adds the unamortized balance to C. Tax effects of the choice are not modeled.
    """
    first_year = SPEND // LIFE_YEARS
    return replace(d, invested=d.invested + SPEND, oi=d.oi + SPEND)


def show(x: Fraction) -> str:
    """Print an exact cents amount to two decimals (display only)."""
    value = (Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{value}"


def main() -> None:
    divisions = generate(SEED, N_DIVISIONS)
    print(f"SIMULATED divisions (seed {SEED}); tax {TAX_BP} bp, capital charge {RATE_BP} bp; money in cents")
    print("name      C         OI      OI/C %   RI          EVA")
    for d in divisions:
        print(
            f"{d.name:<8} {d.invested:>8} {d.oi:>9} {show(100 * return_ratio(d)):>8}"
            f" {show(residual_income(d)):>11} {show(eva(d)):>11}"
        )

    gap_ok = [eva(d) - residual_income(d) == -Fraction(TAX_BP, 10_000) * d.oi for d in divisions]
    sign_ok = [(residual_income(d) >= 0) == (return_ratio(d) >= Fraction(RATE_BP, 10_000)) for d in divisions]
    print(f"identity EVA - RI = -tax * OI holds for {sum(gap_ok)}/{N_DIVISIONS} divisions")
    print(f"RI >= 0 exactly when OI/C >= r holds for {sum(sign_ok)}/{N_DIVISIONS} divisions")

    discordant: list[tuple[str, str]] = []
    for a in divisions:
        for b in divisions:
            if a.name < b.name:
                by_ri = residual_income(a) - residual_income(b)
                by_ratio = return_ratio(a) - return_ratio(b)
                if (by_ri > 0) != (by_ratio > 0) and by_ri != 0 and by_ratio != 0:
                    discordant.append((a.name, b.name))
    print(f"pairs ranked differently by RI and by OI/C: {len(discordant)} of {N_DIVISIONS * (N_DIVISIONS - 1) // 2}")
    if discordant:
        first, second = discordant[0]
        print(f"first such pair: {first} and {second}")

    base = divisions[0]
    adj = capitalized(base)
    print(f"capitalization example on {base.name}: outlay {SPEND} cents, life {LIFE_YEARS} years")
    print(f"  reported:    C {base.invested}  OI {base.oi}  RI {show(residual_income(base))}  EVA {show(eva(base))}")
    print(f"  capitalized: C {adj.invested}  OI {adj.oi}  RI {show(residual_income(adj))}  EVA {show(eva(adj))}")
    print(
        f"  change in RI {show(residual_income(adj) - residual_income(base))}; "
        f"change in EVA {show(eva(adj) - eva(base))}"
    )


main()

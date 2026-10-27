"""Lab AC2-L07-1: the nine Piotroski signals on generated firm-years.

Every firm here is SIMULATED: the statements are drawn from a seeded generator,
no filer is represented, and no figure is an estimate of any real company.
The signal definitions are the contract's (atlas/A15.contract.md, piotroski_f_score),
which follow Piotroski (2000), pp. 8-10 (printed pages) of the Journal of
Accounting Research 38 supplement. Money is in SIMULATED currency units (SCU).
"""

from __future__ import annotations

import random
from dataclasses import dataclass

SEED = 20260527
N_FIRMS = 400


@dataclass(frozen=True)
class YearStatement:
    """One fiscal year of a SIMULATED firm. Money in SCU; shares in millions."""

    revenue: float
    cogs: float
    net_income: float
    cfo: float
    total_assets: float
    current_assets: float
    current_liabilities: float
    long_term_debt: float
    shares: float


def gross_margin(s: YearStatement) -> float:
    """Gross margin (revenue - cogs) / revenue, dimensionless."""
    if s.revenue <= 0.0:
        raise ValueError("revenue must be positive")
    return (s.revenue - s.cogs) / s.revenue


def current_ratio(s: YearStatement) -> float:
    """Current assets / current liabilities, dimensionless."""
    if s.current_liabilities <= 0.0:
        raise ValueError("current liabilities must be positive")
    return s.current_assets / s.current_liabilities


def piotroski_signals(y2: YearStatement, y1: YearStatement, y0: YearStatement) -> tuple[int, ...]:
    """Return the nine binary signals for year t = y0, given t-1 = y1 and t-2 = y2.

    Scaling follows the contract: ROA and CFO use beginning-of-year assets
    (y1.total_assets for t); leverage uses average total assets; asset turnover
    uses beginning-of-year assets. Each signal is 1 when its condition holds.
    """
    if min(y2.total_assets, y1.total_assets, y0.total_assets) <= 0.0:
        raise ValueError("total assets must be positive")
    roa0 = y0.net_income / y1.total_assets
    roa1 = y1.net_income / y2.total_assets
    cfo0 = y0.cfo / y1.total_assets
    lev0 = y0.long_term_debt / ((y0.total_assets + y1.total_assets) / 2.0)
    lev1 = y1.long_term_debt / ((y1.total_assets + y2.total_assets) / 2.0)
    ato0 = y0.revenue / y1.total_assets
    ato1 = y1.revenue / y2.total_assets
    return (
        int(roa0 > 0.0),
        int(cfo0 > 0.0),
        int(roa0 > roa1),
        int(cfo0 > roa0),
        int(lev0 < lev1),
        int(current_ratio(y0) > current_ratio(y1)),
        int(y0.shares <= y1.shares),
        int(gross_margin(y0) > gross_margin(y1)),
        int(ato0 > ato1),
    )


def generate_firm(rng: random.Random) -> tuple[YearStatement, YearStatement, YearStatement]:
    """Generate years t-2, t-1, t for one SIMULATED firm (all values positive, SCU)."""
    assets = rng.uniform(800.0, 1200.0)
    margin = rng.uniform(0.03, 0.12)
    gm = rng.uniform(0.25, 0.55)
    turn = rng.uniform(0.8, 1.6)
    ltd_share = rng.uniform(0.10, 0.45)
    shares = rng.uniform(40.0, 60.0)
    years: list[YearStatement] = []
    for _ in range(3):
        growth = rng.uniform(0.92, 1.10)
        assets = assets * growth
        revenue = assets * turn * rng.uniform(0.9, 1.1)
        cogs = revenue * (1.0 - gm * rng.uniform(0.9, 1.1))
        net_income = revenue * margin * rng.uniform(0.6, 1.4)
        accrual = rng.uniform(-0.04, 0.04) * assets
        cfo = net_income - accrual
        current_assets = assets * rng.uniform(0.25, 0.45)
        current_liabilities = assets * rng.uniform(0.15, 0.35)
        long_term_debt = assets * ltd_share * rng.uniform(0.9, 1.1)
        shares = shares * rng.choice((1.0, 1.0, 1.0, 1.02))
        years.append(
            YearStatement(
                revenue=revenue,
                cogs=cogs,
                net_income=net_income,
                cfo=cfo,
                total_assets=assets,
                current_assets=current_assets,
                current_liabilities=current_liabilities,
                long_term_debt=long_term_debt,
                shares=shares,
            )
        )
        margin = max(0.005, margin + rng.uniform(-0.01, 0.01))
        gm = min(0.9, max(0.05, gm + rng.uniform(-0.02, 0.02)))
        turn = max(0.3, turn + rng.uniform(-0.1, 0.1))
    return years[0], years[1], years[2]


def scale_money(s: YearStatement, k: float) -> YearStatement:
    """Multiply every money item by k > 0; shares are unchanged."""
    return YearStatement(
        revenue=s.revenue * k,
        cogs=s.cogs * k,
        net_income=s.net_income * k,
        cfo=s.cfo * k,
        total_assets=s.total_assets * k,
        current_assets=s.current_assets * k,
        current_liabilities=s.current_liabilities * k,
        long_term_debt=s.long_term_debt * k,
        shares=s.shares,
    )


def main() -> None:
    """Generate the firms, print six worked firm-years, the score distribution and the scale check."""
    rng = random.Random(SEED)
    rows: list[tuple[int, tuple[int, ...]]] = []
    for firm_id in range(N_FIRMS):
        y2, y1, y0 = generate_firm(rng)
        rows.append((firm_id, piotroski_signals(y2, y1, y0)))

    print(f"SIMULATED firm-years (seed {SEED}): signals s1..s9 and F-score")
    for firm_id, sig in rows[:6]:
        bits = "".join(str(b) for b in sig)
        print(f"SIM-{firm_id:03d}  signals={bits}  score={sum(sig)}")

    counts = [0] * 10
    for _, sig in rows:
        counts[sum(sig)] += 1
    print(f"score distribution over {N_FIRMS} SIMULATED firm-years:")
    for score, n in enumerate(counts):
        print(f"  score {score}: {n}")
    mean_score = sum(sum(sig) for _, sig in rows) / N_FIRMS
    print(f"mean score: {mean_score:.4f}")

    # Scale invariance (contract, Conventions): multiplying money by k > 0 leaves every signal unchanged.
    rng2 = random.Random(SEED)
    unchanged = 0
    for _ in range(N_FIRMS):
        y2, y1, y0 = generate_firm(rng2)
        k = 1000.0
        if piotroski_signals(y2, y1, y0) == piotroski_signals(
            scale_money(y2, k), scale_money(y1, k), scale_money(y0, k)
        ):
            unchanged += 1
    print(f"signals unchanged under money x1000: {unchanged}/{N_FIRMS}")


main()

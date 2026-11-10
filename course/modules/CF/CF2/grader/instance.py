"""Instance generator for the CF2 cost of capital project.

Deterministic from seed. Exposes make_instance(seed: int) -> dict.
Standard library only.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic, valid project instance for the given seed.

    Returns market-value and book debt in integer cents, equity market value in integer cents,
    tax rate, monthly return series for the firm and the market (48 periods),
    annual risk-free rate, equity risk premium, debt credit spread,
    cash flow in integer cents, and terminal growth rate.
    """
    rng = random.Random(seed)
    n_periods = 48

    # Underlying parameters for return simulation
    true_beta = round(rng.uniform(0.65, 1.75), 4)
    # Market monthly returns: mean ~0.8%, stdev ~4%
    mkt = [round(rng.gauss(0.008, 0.040), 6) for _ in range(n_periods)]
    # Firm monthly returns: alpha ~0.2%, beta, idiosyncratic noise ~2.5%
    firm = [round(0.002 + true_beta * m + rng.gauss(0.0, 0.025), 6) for m in mkt]

    rf = round(rng.uniform(0.02, 0.06), 4)
    erp = round(rng.uniform(0.04, 0.07), 4)
    spread = round(rng.uniform(0.010, 0.035), 4)
    tax = round(rng.uniform(0.18, 0.32), 4)

    debt_market = int(rng.uniform(10_000_000, 50_000_000))  # 100k to 500k USD in cents
    de_ratio = rng.uniform(0.25, 1.75)
    equity_market = int(debt_market / de_ratio)

    mult = rng.choice([0.80, 0.85, 0.90, 1.10, 1.15, 1.20])
    debt_book = int(debt_market * mult)
    if debt_book == debt_market:
        debt_book += 50_000

    cf_cents = int(rng.uniform(500_000, 2_000_000))

    # Calculate preliminary WACC to set growth with wacc - growth >= 0.02
    mean_m = sum(mkt) / n_periods
    mean_f = sum(firm) / n_periods
    cov_fm = sum((f - mean_f) * (m - mean_m) for f, m in zip(firm, mkt, strict=True)) / (n_periods - 1)
    var_m = sum((m - mean_m) ** 2 for m in mkt) / (n_periods - 1)
    b_est = cov_fm / var_m
    re = rf + b_est * erp
    rd = rf + spread
    we = equity_market / (debt_market + equity_market)
    wd = debt_market / (debt_market + equity_market)
    wacc_val = we * re + wd * rd * (1.0 - tax)

    # growth between 1% and min(2.5%, wacc_val - 0.025)
    max_g = min(0.025, wacc_val - 0.025)
    g = round(rng.uniform(0.010, max(0.011, max_g)), 4)

    return {
        "seed": seed,
        "firm_returns": firm,
        "market_returns": mkt,
        "risk_free": rf,
        "erp": erp,
        "spread": spread,
        "debt_market_cents": debt_market,
        "equity_market_cents": equity_market,
        "debt_book_cents": debt_book,
        "tax_rate": tax,
        "cash_flow_cents": cf_cents,
        "growth": g,
        "wacc": wacc_val,
    }

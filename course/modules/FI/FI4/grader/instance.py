"""Instance generator for FI4 Plumbing Monitor autograder.

Generates deterministic market states with repo rates, cash Treasury prices,
futures prices, conversion factors, haircuts, and margin parameters.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic simulated money-market state from an integer seed."""
    rng = random.Random(seed)

    # Cash Treasury bond price (per 100 face value)
    cash_price = round(rng.uniform(96.0, 104.0), 4)

    # Futures conversion factor for the cheapest-to-deliver bond
    conversion_factor = round(rng.uniform(0.78, 0.92), 4)

    # Basis spread relative to no-arbitrage parity: -40 bps to +40 bps
    basis_spread = rng.uniform(-0.0040, 0.0040)
    implied_forward = cash_price * (1.0 + basis_spread)
    futures_price = round(implied_forward / conversion_factor, 4)

    # Overnight and term repo borrowing rate (annualized, 1.50% to 5.50%)
    repo_rate = round(rng.uniform(0.0150, 0.0550), 4)

    # Days to futures delivery date
    days = rng.choice([30, 60, 91, 180])

    # Bilateral repo haircut on Treasury collateral (1.0% to 3.0%)
    haircut = round(rng.uniform(0.010, 0.030), 4)

    # CME futures initial margin (2.0% to 4.5% of contract value)
    initial_margin = round(rng.uniform(0.020, 0.045), 4)

    # Maintenance margin threshold (typically 75% of initial margin)
    maintenance_margin = round(initial_margin * 0.75, 4)

    # Dealer baseline portfolio parameters (USD millions)
    notional = rng.choice([10_000_000, 25_000_000, 50_000_000])
    dealer_equity = round(notional * rng.uniform(0.05, 0.08), 2)
    cash_treasuries = round(notional * rng.uniform(0.60, 1.20), 2)
    repo_matched_book = round(notional * rng.uniform(0.40, 0.80), 2)
    derivatives_exposure = round(notional * rng.uniform(0.10, 0.30), 2)

    return {
        "seed": seed,
        "cash_price": cash_price,
        "futures_price": futures_price,
        "conversion_factor": conversion_factor,
        "days": days,
        "repo_rate": repo_rate,
        "haircut": haircut,
        "initial_margin": initial_margin,
        "maintenance_margin": maintenance_margin,
        "notional": notional,
        "dealer_equity": dealer_equity,
        "cash_treasuries": cash_treasuries,
        "repo_matched_book": repo_matched_book,
        "derivatives_exposure": derivatives_exposure,
    }

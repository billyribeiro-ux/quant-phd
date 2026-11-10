"""Instance generator for X2 project: Currency factor replication.

Generates deterministic currency panels, spot and forward exchange rates,
and daily returns for seeds 0-49.
"""

from __future__ import annotations

import math
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic problem instance for the X2 project.

    Args:
        seed: Integer seed between 0 and 49 (or arbitrary integer).

    Returns:
        dict containing:
            seed: integer seed
            n_periods: number of monthly periods (120 to 150 months)
            n_currencies: number of foreign currencies (10 currencies)
            currency_names: list of currency codes
            n_portfolios: number of sorted carry portfolios (5 quintiles)
            spot_rates: 2D list (n_periods, n_currencies) of spot exchange rates (USD per unit)
            forward_rates: 2D list (n_periods, n_currencies) of 1-month forward exchange rates
            daily_returns: 2D list (n_periods * 21, n_currencies) of daily FX log returns
    """
    rng = random.Random(seed)

    # Observation count: 120 + deterministic variation (10 to 12.5 years of monthly data)
    n_periods = 120 + (seed * 7) % 31
    n_currencies = 10
    currency_names = ["AUD", "CAD", "CHF", "EUR", "GBP", "JPY", "NOK", "NZD", "SEK", "ZAR"]
    n_portfolios = 5

    # Base annualized interest differentials vs USD in percent
    base_spreads = [
        0.025,  # AUD: +2.5%
        0.005,  # CAD: +0.5%
        -0.020,  # CHF: -2.0% (low rate funding)
        -0.005,  # EUR: -0.5%
        0.010,  # GBP: +1.0%
        -0.035,  # JPY: -3.5% (low rate funding)
        0.015,  # NOK: +1.5%
        0.030,  # NZD: +3.0% (high rate target)
        0.008,  # SEK: +0.8%
        0.060,  # ZAR: +6.0% (high rate target)
    ]

    initial_spots = [0.70, 0.75, 1.10, 1.15, 1.30, 0.009, 0.11, 0.65, 0.10, 0.065]
    log_spots = [math.log(s) for s in initial_spots]
    cur_spreads = [s + (seed % 5 - 2) * 0.002 for s in base_spreads]

    days_per_month = 21
    spot_rates: list[list[float]] = []
    forward_rates: list[list[float]] = []
    daily_returns: list[list[float]] = []

    vol_state = 0.006

    for _t in range(n_periods):
        cur_spots = [round(math.exp(ls), 5) for ls in log_spots]
        spot_rates.append(cur_spots)

        # Forward rates under CIP: F_t = S_t * exp(-(i_t^* - i_t) / 12)
        month_forwards = [round(cur_spots[j] * math.exp(-cur_spreads[j] / 12.0), 5) for j in range(n_currencies)]
        forward_rates.append(month_forwards)

        for _d in range(days_per_month):
            vol_state = max(
                0.003,
                min(0.025, 0.90 * vol_state + 0.10 * 0.006 + rng.gauss(0.0, 0.0007)),
            )
            dol_shock = rng.gauss(0.0, vol_state)
            vol_shock = vol_state - 0.006

            day_rets: list[float] = []
            for j in range(n_currencies):
                # Volatility sensitivity: high carry currencies crash during vol spikes
                vol_loading = -6.0 * cur_spreads[j]
                idio = rng.gauss(0.0, 0.0025)
                d_ret = dol_shock + vol_loading * vol_shock + idio
                log_spots[j] += d_ret
                day_rets.append(round(d_ret, 6))
            daily_returns.append(day_rets)

    return {
        "seed": seed,
        "n_periods": n_periods,
        "n_currencies": n_currencies,
        "currency_names": currency_names,
        "n_portfolios": n_portfolios,
        "spot_rates": spot_rates,
        "forward_rates": forward_rates,
        "daily_returns": daily_returns,
    }

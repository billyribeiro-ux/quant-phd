"""Instance generator for X1 project: Meese-Rogoff re-run.

Generates deterministic exchange rate and macroeconomic fundamental time series
for seeds 0-49 to evaluate out-of-sample forecasting horse races.
"""

from __future__ import annotations

import math
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic problem instance for the X1 project.

    Args:
        seed: Integer seed between 0 and 49 (or arbitrary integer).

    Returns:
        dict containing:
            seed: integer seed
            n_obs: number of monthly periods (between 120 and 180)
            initial_price: initial spot exchange rate S_0
            window_size: rolling estimation window (e.g. 36 or 48 months)
            horizons: list of forecasting horizons [1, 3, 12]
            s_series: log exchange rate series s_t = ln(S_t)
            f_series: macroeconomic fundamentals series (money supply / output differential)
            i_diff_series: interest rate differential series (i_t - i_t^*) in percent/month
    """
    rng = random.Random(seed)

    # Deterministic observation count between 120 and 160 months (10-13 years)
    n_obs = 120 + (seed * 11) % 41
    initial_price = round(1.10 + ((seed * 7) % 30) * 0.01, 4)
    log_s0 = math.log(initial_price)
    window_size = 36
    horizons = [1, 3, 12]

    # Generate persistent fundamental series f_t (e.g. AR(1) with persistent coefficient)
    # f_t = rho_f * f_{t-1} + e_f,t
    rho_f = round(0.92 + (seed % 6) * 0.01, 3)
    sigma_f = 0.02

    f_series: list[float] = [round(rng.gauss(0.0, 0.05), 4)]
    for _ in range(1, n_obs):
        f_next = rho_f * f_series[-1] + rng.gauss(0.0, sigma_f)
        f_series.append(round(f_next, 4))

    # Generate interest rate differential i_diff_series (percent per month, approx 1-5% annualized)
    # Related to fundamental drift with noise
    i_diff_series: list[float] = []
    for t in range(n_obs):
        diff = round(0.0015 * f_series[t] + rng.gauss(0.001, 0.0008), 5)
        i_diff_series.append(diff)

    # Generate log spot exchange rate series s_t
    # In reality, s_t is dominated by random walk shocks plus a small fundamental loading
    # beta_true is small (0.1 to 0.3) so fundamentals have poor short-term predictive power
    beta_true = round(0.12 + (seed % 5) * 0.03, 3)
    sigma_s = 0.03  # monthly FX volatility ~ 3%

    s_series: list[float] = [round(log_s0, 4)]
    for t in range(1, n_obs):
        # RW innovation with slight fundamental co-movement
        shock = rng.gauss(0.0, sigma_s)
        f_delta = f_series[t] - f_series[t - 1]
        ds = beta_true * f_delta + shock
        s_next = s_series[-1] + ds
        s_series.append(round(s_next, 4))

    return {
        "seed": seed,
        "n_obs": n_obs,
        "initial_price": initial_price,
        "window_size": window_size,
        "horizons": horizons,
        "s_series": s_series,
        "f_series": f_series,
        "i_diff_series": i_diff_series,
    }

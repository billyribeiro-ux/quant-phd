"""Lab PM4-project-1: Monte Carlo Agency MBS Valuation and Risk Engine.

Rung 2 completed solution: Simulates short-rate paths, calculates pathwise
prepayment and burnout cash flows, and computes Monte Carlo price and effective Greeks.
"""

from __future__ import annotations

import numpy as np


def simulate_short_rates(
    r0: float,
    kappa: float,
    theta: float,
    sigma: float,
    n_months: int,
    n_paths: int,
    seed: int = 42,
) -> np.ndarray:
    """Simulate risk-neutral short rate paths using exact Gaussian Vasicek transitions."""
    rng = np.random.default_rng(seed)
    dt = 1.0 / 12.0
    exp_k = float(np.exp(-kappa * dt))
    std_step = float(np.sqrt((sigma**2) / (2.0 * kappa) * (1.0 - exp_k**2)))

    rates = np.zeros((n_paths, n_months))
    rates[:, 0] = r0

    for t in range(1, n_months):
        z = rng.normal(size=n_paths)
        rates[:, t] = rates[:, t - 1] * exp_k + theta * (1.0 - exp_k) + std_step * z

    return rates


def compute_mbs_cash_flows(
    notional: float,
    wac: float,
    pass_through_rate: float,
    wam: int,
    rates: np.ndarray,
    base_cpr: float = 0.06,
    max_cpr: float = 0.40,
    beta: float = 60.0,
    mu: float = 0.010,
    margin: float = 0.012,
    gamma_burnout: float = 0.05,
) -> np.ndarray:
    """Generate pathwise cash flows with state-dependent refinancing and burnout."""
    n_paths, n_months = rates.shape
    wac_m = wac / 12.0
    net_m = pass_through_rate / 12.0

    balances = np.full(n_paths, notional)
    cumulative_incentive = np.zeros(n_paths)
    cash_flows = np.zeros((n_paths, n_months))

    for t in range(n_months):
        rem_m = wam - t
        refi_rate = rates[:, t] + margin
        incentive = np.maximum(0.0, wac - refi_rate)
        cumulative_incentive += incentive
        burnout = np.exp(-gamma_burnout * cumulative_incentive)

        refi_spread = wac - refi_rate - mu
        cpr = (base_cpr + (max_cpr - base_cpr) / (1.0 + np.exp(-beta * refi_spread))) * burnout
        smm_t = 1.0 - (1.0 - cpr) ** (1.0 / 12.0)

        denom = 1.0 - (1.0 + wac_m) ** (-rem_m)
        pmt = balances * (wac_m / denom)
        gross_int = balances * wac_m
        sched_prin = pmt - gross_int
        prepay = (balances - sched_prin) * smm_t
        tot_prin = sched_prin + prepay

        net_int = balances * net_m
        cash_flows[:, t] = net_int + tot_prin
        balances -= tot_prin

    return cash_flows


def price_mbs(
    cash_flows: np.ndarray,
    rates: np.ndarray,
    spread: float = 0.0,
    delay_days: int = 24,
) -> float:
    """Discount pathwise cash flows along simulated rate paths with delay adjustment."""
    dt = 1.0 / 12.0
    cum_r = np.cumsum((rates + spread) * dt, axis=1)
    delay_adj = (rates + spread) * (delay_days / 365.0)
    disc = np.exp(-(cum_r + delay_adj))
    return float(np.mean(np.sum(cash_flows * disc, axis=1)))


def main() -> None:
    notional = 100_000_000.0
    wac = 0.065
    pass_through_rate = 0.060
    wam = 360
    delay_days = 24

    r0 = 0.045
    kappa = 0.15
    theta = 0.050
    sigma = 0.015
    n_paths = 500

    rates = simulate_short_rates(r0, kappa, theta, sigma, wam, n_paths, seed=42)
    cash_flows = compute_mbs_cash_flows(notional, wac, pass_through_rate, wam, rates)
    price_base = price_mbs(cash_flows, rates, spread=0.0, delay_days=delay_days)

    dy = 0.0025
    rates_up = simulate_short_rates(r0 + dy, kappa, theta + dy, sigma, wam, n_paths, seed=42)
    cf_up = compute_mbs_cash_flows(notional, wac, pass_through_rate, wam, rates_up)
    price_up = price_mbs(cf_up, rates_up, spread=0.0, delay_days=delay_days)

    rates_down = simulate_short_rates(r0 - dy, kappa, theta - dy, sigma, wam, n_paths, seed=42)
    cf_down = compute_mbs_cash_flows(notional, wac, pass_through_rate, wam, rates_down)
    price_down = price_mbs(cf_down, rates_down, spread=0.0, delay_days=delay_days)

    eff_dur = (price_down - price_up) / (2.0 * price_base * dy)
    eff_cvx = (price_up + price_down - 2.0 * price_base) / (price_base * (dy**2))

    print("MBS Monte Carlo Pricer Engine Output:")
    print(f"Base Model Price ($):        {price_base:14.2f}")
    print(f"Base Model Price (% of par): {price_base / notional * 100:14.4f}")
    print(f"Price Up (+25 bps):          {price_up:14.2f}")
    print(f"Price Down (-25 bps):        {price_down:14.2f}")
    print(f"Effective Duration:          {eff_dur:14.4f} years")
    print(f"Effective Convexity:         {eff_cvx:14.4f}")

    assert price_base > 0.0
    assert eff_dur > 0.0
    assert eff_cvx < 0.0


main()

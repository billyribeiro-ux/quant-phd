"""Lab PM4-L04-1: Option-Adjusted Spread (OAS) and Effective Duration/Convexity.

SIMULATED: Solves for the Option-Adjusted Spread (OAS) of an agency MBS pass-through via Monte Carlo
risk-neutral simulation and computes effective duration and convexity under stochastic prepayment.
"""

from __future__ import annotations

import numpy as np


def simulate_vasicek_paths(
    r0: float,
    kappa: float,
    theta: float,
    sigma: float,
    n_months: int = 360,
    n_paths: int = 500,
    seed: int = 42,
) -> np.ndarray:
    """Simulate exact Gaussian discrete transitions for 1-factor Vasicek short rate."""
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


def generate_path_cash_flows(
    rates: np.ndarray,
    notional: float = 100.0,
    wac: float = 0.065,
    pass_through_rate: float = 0.060,
    base_cpr: float = 0.06,
    max_cpr: float = 0.40,
    beta: float = 60.0,
    mu: float = 0.010,
    margin: float = 0.012,
    gamma_burnout: float = 0.05,
) -> np.ndarray:
    """Generate path-dependent monthly cash flows under state-dependent prepayment and burnout."""
    n_paths, n_months = rates.shape
    wac_m = wac / 12.0
    net_m = pass_through_rate / 12.0

    balances = np.full(n_paths, notional)
    cumulative_incentive = np.zeros(n_paths)
    cash_flows = np.zeros((n_paths, n_months))

    for t in range(n_months):
        rem_m = n_months - t
        refi_rate = rates[:, t] + margin
        incentive = np.maximum(0.0, wac - refi_rate)
        cumulative_incentive += incentive
        burnout = np.exp(-gamma_burnout * cumulative_incentive)

        # Logistic refinancing incentive multiplied by burnout
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


def price_mc_spread(
    rates: np.ndarray,
    cash_flows: np.ndarray,
    spread: float,
    delay_days: int = 24,
) -> float:
    """Discount pathwise cash flows at path short rates plus spread."""
    dt = 1.0 / 12.0
    cum_r = np.cumsum((rates + spread) * dt, axis=1)
    delay_adj = (rates + spread) * (delay_days / 365.0)
    disc = np.exp(-(cum_r + delay_adj))
    return float(np.mean(np.sum(cash_flows * disc, axis=1)))


def calibrate_oas(
    market_price: float,
    rates: np.ndarray,
    cash_flows: np.ndarray,
    delay_days: int = 24,
) -> float:
    """Solve for OAS equating model expectation to market price via bisection."""
    low_s = -0.05
    high_s = 0.05
    for _ in range(50):
        mid_s = 0.5 * (low_s + high_s)
        p_mid = price_mc_spread(rates, cash_flows, mid_s, delay_days)
        if abs(p_mid - market_price) < 1e-4:
            break
        if p_mid > market_price:
            low_s = mid_s
        else:
            high_s = mid_s
    return float(mid_s * 10000.0)


def main() -> None:
    r0 = 0.045
    kappa = 0.15
    theta = 0.050
    sigma = 0.015
    notional = 100.0
    wac = 0.065
    net_c = 0.060
    delay_days = 24

    # Baseline simulation
    rates = simulate_vasicek_paths(r0, kappa, theta, sigma, n_months=360, n_paths=500, seed=42)
    cash_flows = generate_path_cash_flows(rates, notional, wac, net_c)

    p_zero_spread = price_mc_spread(rates, cash_flows, spread=0.0, delay_days=delay_days)
    print("MBS Monte Carlo Simulation Results:")
    print(f"Zero-Spread Model Price:     {p_zero_spread:8.4f}")

    # Market price observation
    target_market_price = 102.00
    oas_bps = calibrate_oas(target_market_price, rates, cash_flows, delay_days=delay_days)
    print(f"Target Market Price:         {target_market_price:8.4f}")
    print(f"Calibrated OAS:              {oas_bps:8.2f} bps")

    # Re-verify price at OAS
    p_at_oas = price_mc_spread(rates, cash_flows, spread=oas_bps / 10000.0, delay_days=delay_days)
    print(f"Price at Calibrated OAS:     {p_at_oas:8.4f}")
    assert abs(p_at_oas - target_market_price) < 0.01

    # Effective Greeks with common random numbers
    dy = 0.0025  # 25 bps
    spread_dec = oas_bps / 10000.0

    rates_up = simulate_vasicek_paths(r0 + dy, kappa, theta + dy, sigma, n_months=360, n_paths=500, seed=42)
    cf_up = generate_path_cash_flows(rates_up, notional, wac, net_c)
    p_up = price_mc_spread(rates_up, cf_up, spread=spread_dec, delay_days=delay_days)

    rates_down = simulate_vasicek_paths(r0 - dy, kappa, theta - dy, sigma, n_months=360, n_paths=500, seed=42)
    cf_down = generate_path_cash_flows(rates_down, notional, wac, net_c)
    p_down = price_mc_spread(rates_down, cf_down, spread=spread_dec, delay_days=delay_days)

    eff_duration = (p_down - p_up) / (2.0 * target_market_price * dy)
    eff_convexity = (p_up + p_down - 2.0 * target_market_price) / (target_market_price * (dy**2))

    print("\nStochastic Effective Risk Metrics:")
    print(f"Price (+25 bps shift):       {p_up:8.4f}")
    print(f"Price (-25 bps shift):       {p_down:8.4f}")
    print(f"Effective Duration:          {eff_duration:8.4f} years")
    print(f"Effective Convexity:         {eff_convexity:8.4f}")

    assert eff_duration > 0.0
    assert eff_convexity < 0.0  # Confirms negative convexity in Monte Carlo OAS model!


main()

"""Mutant 5: Disables prepayment burnout by holding the burnout multiplier constant at 1.0."""

from __future__ import annotations

import numpy as np


def simulate_interest_rates(
    r0: float,
    kappa: float,
    theta: float,
    sigma: float,
    wam: int,
    n_paths: int,
    seed: int = 42,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    dt = 1.0 / 12.0
    exp_k = float(np.exp(-kappa * dt))
    std_step = float(np.sqrt((sigma**2) / (2.0 * kappa) * (1.0 - exp_k**2)))

    rates = np.zeros((n_paths, wam))
    rates[:, 0] = r0

    for t in range(1, wam):
        z = rng.normal(size=n_paths)
        rates[:, t] = rates[:, t - 1] * exp_k + theta * (1.0 - exp_k) + std_step * z

    return rates


def generate_mbs_cash_flows(
    notional: float,
    wac: float,
    pass_through_rate: float,
    wam: int,
    base_cpr: float,
    max_cpr: float,
    beta: float,
    mu: float,
    margin: float,
    gamma_burnout: float,
    rates: np.ndarray,
) -> np.ndarray:
    n_paths, n_months = rates.shape
    wac_m = wac / 12.0
    net_m = pass_through_rate / 12.0

    balances = np.full(n_paths, notional)
    cash_flows = np.zeros((n_paths, n_months))

    for t in range(n_months):
        rem_m = wam - t
        refi_rate = rates[:, t] + margin

        # ERROR: Burnout is omitted completely (set to 1.0)
        burnout = 1.0

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
    dt = 1.0 / 12.0
    cum_r = np.cumsum((rates + spread) * dt, axis=1)
    delay_adj = (rates + spread) * (delay_days / 365.0)
    disc = np.exp(-(cum_r + delay_adj))
    return float(np.mean(np.sum(cash_flows * disc, axis=1)))


def solve_oas(
    rates: np.ndarray,
    cash_flows: np.ndarray,
    target_price: float,
    delay_days: int = 24,
) -> float:
    low_s = -0.05
    high_s = 0.05
    for _ in range(50):
        mid_s = 0.5 * (low_s + high_s)
        p_mid = price_mbs(cash_flows, rates, spread=mid_s, delay_days=delay_days)
        if abs(p_mid - target_price) < 1.0:
            break
        if p_mid > target_price:
            low_s = mid_s
        else:
            high_s = mid_s
    return float(mid_s * 10000.0)


def compute_effective_greeks(
    instance: dict[str, float | int],
    oas_bps: float,
) -> dict[str, float]:
    notional = float(instance["notional"])
    wac = float(instance["wac"])
    pass_through_rate = float(instance["pass_through_rate"])
    wam = int(instance["wam"])
    delay_days = int(instance["delay_days"])

    r0 = float(instance["r0"])
    kappa = float(instance["kappa"])
    theta = float(instance["theta"])
    sigma = float(instance["sigma"])

    base_cpr = float(instance["base_cpr"])
    max_cpr = float(instance["max_cpr"])
    beta = float(instance["beta"])
    mu = float(instance["mu"])
    margin = float(instance["margin"])
    gamma_burnout = float(instance["gamma_burnout"])

    n_paths = int(instance["n_paths"])
    sim_seed = int(instance["sim_seed"])
    dy = float(instance["dy"])
    spread = oas_bps / 10000.0

    rates_base = simulate_interest_rates(r0, kappa, theta, sigma, wam, n_paths, seed=sim_seed)
    cf_base = generate_mbs_cash_flows(
        notional, wac, pass_through_rate, wam, base_cpr, max_cpr, beta, mu, margin, gamma_burnout, rates_base
    )
    price_base = price_mbs(cf_base, rates_base, spread=spread, delay_days=delay_days)

    rates_up = simulate_interest_rates(r0 + dy, kappa, theta + dy, sigma, wam, n_paths, seed=sim_seed)
    cf_up = generate_mbs_cash_flows(
        notional, wac, pass_through_rate, wam, base_cpr, max_cpr, beta, mu, margin, gamma_burnout, rates_up
    )
    price_up = price_mbs(cf_up, rates_up, spread=spread, delay_days=delay_days)

    rates_down = simulate_interest_rates(r0 - dy, kappa, theta - dy, sigma, wam, n_paths, seed=sim_seed)
    cf_down = generate_mbs_cash_flows(
        notional, wac, pass_through_rate, wam, base_cpr, max_cpr, beta, mu, margin, gamma_burnout, rates_down
    )
    price_down = price_mbs(cf_down, rates_down, spread=spread, delay_days=delay_days)

    eff_duration = (price_down - price_up) / (2.0 * price_base * dy)
    eff_convexity = (price_up + price_down - 2.0 * price_base) / (price_base * (dy**2))

    return {
        "price_base": price_base,
        "price_up": price_up,
        "price_down": price_down,
        "effective_duration": eff_duration,
        "effective_convexity": eff_convexity,
    }


def solve_mbs_pricer(instance: dict[str, float | int]) -> dict[str, float]:
    notional = float(instance["notional"])
    wac = float(instance["wac"])
    pass_through_rate = float(instance["pass_through_rate"])
    wam = int(instance["wam"])
    delay_days = int(instance["delay_days"])

    r0 = float(instance["r0"])
    kappa = float(instance["kappa"])
    theta = float(instance["theta"])
    sigma = float(instance["sigma"])

    base_cpr = float(instance["base_cpr"])
    max_cpr = float(instance["max_cpr"])
    beta = float(instance["beta"])
    mu = float(instance["mu"])
    margin = float(instance["margin"])
    gamma_burnout = float(instance["gamma_burnout"])

    n_paths = int(instance["n_paths"])
    sim_seed = int(instance["sim_seed"])
    target_mkt = float(instance["target_market_price"])

    rates = simulate_interest_rates(r0, kappa, theta, sigma, wam, n_paths, seed=sim_seed)
    cash_flows = generate_mbs_cash_flows(
        notional, wac, pass_through_rate, wam, base_cpr, max_cpr, beta, mu, margin, gamma_burnout, rates
    )

    zero_spread_price = price_mbs(cash_flows, rates, spread=0.0, delay_days=delay_days)
    oas_bps = solve_oas(rates, cash_flows, target_mkt, delay_days=delay_days)
    price_at_oas = price_mbs(cash_flows, rates, spread=oas_bps / 10000.0, delay_days=delay_days)

    greeks = compute_effective_greeks(instance, oas_bps)

    return {
        "base_model_price": zero_spread_price,
        "target_market_price": target_mkt,
        "oas_bps": oas_bps,
        "price_at_oas": price_at_oas,
        "price_up": greeks["price_up"],
        "price_down": greeks["price_down"],
        "effective_duration": greeks["effective_duration"],
        "effective_convexity": greeks["effective_convexity"],
    }

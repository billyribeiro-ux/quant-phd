"""Lab PR6-L05-1: Human Capital and Lifecycle Asset Allocation.

SIMULATED: Lifecycle simulation of human capital depletion, financial wealth accumulation,
and optimal equity glide paths under riskless vs cyclical human capital.
"""

from __future__ import annotations

import math

import numpy as np


def simulate_lifecycle_allocation(
    start_age: int = 25,
    retire_age: int = 65,
    initial_wage: float = 50000.0,
    initial_wealth: float = 20000.0,
    savings_rate: float = 0.15,
    r_discount: float = 0.03,
    equity_risk_premium: float = 0.05,
    equity_vol: float = 0.18,
    gamma: float = 4.0,
    beta_h_cyclical: float = 0.50,
    leverage_cap: float = 1.0,
    n_paths: int = 5000,
    seed: int = 42,
) -> dict[int, dict[str, float]]:
    """Simulate career wage paths, human capital valuation, and financial portfolio equity weights."""
    rng = np.random.default_rng(seed)
    years = retire_age - start_age

    # Base target equity weight on total wealth (Merton fraction)
    alpha_star = equity_risk_premium / (gamma * equity_vol**2)

    # Wage trajectory parameters: humped shape peaking around age 50
    # Peak at t = 25 (age 50): g_1 = 0.04, g_2 = 0.0008 -> d(log_w)/dt = 0.04 - 0.0016 t = 0 at t=25
    deterministic_wages = np.zeros(years + 1)
    for i in range(years + 1):
        t = float(i)
        deterministic_wages[i] = initial_wage * math.exp(0.04 * t - 0.0008 * t**2)

    # Human capital at each age: discounted sum of future wages to retirement
    human_capital = np.zeros(years + 1)
    for i in range(years + 1):
        rem_years = (years + 1) - i
        discounts = (1.0 + r_discount) ** (-np.arange(rem_years))
        human_capital[i] = float(np.sum(deterministic_wages[i:] * discounts))

    # Simulate financial wealth paths under riskless human capital policy
    wealth_riskless = np.zeros((n_paths, years + 1))
    wealth_cyclical = np.zeros((n_paths, years + 1))
    wealth_riskless[:, 0] = initial_wealth
    wealth_cyclical[:, 0] = initial_wealth

    alpha_f_riskless = np.zeros(years + 1)
    alpha_f_cyclical = np.zeros(years + 1)

    for i in range(years):
        age = start_age + i
        w_r = np.maximum(wealth_riskless[:, i], 1000.0)
        w_c = np.maximum(wealth_cyclical[:, i], 1000.0)

        # Average optimal financial allocation at this age
        ratio_r = human_capital[i] / np.mean(w_r)
        ratio_c = human_capital[i] / np.mean(w_c)

        # Riskless human capital: alpha_F = alpha* * (1 + H/W)
        uncap_r = alpha_star * (1.0 + ratio_r)
        alpha_f_riskless[i] = min(leverage_cap, max(0.0, uncap_r))

        # Cyclical human capital: alpha_F = alpha* + (alpha* - beta_H) * (H/W)
        uncap_c = alpha_star + (alpha_star - beta_h_cyclical) * ratio_c
        alpha_f_cyclical[i] = min(leverage_cap, max(0.0, uncap_c))

        # Step forward 1 year
        z = rng.standard_normal(n_paths)
        r_eq = r_discount + equity_risk_premium + equity_vol * z
        r_port_r = (1.0 - alpha_f_riskless[i]) * r_discount + alpha_f_riskless[i] * r_eq
        r_port_c = (1.0 - alpha_f_cyclical[i]) * r_discount + alpha_f_cyclical[i] * r_eq

        # Add savings
        savings = savings_rate * deterministic_wages[i]
        wealth_riskless[:, i + 1] = wealth_riskless[:, i] * (1.0 + r_port_r) + savings
        wealth_cyclical[:, i + 1] = wealth_cyclical[:, i] * (1.0 + r_port_c) + savings

    # At retirement (age 65), H = 0, so alpha_F = alpha*
    alpha_f_riskless[-1] = min(leverage_cap, alpha_star)
    alpha_f_cyclical[-1] = min(leverage_cap, alpha_star)

    results: dict[int, dict[str, float]] = {}
    sampled_ages = [25, 35, 45, 55, 65]
    for age in sampled_ages:
        idx = age - start_age
        results[age] = {
            "wage": deterministic_wages[idx],
            "human_capital": human_capital[idx],
            "wealth_riskless": float(np.mean(wealth_riskless[:, idx])),
            "alpha_riskless": alpha_f_riskless[idx],
            "alpha_cyclical": alpha_f_cyclical[idx],
        }

    return results


def main() -> None:
    res = simulate_lifecycle_allocation(
        start_age=25,
        retire_age=65,
        initial_wage=50000.0,
        initial_wealth=20000.0,
        savings_rate=0.15,
        r_discount=0.03,
        equity_risk_premium=0.05,
        equity_vol=0.18,
        gamma=4.0,
        beta_h_cyclical=0.50,
        leverage_cap=1.0,
        n_paths=10000,
        seed=42,
    )

    # Base target Merton weight
    alpha_merton = 0.05 / (4.0 * 0.18**2)

    print("Human Capital, Labour Income & Lifecycle Portfolio Allocation:")
    print(f"Target Total Wealth Equity Fraction (alpha*): {alpha_merton:.4f} (38.58%)")
    print("=" * 90)
    print(
        f"{'Age':<6} {'Annual Wage ($)':<16} {'Human Capital ($)':<18} "
        f"{'Financial W ($)':<16} {'Alpha (Safe HC)':<16} {'Alpha (Cyclical)':<16}"
    )
    print("-" * 90)

    for age in [25, 35, 45, 55, 65]:
        d = res[age]
        print(
            f"{age:<6d} {d['wage']:<16.1f} {d['human_capital']:<18.1f} "
            f"{d['wealth_riskless']:<16.1f} {d['alpha_riskless']:<16.4f} {d['alpha_cyclical']:<16.4f}"
        )

    print("=" * 90)
    print("Core Theoretical Findings (Bodie, Merton & Samuelson 1992):")
    print("1. Safe Human Capital: Young investors hold maximum equity (100%) because implicit wealth is bond-like.")
    print("2. Human Capital Depletion: As age increases and H/W declines, optimal equity glides down toward alpha*.")
    print("3. Cyclical Labour: When labour has high equity beta (beta_H > alpha*), young workers hold LESS equity.")


main()

"""Lab PR6-L04-1: Term Structure of Risk & Liability-Driven Investing (LDI).

SIMULATED: Vasicek term structure simulation evaluating cash reinvestment risk,
duration immunization, and pension surplus volatility under liability-driven investing.
"""

from __future__ import annotations

import math

import numpy as np


def evaluate_ldi_strategies(
    r0: float = 0.03,
    r_bar: float = 0.03,
    kappa: float = 0.20,
    sigma_r: float = 0.015,
    liability_duration: float = 15.0,
    n_years: int = 10,
    n_steps_per_year: int = 12,
    n_paths: int = 10000,
    seed: int = 42,
) -> dict[str, dict[str, float]]:
    """Simulate short rate paths and compare cash, unhedged, and duration-matched LDI surplus volatility."""
    rng = np.random.default_rng(seed)
    total_steps = n_years * n_steps_per_year
    dt = 1.0 / float(n_steps_per_year)
    sqrt_dt = math.sqrt(dt)

    # Simulate Vasicek short-rate paths: dr_t = kappa * (r_bar - r_t) * dt + sigma_r * dW_t
    r = np.zeros((n_paths, total_steps + 1))
    r[:, 0] = r0
    z = rng.standard_normal((n_paths, total_steps))

    for t in range(total_steps):
        dr = kappa * (r_bar - r[:, t]) * dt + sigma_r * sqrt_dt * z[:, t]
        r[:, t + 1] = r[:, t] + dr

    # Liability process: L_t = L_0 * exp( - D_L * (r_t - r0) )
    # Mod-duration sensitivity: dL / L = - D_L * dr
    delta_r = r[:, -1] - r0
    liability_terminal = 100.0 * np.exp(-liability_duration * delta_r)

    # 1. Cash strategy: roll over short rate r_t
    # Terminal cash: 100 * exp( sum(r_t * dt) )
    cum_cash_rate = np.sum(r[:, :-1], axis=1) * dt
    cash_terminal = 100.0 * np.exp(cum_cash_rate)
    cash_surplus = cash_terminal - liability_terminal

    # 2. Equity-dominated unhedged portfolio (60% equities with 16% vol, 40% cash)
    # Equities have mild correlation with interest rates (e.g. -0.20)
    z_eq = rng.standard_normal((n_paths, total_steps))
    z_eq_corr = -0.20 * z + math.sqrt(1.0 - 0.20**2) * z_eq
    eq_returns = np.sum((0.07 - 0.5 * 0.16**2) * dt + 0.16 * sqrt_dt * z_eq_corr, axis=1)
    unhedged_terminal = 100.0 * (0.60 * np.exp(eq_returns) + 0.40 * np.exp(cum_cash_rate))
    unhedged_surplus = unhedged_terminal - liability_terminal

    # 3. LDI Duration-Matched Strategy:
    # 80% duration-matched bond (duration = D_L = 15.0), 20% equity buffer
    # Bond return tracks interest rate shift: B_T = B_0 * exp( - D_B * delta_r + yield_carry )
    ldi_bond_terminal = 100.0 * np.exp(-liability_duration * delta_r + cum_cash_rate)
    ldi_terminal = 0.80 * ldi_bond_terminal + 0.20 * (100.0 * np.exp(eq_returns))
    ldi_surplus = ldi_terminal - liability_terminal

    # 4. Pure Immunization: 100% duration-matched bond
    pure_immunized_terminal = ldi_bond_terminal
    pure_surplus = pure_immunized_terminal - liability_terminal

    strats = {
        "Cash (Short Rollover)": cash_surplus,
        "Unhedged (60% Eq / 40% Cash)": unhedged_surplus,
        "LDI (80% Bond Hedge / 20% Eq)": ldi_surplus,
        "Pure Immunized (100% Bond Hedge)": pure_surplus,
    }

    metrics: dict[str, dict[str, float]] = {}
    for name, surplus in strats.items():
        metrics[name] = {
            "mean_surplus": float(np.mean(surplus)),
            "std_surplus": float(np.std(surplus)),
            "p5_surplus": float(np.percentile(surplus, 5)),
            "prob_deficit": float(np.mean(surplus < 0.0)),
        }

    return metrics


def main() -> None:
    r0 = 0.03
    r_bar = 0.03
    kappa = 0.20
    sigma_r = 0.015
    liability_duration = 15.0
    n_years = 10

    res = evaluate_ldi_strategies(
        r0=r0,
        r_bar=r_bar,
        kappa=kappa,
        sigma_r=sigma_r,
        liability_duration=liability_duration,
        n_years=n_years,
        n_paths=20000,
        seed=42,
    )

    print("Term Structure of Risk & Liability-Driven Investing (LDI):")
    print(
        f"Parameters: r0={r0:.2f}, kappa={kappa:.2f}, sigma_r={sigma_r:.3f}, "
        f"Liability Duration={liability_duration:.1f}y"
    )
    print("=" * 88)
    print(f"{'Strategy':<34} {'Mean Surplus ($)':<18} {'Surplus Vol ($)':<18} {'5th Pct ($)':<14} {'P(Deficit)':<10}")
    print("-" * 88)

    for name, m in res.items():
        print(
            f"{name:<34} {m['mean_surplus']:<18.2f} {m['std_surplus']:<18.2f} "
            f"{m['p5_surplus']:<14.2f} {m['prob_deficit']:<10.4f}"
        )

    print("=" * 88)
    print("Key LDI Invariant: Cash is risky for long-horizon liabilities due to reinvestment risk.")
    print("Matching asset duration to liability duration dramatically compresses surplus volatility.")


main()

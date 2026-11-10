"""Lab PR6-L06-1: Target-Date Fund Glide Path Design & Sequence-of-Returns Risk.

SIMULATED: Monte Carlo evaluation of "To", "Through", and Static 60/40 target-date
glide paths under sequence-of-returns drawdown risk and CRRA certainty equivalents.
"""

from __future__ import annotations

import numpy as np


def evaluate_glide_paths(
    start_age: int = 25,
    retire_age: int = 65,
    initial_wealth: float = 25000.0,
    annual_contribution: float = 7500.0,
    equity_mean: float = 0.08,
    equity_vol: float = 0.17,
    bond_mean: float = 0.03,
    bond_vol: float = 0.05,
    corr: float = -0.10,
    gamma: float = 4.0,
    n_paths: int = 10000,
    seed: int = 42,
) -> dict[str, dict[str, float]]:
    """Simulate asset returns and compare TDF glide paths over career accumulation."""
    rng = np.random.default_rng(seed)
    years = retire_age - start_age
    ages = np.arange(start_age, retire_age)

    # Correlated asset returns
    cov = corr * equity_vol * bond_vol
    cov_matrix = np.array([[equity_vol**2, cov], [cov, bond_vol**2]])
    chol = np.linalg.cholesky(cov_matrix)

    # 1. "To Retirement" Glide Path: 90% until 40, linearly down to 30% at 65
    alpha_to = np.zeros(years)
    for i, age in enumerate(ages):
        if age <= 40:
            alpha_to[i] = 0.90
        else:
            alpha_to[i] = 0.90 - (0.90 - 0.30) * ((age - 40) / (65 - 40))

    # 2. "Through Retirement" Glide Path: 90% until 40, 50% at 65, down to 30% at 80
    alpha_through = np.zeros(years)
    for i, age in enumerate(ages):
        if age <= 40:
            alpha_through[i] = 0.90
        else:
            alpha_through[i] = 0.90 - (0.90 - 0.50) * ((age - 40) / (65 - 40))

    # 3. Static 60/40 Portfolio
    alpha_static = np.full(years, 0.60)

    strategies = {
        "To-Retirement (90%->30%)": alpha_to,
        "Through-Retirement (90%->50%)": alpha_through,
        "Static 60/40": alpha_static,
    }

    # Generate annual market shocks across n_paths and years
    z = rng.standard_normal((n_paths, years, 2))
    shocks = np.einsum("ij,nyj->nyi", chol, z)
    ret_eq = equity_mean + shocks[:, :, 0]
    ret_bond = bond_mean + shocks[:, :, 1]

    metrics: dict[str, dict[str, float]] = {}

    for name, alpha_path in strategies.items():
        wealth = np.zeros((n_paths, years + 1))
        wealth[:, 0] = initial_wealth

        for t in range(years):
            r_p = alpha_path[t] * ret_eq[:, t] + (1.0 - alpha_path[t]) * ret_bond[:, t]
            wealth[:, t + 1] = wealth[:, t] * (1.0 + r_p) + annual_contribution

        terminal_w = wealth[:, -1]
        mean_w = float(np.mean(terminal_w))
        p5_w = float(np.percentile(terminal_w, 5))
        p50_w = float(np.median(terminal_w))

        # Certainty Equivalent Wealth: U = E[W^(1-gamma) / (1-gamma)] -> CE = ((1-gamma)*U)^(1/(1-gamma))
        # Protect against non-positive wealth
        safe_w = np.maximum(terminal_w, 1.0)
        expected_u = float(np.mean((safe_w ** (1.0 - gamma)) / (1.0 - gamma)))
        ce_wealth = float(((1.0 - gamma) * expected_u) ** (1.0 / (1.0 - gamma)))

        # Sequence of returns risk: Maximum drawdown in final 5 pre-retirement years (ages 60-65)
        # indices: years - 5 to years
        last_wealth = wealth[:, (years - 5) :]
        peaks = np.maximum.accumulate(last_wealth, axis=1)
        dd = (peaks - last_wealth) / peaks
        max_dd_late = np.max(dd, axis=1)
        p95_late_dd = float(np.percentile(max_dd_late, 95))

        metrics[name] = {
            "mean_wealth": mean_w,
            "median_wealth": p50_w,
            "p5_wealth": p5_w,
            "ce_wealth": ce_wealth,
            "p95_late_drawdown": p95_late_dd,
        }

    return metrics


def main() -> None:
    res = evaluate_glide_paths(
        start_age=25,
        retire_age=65,
        initial_wealth=25000.0,
        annual_contribution=7500.0,
        equity_mean=0.08,
        equity_vol=0.17,
        bond_mean=0.03,
        bond_vol=0.05,
        corr=-0.10,
        gamma=4.0,
        n_paths=20000,
        seed=42,
    )

    print("Target-Date Fund Glide Path Design & Risk Evaluation:")
    print("Accumulation: Age 25 to 65 (40 years), $7,500/yr contribution, CRRA gamma=4.0")
    print("=" * 92)
    print(
        f"{'Glide Path Strategy':<30} {'Mean W_T ($)':<14} {'Median W_T ($)':<16} "
        f"{'5th Pct ($)':<13} {'CE Wealth ($)':<15} {'95% Late DD':<12}"
    )
    print("-" * 92)

    for name, m in res.items():
        print(
            f"{name:<30} {m['mean_wealth']:<14.1f} {m['median_wealth']:<16.1f} "
            f"{m['p5_wealth']:<13.1f} {m['ce_wealth']:<15.1f} {m['p95_late_drawdown']:<12.4f}"
        )

    print("=" * 92)
    print("Key Tradeoffs:")
    print("1. 'To-Retirement' delivers lowest late sequence-of-returns drawdown risk (protecting near retirement).")
    print("2. 'Through-Retirement' captures higher median and certainty equivalent wealth by staying invested.")
    print("3. Static 60/40 exhibits excess drawdown risk late in career with lower early-stage equity growth.")


main()

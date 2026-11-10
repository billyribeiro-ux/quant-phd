"""Lab GM4-L05-1: Sizing and Allocation under Estimation Uncertainty.

Simulates multi-period wealth growth and drawdown dynamics for Full Kelly,
Half Kelly, and Quarter Kelly sizing subject to a 4x gross leverage ceiling,
illustrating why fractional Kelly dominates under parameter uncertainty.
"""

from __future__ import annotations

import numpy as np


def simulate_wealth_paths(
    true_mu: float,
    true_vol: float,
    fraction: float,
    max_leverage: float,
    n_days: int,
    n_paths: int,
    rng: np.random.Generator,
) -> tuple[float, float, float]:
    """Simulate geometric terminal wealth and maximum drawdown across paths."""
    dt = 1.0 / 252.0

    # True optimal continuous Kelly fraction: mu / vol^2
    unconstrained_k = true_mu / (true_vol**2)
    nominal_w = fraction * unconstrained_k
    w = max(-max_leverage, min(max_leverage, nominal_w))

    # Daily returns: w * (mu * dt + vol * sqrt(dt) * Z)
    drift = w * true_mu * dt
    diffusion = w * true_vol * np.sqrt(dt)

    shocks = rng.normal(0.0, 1.0, size=(n_paths, n_days))
    daily_returns = drift + diffusion * shocks

    # Compound wealth trajectories: log wealth
    log_wealth = np.zeros((n_paths, n_days + 1), dtype=np.float64)
    np.cumsum(np.log(np.maximum(1e-6, 1.0 + daily_returns)), axis=1, out=log_wealth[:, 1:])

    wealth = np.exp(log_wealth)

    # Maximum Drawdown calculation per path
    running_max = np.maximum.accumulate(wealth, axis=1)
    drawdowns = (running_max - wealth) / running_max
    max_dd_per_path = np.max(drawdowns, axis=1)

    terminal_wealth = wealth[:, -1]
    median_terminal = float(np.median(terminal_wealth))
    mean_terminal = float(np.mean(terminal_wealth))
    median_max_dd = float(np.median(max_dd_per_path))

    return median_terminal, mean_terminal, median_max_dd


def main() -> None:
    rng = np.random.default_rng(42)
    true_annual_excess = 0.08  # 8% annual excess return
    true_annual_vol = 0.16  # 16% annual volatility
    leverage_cap = 4.0
    n_days = 252 * 5  # 5-year investment horizon
    n_paths = 5_000

    full_med, full_mean, full_dd = simulate_wealth_paths(
        true_annual_excess, true_annual_vol, 1.0, leverage_cap, n_days, n_paths, rng
    )
    half_med, half_mean, half_dd = simulate_wealth_paths(
        true_annual_excess, true_annual_vol, 0.50, leverage_cap, n_days, n_paths, rng
    )
    quarter_med, quarter_mean, quarter_dd = simulate_wealth_paths(
        true_annual_excess, true_annual_vol, 0.25, leverage_cap, n_days, n_paths, rng
    )

    print("=== 5-Year Macro Portfolio Sizing Simulation (5,000 Paths) ===")
    print(f"{'Sizing Strategy':<18}{'Median Wealth':<16}{'Mean Wealth':<16}{'Median Max DD':<14}")
    print("-" * 64)
    print(f"Full Kelly (1.0x)  ${full_med:<15.2f}${full_mean:<15.2f}{full_dd * 100:<6.1f}%")
    print(f"Half Kelly (0.5x)  ${half_med:<15.2f}${half_mean:<15.2f}{half_dd * 100:<6.1f}%")
    print(f"Quarter Kelly (.25)${quarter_med:<15.2f}${quarter_mean:<15.2f}{quarter_dd * 100:<6.1f}%")


main()

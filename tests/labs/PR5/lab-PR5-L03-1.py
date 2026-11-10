"""Lab PR5-L03-1: Drawdown Stop-Loss Hitting Dynamics and Manager Firing Rates.

SIMULATED: First passage times to drawdown stop-loss boundaries across manager skill levels.
"""

from __future__ import annotations

import math

import numpy as np


def simulate_stop_loss_dynamics(
    stop_threshold: float = 0.08,
    sigma: float = 0.15,
    t_years: float = 1.0,
    n_steps: int = 252,
    n_paths: int = 5000,
    seed: int = 42,
) -> dict[str, dict[str, float]]:
    """Simulate stopping times and liquidation rates for managers with varying drift."""
    rng = np.random.default_rng(seed)
    dt = t_years / float(n_steps)
    sqrt_dt = math.sqrt(dt)

    manager_profiles = {
        "High Skill (SR=1.0)": 0.15,
        "Moderate Skill (SR=0.4)": 0.06,
        "Zero Alpha (SR=0.0)": 0.00,
        "Decaying Alpha (SR=-0.67)": -0.10,
    }

    results: dict[str, dict[str, float]] = {}

    for name, mu in manager_profiles.items():
        z = rng.standard_normal((n_paths, n_steps))
        r_daily = (mu - 0.5 * sigma**2) * dt + sigma * sqrt_dt * z
        log_paths = np.cumsum(r_daily, axis=1)
        log_paths = np.hstack([np.zeros((n_paths, 1)), log_paths])
        wealth = np.exp(log_paths)

        peaks = np.maximum.accumulate(wealth, axis=1)
        drawdowns = (peaks - wealth) / peaks

        # First hitting time of stop threshold
        stopped_mask = np.any(drawdowns >= stop_threshold, axis=1)
        stop_rate = float(np.mean(stopped_mask))

        # For stopped paths, find exact step of stopping
        stop_steps = np.argmax(drawdowns >= stop_threshold, axis=1)
        valid_stop_steps = stop_steps[stopped_mask]
        mean_stop_step = float(np.mean(valid_stop_steps)) if len(valid_stop_steps) > 0 else float("nan")

        # Terminal wealth without stop vs with stop (frozen at stop)
        w_terminal_unstopped = wealth[:, -1]
        w_terminal_stopped = w_terminal_unstopped.copy()
        for i in range(n_paths):
            if stopped_mask[i]:
                w_terminal_stopped[i] = wealth[i, stop_steps[i]]

        results[name] = {
            "stop_rate": stop_rate,
            "mean_stop_day": mean_stop_step,
            "unstopped_mean_w": float(np.mean(w_terminal_unstopped)),
            "stopped_mean_w": float(np.mean(w_terminal_stopped)),
            "unstopped_median_w": float(np.median(w_terminal_unstopped)),
            "stopped_median_w": float(np.median(w_terminal_stopped)),
        }

    return results


def main() -> None:
    stop_h = 0.08
    sim = simulate_stop_loss_dynamics(stop_threshold=stop_h, seed=42)

    print(f"Drawdown Stop-Loss Dynamics (Stop Threshold h={stop_h * 100:.1f}%, T=1.0 yr):")
    print("=" * 76)
    hdr = (
        f"{'Manager Profile':<26} {'Stop Rate':<12} {'Mean Stop Day':<15} "
        f"{'Mean W (No Stop)':<18} {'Mean W (Stopped)':<16}"
    )
    print(hdr)
    print("-" * 76)

    for profile, r in sim.items():
        print(
            f"{profile:<26} {r['stop_rate']:<12.4f} {r['mean_stop_day']:<15.1f} "
            f"{r['unstopped_mean_w']:<18.4f} {r['stopped_mean_w']:<16.4f}"
        )


main()

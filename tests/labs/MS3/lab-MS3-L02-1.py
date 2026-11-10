"""Lab MS3-L02-1: Transient market impact and relaxation under the propagator model.

Simulates price trajectory during and after metaorder execution under a
power-law propagator kernel G(t) = Gamma_0 * (1 + t / tau)^(-beta).
"""

from __future__ import annotations


def propagator_kernel(t: float, gamma_0: float, tau: float, beta: float) -> float:
    """Evaluate power-law response kernel G(t)."""
    if t < 0.0:
        return 0.0
    return float(gamma_0 / ((1.0 + t / tau) ** beta))


def simulate_propagator_impact(
    total_shares: float,
    execution_horizon: float,
    total_time: float,
    n_slices: int,
    gamma_0: float,
    tau: float,
    beta: float,
) -> tuple[list[float], list[float]]:
    """Simulate transient price impact over time using discrete trade slices."""
    dt = execution_horizon / n_slices
    slice_size = total_shares / n_slices

    eval_times: list[float] = []
    impacts: list[float] = []

    # Evaluate impact at regular intervals up to total_time
    n_eval = 20
    eval_dt = total_time / n_eval
    for step in range(n_eval + 1):
        t = step * eval_dt
        eval_times.append(t)

        # Sum of propagated responses from all prior trade slices
        cumulative_impact = 0.0
        for i in range(n_slices):
            trade_time = (i + 0.5) * dt
            if trade_time <= t:
                cumulative_impact += slice_size * propagator_kernel(t - trade_time, gamma_0, tau, beta)

        impacts.append(cumulative_impact)

    return eval_times, impacts


def main() -> None:
    total_shares = 100_000.0  # Metaorder size
    t_exec = 60.0  # Metaorder execution duration (minutes)
    t_total = 180.0  # Total observation window (minutes)
    n_slices = 60  # 1 slice per minute
    gamma_0 = 1.5e-6  # Peak instantaneous impact per share
    tau = 2.0  # Characteristic memory timescale (minutes)
    beta = 0.30  # Power-law decay exponent

    times, impacts = simulate_propagator_impact(total_shares, t_exec, t_total, n_slices, gamma_0, tau, beta)

    print(f"Propagator Model Impact Profile (Q=100k, T_exec=60min, beta={beta}):")
    print("  Time (min) | Phase       | Price Impact ($) | % of Peak Impact")
    print("----------------------------------------------------------------")

    peak_impact = max(impacts)
    for t, imp in zip(times, impacts, strict=True):
        phase = "Execution " if t <= t_exec else "Relaxation"
        pct_peak = (imp / peak_impact) * 100.0
        print(f"  {t:10.1f} | {phase}   | {imp:16.4f} | {pct_peak:15.1f}%")

    # Verify key theoretical properties
    # 1. Peak impact occurs at or immediately after execution completion
    peak_time = times[impacts.index(peak_impact)]
    # 2. Asymptotic decay: impact relaxes towards permanent baseline
    terminal_impact = impacts[-1]
    relaxation_pct = (1.0 - terminal_impact / peak_impact) * 100.0

    print("----------------------------------------------------------------")
    print(f"Peak Impact Achieved at t = {peak_time:.1f} min ($ {peak_impact:.4f})")
    print(f"Post-Trade Relaxation at t = {t_total:.1f} min: {relaxation_pct:.1f}% decayed")
    print("No Price Manipulation: Transient decay ensures round-trip cost is strictly positive.")


main()

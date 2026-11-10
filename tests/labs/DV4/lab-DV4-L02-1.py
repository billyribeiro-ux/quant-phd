"""Lab 1 (L02): American put early-exercise boundary and smooth pasting condition.

SIMULATED market parameters under geometric Brownian motion.
Traces the discrete critical stock price S*(t) at each time step where early exercise
becomes optimal, and estimates option Delta along the exercise boundary.
"""

from __future__ import annotations

import math

import numpy as np


def trace_early_exercise_boundary() -> None:
    spot = 100.0
    strike = 100.0
    rate = 0.05
    vol = 0.25
    maturity = 1.0
    n_steps = 150

    dt = maturity / n_steps
    dx = vol * math.sqrt(3.0 * dt)
    u = math.exp(dx)
    1.0 / u
    df = math.exp(-rate * dt)
    nu = (rate - 0.5 * vol * vol) * dt

    pu = 1.0 / 6.0 + 0.5 * (nu * nu / (dx * dx) + nu / dx)
    pm = 2.0 / 3.0 - (nu * nu / (dx * dx))
    pd = 1.0 / 6.0 + 0.5 * (nu * nu / (dx * dx) - nu / dx)

    indices = np.arange(-n_steps, n_steps + 1)
    s_terminal = spot * np.exp(indices * dx)
    v = np.maximum(strike - s_terminal, 0.0)

    # Store early exercise boundary S*(t) across representative maturities
    check_times = [0.25, 0.50, 0.75, 1.00]
    critical_s: dict[float, float] = {}
    boundary_deltas: dict[float, float] = {}

    for k in range(n_steps - 1, -1, -1):
        t_curr = k * dt
        v_cont = df * (pu * v[2 : 2 * k + 3] + pm * v[1 : 2 * k + 2] + pd * v[0 : 2 * k + 1])
        k_indices = np.arange(-k, k + 1)
        s_k = spot * np.exp(k_indices * dx)
        intrinsic = np.maximum(strike - s_k, 0.0)

        # Early exercise condition
        exercise = intrinsic > v_cont
        v = np.maximum(v_cont, intrinsic)

        # Record critical stock price S*(t) = highest stock price where exercise is optimal
        s_crit = float(np.max(s_k[exercise])) if np.any(exercise) else float(s_k[0])

        for target_t in check_times:
            if abs(t_curr - target_t) < 0.5 * dt:
                critical_s[target_t] = s_crit
                # Compute delta at the boundary
                crit_idx = int(np.where(s_k == s_crit)[0][0])
                if crit_idx < len(v) - 1:
                    d_val = float((v[crit_idx + 1] - v[crit_idx]) / (s_k[crit_idx + 1] - s_k[crit_idx]))
                else:
                    d_val = -1.0
                boundary_deltas[target_t] = d_val

    print(f"American put price at t=0: {float(v[0]):.4f}")
    print("Early exercise boundary S*(t) and boundary Delta:")
    for t_val in sorted(critical_s):
        print(f"  t = {t_val:.2f} yr | S*(t) = {critical_s[t_val]:.2f} | Boundary Delta = {boundary_deltas[t_val]:.4f}")

    # Monotonicity check: S*(t) is non-decreasing as t -> T (maturity approaches)
    t_sorted = sorted(critical_s.keys())
    is_monotonic = all(critical_s[t_sorted[i]] <= critical_s[t_sorted[i + 1]] + 1e-4 for i in range(len(t_sorted) - 1))
    print(f"Boundary monotonicity S*(t1) <= S*(t2) for t1 < t2: {is_monotonic}")


trace_early_exercise_boundary()

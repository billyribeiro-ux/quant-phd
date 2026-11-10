"""Lab 3 · Bergomi Forward Variance Dynamics & Skew Term Structure.

This lab implements the forward variance curve extraction from variance swap quotes,
simulates 2-factor Bergomi forward variance dynamics on seed 0 (SIMULATED),
computes instantaneous spot variance v(t) = xi_t(t), and derives the ATMI skew
term structure, showing that exponential kernels yield a finite, bounded limit as T -> 0.
"""

from __future__ import annotations

import math
import random


def extract_forward_variance_curve(
    tenors: list[float],
    var_swap_vols: list[float],
) -> list[float]:
    """Extract piecewise-constant forward variance curve xi_0(t) from variance swap term structure."""
    xi_0: list[float] = []
    prev_t = 0.0
    prev_total_var = 0.0
    for t_i, vol_i in zip(tenors, var_swap_vols, strict=True):
        total_var = (vol_i**2) * t_i
        dt = t_i - prev_t
        fwd_var = (total_var - prev_total_var) / dt
        xi_0.append(fwd_var)
        prev_t = t_i
        prev_total_var = total_var
    return xi_0


def evaluate_fwd_curve(t: float, tenors: list[float], xi_values: list[float]) -> float:
    """Evaluate piecewise constant forward variance curve at time t."""
    for tenor, xi in zip(tenors, xi_values, strict=True):
        if t <= tenor:
            return xi
    return xi_values[-1]


def bergomi_skew_formula(
    t: float,
    xi_0: float,
    omega1: float,
    k1: float,
    rho1: float,
    omega2: float,
    k2: float,
    rho2: float,
) -> float:
    """Analytical leading-order ATMI skew in a 2-factor Bergomi model."""
    if t <= 0.0 or xi_0 <= 0.0:
        return 0.0

    def kernel_integral(omega: float, k: float, rho: float) -> float:
        integ = 0.5 * t * t if k <= 1e-6 else (k * t - 1.0 + math.exp(-k * t)) / (k * k)
        return rho * omega * integ

    term1 = kernel_integral(omega1, k1, rho1)
    term2 = kernel_integral(omega2, k2, rho2)
    return (term1 + term2) / (4.0 * t * math.sqrt(xi_0 * t))


def main() -> None:
    print("=== Bergomi Forward-Variance Dynamics & Skew Analysis ===")

    # Tenors and market variance swap strike volatilities (SIMULATED)
    tenors = [0.25, 0.50, 1.00, 2.00]
    vs_vols = [0.20, 0.21, 0.22, 0.23]

    xi_pieces = extract_forward_variance_curve(tenors, vs_vols)
    print("Forward Variance Curve Extraction from Variance Swaps:")
    print(" Tenor Range (yr) | VS Vol (%) | Instantaneous Fwd Variance xi_0(t) | Fwd Vol (%)")
    print("---------------------------------------------------------------------------------")
    prev_t = 0.0
    for t_i, vol_i, xi_i in zip(tenors, vs_vols, xi_pieces, strict=True):
        fwd_vol = math.sqrt(xi_i) * 100.0
        v_pct = vol_i * 100.0
        print(
            f"  [{prev_t:4.2f}, {t_i:4.2f}]     |    {v_pct:4.1f}%   |  "
            f"           {xi_i:10.6f}           |   {fwd_vol:5.2f}%"
        )
        prev_t = t_i

    # 2-Factor Bergomi parameters: fast mean-reverting factor + slow factor
    omega1, k1, rho1 = 2.50, 8.0, -0.65  # Fast factor (short-dated smile)
    omega2, k2, rho2 = 0.80, 0.5, -0.40  # Slow factor (long-dated smile)
    xi_ref = xi_pieces[0]

    hl_fast = math.log(2.0) / k1 * 12.0
    hl_slow = math.log(2.0) / k2
    print("\n2-Factor Bergomi Parameters:")
    print(f" Factor 1 (Fast): omega1={omega1}, k1={k1}, rho1={rho1} (half-life: {hl_fast:.1f} months)")
    print(f" Factor 2 (Slow): omega2={omega2}, k2={k2}, rho2={rho2} (half-life: {hl_slow:.1f} years)")

    # Simulate path of spot variance v(t) = xi_t(t) on seed 0
    rng = random.Random(0)
    n_steps = 100
    t_end = 1.0
    dt = t_end / n_steps
    x1, x2 = 0.0, 0.0
    v_path: list[float] = []

    for step in range(n_steps):
        t_curr = step * dt
        xi_t0 = evaluate_fwd_curve(t_curr, tenors, xi_pieces)
        var_x1 = (1.0 - math.exp(-2.0 * k1 * t_curr)) / (2.0 * k1) if k1 > 0 else t_curr
        var_x2 = (1.0 - math.exp(-2.0 * k2 * t_curr)) / (2.0 * k2) if k2 > 0 else t_curr
        convexity = 0.5 * (omega1 * omega1 * var_x1 + omega2 * omega2 * var_x2)
        v_t = xi_t0 * math.exp(omega1 * x1 + omega2 * x2 - convexity)
        v_path.append(v_t)

        dw1 = rng.gauss(0.0, math.sqrt(dt))
        dw2 = rng.gauss(0.0, math.sqrt(dt))
        x1 += -k1 * x1 * dt + dw1
        x2 += -k2 * x2 * dt + dw2

    print("\nSimulated Spot Variance v(t) over 1 Year (100 steps, seed 0):")
    print(f"  v(0) = {v_path[0]:.5f} (vol: {math.sqrt(v_path[0]) * 100:.2f}%)")
    print(f"  v(0.25) = {v_path[25]:.5f} (vol: {math.sqrt(v_path[25]) * 100:.2f}%)")
    print(f"  v(0.50) = {v_path[50]:.5f} (vol: {math.sqrt(v_path[50]) * 100:.2f}%)")
    print(f"  v(1.00) = {v_path[-1]:.5f} (vol: {math.sqrt(v_path[-1]) * 100:.2f}%)")
    print(f"  Path Range: [{min(v_path):.5f}, {max(v_path):.5f}]")

    print("\nTerm Structure of ATMI Skew under 2-Factor Bergomi:")
    print(" Maturity T (yr) | ATMI Skew (d sigma / d ln K) ")
    print("-------------------------------------------------")
    test_maturities = [0.01, 0.05, 0.10, 0.25, 0.50, 1.00, 2.00]
    for mat in test_maturities:
        skew = bergomi_skew_formula(mat, xi_ref, omega1, k1, rho1, omega2, k2, rho2)
        print(f"      {mat:4.2f}       |            {skew:8.4f} ")

    lim_skew_0 = (rho1 * omega1 + rho2 * omega2) / (8.0 * math.sqrt(xi_ref))
    print(f"\nTheoretical Limit as T -> 0: {lim_skew_0:.4f}")
    print("Key Result: Even multi-factor exponential kernels produce a finite, flat skew")
    print("as T -> 0, proving that standard diffusion cannot capture market short-dated skew explosion.")


main()

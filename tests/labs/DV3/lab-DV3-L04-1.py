"""Lab 4 · Rough Fractional Dynamics & ATMI Skew Explosion.

This lab simulates fractional Brownian motion via exact Cholesky factorization of the
covariance matrix for Hurst parameters H=0.10 (rough) and H=0.50 (diffusive) on seed 0 (SIMULATED),
computes pathwise regularity properties, and demonstrates the rBergomi power-law
explosion of short-dated ATMI skew psi(T) ~ T^(H - 1/2).
"""

from __future__ import annotations

import math
import random


def simulate_fbm_cholesky(n: int, h: float, seed: int) -> list[float]:
    """Simulate fractional Brownian motion on [0, 1] using exact Cholesky decomposition."""
    cov: list[list[float]] = [[0.0] * n for _ in range(n)]
    dt = 1.0 / n
    for i in range(n):
        ti = (i + 1) * dt
        for j in range(i + 1):
            tj = (j + 1) * dt
            diff = abs(ti - tj)
            val = 0.5 * (ti ** (2.0 * h) + tj ** (2.0 * h) - diff ** (2.0 * h))
            cov[i][j] = val
            cov[j][i] = val

    l_mat: list[list[float]] = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s_sum = sum(l_mat[i][k] * l_mat[j][k] for k in range(j))
            if i == j:
                diag = cov[i][i] - s_sum
                l_mat[i][j] = math.sqrt(max(1e-12, diag))
            else:
                l_mat[i][j] = (cov[i][j] - s_sum) / l_mat[j][j]

    rng = random.Random(seed)
    z = [rng.gauss(0.0, 1.0) for _ in range(n)]
    fbm: list[float] = [0.0] * n
    for i in range(n):
        fbm[i] = sum(l_mat[i][j] * z[j] for j in range(i + 1))
    return fbm


def rbergomi_skew(t: float, h: float, eta: float, rho: float) -> float:
    """Theoretical leading-order rBergomi ATMI skew."""
    if t <= 0.0:
        return 0.0
    denom = 2.0 * (h + 0.5) * (h + 1.5)
    coef = (rho * eta) / denom
    res = coef * (t ** (h - 0.5))
    return float(res)


def main() -> None:
    print("=== Rough Volatility: fBm Simulation & Skew Explosion ===")
    n_pts = 100
    seed = 0

    print(f"Simulating fBm paths (N={n_pts} steps on [0, 1], seed={seed}, SIMULATED):")
    fbm_rough = simulate_fbm_cholesky(n_pts, h=0.10, seed=seed)
    fbm_brown = simulate_fbm_cholesky(n_pts, h=0.50, seed=seed)

    inc_rough = [fbm_rough[i + 1] - fbm_rough[i] for i in range(n_pts - 1)]
    inc_brown = [fbm_brown[i + 1] - fbm_brown[i] for i in range(n_pts - 1)]

    var_r = sum(x * x for x in inc_rough) / len(inc_rough)
    var_b = sum(x * x for x in inc_brown) / len(inc_brown)

    dt_r = (1.0 / n_pts) ** 0.10
    dt_b = (1.0 / n_pts) ** 0.50
    print("\nIncrement Properties:")
    print(f"  H=0.10 (Rough):      Increment Std Dev = {math.sqrt(var_r):.5f} (scaling dt^H = {dt_r:.5f})")
    print(f"  H=0.50 (Diffusive):  Increment Std Dev = {math.sqrt(var_b):.5f} (scaling dt^H = {dt_b:.5f})")

    print("\nSample Path Values along [0, 1]:")
    print(" Time t | W_t^(H=0.10) (Rough) | W_t^(H=0.50) (Standard BM) ")
    print("-------------------------------------------------------------")
    checkpoints = [10, 25, 50, 75, 99]
    for cp in checkpoints:
        t_val = (cp + 1) / n_pts
        print(f"  {t_val:4.2f}  |       {fbm_rough[cp]:8.4f}       |          {fbm_brown[cp]:8.4f} ")

    eta = 1.90
    rho = -0.70
    maturities = [0.005, 0.01, 0.02, 0.05, 0.10, 0.25, 1.00]

    print(f"\nATMI Skew Term Structure (eta={eta}, rho={rho}):")
    print(" Maturity T (yr) | Skew H=0.10 (Rough T^-0.4) | Skew H=0.50 (Diffusive T^0) ")
    print("-----------------------------------------------------------------------------")
    for mat in maturities:
        sk_rough = rbergomi_skew(mat, h=0.10, eta=eta, rho=rho)
        sk_diff = rbergomi_skew(mat, h=0.50, eta=eta, rho=rho)
        print(f"     {mat:6.3f}      |           {sk_rough:8.4f}          |            {sk_diff:8.4f} ")

    print("\nConclusion: At T = 0.005 (approx 1 trading day):")
    print(f"  Rough skew explodes to {rbergomi_skew(0.005, 0.10, eta, rho):.4f}")
    print(f"  Diffusive skew remains flat at {rbergomi_skew(0.005, 0.50, eta, rho):.4f}")
    print("This power-law divergence matches empirical equity index options without artificial jumps.")


main()

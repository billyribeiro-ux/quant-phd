"""Lab S4-L03-1: GARCH(1,1) variance recursion, stationarity, and persistence.

SIMULATED: simulates a stationary GARCH(1,1) process, computes conditional variance
recursion, and verifies empirical sample moments against theoretical unconditional limits.
"""

from __future__ import annotations

import math
import random


def simulate_garch11(
    omega: float, alpha: float, beta: float, n: int, seed: int = 123
) -> tuple[list[float], list[float]]:
    """Simulate GARCH(1,1) process with burn-in."""
    rng = random.Random(seed)
    burn = 500
    uncond_var = omega / (1.0 - alpha - beta)
    h = uncond_var
    for _ in range(burn):
        z = rng.gauss(0.0, 1.0)
        eps = math.sqrt(h) * z
        h = omega + alpha * (eps**2) + beta * h

    epsilons: list[float] = []
    variances: list[float] = []
    for _ in range(n):
        z = rng.gauss(0.0, 1.0)
        eps = math.sqrt(h) * z
        epsilons.append(eps)
        variances.append(h)
        h = omega + alpha * (eps**2) + beta * h
    return epsilons, variances


def main() -> None:
    omega = 0.05
    alpha = 0.10
    beta = 0.85
    n = 10000
    eps, h = simulate_garch11(omega, alpha, beta, n, seed=123)

    var_emp = sum(e * e for e in eps) / n
    mean_h = sum(h) / n
    theo_var = omega / (1.0 - alpha - beta)
    persistence = alpha + beta
    half_life = math.log(0.5) / math.log(persistence)

    print(f"GARCH(1,1) Simulation (omega={omega:.2f}, alpha={alpha:.2f}, beta={beta:.2f}, n={n})")
    print(f"Theoretical unconditional variance: {theo_var:.4f}")
    print(f"Sample mean conditional variance:   {mean_h:.4f}")
    print(f"Sample variance of returns:         {var_emp:.4f}")
    print(f"Persistence (alpha + beta):         {persistence:.4f}")
    print(f"Shock half-life (periods):          {half_life:.2f}")


main()

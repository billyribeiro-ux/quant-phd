"""Lab S4-L02-1: ARCH(1) simulation, moment recursion, and fat tails.

SIMULATED: generates stationary ARCH(1) path and compares empirical variance
and kurtosis against theoretical closed-form population moments.
"""

from __future__ import annotations

import math
import random


def simulate_arch1(omega: float, alpha: float, n: int, seed: int = 42) -> tuple[list[float], list[float]]:
    """Simulate ARCH(1) process with burn-in."""
    rng = random.Random(seed)
    burn = 500
    uncond_var = omega / (1.0 - alpha)
    h = uncond_var
    for _ in range(burn):
        z = rng.gauss(0.0, 1.0)
        eps = math.sqrt(h) * z
        h = omega + alpha * (eps**2)

    epsilons: list[float] = []
    variances: list[float] = []
    for _ in range(n):
        z = rng.gauss(0.0, 1.0)
        eps = math.sqrt(h) * z
        epsilons.append(eps)
        variances.append(h)
        h = omega + alpha * (eps**2)
    return epsilons, variances


def main() -> None:
    omega = 0.20
    alpha = 0.50
    n = 10000
    eps, _ = simulate_arch1(omega, alpha, n, seed=42)

    var_emp = sum(e * e for e in eps) / n
    m4_emp = sum(e**4 for e in eps) / n
    kurt_emp = m4_emp / (var_emp**2)

    theo_var = omega / (1.0 - alpha)
    theo_kurt = 3.0 * (1.0 - alpha**2) / (1.0 - 3.0 * alpha**2)

    print(f"ARCH(1) Simulation (omega={omega:.2f}, alpha={alpha:.2f}, n={n})")
    print(f"Theoretical unconditional variance: {theo_var:.4f}")
    print(f"Empirical sample variance:          {var_emp:.4f}")
    print(f"Theoretical kurtosis:               {theo_kurt:.4f} (excess kurtosis: {theo_kurt - 3.0:.4f})")
    print(f"Empirical sample kurtosis:          {kurt_emp:.4f} (excess kurtosis: {kurt_emp - 3.0:.4f})")
    print(f"Leptokurtic fat tails confirmed:    {kurt_emp > 3.0}")


main()

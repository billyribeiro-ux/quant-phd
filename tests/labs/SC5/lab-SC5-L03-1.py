"""Lab 3 · Infinite divisibility and characteristic exponent scaling in pure-jump Lévy processes.

By the Lévy-Khintchine theorem, every Lévy process (X_t)_{t >= 0} has a characteristic function that scales
linearly in time: E[exp(i*u*X_t)] = exp(t * psi(u)), where psi(u) is the characteristic exponent.
Consequently, for any two horizons t_1 and t_2, the log characteristic functions satisfy the exact scaling:
ln(phi_{X_{t_2}}(u)) / ln(phi_{X_{t_1}}(u)) = t_2 / t_1.
This lab simulates 5,000 realization paths (SIMULATED) of a compound Poisson process with lambda = 3.0 and
jump distribution Normal(0.1, 0.2^2) at t_1 = 0.5 and t_2 = 1.0 using seed 77, computes the empirical
characteristic functions across a frequency grid, and verifies the linear scaling ratio within 5% tolerance.
"""

from __future__ import annotations

import cmath
import math
import random


def main() -> None:
    seed = 77
    rng = random.Random(seed)

    lam = 3.0
    mu_y = 0.10
    sigma_y = 0.20
    t1 = 0.5
    t2 = 1.0
    n_paths = 5000

    # Draw jumps for t1 and increments from t1 to t2
    x_t1: list[float] = []
    x_t2: list[float] = []

    def draw_poisson(l_param: float) -> int:
        p = 1.0
        k = 0
        l_exp = math.exp(-l_param)
        while True:
            p *= rng.random()
            if p <= l_exp:
                break
            k += 1
        return k

    for _ in range(n_paths):
        n1 = draw_poisson(lam * t1)
        jumps1 = sum(rng.gauss(mu_y, sigma_y) for _ in range(n1))
        x_t1.append(jumps1)

        n_inc = draw_poisson(lam * (t2 - t1))
        jumps_inc = sum(rng.gauss(mu_y, sigma_y) for _ in range(n_inc))
        x_t2.append(jumps1 + jumps_inc)

    # Evaluate empirical characteristic functions at test frequency u = 1.5
    u = 1.5
    theo_ratio = t2 / t1

    emp_phi_t1 = sum(cmath.exp(1j * u * x) for x in x_t1) / n_paths
    emp_phi_t2 = sum(cmath.exp(1j * u * x) for x in x_t2) / n_paths

    log_phi_t1 = cmath.log(emp_phi_t1)
    log_phi_t2 = cmath.log(emp_phi_t2)

    emp_ratio_real = log_phi_t2.real / log_phi_t1.real
    emp_ratio_imag = log_phi_t2.imag / log_phi_t1.imag

    print(f"simulated paths (SIMULATED): {n_paths}, horizons: t1 = {t1}, t2 = {t2}")
    print(f"theoretical scaling ratio t2 / t1 = {theo_ratio:.4f}")
    print(f"empirical log CF at t1: real = {log_phi_t1.real:.6f}, imag = {log_phi_t1.imag:.6f}")
    print(f"empirical log CF at t2: real = {log_phi_t2.real:.6f}, imag = {log_phi_t2.imag:.6f}")
    print(f"empirical ratio: real part = {emp_ratio_real:.4f}, imaginary part = {emp_ratio_imag:.4f}")
    print(
        "real part scaling within 5% of theoretical 2.0:",
        abs(emp_ratio_real - theo_ratio) <= 0.05 * theo_ratio,
    )
    print(
        "imaginary part scaling within 5% of theoretical 2.0:",
        abs(emp_ratio_imag - theo_ratio) <= 0.05 * theo_ratio,
    )


main()

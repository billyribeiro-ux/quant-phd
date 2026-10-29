"""M4 L06 lab 1: a Student-t draw built from a standard normal over an independent chi-square, and its variance.

Inputs are simulated, not data. Every draw uses one standard normal Z and an independent chi-square W with nu
degrees of freedom, where W is the sum of nu squared standard normals. The draw is t = Z / sqrt(W / nu). Part A seeds
random.Random(20260602 + nu) for nu = 5 and nu = 10, and Part B seeds random.Random(20261102). Each draw takes Z
first, then the nu normals of W, in that order.

Part A: for nu = 5 and nu = 10, the sample mean and the sample variance (divisor n - 1) of t over n = 100000
draws, beside nu / (nu - 2) from the formula for the variance of t.
Part B: for nu = 5, the sample mean of W beside nu, and the sample mean of 1 / W beside 1 / (nu - 2).
Part C: the function t_variance(nu) = nu / (nu - 2) for nu = 3 to 8, and the ValueError it raises for nu = 2.
"""

from __future__ import annotations

import random

SEED = 20260602
N_DRAWS = 100000


def chi_square_and_t(rng: random.Random, nu: int) -> tuple[float, float]:
    """One pair (W, t): W is the sum of nu squared standard normals, and t = Z / sqrt(W / nu) with Z drawn first."""
    z = rng.gauss(0.0, 1.0)
    w = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(nu))
    return w, z / (w / nu) ** 0.5


def t_variance(nu: int) -> float:
    """The variance nu / (nu - 2) of a Student-t with nu degrees of freedom. Raises ValueError unless nu > 2."""
    if nu <= 2:
        raise ValueError(f"the variance of a Student-t with nu = {nu} is infinite; the formula needs nu > 2")
    return nu / (nu - 2)


def mean_and_variance(xs: list[float]) -> tuple[float, float]:
    """The sample mean and the sample variance with divisor n - 1."""
    n = len(xs)
    mean = sum(xs) / n
    variance = sum((x - mean) ** 2 for x in xs) / (n - 1)
    return mean, variance


def main() -> None:
    """Print Parts A, B and C. The seed is fixed, so every run prints the same lines."""
    print("Part A: sample mean and variance of t against nu / (nu - 2)")
    for nu in (5, 10):
        rng = random.Random(SEED + nu)
        ts: list[float] = []
        for _ in range(N_DRAWS):
            _, t = chi_square_and_t(rng, nu)
            ts.append(t)
        mean, variance = mean_and_variance(ts)
        exact = t_variance(nu)
        print(f"nu {nu} sample_mean {mean:.6f} sample_variance {variance:.6f} formula {exact:.6f}")
        print(f"nu {nu} relative_error {(variance - exact) / exact:.6f}")

    print("Part B: chi-square moments for nu = 5")
    rng = random.Random(SEED + 500)
    ws: list[float] = []
    inv_ws: list[float] = []
    for _ in range(N_DRAWS):
        w, _ = chi_square_and_t(rng, 5)
        ws.append(w)
        inv_ws.append(1.0 / w)
    mean_w = sum(ws) / N_DRAWS
    mean_inv = sum(inv_ws) / N_DRAWS
    print(f"nu 5 sample_mean_W {mean_w:.6f} formula {5:.6f}")
    print(f"nu 5 sample_mean_1_over_W {mean_inv:.6f} formula {1 / (5 - 2):.6f}")

    print("Part C: the variance formula for nu = 3 to 8, and the guard at nu = 2")
    for nu in range(3, 9):
        print(f"nu {nu} t_variance {t_variance(nu):.6f}")
    try:
        t_variance(2)
    except ValueError as error:
        print(f"nu 2 raises ValueError {error}")


main()

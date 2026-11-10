"""Lab S2-L09-1: Newey-West HAC standard errors and Bartlett kernel lag truncation.

Validates:
1. Exact mathematical identity between Newey-West with lag L=0 and White (1980) HC0.
2. Coverage breakdown of classical and White standard errors under persistent AR(1) errors.
3. Coverage restoration via Newey-West HAC standard errors with Bartlett weights.

Standard library only.
"""

from __future__ import annotations

import math
import random


def compute_nw_se(
    lag: int,
    x: list[float],
    x_bar: float,
    e: list[float],
    sxx: float,
    meat_white: float,
    n: int,
) -> float:
    gamma_0 = meat_white
    sum_g = 0.0
    for j in range(1, lag + 1):
        weight = 1.0 - j / (lag + 1)
        gamma_j = sum((x[t] - x_bar) * (x[t - j] - x_bar) * e[t] * e[t - j] for t in range(j, n))
        sum_g += 2.0 * weight * gamma_j
    long_run_var = max(1e-12, gamma_0 + sum_g)
    return math.sqrt(long_run_var) / sxx


def main() -> None:
    rng = random.Random(42)
    sample_size = 250
    replications = 2500
    beta_0 = 1.00
    beta_1 = 1.50
    rho_x = 0.60
    rho_u = 0.50
    z_crit = 1.96

    max_diff_l0 = 0.0
    cov_classical = 0
    cov_white = 0
    cov_nw0 = 0
    cov_nw4 = 0
    cov_nw8 = 0

    for _ in range(replications):
        # Generate persistent regressor x_t
        x: list[float] = [0.0] * sample_size
        cur_x = 0.0
        for t in range(sample_size):
            cur_x = rho_x * cur_x + rng.gauss(0.0, 1.0)
            x[t] = cur_x

        # Generate persistent disturbance u_t
        u: list[float] = [0.0] * sample_size
        cur_u = 0.0
        for t in range(sample_size):
            cur_u = rho_u * cur_u + rng.gauss(0.0, 1.0)
            u[t] = cur_u

        # Dependent variable
        y = [beta_0 + beta_1 * xt + ut for xt, ut in zip(x, u, strict=True)]

        x_bar = sum(x) / sample_size
        y_bar = sum(y) / sample_size
        sxx = sum((xt - x_bar) ** 2 for xt in x)
        sxy = sum((xt - x_bar) * (yt - y_bar) for xt, yt in zip(x, y, strict=True))
        b1_hat = sxy / sxx
        e = [yt - (y_bar + b1_hat * (xt - x_bar)) for xt, yt in zip(x, y, strict=True)]

        # Classical OLS standard error
        s2 = sum(et**2 for et in e) / (sample_size - 2)
        se_classical = math.sqrt(s2 / sxx)

        # White HC0 standard error
        meat_white = sum(((xt - x_bar) ** 2) * (et**2) for xt, et in zip(x, e, strict=True))
        se_white = math.sqrt(meat_white) / sxx

        se_nw0 = compute_nw_se(0, x, x_bar, e, sxx, meat_white, sample_size)
        se_nw4 = compute_nw_se(4, x, x_bar, e, sxx, meat_white, sample_size)
        se_nw8 = compute_nw_se(8, x, x_bar, e, sxx, meat_white, sample_size)

        diff = abs(se_nw0 - se_white)
        if diff > max_diff_l0:
            max_diff_l0 = diff

        if b1_hat - z_crit * se_classical <= beta_1 <= b1_hat + z_crit * se_classical:
            cov_classical += 1
        if b1_hat - z_crit * se_white <= beta_1 <= b1_hat + z_crit * se_white:
            cov_white += 1
        if b1_hat - z_crit * se_nw0 <= beta_1 <= b1_hat + z_crit * se_nw0:
            cov_nw0 += 1
        if b1_hat - z_crit * se_nw4 <= beta_1 <= b1_hat + z_crit * se_nw4:
            cov_nw4 += 1
        if b1_hat - z_crit * se_nw8 <= beta_1 <= b1_hat + z_crit * se_nw8:
            cov_nw8 += 1

    rate_classical = cov_classical / replications
    rate_white = cov_white / replications
    rate_nw0 = cov_nw0 / replications
    rate_nw4 = cov_nw4 / replications
    rate_nw8 = cov_nw8 / replications

    print(f"Max abs diff |NW(L=0) - White HC0|: {max_diff_l0:.2e}")
    print("Estimator            | Nominal | Empirical Coverage | Under-coverage")
    print("-" * 68)
    print(f"Classical OLS        |  0.9500 |             {rate_classical:.4f} |        {0.95 - rate_classical:+.4f}")
    print(f"White HC0            |  0.9500 |             {rate_white:.4f} |        {0.95 - rate_white:+.4f}")
    print(f"Newey-West HAC (L=0) |  0.9500 |             {rate_nw0:.4f} |        {0.95 - rate_nw0:+.4f}")
    print(f"Newey-West HAC (L=4) |  0.9500 |             {rate_nw4:.4f} |        {0.95 - rate_nw4:+.4f}")
    print(f"Newey-West HAC (L=8) |  0.9500 |             {rate_nw8:.4f} |        {0.95 - rate_nw8:+.4f}")


main()

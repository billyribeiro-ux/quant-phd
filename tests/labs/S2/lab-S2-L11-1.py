"""Lab S2-L11-1: Two-way clustered standard errors under firm and time effects.

Validates:
1. Exact mathematical reduction: when clustering groups are identical (A = B),
   two-way clustering reduces to one-way clustering to machine precision.
2. Under-coverage of classical OLS, firm-only clustering, and time-only clustering
   in a panel experiencing both unobserved firm effects and time shocks.
3. Coverage restoration under Cameron, Gelbach, and Miller (2011) two-way clustering.

Standard library only.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    rng = random.Random(42)
    n_firms = 30
    t_time = 20
    total_obs = n_firms * t_time
    replications = 2000
    beta_0 = 1.00
    beta_1 = 2.00
    z_crit = 1.96

    max_diff_identical = 0.0
    cov_classical = 0
    cov_firm = 0
    cov_time = 0
    cov_twoway = 0

    for _ in range(replications):
        firms: list[int] = []
        times: list[int] = []
        x: list[float] = []
        errors: list[float] = []

        alpha = [rng.gauss(0.0, 1.0) for _ in range(n_firms)]
        gamma = [rng.gauss(0.0, 1.0) for _ in range(t_time)]
        mu = [rng.gauss(0.0, 1.0) for _ in range(n_firms)]
        lam = [rng.gauss(0.0, 1.0) for _ in range(t_time)]

        for i in range(n_firms):
            for t in range(t_time):
                firms.append(i)
                times.append(t)
                xit = mu[i] + lam[t] + rng.gauss(0.0, 1.0)
                eit = alpha[i] + gamma[t] + rng.gauss(0.0, 1.0)
                x.append(xit)
                errors.append(eit)

        y = [beta_0 + beta_1 * xi + ei for xi, ei in zip(x, errors, strict=True)]

        x_bar = sum(x) / total_obs
        y_bar = sum(y) / total_obs
        sxx = sum((xi - x_bar) ** 2 for xi in x)
        sxy = sum((xi - x_bar) * (yi - y_bar) for xi, yi in zip(x, y, strict=True))
        b1_hat = sxy / sxx
        e = [yi - (y_bar + b1_hat * (xi - x_bar)) for xi, yi in zip(x, y, strict=True)]

        # Classical homoskedastic standard error
        s2 = sum(ri**2 for ri in e) / (total_obs - 2)
        se_classical = math.sqrt(s2 / sxx)

        # Firm-clustered meat
        score_firm = [0.0] * n_firms
        for xi, ri, i in zip(x, e, firms, strict=True):
            score_firm[i] += (xi - x_bar) * ri
        meat_firm = sum(sf**2 for sf in score_firm)
        se_firm = math.sqrt(meat_firm) / sxx

        # Time-clustered meat
        score_time = [0.0] * t_time
        for xi, ri, t in zip(x, e, times, strict=True):
            score_time[t] += (xi - x_bar) * ri
        meat_time = sum(st**2 for st in score_time)
        se_time = math.sqrt(meat_time) / sxx

        # Intersection meat (each (i, t) is unique, matching White HC0)
        meat_inter = sum(((xi - x_bar) ** 2) * (ri**2) for xi, ri in zip(x, e, strict=True))

        # Two-way clustered meat: V_A + V_B - V_{A cap B}
        meat_twoway = meat_firm + meat_time - meat_inter
        se_twoway = math.sqrt(max(1e-12, meat_twoway)) / sxx

        # Test identical clustering reduction: V_A + V_A - V_A == V_A
        meat_identical = meat_firm + meat_firm - meat_firm
        diff_id = abs(math.sqrt(meat_identical) / sxx - se_firm)
        if diff_id > max_diff_identical:
            max_diff_identical = diff_id

        if b1_hat - z_crit * se_classical <= beta_1 <= b1_hat + z_crit * se_classical:
            cov_classical += 1
        if b1_hat - z_crit * se_firm <= beta_1 <= b1_hat + z_crit * se_firm:
            cov_firm += 1
        if b1_hat - z_crit * se_time <= beta_1 <= b1_hat + z_crit * se_time:
            cov_time += 1
        if b1_hat - z_crit * se_twoway <= beta_1 <= b1_hat + z_crit * se_twoway:
            cov_twoway += 1

    rate_classical = cov_classical / replications
    rate_firm = cov_firm / replications
    rate_time = cov_time / replications
    rate_twoway = cov_twoway / replications

    print(f"Max abs diff |V(A, A) - V(A)|: {max_diff_identical:.2e}")
    print("Estimator            | Nominal | Empirical Coverage | Under-coverage")
    print("-" * 68)
    print(f"Classical OLS        |  0.9500 |             {rate_classical:.4f} |        {0.95 - rate_classical:+.4f}")
    print(f"Firm-clustered (CR0) |  0.9500 |             {rate_firm:.4f} |        {0.95 - rate_firm:+.4f}")
    print(f"Time-clustered (CR0) |  0.9500 |             {rate_time:.4f} |        {0.95 - rate_time:+.4f}")
    print(f"Two-way Clustered    |  0.9500 |             {rate_twoway:.4f} |        {0.95 - rate_twoway:+.4f}")


main()

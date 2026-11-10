"""Lab S2-L10-1: Clustered standard errors and the Moulton design effect.

Simulates a panel dataset with unobserved cluster random effects across G = 50 clusters
and cluster size m = 10 (N = 500). Compares coverage of classical OLS, White HC0,
and cluster-robust CR0 standard errors against nominal 95% confidence intervals.

Standard library only.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    rng = random.Random(42)
    num_clusters = 50
    cluster_size = 10
    total_obs = num_clusters * cluster_size
    replications = 2500
    beta_0 = 1.00
    beta_1 = 2.00
    z_crit = 1.96

    cov_classical = 0
    cov_white = 0
    cov_cr0 = 0

    for _ in range(replications):
        x: list[float] = []
        errors: list[float] = []
        cluster_ids: list[int] = []

        for g in range(num_clusters):
            # Cluster-level random components
            mu_g = rng.gauss(0.0, 1.0)
            alpha_g = rng.gauss(0.0, 1.0)

            for _ in range(cluster_size):
                # Regressor with intra-cluster correlation rho_x = 0.50
                xi = mu_g + rng.gauss(0.0, 1.0)
                # Error with intra-cluster correlation rho_eps = 0.50
                ei = alpha_g + rng.gauss(0.0, 1.0)

                x.append(xi)
                errors.append(ei)
                cluster_ids.append(g)

        # Dependent variable
        y = [beta_0 + beta_1 * xi + ei for xi, ei in zip(x, errors, strict=True)]

        x_bar = sum(x) / total_obs
        y_bar = sum(y) / total_obs
        sxx = sum((xi - x_bar) ** 2 for xi in x)
        sxy = sum((xi - x_bar) * (yi - y_bar) for xi, yi in zip(x, y, strict=True))
        b1_hat = sxy / sxx
        resids = [yi - (y_bar + b1_hat * (xi - x_bar)) for xi, yi in zip(x, y, strict=True)]

        # Classical OLS standard error
        s2 = sum(r**2 for r in resids) / (total_obs - 2)
        se_classical = math.sqrt(s2 / sxx)

        # White HC0 standard error (ignores clustering)
        meat_white = sum(((xi - x_bar) ** 2) * (r**2) for xi, r in zip(x, resids, strict=True))
        se_white = math.sqrt(meat_white) / sxx

        # Cluster-robust CR0 standard error
        cluster_scores = [0.0] * num_clusters
        for xi, r, g in zip(x, resids, cluster_ids, strict=True):
            cluster_scores[g] += (xi - x_bar) * r
        meat_cr0 = sum(sg**2 for sg in cluster_scores)
        se_cr0 = math.sqrt(meat_cr0) / sxx

        if b1_hat - z_crit * se_classical <= beta_1 <= b1_hat + z_crit * se_classical:
            cov_classical += 1
        if b1_hat - z_crit * se_white <= beta_1 <= b1_hat + z_crit * se_white:
            cov_white += 1
        if b1_hat - z_crit * se_cr0 <= beta_1 <= b1_hat + z_crit * se_cr0:
            cov_cr0 += 1

    rate_classical = cov_classical / replications
    rate_white = cov_white / replications
    rate_cr0 = cov_cr0 / replications

    print("Estimator     | Nominal | Empirical Coverage | Under-coverage")
    print("-" * 59)
    print(f"Classical OLS |  0.9500 |             {rate_classical:.4f} |        {0.95 - rate_classical:+.4f}")
    print(f"White HC0     |  0.9500 |             {rate_white:.4f} |        {0.95 - rate_white:+.4f}")
    print(f"Clustered CR0 |  0.9500 |             {rate_cr0:.4f} |        {0.95 - rate_cr0:+.4f}")


main()

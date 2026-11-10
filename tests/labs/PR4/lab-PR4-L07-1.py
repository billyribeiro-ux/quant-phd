"""Lab 7: Tail Dependence and Asymptotic Co-Movement Diagnostics.

Demonstrates that Gaussian copulas exhibit asymptotic tail independence (lambda -> 0),
whereas Student-t copulas maintain strictly positive tail dependence in extreme crashes.
"""

from __future__ import annotations

import math

import numpy as np
import scipy.special
import scipy.stats


def main() -> None:
    rng = np.random.default_rng(42)
    n_sims = 200_000
    rho = 0.60
    nu = 4

    cov = np.array([[1.0, rho], [rho, 1.0]], dtype=np.float64)
    chol = np.linalg.cholesky(cov)

    # 1. Bivariate Gaussian simulation
    z = rng.standard_normal((n_sims, 2)) @ chol.T
    u_norm = 0.5 * (1.0 + scipy.special.erf(z / math.sqrt(2.0)))

    # 2. Bivariate Student-t simulation
    v = rng.chisquare(df=nu, size=(n_sims, 1))
    u_t = scipy.stats.t.cdf(z / np.sqrt(v / float(nu)), df=nu)

    # 3. Closed-form theoretical tail dependence for Student-t (McNeil, Frey & Embrechts 2015)
    # lambda = 2 * t_{nu+1}( -sqrt( (nu+1)*(1-rho) / (1+rho) ) )
    arg = -math.sqrt((nu + 1.0) * (1.0 - rho) / (1.0 + rho))
    lambda_theory = 2.0 * float(scipy.stats.t.cdf(arg, df=nu + 1))

    print(f"Bivariate Correlation rho: {rho:.2f} | Student-t df: {nu}")
    print(f"Theoretical Student-t Tail Dependence Coefficient lambda_U: {lambda_theory:.4f}")
    print("Theoretical Gaussian Tail Dependence Coefficient lambda_U:  0.0000 (asymptotically zero)")
    print("=" * 70)
    print(f"{'Quantile q':<12} | {'Gaussian lambda_q':<20} | {'Student-t lambda_q':<20}")
    print("-" * 70)

    quantiles = [0.90, 0.95, 0.99, 0.995]
    for q in quantiles:
        lam_g = float(np.mean((u_norm[:, 0] > q) & (u_norm[:, 1] > q))) / (1.0 - q)
        lam_t = float(np.mean((u_t[:, 0] > q) & (u_t[:, 1] > q))) / (1.0 - q)
        print(f"{q:<12.3f} | {lam_g:<20.4f} | {lam_t:<20.4f}")


main()

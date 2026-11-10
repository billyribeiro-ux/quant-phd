"""Lab 3: The 1/N equal-weight benchmark vs optimal mean-variance portfolios.

Illustrative inputs in exact Fraction arithmetic.
Verifies the analytic theorem: under identical expected returns and diagonal,
homoskedastic covariances, the 1/N allocation is identical to both the
minimum-variance and mean-variance portfolios. When parameters diverge,
the optimal weights differ substantially from 1/N.
"""

from __future__ import annotations

from fractions import Fraction


def main() -> None:
    # 1. Symmetric case: N = 3 identical, uncorrelated assets
    n = 3
    sigma2 = Fraction(4, 100)
    mu_sym = [Fraction(5, 100)] * n
    w_1n = [Fraction(1, n)] * n

    # Analytical GMV: w_i = (1 / sigma_i^2) / sum(1 / sigma_k^2)
    inv_diag_sym = [Fraction(1) / sigma2] * n
    sum_inv_sym = sum(inv_diag_sym)
    w_gmv_sym = [inv_diag_sym[i] / sum_inv_sym for i in range(n)]

    # Analytical MV: w = w_gmv + (1/gamma) * (inv_mu - nu * inv_iota)
    gamma = Fraction(2)
    inv_mu_sym = [inv_diag_sym[i] * mu_sym[i] for i in range(n)]
    nu_sym = (sum(inv_mu_sym) - gamma) / sum_inv_sym
    w_mv_sym = [(inv_mu_sym[i] - nu_sym * inv_diag_sym[i]) / gamma for i in range(n)]

    print("Symmetric 1/N weights:", [str(x) for x in w_1n])
    print("Symmetric GMV weights:", [str(x) for x in w_gmv_sym])
    print("Symmetric MV weights:", [str(x) for x in w_mv_sym])
    print("Symmetric matches 1/N exactly:", w_1n == w_gmv_sym == w_mv_sym)

    # 2. Asymmetric case: unequal means and variances
    mu_asym = [Fraction(6, 100), Fraction(4, 100), Fraction(2, 100)]
    var_asym = [Fraction(4, 100), Fraction(9, 100), Fraction(16, 100)]
    inv_diag_asym = [Fraction(1) / v for v in var_asym]
    sum_inv_asym = sum(inv_diag_asym)
    w_gmv_asym = [inv_diag_asym[i] / sum_inv_asym for i in range(n)]

    inv_mu_asym = [inv_diag_asym[i] * mu_asym[i] for i in range(n)]
    nu_asym = (sum(inv_mu_asym) - gamma) / sum_inv_asym
    w_mv_asym = [(inv_mu_asym[i] - nu_asym * inv_diag_asym[i]) / gamma for i in range(n)]

    print("Asymmetric 1/N weights:", [str(x) for x in w_1n])
    print("Asymmetric GMV weights:", [str(x) for x in w_gmv_asym])
    print("Asymmetric MV weights:", [str(x) for x in w_mv_asym])
    print("Asymmetric gap to 1/N:", [str(w_mv_asym[i] - w_1n[i]) for i in range(n)])


main()

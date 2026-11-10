"""Lab AP2-L04-1: The CAPM pricing equation and beta in market equilibrium.

Hypothetical parameters (3 assets), not real data.
In competitive equilibrium with identical beliefs and mean-variance utility,
the market portfolio clears as the tangency portfolio.
Verifies that beta from covariances satisfies the CAPM pricing equation exactly.
"""

from __future__ import annotations

from fractions import Fraction


def invert_3x3(mat: list[list[Fraction]]) -> list[list[Fraction]]:
    """Invert 3x3 matrix using exact row elimination."""
    n = 3
    aug = [[mat[i][j] for j in range(n)] + [Fraction(1 if i == k else 0) for k in range(n)] for i in range(n)]
    for i in range(n):
        p = aug[i][i]
        for j in range(2 * n):
            aug[i][j] /= p
        for r in range(n):
            if r != i:
                f = aug[r][i]
                for j in range(2 * n):
                    aug[r][j] -= f * aug[i][j]
    return [[aug[i][n + j] for j in range(n)] for i in range(n)]


def main() -> None:
    cov = [
        [Fraction(4, 100), Fraction(1, 100), Fraction(1, 100)],
        [Fraction(1, 100), Fraction(5, 100), Fraction(2, 100)],
        [Fraction(1, 100), Fraction(2, 100), Fraction(6, 100)],
    ]
    mu = [Fraction(6, 100), Fraction(10, 100), Fraction(12, 100)]
    r_f = Fraction(2, 100)

    # In equilibrium, market portfolio equals tangency portfolio
    inv = invert_3x3(cov)
    excess = [mu[i] - r_f for i in range(3)]
    inv_excess = [sum((inv[i][j] * excess[j] for j in range(3)), Fraction(0, 1)) for i in range(3)]
    denom_t = sum(inv_excess, Fraction(0, 1))
    w_m = [inv_excess[i] / denom_t for i in range(3)]

    # Market expected return and variance
    mu_m = sum((w_m[i] * mu[i] for i in range(3)), Fraction(0, 1))
    cov_i_m = [sum((cov[i][j] * w_m[j] for j in range(3)), Fraction(0, 1)) for i in range(3)]
    var_m = sum((w_m[i] * cov_i_m[i] for i in range(3)), Fraction(0, 1))

    # Market beta: beta_i = Cov(r_i, r_m) / Var(r_m)
    betas = [cov_i_m[i] / var_m for i in range(3)]

    # CAPM pricing equation: E[r_i] - r_f = beta_i * (E[r_m] - r_f)
    equity_risk_premium = mu_m - r_f
    capm_excess = [betas[i] * equity_risk_premium for i in range(3)]
    capm_expected = [r_f + capm_excess[i] for i in range(3)]

    print(f"Market weights: [{w_m[0]}, {w_m[1]}, {w_m[2]}]")
    print(f"Market expected return E[r_m]: {mu_m}")
    print(f"Market variance Var(r_m): {var_m}")
    print(f"Equity risk premium E[r_m] - r_f: {equity_risk_premium}")
    print(f"Asset betas: [{betas[0]}, {betas[1]}, {betas[2]}]")
    print(f"CAPM expected returns: [{capm_expected[0]}, {capm_expected[1]}, {capm_expected[2]}]")
    print(f"Actual expected returns: [{mu[0]}, {mu[1]}, {mu[2]}]")
    print(f"CAPM identity holds exactly: {capm_expected == mu}")


main()

"""Lab AP2-L07-1: The Roll Critique: proxy efficiency and the exact Security Market Line.

Hypothetical parameters (3 assets), not real data.
Evaluates the SML pricing equation against:
(1) the true tangency portfolio w_T, and
(2) an inefficient market proxy w_proxy (equal weights [1/3, 1/3, 1/3]).
Demonstrates that the SML holds if and only if the proxy is mean-variance efficient.
All calculations performed in exact Fraction arithmetic.
"""

from __future__ import annotations

from fractions import Fraction


def main() -> None:
    cov = [
        [Fraction(4, 100), Fraction(1, 100), Fraction(1, 100)],
        [Fraction(1, 100), Fraction(5, 100), Fraction(2, 100)],
        [Fraction(1, 100), Fraction(2, 100), Fraction(6, 100)],
    ]
    mu = [Fraction(6, 100), Fraction(10, 100), Fraction(12, 100)]
    r_f = Fraction(2, 100)

    # Tangency portfolio from L02
    w_t = [Fraction(21, 131), Fraction(49, 131), Fraction(61, 131)]

    # Non-tangency proxy: equal weights
    w_proxy = [Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)]

    # Helper to evaluate SML for any chosen index/proxy portfolio w
    def evaluate_sml(w: list[Fraction], name: str) -> tuple[list[Fraction], list[Fraction], Fraction]:
        mu_p = sum((w[i] * mu[i] for i in range(3)), Fraction(0, 1))
        cov_i_p = [sum((cov[i][j] * w[j] for j in range(3)), Fraction(0, 1)) for i in range(3)]
        var_p = sum((w[i] * cov_i_p[i] for i in range(3)), Fraction(0, 1))
        betas = [cov_i_p[i] / var_p for i in range(3)]
        erp_p = mu_p - r_f
        alphas = [(mu[i] - r_f) - betas[i] * erp_p for i in range(3)]

        print(f"--- Proxy: {name} ---")
        print(f"Weights:               [{w[0]}, {w[1]}, {w[2]}]")
        print(f"Expected return:       {mu_p}")
        print(f"Variance:              {var_p}")
        print(f"Betas:                 [{betas[0]}, {betas[1]}, {betas[2]}]")
        print(f"Pricing errors (alpha):[{alphas[0]}, {alphas[1]}, {alphas[2]}]")
        return betas, alphas, erp_p

    _, alphas_t, _ = evaluate_sml(w_t, "Tangency Portfolio (Efficient)")
    print(f"SML holds exactly on Tangency: {all(a == Fraction(0, 1) for a in alphas_t)}")

    _, alphas_proxy, _ = evaluate_sml(w_proxy, "Equal-Weighted Proxy (Inefficient)")
    print(f"SML holds on Inefficient Proxy: {all(a == Fraction(0, 1) for a in alphas_proxy)}")
    eff_ok = all(a == Fraction(0, 1) for a in alphas_t)
    ineff_fail = not all(a == Fraction(0, 1) for a in alphas_proxy)
    print(f"Roll conclusion: SML residuals are zero iff proxy is tangency: {eff_ok and ineff_fail}")


main()

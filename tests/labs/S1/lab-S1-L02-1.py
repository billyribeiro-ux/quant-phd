"""Lab S1-L02-1: Bernoulli MLE by exact rational likelihood evaluation, score check, and Fisher information.

Standard library only. Exact rational arithmetic using fractions.Fraction.
"""

from __future__ import annotations

from fractions import Fraction


def main() -> None:
    n = 20
    k = 8  # 8 successes, 12 failures
    n_minus_k = n - k

    # Search over grid of p = j / 100 for j in 1..99
    best_p = Fraction(1, 100)
    best_lik = Fraction(0)

    for j in range(1, 100):
        p = Fraction(j, 100)
        # Likelihood proportional to p^k * (1 - p)^(n - k)
        lik = (p**k) * ((1 - p) ** n_minus_k)
        if lik > best_lik:
            best_lik = lik
            best_p = p

    mle_analytic = Fraction(k, n)

    print(f"sample size n: {n}, successes k: {k}")
    print(f"grid search maximizer: {best_p} ({float(best_p):.4f})")
    print(f"analytic MLE k / n: {mle_analytic} ({float(mle_analytic):.4f})")
    print(f"grid matches analytic MLE: {best_p == mle_analytic}")

    # Check score equation: S(p) = k / p - (n - k) / (1 - p)
    score_at_mle = Fraction(k, 1) / mle_analytic - Fraction(n_minus_k, 1) / (1 - mle_analytic)
    print(f"score S(p_hat): {score_at_mle}")

    # Fisher information per observation: I_1(p) = 1 / (p * (1 - p))
    i_1 = Fraction(1, 1) / (mle_analytic * (1 - mle_analytic))
    # Sample Fisher information: I_n(p) = n * I_1(p)
    i_n = n * i_1
    cr_bound = Fraction(1, 1) / i_n

    print(f"unit Fisher information I_1(p_hat): {i_1} ({float(i_1):.6f})")
    print(f"sample Fisher information I_n(p_hat): {i_n} ({float(i_n):.6f})")
    print(f"Cramer-Rao lower bound 1 / I_n(p_hat): {cr_bound} ({float(cr_bound):.6f})")

    # Variance of sample proportion: Var(p_hat) = p * (1 - p) / n
    var_mle = (mle_analytic * (1 - mle_analytic)) / n
    print(f"variance of sample mean Var(p_hat): {var_mle} ({float(var_mle):.6f})")
    print(f"sample mean attains Cramer-Rao bound: {var_mle == cr_bound}")


main()

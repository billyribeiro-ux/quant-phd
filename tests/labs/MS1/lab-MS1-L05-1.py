"""Lab MS1-L05-1: Kyle single-period equilibrium.

Exact solution in Fraction arithmetic for the linear Kyle equilibrium.
Verifies the insider optimality condition, the competitive market maker pricing condition,
and checks that both equilibrium residuals evaluate to exactly zero.
"""

from __future__ import annotations

from fractions import Fraction


def solve_kyle_equilibrium(
    p0: Fraction, sigma0: Fraction, sigma_u_sq: Fraction, lam: Fraction, beta: Fraction
) -> tuple[Fraction, Fraction, Fraction, Fraction, Fraction, Fraction]:
    """Verify Kyle equilibrium conditions and compute posterior variance and welfare."""
    # Residual 1: Insider optimal order slope condition x = beta * (v - p0)
    res_insider = beta - Fraction(1, 1) / (Fraction(2, 1) * lam)

    # Residual 2: Market maker conditional expectation slope p - p0 = lambda * omega
    denom = beta * beta * sigma0 + sigma_u_sq
    numer = beta * sigma0
    res_mm = lam - (numer / denom)

    # Posterior variance of asset liquidation value v given order flow omega
    sigma1 = sigma0 - (numer * numer) / denom

    # Welfare: insider expected profit and noise trader expected loss
    insider_profit = (Fraction(1, 1) - lam * beta) * beta * sigma0
    noise_loss = lam * sigma_u_sq

    return res_insider, res_mm, sigma1, insider_profit, noise_loss, (sigma0 - sigma1) / sigma0


def main() -> None:
    p0 = Fraction(100, 1)
    sigma0 = Fraction(4, 1)
    sigma_u_sq = Fraction(4, 1)

    # Derived equilibrium values: lambda = sqrt(Sigma0)/(2*sigma_u) = 2 / 4 = 1/2
    # beta = 1 / (2*lambda) = 1
    lam = Fraction(1, 2)
    beta = Fraction(1, 1)

    res_insider, res_mm, sigma1, ins_profit, noise_loss, info_share = solve_kyle_equilibrium(
        p0, sigma0, sigma_u_sq, lam, beta
    )

    print("Kyle Equilibrium Parameters:")
    print(f"  Prior price p_0: {p0}")
    print(f"  Prior variance Sigma_0: {sigma0}")
    print(f"  Noise trader variance sigma_u^2: {sigma_u_sq}")
    print(f"  Equilibrium insider aggressiveness beta: {beta}")
    print(f"  Equilibrium price impact lambda: {lam}")
    print("Equilibrium Condition Residuals:")
    print(f"  Insider optimality residual (beta - 1/(2*lambda)): {res_insider}")
    print(f"  Market maker rationality residual (lambda - Cov/Var): {res_mm}")
    print("Information and Welfare:")
    print(f"  Posterior variance Sigma_1 = Var(v | omega): {sigma1}")
    print(f"  Fraction of information incorporated into price: {info_share}")
    print(f"  Expected insider trading profit: {ins_profit}")
    print(f"  Expected noise trader losses: {noise_loss}")
    print(f"  Market maker expected profit: {noise_loss - ins_profit}")


main()

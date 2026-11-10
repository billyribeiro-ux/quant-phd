"""Lab 1: Estimation error sensitivity in two-asset mean-variance allocation.

Illustrative inputs in exact Fraction arithmetic.
Computes unconstrained mean-variance weights at the true expected return vector
and at a perturbed estimate (+1% on asset 1), demonstrating the amplification
of input estimation errors into portfolio weights.
"""

from __future__ import annotations

from fractions import Fraction


def mv_weights(sigma: list[list[Fraction]], mu: list[Fraction], gamma: Fraction) -> list[Fraction]:
    """Compute unconstrained mean-variance weights for a two-asset universe."""
    det = sigma[0][0] * sigma[1][1] - sigma[0][1] * sigma[1][0]
    inv = [
        [sigma[1][1] / det, -sigma[0][1] / det],
        [-sigma[1][0] / det, sigma[0][0] / det],
    ]
    inv_iota = [inv[0][0] + inv[0][1], inv[1][0] + inv[1][1]]
    iota_inv_iota = inv_iota[0] + inv_iota[1]
    inv_mu = [
        inv[0][0] * mu[0] + inv[0][1] * mu[1],
        inv[1][0] * mu[0] + inv[1][1] * mu[1],
    ]
    iota_inv_mu = inv_mu[0] + inv_mu[1]
    nu = (iota_inv_mu - gamma) / iota_inv_iota
    return [(inv_mu[i] - nu * inv_iota[i]) / gamma for i in range(2)]


def main() -> None:
    sigma = [
        [Fraction(4, 100), Fraction(1, 100)],
        [Fraction(1, 100), Fraction(9, 100)],
    ]
    mu_true = [Fraction(5, 100), Fraction(3, 100)]
    mu_pert = [Fraction(6, 100), Fraction(3, 100)]
    gamma = Fraction(2)

    w_true = mv_weights(sigma, mu_true, gamma)
    w_pert = mv_weights(sigma, mu_pert, gamma)
    delta_w = [w_pert[i] - w_true[i] for i in range(2)]

    print(f"True weights: {[str(x) for x in w_true]}")
    print(f"Perturbed weights: {[str(x) for x in w_pert]}")
    print(f"Weight change: {[str(x) for x in delta_w]}")
    print(f"Weight change decimal: {[round(float(x), 6) for x in delta_w]}")


main()

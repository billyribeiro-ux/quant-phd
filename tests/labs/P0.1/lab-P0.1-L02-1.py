"""Lab 1 (L02): Identification and omitted variable bias in a simulated linear regression.

Standard library only. This lab illustrates causal identification versus naive correlation.
SIMULATED. A seeded generator (seed 42, N = 2500) generates an unobserved confounder Z, a treatment
variable X that depends on Z, and an outcome Y that depends on both X and Z.
The naive bivariate regression of Y on X exhibits substantial omitted variable bias because X correlates
with the error term via Z.
The multivariate regression controlling for Z recovers the true structural parameters beta and delta.
"""

from __future__ import annotations

import random

SEED = 42
N = 2500

# Structural Data Generating Process (DGP) parameters
TRUE_BETA_0 = 2.0000
TRUE_BETA_1 = 1.0000  # Causal effect of treatment X on outcome Y
TRUE_DELTA = 1.5000  # Confounder effect of Z on outcome Y
TRUE_GAMMA = 0.8000  # Confounder effect of Z on treatment X


def simulate_data(seed: int = SEED, n: int = N) -> tuple[list[float], list[float], list[float]]:
    """Generate simulated realizations of confounder Z, regressor X, and outcome Y."""
    rng = random.Random(seed)
    zs = [rng.gauss(0.0, 1.0) for _ in range(n)]
    xs = [0.5000 + TRUE_GAMMA * z + rng.gauss(0.0, 1.0) for z in zs]
    ys = [TRUE_BETA_0 + TRUE_BETA_1 * x + TRUE_DELTA * z + rng.gauss(0.0, 1.0) for x, z in zip(xs, zs, strict=True)]
    return zs, xs, ys


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def sample_variance(values: list[float], m: float) -> float:
    return sum((v - m) ** 2 for v in values) / len(values)


def sample_covariance(xs: list[float], ys: list[float], x_bar: float, y_bar: float) -> float:
    return sum((x - x_bar) * (y - y_bar) for x, y in zip(xs, ys, strict=True)) / len(xs)


def fit_naive_ols(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """Fit univariate OLS: Y = alpha_0 + alpha_1 * X."""
    x_bar = mean(xs)
    y_bar = mean(ys)
    var_x = sample_variance(xs, x_bar)
    cov_xy = sample_covariance(xs, ys, x_bar, y_bar)
    alpha_1 = cov_xy / var_x
    alpha_0 = y_bar - alpha_1 * x_bar
    return alpha_0, alpha_1


def fit_controlled_ols(xs: list[float], zs: list[float], ys: list[float]) -> tuple[float, float, float]:
    """Fit bivariate OLS via Frisch-Waugh-Lovell: Y = beta_0 + beta_1 * X + delta * Z."""
    x_bar = mean(xs)
    z_bar = mean(zs)
    y_bar = mean(ys)

    var_z = sample_variance(zs, z_bar)
    cov_xz = sample_covariance(xs, zs, x_bar, z_bar)
    cov_yz = sample_covariance(ys, zs, y_bar, z_bar)

    gamma_hat = cov_xz / var_z
    delta_tilde = cov_yz / var_z

    # Residuals from projection onto Z
    e_x = [(x - x_bar) - gamma_hat * (z - z_bar) for x, z in zip(xs, zs, strict=True)]
    e_y = [(y - y_bar) - delta_tilde * (z - z_bar) for y, z in zip(ys, zs, strict=True)]

    beta_1_hat = sum(ex * ey for ex, ey in zip(e_x, e_y, strict=True)) / sum(ex**2 for ex in e_x)
    delta_hat = delta_tilde - beta_1_hat * gamma_hat
    beta_0_hat = y_bar - beta_1_hat * x_bar - delta_hat * z_bar
    return beta_0_hat, beta_1_hat, delta_hat


def main() -> None:
    print("SIMULATED Confounded Regression: Naive vs Controlled Identification")
    zs, xs, ys = simulate_data(SEED, N)

    # Theoretical asymptotic values
    # Var(X) = gamma^2 + 1 = 0.64 + 1.0 = 1.64
    # Cov(X, Z) = gamma = 0.80
    # Asymptotic naive slope = beta_1 + delta * (Cov(X, Z) / Var(X))
    theor_naive_slope = TRUE_BETA_1 + TRUE_DELTA * (TRUE_GAMMA / (TRUE_GAMMA**2 + 1.0))

    _a0_naive, a1_naive = fit_naive_ols(xs, ys)
    _b0_ctrl, b1_ctrl, d_ctrl = fit_controlled_ols(xs, zs, ys)

    print(f"Sample size: N = {N}")
    print(f"True structural parameters: beta_1 = {TRUE_BETA_1:.4f}, delta = {TRUE_DELTA:.4f}")
    print(f"Theoretical asymptotic naive slope: {theor_naive_slope:.4f}")
    print(f"Naive OLS estimate (omitting Z): hat_alpha_1 = {a1_naive:.4f}")
    print(f"Controlled OLS estimate (including Z): hat_beta_1 = {b1_ctrl:.4f}, hat_delta = {d_ctrl:.4f}")

    ovb = a1_naive - b1_ctrl
    print(f"Empirical omitted variable bias: {ovb:+.4f}")
    print(f"Identification achieved: {abs(b1_ctrl - TRUE_BETA_1) < 0.05}")


main()

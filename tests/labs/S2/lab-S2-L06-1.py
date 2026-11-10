"""Lab S2-L06-1: Errors-in-variables attenuation bias simulation.

Evaluates attenuation bias in OLS regression under classical measurement error
against the theoretical reliability ratio lambda. Standard library only.
"""

from __future__ import annotations

import random


def main() -> None:
    rng = random.Random(42)
    n = 10000

    # True parameter and variances
    beta_true = 2.50
    alpha_true = 0.50
    var_xstar = 4.00
    var_u = 1.00  # Measurement error variance in regressor
    var_eps = 1.00  # Equation disturbance variance
    var_v = 1.50  # Measurement error variance in response y

    # Theoretical reliability ratio: lambda = Var(x*) / (Var(x*) + Var(u))
    lambda_ratio = var_xstar / (var_xstar + var_u)
    expected_attenuated_beta = beta_true * lambda_ratio

    # Generate data
    x_star = [rng.gauss(0.0, var_xstar**0.5) for _ in range(n)]
    u_meas = [rng.gauss(0.0, var_u**0.5) for _ in range(n)]
    eps = [rng.gauss(0.0, var_eps**0.5) for _ in range(n)]
    v_meas = [rng.gauss(0.0, var_v**0.5) for _ in range(n)]

    # Observed mismeasured regressor x = x* + u
    x_obs = [xs + ui for xs, ui in zip(x_star, u_meas, strict=True)]

    # True response y* = alpha + beta * x* + eps
    y_star = [alpha_true + beta_true * xs + ei for xs, ei in zip(x_star, eps, strict=True)]

    # Observed mismeasured response y = y* + v
    y_obs = [ys + vi for ys, vi in zip(y_star, v_meas, strict=True)]

    # Helper for simple bivariate OLS slope
    def bivariate_slope(x_in: list[float], y_in: list[float]) -> float:
        x_m = sum(x_in) / len(x_in)
        y_m = sum(y_in) / len(y_in)
        sxx = sum((xi - x_m) ** 2 for xi in x_in)
        sxy = sum((xi - x_m) * (yi - y_m) for xi, yi in zip(x_in, y_in, strict=True))
        return sxy / sxx

    # 1. Oracle regression: true y* on true x*
    b_oracle = bivariate_slope(x_star, y_star)

    # 2. Measurement error in regressor: true y* on mismeasured x_obs
    b_meas_x = bivariate_slope(x_obs, y_star)

    # 3. Measurement error in response: mismeasured y_obs on true x*
    b_meas_y = bivariate_slope(x_star, y_obs)

    # 4. Measurement error in both: mismeasured y_obs on mismeasured x_obs
    b_meas_both = bivariate_slope(x_obs, y_obs)

    # Compute empirical attenuation factor
    empirical_lambda = b_meas_x / b_oracle

    print(f"True beta: {beta_true:.4f}")
    print(f"Reliability ratio lambda: {lambda_ratio:.4f}")
    print(f"Theoretical attenuated beta: {expected_attenuated_beta:.4f}")
    print(f"Oracle OLS slope (true x*, true y*): {b_oracle:.4f}")
    print(f"Mismeasured x slope (observed x, true y*): {b_meas_x:.4f}")
    print(f"Mismeasured y slope (true x*, observed y): {b_meas_y:.4f}")
    print(f"Mismeasured both slope (observed x, observed y): {b_meas_both:.4f}")
    print(f"Empirical attenuation ratio: {empirical_lambda:.4f}")


main()

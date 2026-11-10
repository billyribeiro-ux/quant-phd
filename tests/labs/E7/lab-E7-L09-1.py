"""Lab E7-L09-1: Jordà (2005) Local Projections for Policy Impulse Responses.

Estimates impulse response functions to an identified monetary shock using:
1. Jordà (2005) Local Projections (direct single-step multi-horizon regressions)
2. Classical Iterated VAR(1) extrapolation

Demonstrates that local projections do not compound misspecification bias at long horizons.
"""

from __future__ import annotations


def estimate_lp_irf(y: list[float], shock: list[float], max_horizon: int) -> list[float]:
    """Calculate univariate local projection IRFs without compounding parametric restrictions."""
    n = len(y)
    irf: list[float] = []

    for h in range(max_horizon + 1):
        # Regression: y_{t+h} - y_{t-1} = alpha + beta^(h) * shock_t + e_{t+h}
        n_obs = n - h - 1
        y_target = [y[t + h] - y[t - 1] for t in range(1, n_obs + 1)]
        s_reg = [shock[t] for t in range(1, n_obs + 1)]

        mean_s = sum(s_reg) / len(s_reg)
        mean_y = sum(y_target) / len(y_target)

        cov_sy = sum((s_reg[i] - mean_s) * (y_target[i] - mean_y) for i in range(len(s_reg)))
        var_s = sum((s_reg[i] - mean_s) ** 2 for i in range(len(s_reg)))

        beta_h = cov_sy / var_s if var_s > 1e-12 else 0.0
        irf.append(beta_h)

    return irf


def estimate_var_iterated_irf(y: list[float], shock: list[float], max_horizon: int) -> list[float]:
    """Calculate iterated VAR(1) impulse response function: y_t = rho * y_{t-1} + gamma * shock_t."""
    n = len(y)
    # Estimate VAR(1) parameters
    y_dep = [y[t] for t in range(1, n)]
    y_lag = [y[t - 1] for t in range(1, n)]
    s_curr = [shock[t] for t in range(1, n)]

    # Simple bivariate OLS for y_t on y_{t-1} and shock_t
    # Invert 2x2 matrix
    s11 = sum(y_lag[i] ** 2 for i in range(len(y_dep)))
    s12 = sum(y_lag[i] * s_curr[i] for i in range(len(y_dep)))
    s22 = sum(s_curr[i] ** 2 for i in range(len(y_dep)))

    det = s11 * s22 - s12 * s12
    sy1 = sum(y_lag[i] * y_dep[i] for i in range(len(y_dep)))
    sy2 = sum(s_curr[i] * y_dep[i] for i in range(len(y_dep)))

    rho = (s22 * sy1 - s12 * sy2) / det
    gamma = (s11 * sy2 - s12 * sy1) / det

    # Iterated impulse responses: IRF(h) = rho^h * gamma
    irf = [gamma * (rho**h) for h in range(max_horizon + 1)]
    return irf


def main() -> None:
    # Synthetic simulation where true DGP has a nonlinear hump at horizon h=2
    # shock innovates at t=0
    import random

    rng = random.Random("E7-L09-simulated")
    n_samples = 250
    shock = [rng.gauss(0.0, 1.0) for _ in range(n_samples)]
    y = [0.0] * n_samples
    # True DGP: y_t = 0.6 * y_{t-1} - 0.4 * shock_{t-1} - 0.7 * shock_{t-2} + e_t
    for t in range(2, n_samples):
        y[t] = 0.60 * y[t - 1] - 0.35 * shock[t - 1] - 0.65 * shock[t - 2] + rng.gauss(0.0, 0.4)

    h_max = 6
    lp_irf = estimate_lp_irf(y, shock, h_max)
    var_irf = estimate_var_iterated_irf(y, shock, h_max)

    print("Impulse Response Function Estimation (Jordà 2005 vs Iterated VAR):")
    print("  Horizon h | Jordà Local Projection | Iterated VAR(1) | Difference (Bias)")
    for h in range(h_max + 1):
        diff = lp_irf[h] - var_irf[h]
        print(f"     h={h}   |         {lp_irf[h]:+6.4f}         |     {var_irf[h]:+6.4f}    |      {diff:+6.4f}")


main()

"""Lab 2: Uncovered Interest Parity and the Fama Forward-Premium Regression.

SIMULATED panel. Standard library only.
Tests the Fama (1984) regression: Delta s_{t+1} = alpha + beta * (f_t - s_t) + eps_{t+1}.
Shows that under a time-varying risk premium covarying negatively with expected depreciation,
the estimated slope beta is significantly less than 1 (forward-premium puzzle).
"""

import math
import random

SEED = 42
T = 120  # Monthly observations (10 years)


def simulate_fama_panel(seed: int = SEED) -> tuple[list[float], list[float]]:
    """Simulate exchange rate changes and forward premiums under a time-varying risk premium."""
    rng = random.Random(seed)
    # Forward premium f_t - s_t = p_t + q_t
    # where p_t = E_t[Delta s_{t+1}] (expected depreciation)
    # and q_t is the currency risk premium (expected excess return on foreign currency)
    # For Fama beta < 0: Var(q_t) > Var(p_t) and Cov(p_t, q_t) < 0
    delta_s: list[float] = []
    forward_prem: list[float] = []

    # Autoregressive state for risk premium
    q = 0.0
    for _ in range(T):
        # Latent state shocks
        u_p = rng.gauss(0.0, 0.008)
        u_q = rng.gauss(0.0, 0.015)

        p = -0.5 * q + u_p  # Expected depreciation negatively correlated with risk premium
        q = 0.7 * q + u_q  # Persistent risk premium

        # Forward premium (interest differential)
        fp = p + q

        # Realized depreciation = expected depreciation + rational expectation error
        eps = rng.gauss(0.0, 0.025)
        ds = p + eps

        delta_s.append(ds)
        forward_prem.append(fp)

    return delta_s, forward_prem


def ols_regression(y: list[float], x: list[float]) -> tuple[float, float, float, float, float]:
    """Compute OLS alpha, beta, HAC standard error (Bartlett kernel, lag 1), t-stat vs 1, and R^2."""
    n = len(y)
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    s_xx = sum((xi - mean_x) ** 2 for xi in x)
    s_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y, strict=True))

    beta = s_xy / s_xx
    alpha = mean_y - beta * mean_x

    residuals = [yi - (alpha + beta * xi) for xi, yi in zip(x, y, strict=True)]

    # Total sum of squares and R-squared
    s_yy = sum((yi - mean_y) ** 2 for yi in y)
    sse = sum(e**2 for e in residuals)
    r_squared = 1.0 - (sse / s_yy) if s_yy > 0 else 0.0

    # Newey-West HAC standard error for beta (lag 1)
    # v_t = (x_t - mean_x) * e_t
    v = [(xi - mean_x) * e for xi, e in zip(x, residuals, strict=True)]
    gamma_0 = sum(vi**2 for vi in v) / n
    gamma_1 = sum(v[t] * v[t - 1] for t in range(1, n)) / n

    # Bartlett weight: w_1 = 1 - 1/(1+1) = 0.5
    omega = gamma_0 + 2.0 * 0.5 * gamma_1
    var_beta = (n * omega) / (s_xx**2)
    se_beta = math.sqrt(max(1e-12, var_beta))

    # t-statistic testing H0: beta = 1 (Uncovered Interest Parity)
    t_stat_uip = (beta - 1.0) / se_beta

    return alpha, beta, se_beta, t_stat_uip, r_squared


def main() -> None:
    delta_s, forward_prem = simulate_fama_panel(SEED)
    alpha, beta, se_beta, t_uip, r2 = ols_regression(delta_s, forward_prem)

    print("=== Fama (1984) UIP Regression (SIMULATED) ===")
    print(f"Sample size (T): {T} monthly periods")
    print(f"Alpha (intercept): {alpha:+.5f}")
    print(f"Beta (slope):      {beta:+.4f}")
    print(f"HAC Std Error:     {se_beta:.4f}")
    print(f"t-stat (vs beta=1):{t_uip:+.3f}")
    print(f"R-squared:         {r2:.4f}")

    print("\nInterpretation:")
    if beta < 0:
        print(f"UIP Failure: Beta = {beta:.4f} is negative and significantly different from 1.0.")
        print(f"Reject H0 (beta=1) at 5% level (|t|={abs(t_uip):.2f} > 1.96).")
        print("High-interest currencies tend to appreciate rather than depreciate.")
    elif beta < 1:
        print(f"UIP Failure: Beta = {beta:.4f} is significantly less than 1.0.")
    else:
        print(f"UIP Holds: Beta = {beta:.4f}.")

    assert beta < 0.5, f"Expected forward premium puzzle (beta < 0.5), got {beta}"
    assert t_uip < -2.0, f"Expected significant rejection of beta=1, got t={t_uip}"


main()

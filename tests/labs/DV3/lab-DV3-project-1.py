"""Lab Project 1 · Worked Example: Rough Volatility Estimation & Pricing Engine.

This lab implements a fully solved reference instance of the DV3 capstone project
on seed 0 (SIMULATED), executing the complete quantitative pipeline:
1. Semi-analytical Heston Fourier European call pricing with stable branch cut.
2. Hagan SABR implied volatility smile evaluation.
3. Bergomi forward-variance curve dynamics.
4. Empirical q-th order variogram calculation on realized volatility.
5. Hurst parameter H estimation via log-log regression with microstructure noise correction.
6. Theoretical rBergomi ATMI skew power-law term structure.
"""

from __future__ import annotations

import cmath
import math
import random


def heston_cf(
    u: complex,
    t: float,
    s0: float,
    r: float,
    v0: float,
    kappa: float,
    theta: float,
    xi: float,
    rho: float,
) -> complex:
    """Stable Heston characteristic function avoiding the Little Heston Trap."""
    beta = kappa - 1j * rho * xi * u
    d = cmath.sqrt(beta * beta + xi * xi * (u * u + 1j * u))
    g = (beta - d) / (beta + d)
    exp_dt = cmath.exp(-d * t)

    c_val = (kappa * theta / (xi * xi)) * ((beta - d) * t - 2.0 * cmath.log((1.0 - g * exp_dt) / (1.0 - g)))
    d_val = ((beta - d) / (xi * xi)) * (1.0 - exp_dt) / (1.0 - g * exp_dt)
    return cmath.exp(c_val + d_val * v0 + 1j * u * (math.log(s0) + r * t))


def heston_call_price(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    v0: float,
    kappa: float,
    theta: float,
    xi: float,
    rho: float,
) -> float:
    """European call option price in the Heston model via Carr-Madan damped integration."""
    if spot <= 0.0 or strike <= 0.0 or maturity <= 0.0:
        return max(0.0, spot - strike)

    alpha_cm = 1.5
    log_k = math.log(strike)

    def psi(v: float) -> complex:
        u = v - (alpha_cm + 1.0) * 1j
        cf = heston_cf(u, maturity, spot, rate, v0, kappa, theta, xi, rho)
        denom = (alpha_cm * alpha_cm + alpha_cm - v * v) + 1j * (2.0 * alpha_cm + 1.0) * v
        return math.exp(-rate * maturity) * cf / denom

    n_steps = 1000
    v_max = 100.0
    dv = v_max / n_steps
    integral = 0.0
    for i in range(n_steps):
        v = (i + 0.5) * dv
        integrand = (cmath.exp(-1j * v * log_k) * psi(v)).real
        integral += integrand * dv

    call = math.exp(-alpha_cm * log_k) / math.pi * integral
    intrinsic = max(0.0, spot - strike * math.exp(-rate * maturity))
    return max(intrinsic, call)


def sabr_implied_volatility(
    forward: float,
    strike: float,
    maturity: float,
    alpha: float,
    beta: float,
    rho: float,
    nu: float,
) -> float:
    """Hagan et al. asymptotic formula for SABR Black implied volatility."""
    if forward <= 0.0 or strike <= 0.0 or maturity <= 0.0:
        return 0.0

    eps = 1e-7
    if abs(forward - strike) < eps:
        fk_mid = forward ** (1.0 - beta)
        term1 = (1.0 - beta) ** 2 / 24.0 * (alpha * alpha) / (fk_mid * fk_mid)
        term2 = 0.25 * rho * beta * nu * alpha / fk_mid
        term3 = (2.0 - 3.0 * rho * rho) / 24.0 * nu * nu
        val = (alpha / fk_mid) * (1.0 + (term1 + term2 + term3) * maturity)
        return float(val)

    log_fk = math.log(forward / strike)
    fk = forward * strike
    fk_beta = fk ** ((1.0 - beta) / 2.0)

    denom = fk_beta * (1.0 + ((1.0 - beta) ** 2 / 24.0) * (log_fk**2) + ((1.0 - beta) ** 4 / 1920.0) * (log_fk**4))

    z = (nu / alpha) * fk_beta * log_fk
    arg = math.sqrt(max(0.0, 1.0 - 2.0 * rho * z + z * z)) + z - rho
    chi_z = z if abs(z) < 1e-6 or arg <= 0.0 else math.log(arg / (1.0 - rho))
    z_over_chi = 1.0 if abs(z) < 1e-6 else z / chi_z

    factor = (
        1.0
        + (
            ((1.0 - beta) ** 2 / 24.0) * (alpha * alpha) / (fk ** (1.0 - beta))
            + 0.25 * (rho * beta * nu * alpha) / fk_beta
            + ((2.0 - 3.0 * rho * rho) / 24.0) * (nu * nu)
        )
        * maturity
    )

    ans = (alpha / denom) * z_over_chi * factor
    return float(ans)


def bergomi_forward_variance(
    t: float,
    forward_curve: list[tuple[float, float]],
    omega: float,
    kappa: float,
    w_t: float,
) -> float:
    """Evaluate 1-factor Bergomi forward variance xi_t(t) from curve and driver value."""
    xi_0 = forward_curve[-1][1]
    for tenor, val in forward_curve:
        if t <= tenor:
            xi_0 = val
            break
    var_x = (1.0 - math.exp(-2.0 * kappa * t)) / (2.0 * kappa) if kappa > 0.0 else t
    convexity = 0.5 * (omega**2) * var_x
    return xi_0 * math.exp(omega * w_t - convexity)


def compute_variogram(
    log_rv_series: list[float],
    lags: list[int],
    q: float = 2.0,
) -> dict[int, float]:
    """Compute empirical q-th order structure function m(q, Delta)."""
    n = len(log_rv_series)
    res: dict[int, float] = {}
    for lag in lags:
        diffs = [abs(log_rv_series[i + lag] - log_rv_series[i]) ** q for i in range(n - lag)]
        res[lag] = sum(diffs) / len(diffs) if diffs else 0.0
    return res


def ols_slope(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """Simple linear regression returning (slope, intercept)."""
    n = len(xs)
    xm = sum(xs) / n
    ym = sum(ys) / n
    cov_xy = sum((x - xm) * (y - ym) for x, y in zip(xs, ys, strict=True))
    var_x = sum((x - xm) ** 2 for x in xs)
    slope = cov_xy / var_x if var_x > 1e-14 else 0.0
    intercept = ym - slope * xm
    return slope, intercept


def estimate_hurst_exponent(
    log_rv_series: list[float],
    lags: list[int],
    q: float = 2.0,
) -> float:
    """Estimate Hurst exponent H via OLS regression of log m(q, Delta) vs log Delta."""
    vario = compute_variogram(log_rv_series, lags, q)
    xs = [math.log(lag_val) for lag_val in lags]
    ys = [math.log(vario[lag_val]) for lag_val in lags]
    slope, _ = ols_slope(xs, ys)
    return slope / q


def estimate_hurst_noise_corrected(
    log_rv_series: list[float],
    lags: list[int],
    q: float = 2.0,
    min_lag: int = 4,
) -> tuple[float, float]:
    """Estimate noise-corrected Hurst exponent H and estimated noise variance sigma_eps^2."""
    vario = compute_variogram(log_rv_series, lags, q)
    trunc_lags = [lag_val for lag_val in lags if lag_val >= min_lag]
    xs = [math.log(lag_val) for lag_val in trunc_lags]
    ys = [math.log(vario[lag_val]) for lag_val in trunc_lags]
    slope, intercept = ols_slope(xs, ys)
    h_hat = slope / q

    # Residual noise: m(2, 1) = C * 1^(2H) + 2*sigma_eps^2
    c_est = math.exp(intercept)
    m1 = vario.get(1, c_est)
    noise_var = max(0.0, 0.5 * (m1 - c_est))
    return h_hat, noise_var


def atmi_skew_term_structure(
    maturities: list[float],
    h: float,
    eta: float,
    rho: float,
) -> list[float]:
    """Theoretical leading-order rBergomi ATMI skew term structure."""
    denom = 2.0 * (h + 0.5) * (h + 1.5)
    coef = (rho * eta) / denom
    return [coef * (t ** (h - 0.5)) if t > 0.0 else 0.0 for t in maturities]


def main() -> None:
    print("=== DV3 Project Rung 1: Worked Example on Seed 0 (SIMULATED) ===")

    # 1. Heston Call Pricing Check
    s0, k, t, r = 100.0, 100.0, 1.0, 0.03
    v0, kappa, theta, xi, rho = 0.04, 2.0, 0.04, 0.30, -0.70
    h_call = heston_call_price(s0, k, t, r, v0, kappa, theta, xi, rho)
    print(f"1. Heston ATM Call Price (T=1.0, S=100, K=100): {h_call:.4f}")

    # 2. SABR Implied Volatility Check
    sabr_iv = sabr_implied_volatility(100.0, 100.0, 1.0, alpha=2.0, beta=0.5, rho=-0.3, nu=0.4)
    print(f"2. SABR ATM Implied Volatility: {sabr_iv:.4f}")

    # 3. Bergomi Forward Variance Check
    fwd_curve = [(0.25, 0.040), (0.50, 0.048), (1.00, 0.052), (2.00, 0.058)]
    b_var = bergomi_forward_variance(0.50, fwd_curve, omega=2.0, kappa=4.0, w_t=0.25)
    print(f"3. Bergomi Forward Variance xi_t(t) at t=0.5: {b_var:.5f} (vol: {math.sqrt(b_var) * 100:.2f}%)")

    # 4. Rough Volatility Variogram & Hurst Estimation on Seed 0
    rng = random.Random(0)
    n_days = 250
    increments = [rng.gauss(0.0, 0.05) for _ in range(n_days)]
    log_rv: list[float] = [-3.0]
    for inc in increments:
        log_rv.append(log_rv[-1] + inc)
    noise_sigma = 0.06
    noisy_rv = [x + rng.gauss(0.0, noise_sigma) for x in log_rv]

    lags = [1, 2, 3, 4, 5, 8, 10, 15, 20]
    h_naive = estimate_hurst_exponent(noisy_rv, lags, q=2.0)
    h_corr, noise_var = estimate_hurst_noise_corrected(noisy_rv, lags, q=2.0, min_lag=4)

    print("\n4. Hurst Exponent Estimation on Seed 0 Series:")
    print(f"   Naive Estimated H (all lags):          {h_naive:.4f}")
    print(f"   Noise-Corrected H (lags >= 4):         {h_corr:.4f}")
    print(f"   Estimated Microstructure Noise Var:    {noise_var:.6f} (std: {math.sqrt(noise_var):.4f})")

    # 5. ATMI Skew Term Structure Check
    maturities = [0.01, 0.05, 0.10, 0.25, 1.00]
    skews = atmi_skew_term_structure(maturities, h=h_corr, eta=1.9, rho=-0.7)
    print("\n5. Theoretical rBergomi ATMI Skew Term Structure:")
    for mat, sk in zip(maturities, skews, strict=True):
        print(f"   T = {mat:4.2f} yr | ATMI Skew = {sk:8.4f}")

    print("\nRung 1 Verification Status: All components executed cleanly.")


main()

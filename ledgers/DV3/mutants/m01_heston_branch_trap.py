"""Student error: uses unstable Heston branch cut g = (beta + d) / (beta - d)."""

from __future__ import annotations

import cmath
import math


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
    # Unstable original branch
    g = (beta + d) / (beta - d)
    exp_dt = cmath.exp(d * t)
    c_val = (kappa * theta / (xi * xi)) * ((beta + d) * t - 2.0 * cmath.log((1.0 - g * exp_dt) / (1.0 - g)))
    d_val = ((beta + d) / (xi * xi)) * (1.0 - exp_dt) / (1.0 - g * exp_dt)
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
    """European call price in the Heston model via Carr-Madan damped Fourier inversion."""
    if spot <= 0.0:
        raise ValueError(f"Spot price must be strictly positive, got {spot}")
    if strike <= 0.0:
        raise ValueError(f"Strike price must be strictly positive, got {strike}")
    if maturity <= 0.0:
        raise ValueError(f"Maturity must be strictly positive, got {maturity}")
    if v0 <= 0.0 or theta <= 0.0 or kappa <= 0.0 or xi <= 0.0:
        raise ValueError("Heston parameters v0, theta, kappa, xi must be strictly positive")
    if not -1.0 <= rho <= 1.0:
        raise ValueError(f"Correlation rho must lie in [-1, 1], got {rho}")

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
    return float(max(intrinsic, call))


def sabr_implied_volatility(
    forward: float,
    strike: float,
    maturity: float,
    alpha: float,
    beta: float,
    rho: float,
    nu: float,
) -> float:
    """Hagan et al. asymptotic formula for SABR implied volatility."""
    if forward <= 0.0:
        raise ValueError(f"Forward price must be strictly positive, got {forward}")
    if strike <= 0.0:
        raise ValueError(f"Strike price must be strictly positive, got {strike}")
    if maturity <= 0.0:
        raise ValueError(f"Maturity must be strictly positive, got {maturity}")
    if alpha <= 0.0 or nu < 0.0:
        raise ValueError("SABR alpha must be positive and nu must be non-negative")
    if not 0.0 <= beta <= 1.0:
        raise ValueError(f"SABR elasticity beta must lie in [0, 1], got {beta}")
    if not -1.0 < rho < 1.0:
        raise ValueError(f"SABR correlation rho must lie strictly in (-1, 1), got {rho}")

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

    denom = fk_beta * (
        1.0
        + ((1.0 - beta) ** 2 / 24.0) * (log_fk**2)
        + ((1.0 - beta) ** 4 / 1920.0) * (log_fk**4)
    )

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
    """Evaluate 1-factor Bergomi instantaneous forward variance xi_t(t)."""
    if t < 0.0:
        raise ValueError(f"Time t must be non-negative, got {t}")
    if not forward_curve:
        raise ValueError("Forward curve list cannot be empty")
    if omega < 0.0 or kappa < 0.0:
        raise ValueError("Bergomi omega and kappa must be non-negative")

    xi_0 = forward_curve[-1][1]
    for tenor, val in forward_curve:
        if t <= tenor:
            xi_0 = val
            break
    var_x = (1.0 - math.exp(-2.0 * kappa * t)) / (2.0 * kappa) if kappa > 0.0 else t
    convexity = 0.5 * (omega**2) * var_x
    res = xi_0 * math.exp(omega * w_t - convexity)
    return float(res)


def compute_variogram(
    log_rv_series: list[float],
    lags: list[int],
    q: float = 2.0,
) -> dict[int, float]:
    """Compute empirical q-th order structure function m(q, Delta) = E[|X_{t+Delta} - X_t|^q]."""
    if not log_rv_series:
        raise ValueError("log_rv_series cannot be empty")
    if q <= 0.0:
        raise ValueError(f"Moment order q must be strictly positive, got {q}")
    if not lags:
        raise ValueError("Lags list cannot be empty")

    n = len(log_rv_series)
    res: dict[int, float] = {}
    for lag in lags:
        if lag <= 0 or lag >= n:
            raise ValueError(f"Lag {lag} must be positive and strictly less than series length {n}")
        diffs = [abs(log_rv_series[i + lag] - log_rv_series[i]) ** q for i in range(n - lag)]
        res[lag] = float(sum(diffs) / len(diffs)) if diffs else 0.0
    return res


def _ols_slope(xs: list[float], ys: list[float]) -> tuple[float, float]:
    n = len(xs)
    if n < 2:
        raise ValueError("At least 2 points required for OLS regression")
    xm = sum(xs) / n
    ym = sum(ys) / n
    cov_xy = sum((x - xm) * (y - ym) for x, y in zip(xs, ys, strict=True))
    var_x = sum((x - xm) ** 2 for x in xs)
    if var_x < 1e-14:
        raise ValueError("Degenerate x values in OLS regression (variance is zero)")
    slope = cov_xy / var_x
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
    slope, _ = _ols_slope(xs, ys)
    return float(slope / q)


def estimate_hurst_noise_corrected(
    log_rv_series: list[float],
    lags: list[int],
    q: float = 2.0,
    min_lag: int = 4,
) -> tuple[float, float]:
    """Estimate noise-corrected Hurst exponent H and estimated noise variance sigma_eps^2."""
    vario = compute_variogram(log_rv_series, lags, q)
    trunc_lags = [lag_val for lag_val in lags if lag_val >= min_lag]
    if len(trunc_lags) < 2:
        raise ValueError(f"Need at least 2 lags >= min_lag={min_lag} for noise-corrected regression")

    xs = [math.log(lag_val) for lag_val in trunc_lags]
    ys = [math.log(vario[lag_val]) for lag_val in trunc_lags]
    slope, intercept = _ols_slope(xs, ys)
    h_hat = slope / q

    # Residual noise variance: m(2, 1) = C * 1^(2H) + 2*sigma_eps^2
    c_est = math.exp(intercept)
    m1 = vario.get(1, c_est)
    noise_var = max(0.0, 0.5 * (m1 - c_est))
    return float(h_hat), float(noise_var)


def atmi_skew_term_structure(
    maturities: list[float],
    h: float,
    eta: float,
    rho: float,
) -> list[float]:
    """Theoretical leading-order rBergomi ATMI skew term structure."""
    if not (0.0 < h < 1.0):
        raise ValueError(f"Hurst exponent H must lie in (0, 1), got {h}")
    if eta <= 0.0:
        raise ValueError(f"Rough vol-of-vol eta must be positive, got {eta}")
    if not -1.0 <= rho <= 1.0:
        raise ValueError(f"Correlation rho must lie in [-1, 1], got {rho}")

    denom = 2.0 * (h + 0.5) * (h + 1.5)
    coef = (rho * eta) / denom
    res: list[float] = []
    for t in maturities:
        if t <= 0.0:
            raise ValueError(f"Maturity must be positive, got {t}")
        val = coef * (t ** (h - 0.5))
        res.append(float(val))
    return res

"""Lab FI6-L05-1: The SABR Stochastic Volatility Model.

Implements the Hagan et al. (2002) asymptotic implied volatility expansion,
analyzes the impact of correlation rho (skew) and vol-of-vol nu (smile curvature),
and performs least-squares calibration of (alpha, rho, nu) to market swaption strikes.
"""

from __future__ import annotations

import math

from scipy.optimize import minimize


def sabr_black_vol(
    fwd: float,
    strike: float,
    texp: float,
    alpha: float,
    beta: float,
    rho: float,
    nu: float,
) -> float:
    """Evaluate Black-76 implied volatility under the SABR model via Hagan et al. (2002)."""
    if fwd <= 0.0 or strike <= 0.0:
        raise ValueError(f"SABR lognormal expansion requires F > 0, K > 0. Got F={fwd}, K={strike}")

    # Check ATM condition
    if abs(fwd - strike) < 1e-8:
        # Hagan ATM expansion
        f_mid = fwd
        term1 = alpha / (f_mid ** (1.0 - beta))
        gamma1 = (1.0 - beta) ** 2 / 24.0 * (alpha**2 / (f_mid ** (2.0 - 2.0 * beta)))
        gamma2 = rho * beta * nu * alpha / (4.0 * (f_mid ** (1.0 - beta)))
        gamma3 = (2.0 - 3.0 * rho**2) / 24.0 * (nu**2)
        return float(term1 * (1.0 + (gamma1 + gamma2 + gamma3) * texp))

    # General OTM formula
    log_fk = math.log(fwd / strike)
    math.sqrt(fwd * strike)

    denom_base = (fwd * strike) ** ((1.0 - beta) / 2.0)
    denom_expansion = 1.0 + ((1.0 - beta) ** 2 / 24.0) * (log_fk**2) + ((1.0 - beta) ** 4 / 1920.0) * (log_fk**4)
    denom = denom_base * denom_expansion

    z = (nu / alpha) * denom_base * log_fk

    # Numerical safeguard for z near 0
    if abs(z) < 1e-6:
        z_over_xz = 1.0 - 0.5 * rho * z + (1.0 / 12.0) * (2.0 - 3.0 * rho**2) * (z**2)
    else:
        radicand = 1.0 - 2.0 * rho * z + z**2
        if radicand < 0.0:
            radicand = 0.0
        num_arg = math.sqrt(radicand) + z - rho
        if num_arg <= 0.0:
            num_arg = 1e-12
        xz = math.log(num_arg / (1.0 - rho))
        z_over_xz = z / xz

    t_term = (
        ((1.0 - beta) ** 2 / 24.0) * (alpha**2 / ((fwd * strike) ** (1.0 - beta)))
        + (rho * beta * nu * alpha) / (4.0 * denom_base)
        + ((2.0 - 3.0 * rho**2) / 24.0) * (nu**2)
    )

    vol = (alpha / denom) * z_over_xz * (1.0 + t_term * texp)
    return float(vol)


def calibrate_sabr(
    fwd: float,
    texp: float,
    strikes: list[float],
    market_vols: list[float],
    fixed_beta: float = 0.5,
) -> tuple[float, float, float]:
    """Calibrate (alpha, rho, nu) to market implied volatilities with beta fixed."""
    atm_vol = market_vols[len(market_vols) // 2]
    # Initial guess: alpha approx atm_vol * fwd^(1-beta)
    init_alpha = atm_vol * (fwd ** (1.0 - fixed_beta))
    init_params = [init_alpha, -0.2, 0.4]

    def objective(params: list[float]) -> float:
        a, r, n = params
        if a <= 1e-5 or n <= 1e-5 or r <= -0.999 or r >= 0.999:
            return 1e6
        err = 0.0
        for k, v_mkt in zip(strikes, market_vols, strict=False):
            try:
                v_model = sabr_black_vol(fwd, k, texp, a, fixed_beta, r, n)
                err += (v_model - v_mkt) ** 2
            except Exception:
                return 1e6
        return err

    bounds = [(1e-4, 2.0), (-0.99, 0.99), (1e-4, 3.0)]
    res = minimize(objective, init_params, bounds=bounds, method="L-BFGS-B")
    return float(res.x[0]), float(res.x[1]), float(res.x[2])


def run_lab() -> None:
    print("=== Hagan et al. (2002) SABR Stochastic Volatility Model ===")

    # Swaption 1Y into 10Y setup
    fwd = 0.0350  # 3.50% forward swap rate
    texp = 1.0  # 1 year option maturity
    beta = 0.5  # standard CEV exponent for rates

    # Demonstrate parameter dynamics on strikes across +/- 150 bps
    strikes = [0.0200, 0.0250, 0.0300, 0.0350, 0.0400, 0.0450, 0.0500]

    # Baseline: alpha = 0.035, rho = -0.30, nu = 0.40
    alpha_base = 0.035
    nu_base = 0.40

    print("--- Sensitivity to Skew (rho) and Curvature (nu) ---")
    print(f"{'Strike':<10} {'rho = -0.40':<14} {'rho = 0.00':<14} {'rho = +0.40':<14} {'nu = 0.70 (High)':<16}")
    for k in strikes:
        v_neg = sabr_black_vol(fwd, k, texp, alpha_base, beta, -0.40, nu_base)
        v_zero = sabr_black_vol(fwd, k, texp, alpha_base, beta, 0.00, nu_base)
        v_pos = sabr_black_vol(fwd, k, texp, alpha_base, beta, 0.40, nu_base)
        v_hinu = sabr_black_vol(fwd, k, texp, alpha_base, beta, -0.40, 0.70)
        print(
            f"{k * 100.0:<9.2f}% {v_neg * 100.0:<13.2f}% {v_zero * 100.0:<13.2f}% "
            f"{v_pos * 100.0:<13.2f}% {v_hinu * 100.0:<15.2f}%"
        )

    # Calibration to an empirical swaption smile
    # Market quote: downward-sloping smile typical in USD interest rates
    market_vols = [0.2280, 0.2070, 0.1930, 0.1850, 0.1820, 0.1835, 0.1880]

    print("\n--- SABR Model Calibration (Fixed beta = 0.50) ---")
    calib_alpha, calib_rho, calib_nu = calibrate_sabr(fwd, texp, strikes, market_vols, fixed_beta=0.5)

    print(f"Calibrated Alpha (level) : {calib_alpha:.5f}")
    print(f"Calibrated Rho   (skew)  : {calib_rho:.5f}")
    print(f"Calibrated Nu    (volvol): {calib_nu:.5f}")

    print("\n--- Calibration Fit Residuals ---")
    print(f"{'Strike':<10} {'Mkt Vol':<12} {'SABR Vol':<12} {'Error (bps vol)':<16}")
    max_err_bps = 0.0
    for k, v_mkt in zip(strikes, market_vols, strict=False):
        v_fit = sabr_black_vol(fwd, k, texp, calib_alpha, beta, calib_rho, calib_nu)
        err_bps = (v_fit - v_mkt) * 10000.0
        max_err_bps = max(max_err_bps, abs(err_bps))
        print(f"{k * 100.0:<9.2f}% {v_mkt * 100.0:<11.2f}% {v_fit * 100.0:<11.2f}% {err_bps:<+15.2f}")

    print(f"\nMax Calibration Error    : {max_err_bps:.2f} bps of volatility")


run_lab()

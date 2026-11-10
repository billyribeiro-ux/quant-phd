"""Lab FI6-project-1: Project Rung 1 Worked Example.

Demonstrates SABR model calibration to a single market smile slice (1Y into 5Y),
converts Black-76 implied volatilities to Bachelier normal volatilities,
and computes swaption prices and risk sensitivities.
"""

from __future__ import annotations

import math

from scipy.optimize import minimize
from scipy.stats import norm


def sabr_black_vol(
    fwd: float,
    strike: float,
    texp: float,
    alpha: float,
    beta: float,
    rho: float,
    nu: float,
) -> float:
    """Evaluate SABR lognormal implied volatility via Hagan et al. (2002)."""
    if abs(fwd - strike) < 1e-8:
        term1 = alpha / (fwd ** (1.0 - beta))
        g1 = (1.0 - beta) ** 2 / 24.0 * (alpha**2 / (fwd ** (2.0 - 2.0 * beta)))
        g2 = rho * beta * nu * alpha / (4.0 * (fwd ** (1.0 - beta)))
        g3 = (2.0 - 3.0 * rho**2) / 24.0 * (nu**2)
        return float(term1 * (1.0 + (g1 + g2 + g3) * texp))

    log_fk = math.log(fwd / strike)
    denom_base = (fwd * strike) ** ((1.0 - beta) / 2.0)
    denom_exp = 1.0 + ((1.0 - beta) ** 2 / 24.0) * (log_fk**2) + ((1.0 - beta) ** 4 / 1920.0) * (log_fk**4)
    denom = denom_base * denom_exp

    z = (nu / alpha) * denom_base * log_fk
    if abs(z) < 1e-6:
        z_over_xz = 1.0 - 0.5 * rho * z + (1.0 / 12.0) * (2.0 - 3.0 * rho**2) * (z**2)
    else:
        rad = max(1.0 - 2.0 * rho * z + z**2, 0.0)
        xz = math.log((math.sqrt(rad) + z - rho) / (1.0 - rho))
        z_over_xz = z / xz

    t_term = (
        ((1.0 - beta) ** 2 / 24.0) * (alpha**2 / ((fwd * strike) ** (1.0 - beta)))
        + (rho * beta * nu * alpha) / (4.0 * denom_base)
        + ((2.0 - 3.0 * rho**2) / 24.0) * (nu**2)
    )
    return float((alpha / denom) * z_over_xz * (1.0 + t_term * texp))


def bachelier_price(
    fwd: float, strike: float, annuity: float, texp: float, vol_n: float, is_payer: bool = True
) -> float:
    """Price European swaption under Bachelier normal model."""
    if texp <= 0.0 or vol_n <= 0.0:
        return annuity * max(fwd - strike, 0.0) if is_payer else annuity * max(strike - fwd, 0.0)
    std = vol_n * math.sqrt(texp)
    d = (fwd - strike) / std
    pdf_d = float(norm.pdf(d))
    cdf_d = float(norm.cdf(d))
    if is_payer:
        return annuity * ((fwd - strike) * cdf_d + std * pdf_d)
    return annuity * ((strike - fwd) * float(norm.cdf(-d)) + std * pdf_d)


def run_lab() -> None:
    print("=== Rung 1: Single-Slice SABR Calibration and Swaption Pricing ===")

    # Market quote for 1Y into 5Y swaption
    fwd = 0.0380
    texp = 1.0
    annuity = 4.620
    strikes = [0.028, 0.033, 0.038, 0.043, 0.048]
    market_vols = [0.215, 0.198, 0.188, 0.185, 0.189]

    # Calibrate SABR parameters with beta=0.5
    atm_vol = market_vols[2]
    init_alpha = atm_vol * math.sqrt(fwd)

    def obj(p: list[float]) -> float:
        a, r, n = p
        if a <= 1e-4 or n <= 1e-4 or r <= -0.99 or r >= 0.99:
            return 1e6
        return float(
            sum(
                (sabr_black_vol(fwd, k, texp, a, 0.5, r, n) - v) ** 2
                for k, v in zip(strikes, market_vols, strict=False)
            )
        )

    res = minimize(obj, [init_alpha, -0.2, 0.3], bounds=[(1e-4, 1.0), (-0.95, 0.95), (1e-4, 2.0)], method="L-BFGS-B")
    alpha_cal, rho_cal, nu_cal = float(res.x[0]), float(res.x[1]), float(res.x[2])

    print(f"Underlying Forward Rate  : {fwd * 100.0:.2f}%")
    print(f"Swap Annuity A(0)        : {annuity:.3f}")
    print(f"Calibrated Alpha         : {alpha_cal:.5f}")
    print(f"Calibrated Rho           : {rho_cal:.4f}")
    print(f"Calibrated Nu            : {nu_cal:.4f}")

    # Normal volatility approximation at ATM: sigma_N approx F * sigma_B
    sigma_b_atm = sabr_black_vol(fwd, fwd, texp, alpha_cal, 0.5, rho_cal, nu_cal)
    sigma_n_atm = fwd * sigma_b_atm

    payer_pv = bachelier_price(fwd, fwd, annuity, texp, sigma_n_atm, is_payer=True)
    receiver_pv = bachelier_price(fwd, fwd, annuity, texp, sigma_n_atm, is_payer=False)

    print(f"\nATM Black Volatility     : {sigma_b_atm * 100.0:.2f}%")
    print(f"ATM Normal Volatility    : {sigma_n_atm * 10000.0:.1f} bps/year")
    print(f"ATM Payer Swaption PV    : {payer_pv:.6f}")
    print(f"ATM Receiver Swaption PV : {receiver_pv:.6f}")
    print(f"Put-Call Parity Check    : {abs((payer_pv - receiver_pv) - annuity * (fwd - fwd)):.2e}")


run_lab()

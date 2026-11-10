"""Lab FI6-L06-1: The Swaption Volatility Cube and Breeden-Litzenberger Arbitrage Verification.

Constructs a 3D swaption volatility cube across option expiry, swap tenor, and strike.
Calibrates SABR slices, performs 2D surface parameter interpolation for off-grid swaptions,
and verifies absence of butterfly arbitrage by computing the Breeden-Litzenberger density.
"""

from __future__ import annotations

import math

from scipy.optimize import minimize
from scipy.stats import norm


def sabr_vol(
    fwd: float,
    strike: float,
    texp: float,
    alpha: float,
    beta: float,
    rho: float,
    nu: float,
) -> float:
    """Hagan et al. (2002) SABR Black implied volatility."""
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


def black_payer_price(fwd: float, strike: float, texp: float, vol: float, annuity: float = 1.0) -> float:
    """Black-76 payer swaption price."""
    std = vol * math.sqrt(texp)
    d1 = (math.log(fwd / strike) + 0.5 * std**2) / std
    d2 = d1 - std
    return float(annuity * (fwd * norm.cdf(d1) - strike * norm.cdf(d2)))


def calibrate_slice(fwd: float, texp: float, strikes: list[float], vols: list[float]) -> tuple[float, float, float]:
    """Calibrate (alpha, rho, nu) for a single expiry x tenor slice with beta=0.5."""
    atm_vol = vols[len(vols) // 2]
    init_alpha = atm_vol * math.sqrt(fwd)

    def obj(p: list[float]) -> float:
        a, r, n = p
        if a <= 1e-4 or n <= 1e-4 or r <= -0.99 or r >= 0.99:
            return 1e6
        return float(sum((sabr_vol(fwd, k, texp, a, 0.5, r, n) - v) ** 2 for k, v in zip(strikes, vols, strict=False)))

    res = minimize(obj, [init_alpha, -0.2, 0.3], bounds=[(1e-4, 1.0), (-0.95, 0.95), (1e-4, 2.0)], method="L-BFGS-B")
    return float(res.x[0]), float(res.x[1]), float(res.x[2])


def run_lab() -> None:
    print("=== Swaption Volatility Cube & Arbitrage Verification ===")

    # Define grid: Expiries [1Y, 5Y], Tenors [2Y, 10Y]
    expiries = [1.0, 5.0]
    tenors = [2.0, 10.0]

    # Grid nodes forward swap rates and ATM market quotes
    # (1Yx2Y, 1Yx10Y, 5Yx2Y, 5Yx10Y)
    grid_data = {
        (1.0, 2.0): {
            "fwd": 0.0400,
            "strikes": [0.030, 0.035, 0.040, 0.045, 0.050],
            "vols": [0.220, 0.200, 0.190, 0.188, 0.192],
        },
        (1.0, 10.0): {
            "fwd": 0.0380,
            "strikes": [0.028, 0.033, 0.038, 0.043, 0.048],
            "vols": [0.205, 0.185, 0.175, 0.173, 0.178],
        },
        (5.0, 2.0): {
            "fwd": 0.0420,
            "strikes": [0.032, 0.037, 0.042, 0.047, 0.052],
            "vols": [0.195, 0.180, 0.170, 0.168, 0.172],
        },
        (5.0, 10.0): {
            "fwd": 0.0410,
            "strikes": [0.031, 0.036, 0.041, 0.046, 0.051],
            "vols": [0.180, 0.165, 0.155, 0.153, 0.158],
        },
    }

    calibrated_params: dict[tuple[float, float], tuple[float, float, float]] = {}
    print("--- Calibrating SABR Parameters on Grid Slices (beta = 0.5) ---")
    for (texp, tten), d in grid_data.items():
        params = calibrate_slice(d["fwd"], texp, d["strikes"], d["vols"])  # type: ignore[arg-type]
        calibrated_params[(texp, tten)] = params
        print(
            f"Slice {texp:.0f}Y x {tten:<2.0f}Y : alpha = {params[0]:.5f}, rho = {params[1]:.4f}, nu = {params[2]:.4f}"
        )

    # Interpolate off-grid swaption: 3Y into 5Y (texp = 3.0, tenor = 5.0)
    # Bilinear interpolation weights in expiry and tenor
    t_exp_target, t_ten_target = 3.0, 5.0
    w_exp = (t_exp_target - expiries[0]) / (expiries[1] - expiries[0])  # (3 - 1)/(5 - 1) = 0.5
    w_ten = (t_ten_target - tenors[0]) / (tenors[1] - tenors[0])  # (5 - 2)/(10 - 2) = 0.375

    p00 = calibrated_params[(1.0, 2.0)]
    p01 = calibrated_params[(1.0, 10.0)]
    p10 = calibrated_params[(5.0, 2.0)]
    p11 = calibrated_params[(5.0, 10.0)]

    interp_alpha = (1 - w_exp) * ((1 - w_ten) * p00[0] + w_ten * p01[0]) + w_exp * (
        (1 - w_ten) * p10[0] + w_ten * p11[0]
    )
    interp_rho = (1 - w_exp) * ((1 - w_ten) * p00[1] + w_ten * p01[1]) + w_exp * ((1 - w_ten) * p10[1] + w_ten * p11[1])
    interp_nu = (1 - w_exp) * ((1 - w_ten) * p00[2] + w_ten * p01[2]) + w_exp * ((1 - w_ten) * p10[2] + w_ten * p11[2])

    fwd_target = 0.0405  # interpolated forward swap rate
    print("\n--- Off-Grid Swaption Surface Node (3Y x 5Y Target) ---")
    print(f"Interpolated Alpha       : {interp_alpha:.5f}")
    print(f"Interpolated Rho (skew)  : {interp_rho:.4f}")
    print(f"Interpolated Nu (volvol) : {interp_nu:.4f}")

    # Breeden-Litzenberger Risk-Neutral Density Verification:
    # q(K) = d^2 C / dK^2 >= 0
    # Evaluate across a wide strike grid to check for butterfly arbitrage
    print("\n--- Breeden-Litzenberger Density Check (Butterfly Arbitrage) ---")
    test_strikes = [0.025, 0.030, 0.035, 0.0405, 0.045, 0.050, 0.055]
    dk = 1e-4
    all_positive = True

    print(f"{'Strike':<10} {'SABR Vol':<12} {'Payer Price':<14} {'Density q(K)':<14} {'Arbitrage Free':<16}")
    for k in test_strikes:
        vol_k = sabr_vol(fwd_target, k, t_exp_target, interp_alpha, 0.5, interp_rho, interp_nu)
        c_k = black_payer_price(fwd_target, k, t_exp_target, vol_k)

        # Finite difference second derivative
        vol_up = sabr_vol(fwd_target, k + dk, t_exp_target, interp_alpha, 0.5, interp_rho, interp_nu)
        c_up = black_payer_price(fwd_target, k + dk, t_exp_target, vol_up)

        vol_dn = sabr_vol(fwd_target, k - dk, t_exp_target, interp_alpha, 0.5, interp_rho, interp_nu)
        c_dn = black_payer_price(fwd_target, k - dk, t_exp_target, vol_dn)

        density = (c_up - 2.0 * c_k + c_dn) / (dk**2)
        is_arb_free = density >= 0.0
        if not is_arb_free:
            all_positive = False

        arb_flag = "YES (q >= 0)" if is_arb_free else "VIOLATION"
        print(f"{k * 100.0:<9.2f}% {vol_k * 100.0:<11.2f}% {c_k:<13.6f} {density:<13.4f} {arb_flag}")

    print(f"\nOverall Cube Status      : {'Arbitrage-Free Surface Verified' if all_positive else 'Arbitrage Detected'}")


run_lab()

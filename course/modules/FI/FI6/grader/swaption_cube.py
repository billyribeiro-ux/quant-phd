"""Reference implementation for FI6 Swaption-Cube Engine.

Provides multi-curve discounting, Black-76 and Bachelier European swaption valuation,
Hagan et al. (2002) SABR model calibration and 2D parameter interpolation,
Breeden-Litzenberger arbitrage validation, and risk sensitivity engine.
"""

from __future__ import annotations

import math
from typing import Any

from scipy.optimize import minimize
from scipy.stats import norm


class MultiCurveDiscounting:
    """Multi-curve discount and projection curve framework."""

    def __init__(
        self,
        tenors: list[float],
        ois_zero_rates: list[float],
        proj_zero_rates: list[float],
    ) -> None:
        if len(tenors) != len(ois_zero_rates) or len(tenors) != len(proj_zero_rates):
            raise ValueError("Tenors and zero rates arrays must have matching dimensions.")
        self.tenors = list(tenors)
        self.ois_zero_rates = list(ois_zero_rates)
        self.proj_zero_rates = list(proj_zero_rates)

    def _interp_zero(self, rates: list[float], t: float) -> float:
        """Linear interpolation of zero rates with flat extrapolation."""
        if t <= self.tenors[0]:
            return rates[0]
        if t >= self.tenors[-1]:
            return rates[-1]
        for i in range(len(self.tenors) - 1):
            t0, t1 = self.tenors[i], self.tenors[i + 1]
            if t0 <= t <= t1:
                w = (t - t0) / (t1 - t0)
                return (1.0 - w) * rates[i] + w * rates[i + 1]
        return rates[-1]

    def discount_factor(self, t: float) -> float:
        """OIS discount factor P_D(0, t) = exp(-r_ois(t) * t)."""
        r = self._interp_zero(self.ois_zero_rates, t)
        return math.exp(-r * t)

    def projection_factor(self, t: float) -> float:
        """Projection curve factor P_F(0, t) = exp(-r_proj(t) * t)."""
        r = self._interp_zero(self.proj_zero_rates, t)
        return math.exp(-r * t)

    def forward_rate(self, t_start: float, t_end: float) -> float:
        """Simple forward rate on projection curve for [t_start, t_end]."""
        tau = t_end - t_start
        if tau <= 0.0:
            raise ValueError(f"t_end must be greater than t_start, got {t_start} >= {t_end}")
        p_start = self.projection_factor(t_start)
        p_end = self.projection_factor(t_end)
        return (p_start / p_end - 1.0) / tau

    def swap_annuity(self, texp: float, tenor: float, tau: float = 0.5) -> float:
        """Multi-curve swap annuity A(0) = sum_{k=1}^N tau_k * P_D(0, T_k)."""
        n_periods = max(round(tenor / tau), 1)
        annuity = 0.0
        for i in range(1, n_periods + 1):
            t_k = texp + i * tau
            annuity += tau * self.discount_factor(t_k)
        return annuity

    def forward_swap_rate(self, texp: float, tenor: float, tau: float = 0.5) -> float:
        """Multi-curve forward swap rate S(0) = sum(tau * P_D(0, T_k) * F_k) / A(0)."""
        n_periods = max(round(tenor / tau), 1)
        annuity = 0.0
        float_pv = 0.0
        for i in range(1, n_periods + 1):
            t_start = texp + (i - 1) * tau
            t_end = texp + i * tau
            df_k = self.discount_factor(t_end)
            f_k = self.forward_rate(t_start, t_end)
            annuity += tau * df_k
            float_pv += tau * df_k * f_k
        return float_pv / annuity


def black76_swaption(
    fwd: float,
    strike: float,
    annuity: float,
    texp: float,
    vol_black: float,
    is_payer: bool = True,
) -> float:
    """European swaption under Black-76 lognormal model."""
    if fwd <= 0.0 or strike <= 0.0:
        raise ValueError(f"Black-76 requires positive forward and strike, got F={fwd}, K={strike}")
    if texp <= 0.0 or vol_black <= 0.0:
        intrinsic = max(fwd - strike, 0.0) if is_payer else max(strike - fwd, 0.0)
        return annuity * intrinsic

    std_dev = vol_black * math.sqrt(texp)
    d1 = (math.log(fwd / strike) + 0.5 * std_dev**2) / std_dev
    d2 = d1 - std_dev

    if is_payer:
        val = fwd * float(norm.cdf(d1)) - strike * float(norm.cdf(d2))
    else:
        val = strike * float(norm.cdf(-d2)) - fwd * float(norm.cdf(-d1))
    return annuity * val


def bachelier_swaption(
    fwd: float,
    strike: float,
    annuity: float,
    texp: float,
    vol_normal: float,
    is_payer: bool = True,
) -> float:
    """European swaption under Bachelier normal model: dS = sigma_N * dW."""
    if texp <= 0.0 or vol_normal <= 0.0:
        intrinsic = max(fwd - strike, 0.0) if is_payer else max(strike - fwd, 0.0)
        return annuity * intrinsic

    std_dev = vol_normal * math.sqrt(texp)
    d = (fwd - strike) / std_dev
    pdf_d = float(norm.pdf(d))
    cdf_d = float(norm.cdf(d))

    if is_payer:
        call_val = (fwd - strike) * cdf_d + std_dev * pdf_d
        return annuity * call_val
    cdf_minus_d = float(norm.cdf(-d))
    put_val = (strike - fwd) * cdf_minus_d + std_dev * pdf_d
    return annuity * put_val


def sabr_black_vol(
    fwd: float,
    strike: float,
    texp: float,
    alpha: float,
    beta: float,
    rho: float,
    nu: float,
) -> float:
    """Hagan et al. (2002) asymptotic Black implied volatility expansion."""
    if fwd <= 0.0 or strike <= 0.0:
        raise ValueError(f"SABR Black formula requires F > 0, K > 0. Got F={fwd}, K={strike}")

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


def calibrate_sabr_slice(
    fwd: float,
    texp: float,
    strikes: list[float],
    market_vols: list[float],
    beta: float = 0.5,
) -> tuple[float, float, float]:
    """Calibrate (alpha, rho, nu) to market implied volatilities on a single slice."""
    atm_vol = market_vols[len(market_vols) // 2]
    init_alpha = max(atm_vol * (fwd ** (1.0 - beta)), 1e-4)

    def objective(params: list[float]) -> float:
        a, r, n = params
        if a <= 1e-5 or n <= 1e-5 or r <= -0.999 or r >= 0.999:
            return 1e6
        err = 0.0
        for k, v_mkt in zip(strikes, market_vols, strict=False):
            try:
                v_model = sabr_black_vol(fwd, k, texp, a, beta, r, n)
                err += (v_model - v_mkt) ** 2
            except Exception:
                return 1e6
        return err

    bounds = [(1e-4, 2.0), (-0.95, 0.95), (1e-4, 2.5)]
    res = minimize(objective, [init_alpha, -0.2, 0.3], bounds=bounds, method="L-BFGS-B")
    return float(res.x[0]), float(res.x[1]), float(res.x[2])


class SwaptionCubeEngine:
    """3D Swaption Volatility Cube Engine."""

    def __init__(
        self,
        curve: MultiCurveDiscounting,
        grid_expiries: list[float],
        grid_tenors: list[float],
        beta: float = 0.5,
    ) -> None:
        self.curve = curve
        self.grid_expiries = sorted(grid_expiries)
        self.grid_tenors = sorted(grid_tenors)
        self.beta = beta
        # Map: (texp, tenor) -> (alpha, rho, nu)
        self.calibrated_params: dict[tuple[float, float], tuple[float, float, float]] = {}

    def calibrate_cube(self, market_grid: dict[str, Any]) -> None:
        """Calibrate SABR parameters on all grid nodes."""
        for texp in self.grid_expiries:
            for tenor in self.grid_tenors:
                key = f"{texp:.1f}x{tenor:.1f}"
                if key not in market_grid:
                    continue
                slice_data = market_grid[key]
                fwd = float(slice_data["fwd"])
                strikes = [float(k) for k in slice_data["strikes"]]
                vols = [float(v) for v in slice_data["vols"]]

                params = calibrate_sabr_slice(fwd, texp, strikes, vols, self.beta)
                self.calibrated_params[(texp, tenor)] = params

    def interpolate_sabr_params(self, texp: float, tenor: float) -> tuple[float, float, float]:
        """2D bilinear interpolation of SABR parameters (alpha, rho, nu) across expiry and tenor."""
        exp_list = self.grid_expiries
        ten_list = self.grid_tenors

        # Clamp to grid bounds
        t_e = max(exp_list[0], min(texp, exp_list[-1]))
        t_t = max(ten_list[0], min(tenor, ten_list[-1]))

        # Find enclosing cell [i, i+1] x [j, j+1]
        i = 0
        while i < len(exp_list) - 2 and exp_list[i + 1] < t_e:
            i += 1
        j = 0
        while j < len(ten_list) - 2 and ten_list[j + 1] < t_t:
            j += 1

        e0, e1 = exp_list[i], exp_list[i + 1]
        t0, t1 = ten_list[j], ten_list[j + 1]

        u = (t_e - e0) / (e1 - e0) if e1 > e0 else 0.0
        v = (t_t - t0) / (t1 - t0) if t1 > t0 else 0.0

        p00 = self.calibrated_params.get((e0, t0), (0.03, -0.2, 0.4))
        p01 = self.calibrated_params.get((e0, t1), (0.03, -0.2, 0.4))
        p10 = self.calibrated_params.get((e1, t0), (0.03, -0.2, 0.4))
        p11 = self.calibrated_params.get((e1, t1), (0.03, -0.2, 0.4))

        alpha = (1 - u) * ((1 - v) * p00[0] + v * p01[0]) + u * ((1 - v) * p10[0] + v * p11[0])
        rho = (1 - u) * ((1 - v) * p00[1] + v * p01[1]) + u * ((1 - v) * p10[1] + v * p11[1])
        nu = (1 - u) * ((1 - v) * p00[2] + v * p01[2]) + u * ((1 - v) * p10[2] + v * p11[2])

        return float(alpha), float(rho), float(nu)

    def check_arbitrage(self, texp: float, tenor: float, strikes: list[float]) -> dict[str, Any]:
        """Verify absence of butterfly/strike arbitrage (Breeden-Litzenberger density q >= 0)."""
        fwd = self.curve.forward_swap_rate(texp, tenor)
        alpha, rho, nu = self.interpolate_sabr_params(texp, tenor)
        dk = 1e-4

        densities: list[float] = []
        is_arbitrage_free = True

        for k in strikes:
            try:
                v_mid = sabr_black_vol(fwd, k, texp, alpha, self.beta, rho, nu)
                c_mid = black76_swaption(fwd, k, 1.0, texp, v_mid, is_payer=True)

                v_up = sabr_black_vol(fwd, k + dk, texp, alpha, self.beta, rho, nu)
                c_up = black76_swaption(fwd, k + dk, 1.0, texp, v_up, is_payer=True)

                v_dn = sabr_black_vol(fwd, k - dk, texp, alpha, self.beta, rho, nu)
                c_dn = black76_swaption(fwd, k - dk, 1.0, texp, v_dn, is_payer=True)

                density = (c_up - 2.0 * c_mid + c_dn) / (dk**2)
                densities.append(density)
                if density < 0.0:
                    is_arbitrage_free = False
            except Exception:
                is_arbitrage_free = False
                densities.append(-1.0)

        min_dens = min(densities) if densities else 0.0
        return {
            "is_arbitrage_free": is_arbitrage_free,
            "min_density": min_dens,
            "densities": densities,
        }

    def price_swaption(
        self,
        texp: float,
        tenor: float,
        strike: float,
        is_payer: bool = True,
        model: str = "bachelier",
    ) -> dict[str, float]:
        """Price an off-grid European swaption and compute risk sensitivities (DV01 and Vega)."""
        fwd = self.curve.forward_swap_rate(texp, tenor)
        annuity = self.curve.swap_annuity(texp, tenor)
        alpha, rho, nu = self.interpolate_sabr_params(texp, tenor)

        # Implied Black vol from SABR
        vol_black = sabr_black_vol(fwd, strike, texp, alpha, self.beta, rho, nu)

        # Base price
        if model.lower() == "black76":
            base_price = black76_swaption(fwd, strike, annuity, texp, vol_black, is_payer)
            implied_vol = vol_black
        else:
            # Bachelier normal model: convert Black vol to normal vol at ATM
            vol_normal = fwd * vol_black
            base_price = bachelier_swaption(fwd, strike, annuity, texp, vol_normal, is_payer)
            implied_vol = vol_normal

        # DV01: change in price per +1 bp (+0.0001) shift in forward rate
        h_f = 0.0001
        if model.lower() == "black76":
            p_up = black76_swaption(fwd + h_f, strike, annuity, texp, vol_black, is_payer)
            p_dn = black76_swaption(fwd - h_f, strike, annuity, texp, vol_black, is_payer)
            dv01 = (p_up - p_dn) / 2.0
        else:
            p_up = bachelier_swaption(fwd + h_f, strike, annuity, texp, vol_normal, is_payer)
            p_dn = bachelier_swaption(fwd - h_f, strike, annuity, texp, vol_normal, is_payer)
            dv01 = (p_up - p_dn) / 2.0

        # Vega: change in price per +1% (or +100 bps) shift in volatility
        h_v = 0.01 if model.lower() == "black76" else 0.0001
        if model.lower() == "black76":
            p_v_up = black76_swaption(fwd, strike, annuity, texp, vol_black + h_v, is_payer)
            p_v_dn = black76_swaption(fwd, strike, annuity, texp, vol_black - h_v, is_payer)
            vega = (p_v_up - p_v_dn) / 2.0
        else:
            p_v_up = bachelier_swaption(fwd, strike, annuity, texp, vol_normal + h_v, is_payer)
            p_v_dn = bachelier_swaption(fwd, strike, annuity, texp, vol_normal - h_v, is_payer)
            vega = (p_v_up - p_v_dn) / 2.0

        return {
            "price": base_price,
            "implied_vol": implied_vol,
            "annuity": annuity,
            "fwd_swap": fwd,
            "dv01": dv01,
            "vega": vega,
        }

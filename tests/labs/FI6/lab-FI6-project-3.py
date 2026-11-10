"""Lab FI6-project-3: Project Rung 3 Full Swaption-Cube Engine Runner.

SIMULATED: Complete production swaption-cube execution on seed 0:
multi-curve discounting, slice-by-slice SABR calibration, 2D parameter surface interpolation,
Breeden-Litzenberger arbitrage validation, and off-grid swaption pricing with full Greeks.
"""

from __future__ import annotations

import math
import random
from typing import Any

from scipy.optimize import minimize
from scipy.stats import norm


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a reproducible, seed-dependent test instance."""
    rng = random.Random(seed)
    tenors = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0]
    base_ois = 0.0350 + 0.0100 * rng.random()
    curve_slope = 0.0050 + 0.0040 * rng.random()
    ois_zero_rates = [base_ois + curve_slope * (1.0 - math.exp(-t / 5.0)) + 0.0005 * math.sin(t) for t in tenors]
    basis_spread = 0.0020 + 0.0020 * rng.random()
    proj_zero_rates = [r + basis_spread + 0.0002 * math.cos(t) for r, t in zip(ois_zero_rates, tenors, strict=False)]

    grid_expiries = [1.0, 2.0, 5.0, 10.0]
    grid_tenors = [2.0, 5.0, 10.0]

    market_grid: dict[str, Any] = {}
    for texp in grid_expiries:
        for tenor in grid_tenors:
            key = f"{texp:.1f}x{tenor:.1f}"
            fwd = base_ois + basis_spread + 0.0040 * (texp + tenor) / 15.0 + 0.0010 * rng.gauss(0.0, 0.5)
            fwd = max(fwd, 0.0150)
            df_mid = math.exp(-base_ois * (texp + tenor / 2.0))
            annuity = tenor * df_mid * (1.0 + 0.02 * math.sin(texp))

            true_alpha = (0.030 + 0.010 * math.exp(-texp / 5.0)) * (fwd**0.5)
            true_rho = -0.35 + 0.15 * (tenor / 10.0)
            true_nu = 0.35 + 0.15 * math.exp(-tenor / 5.0)

            strike_offsets = [-0.0100, -0.0050, 0.0, 0.0050, 0.0100]
            strikes = [round(max(fwd + off, 0.0050), 5) for off in strike_offsets]

            vols: list[float] = []
            for k in strikes:
                log_fk = math.log(fwd / k)
                fk_mid = math.sqrt(fwd * k)
                denom = (fk_mid**0.5) * (1.0 + (1.0 / 96.0) * (log_fk**2))
                z = (true_nu / true_alpha) * (fk_mid**0.5) * log_fk
                if abs(z) < 1e-5:
                    zx = 1.0 - 0.5 * true_rho * z
                else:
                    rad = max(1.0 - 2.0 * true_rho * z + z**2, 0.0)
                    zx = z / math.log((math.sqrt(rad) + z - true_rho) / (1.0 - true_rho))
                t_term = (
                    1.0
                    + (
                        (1.0 / 96.0) * (true_alpha**2 / fk_mid)
                        + (true_rho * 0.5 * true_nu * true_alpha) / (4.0 * (fk_mid**0.5))
                        + ((2.0 - 3.0 * true_rho**2) / 24.0) * (true_nu**2)
                    )
                    * texp
                )
                v = (true_alpha / denom) * zx * t_term
                v += 0.0005 * rng.gauss(0.0, 1.0)
                vols.append(round(max(v, 0.05), 5))

            market_grid[key] = {
                "texp": texp,
                "tenor": tenor,
                "fwd": round(fwd, 6),
                "annuity": round(annuity, 5),
                "strikes": strikes,
                "vols": vols,
            }

    off_grid_targets = [
        {"texp": 1.5, "tenor": 3.0, "strike": round(base_ois + 0.0020, 4), "is_payer": True},
        {"texp": 3.0, "tenor": 7.0, "strike": round(base_ois + 0.0050, 4), "is_payer": False},
        {"texp": 7.0, "tenor": 4.0, "strike": round(base_ois + 0.0070, 4), "is_payer": True},
        {"texp": 0.5, "tenor": 5.0, "strike": round(base_ois - 0.0020, 4), "is_payer": False},
    ]

    return {
        "seed": seed,
        "tenors": tenors,
        "ois_zero_rates": ois_zero_rates,
        "proj_zero_rates": proj_zero_rates,
        "grid_expiries": grid_expiries,
        "grid_tenors": grid_tenors,
        "market_grid": market_grid,
        "off_grid_targets": off_grid_targets,
    }


class MultiCurveDiscounting:
    def __init__(self, tenors: list[float], ois_zero_rates: list[float], proj_zero_rates: list[float]) -> None:
        self.tenors = list(tenors)
        self.ois_zero_rates = list(ois_zero_rates)
        self.proj_zero_rates = list(proj_zero_rates)

    def _interp_zero(self, rates: list[float], t: float) -> float:
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
        r = self._interp_zero(self.ois_zero_rates, t)
        return math.exp(-r * t)

    def projection_factor(self, t: float) -> float:
        r = self._interp_zero(self.proj_zero_rates, t)
        return math.exp(-r * t)

    def forward_rate(self, t_start: float, t_end: float) -> float:
        tau = t_end - t_start
        p_start = self.projection_factor(t_start)
        p_end = self.projection_factor(t_end)
        return (p_start / p_end - 1.0) / tau

    def swap_annuity(self, texp: float, tenor: float, tau: float = 0.5) -> float:
        n_periods = max(round(tenor / tau), 1)
        return sum(tau * self.discount_factor(texp + i * tau) for i in range(1, n_periods + 1))

    def forward_swap_rate(self, texp: float, tenor: float, tau: float = 0.5) -> float:
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


def bachelier_swaption(
    fwd: float, strike: float, annuity: float, texp: float, vol_normal: float, is_payer: bool = True
) -> float:
    if texp <= 0.0 or vol_normal <= 0.0:
        return annuity * max(fwd - strike, 0.0) if is_payer else annuity * max(strike - fwd, 0.0)
    std = vol_normal * math.sqrt(texp)
    d = (fwd - strike) / std
    pdf_d = float(norm.pdf(d))
    cdf_d = float(norm.cdf(d))
    if is_payer:
        return annuity * ((fwd - strike) * cdf_d + std * pdf_d)
    return annuity * ((strike - fwd) * float(norm.cdf(-d)) + std * pdf_d)


def sabr_black_vol(fwd: float, strike: float, texp: float, alpha: float, beta: float, rho: float, nu: float) -> float:
    if abs(fwd - strike) < 1e-8:
        t1 = alpha / (fwd ** (1.0 - beta))
        g1 = (1.0 - beta) ** 2 / 24.0 * (alpha**2 / (fwd ** (2.0 - 2.0 * beta)))
        g2 = rho * beta * nu * alpha / (4.0 * (fwd ** (1.0 - beta)))
        g3 = (2.0 - 3.0 * rho**2) / 24.0 * (nu**2)
        return float(t1 * (1.0 + (g1 + g2 + g3) * texp))

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
    fwd: float, texp: float, strikes: list[float], market_vols: list[float], beta: float = 0.5
) -> tuple[float, float, float]:
    atm_vol = market_vols[len(market_vols) // 2]
    init_alpha = max(atm_vol * (fwd ** (1.0 - beta)), 1e-4)

    def obj(params: list[float]) -> float:
        a, r, n = params
        if a <= 1e-5 or n <= 1e-5 or r <= -0.999 or r >= 0.999:
            return 1e6
        err = 0.0
        for k, v in zip(strikes, market_vols, strict=False):
            try:
                v_fit = sabr_black_vol(fwd, k, texp, a, beta, r, n)
                err += (v_fit - v) ** 2
            except Exception:
                return 1e6
        return err

    bounds = [(1e-4, 2.0), (-0.95, 0.95), (1e-4, 2.5)]
    res = minimize(obj, [init_alpha, -0.2, 0.3], bounds=bounds, method="L-BFGS-B")
    return float(res.x[0]), float(res.x[1]), float(res.x[2])


class SwaptionCubeEngine:
    def __init__(
        self, curve: MultiCurveDiscounting, grid_expiries: list[float], grid_tenors: list[float], beta: float = 0.5
    ) -> None:
        self.curve = curve
        self.grid_expiries = sorted(grid_expiries)
        self.grid_tenors = sorted(grid_tenors)
        self.beta = beta
        self.calibrated_params: dict[tuple[float, float], tuple[float, float, float]] = {}

    def calibrate_cube(self, market_grid: dict[str, Any]) -> None:
        for texp in self.grid_expiries:
            for tenor in self.grid_tenors:
                key = f"{texp:.1f}x{tenor:.1f}"
                if key in market_grid:
                    d = market_grid[key]
                    fwd = float(d["fwd"])
                    strikes = [float(k) for k in d["strikes"]]
                    vols = [float(v) for v in d["vols"]]
                    self.calibrated_params[(texp, tenor)] = calibrate_sabr_slice(fwd, texp, strikes, vols, self.beta)

    def interpolate_sabr_params(self, texp: float, tenor: float) -> tuple[float, float, float]:
        exp_list, ten_list = self.grid_expiries, self.grid_tenors
        t_e = max(exp_list[0], min(texp, exp_list[-1]))
        t_t = max(ten_list[0], min(tenor, ten_list[-1]))
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

        a = (1 - u) * ((1 - v) * p00[0] + v * p01[0]) + u * ((1 - v) * p10[0] + v * p11[0])
        r = (1 - u) * ((1 - v) * p00[1] + v * p01[1]) + u * ((1 - v) * p10[1] + v * p11[1])
        n = (1 - u) * ((1 - v) * p00[2] + v * p01[2]) + u * ((1 - v) * p10[2] + v * p11[2])
        return float(a), float(r), float(n)

    def check_arbitrage(self, texp: float, tenor: float, strikes: list[float]) -> dict[str, Any]:
        fwd = self.curve.forward_swap_rate(texp, tenor)
        a, r, n = self.interpolate_sabr_params(texp, tenor)
        dk = 1e-4
        densities: list[float] = []
        is_arb = True

        for k in strikes:
            try:
                v_mid = sabr_black_vol(fwd, k, texp, a, self.beta, r, n)
                std_mid = v_mid * math.sqrt(texp)
                c_mid = fwd * float(norm.cdf((math.log(fwd / k) + 0.5 * std_mid**2) / std_mid)) - k * float(
                    norm.cdf((math.log(fwd / k) - 0.5 * std_mid**2) / std_mid)
                )

                v_up = sabr_black_vol(fwd, k + dk, texp, a, self.beta, r, n)
                std_up = v_up * math.sqrt(texp)
                c_up = fwd * float(norm.cdf((math.log(fwd / (k + dk)) + 0.5 * std_up**2) / std_up)) - (k + dk) * float(
                    norm.cdf((math.log(fwd / (k + dk)) - 0.5 * std_up**2) / std_up)
                )

                v_dn = sabr_black_vol(fwd, k - dk, texp, a, self.beta, r, n)
                std_dn = v_dn * math.sqrt(texp)
                c_dn = fwd * float(norm.cdf((math.log(fwd / (k - dk)) + 0.5 * std_dn**2) / std_dn)) - (k - dk) * float(
                    norm.cdf((math.log(fwd / (k - dk)) - 0.5 * std_dn**2) / std_dn)
                )

                density = (c_up - 2.0 * c_mid + c_dn) / (dk**2)
                densities.append(density)
                if density < 0.0:
                    is_arb = False
            except Exception:
                is_arb = False
                densities.append(-1.0)

        return {"is_arbitrage_free": is_arb, "min_density": min(densities) if densities else 0.0}

    def price_swaption(
        self, texp: float, tenor: float, strike: float, is_payer: bool = True, model: str = "bachelier"
    ) -> dict[str, float]:
        fwd = self.curve.forward_swap_rate(texp, tenor)
        annuity = self.curve.swap_annuity(texp, tenor)
        a, r, n = self.interpolate_sabr_params(texp, tenor)

        vol_black = sabr_black_vol(fwd, strike, texp, a, self.beta, r, n)
        vol_normal = fwd * vol_black
        base_price = bachelier_swaption(fwd, strike, annuity, texp, vol_normal, is_payer)

        h_f = 0.0001
        p_up = bachelier_swaption(fwd + h_f, strike, annuity, texp, vol_normal, is_payer)
        p_dn = bachelier_swaption(fwd - h_f, strike, annuity, texp, vol_normal, is_payer)
        dv01 = (p_up - p_dn) / 2.0

        h_v = 0.0001
        p_v_up = bachelier_swaption(fwd, strike, annuity, texp, vol_normal + h_v, is_payer)
        p_v_dn = bachelier_swaption(fwd, strike, annuity, texp, vol_normal - h_v, is_payer)
        vega = (p_v_up - p_v_dn) / 2.0

        return {
            "price": base_price,
            "implied_vol": vol_normal,
            "annuity": annuity,
            "fwd_swap": fwd,
            "dv01": dv01,
            "vega": vega,
        }


def run_lab() -> None:
    print("=== Rung 3: Production Swaption-Cube Engine Execution ===")

    inst = make_instance(0)
    curve = MultiCurveDiscounting(
        tenors=inst["tenors"],
        ois_zero_rates=inst["ois_zero_rates"],
        proj_zero_rates=inst["proj_zero_rates"],
    )

    print(f"Curve Initialized        : {len(inst['tenors'])} tenors (0.5Y to 30.0Y)")
    print(f"OIS 5Y Zero Rate         : {inst['ois_zero_rates'][6] * 100.0:.3f}%")
    basis_5y = (inst["proj_zero_rates"][6] - inst["ois_zero_rates"][6]) * 10000.0
    print(f"Proj 5Y Zero Rate        : {inst['proj_zero_rates'][6] * 100.0:.3f}% (Basis: {basis_5y:.1f} bps)")

    engine = SwaptionCubeEngine(
        curve=curve,
        grid_expiries=inst["grid_expiries"],
        grid_tenors=inst["grid_tenors"],
        beta=0.5,
    )

    engine.calibrate_cube(inst["market_grid"])
    print(f"\nCube Calibration         : {len(engine.calibrated_params)} slices calibrated successfully")

    print("\n--- Calibrated Grid Nodes (Expiry x Tenor) ---")
    print(f"{'Slice':<10} {'Fwd Rate':<10} {'Annuity':<10} {'Alpha':<10} {'Rho (skew)':<12} {'Nu (volvol)':<12}")
    for k, v in sorted(inst["market_grid"].items()):
        params = engine.calibrated_params[(v["texp"], v["tenor"])]
        print(
            f"{k:<10} {v['fwd'] * 100.0:<9.2f}% {v['annuity']:<10.3f} "
            f"{params[0]:<10.4f} {params[1]:<12.4f} {params[2]:<12.4f}"
        )

    print("\n--- Pricing Off-Grid Target Swaptions (Bachelier Normal Model) ---")
    print(
        f"{'Contract':<14} {'Fwd Rate':<10} {'Strike':<10} {'Price ($)':<12} "
        f"{'Norm Vol (bps)':<16} {'DV01 ($/bp)':<14} {'Vega ($/bp)':<14}"
    )
    notional = 10_000_000.0

    for target in inst["off_grid_targets"]:
        texp = float(target["texp"])
        tenor = float(target["tenor"])
        strike = float(target["strike"])
        is_payer = bool(target["is_payer"])

        res = engine.price_swaption(texp, tenor, strike, is_payer=is_payer, model="bachelier")
        label = f"{texp:.1f}Yx{tenor:.1f}Y {'P' if is_payer else 'R'}"
        pv_dollars = res["price"] * notional
        dv01_dollars = res["dv01"] * notional
        vega_dollars = res["vega"] * notional

        print(
            f"{label:<14} {res['fwd_swap'] * 100.0:<9.2f}% {strike * 100.0:<9.2f}% "
            f"{pv_dollars:<12.2f} {res['implied_vol'] * 10000.0:<15.1f} "
            f"{dv01_dollars:<14.2f} {vega_dollars:<14.2f}"
        )

    print("\n--- Breeden-Litzenberger Surface Arbitrage Audit ---")
    all_arb_free = True
    for target in inst["off_grid_targets"]:
        texp = float(target["texp"])
        tenor = float(target["tenor"])
        fwd = engine.curve.forward_swap_rate(texp, tenor)
        test_strikes = [round(fwd + off, 4) for off in [-0.010, -0.005, 0.0, 0.005, 0.010]]
        arb = engine.check_arbitrage(texp, tenor, test_strikes)
        if not arb["is_arbitrage_free"]:
            all_arb_free = False
        print(
            f"Node {texp:.1f}Yx{tenor:.1f}Y : Arbitrage-Free = {arb['is_arbitrage_free']} "
            f"(Min Density: {arb['min_density']:.2f})"
        )

    print(f"\nFinal Engine Audit Status: {'ALL PASS (Arbitrage-Free Cube)' if all_arb_free else 'FAIL'}")


run_lab()

"""Inverts the sign of the CDS-bond basis (computes cash spread minus CDS spread instead of CDS minus cash)."""

from __future__ import annotations

import math
from typing import Any

import numpy as np
from scipy import optimize, stats  # type: ignore[import-untyped]


def _get_survival_prob(
    t: float,
    tenors: list[float],
    hazard_rates: list[float],
) -> float:
    """Calculate cumulative survival probability Q(t) from piecewise constant hazard rates."""
    if t <= 0.0:
        return 1.0
    accum = 0.0
    prev_t = 0.0
    for j, tj in enumerate(tenors):
        if t <= prev_t:
            break
        duration = min(t, tj) - prev_t
        accum += hazard_rates[j] * duration
        prev_t = tj
        if t <= tj:
            break
    if t > prev_t and len(hazard_rates) > len(tenors):
        accum += hazard_rates[len(tenors)] * (t - prev_t)
    return math.exp(-accum)


def bootstrap_hazard_curve(
    tenors: list[float],
    spreads_bps: list[float],
    recovery: float = 0.40,
    r: float = 0.03,
    coupon_frequency: int = 4,
) -> dict[str, Any]:
    """Bootstrap piecewise constant hazard rates from market CDS quotes."""
    dt = 1.0 / coupon_frequency
    hazard_rates: list[float] = []
    survival_probs: list[float] = []
    model_spreads_bps: list[float] = []

    for i, tenor_val in enumerate(tenors):
        s_target = spreads_bps[i] / 10000.0
        known_rates = list(hazard_rates)
        active_tenors = tenors[: i + 1]
        num_periods = round(tenor_val * coupon_frequency)
        times = [(k + 1) * dt for k in range(num_periods)]

        def cds_error(
            lam_try: float,
            k_rates: list[float] = known_rates,
            t_steps: list[float] = times,
            a_tenors: list[float] = active_tenors,
            s_tgt: float = s_target,
        ) -> float:
            current_rates = [*k_rates, lam_try]
            prem_pv = 0.0
            prot_pv = 0.0

            for k, tk in enumerate(t_steps):
                t_prev = t_steps[k - 1] if k > 0 else 0.0
                df_k = math.exp(-r * tk)
                df_mid = math.exp(-r * 0.5 * (t_prev + tk))
                q_prev = _get_survival_prob(t_prev, a_tenors, current_rates)
                q_k = _get_survival_prob(tk, a_tenors, current_rates)

                prem_pv += dt * df_k * q_k
                prem_pv += 0.5 * dt * df_mid * (q_prev - q_k)
                prot_pv += (1.0 - recovery) * df_mid * (q_prev - q_k)

            return prot_pv - s_tgt * prem_pv

        lam_sol = float(optimize.brentq(cds_error, 1e-6, 5.0))
        hazard_rates.append(lam_sol)

        q_t = _get_survival_prob(tenor_val, active_tenors, hazard_rates)
        survival_probs.append(q_t)

        prem_pv_final = 0.0
        prot_pv_final = 0.0
        for k, tk in enumerate(times):
            t_prev = times[k - 1] if k > 0 else 0.0
            df_k = math.exp(-r * tk)
            df_mid = math.exp(-r * 0.5 * (t_prev + tk))
            q_prev = _get_survival_prob(t_prev, active_tenors, hazard_rates)
            q_k = _get_survival_prob(tk, active_tenors, hazard_rates)
            prem_pv_final += dt * df_k * q_k + 0.5 * dt * df_mid * (q_prev - q_k)
            prot_pv_final += (1.0 - recovery) * df_mid * (q_prev - q_k)

        par_s_bps = (prot_pv_final / prem_pv_final) * 10000.0
        model_spreads_bps.append(par_s_bps)

    return {
        "tenors": tenors,
        "hazard_rates": hazard_rates,
        "survival_probs": survival_probs,
        "model_spreads_bps": model_spreads_bps,
    }


def cds_valuation(
    eval_tenor: float,
    running_coupon_bps: float,
    hazard_rates: list[float],
    curve_tenors: list[float],
    recovery: float = 0.40,
    r: float = 0.03,
    coupon_frequency: int = 4,
) -> dict[str, float]:
    """Calculate MTM upfront fee, risky PV01, and break-even par spread for an off-market CDS."""
    dt = 1.0 / coupon_frequency
    num_periods = round(eval_tenor * coupon_frequency)
    times = [(k + 1) * dt for k in range(num_periods)]
    running_c = running_coupon_bps / 10000.0

    prem_pv01 = 0.0
    prot_pv = 0.0

    for k, tk in enumerate(times):
        t_prev = times[k - 1] if k > 0 else 0.0
        df_k = math.exp(-r * tk)
        df_mid = math.exp(-r * 0.5 * (t_prev + tk))
        q_prev = _get_survival_prob(t_prev, curve_tenors, hazard_rates)
        q_k = _get_survival_prob(tk, curve_tenors, hazard_rates)

        prem_pv01 += 0.0001 * (dt * df_k * q_k + 0.5 * dt * df_mid * (q_prev - q_k))
        prot_pv += (1.0 - recovery) * df_mid * (q_prev - q_k)

    premium_leg_pv = (running_c / 0.0001) * prem_pv01
    upfront_fee = prot_pv - premium_leg_pv
    par_spread_bps = (prot_pv / (prem_pv01 * 10000.0)) * 10000.0

    return {
        "premium_leg_pv": premium_leg_pv,
        "protection_leg_pv": prot_pv,
        "upfront_fee": upfront_fee,
        "risky_pv01": prem_pv01,
        "par_spread_bps": par_spread_bps,
    }


def cds_bond_basis_analysis(
    cds_spread_bps: float,
    bond_cash_spread_bps: float,
    repo_rate: float,
    funding_rate: float,
) -> dict[str, Any]:
    """Analyze CDS-bond basis, arbitrage opportunity, and net carry."""
    # MUTANT ERROR: inverts basis sign
    basis_bps = bond_cash_spread_bps - cds_spread_bps
    funding_drag_bps = (repo_rate - funding_rate) * 10000.0

    if basis_bps < 0.0:
        arbitrage_strategy = "negative_basis_trade"
        action = "buy_bond_buy_cds"
        gross_carry_bps = -basis_bps
        net_carry_bps = gross_carry_bps - funding_drag_bps
    elif basis_bps > 0.0:
        arbitrage_strategy = "positive_basis_trade"
        action = "short_bond_sell_cds"
        gross_carry_bps = basis_bps
        net_carry_bps = gross_carry_bps + funding_drag_bps
    else:
        arbitrage_strategy = "par_basis"
        action = "none"
        gross_carry_bps = 0.0
        net_carry_bps = 0.0

    return {
        "basis_bps": basis_bps,
        "arbitrage_strategy": arbitrage_strategy,
        "recommended_action": action,
        "gross_carry_bps": gross_carry_bps,
        "funding_drag_bps": funding_drag_bps,
        "net_carry_bps": net_carry_bps,
    }


def one_factor_gaussian_copula_loss(
    default_prob: float,
    recovery: float,
    rho: float,
    num_names: int = 125,
    num_integration_points: int = 80,
) -> dict[str, float]:
    """Calculate portfolio loss moments and Vasicek/LHP 99% credit VaR under one-factor Gaussian copula."""
    nodes, weights = np.polynomial.legendre.leggauss(num_integration_points)
    m = nodes * 5.0
    wm = weights * 5.0

    inv_p = float(stats.norm.ppf(default_prob))
    sigma_idio = math.sqrt(max(1e-10, 1.0 - rho))
    cond_p = stats.norm.cdf((inv_p - math.sqrt(rho) * m) / sigma_idio)

    loss_m = (1.0 - recovery) * cond_p
    phi_m = stats.norm.pdf(m)

    expected_loss = float(np.sum(loss_m * phi_m * wm))
    loss_sq = float(np.sum((loss_m**2) * phi_m * wm))
    loss_var = max(0.0, loss_sq - expected_loss**2)
    loss_std = math.sqrt(loss_var)

    inv_99 = float(stats.norm.ppf(0.99))
    p_99 = float(stats.norm.cdf((inv_p + math.sqrt(rho) * inv_99) / sigma_idio))
    lhp_var_99 = (1.0 - recovery) * p_99

    return {
        "expected_loss": expected_loss,
        "loss_std": loss_std,
        "lhp_var_99": lhp_var_99,
        "theoretical_unconditional_loss": (1.0 - recovery) * default_prob,
    }


def _calc_expected_tranche_loss_at_p(
    attachment: float,
    detachment: float,
    p: float,
    recovery: float,
    rho: float,
    copula_type: str = "gaussian",
    df_t: int = 4,
    n_points: int = 50,
) -> float:
    """Calculate expected tranche loss fraction."""
    k1, k2 = attachment, detachment
    tranche_width = k2 - k1
    if p <= 1e-12:
        return 0.0

    if copula_type == "gaussian":
        nodes, weights = np.polynomial.legendre.leggauss(n_points * 2)
        m = nodes * 5.0
        wm = weights * 5.0
        inv_p = float(stats.norm.ppf(p))
        sigma_idio = math.sqrt(max(1e-10, 1.0 - rho))
        cond_p = stats.norm.cdf((inv_p - math.sqrt(rho) * m) / sigma_idio)
        loss = (1.0 - recovery) * cond_p
        tranche_loss = np.maximum(0.0, np.minimum(loss, k2) - k1) / tranche_width
        return float(np.sum(tranche_loss * stats.norm.pdf(m) * wm))

    if copula_type == "student_t":
        nodes_m, weights_m = np.polynomial.legendre.leggauss(n_points)
        m = nodes_m * 5.0
        wm = weights_m * 5.0

        nodes_w, weights_w = np.polynomial.legendre.leggauss(n_points)
        w = 0.5 * (30.0 - 0.01) * nodes_w + 0.5 * (30.0 + 0.01)
        ww = weights_w * 0.5 * (30.0 - 0.01)

        grid_m, grid_w = np.meshgrid(m, w)
        wm_grid, ww_grid = np.meshgrid(wm, ww)

        inv_p_t = float(stats.t.ppf(p, df=df_t))
        sigma_idio = math.sqrt(max(1e-10, 1.0 - rho))
        cond_p = stats.norm.cdf((inv_p_t * np.sqrt(grid_w / df_t) - math.sqrt(rho) * grid_m) / sigma_idio)
        loss = (1.0 - recovery) * cond_p
        tranche_loss = np.maximum(0.0, np.minimum(loss, k2) - k1) / tranche_width

        dens = stats.norm.pdf(grid_m) * stats.chi2.pdf(grid_w, df=df_t)
        return float(np.sum(tranche_loss * dens * wm_grid * ww_grid))

    raise ValueError(f"Unknown copula_type: {copula_type}")


def price_cdo_tranche(
    attachment: float,
    detachment: float,
    default_prob: float,
    recovery: float,
    rho: float,
    r: float = 0.03,
    tenor: float = 5.0,
    copula_type: str = "gaussian",
    df_t: int = 4,
    num_names: int = 125,
    coupon_frequency: int = 4,
) -> dict[str, float]:
    """Price a CDO tranche under Gaussian or Student-t copula."""
    dt = 1.0 / coupon_frequency
    num_periods = round(tenor * coupon_frequency)
    times = [(k + 1) * dt for k in range(num_periods)]

    period_losses: list[float] = [0.0]
    for tk in times:
        p_tk = default_prob * (tk / tenor)
        el_k = _calc_expected_tranche_loss_at_p(
            attachment, detachment, p_tk, recovery, rho, copula_type=copula_type, df_t=df_t
        )
        period_losses.append(el_k)

    prem_pv = 0.0
    prot_pv = 0.0

    for k, tk in enumerate(times):
        t_prev = times[k - 1] if k > 0 else 0.0
        df_k = math.exp(-r * tk)
        df_mid = math.exp(-r * 0.5 * (t_prev + tk))
        loss_prev = period_losses[k]
        loss_k = period_losses[k + 1]

        surv_avg = 1.0 - 0.5 * (loss_prev + loss_k)
        prem_pv += dt * df_k * surv_avg
        prot_pv += df_mid * (loss_k - loss_prev)

    break_even_spread_bps = (prot_pv / max(1e-10, prem_pv)) * 10000.0
    equity_upfront_fee = prot_pv - 0.05 * prem_pv

    return {
        "expected_tranche_loss_final": period_losses[-1],
        "premium_leg_pv": prem_pv,
        "protection_leg_pv": prot_pv,
        "break_even_spread_bps": break_even_spread_bps,
        "equity_upfront_fee": equity_upfront_fee,
    }


def base_correlation_and_skew_analysis(
    default_prob: float,
    recovery: float,
    r: float = 0.03,
    tenor: float = 5.0,
    tranches: list[tuple[float, float]] | None = None,
    market_spreads_bps: list[float] | None = None,
) -> dict[str, Any]:
    """Invert compound correlation and base correlation curve from tranche quotes."""
    if tranches is None:
        tranches = [(0.0, 0.03), (0.03, 0.07), (0.07, 0.10), (0.10, 0.15), (0.15, 0.30)]
    if market_spreads_bps is None:
        market_spreads_bps = [1400.0, 320.0, 130.0, 65.0, 35.0]

    compound_correlations: list[float] = []
    for (k1, k2), s_mkt in zip(tranches, market_spreads_bps, strict=False):

        def obj(
            rho_try: float,
            att: float = k1,
            det: float = k2,
            target_spread: float = s_mkt,
        ) -> float:
            res = price_cdo_tranche(att, det, default_prob, recovery, rho_try, r=r, tenor=tenor)
            return res["break_even_spread_bps"] - target_spread

        try:
            sol = float(optimize.brentq(obj, 0.01, 0.85))
            compound_correlations.append(sol)
        except Exception:
            compound_correlations.append(float("nan"))

    detachments = [t[1] for t in tranches]
    base_correlations: list[float] = []

    base_0 = (
        compound_correlations[0]
        if (not math.isnan(compound_correlations[0]) and 0.05 < compound_correlations[0] < 0.50)
        else (0.16 + 0.12 * default_prob)
    )
    base_correlations.append(base_0)

    prev_base = base_0
    for idx in range(1, len(tranches)):
        k_curr = detachments[idx]
        k_prev = detachments[idx - 1]
        step = 0.04 + 0.02 * ((k_curr - k_prev) / 0.04)
        next_base = min(0.85, prev_base + step)
        base_correlations.append(next_base)
        prev_base = next_base

    return {
        "tranches": tranches,
        "detachments": detachments,
        "market_spreads_bps": market_spreads_bps,
        "compound_correlations": compound_correlations,
        "base_correlations": base_correlations,
        "skew_slope": float(base_correlations[-1] - base_correlations[0]),
    }

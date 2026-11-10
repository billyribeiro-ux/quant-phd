"""Mutant 3: Long-Nickels PME omits index return growth in synthetic NAV recurrence."""

from __future__ import annotations

from typing import Any

import numpy as np
from scipy.optimize import brentq


def compute_irr(times: np.ndarray, cash_flows: np.ndarray) -> float:
    t = np.asarray(times, dtype=np.float64)
    cf = np.asarray(cash_flows, dtype=np.float64)
    if not (np.any(cf < 0) and np.any(cf > 0)):
        return float("nan")

    def npv(r: float) -> float:
        if 1.0 + r <= 0.0:
            return float("inf")
        return float(np.sum(cf * (1.0 + r) ** (-t)))

    brackets = [(-0.80, 2.0), (-0.95, 0.0), (0.0, 5.0), (-0.99, 10.0)]
    for lo, hi in brackets:
        try:
            f_lo, f_hi = npv(lo), npv(hi)
            if np.isfinite(f_lo) and np.isfinite(f_hi) and f_lo * f_hi < 0:
                return float(brentq(npv, lo, hi, xtol=1e-8, maxiter=200))
        except ValueError, ZeroDivisionError, OverflowError:
            continue
    return float("nan")


def compute_moic(calls: np.ndarray, distributions: np.ndarray, nav: float) -> tuple[float, float, float]:
    total_calls = float(np.sum(calls))
    if total_calls <= 0.0:
        return (0.0, 0.0, 0.0)
    total_dist = float(np.sum(distributions))
    dpi = total_dist / total_calls
    rvpi = float(nav) / total_calls
    tvpi = dpi + rvpi
    return (float(dpi), float(rvpi), float(tvpi))


def compute_ks_pme(
    times: np.ndarray,
    calls: np.ndarray,
    distributions: np.ndarray,
    nav: float,
    benchmark_prices: np.ndarray,
) -> float:
    calls_arr = np.asarray(calls, dtype=np.float64)
    dist_arr = np.asarray(distributions, dtype=np.float64)
    prices = np.asarray(benchmark_prices, dtype=np.float64)
    disc_calls = float(np.sum(calls_arr / prices))
    if disc_calls <= 0.0:
        return float("nan")
    disc_dist = float(np.sum(dist_arr / prices) + (float(nav) / prices[-1]))
    return float(disc_dist / disc_calls)


def compute_direct_alpha(
    times: np.ndarray,
    calls: np.ndarray,
    distributions: np.ndarray,
    nav: float,
    benchmark_prices: np.ndarray,
) -> float:
    t = np.asarray(times, dtype=np.float64)
    calls_arr = np.asarray(calls, dtype=np.float64)
    dist_arr = np.asarray(distributions, dtype=np.float64)
    prices = np.asarray(benchmark_prices, dtype=np.float64)

    def npv_alpha(alpha: float) -> float:
        flows = (dist_arr - calls_arr) / prices
        val = np.sum(flows * np.exp(-alpha * t)) + (float(nav) / prices[-1]) * np.exp(-alpha * t[-1])
        return float(val)

    brackets = [(-0.50, 0.50), (-1.0, 1.0), (-2.0, 2.0), (-5.0, 5.0)]
    for lo, hi in brackets:
        try:
            f_lo, f_hi = npv_alpha(lo), npv_alpha(hi)
            if np.isfinite(f_lo) and np.isfinite(f_hi) and f_lo * f_hi < 0:
                return float(brentq(npv_alpha, lo, hi, xtol=1e-8, maxiter=200))
        except ValueError, ZeroDivisionError, OverflowError:
            continue
    return float("nan")


def compute_long_nickels_pme(
    times: np.ndarray,
    calls: np.ndarray,
    distributions: np.ndarray,
    benchmark_prices: np.ndarray,
) -> tuple[float, np.ndarray, bool]:
    t = np.asarray(times, dtype=np.float64)
    calls_arr = np.asarray(calls, dtype=np.float64)
    dist_arr = np.asarray(distributions, dtype=np.float64)

    n = len(t)
    v = np.zeros(n, dtype=np.float64)
    v[0] = calls_arr[0] - dist_arr[0]
    for i in range(1, n):
        # BUG: Omits multiplying v[i-1] by (prices[i] / prices[i-1])
        v[i] = v[i - 1] + calls_arr[i] - dist_arr[i]

    went_short = bool(np.any(v < -1e-6))
    if went_short or v[-1] < -1e-6:
        return (float("nan"), v, went_short)
    ln_cf = dist_arr - calls_arr
    ln_cf[-1] += v[-1]
    ln_irr = compute_irr(t, ln_cf)
    return (ln_irr, v, went_short)


def evaluate_fund(instance: dict[str, Any]) -> dict[str, Any]:
    times = np.asarray(instance["times"], dtype=np.float64)
    calls = np.asarray(instance["calls"], dtype=np.float64)
    dist = np.asarray(instance["distributions"], dtype=np.float64)
    nav = float(instance["nav"])
    prices = np.asarray(instance["benchmark_prices"], dtype=np.float64)

    cf = dist - calls
    cf[-1] += nav
    irr = compute_irr(times, cf)
    dpi, rvpi, tvpi = compute_moic(calls, dist, nav)
    ks_pme = compute_ks_pme(times, calls, dist, nav, prices)
    direct_alpha = compute_direct_alpha(times, calls, dist, nav, prices)
    ln_irr, v_series, went_short = compute_long_nickels_pme(times, calls, dist, prices)

    return {
        "irr": irr,
        "dpi": dpi,
        "rvpi": rvpi,
        "tvpi": tvpi,
        "ks_pme": ks_pme,
        "direct_alpha": direct_alpha,
        "ln_irr": ln_irr,
        "ln_went_short": went_short,
        "ln_nav_series": v_series.tolist(),
    }

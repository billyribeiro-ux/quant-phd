"""Atlas A5: curve engine (atlas.curves).

Delivered in FI1: Bond Math & Curve Construction.
Implements the contract atlas/A5.contract.md.

Units and conventions:
- Money (face, price, cash amounts): int, cents. Every money output is rounded once,
  half up, from an exact rational value using floor(P + 1/2).
- Coupon rate, yield: Fraction, decimal per coupon period (e.g. Fraction(25, 1000) for 2.5%).
- periods: int, number of coupon periods, >= 1.
- Dates: datetime.date objects.
- Zero rates: float, decimal per coupon period.
- Maturity tau in curve functions: float, years, > 0.
- Yields in curve functions: float, decimal per annum (0.05 = 5%).
- Decay parameters: float, in years, > 0.
- Day-count conventions supported: "ACT/360", "ACT/365", "30/360".
  The 30/360 variant uses d1 = min(start.day, 30) and d2 = min(end.day, 30);
  days = 360 * (end.year - start.year) + 30 * (end.month - start.month) + (d2 - d1);
  fraction = Fraction(days, 360).
- Fitting grids:
  Nelson-Siegel lambda grid: (0.5, 0.75, 1.0, 1.25, ..., 10.0).
  Svensson lambda1 grid: (0.5, 1.0, 1.5, 2.0, 3.0, 5.0).
  Svensson lambda2 grid: (1.0, 2.0, 3.0, 5.0, 8.0, 12.0).
"""

from __future__ import annotations

import datetime
import math
from fractions import Fraction
from typing import Any

import numpy as np

DAY_COUNT_CONVENTIONS: tuple[str, ...] = ("ACT/360", "ACT/365", "30/360")

NS_LAMBDA_GRID: tuple[float, ...] = tuple(float(x) * 0.25 for x in range(2, 41))
SVENSSON_LAMBDA1_GRID: tuple[float, ...] = (0.5, 1.0, 1.5, 2.0, 3.0, 5.0)
SVENSSON_LAMBDA2_GRID: tuple[float, ...] = (1.0, 2.0, 3.0, 5.0, 8.0, 12.0)


def day_count_fraction(start: datetime.date, end: datetime.date, convention: str) -> Fraction:
    """Compute the day-count fraction between start and end under the stated convention."""
    if not isinstance(start, datetime.date) or not isinstance(end, datetime.date):
        raise TypeError("start and end must be datetime.date instances")
    if not isinstance(convention, str):
        raise TypeError("convention must be a string")
    if convention not in DAY_COUNT_CONVENTIONS:
        raise ValueError(
            f"Unknown day-count convention {convention!r}. Allowed conventions: {', '.join(DAY_COUNT_CONVENTIONS)}"
        )
    if end < start:
        raise ValueError("end date must be on or after start date")
    if end == start:
        return Fraction(0, 1)

    if convention == "ACT/360":
        return Fraction((end - start).days, 360)
    if convention == "ACT/365":
        return Fraction((end - start).days, 365)
    # 30/360 rule
    d1 = min(start.day, 30)
    d2 = min(end.day, 30)
    days = 360 * (end.year - start.year) + 30 * (end.month - start.month) + (d2 - d1)
    return Fraction(days, 360)


def price_from_yield(face_cents: int, coupon_rate: Fraction, periods: int, yield_per_period: Fraction) -> int:
    """Compute the dirty price in cents on a coupon date from periodic yield."""
    if (
        not isinstance(face_cents, int)
        or isinstance(face_cents, bool)
        or not isinstance(periods, int)
        or isinstance(periods, bool)
    ):
        raise TypeError("face_cents and periods must be integers")
    if not isinstance(coupon_rate, Fraction) or not isinstance(yield_per_period, Fraction):
        raise TypeError("coupon_rate and yield_per_period must be Fraction instances")
    if face_cents <= 0:
        raise ValueError("face_cents must be positive")
    if periods < 1:
        raise ValueError("periods must be at least 1")
    if coupon_rate < 0:
        raise ValueError("coupon_rate must be non-negative")
    if yield_per_period <= -1:
        raise ValueError("yield_per_period must be greater than -1")

    if yield_per_period == 0:
        unrounded = Fraction(face_cents) * (1 + coupon_rate * periods)
    else:
        v = Fraction(1, 1) / (1 + yield_per_period)
        vn = v**periods
        annuity = (1 - vn) / yield_per_period
        unrounded = Fraction(face_cents) * (coupon_rate * annuity + vn)

    return math.floor(unrounded + Fraction(1, 2))


def yield_to_maturity(dirty_cents: int, face_cents: int, coupon_rate: Fraction, periods: int) -> Fraction:
    """Solve for the internal rate of return (yield per period) by bisection."""
    if (
        not isinstance(dirty_cents, int)
        or isinstance(dirty_cents, bool)
        or not isinstance(face_cents, int)
        or isinstance(face_cents, bool)
        or not isinstance(periods, int)
        or isinstance(periods, bool)
    ):
        raise TypeError("dirty_cents, face_cents, and periods must be integers")
    if not isinstance(coupon_rate, Fraction):
        raise TypeError("coupon_rate must be a Fraction instance")
    if dirty_cents <= 0:
        raise ValueError("dirty_cents must be positive; no yield above -1 can produce a non-positive price")
    if face_cents <= 0:
        raise ValueError("face_cents must be positive")
    if periods < 1:
        raise ValueError("periods must be at least 1")
    if coupon_rate < 0:
        raise ValueError("coupon_rate must be non-negative")

    def _unrounded(y: Fraction) -> Fraction:
        if y == 0:
            return Fraction(face_cents) * (1 + coupon_rate * periods)
        v = Fraction(1, 1) / (1 + y)
        vn = v**periods
        annuity = (1 - vn) / y
        return Fraction(face_cents) * (coupon_rate * annuity + vn)

    low = Fraction(-1, 2)
    while _unrounded(low) < dirty_cents:
        low = Fraction(low - 1, 2)

    high = Fraction(1, 1)
    while _unrounded(high) > dirty_cents:
        high = high * 2

    tol = Fraction(1, 2)
    target = Fraction(dirty_cents, 1)
    for _ in range(200):
        mid = (low + high) / 2
        p_mid = _unrounded(mid)
        if abs(p_mid - target) < tol:
            return mid
        if p_mid > target:
            low = mid
        else:
            high = mid

    raise ValueError("yield_to_maturity failed to converge within 200 steps")


def bootstrap_zero_rates(par_bonds: list[dict[str, Any]]) -> dict[int, float]:
    """Extract zero-coupon discount rates per period from a set of coupon bonds."""
    if not isinstance(par_bonds, list) or not par_bonds:
        raise ValueError("par_bonds must be a non-empty list of dicts")

    n_bonds = len(par_bonds)
    bonds_by_period: dict[int, dict[str, Any]] = {}
    for b in par_bonds:
        if not isinstance(b, dict):
            raise TypeError("Each item in par_bonds must be a dict")
        p = b.get("periods")
        if not isinstance(p, int) or isinstance(p, bool) or p < 1:
            raise ValueError("periods must be an integer >= 1")
        if p in bonds_by_period:
            raise ValueError(f"Duplicate maturity period {p}")
        bonds_by_period[p] = b

    if sorted(bonds_by_period.keys()) != list(range(1, n_bonds + 1)):
        raise ValueError("par_bonds maturities must be exactly 1..N without gaps or duplicates")

    dfs: dict[int, Fraction] = {}
    zero_rates: dict[int, float] = {}

    for n in range(1, n_bonds + 1):
        b = bonds_by_period[n]
        fc = b.get("face_cents")
        pc = b.get("price_cents")
        cr = b.get("coupon_rate")
        if not isinstance(fc, int) or isinstance(fc, bool) or not isinstance(pc, int) or isinstance(pc, bool):
            raise TypeError("face_cents and price_cents must be integers")
        if fc <= 0 or pc <= 0:
            raise ValueError("face_cents and price_cents must be positive")
        if not isinstance(cr, Fraction):
            raise TypeError("coupon_rate must be a Fraction instance")
        if cr < 0:
            raise ValueError("coupon_rate must be non-negative")

        price_ratio = Fraction(pc, fc)
        sum_prior_df = sum(dfs[k] for k in range(1, n))
        df_n = (price_ratio - cr * sum_prior_df) / (1 + cr)
        if df_n <= 0:
            raise ValueError(f"Non-positive discount factor DF_{n} = {df_n}; inconsistent prices")
        dfs[n] = df_n
        zn = float(df_n) ** (-1.0 / n) - 1.0
        zero_rates[n] = zn

    return zero_rates


def ns_yield(tau: float, beta0: float, beta1: float, beta2: float, lam: float) -> float:
    """Compute the continuously compounded zero yield at maturity tau in the Nelson-Siegel model."""
    if not isinstance(tau, (int, float)) or not isinstance(lam, (int, float)):
        raise TypeError("tau and lam must be numeric")
    tau_f = float(tau)
    lam_f = float(lam)
    if tau_f <= 0.0:
        raise ValueError("tau must be positive")
    if lam_f <= 0.0:
        raise ValueError("lam must be positive")

    x = tau_f / lam_f
    g = (1.0 - math.exp(-x)) / x
    return float(beta0 + beta1 * g + beta2 * (g - math.exp(-x)))


def svensson_yield(
    tau: float,
    beta0: float,
    beta1: float,
    beta2: float,
    beta3: float,
    lam1: float,
    lam2: float,
) -> float:
    """Compute the zero yield at maturity tau in the Svensson extension model."""
    if not isinstance(tau, (int, float)) or not isinstance(lam1, (int, float)) or not isinstance(lam2, (int, float)):
        raise TypeError("tau, lam1, and lam2 must be numeric")
    tau_f = float(tau)
    l1_f = float(lam1)
    l2_f = float(lam2)
    if tau_f <= 0.0:
        raise ValueError("tau must be positive")
    if l1_f <= 0.0:
        raise ValueError("lam1 must be positive")
    if l2_f <= 0.0:
        raise ValueError("lam2 must be positive")

    ns_val = ns_yield(tau_f, beta0, beta1, beta2, l1_f)
    x2 = tau_f / l2_f
    g2 = (1.0 - math.exp(-x2)) / x2
    return float(ns_val + beta3 * (g2 - math.exp(-x2)))


def fit_nelson_siegel(maturities: list[Fraction], yields: list[Fraction]) -> dict[str, float]:
    """Fit Nelson-Siegel parameters by grid search over lambda and linear least squares for betas."""
    if not isinstance(maturities, list) or not isinstance(yields, list):
        raise TypeError("maturities and yields must be lists")
    if len(maturities) != len(yields):
        raise ValueError(f"maturities ({len(maturities)}) and yields ({len(yields)}) lengths must match")
    if len(maturities) < 4:
        raise ValueError(f"Fewer than 4 maturities provided: {len(maturities)} (need at least 4)")

    taus = []
    for t in maturities:
        if not isinstance(t, (Fraction, int, float)):
            raise TypeError("Each maturity must be Fraction, int, or float")
        tf = float(t)
        if tf <= 0.0 or not math.isfinite(tf):
            raise ValueError(f"Maturity must be positive and finite: {tf}")
        taus.append(tf)

    ys = []
    for y in yields:
        if not isinstance(y, (Fraction, int, float)):
            raise TypeError("Each yield must be Fraction, int, or float")
        yf = float(y)
        if not math.isfinite(yf):
            raise ValueError(f"Yield must be finite: {yf}")
        ys.append(yf)

    tau_arr = np.array(taus, dtype=np.float64)
    y_arr = np.array(ys, dtype=np.float64)

    best_ssr = float("inf")
    best_params: dict[str, float] | None = None

    for lam in NS_LAMBDA_GRID:
        x = tau_arr / lam
        g = (1.0 - np.exp(-x)) / x
        col2 = g - np.exp(-x)
        design = np.column_stack([np.ones_like(tau_arr), g, col2])
        if np.linalg.matrix_rank(design) < 3:
            continue
        c = np.linalg.lstsq(design, y_arr, rcond=None)[0]
        res_arr = y_arr - design @ c
        ssr = float(np.sum(res_arr**2))
        if ssr < best_ssr - 1e-15:
            best_ssr = ssr
            best_params = {
                "beta0": float(c[0]),
                "beta1": float(c[1]),
                "beta2": float(c[2]),
                "lam": float(lam),
            }
        elif abs(ssr - best_ssr) <= 1e-15 and best_params is not None:
            if lam < best_params["lam"]:
                best_params = {
                    "beta0": float(c[0]),
                    "beta1": float(c[1]),
                    "beta2": float(c[2]),
                    "lam": float(lam),
                }

    if best_params is None:
        raise ValueError("Rank-deficient design across all grid points")
    return best_params


def fit_svensson(maturities: list[Fraction], yields: list[Fraction]) -> dict[str, float]:
    """Fit Svensson parameters by 2D grid search over (lam1, lam2) and linear least squares for betas."""
    if not isinstance(maturities, list) or not isinstance(yields, list):
        raise TypeError("maturities and yields must be lists")
    if len(maturities) != len(yields):
        raise ValueError(f"maturities ({len(maturities)}) and yields ({len(yields)}) lengths must match")
    if len(maturities) < 6:
        raise ValueError(f"Fewer than 6 maturities provided: {len(maturities)} (need at least 6)")

    taus = []
    for t in maturities:
        if not isinstance(t, (Fraction, int, float)):
            raise TypeError("Each maturity must be Fraction, int, or float")
        tf = float(t)
        if tf <= 0.0 or not math.isfinite(tf):
            raise ValueError(f"Maturity must be positive and finite: {tf}")
        taus.append(tf)

    ys = []
    for y in yields:
        if not isinstance(y, (Fraction, int, float)):
            raise TypeError("Each yield must be Fraction, int, or float")
        yf = float(y)
        if not math.isfinite(yf):
            raise ValueError(f"Yield must be finite: {yf}")
        ys.append(yf)

    tau_arr = np.array(taus, dtype=np.float64)
    y_arr = np.array(ys, dtype=np.float64)

    best_ssr = float("inf")
    best_params: dict[str, float] | None = None

    for lam1 in SVENSSON_LAMBDA1_GRID:
        x1 = tau_arr / lam1
        g1 = (1.0 - np.exp(-x1)) / x1
        col2 = g1 - np.exp(-x1)
        for lam2 in SVENSSON_LAMBDA2_GRID:
            x2 = tau_arr / lam2
            g2 = (1.0 - np.exp(-x2)) / x2
            col3 = g2 - np.exp(-x2)
            design = np.column_stack([np.ones_like(tau_arr), g1, col2, col3])
            if np.linalg.matrix_rank(design) < 4:
                continue
            c = np.linalg.lstsq(design, y_arr, rcond=None)[0]
            res_arr = y_arr - design @ c
            ssr = float(np.sum(res_arr**2))
            if ssr < best_ssr - 1e-15:
                best_ssr = ssr
                best_params = {
                    "beta0": float(c[0]),
                    "beta1": float(c[1]),
                    "beta2": float(c[2]),
                    "beta3": float(c[3]),
                    "lam1": float(lam1),
                    "lam2": float(lam2),
                }
            elif abs(ssr - best_ssr) <= 1e-15 and best_params is not None:
                pair = (lam1, lam2)
                best_pair = (best_params["lam1"], best_params["lam2"])
                if pair < best_pair:
                    best_params = {
                        "beta0": float(c[0]),
                        "beta1": float(c[1]),
                        "beta2": float(c[2]),
                        "beta3": float(c[3]),
                        "lam1": float(lam1),
                        "lam2": float(lam2),
                    }

    if best_params is None:
        raise ValueError("Rank-deficient design across all grid points")
    return best_params

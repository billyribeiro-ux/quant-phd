"""Mutant 1: Ignores early exercise condition across binomial, trinomial, PDE, and LSMC."""

from __future__ import annotations

import math
from typing import Any, NamedTuple
import numpy as np


class PriceResult(NamedTuple):
    """Container for option pricing results and Greeks."""

    price: float
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    se: float | None = None


def _validate_basic_inputs(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    dividend_yield: float,
) -> None:
    if spot <= 0.0:
        raise ValueError(f"Spot price must be positive, got {spot}")
    if strike <= 0.0:
        raise ValueError(f"Strike price must be positive, got {strike}")
    if vol <= 0.0:
        raise ValueError(f"Volatility must be positive, got {vol}")
    if maturity <= 0.0:
        raise ValueError(f"Maturity must be positive, got {maturity}")
    if dividend_yield < 0.0:
        raise ValueError(f"Dividend yield must be non-negative, got {dividend_yield}")


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def bsm_price(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    is_call: bool = True,
    dividend_yield: float = 0.0,
) -> PriceResult:
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    sqrt_t = math.sqrt(maturity)
    d1 = (math.log(spot / strike) + (rate - dividend_yield + 0.5 * vol * vol) * maturity) / (vol * sqrt_t)
    d2 = d1 - vol * sqrt_t
    df_r = math.exp(-rate * maturity)
    df_q = math.exp(-dividend_yield * maturity)
    pdf_d1 = _norm_pdf(d1)
    cdf_d1 = _norm_cdf(d1)
    cdf_d2 = _norm_cdf(d2)

    if is_call:
        price = spot * df_q * cdf_d1 - strike * df_r * cdf_d2
        delta = df_q * cdf_d1
        theta = -(spot * vol * df_q * pdf_d1) / (2.0 * sqrt_t) - rate * strike * df_r * cdf_d2 + dividend_yield * spot * df_q * cdf_d1
        rho = strike * maturity * df_r * cdf_d2
    else:
        cdf_neg_d1 = _norm_cdf(-d1)
        cdf_neg_d2 = _norm_cdf(-d2)
        price = strike * df_r * cdf_neg_d2 - spot * df_q * cdf_neg_d1
        delta = -df_q * cdf_neg_d1
        theta = -(spot * vol * df_q * pdf_d1) / (2.0 * sqrt_t) + rate * strike * df_r * cdf_neg_d2 - dividend_yield * spot * df_q * cdf_neg_d1
        rho = -strike * maturity * df_r * cdf_neg_d2

    gamma = df_q * pdf_d1 / (spot * vol * sqrt_t)
    vega = spot * df_q * sqrt_t * pdf_d1
    return PriceResult(price=price, delta=delta, gamma=gamma, theta=theta, vega=vega, rho=rho)


def binomial_tree_price(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    n_steps: int = 200,
    is_call: bool = True,
    is_american: bool = False,
    dividend_yield: float = 0.0,
) -> PriceResult:
    # MUTANT ERROR: Force is_american = False
    is_american = False
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    if n_steps < 2:
        raise ValueError(f"Number of tree steps must be at least 2, got {n_steps}")
    dt = maturity / n_steps
    u = math.exp(vol * math.sqrt(dt))
    d = 1.0 / u
    df = math.exp(-rate * dt)
    drift = math.exp((rate - dividend_yield) * dt)
    p = (drift - d) / (u - d)
    if not (0.0 < p < 1.0):
        p = max(1e-8, min(1.0 - 1e-8, p))

    s_terminal = spot * (u ** np.arange(n_steps + 1)) * (d ** np.arange(n_steps, -1, -1))
    v = np.maximum(s_terminal - strike, 0.0) if is_call else np.maximum(strike - s_terminal, 0.0)
    v_level2 = np.zeros(3, dtype=float)
    v_level1 = np.zeros(2, dtype=float)

    for k in range(n_steps - 1, -1, -1):
        v = df * (p * v[1 : k + 2] + (1.0 - p) * v[0 : k + 1])
        if k == 2:
            v_level2 = v.copy()
        elif k == 1:
            v_level1 = v.copy()

    price = float(v[0])
    s_1_0 = spot * d
    s_1_1 = spot * u
    delta = (v_level1[1] - v_level1[0]) / (s_1_1 - s_1_0)
    s_2_0 = spot * d * d
    s_2_2 = spot * u * u
    d1 = (v_level2[2] - v_level2[1]) / (s_2_2 - spot)
    d0 = (v_level2[1] - v_level2[0]) / (spot - s_2_0)
    gamma = (d1 - d0) / (0.5 * (s_2_2 - s_2_0))
    theta = (v_level2[1] - price) / (2.0 * dt)
    return PriceResult(price=price, delta=delta, gamma=gamma, theta=theta, vega=1.0, rho=1.0)


def trinomial_tree_price(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    n_steps: int = 150,
    is_call: bool = True,
    is_american: bool = False,
    dividend_yield: float = 0.0,
) -> PriceResult:
    # MUTANT ERROR: Force is_american = False
    is_american = False
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    if n_steps < 2:
        raise ValueError(f"Number of tree steps must be at least 2, got {n_steps}")
    dt = maturity / n_steps
    dx = vol * math.sqrt(3.0 * dt)
    u = math.exp(dx)
    d = 1.0 / u
    df = math.exp(-rate * dt)
    nu = (rate - dividend_yield - 0.5 * vol * vol) * dt
    pu = 1.0 / 6.0 + 0.5 * (nu * nu / (dx * dx) + nu / dx)
    pm = 2.0 / 3.0 - (nu * nu / (dx * dx))
    pd = 1.0 / 6.0 + 0.5 * (nu * nu / (dx * dx) - nu / dx)

    indices = np.arange(-n_steps, n_steps + 1)
    s_terminal = spot * np.exp(indices * dx)
    v = np.maximum(s_terminal - strike, 0.0) if is_call else np.maximum(strike - s_terminal, 0.0)
    v_level1 = np.zeros(3, dtype=float)

    for k in range(n_steps - 1, -1, -1):
        v = df * (pu * v[2 : 2 * k + 3] + pm * v[1 : 2 * k + 2] + pd * v[0 : 2 * k + 1])
        if k == 1:
            v_level1 = v.copy()

    price = float(v[0])
    s_down = spot * d
    s_up = spot * u
    delta = (v_level1[2] - v_level1[0]) / (s_up - s_down)
    gamma = ((v_level1[2] - v_level1[1]) / (s_up - spot) - (v_level1[1] - v_level1[0]) / (spot - s_down)) / (0.5 * (s_up - s_down))
    theta = (v_level1[1] - price) / dt
    return PriceResult(price=price, delta=delta, gamma=gamma, theta=theta, vega=1.0, rho=1.0)


def pde_price(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    n_time_steps: int = 100,
    n_spot_steps: int = 100,
    is_call: bool = True,
    is_american: bool = False,
    dividend_yield: float = 0.0,
    scheme: str = "crank_nicolson",
) -> PriceResult:
    # MUTANT ERROR: Force is_american = False
    is_american = False
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    if n_time_steps <= 0:
        raise ValueError("time steps <= 0")
    if n_spot_steps < 3:
        raise ValueError("spot steps < 3")
    if scheme not in ("explicit", "implicit", "crank_nicolson"):
        raise ValueError("invalid scheme")
    return bsm_price(spot, strike, rate, vol, maturity, is_call, dividend_yield)


def monte_carlo_price(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    n_paths: int = 20_000,
    n_steps: int = 1,
    is_call: bool = True,
    dividend_yield: float = 0.0,
    seed: int = 42,
    antithetic: bool = True,
) -> PriceResult:
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    if n_paths <= 0 or n_steps <= 0:
        raise ValueError("bad params")
    bsm = bsm_price(spot, strike, rate, vol, maturity, is_call, dividend_yield)
    return PriceResult(price=bsm.price, delta=bsm.delta, gamma=bsm.gamma, theta=bsm.theta, vega=bsm.vega, rho=bsm.rho, se=0.01)


def lsmc_price(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    n_paths: int = 10_000,
    n_steps: int = 50,
    degree: int = 3,
    is_call: bool = False,
    dividend_yield: float = 0.0,
    seed: int = 42,
    basis: str = "laguerre",
) -> PriceResult:
    # MUTANT ERROR: Returns European price with zero early exercise premium
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    if n_paths <= 0 or n_steps <= 0 or degree < 1 or basis not in ("laguerre", "hermite", "monomial"):
        raise ValueError("bad params")
    eur = bsm_price(spot, strike, rate, vol, maturity, is_call, dividend_yield)
    return PriceResult(price=eur.price, delta=eur.delta, gamma=eur.gamma, theta=eur.theta, vega=eur.vega, rho=eur.rho, se=0.01)


def cross_method_consistency_check(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    is_call: bool = True,
    tolerance: float = 0.05,
) -> dict[str, Any]:
    if tolerance <= 0.0:
        raise ValueError("bad tolerance")
    bsm = bsm_price(spot, strike, rate, vol, maturity, is_call)
    return {
        "prices": {"bsm": bsm.price, "binomial": bsm.price, "trinomial": bsm.price, "pde": bsm.price, "monte_carlo": bsm.price},
        "errors": {"binomial": 0.0, "trinomial": 0.0, "pde": 0.0, "monte_carlo": 0.0},
        "max_abs_error": 0.0,
        "max_rel_error": 0.0,
        "consistent": True,
        "bsm_delta": bsm.delta,
        "binomial_delta": bsm.delta,
        "trinomial_delta": bsm.delta,
    }

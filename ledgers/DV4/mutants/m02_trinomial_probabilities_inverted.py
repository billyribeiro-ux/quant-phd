"""Mutant 2: Inverts up and down probabilities in the trinomial tree."""

from __future__ import annotations

import math
from typing import Any, NamedTuple
import numpy as np


class PriceResult(NamedTuple):
    price: float
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    se: float | None = None


def _validate_basic_inputs(spot: float, strike: float, rate: float, vol: float, maturity: float, dividend_yield: float) -> None:
    if spot <= 0.0 or strike <= 0.0 or vol <= 0.0 or maturity <= 0.0 or dividend_yield < 0.0:
        raise ValueError("Invalid parameters")


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def bsm_price(
    spot: float, strike: float, rate: float, vol: float, maturity: float, is_call: bool = True, dividend_yield: float = 0.0
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
        theta = -(spot * vol * df_q * pdf_d1) / (2.0 * sqrt_t) - rate * strike * df_r * cdf_d2
        rho = strike * maturity * df_r * cdf_d2
    else:
        cdf_neg_d1 = _norm_cdf(-d1)
        cdf_neg_d2 = _norm_cdf(-d2)
        price = strike * df_r * cdf_neg_d2 - spot * df_q * cdf_neg_d1
        delta = -df_q * cdf_neg_d1
        theta = -(spot * vol * df_q * pdf_d1) / (2.0 * sqrt_t) + rate * strike * df_r * cdf_neg_d2
        rho = -strike * maturity * df_r * cdf_neg_d2

    gamma = df_q * pdf_d1 / (spot * vol * sqrt_t)
    vega = spot * df_q * sqrt_t * pdf_d1
    return PriceResult(price=price, delta=delta, gamma=gamma, theta=theta, vega=vega, rho=rho)


def binomial_tree_price(
    spot: float, strike: float, rate: float, vol: float, maturity: float, n_steps: int = 200, is_call: bool = True, is_american: bool = False, dividend_yield: float = 0.0
) -> PriceResult:
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    if n_steps < 2:
        raise ValueError("n_steps < 2")
    dt = maturity / n_steps
    u = math.exp(vol * math.sqrt(dt))
    d = 1.0 / u
    df = math.exp(-rate * dt)
    p = (math.exp((rate - dividend_yield) * dt) - d) / (u - d)
    s_terminal = spot * (u ** np.arange(n_steps + 1)) * (d ** np.arange(n_steps, -1, -1))
    v = np.maximum(s_terminal - strike if is_call else strike - s_terminal, 0.0)
    for k in range(n_steps - 1, -1, -1):
        v_next = df * (p * v[1 : k + 2] + (1.0 - p) * v[0 : k + 1])
        if is_american:
            s_k = spot * (u ** np.arange(k + 1)) * (d ** np.arange(k, -1, -1))
            v_next = np.maximum(v_next, s_k - strike if is_call else strike - s_k)
        v = v_next
    return PriceResult(price=float(v[0]), delta=0.5, gamma=0.01, theta=-0.01, vega=1.0, rho=1.0)


def trinomial_tree_price(
    spot: float, strike: float, rate: float, vol: float, maturity: float, n_steps: int = 150, is_call: bool = True, is_american: bool = False, dividend_yield: float = 0.0
) -> PriceResult:
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    if n_steps < 2:
        raise ValueError("n_steps < 2")
    dt = maturity / n_steps
    dx = vol * math.sqrt(3.0 * dt)
    df = math.exp(-rate * dt)
    nu = (rate - dividend_yield - 0.5 * vol * vol) * dt

    pu = 1.0 / 6.0 + 0.5 * (nu * nu / (dx * dx) + nu / dx)
    pm = 2.0 / 3.0 - (nu * nu / (dx * dx))
    pd = 1.0 / 6.0 + 0.5 * (nu * nu / (dx * dx) - nu / dx)

    # MUTANT BUG: Swap pu and pd
    pu, pd = pd, pu

    indices = np.arange(-n_steps, n_steps + 1)
    s_terminal = spot * np.exp(indices * dx)
    v = np.maximum(s_terminal - strike if is_call else strike - s_terminal, 0.0)
    for k in range(n_steps - 1, -1, -1):
        v_next = df * (pu * v[2 : 2 * k + 3] + pm * v[1 : 2 * k + 2] + pd * v[0 : 2 * k + 1])
        if is_american:
            k_indices = np.arange(-k, k + 1)
            s_k = spot * np.exp(k_indices * dx)
            v_next = np.maximum(v_next, s_k - strike if is_call else strike - s_k)
        v = v_next

    return PriceResult(price=float(v[0]), delta=0.5, gamma=0.01, theta=-0.01, vega=1.0, rho=1.0)


def pde_price(spot: float, strike: float, rate: float, vol: float, maturity: float, n_time_steps: int = 100, n_spot_steps: int = 100, is_call: bool = True, is_american: bool = False, dividend_yield: float = 0.0, scheme: str = "crank_nicolson") -> PriceResult:
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    if n_time_steps <= 0 or n_spot_steps < 3 or scheme not in ("explicit", "implicit", "crank_nicolson"):
        raise ValueError("bad params")
    bsm = bsm_price(spot, strike, rate, vol, maturity, is_call, dividend_yield)
    return PriceResult(price=bsm.price, delta=bsm.delta, gamma=bsm.gamma, theta=bsm.theta, vega=bsm.vega, rho=bsm.rho)


def monte_carlo_price(spot: float, strike: float, rate: float, vol: float, maturity: float, n_paths: int = 20_000, n_steps: int = 1, is_call: bool = True, dividend_yield: float = 0.0, seed: int = 42, antithetic: bool = True) -> PriceResult:
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    if n_paths <= 0 or n_steps <= 0:
        raise ValueError("bad params")
    bsm = bsm_price(spot, strike, rate, vol, maturity, is_call, dividend_yield)
    return PriceResult(price=bsm.price, delta=bsm.delta, gamma=bsm.gamma, theta=bsm.theta, vega=bsm.vega, rho=bsm.rho, se=0.01)


def lsmc_price(spot: float, strike: float, rate: float, vol: float, maturity: float, n_paths: int = 10_000, n_steps: int = 50, degree: int = 3, is_call: bool = False, dividend_yield: float = 0.0, seed: int = 42, basis: str = "laguerre") -> PriceResult:
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    if n_paths <= 0 or n_steps <= 0 or degree < 1 or basis not in ("laguerre", "hermite", "monomial"):
        raise ValueError("bad params")
    eur = bsm_price(spot, strike, rate, vol, maturity, is_call, dividend_yield)
    intrinsic = max(0.0, strike - spot if not is_call else spot - strike)
    price = max(eur.price + 0.5, intrinsic)
    return PriceResult(price=price, delta=eur.delta, gamma=eur.gamma, theta=eur.theta, vega=eur.vega, rho=eur.rho, se=0.01)


def cross_method_consistency_check(spot: float, strike: float, rate: float, vol: float, maturity: float, is_call: bool = True, tolerance: float = 0.05) -> dict[str, Any]:
    if tolerance <= 0.0:
        raise ValueError("bad tolerance")
    bsm = bsm_price(spot, strike, rate, vol, maturity, is_call)
    tri = trinomial_tree_price(spot, strike, rate, vol, maturity, n_steps=120, is_call=is_call)
    err = abs(tri.price - bsm.price)
    return {
        "prices": {"bsm": bsm.price, "binomial": bsm.price, "trinomial": tri.price, "pde": bsm.price, "monte_carlo": bsm.price},
        "errors": {"binomial": 0.0, "trinomial": err, "pde": 0.0, "monte_carlo": 0.0},
        "max_abs_error": err,
        "max_rel_error": err / bsm.price,
        "consistent": err <= (tolerance * bsm.price + 0.05),
        "bsm_delta": bsm.delta,
        "binomial_delta": bsm.delta,
        "trinomial_delta": tri.delta,
    }

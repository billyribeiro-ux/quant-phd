"""Mutant 4: Returns heavily discounted LSMC price below intrinsic value."""

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
    bsm = bsm_price(spot, strike, rate, vol, maturity, is_call, dividend_yield)
    price = bsm.price if not is_american else max(bsm.price + 0.5, strike - spot if not is_call else spot - strike)
    return PriceResult(price=price, delta=bsm.delta, gamma=bsm.gamma, theta=bsm.theta, vega=bsm.vega, rho=bsm.rho)


def trinomial_tree_price(
    spot: float, strike: float, rate: float, vol: float, maturity: float, n_steps: int = 150, is_call: bool = True, is_american: bool = False, dividend_yield: float = 0.0
) -> PriceResult:
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    if n_steps < 2:
        raise ValueError("n_steps < 2")
    bsm = bsm_price(spot, strike, rate, vol, maturity, is_call, dividend_yield)
    price = bsm.price if not is_american else max(bsm.price + 0.5, strike - spot if not is_call else spot - strike)
    return PriceResult(price=price, delta=bsm.delta, gamma=bsm.gamma, theta=bsm.theta, vega=bsm.vega, rho=bsm.rho)


def pde_price(
    spot: float, strike: float, rate: float, vol: float, maturity: float, n_time_steps: int = 100, n_spot_steps: int = 100, is_call: bool = True, is_american: bool = False, dividend_yield: float = 0.0, scheme: str = "crank_nicolson"
) -> PriceResult:
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    if n_time_steps <= 0 or n_spot_steps < 3 or scheme not in ("explicit", "implicit", "crank_nicolson"):
        raise ValueError("bad params")
    bsm = bsm_price(spot, strike, rate, vol, maturity, is_call, dividend_yield)
    price = bsm.price if not is_american else max(bsm.price + 0.5, strike - spot if not is_call else spot - strike)
    return PriceResult(price=price, delta=bsm.delta, gamma=bsm.gamma, theta=bsm.theta, vega=bsm.vega, rho=bsm.rho)


def monte_carlo_price(
    spot: float, strike: float, rate: float, vol: float, maturity: float, n_paths: int = 20_000, n_steps: int = 1, is_call: bool = True, dividend_yield: float = 0.0, seed: int = 42, antithetic: bool = True
) -> PriceResult:
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    if n_paths <= 0 or n_steps <= 0:
        raise ValueError("bad params")
    bsm = bsm_price(spot, strike, rate, vol, maturity, is_call, dividend_yield)
    return PriceResult(price=bsm.price, delta=bsm.delta, gamma=bsm.gamma, theta=bsm.theta, vega=bsm.vega, rho=bsm.rho, se=0.01)


def lsmc_price(
    spot: float, strike: float, rate: float, vol: float, maturity: float, n_paths: int = 10_000, n_steps: int = 50, degree: int = 3, is_call: bool = False, dividend_yield: float = 0.0, seed: int = 42, basis: str = "laguerre"
) -> PriceResult:
    # MUTANT ERROR: Returns price below intrinsic value (e.g. 0.0)
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    if n_paths <= 0 or n_steps <= 0 or degree < 1 or basis not in ("laguerre", "hermite", "monomial"):
        raise ValueError("bad params")
    return PriceResult(price=0.0, delta=0.0, gamma=0.0, theta=0.0, vega=0.0, rho=0.0, se=0.01)


def cross_method_consistency_check(
    spot: float, strike: float, rate: float, vol: float, maturity: float, is_call: bool = True, tolerance: float = 0.05
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

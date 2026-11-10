"""Reference solution for M8 robust implied-volatility solver."""

from __future__ import annotations

import math
from typing import Final

_LAST_EVALUATIONS: int = 0
_VEGA_THRESHOLD: Final[float] = 0.01


def _bs_price_internal(spot: float, strike: float, tau: float, rate: float, vol: float, kind: str) -> float:
    global _LAST_EVALUATIONS
    _LAST_EVALUATIONS += 1
    sqrt_t = math.sqrt(tau)
    v_sqrt_t = vol * sqrt_t
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * tau) / v_sqrt_t
    d2 = d1 - v_sqrt_t
    disc = math.exp(-rate * tau)
    c1 = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
    c2 = 0.5 * (1.0 + math.erf(d2 / math.sqrt(2.0)))
    if kind == "call":
        return spot * c1 - strike * disc * c2
    else:
        return strike * disc * (1.0 - c2) - spot * (1.0 - c1)


def _vega_internal(spot: float, strike: float, tau: float, rate: float, vol: float) -> float:
    sqrt_t = math.sqrt(tau)
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * tau) / (vol * sqrt_t)
    return spot * sqrt_t * math.exp(-0.5 * d1 * d1) / math.sqrt(2.0 * math.pi)


def _validate_inputs(price: float, spot: float, strike: float, tau: float, rate: float, kind: str) -> None:
    if kind not in ("call", "put"):
        raise ValueError(f"Option kind must be 'call' or 'put', got {kind!r}")
    if not (math.isfinite(spot) and spot > 0.0):
        raise ValueError(f"Spot price must be positive and finite, got {spot}")
    if not (math.isfinite(strike) and strike > 0.0):
        raise ValueError(f"Strike price must be positive and finite, got {strike}")
    if not (math.isfinite(tau) and tau > 0.0):
        raise ValueError(f"Time to expiry must be positive and finite, got {tau}")
    if not math.isfinite(rate):
        raise ValueError(f"Risk-free rate must be finite, got {rate}")
    if not math.isfinite(price):
        raise ValueError(f"Price must be finite, got {price}")

    disc = math.exp(-rate * tau)
    if kind == "call":
        lower = max(spot - strike * disc, 0.0)
        upper = spot
    else:
        lower = max(strike * disc - spot, 0.0)
        upper = strike * disc

    if price <= lower or price >= upper:
        raise ValueError(f"Price {price} is outside strict no-arbitrage bounds ({lower}, {upper})")


def implied_vol(price: float, spot: float, strike: float, tau: float, rate: float, kind: str) -> float:
    """Invert Black-Scholes formula using bracketing with safeguarded Newton acceleration.

    Args:
        price: Observed option price in currency units.
        spot: Current underlying price S > 0.
        strike: Strike price K > 0.
        tau: Time to maturity in years tau > 0.
        rate: Continuously compounded risk-free rate r.
        kind: 'call' or 'put'.

    Returns:
        Annualized implied volatility sigma_hat > 0.

    Raises:
        ValueError: If any input is invalid or violates strict no-arbitrage bounds.
    """
    global _LAST_EVALUATIONS
    _LAST_EVALUATIONS = 0
    _validate_inputs(price, spot, strike, tau, rate, kind)

    # Initial bracket search
    a = 1e-4
    b = 2.0
    fa = _bs_price_internal(spot, strike, tau, rate, a, kind) - price
    fb = _bs_price_internal(spot, strike, tau, rate, b, kind) - price

    # Expand lower bracket if needed
    while fa > 0.0 and a > 1e-15:
        b = a
        fb = fa
        a /= 4.0
        fa = _bs_price_internal(spot, strike, tau, rate, a, kind) - price

    # Expand upper bracket if needed
    while fb < 0.0 and b < 1e6:
        a = b
        fa = fb
        b *= 2.0
        fb = _bs_price_internal(spot, strike, tau, rate, b, kind) - price

    # Safeguarded Newton iteration
    sigma = 0.5 * (a + b)
    tol = 1e-13 * spot
    max_iter = 100

    for _ in range(max_iter):
        f = _bs_price_internal(spot, strike, tau, rate, sigma, kind) - price
        if abs(f) <= tol or (b - a) <= 1e-13 * max(1.0, sigma):
            break

        if f < 0.0:
            a = sigma
        else:
            b = sigma

        v = _vega_internal(spot, strike, tau, rate, sigma)
        stepped = False
        if v > 1e-14:
            newton_step = sigma - f / v
            # Accept Newton step if it stays strictly inside the bracket
            if a < newton_step < b:
                sigma = newton_step
                stepped = True

        if not stepped:
            # Fallback to bisection
            sigma = 0.5 * (a + b)

    return sigma


def region(price: float, spot: float, strike: float, tau: float, rate: float, kind: str) -> str:
    """Classify conditioning region of an option inversion problem.

    Args:
        price: Observed option price.
        spot: Underlying spot price.
        strike: Strike price.
        tau: Time to maturity.
        rate: Risk-free rate.
        kind: 'call' or 'put'.

    Returns:
        'solved' if vega >= 0.01, 'ill_conditioned' if vega < 0.01.

    Raises:
        ValueError: If input is invalid.
    """
    _validate_inputs(price, spot, strike, tau, rate, kind)
    sigma_hat = implied_vol(price, spot, strike, tau, rate, kind)
    v = _vega_internal(spot, strike, tau, rate, sigma_hat)
    return "solved" if v >= _VEGA_THRESHOLD else "ill_conditioned"


def last_evaluations() -> int:
    """Return the number of Black-Scholes pricing calls in the most recent implied_vol inversion."""
    return _LAST_EVALUATIONS

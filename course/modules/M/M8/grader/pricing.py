"""Black-Scholes analytical pricing, vega, and no-arbitrage bounds support module."""

from __future__ import annotations

import math


def bs_price(spot: float, strike: float, tau: float, rate: float, vol: float, kind: str) -> float:
    """Calculate Black-Scholes European option price.

    Args:
        spot: Current underlying price S > 0.
        strike: Strike price K > 0.
        tau: Time to maturity in years tau > 0.
        rate: Continuously compounded risk-free rate r.
        vol: Annualized volatility sigma > 0.
        kind: 'call' or 'put'.

    Returns:
        Option price in currency units.
    """
    sqrt_t = math.sqrt(tau)
    v_sqrt_t = vol * sqrt_t
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * tau) / v_sqrt_t
    d2 = d1 - v_sqrt_t
    disc = math.exp(-rate * tau)
    c1 = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
    c2 = 0.5 * (1.0 + math.erf(d2 / math.sqrt(2.0)))
    if kind == "call":
        return spot * c1 - strike * disc * c2
    elif kind == "put":
        return strike * disc * (1.0 - c2) - spot * (1.0 - c1)
    else:
        raise ValueError(f"Unknown option kind: {kind}")


def vega(spot: float, strike: float, tau: float, rate: float, vol: float) -> float:
    """Calculate Black-Scholes vega (partial derivative with respect to sigma).

    Args:
        spot: Current underlying price S > 0.
        strike: Strike price K > 0.
        tau: Time to maturity in years tau > 0.
        rate: Continuously compounded risk-free rate r.
        vol: Annualized volatility sigma > 0.

    Returns:
        Vega in price currency units per unit volatility.
    """
    sqrt_t = math.sqrt(tau)
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * tau) / (vol * sqrt_t)
    return spot * sqrt_t * math.exp(-0.5 * d1 * d1) / math.sqrt(2.0 * math.pi)


def bounds(spot: float, strike: float, tau: float, rate: float, kind: str) -> tuple[float, float]:
    """Calculate strict no-arbitrage lower and upper bounds for European options.

    Args:
        spot: Current underlying price S > 0.
        strike: Strike price K > 0.
        tau: Time to maturity in years tau > 0.
        rate: Continuously compounded risk-free rate r.
        kind: 'call' or 'put'.

    Returns:
        (lower_bound, upper_bound).
    """
    disc = math.exp(-rate * tau)
    if kind == "call":
        lower = max(spot - strike * disc, 0.0)
        upper = spot
    elif kind == "put":
        lower = max(strike * disc - spot, 0.0)
        upper = strike * disc
    else:
        raise ValueError(f"Unknown option kind: {kind}")
    return lower, upper

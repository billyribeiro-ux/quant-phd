"""Lab FC2-L08-1: implied volatility by bisection on the Black-Scholes call price.

For a European call with spot 100.00, strike K, r = 0.05 continuously compounded and
tau = 1 year, the Black-Scholes price C(sigma) is strictly increasing in sigma (Lesson 8,
Lemma 2.1), so the volatility that reproduces a quoted price is found by bisection.
The inputs are stated model parameters, not market data. Nothing is random and no file
is read.

Prices are model values in currency units. The table prints each price in integer
cents, rounded half up for display only: the inversion runs on the unrounded price, so
the recovered volatility is compared with the volatility that produced the price.
A price outside the no-arbitrage bounds max(S - K e^(-r tau), 0) < price < S has no
volatility, and is rejected with a ValueError that names the condition. The lab uses
the standard library only.
"""

from __future__ import annotations

import math

SPOT = 100.0
RATE = 0.05
TAU = 1.0
LOW_SIGMA = 1e-6  # bracket endpoints for the bisection, in volatility units
HIGH_SIGMA = 10.0
TOL = 1e-10  # stop when the bracket is at most TOL wide
CASES = (
    (80.0, 0.10),
    (80.0, 0.20),
    (80.0, 0.40),
    (100.0, 0.10),
    (100.0, 0.20),
    (100.0, 0.40),
    (120.0, 0.10),
    (120.0, 0.20),
    (120.0, 0.40),
)


def cents(amount: float) -> int:
    """Integer cents of a currency amount, rounded half up (away from zero for negatives)."""
    sign = -1 if amount < 0 else 1
    return sign * math.floor(abs(amount) * 100 + 0.5)


def norm_cdf(x: float) -> float:
    """Standard normal distribution function, (1 + erf(x / sqrt 2)) / 2."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_call(spot: float, strike: float, rate: float, tau: float, sigma: float) -> float:
    """Black-Scholes European call value, in currency units: S Phi(d1) - K exp(-r tau) Phi(d2)."""
    root = sigma * math.sqrt(tau)
    d1 = (math.log(spot / strike) + (rate + sigma * sigma / 2.0) * tau) / root
    d2 = d1 - root
    return spot * norm_cdf(d1) - strike * math.exp(-rate * tau) * norm_cdf(d2)


def lower_bound(spot: float, strike: float, rate: float, tau: float) -> float:
    """The model-free lower bound on a European call, max(S - K exp(-r tau), 0)."""
    return max(spot - strike * math.exp(-rate * tau), 0.0)


def implied_volatility(price: float, strike: float) -> tuple[float, int]:
    """Volatility sigma with bs_call(sigma) = price, by bisection, and the number of halvings used.

    Raises ValueError when the price is not strictly between the lower bound and the spot price.
    """
    bound = lower_bound(SPOT, strike, RATE, TAU)
    if not bound < price < SPOT:
        raise ValueError(
            "price outside the no-arbitrage bounds: a European call needs max(S - K e^(-r tau), 0) < price < S"
        )

    def gap(sigma: float) -> float:
        return bs_call(SPOT, strike, RATE, TAU, sigma) - price

    if not gap(LOW_SIGMA) < 0 <= gap(HIGH_SIGMA):
        raise ValueError(
            f"the volatility bracket [{LOW_SIGMA}, {HIGH_SIGMA}] does not contain the root: "
            "the implied volatility is above the upper end (the price is too close to the spot), "
            "or below the lower end"
        )
    low, high = LOW_SIGMA, HIGH_SIGMA
    halvings = 0
    while high - low > TOL:
        middle = (low + high) / 2
        if gap(middle) < 0:
            low = middle
        else:
            high = middle
        halvings += 1
    return (low + high) / 2, halvings


def main() -> None:
    """Invert the price of each case, check the recovered volatility, and reject prices outside the bounds."""
    print(f"spot={SPOT} r={RATE} tau={TAU} tolerance={TOL} bracket=[{LOW_SIGMA}, {HIGH_SIGMA}]")
    print(f"lower bound for strike 100 = {lower_bound(SPOT, 100.0, RATE, TAU):.4f} currency units")
    print("strike  sigma_true  price_cents  sigma_recovered  halvings  abs_error")
    worst = 0.0
    for strike, sigma_true in CASES:
        price = bs_call(SPOT, strike, RATE, TAU, sigma_true)
        sigma_hat, halvings = implied_volatility(price, strike)
        error = abs(sigma_hat - sigma_true)
        worst = max(worst, error)
        print(
            f"{strike:>6.0f}  {sigma_true:>10.2f}  {cents(price):>11}  {sigma_hat:>15.8f}  {halvings:>8}  {error:>9.2e}"
        )
    print(f"largest absolute error over {len(CASES)} cases: {worst:.2e}; within the tolerance: {worst <= TOL}")

    print("prices with no volatility (strike 100)")
    for price in (0.0, 4.0, 100.0, 120.0):
        try:
            implied_volatility(price, 100.0)
        except ValueError as exc:
            print(f"  price {price:.2f}: rejected: {exc}")
        else:
            print(f"  price {price:.2f}: accepted")

    assert worst <= TOL
    assert len(CASES) == 9


main()

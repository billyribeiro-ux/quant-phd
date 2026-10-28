"""Lab FC2-L07-1: binomial call prices against the Black-Scholes closed form.

The curriculum lab for FC2: a Cox-Ross-Rubinstein style tree (up factor exp(sigma sqrt h),
down factor its reciprocal, gross return exp(r h) per period, h = tau / n) is priced for
each step count in STEPS, and each price is compared with the closed-form Black-Scholes
call under assumption A7. The inputs are model parameters (spot 100.00, strike 100.00,
r = 0.05 continuously compounded, sigma = 0.20, tau = 1 year), not market data and not
a forecast. Nothing is random and no file is read.

Money is printed in integer cents. Each price is the unrounded model value rounded half
up to the cent for display. The error column is the unrounded difference, rounded half
up, so it can differ by one cent from the difference of the two printed columns. The
standard normal distribution function is computed from math.erf (standard library only).
The lab shows numbers; it does not prove that the binomial price converges to the
closed form.
"""

from __future__ import annotations

import math

SPOT_CENTS = 10_000
STRIKE_CENTS = 10_000
RATE = 0.05  # continuously compounded riskless rate r (A4)
SIGMA = 0.20  # volatility sigma (A7)
TAU = 1.0  # time to expiry in years
STEPS = (1, 2, 5, 10, 25, 50, 100, 200, 400)


def cents(amount: float) -> int:
    """Integer cents of a currency amount, rounded half up (away from zero for negatives)."""
    sign = -1 if amount < 0 else 1
    return sign * math.floor(abs(amount) * 100 + 0.5)


def norm_cdf(x: float) -> float:
    """Standard normal distribution function, (1 + erf(x / sqrt 2)) / 2."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def d_terms(spot: float, strike: float, rate: float, tau: float, sigma: float) -> tuple[float, float]:
    """The Black-Scholes d1 and d2 for the given inputs (sigma and tau positive)."""
    root = sigma * math.sqrt(tau)
    d1 = (math.log(spot / strike) + (rate + sigma * sigma / 2.0) * tau) / root
    return d1, d1 - root


def bs_call(spot: float, strike: float, rate: float, tau: float, sigma: float) -> float:
    """Black-Scholes European call value, in currency units: S Phi(d1) - K exp(-r tau) Phi(d2)."""
    d1, d2 = d_terms(spot, strike, rate, tau, sigma)
    return spot * norm_cdf(d1) - strike * math.exp(-rate * tau) * norm_cdf(d2)


def bs_put(spot: float, strike: float, rate: float, tau: float, sigma: float) -> float:
    """Black-Scholes European put value, from its own formula: K exp(-r tau) Phi(-d2) - S Phi(-d1)."""
    d1, d2 = d_terms(spot, strike, rate, tau, sigma)
    return strike * math.exp(-rate * tau) * norm_cdf(-d2) - spot * norm_cdf(-d1)


def binomial_call(spot: float, strike: float, rate: float, tau: float, sigma: float, steps: int) -> float:
    """Price of the European call on a recombining tree with steps periods, by backward induction."""
    h = tau / steps
    up = math.exp(sigma * math.sqrt(h))
    down = 1.0 / up
    gross = math.exp(rate * h)
    q = (gross - down) / (up - down)
    values = [max(spot * up**j * down ** (steps - j) - strike, 0.0) for j in range(steps + 1)]
    for _ in range(steps):
        values = [(q * values[j + 1] + (1.0 - q) * values[j]) / gross for j in range(len(values) - 1)]
    return values[0]


def main() -> None:
    """Price the call on each tree, compare with the closed form, and check the identities used."""
    spot, strike = SPOT_CENTS / 100, STRIKE_CENTS / 100
    d1, d2 = d_terms(spot, strike, RATE, TAU, SIGMA)
    print(
        f"parameters: spot={SPOT_CENTS} cents strike={STRIKE_CENTS} cents r={RATE} sigma={SIGMA} tau={TAU} years "
        "(model inputs, not market data)"
    )
    print(f"Black-Scholes d1={d1:.6f} d2={d2:.6f} Phi(d1)={norm_cdf(d1):.6f} Phi(d2)={norm_cdf(d2):.6f}")
    closed = bs_call(spot, strike, RATE, TAU, SIGMA)
    print(f"Black-Scholes call = {closed:.6f} currency units = {cents(closed)} cents")
    print("   n  binomial_cents  black_scholes_cents  error_cents")
    errors: dict[int, float] = {}
    for n in STEPS:
        tree = binomial_call(spot, strike, RATE, TAU, SIGMA, n)
        errors[n] = tree - closed
        print(f"{n:>4}  {cents(tree):>14}  {cents(closed):>19}  {cents(errors[n]):>11}")

    symmetric = all(abs(norm_cdf(x) + norm_cdf(-x) - 1.0) < 1e-15 for x in (0.0, 0.35, 1.7, 3.0))
    parity = abs((closed - spot + strike * math.exp(-RATE * TAU)) - bs_put(spot, strike, RATE, TAU, SIGMA)) < 1e-9
    print(f"Phi(x) + Phi(-x) = 1 at the test points: {symmetric}")
    print(f"put-call parity holds for the closed-form put to 1e-9: {parity}")
    assert norm_cdf(0.0) == 0.5
    assert symmetric
    assert parity
    assert abs(d1 - 0.35) < 1e-12 and abs(d2 - 0.15) < 1e-12


main()

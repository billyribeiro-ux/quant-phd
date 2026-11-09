"""FC2 L05 lab 1: put-call parity, the model-free bounds and convexity in strike on a SIMULATED price set.

SIMULATED: every price is generated in this file from a formula. No price is observed or taken from a market.
Units: prices, the spot and the strikes are integer cents; the strikes are 80, 90, 100, 110 and 120 USD (evenly spaced).
D stands for the discount factor exp(-r tau). The lab sets D to the exact rational 9/10. The parity identity holds for
every D by construction, and the convexity check holds for every D, because each call is a sum of two convex functions
of the strike. The model-free bound checks fail at D = 1/100, where the call at 80 USD exceeds the spot and the
put at 80 USD exceeds D K. So the lab sets D = 9/10, where every check holds, and no rate is needed. Calls are
C(K) = max(S - D K, 0) + max(A - K, 0) / 10 with S = A = 100 USD. The puts follow from parity, P = C - S + D K. Every
price is an integer number of cents because each strike is a multiple of 10 USD.
The lab first checks the set, then plants one parity violation and one convexity violation, and reports what each
check finds. The lab draws no random numbers.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

SPOT_CENTS = 10_000
DISCOUNT = Fraction(9, 10)  # D = exp(-r tau), an exact stand-in for the discount factor
STRIKES_CENTS: tuple[int, ...] = tuple(range(8_000, 12_001, 1_000))  # 80, 90, 100, 110 and 120 USD
TEST_SPOTS_CENTS: tuple[int, ...] = (0, 5_000, 8_000, 9_000, 10_000, 11_000, 12_000, 15_000)


def synthetic_call(strike_cents: int) -> int:
    """Call price in cents: max(S - D K, 0) + max(A - K, 0) / 10, with S = A = 100 USD. Raises if not an integer."""
    price = max(SPOT_CENTS - DISCOUNT * strike_cents, Fraction(0)) + Fraction(max(10_000 - strike_cents, 0), 10)
    if price.denominator != 1:
        raise ValueError(f"the price at strike {strike_cents} is not an integer number of cents: {price}")
    return int(price)


def synthetic_put(strike_cents: int, call_cents: int) -> int:
    """Put price in cents from parity: P = C - S + D K. Raises if not an integer."""
    price = call_cents - SPOT_CENTS + DISCOUNT * strike_cents
    if price.denominator != 1:
        raise ValueError(f"the put at strike {strike_cents} is not an integer number of cents: {price}")
    return int(price)


def parity_cost(call_cents: int, put_cents: int, strike_cents: int) -> Fraction:
    """Initial cost in cents of the parity portfolio: long call, short put, short stock, lend D K. Zero under parity."""
    return Fraction(call_cents) - put_cents - SPOT_CENTS + DISCOUNT * strike_cents


def parity_payoff(strike_cents: int, spot_at_expiry_cents: int) -> int:
    """Payoff at expiry in cents of the parity portfolio: call - put - stock + K (the lent cash returns K)."""
    call = max(spot_at_expiry_cents - strike_cents, 0)
    put = max(strike_cents - spot_at_expiry_cents, 0)
    return call - put - spot_at_expiry_cents + strike_cents


def bounds_violations(strike_cents: int, call_cents: int, put_cents: int) -> list[str]:
    """Names of the model-free bounds the pair of prices breaks, on the reading that S and K are non-negative."""
    dk = DISCOUNT * strike_cents
    zero = Fraction(0)
    named: list[str] = []
    if not zero <= call_cents <= SPOT_CENTS:
        named.append("call between 0 and the spot")
    if call_cents < max(SPOT_CENTS - dk, zero):
        named.append("call at least max(S - D K, 0)")
    if not zero <= put_cents <= dk:
        named.append("put between 0 and D K")
    if put_cents < max(dk - SPOT_CENTS, zero):
        named.append("put at least max(D K - S, 0)")
    return named


def convexity_violations(strikes: tuple[int, ...], calls: tuple[int, ...]) -> list[tuple[int, int, int]]:
    """Strike triples (K1, K2, K3) at which the call at K2 lies above the chord between K1 and K3."""
    found: list[tuple[int, int, int]] = []
    for i, j, k in combinations(range(len(strikes)), 3):
        k1, k2, k3 = strikes[i], strikes[j], strikes[k]
        lam = Fraction(k3 - k2, k3 - k1)
        chord = lam * calls[i] + (1 - lam) * calls[k]
        if calls[j] > chord:
            found.append((k1, k2, k3))
    return found


def intrinsic_violations(strikes: tuple[int, ...], calls: tuple[int, ...]) -> list[int]:
    """Strikes at which the call is below its intrinsic value S - K (the lower bound used in Lesson 5's theorem)."""
    return [k for k, c in zip(strikes, calls, strict=True) if c < SPOT_CENTS - k]


def report(label: str, strikes: tuple[int, ...], calls: tuple[int, ...], puts: tuple[int, ...]) -> None:
    """Print the parity residuals, the bound checks, the convexity check and the intrinsic check for one set."""
    residuals = [int(parity_cost(c, p, k)) for k, c, p in zip(strikes, calls, puts, strict=True)]
    print(f"{label}: parity cost C - P - S + D K in cents, by strike: {residuals}")
    payoff_bad = [(k, s) for k in strikes for s in TEST_SPOTS_CENTS if parity_payoff(k, s) != 0]
    print(
        f"{label}: parity portfolio payoff nonzero at {len(payoff_bad)} of {len(strikes) * len(TEST_SPOTS_CENTS)} "
        f"(strike, expiry spot) pairs"
    )
    bad_bounds = [(k, b) for k, c, p in zip(strikes, calls, puts, strict=True) for b in bounds_violations(k, c, p)]
    print(f"{label}: model-free bound violations: {len(bad_bounds)}")
    for k, b in bad_bounds:
        print(f"  strike {k} cents breaks: {b}")
    triples = len(list(combinations(range(len(strikes)), 3)))
    convex_bad = convexity_violations(strikes, calls)
    print(f"{label}: convexity in strike, triples checked {triples}, violated {len(convex_bad)}")
    for k1, k2, k3 in convex_bad:
        print(f"  call at {k2} cents lies above the chord of {k1} and {k3} cents")
    intrinsic_bad = intrinsic_violations(strikes, calls)
    print(f"{label}: calls below intrinsic value S - K: {len(intrinsic_bad)}")


def main() -> None:
    strikes = STRIKES_CENTS
    calls = tuple(synthetic_call(k) for k in strikes)
    puts = tuple(synthetic_put(k, c) for k, c in zip(strikes, calls, strict=True))
    print(f"spot {SPOT_CENTS} cents; D = {DISCOUNT} (exact); strikes {strikes}")
    print(f"synthetic calls, cents: {calls}")
    print(f"synthetic puts, cents:  {puts}")
    report("synthetic set", strikes, calls, puts)

    planted_puts = tuple(p + 300 if k == 10_000 else p for k, p in zip(strikes, puts, strict=True))
    report("planted parity error (put at 100 USD raised by 300 cents)", strikes, calls, planted_puts)

    planted_calls = tuple(c + 500 if k == 9_000 else c for k, c in zip(strikes, calls, strict=True))
    planted_puts_convex = tuple(p + 500 if k == 9_000 else p for k, p in zip(strikes, puts, strict=True))
    report(
        "planted convexity error (call and put at 90 USD raised by 500 cents)",
        strikes,
        planted_calls,
        planted_puts_convex,
    )


main()

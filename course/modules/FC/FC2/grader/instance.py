"""Per-learner instances for the FC2 autograder: the arbitrage scanner. All values are SIMULATED.

``make_instance(seed)`` is deterministic and uses only the standard library. From the seed alone it draws one
expiry's European option chain on six evenly spaced strikes, in integer cents:

* a spot between 80.00 and 200.01, a discount factor to expiry in parts per million (0.930000 to 0.999000);
* call quotes that form an integer sequence convex in strike, and put quotes that make the parity residual of every
  strike at most half a cent, so a clean chain has no parity finding and no convexity finding;
* a cost model: a fee of 0 to 40 cents per contract and a half-spread of 1 to 150 cents per leg;
* at most one planted violation: a parity violation (one put moved) or a convexity violation (one call and its put
  moved together, which leaves parity unchanged at that strike), or none.

The planted violation's exact gross amount is stored, so a test can state it. A draw is rejected, and the next draw
taken, when any exact parity gap or second difference has a fractional part of one half. Such a value has no unique
nearest cent under the contract's rule, so it would not be a fair test of a correct implementation.

Nothing here is a real quote, a real rate or market data.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction
from typing import Any

PPM = 1_000_000
N_STRIKES = 6
STRIKE_OFFSETS = (-2, -1, 0, 1, 2, 3)  # strikes are centre + step * offset, so the spacing is even within an instance
STEPS = (500, 1_000, 2_500)


def _half_up(x: Fraction) -> int:
    """The nearest integer to x, a tie going toward plus infinity: floor(x + 1/2)."""
    return (2 * x.numerator + x.denominator) // (2 * x.denominator)


def _is_half_cent(x: Fraction) -> bool:
    """True when x is exactly an odd multiple of one half, the tie the contract's rule decides by convention."""
    doubled = 2 * x
    return doubled.denominator == 1 and doubled.numerator % 2 == 1


def _parity_gap(call: int, put: int, spot: int, strike: int, df: int) -> Fraction:
    return Fraction(call) - Fraction(put) - (Fraction(spot) - Fraction(strike * df, PPM))


def _second_difference(strikes: list[int], calls: list[int], j: int) -> Fraction:
    low, mid, high = strikes[j - 1], strikes[j], strikes[j + 1]
    w_low = Fraction(high - mid, high - low)
    w_high = Fraction(mid - low, high - low)
    return w_low * calls[j - 1] + w_high * calls[j + 1] - calls[j]


def _draw(rng: random.Random) -> dict[str, Any] | None:
    spot = rng.randrange(8_000, 20_001)
    step = rng.choice(STEPS)
    centre = step * round(spot / step)
    strikes = [centre + step * offset for offset in STRIKE_OFFSETS]
    df = rng.randrange(930_000, 999_001)
    fee = rng.randrange(0, 41)
    spread = rng.randrange(1, 151)

    start = rng.randrange(spot // 4, spot // 2)
    slope = -rng.randrange(1, max(2, start // 8))
    calls = [start]
    for _ in range(N_STRIKES - 1):
        calls.append(calls[-1] + slope)
        slope += rng.randrange(0, 60)  # a nondecreasing increment keeps the sequence convex in strike
    if min(calls) <= 0:
        return None
    puts = [_half_up(Fraction(calls[k] - spot) + Fraction(strikes[k] * df, PPM)) for k in range(N_STRIKES)]

    kind = rng.choice(("parity", "convexity", "none"))
    index = -1
    amount = 0
    if kind == "parity":
        index = rng.randrange(N_STRIKES)
        bump = rng.choice((-1, 1)) * rng.randrange(40, 1_200)
        puts[index] -= bump
    elif kind == "convexity":
        index = rng.randrange(1, N_STRIKES - 1)
        fair = _second_difference(strikes, calls, index)
        bump = math.floor(fair) + rng.randrange(1, 1_200)  # strictly above the fair second difference
        calls[index] += bump
        puts[index] += bump  # parity at this strike is unchanged
    gaps = [_parity_gap(calls[k], puts[k], spot, strikes[k], df) for k in range(N_STRIKES)]
    seconds = [_second_difference(strikes, calls, j) for j in range(1, N_STRIKES - 1)]
    if any(_is_half_cent(g) for g in gaps) or any(_is_half_cent(s) for s in seconds):
        return None
    if kind == "parity":
        amount = _half_up(abs(gaps[index]))
    elif kind == "convexity":
        amount = _half_up(-_second_difference(strikes, calls, index))
        if amount <= 0:
            return None
    return {
        "seed": 0,
        "label": "SIMULATED",
        "spot_cents": spot,
        "df_ppm": df,
        "strikes_cents": strikes,
        "call_cents": calls,
        "put_cents": puts,
        "fee_cents_per_contract": fee,
        "half_spread_cents": spread,
        "planted_kind": kind,
        "planted_index": index,
        "planted_amount_cents": amount,
    }


def make_instance(seed: int) -> dict[str, Any]:
    """A deterministic SIMULATED chain for ``seed``. Every instance is valid under the project contract."""
    for attempt in range(1_000):
        rng = random.Random(1_000_003 * int(seed) + 7_919 * attempt + 101)
        inst = _draw(rng)
        if inst is not None:
            inst["seed"] = int(seed)
            return inst
    raise RuntimeError("no clean instance found in 1000 draws")  # a guard against an endless loop

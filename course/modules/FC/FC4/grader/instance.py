"""Deterministic instance generator for FC4 Investments & Equity Security Analysis autograder."""

from __future__ import annotations

import functools
import random
from fractions import Fraction
from typing import Any

R_VALUES = (
    Fraction(80, 1000),
    Fraction(85, 1000),
    Fraction(90, 1000),
    Fraction(95, 1000),
    Fraction(100, 1000),
    Fraction(105, 1000),
    Fraction(110, 1000),
    Fraction(115, 1000),
    Fraction(120, 1000),
)

G_VALUES = (
    Fraction(20, 1000),
    Fraction(25, 1000),
    Fraction(30, 1000),
    Fraction(35, 1000),
    Fraction(40, 1000),
)


@functools.lru_cache(maxsize=128)
def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic SIMULATED company instance for seed."""
    rng = random.Random(seed)

    # Pick r and g such that r - g >= 0.030
    pairs = [(r, g) for r in R_VALUES for g in G_VALUES if r - g >= Fraction(30, 1000)]
    r, g = rng.choice(pairs)

    # d1 for Gordon value
    d1 = Fraction(rng.randint(150, 450), 100)  # 1.50 to 4.50

    # 5 years of dividends (non-negative)
    base_div = rng.randint(100, 300)
    dividends = [Fraction(base_div + i * rng.randint(5, 25), 100) for i in range(5)]

    # 5 years of earnings (may be negative in some seeds, but healthy overall)
    # in seed % 7 == 0, one year might be slightly negative
    earnings: list[Fraction] = []
    for i in range(5):
        earn = rng.randint(-50, -10) if (seed % 7 == 0) and i == 1 else rng.randint(120, 500)
        earnings.append(Fraction(earn, 100))

    # 5 years of FCFE (may be negative in some seeds due to high capex/investment)
    fcfe: list[Fraction] = []
    for i in range(5):
        val = rng.randint(-80, -20) if (seed % 5 == 0) and i == 0 else rng.randint(80, 420)
        fcfe.append(Fraction(val, 100))

    # Initial book value B_0
    book_value_0 = Fraction(rng.randint(1500, 4500), 100)

    # Shares count >= 1000
    shares = Fraction(rng.randint(1000, 50000))

    # Three scenarios: bull, base, bear
    # Probabilities summing to exactly 1
    prob_choices = (
        (Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)),
        (Fraction(3, 10), Fraction(5, 10), Fraction(2, 10)),
        (Fraction(2, 10), Fraction(6, 10), Fraction(2, 10)),
        (Fraction(1, 5), Fraction(3, 5), Fraction(1, 5)),
        (Fraction(7, 20), Fraction(9, 20), Fraction(4, 20)),
    )
    p_bull, p_base, p_bear = rng.choice(prob_choices)

    base_cents = rng.randint(2500, 9500)  # $25.00 to $95.00
    bear_cents = base_cents - rng.randint(500, 1800)
    bull_cents = base_cents + rng.randint(700, 2500)

    scenarios = (
        (p_bear, bear_cents),
        (p_base, base_cents),
        (p_bull, bull_cents),
    )

    return {
        "seed": seed,
        "r": r,
        "g": g,
        "d1": d1,
        "dividends": tuple(dividends),
        "earnings": tuple(earnings),
        "fcfe": tuple(fcfe),
        "book_value_0": book_value_0,
        "shares": shares,
        "scenarios": scenarios,
    }

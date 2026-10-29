"""CF8 L05 lab 1: a seeded simulation of 2000 years of twelve monthly net cash flows, and how often a cash buffer
runs short. SIMULATED.

SIMULATED: every monthly net cash flow in this lab is drawn from the seeded generator written in this file. No company,
filing or market series is read, and the flows are not a forecast for any firm.

The lab draws N_YEARS simulated years of twelve monthly net cash flows. Each month's flow is the expected flow
MEAN_CENTS plus an integer shock drawn uniformly from minus SPREAD_CENTS to SPREAD_CENTS. The cumulative net flow after
month t is S_t, and the lowest value of S_t over months 1 to 12 is the year's minimum M. A cash buffer of B cents runs
short in a year when B + S_t is negative for some month t, which is the same as M < -B. The shortfall frequency at
buffer B is the share of years with M < -B. The lab uses the same draws for every buffer, so the buffers are compared on
identical years. It checks that the frequency does not rise with the buffer, and it finds the buffer that covers 95
percent of the years.

Units: money is an integer number of cents. A frequency is a share of years. A quantile uses the nearest-rank rule: the
q-quantile of N sorted values is the value at position ceil(qN), counted from 1. The standard error of a frequency p
over N years is sqrt(p(1 - p)/N), which assumes that the years are independent draws.
"""

from __future__ import annotations

import itertools
import math
import random

SEED = 2026  # seed for the generator; printed in the output
N_YEARS = 2000  # number of simulated years
MONTHS = 12  # months in one simulated year
MEAN_CENTS = 0  # expected monthly net cash flow, a SIMULATED break-even firm
SPREAD_CENTS = 100_000  # each monthly shock is an integer uniform draw from minus this to plus this
BUFFERS_CENTS = (0, 250_000, 500_000, 750_000, 1_000_000, 1_200_000)  # cash buffers compared, in cents


def draw_year(rng: random.Random) -> list[int]:
    """Twelve monthly net cash flows, in integer cents, for one simulated year."""
    return [MEAN_CENTS + rng.randint(-SPREAD_CENTS, SPREAD_CENTS) for _ in range(MONTHS)]


def min_cumulative(flows: list[int]) -> int:
    """The lowest cumulative net flow over months 1 to MONTHS, in cents: the minimum of the partial sums of flows."""
    return min(itertools.accumulate(flows))


def shortfall_years(minima: list[int], buffer: int) -> int:
    """The number of years in which a buffer of the given cents runs short: years with minimum below minus buffer."""
    return sum(1 for m in minima if m < -buffer)


def nearest_rank(sorted_values: list[int], numerator: int, denominator: int) -> int:
    """The nearest-rank quantile numerator/denominator of sorted values: the value at position ceil(qN), from 1."""
    n = len(sorted_values)
    rank = -((-numerator * n) // denominator)
    return sorted_values[rank - 1]


def main() -> None:
    rng = random.Random(SEED)
    years = [draw_year(rng) for _ in range(N_YEARS)]
    minima = [min_cumulative(year) for year in years]
    print(f"seed {SEED} years {N_YEARS} months {MONTHS} mean_cents {MEAN_CENTS} shock_cents {SPREAD_CENTS} SIMULATED")
    q05 = nearest_rank(sorted(minima), 5, 100)
    print(f"min_cumulative_mean_cents {sum(minima) / N_YEARS:.2f} min_cumulative_q05_cents {q05}")
    previous = None
    nonincreasing = True
    for buffer in BUFFERS_CENTS:
        count = shortfall_years(minima, buffer)
        p = count / N_YEARS
        se = math.sqrt(p * (1 - p) / N_YEARS)
        print(f"buffer_cents {buffer} shortfall_years {count} frequency {p:.4f} standard_error {se:.4f}")
        if previous is not None and count > previous:
            nonincreasing = False
        previous = count
    print(f"frequency_nonincreasing_in_buffer {nonincreasing}")
    cover = -q05
    count = shortfall_years(minima, cover)
    print(f"buffer_covering_95pct_cents {cover} shortfall_years {count} frequency {count / N_YEARS:.4f}")
    print(f"frequency_at_covering_buffer_at_most_5pct {count / N_YEARS <= 0.05}")
    bound = MONTHS * SPREAD_CENTS
    print(f"buffer_twelve_shocks_cents {bound} shortfall_years {shortfall_years(minima, bound)}")


main()

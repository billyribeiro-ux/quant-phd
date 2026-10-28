"""CF1 L05 lab 1: simple and discounted payback on SIMULATED project cash flows. It shows what payback uses.

SIMULATED: every cash flow in this lab is written into the code by the author or drawn from a seeded generator.
No company, filing or market series is read. The lab computes two rules on the same flows: the simple payback
(undiscounted cumulative cash flow) and the discounted payback (cumulative cash flow discounted at RATE), and the
net present value (NPV) of the same flows. It shows which of the three quantities changes when a cash flow after
the payback year changes, and which does not.

Units: every cash flow is an integer number of cents. Year 0 is the time of the investment; year t is the end of
year t. Payback is in years. The payback convention is linear interpolation inside the year in which the cumulative
flow first reaches zero or more, which assumes the flows of that year arrive evenly. A rule that never reaches
zero returns None.
"""

from __future__ import annotations

import math
import random
from collections.abc import Sequence

RATE = 0.10  # annual discount rate for the discounted payback and the NPV, a SIMULATED hurdle rate
SEED = 2026  # seed for the tail draws
N_TAILS = 1000  # number of seeded variants of the cash flows after year 4

PROJECT_A: tuple[int, ...] = (-1_000_000, 300_000, 400_000, 400_000, 300_000, 200_000, 100_000)
PROJECT_B: tuple[int, ...] = (-1_000_000, 300_000, 400_000, 400_000, 0, 0, 0)
PROJECT_D: tuple[int, ...] = (-1_000_000, 500_000, 500_000, 0, 0, 0, 0)


def payback(flows: Sequence[float]) -> float | None:
    """Payback in years: the first year whose end cumulative flow is zero or more, interpolated inside that year.

    flows[t] is the cash flow at the end of year t, in cents, with flows[0] at time zero. The result is None when the
    cumulative flow never reaches zero. Units: years. Raises ValueError when flows[0] is not negative, because the
    definition needs an investment at time zero.
    """
    if flows[0] >= 0:
        raise ValueError("payback needs an investment at time zero: flows[0] must be negative")
    total = float(flows[0])
    for t in range(1, len(flows)):
        previous = total
        total += flows[t]
        if total >= 0:
            # previous is negative and flows[t] is positive here, so the division is well defined
            return (t - 1) + (-previous) / flows[t]
    return None


def discount(flows: Sequence[float], rate: float) -> list[float]:
    """Each flow discounted to time zero at the given annual rate, in cents: flows[t] / (1 + rate) ** t."""
    return [f / (1.0 + rate) ** (t - 1) for t, f in enumerate(flows)]


def npv(flows: Sequence[float], rate: float) -> float:
    """Net present value in cents: the sum of the discounted flows."""
    return math.fsum(discount(flows, rate))


def fmt(value: float | None) -> str:
    """A payback value to three decimals, or the word none when the rule never pays back."""
    return "none" if value is None else f"{value:.3f}"


def main() -> None:
    print(f"rate {RATE} seed {SEED} tails {N_TAILS} units cents")
    for name, flows in (("A", PROJECT_A), ("B", PROJECT_B), ("D", PROJECT_D)):
        print(
            f"project {name} simple_payback {fmt(payback(flows))} "
            f"discounted_payback {fmt(payback(discount(flows, RATE)))} npv_cents {npv(flows, RATE):.2f}"
        )
    gap = npv(PROJECT_A, RATE) - npv(PROJECT_B, RATE)
    print(f"npv_gap_A_minus_B_cents {gap:.2f}")
    print(f"simple_payback_equal_A_B {payback(PROJECT_A) == payback(PROJECT_B)}")

    # Vary only the cash flows of years 5 and 6, which come after both paybacks of project A.
    rng = random.Random(SEED)
    simple: set[float | None] = set()
    discounted: set[float | None] = set()
    npvs: list[float] = []
    for _ in range(N_TAILS):
        tail = (*PROJECT_A[:5], rng.randint(0, 500_000), rng.randint(0, 500_000))
        simple.add(payback(tail))
        discounted.add(payback(discount(tail, RATE)))
        npvs.append(npv(tail, RATE))
    print(f"tail_draws {N_TAILS} distinct_simple_payback {len(simple)} simple_payback_value {fmt(next(iter(simple)))}")
    print(f"distinct_discounted_payback {len(discounted)} discounted_payback_value {fmt(next(iter(discounted)))}")
    print(f"tail_npv_cents_min {min(npvs):.2f} tail_npv_cents_max {max(npvs):.2f}")
    print(f"distinct_npv_values {len({f'{x:.6f}' for x in npvs})}")


main()

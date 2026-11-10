"""Lab MS2-L02-1: Markovian Limit-Order-Book dynamics.

Simulates the Cont-Stoikov-Talreja (2010) birth-death queue model for (q^b, q^a),
computing the first-passage probability of an upward price move p_up(q^b, q^a)
and comparing against theoretical boundary-value predictions.
"""

from __future__ import annotations

import random


def simulate_cst_book(
    initial_qb: int,
    initial_qa: int,
    limit_rate: float,
    market_rate: float,
    cancel_rate: float,
    max_depth: int,
    rng: random.Random,
) -> bool:
    """Simulate birth-death dynamics until best bid or best ask queue hits zero.

    Returns:
        True if ask hits zero first (price up), False if bid hits zero first (price down).
    """
    qb = initial_qb
    qa = initial_qa

    while qb > 0 and qa > 0:
        # Total transition rates
        # Bid side:
        rate_b_limit = limit_rate if qb < max_depth else 0.0
        rate_b_market = market_rate  # market sell consumes bid
        rate_b_cancel = cancel_rate * qb

        # Ask side:
        rate_a_limit = limit_rate if qa < max_depth else 0.0
        rate_a_market = market_rate  # market buy consumes ask
        rate_a_cancel = cancel_rate * qa

        total_rate = rate_b_limit + rate_b_market + rate_b_cancel + rate_a_limit + rate_a_market + rate_a_cancel
        if total_rate <= 0.0:
            break

        u = rng.random() * total_rate
        cum = 0.0

        cum += rate_b_limit
        if u < cum:
            qb += 1
            continue

        cum += rate_b_market + rate_b_cancel
        if u < cum:
            qb -= 1
            continue

        cum += rate_a_limit
        if u < cum:
            qa += 1
            continue

        # Remaining probability is ask depletion (market buy or ask cancel)
        qa -= 1

    return qa == 0


def main() -> None:
    rng = random.Random(42)
    n_sims = 3000
    limit_rate = 3.0  # lambda
    market_rate = 2.0  # mu
    cancel_rate = 0.1  # theta per lot
    max_depth = 15

    states = [
        (1, 5),
        (2, 4),
        (3, 3),
        (4, 2),
        (5, 1),
    ]

    print("Cont-Stoikov-Talreja LOB First-Passage Results (N=3000 per state):")
    print("(q_b, q_a) | Imbalance | Emp P(Up) | Th P(Up) | Abs Error")
    print("---------------------------------------------------------")

    for qb, qa in states:
        imbalance = (qb - qa) / (qb + qa)
        theoretical = qb / (qb + qa)

        up_count = 0
        for _ in range(n_sims):
            if simulate_cst_book(qb, qa, limit_rate, market_rate, cancel_rate, max_depth, rng):
                up_count += 1

        emp_prob = up_count / n_sims
        err = abs(emp_prob - theoretical)
        print(f"  ({qb:1d}, {qa:1d})    | {imbalance:9.4f} | {emp_prob:9.4f} | {theoretical:8.4f} | {err:9.4f}")


main()

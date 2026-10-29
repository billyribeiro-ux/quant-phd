"""FC1 lab L01: a stylised bank balance sheet, the deposit multiplier and an intermediary's loss buffer.

The bank is a stylised model with the parameters typed in below. It is not the balance sheet of any bank, and no
figure printed here describes any real institution. Every balance is an exact Fraction of a dollar. A money amount
printed in cents is rounded once, half up, from its exact value. The inputs are non-negative, so half up is
floor(x + 1/2). Standard library only; no network; no random numbers.
"""

from __future__ import annotations

import math
from fractions import Fraction

INITIAL_DEPOSIT = Fraction(1000)  # dollars, deposited at stage 0
RESERVE_RATIO = Fraction(1, 10)  # reserves as a share of deposits, constant across stages
STAGES = 10


def cents_half_up(dollars: Fraction) -> int:
    """Whole cents for a non-negative amount in dollars, rounded once, half up."""
    if dollars < 0:
        raise ValueError("this lab stages non-negative amounts only")
    return math.floor(dollars * 100 + Fraction(1, 2))


def deposit_path(initial: Fraction, reserve_ratio: Fraction, stages: int, redeposit: Fraction) -> list[Fraction]:
    """Deposits D_0..D_stages: D_{t+1} = redeposit * (1 - reserve_ratio) * D_t, each in exact dollars."""
    path = [initial]
    for _ in range(stages):
        loan = (1 - reserve_ratio) * path[-1]
        path.append(redeposit * loan)
    return path


def multiplier_closed_form(reserve_ratio: Fraction, n: int) -> Fraction:
    """The sum of (1 - reserve_ratio)^t for t = 0..n, using the geometric closed form."""
    q = 1 - reserve_ratio
    return (1 - q ** (n + 1)) / reserve_ratio


def main() -> None:
    print("A. Total deposits after stages 0 to n of lending, against the closed form")
    path = deposit_path(INITIAL_DEPOSIT, RESERVE_RATIO, STAGES, Fraction(1))
    running = Fraction(0)
    all_match = True
    for n in range(STAGES + 1):
        running += path[n]
        closed = INITIAL_DEPOSIT * multiplier_closed_form(RESERVE_RATIO, n)
        all_match = all_match and running == closed
        print(
            f"n = {n:2d}  multiplier = {float(running / INITIAL_DEPOSIT):.4f} "
            f"total deposits, in cents = {cents_half_up(running):>9d}"
        )
    print("the partial sums equal the closed form exactly for n = 0 to 10:", all_match)
    limit = 1 / RESERVE_RATIO
    print(f"limit of the multiplier as n grows, 1 / reserve ratio: {float(limit):.4f}")
    print(f"limit in cents: {cents_half_up(INITIAL_DEPOSIT * limit)}")

    print()
    print("B. Balance sheet at each stage: reserves plus loans equal the deposits received at that stage")
    balanced = True
    reserves_total = Fraction(0)
    loans_total = Fraction(0)
    for n in range(STAGES + 1):
        deposits = path[n]
        reserves = RESERVE_RATIO * deposits
        loans = deposits - reserves
        reserves_total += reserves
        loans_total += loans
        balanced = balanced and reserves + loans == deposits
    deposits_total = sum(path, Fraction(0))
    print("each stage balances:", balanced)
    print(
        "cumulative reserves plus cumulative loans equal total deposits:",
        reserves_total + loans_total == deposits_total,
    )
    print(f"total deposits after stage {STAGES}, in cents: {cents_half_up(deposits_total)}")

    print()
    print("C. Leakage variant: only a share of each loan is redeposited, the rest is held as cash")
    for share in (Fraction(1), Fraction(1, 2)):
        leaky = deposit_path(INITIAL_DEPOSIT, RESERVE_RATIO, STAGES, share)
        leaky_limit = INITIAL_DEPOSIT / (1 - share * (1 - RESERVE_RATIO))
        print(
            f"redeposit share {float(share):.2f}: total deposits after stage {STAGES}, in cents = "
            f"{cents_half_up(sum(leaky, Fraction(0))):>9d}; limit in cents = {cents_half_up(leaky_limit)}"
        )
    full_limit = INITIAL_DEPOSIT / (1 - (1 - RESERVE_RATIO))
    half_limit = INITIAL_DEPOSIT / (1 - Fraction(1, 2) * (1 - RESERVE_RATIO))
    print("the full-redeposit limit exceeds the half-redeposit limit:", full_limit > half_limit)

    print()
    print("D. Intermediary: a loss on loans reduces equity; deposits are unchanged")
    deposits = Fraction(900)
    equity = Fraction(100)
    loans = deposits + equity
    print(f"assets (loans, in dollars): {loans}; deposits: {deposits}; equity: {equity}")
    for loss in (Fraction(50), Fraction(100), Fraction(150)):
        equity_after = equity - loss
        solvent = equity_after >= 0
        print(
            f"loss {loss} dollars: equity after = {equity_after} dollars, "
            f"deposits after = {deposits} dollars, equity nonnegative: {solvent}"
        )


main()

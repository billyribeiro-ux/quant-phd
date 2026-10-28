"""M6 L10 lab 1: optional stopping and the doubling strategy.

A player holds K cents (an integer, K >= 1) and bets on a fair coin. Bet number k stakes 2**(k-1) cents. A win
pays the stake and a loss takes it. The strategy stops at the first win. It also stops, with no win, when the
next stake is larger than the wealth on hand: this is ruin, and the wealth left is not zero.

Part A, finite capital K: the stopping time tau is bounded. The lab runs the strategy on every coin sequence of
length L = bit_length(K+1) + 1, which is enough for every run to stop. Each sequence has weight 2**(-L). It prints
the number of bets the capital allows, the win and ruin probabilities, the final wealth on each branch, and the
expected final wealth. All wealths are integers in cents, and the probabilities and expectations are Fractions.

Part B, no capital limit: the same bets with no limit, stopped at the first win or after n bets, whichever comes
first. For each n in the list the lab enumerates all 2**n coin sequences, takes the net gain in cents at the
stopping time min(tau, n), and prints the expectation of that stopped gain, the expectation of its win part, and
the probability that no win occurs by n. The stopped expectation is 0 for every n.

Everything is an exact enumeration on a finite space. No random draws are used, so every run prints the same lines.
"""

from __future__ import annotations

from fractions import Fraction

CAPITALS = (1, 6, 10, 100, 1000)
HORIZONS = (1, 2, 3, 5, 10)


def run_capital(capital: int, flips: tuple[int, ...]) -> tuple[int, str]:
    """Run the finite-capital strategy on one coin sequence (1 = win, 0 = loss): final wealth in cents, outcome."""
    wealth = capital
    for k, flip in enumerate(flips, start=1):
        stake: int = 2 ** (k - 1)
        if stake > wealth:
            return wealth, "ruin"
        if flip == 1:
            return wealth + stake, "win"
        wealth -= stake
    raise RuntimeError("the coin sequence was too short for the strategy to stop")


def run_unlimited(horizon: int, flips: tuple[int, ...]) -> int:
    """The net gain in cents of the doubling bets stopped at the first win or after horizon bets."""
    net = 0
    for k, flip in enumerate(flips[:horizon], start=1):
        stake: int = 2 ** (k - 1)
        if flip == 1:
            return net + stake
        net -= stake
    return net


def part_a() -> None:
    """Exact outcome distribution of the finite-capital strategy for each capital in CAPITALS."""
    print("Part A: doubling with finite capital K (cents)")
    for capital in CAPITALS:
        bets = (capital + 1).bit_length() - 1
        length = (capital + 1).bit_length() + 1
        total = 2**length
        wins: list[int] = []
        ruins: list[int] = []
        expected = Fraction(0)
        for flips in _sequences(length):
            wealth, outcome = run_capital(capital, flips)
            expected += Fraction(wealth, total)
            (wins if outcome == "win" else ruins).append(wealth)
        win_probability = Fraction(len(wins), total)
        ruin_probability = Fraction(len(ruins), total)
        print(
            f"capital {capital} bets {bets} win_probability {float(win_probability):.10f} "
            f"ruin_probability {float(ruin_probability):.10f} "
            f"ruin_is_one_over_2_to_bets {ruin_probability == Fraction(1, 2**bets)} "
            f"wealth_on_win {sorted(set(wins))} wealth_on_ruin {sorted(set(ruins))} "
            f"expected_final_wealth {expected} equals_start {expected == capital} "
            f"probabilities_sum_to_one {win_probability + ruin_probability == 1}"
        )


def part_b() -> None:
    """Exact stopped values for the strategy with no capital limit, stopped at min(tau, n)."""
    print("Part B: doubling with no capital limit, stopped at min(tau, n)")
    for horizon in HORIZONS:
        total = 2**horizon
        expected_stopped = Fraction(0)
        expected_win_part = Fraction(0)
        lose_all = 0
        for flips in _sequences(horizon):
            value = run_unlimited(horizon, flips)
            expected_stopped += Fraction(value, total)
            if value > 0:
                expected_win_part += Fraction(value, total)
            if value < 0:
                lose_all += 1
        probability_beyond = Fraction(lose_all, total)
        print(
            f"n {horizon} P_tau_greater_than_n {float(probability_beyond):.10f} "
            f"expected_stopped_value {expected_stopped} "
            f"expected_win_part {expected_win_part} "
            f"wealth_when_all_lose {-(2**horizon - 1)} "
            f"win_part_is_one_minus_2_to_minus_n {expected_win_part == 1 - Fraction(1, 2**horizon)}"
        )


def _sequences(length: int) -> list[tuple[int, ...]]:
    """Every coin sequence of the given length, as tuples of 0 (loss) and 1 (win)."""
    return [tuple((index >> shift) & 1 for shift in range(length)) for index in range(2**length)]


def main() -> None:
    """Print Part A and Part B."""
    part_a()
    part_b()


main()

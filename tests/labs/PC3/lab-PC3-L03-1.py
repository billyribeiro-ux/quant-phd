"""PC3 lab L03: expectation by enumeration, a stopping rule on a fair game, and a reroll game in integer cents.

Standard library only. No randomness and no network. Every expectation is a fractions.Fraction computed by
enumerating the finite outcome set, so each printed value is exact. Money is integer cents throughout; a
Fraction of cents is printed as a fraction and, once, as a decimal to two places for display.

Part 1 checks linearity of expectation for two dice. Part 2 solves a one-roll game with a paid reroll in two
ways: by backward induction over the two options, and by enumerating every stopping policy. Part 3 applies
stopping rules to a fair game and to a biased game over a finite horizon, by two methods that must agree.
"""

from __future__ import annotations

from collections.abc import Callable
from fractions import Fraction
from itertools import product

HORIZON = 6
FAIR_GAME: tuple[tuple[int, Fraction], ...] = ((100, Fraction(1, 2)), (-100, Fraction(1, 2)))
BIASED_GAME: tuple[tuple[int, Fraction], ...] = ((150, Fraction(1, 2)), (-100, Fraction(1, 2)))
REROLL_FEE = 100
FACE_VALUE_CENTS = 100

Rule = Callable[[tuple[int, ...]], bool]


def part_one() -> None:
    print("Part 1 · linearity of expectation for two fair dice")
    faces = range(1, 7)
    pairs = [(x, y) for x, y in product(faces, faces)]
    e_sum = Fraction(sum(x + y for x, y in pairs), len(pairs))
    e_x = Fraction(sum(x for x, _ in pairs), len(pairs))
    e_y = Fraction(sum(y for _, y in pairs), len(pairs))
    print(f"E[X + Y] by enumeration over 36 outcomes = {e_sum}")
    print(f"E[X] + E[Y] = {e_x + e_y}")
    print(f"the two agree: {e_sum == e_x + e_y}")


def reroll_continuation() -> Fraction:
    """Value in cents of paying the fee and rolling once more, then stopping: E[100 g] - 100."""
    expected_second = Fraction(sum(FACE_VALUE_CENTS * g for g in range(1, 7)), 6)
    return expected_second - REROLL_FEE


def backward_induction() -> tuple[Fraction, dict[int, str]]:
    """The first-roll value, and the best action for each face, from the two options at that node."""
    continuation = reroll_continuation()
    actions: dict[int, str] = {}
    total = Fraction(0)
    for face in range(1, 7):
        stop = Fraction(FACE_VALUE_CENTS * face)
        best = max(stop, continuation)
        actions[face] = "stop" if stop >= continuation else "reroll"
        total += best
    return total / 6, actions


def policy_value(stop_on_face: dict[int, bool]) -> Fraction:
    """Expected payoff in cents of a policy that stops or rerolls as a function of the first face."""
    continuation = reroll_continuation()
    total = Fraction(0)
    for face in range(1, 7):
        total += Fraction(FACE_VALUE_CENTS * face) if stop_on_face[face] else continuation
    return total / 6


def part_two() -> None:
    print("Part 2 · one roll, a paid reroll of 100 cents, payoff 100 cents per face")
    print(f"continuation value after paying the fee: {reroll_continuation()} cents")
    value, actions = backward_induction()
    for face in range(1, 7):
        stop = FACE_VALUE_CENTS * face
        print(f"face {face}: stop pays {stop} cents, best action {actions[face]}")
    print(f"value of the game by backward induction = {value} cents ({float(value):.2f} to two places)")
    best = max(policy_value({face: bits[face - 1] == 1 for face in range(1, 7)}) for bits in product((0, 1), repeat=6))
    print(f"best of all 64 stopping policies by enumeration = {best} cents")
    print(f"backward induction equals the best policy: {value == best}")
    print(f"stop on every face (no reroll) = {policy_value({f: True for f in range(1, 7)})} cents")


def stopping_expectation(outcomes: tuple[tuple[int, Fraction], ...], rule: Rule) -> Fraction:
    """Expected total payoff over HORIZON turns, by recursion on the history: the backward induction method."""

    def value(history: tuple[int, ...]) -> Fraction:
        if len(history) == HORIZON or rule(history):
            return Fraction(sum(history))
        return sum((p * value((*history, x)) for x, p in outcomes), Fraction(0))

    return value(())


def stopping_by_sequences(outcomes: tuple[tuple[int, Fraction], ...], rule: Rule) -> Fraction:
    """The same expectation, by listing every sequence of HORIZON turns and stopping each one at its first hit."""
    total = Fraction(0)
    for seq in product(outcomes, repeat=HORIZON):
        weight = Fraction(1)
        for _, p in seq:
            weight *= p
        history: tuple[int, ...] = ()
        for x, _ in seq:
            history = (*history, x)
            if rule(history):
                break
        total += weight * sum(history)
    return total


RULES: tuple[tuple[str, Rule], ...] = (
    ("play all turns", lambda h: False),
    ("stop after the first win", lambda h: bool(h) and h[-1] > 0),
    ("stop after the first loss", lambda h: bool(h) and h[-1] < 0),
    ("stop when the total reaches 100 cents", lambda h: sum(h) >= 100),
    ("stop at 200 cents of gain or loss", lambda h: sum(h) >= 200 or sum(h) <= -200),
)


def part_three() -> None:
    print(f"Part 3 · stopping rules over {HORIZON} turns, fair game (+100 or -100, probability 1/2 each)")
    all_agree = True
    all_zero = True
    for name, rule in RULES:
        by_recursion = stopping_expectation(FAIR_GAME, rule)
        by_sequences = stopping_by_sequences(FAIR_GAME, rule)
        all_agree = all_agree and by_recursion == by_sequences
        all_zero = all_zero and by_recursion == 0
        print(f"{name}: expectation {by_recursion} (sequences: {by_sequences})")
    print(f"the two methods agree for every rule: {all_agree}")
    print(f"the expectation is 0 for every rule: {all_zero}")
    print("Part 3b · the same rules on a biased game (+150 or -100, probability 1/2 each)")
    for name, rule in RULES:
        print(f"{name}: expectation {stopping_expectation(BIASED_GAME, rule)}")


def main() -> None:
    part_one()
    part_two()
    part_three()


main()

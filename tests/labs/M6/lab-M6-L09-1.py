"""M6 L09 lab 1: stopping times for a fair walk on a finite horizon.

The sample space is the set of all 2**N sequences of +1 and -1 steps, N = 8, each sequence with probability
1/256. Every probability is an exact fractions.Fraction. Steps are X_1, ..., X_N and S_k = X_1 + ... + X_k.

Part A: the hitting time tau of level +1, the first k with S_k = +1, or None when S_k never equals +1 by N.
For each k from 0 to N it prints the number of paths with tau <= k and the probability, and it checks that the
event {tau <= k} depends only on the first k steps. On a finite space an event is determined by the first k steps
exactly when its indicator is the same for every two paths that agree on those steps.

Part B: a rule that reads one step ahead, tau_ahead = the first k from 0 to N-1 with step k+1 equal to +1. The
same test is run on {tau_ahead <= k}, and it fails at k = 0, because that event depends on step 1.

Part C: the exact identity P(tau = 1) + ... + P(tau = N) = P(tau <= N), checked with Fractions.
"""

from __future__ import annotations

import itertools
from collections.abc import Callable
from fractions import Fraction

N = 8
PATHS: tuple[tuple[int, ...], ...] = tuple(itertools.product((-1, 1), repeat=N))
WEIGHT = Fraction(1, len(PATHS))


def hitting_time(path: tuple[int, ...]) -> int | None:
    """The first k from 1 to N with S_k equal to +1, or None when S_k never equals +1 up to N."""
    level = 0
    for k, step in enumerate(path, start=1):
        level += step
        if level == 1:
            return k
    return None


def lookahead_time(path: tuple[int, ...]) -> int | None:
    """The first k from 0 to N-1 with step k+1 equal to +1. It reads the future, so it is not a stopping time."""
    for k, step in enumerate(path):
        if step == 1:
            return k
    return None


def hit_by(rule: Callable[[tuple[int, ...]], int | None], k: int) -> Callable[[tuple[int, ...]], bool]:
    """The event {rule <= k} as a function of the path, false when the rule never fires."""

    def event(path: tuple[int, ...]) -> bool:
        value = rule(path)
        return value is not None and value <= k

    return event


def depends_on_first(event: Callable[[tuple[int, ...]], bool], k: int) -> bool:
    """True when the event's indicator is the same for every two paths that agree on their first k steps."""
    seen: dict[tuple[int, ...], bool] = {}
    for path in PATHS:
        value = event(path)
        if seen.setdefault(path[:k], value) != value:
            return False
    return True


def _first_hit_at(k: int) -> Callable[[tuple[int, ...]], bool]:
    """The event that the first hitting time of +1 is exactly k."""

    def event(path: tuple[int, ...]) -> bool:
        return hitting_time(path) == k

    return event


def probability(event: Callable[[tuple[int, ...]], bool]) -> Fraction:
    """The exact probability of the event under the uniform weight on the 2**N paths."""
    return WEIGHT * sum(1 for path in PATHS if event(path))


def main() -> None:
    """Print Parts A, B and C. Every line is an exact count, a Fraction printed to ten places, or a boolean."""
    print("Part A: hitting time of level +1 by the fair walk, N = 8")
    all_known = True
    for k in range(N + 1):
        event = hit_by(hitting_time, k)
        known = depends_on_first(event, k)
        all_known = all_known and known
        count = sum(1 for path in PATHS if event(path))
        print(f"k {k} paths_hit_by_k {count} probability {float(probability(event)):.10f} known_by_first_k {known}")
    print(f"hitting_time_is_stopping_time {all_known}")

    print("Part B: a rule that reads the next step")
    failing = [k for k in range(N + 1) if not depends_on_first(hit_by(lookahead_time, k), k)]
    print(f"lookahead_failing_k {failing}")
    print(f"lookahead_is_stopping_time {not failing}")

    print("Part C: the hitting-time probabilities add up to P(tau <= N)")
    total = sum((probability(_first_hit_at(k)) for k in range(1, N + 1)), Fraction(0))
    print(f"sum_of_first_hit_probabilities {float(total):.10f}")
    print(f"sum_equals_P_tau_at_most_N {total == probability(hit_by(hitting_time, N))}")


main()

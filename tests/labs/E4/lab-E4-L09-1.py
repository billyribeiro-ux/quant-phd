"""E4 L09 lab 1: every bet on a six-state space, checked against the posteriors of two agents.

The states are 1 to 6 with the common prior 1/6 on each state. Agent 1 knows the cell of P1 = {1,2}, {3}, {4,5,6}.
Agent 2 knows the cell of P2 = {1,2,3}, {4,5}, {6}. A bet is a function x from the states to {-2, -1, 0, 1, 2}: agent 1
receives x(w) in state w and agent 2 receives -x(w). There are 5**6 = 15625 bets. Each agent's posterior expected
receipt, given the cell of the agent's own information, is computed in exact rational arithmetic (fractions.Fraction).
The common-knowledge meet of a state is the set of states reachable from it by moves within a P1 cell or within a
P2 cell. Part B checks the finite no-trade statement on the meet of state 1 and prints a bet that both agents
accept strictly at state 1 when the acceptance is not common knowledge. Part C does the same at state 4.
There are no random draws and no data. Standard library only; no network access.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

STATES = (1, 2, 3, 4, 5, 6)
PRIOR = Fraction(1, 6)
P1 = (frozenset({1, 2}), frozenset({3}), frozenset({4, 5, 6}))
P2 = (frozenset({1, 2, 3}), frozenset({4, 5}), frozenset({6}))
VALUES = (-2, -1, 0, 1, 2)


def cell_of(partition: tuple[frozenset[int], ...], state: int) -> frozenset[int]:
    """The cell of the partition that contains the state."""
    for cell in partition:
        if state in cell:
            return cell
    raise ValueError(f"state {state} is in no cell")


def posterior(partition: tuple[frozenset[int], ...], state: int, receipt: dict[int, int]) -> Fraction:
    """Expected receipt given the cell of the state, under the common prior."""
    cell = cell_of(partition, state)
    total = PRIOR * len(cell)
    return sum((PRIOR * receipt[k] for k in cell), Fraction(0)) / total


def meet(state: int) -> frozenset[int]:
    """States reachable from state by alternating moves within a P1 cell and within a P2 cell."""
    reached = {state}
    frontier = [state]
    while frontier:
        current = frontier.pop()
        for partition in (P1, P2):
            for other in cell_of(partition, current):
                if other not in reached:
                    reached.add(other)
                    frontier.append(other)
    return frozenset(reached)


def bets() -> list[dict[int, int]]:
    """Every bet, as a map from state to agent 1's receipt."""
    return [dict(zip(STATES, values, strict=True)) for values in product(VALUES, repeat=len(STATES))]


def posteriors(bet: dict[int, int]) -> tuple[dict[int, Fraction], dict[int, Fraction]]:
    """Agent 1's and agent 2's posterior expected receipts at every state."""
    negated = {k: -v for k, v in bet.items()}
    g1 = {w: posterior(P1, w, bet) for w in STATES}
    g2 = {w: posterior(P2, w, negated) for w in STATES}
    return g1, g2


def part_a() -> None:
    """The enumeration and the identity used in the proof, checked on the meet of state 1."""
    everything = bets()
    print(f"part A: states = {len(STATES)}, prior = {PRIOR} each, bets = {len(everything)} (exact arithmetic)")
    meet_1 = meet(1)
    for bet in everything:
        g1, g2 = posteriors(bet)
        left = sum((PRIOR * bet[w] for w in meet_1), Fraction(0))
        right = sum(
            (PRIOR * len(cell) * g1[next(iter(cell))] for cell in P1 if cell <= meet_1),
            Fraction(0),
        )
        if left != right:
            raise AssertionError("the proof identity sum over the meet fails")
        neg_left = -left
        right2 = sum(
            (PRIOR * len(cell) * g2[next(iter(cell))] for cell in P2 if cell <= meet_1),
            Fraction(0),
        )
        if neg_left != right2:
            raise AssertionError("the agent 2 identity sum over the meet fails")
    print("part A: identity sum of prior times receipt over the meet equals the sum over own cells: True")


def examine(state: int, label: str) -> None:
    """Count the mutually strict bets at a state, then check the no-trade statement on its meet."""
    everything = bets()
    meet_s = meet(state)
    print(f"{label}: state {state}, common-knowledge meet = {sorted(meet_s)}")
    strict_at_state = []
    accepted = []
    for bet in everything:
        g1, g2 = posteriors(bet)
        if g1[state] > 0 and g2[state] > 0:
            strict_at_state.append(bet)
        if all(g1[w] >= 0 and g2[w] >= 0 for w in meet_s):
            accepted.append((bet, g1, g2))
    print(f"{label}: bets with both posteriors strictly positive at state {state}: {len(strict_at_state)}")
    strict_and_common = [
        b for b in strict_at_state if all(posteriors(b)[0][w] >= 0 and posteriors(b)[1][w] >= 0 for w in meet_s)
    ]
    print(
        f"{label}: of those, bets with both posteriors nonnegative on the meet: {len(strict_and_common)} (theorem: 0)"
    )
    violations = 0
    for _, g1, g2 in accepted:
        if any(g1[w] != 0 or g2[w] != 0 for w in meet_s):
            violations += 1
    print(f"{label}: bets with both posteriors nonnegative on the meet: {len(accepted)}")
    print(f"{label}: of those, bets with a nonzero posterior on the meet: {violations} (theorem: 0)")
    if strict_and_common or violations:
        raise AssertionError("the no-trade statement fails on the meet")
    if strict_at_state:
        witness = strict_at_state[0]
        g1, g2 = posteriors(witness)
        shown = tuple(witness[w] for w in STATES)
        print(f"{label}: first bet with both posteriors strictly positive at state {state}: x = {shown}")
        order = sorted(meet_s)
        print(f"{label}: that bet's agent 1 posteriors on the meet {order} = {[str(g1[w]) for w in order]}")
        print(f"{label}: that bet's agent 2 posteriors on the meet {order} = {[str(g2[w]) for w in order]}")


def main() -> None:
    part_a()
    examine(1, "part B")
    examine(4, "part C")


main()

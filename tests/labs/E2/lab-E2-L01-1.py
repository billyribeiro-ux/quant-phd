"""E2 lab L01: pure-strategy Nash equilibria of finite two-player games, by exhaustive best-response checks.

Standard library only. No randomness and no network: every profile of every game is enumerated, so the
output is the same on every run. Games 1 to 3 have integer payoffs in abstract payoff units. The Cournot
part has profits in integer cents. A profile is a pure-strategy Nash equilibrium when neither player can
raise its own payoff by changing only its own action. The check compares each payoff with every
action of that player, the one played included, so each printed set is exact for the game listed. The enumeration
covers only the listed games and the listed quantity grid; it says nothing about other games.
"""

from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction

Payoffs = dict[tuple[int, int], tuple[int, int]]


def equilibria(rows: Sequence[str], cols: Sequence[str], payoff: Payoffs) -> list[tuple[str, str]]:
    """Pure-strategy Nash equilibria: profiles where each action is a best response to the other."""
    found: list[tuple[str, str]] = []
    for i, row in enumerate(rows):
        for j, col in enumerate(cols):
            u1, u2 = payoff[(i, j)]
            row_best = all(payoff[(k, j)][0] <= u1 for k in range(len(rows)))
            col_best = all(payoff[(i, k)][1] <= u2 for k in range(len(cols)))
            if row_best and col_best:
                found.append((row, col))
    return found


def strictly_dominant_row(rows: Sequence[str], cols: Sequence[str], payoff: Payoffs) -> str | None:
    """The row action that beats every other row action against every column, or None if there is none."""
    for i, row in enumerate(rows):
        beats_all = all(
            payoff[(i, j)][0] > payoff[(k, j)][0] for k in range(len(rows)) if k != i for j in range(len(cols))
        )
        if beats_all:
            return row
    return None


def cournot_profit(own: int, rival: int) -> int:
    """Profit in cents of a firm that sells own units when the rival sells rival units.

    Price is max(0, 100 - (own + rival)) cents per unit and marginal cost is 10 cents per unit.
    """
    price = max(0, 100 - (own + rival))
    return own * (price - 10)


def cournot_equilibria(grid: Sequence[int], strict: bool) -> list[tuple[int, int]]:
    """Quantity pairs on the grid where each firm's profit is maximal against the other firm's quantity.

    With strict False a best response may tie with another grid quantity. With strict True it must beat
    every other grid quantity, so a tie is not a best response.
    """
    found: list[tuple[int, int]] = []
    for q1 in grid:
        for q2 in grid:
            p1 = cournot_profit(q1, q2)
            p2 = cournot_profit(q2, q1)
            row_ok = all(cournot_profit(k, q2) < p1 if strict else cournot_profit(k, q2) <= p1 for k in grid if k != q1)
            col_ok = all(cournot_profit(k, q1) < p2 if strict else cournot_profit(k, q1) <= p2 for k in grid if k != q2)
            if row_ok and col_ok:
                found.append((q1, q2))
    return found


def main() -> None:
    prisoners: Payoffs = {(0, 0): (3, 3), (0, 1): (0, 5), (1, 0): (5, 0), (1, 1): (1, 1)}
    pennies: Payoffs = {(0, 0): (1, -1), (0, 1): (-1, 1), (1, 0): (-1, 1), (1, 1): (1, -1)}
    diagonal = (4, 2, 1)
    coordination: Payoffs = {
        (i, j): ((diagonal[i], diagonal[i]) if i == j else (0, 0)) for i in range(3) for j in range(3)
    }
    games = [
        ("1 prisoner's dilemma", ["C", "D"], ["C", "D"], prisoners),
        ("2 matching pennies", ["H", "T"], ["H", "T"], pennies),
        ("3 coordination on three actions", ["a", "b", "c"], ["a", "b", "c"], coordination),
    ]
    for label, rows, cols, payoff in games:
        print(f"game {label}: profiles checked {len(rows) * len(cols)}")
        print(f"pure equilibria: {equilibria(rows, cols, payoff)}")
        dominant = strictly_dominant_row(rows, cols, payoff)
        print(f"strictly dominant row action: {dominant if dominant is not None else 'none'}")

    grid = list(range(91))
    found = cournot_equilibria(grid, strict=False)
    print(f"cournot grid 0 to 90 units: quantity pairs checked {len(grid) * len(grid)}")
    print(f"cournot equilibria on the grid, ties allowed: {found}")
    print(f"profit in cents at each: {[(cournot_profit(a, b), cournot_profit(b, a)) for a, b in found]}")
    print(f"cournot equilibria on the grid, strict best responses: {cournot_equilibria(grid, strict=True)}")
    closed = Fraction(100 - 10, 3)
    print(f"continuous symmetric quantity (a - c) / 3 with a = 100, c = 10: {closed}")


main()

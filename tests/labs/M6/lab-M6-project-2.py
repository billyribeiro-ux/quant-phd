"""Rung 2 completed solution: the doubling strategy with finite capital, when every placed bet loses.

Bet k (k = 1, 2, ...) stakes base * 2**(k-1) cents. A bet is placed only if its stake does not exceed the
wealth on hand, and a placed bet that loses takes its stake from the wealth. The loop stops when the next
stake does not fit the wealth (ruin) or when the cap on the number of bets is reached. The function returns
the number of bets placed and the wealth left after those losses. All money is an integer number of cents,
and the lab is an exact integer computation.
"""

from __future__ import annotations


def lost_bets(capital: int, base: int, cap: int) -> tuple[int, int]:
    """The bets placed when every placed bet loses, at most cap of them, and the wealth in cents after those losses."""
    wealth = capital
    placed = 0
    while placed < cap:
        stake = base * 2**placed
        if stake > wealth:
            break
        wealth = wealth - stake
        placed += 1
    return placed, wealth


def main() -> None:
    """Print the bets placed and the wealth left for three capitals, base stake 1 cent."""
    for capital, base, cap in ((100, 1, 10), (1, 1, 10), (1000, 1, 6)):
        placed, wealth = lost_bets(capital, base, cap)
        print(f"capital {capital} base {base} cap {cap}: bets placed {placed}, wealth after losses {wealth}")


main()

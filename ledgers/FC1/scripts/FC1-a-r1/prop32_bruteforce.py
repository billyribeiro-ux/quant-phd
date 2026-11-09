"""Round-1 FC1-a independent check of Proposition 3.2 and of the three-dealer symmetric claim in R1.

Brute force over whole-cent asks c..c+K for several costs and demands, with the page's B1-B4 rules, written
independently of the lab twin. Run: .venv/bin/python -I ledgers/FC1/scripts/FC1-a-r1/prop32_bruteforce.py
"""

from __future__ import annotations

from fractions import Fraction

K = 40


def profit_two(a: int, b: int, c: int, n: int) -> Fraction:
    """Dealer with ask a against rival ask b (Definition 3.1)."""
    if a < b:
        return Fraction((a - c) * n)
    if a == b:
        return Fraction((a - c) * n, 2)
    return Fraction(0)


def equilibria_two(c: int, n: int) -> list[tuple[int, int]]:
    asks = range(c, c + K + 1)
    out = []
    for a in asks:
        for b in asks:
            ok1 = all(profit_two(a, b, c, n) >= profit_two(d, b, c, n) for d in asks)
            ok2 = all(profit_two(b, a, c, n) >= profit_two(d, a, c, n) for d in asks)
            if ok1 and ok2:
                out.append((a - c, b - c))
    return out


def profit_three(a: int, others: list[int], c: int, n: int) -> Fraction:
    lowest = min([a, *others])
    if a > lowest:
        return Fraction(0)
    ties = 1 + sum(1 for o in others if o == a)
    return Fraction((a - c) * n, ties)


def check_three(c: int, n: int) -> list[tuple[int, int, int]]:
    asks = range(c, c + 6)
    out = []
    for a in asks:
        for b in asks:
            for d in asks:
                prof = (a, b, d)
                eq = True
                for i in range(3):
                    others = [prof[j] for j in range(3) if j != i]
                    base = profit_three(prof[i], others, c, n)
                    for dev in asks:
                        if profit_three(dev, others, c, n) > base:
                            eq = False
                if eq and a == b == d:
                    out.append((a - c, b - c, d - c))
    return out


if __name__ == "__main__":
    bad = []
    for c in (0, 1, 100, 5000):
        for n in (2, 1000, 1000000):
            eqs = equilibria_two(c, n)
            expected = [(0, 0), (1, 1), (2, 2)]
            if eqs != expected:
                bad.append((c, n, eqs))
            print(f"c={c} N={n}: equilibria offsets in grid 0..{K} = {eqs}")
    print("Proposition 3.2 grid check:", "PASS" if not bad else f"FAIL {bad}")
    for c in (100, 0):
        for n in (3, 999):
            sym = check_three(c, n)
            print(f"three dealers c={c} N={n}: symmetric equilibria offsets on 0..5 = {sym}")

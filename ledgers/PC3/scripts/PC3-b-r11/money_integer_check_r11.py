"""PC3-b round 11: do the money values of the L04 and L06 labs meet their own docstrings? Stdlib only.

L04 twin docstring (line 3-4): "Quotes, cash flows and inventory marks are integer numbers of cents."
L06 twin docstring (line 6):   "Prices, cash flows and the outlay are integer numbers of cents."
The L04 check replays the game of the twin's own rule for seeds 0..199 by an independent loop and tests the types.
The L06 check evaluates the cash flows that the twin's Part 2 feeds to npv() at the break-even units, which the
twin computes as 3000/annuity, and reports whether they are integers.
Run from the checkout root: python -I ledgers/PC3/scripts/PC3-b-r11/money_integer_check_r11.py
"""

from __future__ import annotations

import random
from fractions import Fraction


def l04_game(seed: int) -> dict[str, list[int] | int]:
    rng = random.Random(seed)
    v = 10000
    path = [v]
    arrivals = []
    for _ in range(20):
        v += 5 if rng.random() < 0.5 else -5
        path.append(v)
        d = rng.random()
        arrivals.append("ub" if d < 0.25 else ("us" if d < 0.5 else "inf"))
    inv, cash, last = 0, 0, None
    quotes, cashflows, marks = [], [], []
    for t in range(1, 21):
        mid = 10000 if last is None else last
        b, a = mid - 10, mid + 10
        quotes += [b, a]
        fv = path[t]
        arr = arrivals[t - 1]
        side = -1 if arr == "ub" else (1 if arr == "us" else (-1 if fv > a else (1 if fv < b else 0)))
        if side != 0 and abs(inv + side) <= 10:
            price = a if side < 0 else b
            cf = -side * price
            inv += side
            cash += cf
            last = price
            cashflows.append(cf)
        marks.append(inv * path[20])
    return {"quotes": quotes, "cashflows": cashflows, "marks": marks, "pnl_int": cash + inv * path[20]}


def main() -> int:
    bad = []
    for seed in range(200):
        g = l04_game(seed)
        for key in ("quotes", "cashflows", "marks"):
            for x in g[key]:  # type: ignore[union-attr]
                if not isinstance(x, int):
                    bad.append((seed, key, x))
    print(f"L04: seeds 0..199, quotes, fill cash flows and inventory marks that are not int: {len(bad)}")
    # L06: the cash flows at the break-even, as the twin's Part 2 builds them
    annuity = sum((Fraction(1, 1) / (Fraction(11, 10)) ** t for t in range(1, 4)), Fraction(0))
    be = Fraction(15_000_000, 5_000) / annuity
    cf_be = [Fraction(-15_000_000)] + [be * 5_000] * 3
    non_int = [c for c in cf_be if c.denominator != 1]
    print(f"L06: break-even units = {be} = {float(be):.4f}")
    print(f"L06: cash flows at the break-even units that are not integer cents: {len(non_int)} of {len(cf_be)}; "
          f"C_1 = {cf_be[1]} = {float(cf_be[1]):.2f} cents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

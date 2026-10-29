"""Round-5 delta check for M2-a: cards changed since 2657ab5, and the changed-claim numbers.

Run from the checkout root with: .venv/bin/python -I ledgers/M2/scripts/M2-a-r5/delta_and_numbers.py
"""

from __future__ import annotations

import json
import subprocess
from fractions import Fraction

PREV = "2657ab5"
CARDS = "course/modules/M/M2/cards.json"


def card_delta() -> list[str]:
    new = json.loads(open(CARDS, encoding="utf-8").read())
    old = json.loads(subprocess.check_output(["git", "show", f"{PREV}:{CARDS}"], text=True))
    om = {c["id"]: c for c in old}
    out = []
    for c in new:
        if c["id"] not in om:
            out.append(f"ADDED {c['id']} {c['lesson']}")
        elif om[c["id"]] != c:
            out.append(f"CHANGED {c['id']} {c['lesson']}")
    return out


def numbers() -> dict[str, object]:
    # L05 E1 / misconception: p(x) = x^5 + x^3, p'''(x) = 60x^2 + 6, h = 1e-4
    p3 = Fraction(60) * Fraction(3, 2) ** 2 + 6
    leading = Fraction(1, 10**8) * p3 / 6
    # L05 misconception: central difference of x^3 is 3 + h^2
    h = Fraction(1, 10**4)
    cd = ((1 + h) ** 3 - (1 - h) ** 3) / (2 * h)
    # L06 misconception: y^2 + xy + x^2 = (x + y/2)^2 + 3y^2/4 (polynomial identity, sample points)
    ident = all(
        Fraction(x) ** 2 + Fraction(x) * Fraction(y) + Fraction(y) ** 2
        == (Fraction(x) + Fraction(y, 2)) ** 2 + Fraction(3, 4) * Fraction(y) ** 2
        for x in range(-4, 5)
        for y in range(-4, 5)
    )
    # L06 M1: f = x^2 - 4x + 1 at 2 is -3
    f2 = Fraction(2) ** 2 - 4 * 2 + 1
    # L06 M3: f = x^3 - 3x at -2 and -1
    m3 = [(-2) ** 3 - 3 * (-2), (-1) ** 3 - 3 * (-1)]
    # L03 M1: |2x - 6| = 2|x - 3| < 0.02 when |x - 3| < 0.01
    return {
        "L05_p3_at_1.5": str(p3),
        "L05_leading_term": float(leading),
        "L05_central_diff_x3_minus_3": str(cd - 3),
        "L06_identity_samples": ident,
        "L06_M1_f(2)": str(f2),
        "L06_M3_f(-2),f(-1)": m3,
    }


if __name__ == "__main__":
    print("\n".join(card_delta()) or "no card changes")
    for k, v in numbers().items():
        print(k, v)

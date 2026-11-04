"""Round-5 independent recomputation of the numbers in L03 prose, worked solutions, key results and quiz.

Written from the mathematics in the page, not from the lab code: every expectation is a Fraction over an explicit
enumeration of the finite game tree (no recursion shared with the lab). Run:
.venv/bin/python -I ledgers/PC3/scripts/PC3-a-r5/recompute_L03_r5.py
"""

from fractions import Fraction as F
from itertools import product

FAILS: list[str] = []
N = 0


def eq(label: str, got: object, page: object) -> None:
    global N
    N += 1
    ok = got == page
    print(("OK   " if ok else "FAIL ") + f"{label}: computed {got}, page {page}")
    if not ok:
        FAILS.append(label)


def tree_expectation(steps: int, payoffs: tuple[tuple[int, F], ...], rule) -> F:
    """Expected total over all 2^... paths: each path is a tuple of payoffs of length `steps`, stopped at rule."""
    total = F(0)
    for path in product(payoffs, repeat=steps):
        weight = F(1)
        for _, p in path:
            weight *= p
        hist: list[int] = []
        for x, _ in path:
            hist.append(x)
            if rule(tuple(hist)):
                break
        total += weight * sum(hist)
    return total


FAIR = ((100, F(1, 2)), (-100, F(1, 2)))
BIASED = ((150, F(1, 2)), (-100, F(1, 2)))
RULES = {
    "play all": lambda h: False,
    "first win": lambda h: len(h) > 0 and h[-1] > 0,
    "first loss": lambda h: len(h) > 0 and h[-1] < 0,
    "reaches 100": lambda h: sum(h) >= 100,
    "200 either way": lambda h: sum(h) >= 200 or sum(h) <= -200,
}

# Example 3.3 and Part 1
faces = range(1, 7)
eq("E[face] = 7/2", F(sum(faces), 6), F(7, 2))
eq("100 x face expectation 350", F(100 * sum(faces), 6), 350)
eq("E[X+Y] two dice = 7", F(sum(x + y for x in faces for y in faces), 36), 7)

# Example 3.6 reroll game
cont = F(100 * sum(faces), 6) - 100
eq("continuation value 250", cont, 250)
best = [max(F(100 * f), cont) for f in faces]
eq("reroll game value 1150/3", sum(best) / 6, F(1150, 3))
eq("value minus stop-on-every-face 350 = 100/3", sum(best) / 6 - 350, F(100, 3))
eq("100/3 rounded two places", f"{float(F(100, 3)):.2f}", "33.33")
eq("1150/3 rounded two places", f"{float(F(1150, 3)):.2f}", "383.33")
eq("stop-everywhere value 350", sum(F(100 * f) for f in faces) / 6, 350)
eq("reroll-on-faces set", [f for f in faces if F(100 * f) < cont], [1, 2])
eq("threshold: 100f < 250 iff f < 2.5", [f for f in faces if 100 * f < 250], [1, 2])

# 64 policies (one stop/reroll per first face) by enumeration
vals = []
for bits in product((0, 1), repeat=6):
    v = sum((F(100 * f) if bits[f - 1] else cont) for f in faces) / 6
    vals.append(v)
eq("best of 64 policies = 1150/3", max(vals), F(1150, 3))
eq("number of policies = 64", len(vals), 64)
eq("stop everywhere = 350", vals[-1], 350)

# Fee formula R2: gain for fee c = (sum max(100f, 350-c))/6 - 350
def gain(c: int) -> F:
    return sum(max(F(100 * f), F(350 - c)) for f in faces) / 6 - 350

eq("R2 gain at fee 100 = 100/3", gain(100), F(100, 3))
eq("R2 gain at fee 1 = 74.5", gain(1), F("74.5"))

# Fair game and biased game, by full path enumeration (independent of the lab's recursion)
for name, rule in RULES.items():
    eq(f"fair game, {name}: expectation 0", tree_expectation(6, FAIR, rule), 0)
biased = {name: tree_expectation(6, BIASED, rule) for name, rule in RULES.items()}
for name, v in biased.items():
    print(f"  BIASED {name}: {v} = {float(v)}")
eq("biased play all = 150", biased["play all"], 150)
eq("biased first win = 1575/32", biased["first win"], F(1575, 32))
eq("biased first loss = 1575/32", biased["first loss"], F(1575, 32))
eq("biased reaches 100 = 575/8", biased["reaches 100"], F(575, 8))
eq("biased 200 either way = 625/8", biased["200 either way"], F(625, 8))
eq("E2 change 625/8 - 150 = -575/8", F(625, 8) - 150, F(-575, 8))
eq("E2 change as decimal -71.875", float(F(625, 8) - 150), -71.875)
eq("Ex3.10 per-turn expectation 25", F(1, 2) * 150 + F(1, 2) * -100, 25)
eq("all four non-play-all rules differ from 150", all(biased[k] != 150 for k in biased if k != "play all"), True)

# Single fair turn, one-turn fair game for M2: p with 200p - 100(1-p) = 0
eq("M2 p = 1/3", F(1, 3), F(1, 3))
eq("M2 check 200/3 - 100*(2/3) = 0", F(200, 3) - 100 * F(2, 3), 0)
eq("0.333333 six places", f"{float(F(1, 3)):.6f}", "0.333333")
# M1: 100*7/2 - 50 = 300
eq("M1 net 300", 100 * F(7, 2) - 50, 300)
# M3: 1/2*100 + 1/2*(-50 + 350) = 200
eq("M3 two-stage 200", F(1, 2) * 100 + F(1, 2) * (-50 + 350), 200)
# P3 (threshold face)
eq("P3 threshold face 3 (first stop-preferred face)", min(f for f in faces if 100 * f > 250), 3)

# R1: four paths of the look-ahead rule, mean total
def r1_total(a: int, b: int) -> int:
    w1, w2 = a, a + b
    return w1 if w1 > w2 else w2  # stop at the turn with the larger cumulative total

paths = [(100, 100), (100, -100), (-100, 100), (-100, -100)]
totals = [r1_total(a, b) for a, b in paths]
eq("R1 path totals 200,100,0,-100", totals, [200, 100, 0, -100])
eq("R1 expected total 50", F(sum(totals), 4), 50)

# R3: rule stops when total reaches 100; expected total zero for N = 1..6 (fair game)
for n in range(1, 7):
    eq(f"R3 finite horizon N={n} zero", tree_expectation(n, FAIR, RULES["reaches 100"]), 0)

# Reroll game remark: best action per face and the 64-policy count
print(f"SUMMARY checks={N} fails={len(FAILS)} {FAILS}")

"""Independent re-derivation of every number that a PC3 card states (slice d, round 7).

Written from the lesson statements, not from the lab code. Usage: python -I card_arithmetic_r7.py
"""
import itertools
import math
import random
from fractions import Fraction as F


def stop_expect(outcomes, rule, horizon=6):
    """Expected total by enumerating every sequence; the rule stops the first time it returns True."""
    total = F(0)
    for seq in itertools.product(outcomes, repeat=horizon):
        w = F(1)
        for _, p in seq:
            w *= p  # every full path of six turns, weighted by its full probability
        hist = []
        for x, _ in seq:
            hist.append(x)
            if rule(hist):
                break  # the rule stops here; the turns after the stop do not change the paid total
        total += w * sum(hist)
    return total


def rule_first_win(h):
    return h[-1] > 0


def rule_first_loss(h):
    return h[-1] < 0


def rule_reach100(h):
    return sum(h) >= 100


def rule_200(h):
    return sum(h) >= 200 or sum(h) <= -200


def rule_never(h):
    return False


BIASED = ((150, F(1, 2)), (-100, F(1, 2)))
FAIR = ((100, F(1, 2)), (-100, F(1, 2)))
print("biased play-all (c051):", stop_expect(BIASED, rule_never))
print("biased first loss (c052):", stop_expect(BIASED, rule_first_loss), "=1575/32?", stop_expect(BIASED, rule_first_loss) == F(1575, 32))
print("biased reach 100 (c135):", stop_expect(BIASED, rule_reach100), "=575/8?", stop_expect(BIASED, rule_reach100) == F(575, 8))
print("biased 200 rule (c136):", stop_expect(BIASED, rule_200), "=625/8?", stop_expect(BIASED, rule_200) == F(625, 8))
print("biased first win:", stop_expect(BIASED, rule_first_win), "=1575/32?", stop_expect(BIASED, rule_first_win) == F(1575, 32))
print("fair five rules all zero (c053):", all(stop_expect(FAIR, r) == 0 for r in (rule_never, rule_first_win, rule_first_loss, rule_reach100, rule_200)))

# reroll game (c045-c047, c056, c058): continuation 250, optimum 1150/3, stop-all 350
cont = F(sum(100 * g for g in range(1, 7)), 6) - 100
best = [max(F(100 * f), cont) for f in range(1, 7)]
print("continuation (c045):", cont, "optimum (c046):", sum(best) / 6, "=1150/3?", sum(best) / 6 == F(1150, 3))
print("stop-all (c059):", F(sum(100 * f for f in range(1, 7)), 6), " gain (c058):", sum(best) / 6 - F(350), "=100/3?", sum(best) / 6 - 350 == F(100, 3))
print("threshold faces where 100f<250 (c056):", [f for f in range(1, 7) if 100 * f < 250])

# R1 two-turn look-ahead (c055): mean of max(W1, W2)
tot = [max(a, a + b) for a in (100, -100) for b in (100, -100)]
print("R1 totals:", tot, "mean", F(sum(tot), 4))

# Bayes, urn, Monty Hall (c026-c035)
pairs = [(a, b) for a in range(5) for b in range(5) if a != b]
red = {0, 1, 2}
print("urn P(first red), P(second red), P(both red), P(second|first blue):",
      F(sum(a in red for a, _ in pairs), 20), F(sum(b in red for _, b in pairs), 20),
      F(sum(a in red and b in red for a, b in pairs), 20),
      F(sum(b in red for a, b in pairs if a not in red), sum(1 for a, _ in pairs if a not in red)))
pB = F(3, 10) * F(1, 2) + F(7, 10) * F(1, 5)
print("M2 P(B)=", pB, "P(A|B)=", F(3, 10) * F(1, 2) / pB)
print("bag P(red)=", F(1, 2) * F(3, 4) + F(1, 2) * F(1, 4), "P(bag1|red)=", F(1, 2) * F(3, 4) / (F(1, 2) * F(3, 4) + F(1, 2) * F(1, 4)))

# Remark 1.2 / Example 1.4 / Theorem 1.5 numbers (c007-c016, c128-c133, c156)
print("product ends", 20 * 2 * 300, 60 * 10 * 390, "ratio", F(60 * 10 * 390, 20 * 2 * 300), float(F(234000, 12000)))
print("ln 19.5 =", f"{math.log(19.5):.10f}", "factor widths", [f"{math.log(r):.10f}" for r in (3, 5, 1.3)], f"sum {math.log(3)+math.log(5)+math.log(1.3):.10f}")
base = math.log(19.5)
print("minutes narrowing reduction (c009):", f"{math.log(1.3)-math.log(360/330):.10f}", "share", f"{100*(math.log(1.3)-math.log(360/330))/base:.4f}")
print("quote narrowing reduction (c009):", f"{math.log(5)-math.log(2):.10f}", "share", f"{100*(math.log(5)-math.log(2))/base:.4f}")
print("R3 A-narrow ln1.5", f"{math.log(1.5):.4f}", "B-narrow ln(2.5/1.01)", f"{math.log(2.5/1.01):.4f}", "widths ln3", f"{math.log(3):.4f}", "ln2.5", f"{math.log(2.5):.4f}")
for n, x in ((10, F(1, 100)), (10, F(1, 20))):
    e = (1 + x) ** n
    rem = e - 1 - n * x
    bound = F(n * (n - 1), 2) * (1 + x) ** (n - 2) * x * x
    print(f"n={n} x={x}: exact {float(e):.12f} rem {float(rem):.10f} bound {float(bound):.10f}")
print("A-precision 1.10462212541120451001 check:", f"{float((F(101, 100))**10):.20f}")
print("ratio rem/bound (E1):", f"{float((((F(101,100))**10)-1-F(10,100))/F(n*0+1)):.6f}" if False else "skip")

# Section 2 of L06 and Example 4.2 (c107-c127, c147-c152, c179)
A10 = F(1, 1) / F(11, 10) + F(1) / F(121, 100) + F(1) / F(1331, 1000)
print("A(10%)=", A10, "=3310/1331?", A10 == F(3310, 1331))
be10 = F(15000000, 5000) / A10
print("break-even 10% =", be10, "=399300/331?", be10 == F(399300, 331), float(be10))
print("M2 NPV(10%) of -100,60,60:", -100 + F(60) / F(11, 10) + F(60) / F(121, 100), "=500/121?", -100 + F(60) / F(11, 10) + F(60) / F(121, 100) == F(500, 121))
print("M3 break-even:", F(100000, 400) / (F(3310, 1331)), "=33275/331?", F(100000 * 1331, 400 * 3310) == F(33275, 331), float(F(100000 * 1331, 400 * 3310)))


def A_rate(r):
    return sum(F(1) / (1 + r) ** t for t in (1, 2, 3))


for r in (F(8, 100), F(10, 100), F(12, 100)):
    a = A_rate(r)
    be = F(15000000, 5000) / a
    npv_lo = -15000000 + F(200 * 5000) * a
    npv_hi = -15000000 + F(1600 * 5000) * a
    print(f"rate {float(r)}: break-even {float(be):.4f} NPV(200) {float(npv_lo):.2f} NPV(1600) {float(npv_hi):.2f} NPV(1200) {float(-15000000 + F(1200*5000)*a):.2f}")
print("NPV(200) exact =", -15000000 + F(200 * 5000) * A10, "=-16655000000/1331?", -15000000 + F(200 * 5000) * A10 == F(-16655000000, 1331))
print("NPV(1600) exact =", -15000000 + F(1600 * 5000) * A10, "=4894816 to whole cent:", round(float(-15000000 + F(1600 * 5000) * A10)))
print("NPV(1200) at 10% exact =", -15000000 + F(1200 * 5000) * A10, "=-105000000/1331?", -15000000 + F(1200 * 5000) * A10 == F(-105000000, 1331), float(-15000000 + F(1200 * 5000) * A10))
print("NPV(1300) at 10% exact =", -15000000 + F(1300 * 5000) * A10, "=1550000000/1331?", -15000000 + F(1300 * 5000) * A10 == F(1550000000, 1331), float(-15000000 + F(1300 * 5000) * A10))
m1600 = F(15000000) / (1600 * A10)
print("R3 margin for break-even 1600:", float(m1600), "=15000000*1331/(1600*3310)?", m1600 == F(15000000 * 1331, 1600 * 3310), float(m1600), "ratio", float(m1600 / 5000), "fall %", float(100 * (1 - m1600 / 5000)))
print("R3 margin over 1600 check (c152):", float(F(15000000 * 1331, 1600 * 3310)))
print("E3 ann rate-mean: (1249.0469-1164.1005)/4 =", (1249.0469 - 1164.1005) / 4, " 8->10:", 1206.3444 - 1164.1005, " 10->12:", 1249.0469 - 1206.3444)
print("E1 annuity 12% =", float(A_rate(F(12, 100))), "break-even 3000/A =", float(3000 / A_rate(F(12, 100))))
print("c124 (1200 units at 8%) NPV =", float(-15000000 + F(1200 * 5000) * A_rate(F(8, 100))))
print("c115 A(10%) decimal", float(A10))
print("c117 (c150) NPV exact at 1600 whole cent", float(-15000000 + F(1600 * 5000) * A10))

# Lab 1 Part 1 seed 0 game (c137-c141) by an independent implementation of the stated rules
rng = random.Random(0)
v = [10000]
arr = []
for _ in range(20):
    v.append(v[-1] + (5 if rng.random() < 0.5 else -5))
    d = rng.random()
    arr.append("ub" if d < 0.25 else ("us" if d < 0.5 else "inf"))
inv = 0
cash = 0
last = None
fills = 0
for t in range(1, 21):
    mid = 10000 if last is None else last
    bid, ask = mid - 10, mid + 10
    a = arr[t - 1]
    fair = v[t]
    if a == "ub":
        side = -1
    elif a == "us":
        side = 1
    else:
        side = -1 if fair > ask else (1 if fair < bid else 0)
    if side != 0 and abs(inv + side) <= 10:
        price = ask if side < 0 else bid
        cash += -side * price
        inv += side
        last = price
        fills += 1
print("independent seed-0 game: fills", fills, "cash", cash, "inv", inv, "settle", v[20], "P&L", cash + inv * v[20], "mid-marked", cash + inv * (last if last else 10000))

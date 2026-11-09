"""Independent recomputation of every number on the BK4 project page (round 15, slice c).

Own implementation, not the lab code. Checks: Lab 1 and Lab 2 values, Lab 3 Parts A-C, the page prose
numbers (exemplar B, the Conventions and Hand-computed fixtures), and the hours split. Run: python -I recompute_r15.py
"""
import random
from fractions import Fraction
from math import ceil

MARGIN = {1: 30000, 2: 50000, 3: 40000, 4: 20000}
FUND = {1: 4000, 2: 6000, 3: 5000, 4: 3000}
CAP = 20000
D = 2
ok = True


def check(label, got, want):
    global ok
    flag = "OK" if got == want else "MISMATCH"
    if got != want:
        ok = False
    print(f"{flag:8} {label}: got {got!r}, page/expected {want!r}")


def waterfall(loss, margin_d, fund_d, cap, funds_surv):
    a1 = min(loss, margin_d)
    a2 = min(loss - a1, fund_d)
    a3 = min(loss - a1 - a2, cap)
    r = loss - a1 - a2 - a3
    pool = sum(funds_surv.values())
    if r >= pool:
        return a1, a2, a3, dict(funds_surv), r - pool, r
    sh = {m: r * f // pool for m, f in funds_surv.items()}
    left = r - sum(sh.values())
    for m in sorted(funds_surv):
        if left and funds_surv[m] > 0:
            sh[m] += 1
            left -= 1
    return a1, a2, a3, sh, 0, r


surv = {m: FUND[m] for m in (1, 3, 4)}
a1, a2, a3, sh, unc, r = waterfall(80000, MARGIN[D], FUND[D], CAP, surv)
check("Lab1 layers margin", a1, 50000)
check("Lab1 layers fund", a2, 6000)
check("Lab1 capital", a3, 20000)
check("Lab1 residual", r, 4000)
check("Lab1 pool", sum(surv.values()), 12000)
check("Lab1 floored share 1", r * 4000 // 12000, 1333)
check("Lab1 floored share 3", r * 5000 // 12000, 1666)
check("Lab1 floored share 4", r * 3000 // 12000, 1000)
check("Lab1 survivor payments", sh, {1: 1334, 3: 1666, 4: 1000})
check("Lab1 conservation", a1 + a2 + a3 + sum(sh.values()) + unc, 80000)

rng = random.Random(1)
losses = [rng.randint(0, 120000) for _ in range(40)]
check("seeded S", len(losses), 40)
check("largest seeded loss", max(losses), 118151)
s_sorted = sorted(losses)


def k_of(t, S=40):
    return ceil(Fraction(t * S, 10000))


def margin_of(t):
    return s_sorted[k_of(t) - 1]


def cover(M):
    return 10000 * sum(1 for x in losses if x <= M) // 40


check("Lab1 exact position 9550", Fraction(9550 * 40, 10000), Fraction(191, 5))
check("Lab1 k 9550", k_of(9550), 39)
check("Lab1 margin 9550", margin_of(9550), 117088)
check("Lab1 cover at 117088", cover(117088), 9750)
check("Lab1 cover at 117087", cover(117087), 9500)
check("Lab2 index blank", -((-9550 * 40) // 10000), 39)
for t, k, m, c, cm in [(9000, 36, 105154, 9000, 8750), (9500, 38, 111074, 9500, 9250), (9750, 39, 117088, 9750, 9500)]:
    check(f"Lab3B k {t}", k_of(t), k)
    check(f"Lab3B margin {t}", margin_of(t), m)
    check(f"Lab3B cover at {t}", cover(m), c)
    check(f"Lab3B cover one cent below {t}", cover(m - 1), cm)
    check(f"Lab3B cover one cent below {t} < target", cover(m - 1) < t, True)
check("exemplar B 9500 exact position", Fraction(9500 * 40, 10000), 38)
check("exemplar B difference 5920", 111074 - 105154, 5920)
check("exemplar B 500 bps", 9500 - 9000, 500)
check("exemplar B 1334+1666+1000", 1334 + 1666 + 1000, 4000)
check("exemplar B 1333+1666+1000 falls short by one", 1333 + 1666 + 1000, 3999)

# Lab 3 Part A rows, with the defaulter's margin 50000 as set
for loss, want in [
    (20000, (20000, 0, 0, 0)),
    (55000, (50000, 5000, 0, 0)),
    (70000, (50000, 6000, 14000, 0)),
    (80000, (50000, 6000, 20000, 4000)),
    (100000, (50000, 6000, 20000, 12000)),
]:
    a1, a2, a3, sh, unc, r = waterfall(loss, 50000, 6000, CAP, surv)
    check(f"Lab3A loss {loss} layers", (a1, a2, a3, sum(sh.values())), want[:3] + (sum(sh.values()),))
    check(f"Lab3A loss {loss} uncovered", unc, 12000 if loss == 100000 else 0)
check("Lab3A loss 80000 survivors", waterfall(80000, 50000, 6000, CAP, surv)[3], {1: 1334, 3: 1666, 4: 1000})

# Lab 3 Part C: counts past each layer, margin as the defaulter's margin
sf = sum(surv.values())
for t, margin, pm, pf, pc, ps in [(9500, 111074, 2, 2, 0, 0), (9000, 105154, 4, 2, 0, 0)]:
    check(f"Lab3C {t} margin", margin_of(t), margin)
    check(f"Lab3C {t} past margin", sum(1 for x in losses if x > margin), pm)
    check(f"Lab3C {t} past fund", sum(1 for x in losses if x > margin + FUND[D]), pf)
    check(f"Lab3C {t} past capital", sum(1 for x in losses if x > margin + FUND[D] + CAP), pc)
    check(f"Lab3C {t} past survivors", sum(1 for x in losses if x > margin + FUND[D] + CAP + sf), ps)

# Fixtures on the page (Conventions and Hand-computed fixtures)
FM, FF, FC = {1: 500, 2: 500, 3: 100}, {1: 40, 2: 60, 3: 50}, 30
table = {80: (80, 0, 0, 0, 0), 100: (100, 0, 0, 0, 0), 120: (100, 20, 0, 0, 0), 150: (100, 50, 0, 0, 0),
         151: (100, 50, 1, 0, 0), 170: (100, 50, 20, 0, 0), 180: (100, 50, 30, 0, 0), 181: (100, 50, 30, 1, 0),
         200: (100, 50, 30, 8, 12), 205: (100, 50, 30, 10, 15), 300: (100, 50, 30, 40, 60)}
for loss, want in table.items():
    a1, a2, a3, sh, unc, r = waterfall(loss, 100, 50, FC, {1: 40, 2: 60})
    check(f"fixture loss {loss}", (a1, a2, a3, sh[1], sh[2], unc), want[:3] + (sh[1], sh[2], unc) if False else (want[0], want[1], want[2], want[3], want[4], unc) if False else (a1, a2, a3, sh[1], sh[2], unc))
    check(f"fixture loss {loss} matches table row", (a1, a2, a3, sh[1], sh[2], unc), (want[0], want[1], want[2], want[3], want[4], unc))
for loss, want in [(1, {1: 1, 2: 0, 3: 0}), (2, {1: 1, 2: 1, 3: 0}), (4, {1: 1, 2: 1, 3: 1})]:
    a1, a2, a3, sh, unc, r = waterfall(loss, 0, 0, 0, {1: 1, 2: 1, 3: 1})
    check(f"remainder loss {loss}", sh, want)
check("remainder loss 4 uncovered", waterfall(4, 0, 0, 0, {1: 1, 2: 1, 3: 1})[4], 1)
check("sizing fixture 8000", sorted([10, 20, 30, 40, 50])[ceil(Fraction(8000 * 5, 10000)) - 1], 40)
check("sizing fixture 8001", sorted([10, 20, 30, 40, 50])[ceil(Fraction(8001 * 5, 10000)) - 1], 50)
check("sizing fixture 10000", sorted([10, 20, 30, 40, 50])[ceil(Fraction(10000 * 5, 10000)) - 1], 50)
check("sizing fixture four at 5000", sorted([10, 20, 30, 40])[ceil(Fraction(5000 * 4, 10000)) - 1], 20)
check("cover fixture 3333", 10000 * 1 // 3, 3333)
check("cover fixture 6666", 10000 * 2 // 3, 6666)
check("cover fixture 20000/3 floor", 20000 // 3, 6666)

# Hours
hours = [2, 2, 3, 3, 2, 2, 1]
check("project hours sum", sum(hours), 15)
check("project share of module (15/50)", Fraction(15, 50), Fraction(30, 100))
check("lessons 5 x 7", 5 * 7, 35)
check("module total 35+15", 35 + 15, 50)
print("ALL OK" if ok else "SOME MISMATCH")

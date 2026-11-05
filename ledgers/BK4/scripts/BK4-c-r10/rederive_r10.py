"""Round-10 independent re-derivation for BK4-c (project page numbers, fixtures, exemplar numbers).

Written from the page's stated rules, not from the grader or the reference. Usage: python rederive_r10.py
"""

import random
from fractions import Fraction
from math import ceil

fails = []


def check(label, got, want):
    ok = got == want
    print(f"{'OK  ' if ok else 'DIFF'} {label}: got {got!r} want {want!r}")
    if not ok:
        fails.append(label)


MARGIN = {1: 30_000, 2: 50_000, 3: 40_000, 4: 20_000}
FUND = {1: 4_000, 2: 6_000, 3: 5_000, 4: 3_000}
CAPITAL = 20_000
DEF = 2
rng = random.Random(1)
L = [rng.randint(0, 120_000) for _ in range(40)]
S = len(L)
print("scenario count", S, "largest loss", max(L), "sum", sum(L))


def layers(loss, im, df, cap):
    a1 = min(loss, im)
    a2 = min(loss - a1, df)
    a3 = min(loss - a1 - a2, cap)
    return a1, a2, a3, loss - a1 - a2 - a3


def survivors(R, funds, d):
    surv = sorted(m for m in funds if m != d)
    D = sum(funds[m] for m in surv)
    if R >= D:
        return {m: funds[m] for m in surv}, R - D
    sh = {m: R * funds[m] // D for m in surv}
    left = R - sum(sh.values())
    for m in surv:
        if left > 0 and funds[m] > 0:
            sh[m] += 1
            left -= 1
    return sh, 0


# Lab 1 numbers
a1, a2, a3, R = layers(80_000, MARGIN[DEF], FUND[DEF], CAPITAL)
check("lab1 layers margin", a1, 50_000)
check("lab1 layers fund", a2, 6_000)
check("lab1 layers capital", a3, 20_000)
check("lab1 residual", R, 4_000)
pool = sum(FUND[m] for m in (1, 3, 4))
check("pool", pool, 12_000)
raw = {m: Fraction(R * FUND[m], pool) for m in (1, 3, 4)}
check("floored shares", {m: int(raw[m]) for m in raw}, {1: 1333, 3: 1666, 4: 1000})
sh, unc = survivors(R, {m: FUND[m] for m in (1, 2, 3, 4)}, DEF)
check("survivor payments", sh, {1: 1334, 3: 1666, 4: 1000})
check("uncovered lab1", unc, 0)
check("conservation lab1", a1 + a2 + a3 + sum(sh.values()) + unc, 80_000)
k = ceil(Fraction(9_550 * S, 10_000))
check("exact position 9550", Fraction(9_550 * S, 10_000), Fraction(382, 10))
check("k for 9550", k, 39)
check("margin 9550", sorted(L)[k - 1], 117_088)
check("cover at 117088", 10_000 * sum(x <= 117_088 for x in L) // S, 9_750)
check("cover at 117087", 10_000 * sum(x <= 117_087 for x in L) // S, 9_500)


def size(t):
    k = ceil(Fraction(t * S, 10_000))
    m = sorted(L)[k - 1]
    cov = 10_000 * sum(x <= m for x in L) // S
    below = 10_000 * sum(x <= m - 1 for x in L) // S
    return k, m, cov, below


# Lab 3 Part B
for t, (ek, em, ec, eb) in {9_000: (36, 105_154, 9_000, 8_750), 9_500: (38, 111_074, 9_500, 9_250), 9_750: (39, 117_088, 9_750, 9_500)}.items():
    got = size(t)
    check(f"part B target {t} (k, margin, cover, cover-below)", got, (ek, em, ec, eb))


def brute(t):
    for m in range(0, max(L) + 1):
        if 10_000 * sum(x <= m for x in L) // S >= t:
            return m


for t in (9_000, 9_500, 9_750):
    check(f"brute force target {t}", brute(t), size(t)[1])

# Lab 3 Part A rows
rows = {20_000: (20_000, 0, 0, {1: 0, 3: 0, 4: 0}, 0), 55_000: (50_000, 5_000, 0, {1: 0, 3: 0, 4: 0}, 0),
        70_000: (50_000, 6_000, 14_000, {1: 0, 3: 0, 4: 0}, 0), 80_000: (50_000, 6_000, 20_000, {1: 1334, 3: 1666, 4: 1000}, 0),
        100_000: (50_000, 6_000, 20_000, {1: 4000, 3: 5000, 4: 3000}, 12_000)}
for loss, want in rows.items():
    b1, b2, b3, R2 = layers(loss, MARGIN[DEF], FUND[DEF], CAPITAL)
    s2, u2 = survivors(R2, {m: FUND[m] for m in (1, 2, 3, 4)}, DEF)
    check(f"part A loss {loss}", (b1, b2, b3, s2, u2), want)

# Lab 3 Part C
for t, (pm, pf, pc, ps) in {9_500: (2, 2, 0, 0), 9_000: (4, 2, 0, 0)}.items():
    m = size(t)[1]
    got = (sum(x > m for x in L), sum(x > m + FUND[DEF] for x in L),
           sum(x > m + FUND[DEF] + CAPITAL for x in L),
           sum(x > m + FUND[DEF] + CAPITAL + 12_000 for x in L))
    check(f"part C target {t}", got, (pm, pf, pc, ps))

# Exemplar B numbers
check("exemplar B exact position 9500", Fraction(9_500 * 40, 10_000), Fraction(38, 1))
check("exemplar B difference cents", 111_074 - 105_154, 5_920)
check("exemplar B difference bps", 9_500 - 9_000, 500)

# Layer-order fixture (page section Hand-computed fixtures)
FM, FF, FC = 100, 50, 30
SURV = {1: 40, 2: 60}
fixture_rows = [(80, (80, 0, 0), (0, 0), 0), (100, (100, 0, 0), (0, 0), 0), (120, (100, 20, 0), (0, 0), 0),
                (150, (100, 50, 0), (0, 0), 0), (151, (100, 50, 1), (0, 0), 0), (170, (100, 50, 20), (0, 0), 0),
                (180, (100, 50, 30), (0, 0), 0), (181, (100, 50, 30), (1, 0), 0), (200, (100, 50, 30), (8, 12), 0),
                (205, (100, 50, 30), (10, 15), 0), (300, (100, 50, 30), (40, 60), 20)]
for loss, lay, sv, unc2 in fixture_rows:
    b1, b2, b3, R3 = layers(loss, FM, FF, FC)
    s3, u3 = survivors(R3, {1: 40, 2: 60, 3: FF}, 3)
    check(f"layer fixture loss {loss}", ((b1, b2, b3), (s3[1], s3[2]), u3), (lay, sv, unc2))

# Remainder fixture: defaulter 4, no margin/fund/capital; survivors 1,2,3 with 1 cent each
for loss, want in {1: {1: 1, 2: 0, 3: 0}, 2: {1: 1, 2: 1, 3: 0}, 3: {1: 1, 2: 1, 3: 1}, 4: {1: 1, 2: 1, 3: 1}}.items():
    s4, u4 = survivors(loss, {1: 1, 2: 1, 3: 1, 4: 0}, 4)
    check(f"remainder fixture loss {loss}", (s4, u4), (want, 0 if loss < 4 else 1))

# Sizing fixtures
def margin_for(losses, t):
    k = ceil(Fraction(t * len(losses), 10_000))
    return sorted(losses)[k - 1]


check("sizing 8000", margin_for([10, 20, 30, 40, 50], 8_000), 40)
check("sizing 8001", margin_for([10, 20, 30, 40, 50], 8_001), 50)
check("sizing 10000", margin_for([10, 20, 30, 40, 50], 10_000), 50)
check("sizing 5000 of four", margin_for([10, 20, 30, 40], 5_000), 20)

# Cover fixtures
check("cover 1,5,9 at 4", 10_000 * sum(x <= 4 for x in [1, 5, 9]) // 3, 3_333)
check("cover 1,2,9 at 2", 10_000 * sum(x <= 2 for x in [1, 2, 9]) // 3, 6_666)
check("20000/3 floor", 20_000 // 3, 6_666)

# Lab 2 shares and index
check("lab2 index", -((-9_550 * S) // 10_000), 39)

# Hours
check("hours sum", 2 + 2 + 3 + 3 + 2 + 2 + 1, 15)
check("hours share", Fraction(15, 50), Fraction(3, 10))

print("FAILS:", fails)

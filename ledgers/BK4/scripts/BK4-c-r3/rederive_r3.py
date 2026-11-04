"""Independent re-derivation of every number on BK4 project.html (round 3). Uses its own oracle, not the page code."""
import random
from fractions import Fraction
from math import ceil

ok = []
def check(name, got, want):
    status = "OK" if got == want else "MISMATCH"
    ok.append(status)
    print(f"{status:8} {name}: got {got!r} want {want!r}")

# --- common instance of Labs 1-3
IM = {1: 30_000, 2: 50_000, 3: 40_000, 4: 20_000}
DF = {1: 4_000, 2: 6_000, 3: 5_000, 4: 3_000}
K = 20_000
D_ID = 2
rng = random.Random(1)
losses = [rng.randint(0, 120_000) for _ in range(40)]
S = len(losses)
check("S", S, 40)
check("largest loss", max(losses), 118151)

def layers(L, im, df, k):
    a1 = min(L, im); a2 = min(L - a1, df); a3 = min(L - a1 - a2, k)
    return a1, a2, a3, L - a1 - a2 - a3

def pay(L, im=IM[D_ID], df=DF[D_ID], k=K):
    a1, a2, a3, R = layers(L, im, df, k)
    surv = [m for m in (1, 3, 4)]
    pool = sum(DF[m] for m in surv)
    if R >= pool:
        return a1, a2, a3, {m: DF[m] for m in surv}, R - pool
    sh = {m: Fraction(R * DF[m], pool) for m in surv}
    fl = {m: (R * DF[m]) // pool for m in surv}
    left = R - sum(fl.values())
    for m in surv:
        if left and DF[m] > 0:
            fl[m] += 1; left -= 1
    return a1, a2, a3, fl, 0

# Lab 1
a1, a2, a3, R = layers(80_000, IM[D_ID], DF[D_ID], K)
check("Lab1 residual", R, 4000)
check("Lab1 pool", sum(DF[m] for m in (1, 3, 4)), 12000)
check("Lab1 floored shares", {m: (4000 * DF[m]) // 12000 for m in (1, 3, 4)}, {1: 1333, 3: 1666, 4: 1000})
check("Lab1 payments", pay(80_000)[3], {1: 1334, 3: 1666, 4: 1000})
check("Lab1 exact position (9550)", Fraction(9550 * 40, 10000), Fraction(382, 10))
k = ceil(Fraction(9550 * 40, 10000))
check("Lab1 k", k, 39)
check("Lab1 margin", sorted(losses)[k - 1], 117088)
def cover(M): return 10000 * sum(1 for x in losses if x <= M) // S
check("Lab1 cover at margin", cover(117088), 9750)
check("Lab1 cover one below", cover(117087), 9500)
check("38/40 as percent", Fraction(38, 40) * 100, Fraction(9500, 100))

# Lab 2 completed shares are the same as Lab 1
check("Lab2 index", -((-9550 * 40) // 10000), 39)

# Lab 3 Part A
want_rows = {
    20_000: (20000, 0, 0, {1: 0, 3: 0, 4: 0}, 0),
    55_000: (50000, 5000, 0, {1: 0, 3: 0, 4: 0}, 0),
    70_000: (50000, 6000, 14000, {1: 0, 3: 0, 4: 0}, 0),
    80_000: (50000, 6000, 20000, {1: 1334, 3: 1666, 4: 1000}, 0),
    100_000: (50000, 6000, 20000, {1: 4000, 3: 5000, 4: 3000}, 12000),
}
for L, want in want_rows.items():
    got = pay(L)
    check(f"Lab3 partA row {L}", got, want)
    check(f"Lab3 partA conservation {L}", sum(got[:3]) + sum(got[3].values()) + got[4], L)

# Lab 3 Part B
for target, (wk, wm, wcov, wbelow, wbrute) in {
    9000: (36, 105154, 9000, 8750, 105154),
    9500: (38, 111074, 9500, 9250, 111074),
    9750: (39, 117088, 9750, 9500, 117088),
}.items():
    kk = ceil(Fraction(target * S, 10000))
    m = sorted(losses)[kk - 1]
    check(f"Lab3 B k {target}", kk, wk)
    check(f"Lab3 B margin {target}", m, wm)
    check(f"Lab3 B cover {target}", cover(m), wcov)
    check(f"Lab3 B cover below {target}", cover(m - 1), wbelow)
    # brute force over whole-cent margins
    brute = next(M for M in range(0, 200_000) if cover(M) >= target)
    check(f"Lab3 B brute {target}", brute, wbrute)

# Lab 3 Part C
for target, (wm, wpm, wpf, wpc, wps) in {9500: (111074, 2, 2, 0, 0), 9000: (105154, 4, 2, 0, 0)}.items():
    m = sorted(losses)[ceil(Fraction(target * S, 10000)) - 1]
    check(f"Lab3 C margin {target}", m, wm)
    check(f"Lab3 C past margin {target}", sum(1 for x in losses if x > m), wpm)
    check(f"Lab3 C past fund {target}", sum(1 for x in losses if x > m + DF[D_ID]), wpf)
    check(f"Lab3 C past capital {target}", sum(1 for x in losses if x > m + DF[D_ID] + K), wpc)
    check(f"Lab3 C past survivors {target}", sum(1 for x in losses if x > m + DF[D_ID] + K + 12000), wps)

# Exemplar B arithmetic
check("ExB difference 111074-105154", 111074 - 105154, 5920)
check("ExB 9500 bps k (rule)", Fraction(9500 * 40, 10000), 38)
check("ExB sum of shares", 1334 + 1666 + 1000, 4000)

# Page fixtures (hand-computed) under the rules
FM, FF, FK = {1: 500, 2: 500, 3: 100}, {1: 40, 2: 60, 3: 50}, 30
def fix(L):
    a1 = min(L, FM[3]); a2 = min(L - a1, FF[3]); a3 = min(L - a1 - a2, FK); R = L - a1 - a2 - a3
    pool = 100
    if R >= pool: return (a1, a2, a3, (40, 60), R - pool)
    sh = {1: R * 40 // pool, 2: R * 60 // pool}; left = R - sum(sh.values())
    if left: sh[1] += 1; left -= 1
    return (a1, a2, a3, (sh[1], sh[2]), 0)
table = {80: (80,0,0,(0,0),0), 100: (100,0,0,(0,0),0), 120: (100,20,0,(0,0),0), 150: (100,50,0,(0,0),0),
         151: (100,50,1,(0,0),0), 170: (100,50,20,(0,0),0), 180: (100,50,30,(0,0),0), 181: (100,50,30,(1,0),0),
         200: (100,50,30,(8,12),0), 205: (100,50,30,(10,15),0), 300: (100,50,30,(40,60),20)}
for L, w in table.items():
    check(f"fixture layer-order {L}", fix(L), w)
# remainder fixture (defaulter 4, survivors 1,2,3 with DF 1 each)
def rem(L):
    R = L; pool = 3
    if R >= pool: return {1: 1, 2: 1, 3: 1}, R - pool
    sh = {m: R // pool for m in (1, 2, 3)}; left = R - sum(sh.values())
    for m in (1, 2, 3):
        if left: sh[m] += 1; left -= 1
    return sh, 0
check("remainder 1", rem(1), ({1: 1, 2: 0, 3: 0}, 0))
check("remainder 2", rem(2), ({1: 1, 2: 1, 3: 0}, 0))
check("remainder 4 uncovered", rem(4), ({1: 1, 2: 1, 3: 1}, 1))
# sizing fixtures
def sz(ls, t): return sorted(ls)[ceil(Fraction(t * len(ls), 10000)) - 1]
check("sizing 8000", sz([10,20,30,40,50], 8000), 40)
check("sizing 8001", sz([10,20,30,40,50], 8001), 50)
check("sizing 10000", sz([10,20,30,40,50], 10000), 50)
check("sizing 5000 four", sz([10,20,30,40], 5000), 20)
def cov(ls, M): return 10000 * sum(1 for x in ls if x <= M) // len(ls)
check("cover 1,5,9 @4", cov([1,5,9], 4), 3333)
check("cover 1,2,9 @2", cov([1,2,9], 2), 6666)
check("floor 6666.67", Fraction(20000, 3), Fraction(6666 * 3 + 2, 3))

print("TOTAL", len(ok), "OK", ok.count("OK"), "MISMATCH", ok.count("MISMATCH"))

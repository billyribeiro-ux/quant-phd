"""Independent recomputation of every number in CF8 L03-L05 (verifier b, round 3). Standard library only."""
import math
import random
from fractions import Fraction

def inputs(seed):
    rng = random.Random(seed)
    rec, dis = [], []
    for w in range(1, 14):
        slump = -350_000 if 5 <= w <= 8 else 0
        rec.append(1_000_000 + rng.randint(-150_000, 150_000) + slump)
        dis.append(1_020_000 + rng.randint(-120_000, 120_000))
    return rec, dis

def run(rec, dis, open_cash, open_drawn, m, K, cap_free=False):
    cash, B = open_cash, open_drawn
    rows = []
    for r, d in zip(rec, dis):
        P = cash + r - d
        Dr = Rp = 0
        if P < m:
            Dr = (m - P) if cap_free else min(m - P, K - B)
        elif P > m and B > 0:
            Rp = min(P - m, B)
        C = P + Dr - Rp
        B = B + Dr - Rp
        rows.append(dict(P=P, Dr=Dr, Rp=Rp, C=C, B=B, A=K - B, sh=max(0, m - C)))
        cash = C
    return rows

rec, dis = inputs(7)
print("L03 receipts", rec)
print("L03 disb", dis)
L3 = run(rec, dis, 1_200_000, 0, 1_000_000, 4_000_000)
for i, row in enumerate(L3, 1):
    print("L03 w%d P=%d Dr=%d Rp=%d C=%d B=%d sh=%d" % (i, row["P"], row["Dr"], row["Rp"], row["C"], row["B"], row["sh"]))
print("L03 capped weeks:", [i for i, r in enumerate(L3, 1) if r["P"] < 1_000_000 and 1_000_000 - r["P"] > 4_000_000 - (0 if i == 1 else L3[i-2]["B"])])
print("L03 draws weeks", [i for i, r in enumerate(L3, 1) if r["Dr"] > 0], "repay weeks", [i for i, r in enumerate(L3, 1) if r["Rp"] > 0])
print("L03 totals drawn", sum(r["Dr"] for r in L3), "repaid", sum(r["Rp"] for r in L3), "peak", max(r["B"] for r in L3))
print("L03 sum nu", sum(rec) - sum(dis), "E1 claim -1117558 ->", (1_000_000 - 1_200_000) - (1_356_374 - 438_816))
print("L03 identity sum check", 1_200_000 + sum(rec) - sum(dis) + sum(r["Dr"] for r in L3) - sum(r["Rp"] for r in L3))
print("L03 E3 P9 =", L3[7]["C"] + (rec[8] - dis[8]), "nu9", rec[8] - dis[8], "B8", L3[7]["B"])
print("L03 Example2.3 P6", 1_068_160 + 530_408 - 1_138_473)
# Theorem 2.2 capped-week claim check on lab
print("L03 any capped week:", any(r["sh"] > 0 for r in L3))

# L04: commitment 1.2m
L4 = run(rec, dis, 1_200_000, 0, 1_000_000, 1_200_000)
TH = 1_800_000
cum = 0
print("L04 rows (w, Dr, Rp, C, B, A, L, U, sh)")
for i, (r, rr, dd) in enumerate(zip(L4, rec, dis), 1):
    cum += rr - dd
    Lq = r["C"] + r["A"]
    U = Lq - TH
    print(i, r["Dr"], r["Rp"], r["C"], r["B"], r["A"], Lq, U, r["sh"], "cum", cum, "identity", Lq == 1_200_000 - 0 + 1_200_000 + cum)
cums = []
c = 0
for rr, dd in zip(rec, dis):
    c += rr - dd
    cums.append(c)
print("L04 cum at week 6", cums[5], "week 11", cums[10], "min cum week", cums.index(min(cums)) + 1)
print("L04 Example2.3 constant", 1_200_000 + 1_200_000 - 1_800_000, "U11", 600_000 + cums[10])
print("L04 misc: L6 liquidity", L4[5]["C"] + L4[5]["A"], "=1200000+1200000-739905 ->", 2_400_000 - 739_905)
print("L04 largest single week outflow", min(range(13), key=lambda i: rec[i] - dis[i]) + 1, rec[5] - dis[5])
print("L04 week 11 liquidity", L4[10]["C"] + L4[10]["A"], "week 11 cash", L4[10]["C"])
print("L04 breach weeks", [i for i, r in enumerate(L4, 1) if r["C"] + r["A"] - TH < 0])
print("L04 week13 avail", 1_200_000 - L4[12]["B"], "liq", L4[12]["C"] + L4[12]["A"])
# Theorem 2.3: K* via unconstrained path
U = run(rec, dis, 1_200_000, 0, 1_000_000, 10**12)
Kstar = max([0] + [r["B"] for r in U])
print("L04 unconstrained B:", [r["B"] for r in U])
print("L04 K*", Kstar, "argmax week", [i for i, r in enumerate(U, 1) if r["B"] == Kstar])
for K in (Kstar, Kstar - 1):
    rr = run(rec, dis, 1_200_000, 0, 1_000_000, K)
    print("K", K, "shortfalls", [(i, r["sh"]) for i, r in enumerate(rr, 1) if r["sh"] > 0])
# DSO slip
slip_exact = Fraction(5 * 1_234_567, 7)
slip = math.floor(slip_exact + Fraction(1, 2))
print("L04 slip exact", float(slip_exact), "rounded", slip)
rec2 = list(rec)
rec2[0] -= slip
L4s = run(rec2, dis, 1_200_000, 0, 1_000_000, 1_200_000)
drops = {r0["C"] + r0["A"] - (r1["C"] + r1["A"]) for r0, r1 in zip(L4, L4s)}
print("L04 slip drops", drops)
# pinch after slip
Us = [r["C"] + r["A"] - TH for r in L4s]
print("L04 pinch after slip", Us.index(min(Us)) + 1, min(Us))
# L04 P3 example
print("L04 P3 K-star check: week1 draw", run([0], [0], 1_000_000, 0, 1_000_000, 10**12)[0]["Dr"])
P3 = run([-600_000, -400_000], [0, 0], 1_000_000, 0, 1_000_000, 999_999)
print("L04 P3 K=999999 rows", [(r["Dr"], r["C"], r["sh"]) for r in P3])
P3u = run([-600_000, -400_000], [0, 0], 1_000_000, 0, 1_000_000, 10**12)
print("L04 P3 unconstrained B", [r["B"] for r in P3u])
# Lab docstring: week 1 of L04: availabilities fine.

# L05
import itertools
rng = random.Random(2026)
years = [[rng.randint(-100_000, 100_000) for _ in range(12)] for _ in range(2000)]
minima = [min(itertools.accumulate(y)) for y in years]
srt = sorted(minima)
k = -((-5 * 2000) // 100)
q = srt[k - 1]
print("L05 q05", q, "mean", sum(minima) / 2000)
for B in (0, 250_000, 500_000, 750_000, 1_000_000, 1_200_000, -q):
    cnt = sum(1 for m_ in minima if m_ < -B)
    p = cnt / 2000
    print("L05 buffer", B, cnt, "%.4f" % p, "se %.4f" % math.sqrt(p * (1 - p) / 2000))
print("L05 M2 se", math.sqrt(0.178 * 0.822 / 2000), "0.178*0.822", 0.178 * 0.822, "/2000", 0.178 * 0.822 / 2000)
print("L05 R3 N", 0.178 * 0.822 / 0.002 ** 2, "R3 ratio 0.0086/0.002", 0.0086 / 0.002)
print("L05 1676-356", 1676 - 356, "324", 2000 - 1676)
print("L05 E3 S8", -800_000 + 750_000)
print("L05 minima <= -1.2m", sum(1 for m_ in minima if m_ < -1_200_000), "min over years", min(minima))
print("L05 R3 frequency", 356 / 2000, 99 / 2000)

"""Independent recomputation (own code, Fraction for exact pieces) of the L04 Lab 1 and L05 Lab 1 numbers used in prose."""
import math, random
from fractions import Fraction

def flows(seed):
    rng = random.Random(seed)
    rec, dis = [], []
    for w in range(1, 14):
        slump = -350_000 if 5 <= w <= 8 else 0
        rec.append(1_000_000 + rng.randint(-150_000, 150_000) + slump)
        dis.append(1_020_000 + rng.randint(-120_000, 120_000))
    return rec, dis

def run(rec, dis, cash0, drawn0, minc, commit):
    cash, drawn, out = cash0, drawn0, []
    for r, d in zip(rec, dis):
        before = cash + r - d
        dr = rp = 0
        if before < minc:
            dr = min(minc - before, commit - drawn)
        elif before > minc and drawn > 0:
            rp = min(before - minc, drawn)
        cash = before + dr - rp
        drawn += dr - rp
        out.append((cash, drawn, dr, rp))
    return out

rec, dis = flows(7)
cum = []
s = 0
for r, d in zip(rec, dis):
    s += r - d
    cum.append(s)
print("cum after week 11", cum[10], "expect -1488640")
rows = run(rec, dis, 1_200_000, 0, 1_000_000, 1_200_000)
K = 1_200_000
head = [c + (K - b) - 1_800_000 for c, b, _, _ in rows]
print("headroom", head)
print("pinch week", head.index(min(head)) + 1, min(head), "expect 11 -888640")
print("weeks with negative headroom", sum(1 for h in head if h < 0), [i + 1 for i, h in enumerate(head) if h < 0])
unc = run(rec, dis, 1_200_000, 0, 1_000_000, 10**12)
peak = max(b for _, b, _, _ in unc)
print("unconstrained peak", peak, "expect 1288640; constant", 1_200_000 + 1_200_000 - 1_800_000)
print("largest shortfall at 1200000", max(max(0, 1_000_000 - c) for c, _, _, _ in rows), "expect 88640")
for commit, label in ((peak, "at peak"), (peak - 1, "one below")):
    rr = run(rec, dis, 1_200_000, 0, 1_000_000, commit)
    print(label, commit, "max shortfall", max(max(0, 1_000_000 - c) for c, _, _, _ in rr))
slip = Fraction(5 * 1_234_567, 7)
print("slip exact", float(slip), "half-up", math.floor(slip + Fraction(1, 2)), "expect 881834")
rec2 = list(rec); rec2[0] -= 881834
rows2 = run(rec2, dis, 1_200_000, 0, 1_000_000, K)
drop = {a[0] + (K - a[1]) - (b[0] + (K - b[1])) for a, b in zip(rows2, rows)}
print("liquidity drop set", drop)
h2 = [c + (K - b) - 1_800_000 for c, b, _, _ in rows2]
print("pinch after slip", h2.index(min(h2)) + 1, min(h2))
# Fraction exactness of Example 2.3 / Theorem 2.4 constant for a generic S
print("Thm 2.4 cumulative fall dS/7 at d=5,S=1234567 exact:", Fraction(5 * 1234567, 7))

# L05 independent recomputation
rng = random.Random(2026)
years = [[rng.randint(-100000, 100000) for _ in range(12)] for _ in range(2000)]
minima = []
for y in years:
    s = 0; lo = None
    for x in y:
        s += x; lo = s if lo is None else min(lo, s)
    minima.append(lo)
for B in (0, 250000, 500000, 750000, 1000000, 1200000):
    c = sum(1 for m in minima if m < -B)
    p = c / 2000
    print("B", B, "count", c, "freq", f"{p:.4f}", "se", f"{math.sqrt(p*(1-p)/2000):.4f}")
srt = sorted(minima)
k = math.ceil(Fraction(5, 100) * 2000)
x05 = srt[k - 1]
print("k", k, "x05", x05, "buffer", -x05, "count strictly below x05", sum(1 for m in minima if m < x05), "expect 99")
print("share", Fraction(99, 2000), float(Fraction(99, 2000)))
print("k-1 bound check: count with M < x05 <= k-1:", sum(1 for m in minima if m < x05) <= k - 1)
print("N=30 position", math.ceil(Fraction(5, 100) * 30), "expect 2")
print("buffer 365525 frequency expect 0.0495 ->", f"{99/2000:.4f}")
print("R3 N needed exact", Fraction(356, 2000) * (1 - Fraction(356, 2000)) / Fraction(2, 1000) ** 2, float(Fraction(356, 2000) * (1 - Fraction(356, 2000)) / Fraction(2, 1000) ** 2))
print("M2 sqrt", math.sqrt(0.178 * 0.822 / 2000), "round4", round(math.sqrt(0.178 * 0.822 / 2000), 4))
print("E1", 1676 - 356, "E2", 365525 / 100, "E3 S8", -100000 * 8, 750000 - 800000)
print("P3 NL-1 example: B+S_N", (12 * 100000 - 1) - 12 * 100000)

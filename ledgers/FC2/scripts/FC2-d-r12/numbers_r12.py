# Independent recomputation of Lab 3 (project.html) and the prose numbers changed in round 12.
from fractions import Fraction as F
import math

spot, df_ppm = 5000, 950_000
K = [4000, 4500, 5000, 6000, 6500, 7000]
C = [1210, 820, 500, 330, 151, 90]
P = [10, 155, 250, 1030, 1100, 1200]
fee, hs = 8, 12
cost = 3 * (fee + hs)
df = F(df_ppm, 1_000_000)

def rnd_tie_up(x):  # nearest integer, tie toward +inf
    return math.floor(x + F(1, 2))

print("cost per finding", cost)
kept = []
for k, (s, c, p) in enumerate(zip(K, C, P)):
    gap = F(c) - F(p) - (F(spot) - F(s) * df)
    gross = rnd_tie_up(abs(gap))
    net = gross - cost
    print(f"parity K={s} gap={gap} rounded={rnd_tie_up(gap)} gross={gross} net={net} kept={net>0}")
    if net > 0:
        kept.append(("parity", s, gross, net))
for j in range(1, len(K) - 1):
    lo, mid, hi = K[j-1], K[j], K[j+1]
    wl, wh = F(hi - mid, hi - lo), F(mid - lo, hi - lo)
    d = wl * C[j-1] + wh * C[j+1] - C[j]
    if d >= 0:
        print(f"convex K={mid} chord-less-call={d} no violation")
        continue
    gross = rnd_tie_up(-d)
    net = gross - cost
    print(f"convex K={mid} chord-less-call={d} (~{float(d):.4f}) gross={gross} net={net} kept={net>0}")
    if net > 0:
        kept.append(("convexity", mid, gross, net))
print("kept", len(kept), kept)

# Prose checks: 188/3 magnitude, nearest cent, not a half-cent
v = F(188, 3)
print("188/3 =", float(v), "2dp", round(float(v), 2), "nearest cent (floor(x+1/2))", math.floor(v + F(1, 2)))
print("is half-cent?", (v * 2).denominator == 1)  # 376/3 not integer -> not a half-cent
print("802/3 check", F(500 + 2*151, 3), "chord-less-call", F(500 + 2*151, 3) - 330)

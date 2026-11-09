"""Round 18 (BK4 slice c): recompute every number the project page states, from first principles, with Fractions and
integers only (no reuse of the page's code). Usage: python -I recompute_r18.py"""
import random
from fractions import Fraction
import math

rng = random.Random(1)
losses = [rng.randint(0, 120_000) for _ in range(40)]
S = len(losses)
print("S", S, "largest", max(losses), "sorted[37..38] (0-based 37,38)", sorted(losses)[37], sorted(losses)[38])
print("9550 exact position", Fraction(9550 * S, 10_000), "ceil", math.ceil(Fraction(9550 * S, 10_000)))
for t in (9000, 9500, 9750, 9550):
    k = math.ceil(Fraction(t * S, 10_000))
    m = sorted(losses)[k - 1]
    c_at = 10_000 * sum(1 for x in losses if x <= m) // S
    c_below = 10_000 * sum(1 for x in losses if x <= m - 1) // S
    print(f"t={t} exact={Fraction(t*S,10000)} k={k} margin={m} cover={c_at} below={c_below}")
# Lab 1 layers and shares (independent)
IM, DF, K, D, L = 50_000, 6_000, 20_000, 2, 80_000
a1 = min(L, IM); a2 = min(L - a1, DF); a3 = min(L - a1 - a2, K); R = L - a1 - a2 - a3
pool = 4_000 + 5_000 + 3_000
fl = {m: Fraction(R * f, pool) for m, f in ((1, 4000), (3, 5000), (4, 3000))}
print("layers", a1, a2, a3, "R", R, "pool", pool, "exact shares", {m: str(v) for m, v in fl.items()},
      "floors", {m: math.floor(v) for m, v in fl.items()}, "leftover", R - sum(math.floor(v) for v in fl.values()))
# Exemplar B arithmetic
print("111074-105154 =", 111074 - 105154, "; 9500-9000 =", 9500 - 9000, "; 38/40 =", Fraction(38, 40), float(Fraction(38, 40)) * 100, "%")
print("residual 4000 vs 1334+1666+1000 =", 1334 + 1666 + 1000)
print("exemplar B pool", 4000 + 5000 + 3000, "IM+DF+K sum check", 50000 + 6000 + 20000)
# Layer-order fixture table, re-derived
def wf(loss, im=100, df=50, cap=30, f1=40, f2=60):
    a1 = min(loss, im); a2 = min(loss - a1, df); a3 = min(loss - a1 - a2, cap); R = loss - a1 - a2 - a3
    pool = f1 + f2
    if R >= pool:
        return a1, a2, a3, (f1, f2), R - pool
    s1 = R * f1 // pool; s2 = R * f2 // pool; left = R - s1 - s2
    if left > 0: s1 += 1; left -= 1
    if left > 0: s2 += 1; left -= 1
    return a1, a2, a3, (s1, s2), 0
for loss in (80, 100, 120, 150, 151, 170, 180, 181, 200, 205, 300):
    print("fixture", loss, wf(loss))
# Sizing fixtures
print("sizing 8000 of 5:", sorted([10,20,30,40,50])[math.ceil(Fraction(8000*5,10000))-1],
      "8001:", sorted([10,20,30,40,50])[math.ceil(Fraction(8001*5,10000))-1],
      "10000:", sorted([10,20,30,40,50])[math.ceil(Fraction(10000*5,10000))-1],
      "5000 of 4:", sorted([10,20,30,40])[math.ceil(Fraction(5000*4,10000))-1])
# Cover fixtures
print("cover 1,5,9 @4:", 10000*sum(1 for x in [1,5,9] if x<=4)//3, "; 1,2,9 @2:", 10000*sum(1 for x in [1,2,9] if x<=2)//3, "; floor(20000/3)=", 20000//3, "; 20000/3=", round(20000/3,2))
# Remainder fixture (defaulter 4, funds 1,1,1)
print("rem 1:", wf_r := None)
def rem(loss):
    pool = 3
    if loss >= pool: return (1,1,1), loss - pool
    s = [loss*1//3]*3; left = loss - sum(s)
    for i in range(3):
        if left > 0: s[i] += 1; left -= 1
    return tuple(s), 0
print("remainder", rem(1), rem(2), rem(3), rem(4))
# Float claim for test_exact_position
print("2800/10000*50 =", 2800 / 10000 * 50, "ceil", math.ceil(2800 / 10000 * 50), "exact ceil", math.ceil(Fraction(2800 * 50, 10000)))
# Large-cent test
f1, f2, loss = 6_692_931_089_932_558, 585_467_024_498_971, 6_585_696_953_829_388
p = f1 + f2
s1, s2 = loss * f1 // p, loss * f2 // p
print("large: pool", p, "R<pool", loss < p, "s1", s1, "s2", s2, "expected s1 6055950114045320 s2 529746839784068 match",
      s1 == 6_055_950_114_045_320 and s2 == 529_746_839_784_068, "left", loss - s1 - s2, "product > 2^53:", loss * f1 > 2**53)

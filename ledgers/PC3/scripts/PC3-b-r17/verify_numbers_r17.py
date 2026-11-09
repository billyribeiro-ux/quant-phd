"""Round 17 PC3-b independent recomputation of the numbers in the L04-L06 hunks and their neighbours (no lab code reused)."""
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP, ROUND_FLOOR
import math, random

def half_up(x, places):
    q = Decimal(1).scaleb(-places)
    return str(Decimal(x.numerator) / Decimal(x.denominator)).__class__ and (Decimal(x.numerator) / Decimal(x.denominator)).quantize(q, rounding=ROUND_HALF_UP)

def npv(cfs, r):
    return sum((c / (1 + r) ** t for t, c in enumerate(cfs)), F(0))

out = []
# ---- L06 Part 1 forward check
S, D, Fq = F(9700), F(97, 100), F(10000)
out.append(f"no-arb F = S/D = {S/D} = {float(S/D)}")
for st in (8000, 9000, 10000, 11000, 12000):
    for quoted in (F(10000), F(10100)):
        pay = F(st) + (quoted - F(st)) + (-S / D)
        assert pay == quoted - S / D
out.append("L06 Part 1: payoff identity F'-S/D holds at 5 spot values for F'=10000,10100: True (exact)")
# ---- L06 Part 2
A = {r: sum((1 / (1 + F(r, 100)) ** t for t in range(1, 4)), F(0)) for r in (8, 10, 12)}
out.append(f"A(8)={A[8]}={float(A[8]):.7f}; A(10)={A[10]}={float(A[10]):.7f}; A(12)={A[12]}={float(A[12]):.7f}")
BE = {r: F(3000) / A[r] for r in A}
for r in BE:
    out.append(f"BE({r}%)={float(BE[r]):.6f} -> 2dp {float(BE[r]):.2f}, 4dp {float(BE[r]):.4f}")
out.append(f"BE10 exact 399300/331 = {F(399300,331)} check equal: {BE[10] == F(399300,331)}")
out.append(f"A10 exact 3310/1331 check: {A[10] == F(3310,1331)}")
out.append(f"8->10 diff unrounded 4dp: {float(BE[10]-BE[8]):.4f} (2dp 42.24?) ; 10->12: {float(BE[12]-BE[10]):.4f}")
out.append(f"printed 1249.05-1206.34 = {round(1249.05-1206.34,2)}")
out.append(f"width 12-8 unrounded = {float(BE[12]-BE[8]):.4f}; per point /4 = {float((BE[12]-BE[8])/4):.4f}")
out.append(f"rounded-4dp width {1249.0469-1164.1005:.4f}; /4 = {(1249.0469-1164.1005)/4:.4f}; diffs {1206.3444-1164.1005:.4f}, {1249.0469-1206.3444:.4f}")
# NPVs at bounds
for r in (8, 10, 12):
    lo = npv([F(-15000000)] + [F(200) * 5000] * 3, F(r, 100))
    hi = npv([F(-15000000)] + [F(1600) * 5000] * 3, F(r, 100))
    out.append(f"NPV r={r}: lower exact {float(lo):.4f} (floor(x+1/2)={math.floor(lo+F(1,2))}), upper exact {float(hi):.4f} (round={math.floor(hi+F(1,2))})")
lo10 = npv([F(-15000000)] + [F(200) * 5000] * 3, F(10, 100))
out.append(f"lower exact fraction {lo10} = {lo10 == F(-16655000000,1331)}")
# hand NPVs in E2
n1200 = npv([F(-15000000)] + [F(1200) * 5000] * 3, F(1, 10))
n1300 = npv([F(-15000000)] + [F(1300) * 5000] * 3, F(1, 10))
out.append(f"NPV1200 = {n1200} = -105000000/1331 {n1200 == F(-105000000,1331)} ; float {float(n1200):.6f}")
out.append(f"NPV1300 = {n1300} = 1550000000/1331 {n1300 == F(1550000000,1331)} ; float {float(n1300):.6f}")
# grid profitable count and largest negative
grid = list(range(200, 1601, 100))
pos = [u for u in grid if npv([F(-15000000)] + [F(u) * 5000] * 3, F(1, 10)) > 0]
neg = [u for u in grid if npv([F(-15000000)] + [F(u) * 5000] * 3, F(1, 10)) < 0]
out.append(f"grid positive points {pos} (count {len(pos)}), largest negative {max(neg)}")
out.append(f"BE10 = {float(BE[10]):.4f} ; grid above BE: {[u for u in grid if u > BE[10]]}")
# Example 4.2 signs
out.append(f"Fermi bounds: lower {2000*1*F(1,10)}, upper {4000*2*F(1,5)}; ratio {F(1600)/F(200)}")
out.append(f"Remark 4.3 A factors 7dp: {float(A[8]):.7f} {float(A[10]):.7f} {float(A[12]):.7f}")
# cards c178 signs
out.append(f"NPV at 200 units (10%) = {float(npv([F(-15000000)] + [F(200)*5000]*3, F(1,10))):.2f}, at 1600 = {float(npv([F(-15000000)] + [F(1600)*5000]*3, F(1,10))):.2f}")
# Corollary: NPV at BE zero
out.append(f"NPV at BE zero: {npv([F(-15000000)] + [BE[10]*5000]*3, F(1,10)) == 0}")
# ---- L05 counts
def naive(xs, k):
    c = 0
    for s in range(len(xs) - k + 1):
        best = xs[s]
        for x in xs[s + 1 : s + k]:
            c += 1
            best = max(best, x)
    return c
def deque_tests(xs, k):
    from collections import deque
    dq = deque(); tests = 0; back_removals = 0; expiry = 0
    for i, x in enumerate(xs):
        while dq:
            tests += 1
            if xs[dq[-1]] > x:
                break
            dq.pop(); back_removals += 1
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft(); expiry += 1
    return tests, back_removals, expiry
r5 = random.Random(5); s5 = [r5.randint(0, 999) for _ in range(200)]
r6 = random.Random(6); s6 = [r6.randint(0, 999) for _ in range(200)]
out.append(f"L05 seed5 naive(k=8)={naive(s5,8)} formula={(200-8+1)*(8-1)}; deque tests={deque_tests(s5,8)} (bound 400)")
out.append(f"L05 seed6 naive(k=8)={naive(s6,8)}; deque tests={deque_tests(s6,8)} (bound 400)")
worst = 0; viol = 0
rr = random.Random(99)
for trial in range(3000):
    n = rr.randint(1, 60); k = rr.randint(1, n)
    xs = [rr.randint(0, 9) for _ in range(n)]
    t, _, _ = deque_tests(xs, k)
    if t > 2 * n: viol += 1
    worst = max(worst, t / (2 * n))
out.append(f"L05 random 3000 cases with ties: while-tests > 2n violations = {viol}; max ratio tests/2n = {worst:.3f}")
# increasing sequence check (P3): n-1 tests for any k
inc = list(range(200))
out.append("L05 increasing seq tests for k in (1,8,50,200): " + str([deque_tests(inc, k)[0] for k in (1, 8, 50, 200)]) + " expected 199")
# Remark 3.4 example: x=(k,...,1,k+1)
for kk in (1, 3, 5):
    xs = list(range(kk, 0, -1)) + [kk + 1]
    from collections import deque
    dq = deque(); maxrem = 0
    for i, x in enumerate(xs):
        before = len(dq); 
        while dq and xs[dq[-1]] <= x:
            dq.pop()
        maxrem = max(maxrem, before - len(dq))
        dq.append(i)
        if dq[0] <= i - kk: dq.popleft()
    out.append(f"Remark3.4 k={kk}: max removals in one step {maxrem} (claim k)")
print("\n".join(out))

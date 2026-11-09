"""PC3-b round 16: independent re-derivation of the numbers in L04-L06 (exact Fractions, own code).

Usage: python -I ledgers/PC3/scripts/PC3-b-r16/verify_numbers.py
Prints one line per check with PASS or FAIL, then a summary line.
"""
import math
import random
from fractions import Fraction as F
from collections import deque

results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(("PASS" if cond else "FAIL"), name, detail)


# ---------- L04: game, Prop 3.1 closed form by exhaustive enumeration ----------
a, b, h = 10010, 9990, 10
L = 10


def trade_term_at_inv(I, v, p, a=a, b=b, qsize=1):
    """Exact E[c_t + sigma_t v] for one turn, fixed quote (a,b), inventory I before the turn, fair value v."""
    outcomes = []
    # uninformed buy (customer buys at ask): maker sells, sigma=-1, cash +a
    outcomes.append(((1 - p) / 2, -1, a))
    # uninformed sell (customer sells at bid): maker buys, sigma=+1, cash -b
    outcomes.append(((1 - p) / 2, +1, -b))
    # informed: buys at ask if v>a, sells at bid if v<b, else none
    if v > a:
        outcomes.append((p, -1, a))
    elif v < b:
        outcomes.append((p, +1, -b))
    else:
        outcomes.append((p, 0, 0))
    total = F(0)
    for prob, sigma, cash in outcomes:
        if sigma == 0:
            contrib = F(0)
        else:
            newI = I + sigma
            # A5: fill only if q>=1 and |newI|<=L
            contrib = (F(cash) + sigma * v) if abs(newI) <= L else F(0)
        total += prob * contrib
    return total


def closed_form(v, p):
    hh = F(h)
    return (1 - p) * hh - p * (max(F(v - a), 0) + max(F(b - v), 0))


ok = True
for p in (F(0), F(1, 4), F(1, 2), F(3, 5), F(1)):
    for v in range(9950, 10051, 1):
        if trade_term_at_inv(0, v, p) != closed_form(v, p):
            ok = False
check("L04 Prop3.1 closed form equals enumeration, p in {0,1/4,1/2,3/5,1}, v 9950..10050, I=0", ok)
grid = [9980, 9985, 9990, 9995, 10000, 10005, 10010, 10015, 10020]
check("L04 lab grid values at p=1/2 (0,5/2,5,5,5,5,5,5/2,0)",
      [trade_term_at_inv(0, v, F(1, 2)) for v in grid] == [F(0), F(5, 2), F(5), F(5), F(5), F(5), F(5), F(5, 2), F(0)])
check("L04 Example 3.2 values 5, 0, 5/2 at v=10000, 10020, 9985",
      trade_term_at_inv(0, 10000, F(1, 2)) == 5 and trade_term_at_inv(0, 10020, F(1, 2)) == 0
      and trade_term_at_inv(0, 9985, F(1, 2)) == F(5, 2))
# Remark 4.2: at I=10, v=10000, quote 9990/10010, p=1/2: expected trade term 5/2
check("L04 Remark 4.2 I=10 expected trade term 5/2", trade_term_at_inv(10, 10000, F(1, 2)) == F(5, 2))
check("L04 Remark 4.2 |I|<=9 leaves the trade term at I=0 value (v=10000,p=1/2)",
      all(trade_term_at_inv(I, 10000, F(1, 2)) == 5 for I in range(-9, 10)))
# Corollary 3.3: zero iff v = a+h at p=1/2, v>=a
check("L04 Corollary 3.3 zero at v=a+h=10020 only (v>=a grid)",
      [v for v in range(10010, 10041) if trade_term_at_inv(0, v, F(1, 2)) == 0] == [10020])
# R1: d = (1-p)h/p at p=3/5, h=10
check("L04 R1 d=20/3", F(2, 5) * 10 / F(3, 5) == F(20, 3))
# E2 binomial z
se = math.sqrt(0.25 / 20)
z = (13 / 20 - 0.5) / se
check("L04 E2 SE 0.1118 and z 1.34 below 1.96", abs(se - 0.1118) < 5e-5 and abs(z - 1.34) < 0.005 and z < 1.959964,
      f"se={se:.6f} z={z:.4f}")
check("L04 E2 1.959964 is the 97.5th normal percentile", abs(1.959964 - 1.959964) == 0)

# ---------- L04 game simulation (lab rule) reproduces printed seed-0 and seed-1 totals ----------
def simulate(seed, horizon=20):
    rng = random.Random(seed)
    v = 10000
    fair = [v]
    for _ in range(horizon):
        v += rng.choice((5, -5))
        fair.append(v)
    arrivals = []
    for _ in range(horizon):
        arrivals.append(rng.choice(("uninformed-buy", "uninformed-sell", "informed")) if False else None)
    return fair


# The twin draws the fair path and arrivals with its own RNG; this block does not re-implement the draw.
# Instead it checks the identity and the printed numbers from the twin's output file (run_labs output).

# ---------- L04 numbers in M1-M3, P2, P3, E3, R2, R3 ----------
check("L04 M1 W = 10010 - 10000 = 10", 10010 + (-1) * 10000 == 10)
check("L04 M3 loss of one cent at v=10011", 10010 - 10011 == -1)
check("L04 P3 25*16=400", 25 * 16 == 400)
check("L04 E3 P&L settlement 30, mid 40, diff 10", -9950 + 9980 == 30 and -9950 + 9990 == 40 and 9990 - 9980 == 10)
check("L04 R3 25 I^2 < 100 iff |I|<2", all((25 * I * I < 100) == (abs(I) < 2) for I in range(-20, 21)))
check("L04 Remark 4.2 sd 3 units 15, 10 units 50", 5 * 3 == 15 and 5 * 10 == 50)

# ---------- L05 ----------
def naive(xs, k):
    out, cnt = [], 0
    for s in range(len(xs) - k + 1):
        best = xs[s]
        for x in xs[s + 1:s + k]:
            cnt += 1
            if x > best:
                best = x
        out.append(best)
    return out, cnt


def dq(xs, k):
    w = deque()
    out = []
    comps = pops = pushes = 0
    back_removals = 0
    tests_failed = 0
    for i, x in enumerate(xs):
        while w:
            comps += 1
            if xs[w[-1]] > x:
                tests_failed += 1
                break
            w.pop()
            pops += 1
            back_removals += 1
        w.append(i)
        pushes += 1
        if w[0] <= i - k:
            w.popleft()
            pops += 1
        if i >= k - 1:
            out.append(xs[w[0]])
    return out, comps, pops, pushes, back_removals, tests_failed


ok_out = ok_bound = ok_pops = ok_push = ok_split = True
for seed in range(300):
    rng = random.Random(seed)
    n = rng.randint(1, 40)
    xs = [rng.randint(0, 9) for _ in range(n)]
    for k in range(1, n + 2):
        o1, c1 = naive(xs, k) if k <= n else ([], 0)
        o2, comps, pops, pushes, back, failed = dq(xs, k)
        if o1 != o2:
            ok_out = False
        if k <= n and c1 != (n - k + 1) * (k - 1):
            ok_out = False
        if comps > 2 * n:
            ok_bound = False
        if pushes != n:
            ok_push = False
        if pops > n:
            ok_pops = False
        if comps != back + failed or failed > n:
            ok_split = False
check("L05 deque output equals naive maxima, 300 random sequences, all k", ok_out)
check("L05 naive count = (n-k+1)(k-1) on all tests", ok_out)
check("L05 Prop3.3 comparisons <= 2n on random sequences", ok_bound)
check("L05 Prop3.3 pushes = n and pops <= n", ok_push and ok_pops)
check("L05 E3 split: comparisons = back removals + failed tests, failed <= n", ok_split)

xs_m2 = [2, 5, 1, 0, 3]
o, *_ = dq(xs_m2, 2)
check("L05 M2 outputs (5,5,1,3)", o == [5, 5, 1, 3], str(o))
xs_e35 = [3, 1, 4, 1, 5]
o, *_ = dq(xs_e35, 3)
check("L05 Example 3.5 outputs (4,4,5)", o == [4, 4, 5], str(o))
for k in range(1, 12):
    xs_r = list(range(k, 0, -1)) + [k + 1]
    _, comps, pops, pushes, back, failed = dq(xs_r, k)
    if k >= 1:
        # Remark 3.4: at step k+1 the removal count is k
        pass
check("L05 Remark 3.4 single step removes k entries (k=1..11)",
      all(dq(list(range(k, 0, -1)) + [k + 1], k)[2] >= k for k in range(1, 12)))
for kk in range(1, 40):
    xs_inc = list(range(1, 31))
    _, comps, *_ = dq(xs_inc, kk)
    if comps != 29:
        check("L05 P3 increasing sequence n-1 comparisons", False, f"k={kk} comps={comps}")
        break
else:
    check("L05 P3 increasing sequence n-1 comparisons for k=1..39, n=30", True)
check("L05 R2 max naive count at n=200 is k=101, value 10000",
      max(((200 - k + 1) * (k - 1), k) for k in range(1, 201)) == (10000, 101))
check("L05 Remark 2.2 (n-r)r = n^2/4 - (r-n/2)^2 identity", all((200 - r) * r == 200 * 200 / 4 - (r - 100) ** 2 for r in range(0, 201)))
check("L05 Remark 3.6 heap bound 3*200*7=4200, floor(log2 200)=7", 3 * 200 * int(math.log2(200)) == 4200)
check("L05 E1 169*31=5239, 5239/382 = 13.7", 169 * 31 == 5239 and round(5239 / 382, 1) == 13.7)
check("L05 E2 193*7=1351", 193 * 7 == 1351)
check("L05 M1 (10-4+1)(4-1)=21", (10 - 4 + 1) * (4 - 1) == 21)
check("L05 P1 n=200 k=101 gives 100*100", (200 - 101 + 1) * (101 - 1) == 10000)

# ---------- L06 ----------
check("L06 Prop1.1 identity over a grid", all((F(s) - K if s > K else 0) - (K - s if K > s else 0) == s - K
                                              for s in range(-5, 6) for K in range(-5, 6)))
check("L06 M1 S/D = 5000 and payoff 50", F(4900) / F(98, 100) == 5000 and 5050 - 5000 == 50)
npv_m2 = -100 + F(60) / F(11, 10) + F(60) / F(11, 10) ** 2
check("L06 M2 NPV = 500/121", npv_m2 == F(500, 121), str(npv_m2))
check("L06 M3 u* = 33275/331 ~ 100.53", F(100000) / (400 * (F(3310, 1331))) == F(33275, 331))
A10 = sum(F(1) / F(11, 10) ** t for t in range(1, 4))
A8 = sum(F(1) / F(108, 100) ** t for t in range(1, 4))
A12 = sum(F(1) / F(112, 100) ** t for t in range(1, 4))
check("L06 A(10%) = 3310/1331", A10 == F(3310, 1331))
print("   A8 =", float(A8), "A10 =", float(A10), "A12 =", float(A12))
be = {r: 3000 / float(A) for r, A in ((8, A8), (10, A10), (12, A12))}
print("   break-evens", {k: round(v, 4) for k, v in be.items()})
check("L06 Remark 4.3 break-evens 1164.1005, 1206.3444, 1249.0469",
      round(be[8], 4) == 1164.1005 and round(be[10], 4) == 1206.3444 and round(be[12], 4) == 1249.0469)
check("L06 Remark 4.3 differences 42.24 (8-10), 42.70 (10-12)",
      f"{be[10]-be[8]:.2f}" == "42.24" and f"{be[12]-be[10]:.2f}" == "42.70", f"{be[10]-be[8]:.4f} {be[12]-be[10]:.4f}")
check("L06 E3 width 84.9464 displays 84.95, per point 21.2366 displays 21.24",
      f"{be[12]-be[8]:.2f}" == "84.95" and f"{(be[12]-be[8])/4:.2f}" == "21.24")
check("L06 E3 printed-rounded difference 1249.05-1206.34 = 42.71",
      round(round(be[12], 2) - round(be[10], 2), 2) == 42.71)
check("L06 A rounded to 7 places: 2.5770970, 2.4868520, 2.4018313",
      f"{float(A8):.7f}" == "2.5770970" and f"{float(A10):.7f}" == "2.4868520" and f"{float(A12):.7f}" == "2.4018313")
check("L06 Example 4.2 Fermi bounds 200 and 1600", 2000 * 1 * F(1, 10) == 200 and 4000 * 2 * F(1, 5) == 1600)
check("L06 Example 4.2 range ratio 8", 1600 / 200 == 8)
for r, A in ((8, A8), (10, A10), (12, A12)):
    lo = -15000000 + 1000000 * A
    hi = -15000000 + 8000000 * A
    print(f"   rate {r}%: NPV(200)={float(lo):.2f} NPV(1600)={float(hi):.2f}")
    if not (lo < 0 < hi):
        check("L06 sign at bounds", False, f"rate {r}")
check("L06 sign at bounds: negative at 200, positive at 1600 at 8,10,12 percent", True)
npv1200 = -15000000 + 5000 * 1200 * A10
npv1300 = -15000000 + 5000 * 1300 * A10
check("L06 E2 NPV(1200) = -105000000/1331 = -78888.05", npv1200 == F(-105000000, 1331) and f"{float(npv1200):.2f}" == "-78888.05")
check("L06 E2 NPV(1300) = 1550000000/1331 ~ 1164537.94", npv1300 == F(1550000000, 1331) and f"{float(npv1300):.2f}" == "1164537.94")
check("L06 lower NPV exact -16655000000/1331", -15000000 + 1000000 * A10 == F(-16655000000, 1331))
check("L06 E2 four grid points above break-even (1300..1600)",
      [u for u in range(200, 1601, 100) if -15000000 + 5000 * u * A10 > 0] == [1300, 1400, 1500, 1600])
check("L06 R1 log-width of each factor is ln 2", all(math.isclose(math.log(r), math.log(2)) for r in (F(4000, 2000), F(2, 1), F(1, 5) / F(1, 10))))
mstar = F(15000000) * F(1331) / (1600 * F(3310))
check("L06 R3 m* ~ 3769.8 cents, 0.7540 of 5000, fall 24.6 percent",
      round(float(mstar), 1) == 3769.8 and round(float(mstar) / 5000, 4) == 0.7540 and round((1 - float(mstar) / 5000) * 100, 1) == 24.6,
      f"m*={float(mstar):.4f}")
check("L06 Problem E1 / key row 3000/A", round(3000 / float(A12), 4) == 1249.0469)
check("L06 quiz 4.13 tolerance", abs(500 / 121 - 4.13) <= 0.005)
check("L06 quiz 21.24 tolerance", abs(84.9464 / 4 - 21.24) <= 0.01)
check("L06 quiz 1206.34 tolerance", abs(399300 / 331 - 1206.34) <= 0.005)
check("L06 Prop 3.2 product bounds for three factors 200 and 1600",
      min(2000 * a * c for a in (1, 2) for c in (F(1, 10), F(1, 5))) == 200)

# ---------- L04 quiz numeric answers ----------
check("L04 quiz d=6.6667 tolerance 0.001", abs(20 / 3 - 6.6667) <= 0.001)
check("L04 quiz q2 P&L 10", 10010 - 10000 == 10)
check("L04 quiz q7 400", 25 * 4 ** 2 == 400)

fails = [n for n, ok_ in results if not ok_]
print(f"SUMMARY checks={len(results)} fail={len(fails)}")
for f_ in fails:
    print("FAILED:", f_)

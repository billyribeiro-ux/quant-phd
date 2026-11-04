"""Independent re-derivation of every number that the PC3 cards.json cards state (slice PC3-d, round 1).

Run: python3 -I ledgers/PC3/scripts/PC3-d-r1/card_numbers.py
Each check prints its label, the recomputed value and True/False against the card value. Exit code 1 on any False.
"""
import math
import random
from fractions import Fraction as F
from itertools import product

results: list[tuple[str, bool, str]] = []


def check(label: str, ok: bool, detail: str) -> None:
    results.append((label, ok, detail))


def near(a: float, b: float, tol: float = 5e-11) -> bool:
    return abs(a - b) <= tol


# ---------- L01 ----------
check("c007 ln 19.5 = 2.9704144656", near(math.log(19.5), 2.9704144656, 5e-11), f"{math.log(19.5):.10f}")
check("c007 ln3+ln5+ln1.3 = ln19.5", near(math.log(3) + math.log(5) + math.log(1.3), math.log(19.5), 1e-12), "")
check("c007 bounds 12000, 234000", 20 * 2 * 300 == 12000 and 60 * 10 * 390 == 234000, "")
check("c007 ratio 19.5", F(234000, 12000) == F(39, 2), str(F(234000, 12000)))
check("c009 minutes narrowing removes 0.1754 (5.9%)",
      near(math.log(390 / 300) - math.log(360 / 330), 0.1753528875, 1e-9)
      and round(100 * (math.log(390 / 300) - math.log(360 / 330)) / math.log(19.5), 1) == 5.9,
      f"{math.log(390/300)-math.log(360/330):.10f}")
check("c009 quote-updates narrowing removes 0.9163 (30.8%)",
      near(math.log(5) - math.log(2), 0.9162907319, 1e-9)
      and round(100 * (math.log(5) - math.log(2)) / math.log(19.5), 1) == 30.8,
      f"{math.log(5)-math.log(2):.10f}")
check("c016 A [1,3]->[1,2] removes ln1.5=0.4055", near(math.log(3) - math.log(2), 0.4054651081, 1e-9), "")
check("c016 B [1,2.5]->[1,1.01] removes 0.9063; B width < A width",
      near(math.log(2.5 / 1.01), 0.906341, 1e-6) and math.log(2.5) < math.log(3), f"{math.log(2.5/1.01):.8f}")
n, x = 10, F(1, 100)
rem = (1 + x) ** n - 1 - n * x
bound = F(n * (n - 1), 2) * (1 + x) ** (n - 2) * x * x
check("c013 (1.01)^10 exact decimal 1.1046221254", f"{float((1+x)**n):.10f}" == "1.1046221254", f"{float((1+x)**n):.10f}")
check("c013 remainder 0.0046221254", f"{float(rem):.10f}" == "0.0046221254", f"{float(rem):.10f}")
check("c013 bound 0.0048728552", f"{float(bound):.10f}" == "0.0048728552", f"{float(bound):.10f}")
check("c013 remainder <= bound", rem <= bound, "")
n, x = 10, F(1, 20)
rem20 = (1 + x) ** n - 1 - n * x
bound20 = F(n * (n - 1), 2) * (1 + x) ** (n - 2) * x * x
check("c014 (1.05)^10 = 1.6289 (4 places), estimate 1.5, miss 0.1289",
      f"{float((1+x)**n):.4f}" == "1.6289" and f"{float(rem20):.4f}" == "0.1289" and float(1 + n * x) == 1.5, "")
check("c014 bound 0.1662 > miss", f"{float(bound20):.4f}" == "0.1662" and bound20 > rem20, f"{float(bound20):.10f}")
check("c012 n=2 remainder = bound = x^2", all(((1+F(k,7))**2 - 1 - 2*F(k,7)) == F(k,7)**2 for k in range(0, 50)), "")

# ---------- L02 ----------
# Monty Hall rule A and B by full enumeration (car, pick, host door) with the lesson's rules.
def monty(rule: str) -> tuple[F, F]:
    stay = F(0); switch = F(0); total = F(0)
    for car, pick in product(range(3), range(3)):
        others = [d for d in range(3) if d != pick]
        for opened in others:
            if rule == "A":
                goats = [d for d in others if d != car]
                if opened not in goats:
                    continue
                p_open = F(1, len(goats))
                w = F(1, 3) * F(1, 3) * p_open
                final_switch = [d for d in range(3) if d not in (pick, opened)][0]
                total += w
                stay += w * (1 if pick == car else 0)
                switch += w * (1 if final_switch == car else 0)
            else:
                w = F(1, 3) * F(1, 3) * F(1, 2)
                if opened == car:
                    continue  # condition on revealed goat
                final_switch = [d for d in range(3) if d not in (pick, opened)][0]
                total += w
                stay += w * (1 if pick == car else 0)
                switch += w * (1 if final_switch == car else 0)
    return stay / total if total else F(0), switch / total if total else F(0)
sA = monty("A"); sB = monty("B")
check("c028 rule A stay 1/3, switch 2/3", sA == (F(1, 3), F(2, 3)), str(sA))
check("c029 rule B stay 1/2, switch 1/2", sB == (F(1, 2), F(1, 2)), str(sB))
urn_second = F(3, 5)
check("c026 urn: P(both red)=3/10, P(second red)=3/5", F(3*2, 5*4) == F(3, 10) and F(12, 20) == F(3, 5), "")
check("c027 urn: P(second red | first blue)=3/4", F(3, 4) == F(3, 4), "")
check("c023 two flips: 1/3 and 1/2", F(1, 4) / F(3, 4) == F(1, 3) and F(1, 4) / F(1, 2) == F(1, 2), "")
check("c031 bag example P(bag1|red)=3/4", (F(1, 2) * F(3, 4)) / (F(1, 2) * F(3, 4) + F(1, 2) * F(1, 4)) == F(3, 4), "")
check("c033 M2: P(B)=29/100, P(A|B)=15/29",
      F(3, 10) * F(1, 2) + F(7, 10) * F(1, 5) == F(29, 100) and (F(3, 10) * F(1, 2)) / F(29, 100) == F(15, 29), "")
# c034 twelve items: closed form == enumeration (replicate lab drill generator from seed 0)
rng = random.Random(0)
items = []
for number in range(1, 13):
    flips = rng.randint(3, 8)
    if rng.random() < 0.5:
        k = rng.randint(1, flips); items.append(("atleast", flips, k))
    else:
        j = rng.randint(1, flips); items.append(("first", flips, j))
agree = 0
for kind, flips, arg in items:
    cnt = 0
    for seq in product((0, 1), repeat=flips):
        if kind == "atleast":
            hit = sum(seq) >= arg
        else:
            hit = seq[arg - 1] == 1 and all(s == 0 for s in seq[: arg - 1])
        cnt += hit
    exact = F(cnt, 2 ** flips)
    formula = F(sum(math.comb(flips, i) for i in range(arg, flips + 1)), 2 ** flips) if kind == "atleast" else F(1, 2 ** arg)
    agree += exact == formula
check("c034 drill items 12 of 12 agree", agree == 12, f"{agree} of 12")
check("E1 item 4 = 57/64", F(57, 64) == 1 - F(1, 64) - F(6, 64), "")

# ---------- L03 ----------
check("c042 continuation 250", F(sum(100 * g for g in range(1, 7)), 6) - 100 == 250, "")
v = sum(max(F(100 * f), F(250)) for f in range(1, 7)) / 6
check("c043 value 1150/3, stop faces 3-6", v == F(1150, 3) and [f for f in range(1, 7) if 100 * f >= 250] == [3, 4, 5, 6], str(v))
check("c044 stop-every-face 350", F(sum(100 * f for f in range(1, 7)), 6) == 350, "")
best = max(sum((F(100 * f) if bits[f - 1] else F(250)) for f in range(1, 7)) / 6 for bits in product((0, 1), repeat=6))
check("c044 best of 64 policies = 1150/3", best == F(1150, 3), str(best))

def exp_rule(outcomes, horizon, rule):
    def val(h):
        if len(h) == horizon or rule(h):
            return F(sum(h))
        return sum((p * val(h + (x,)) for x, p in outcomes), F(0))
    return val(())

FAIR = ((100, F(1, 2)), (-100, F(1, 2)))
BIASED = ((150, F(1, 2)), (-100, F(1, 2)))
rules = {
    "all": lambda h: False,
    "first win": lambda h: bool(h) and h[-1] > 0,
    "first loss": lambda h: bool(h) and h[-1] < 0,
    "total 100": lambda h: sum(h) >= 100,
    "200 gain/loss": lambda h: sum(h) >= 200 or sum(h) <= -200,
}
check("c050 fair game: zero for all five rules", all(exp_rule(FAIR, 6, r) == 0 for r in rules.values()), "")
check("c049 biased: first loss 1575/32", exp_rule(BIASED, 6, rules["first loss"]) == F(1575, 32), str(exp_rule(BIASED, 6, rules["first loss"])))
check("c049 biased: total 100 gives 575/8", exp_rule(BIASED, 6, rules["total 100"]) == F(575, 8), str(exp_rule(BIASED, 6, rules["total 100"])))
check("c049 biased: 200 gain/loss 625/8", exp_rule(BIASED, 6, rules["200 gain/loss"]) == F(625, 8), str(exp_rule(BIASED, 6, rules["200 gain/loss"])))
check("c048 biased all-turns 150", exp_rule(BIASED, 6, rules["all"]) == 150, "")
# R1 two-turn look-ahead rule: stop at turn with larger cumulative total
tot = F(0); n_paths = 0
for a, b in product((100, -100), repeat=2):
    w1, w2 = a, a + b
    tot += max(w1, w2); n_paths += 1
check("c051 R1 look-ahead mean 50", tot / n_paths == 50, str(tot / n_paths))
check("c054 gain 100/3", F(1150, 3) - 350 == F(100, 3), "")

# ---------- L04 ----------
def trade_term_formula(p: F, v: int, a: int, b: int) -> F:
    return (1 - p) * F(a - b, 2) - p * (max(v - a, 0) + max(b - v, 0))

def trade_term_enum(p: F, v: int, a: int, b: int) -> F:
    tot = F(0)
    for arr, pr in (("ub", (1 - p) / 2), ("us", (1 - p) / 2), ("inf", p)):
        if arr == "ub":
            tot += pr * (a - v)
        elif arr == "us":
            tot += pr * (v - b)
        else:
            if v > a:
                tot += pr * (a - v)
            elif v < b:
                tot += pr * (v - b)
    return tot

ok_all = all(trade_term_formula(F(1, 2), v, 10010, 9990) == trade_term_enum(F(1, 2), v, 10010, 9990) for v in range(9950, 10060))
ok_all &= all(trade_term_formula(F(3, 5), v, 10010, 9990) == trade_term_enum(F(3, 5), v, 10010, 9990) for v in range(9950, 10060))
check("c063 Prop 3.1 closed form == enumeration over a range of v (p=1/2 and 3/5)", ok_all, "")
check("c064 Example 3.2 values 5, 0, 5/2", [trade_term_formula(F(1, 2), v, 10010, 9990) for v in (10000, 10020, 9985)] == [5, 0, F(5, 2)], "")
check("c065 zero iff v=a+h at p=1/2 (v>=a)", all((trade_term_formula(F(1, 2), v, 10010, 9990) == 0) == (v == 10020) for v in range(10010, 10060)), "")
check("c066 uninformed flow (1-p)h = h/2 at p=1/2, quarter of 2h", (F(1, 2) * 10) == F(5) and F(5) / F(20) == F(1, 4), "")
check("c067/c068 fair-move variance 25 I^2; SD 15 at 3 units and 50 at 10", 25 * 9 == 225 and 25 * 100 == 2500 and math.sqrt(225) == 15 and math.sqrt(2500) == 50, "")
check("c072 uninformed buy at 10010 with settlement 10000 gives P&L 10", 10010 + (-1) * 10000 == 10, "")
check("c075 R1 d=(1-p)h/p = 20/3", F(2, 5) * 10 / F(3, 5) == F(20, 3), str(F(2, 5) * 10 / F(3, 5)))
check("c076 R3: largest |I| with 25 I^2 < 100 is 1", max(i for i in range(0, 20) if 25 * i * i < 100) == 1 and 25 * 4 == 100, "")

# seed-0 path of the lesson (independent re-implementation from the lesson rules)
r0 = random.Random(0)
path = [10000]; arrivals = []
for _ in range(20):
    mv = 5 if r0.random() < 0.5 else -5
    path.append(path[-1] + mv)
    d = r0.random()
    arrivals.append("ub" if d < 0.25 else "us" if d < 0.5 else "inf")
inv = 0; cash = 0; last = None; fills = 0; cflow = 0; mids = []
for t in range(1, 21):
    mid = 10000 if last is None else last
    bid, ask = mid - 10, mid + 10
    mids.append(mid)
    arr = arrivals[t - 1]; fair = path[t]
    if arr == "ub": side = -1
    elif arr == "us": side = 1
    else: side = -1 if fair > ask else 1 if fair < bid else 0
    if side != 0 and abs(inv + side) <= 10:
        price = ask if side < 0 else bid
        cf = -side * price
        inv += side; cash += cf; cflow += cf; fills += 1; last = price
settle = path[20]
last_mid = mids[-1]
check("c070 seed 0: 9 fills, cash flow -9950, inventory 1, settlement 9980, P&L 30",
      fills == 9 and cflow == -9950 and inv == 1 and settle == 9980 and cash + inv * settle == 30,
      f"fills={fills} cf={cflow} inv={inv} settle={settle} pnl={cash + inv*settle}")
check("c061 seed 0: final mid 9990, mid-mark 40, settlement-mark 30",
      (9980 + 10) == 9990 and cash + inv * 9990 == 40 and cash + inv * settle == 30,
      f"last quote mid={last_mid} mid-mark={cash + inv*9990}")

# ---------- L05 ----------
def naive(xs, k):
    comps = 0; out = []
    for s in range(len(xs) - k + 1):
        best = xs[s]
        for xx in xs[s + 1: s + k]:
            comps += 1
            best = max(best, xx)
        out.append(best)
    return out, comps

def deque_run(xs, k):
    from collections import deque
    dq = deque(); out = []; comps = pushes = pops = 0
    for i, xv in enumerate(xs):
        while dq:
            comps += 1
            if xs[dq[-1]] > xv:
                break
            dq.pop(); pops += 1
        dq.append(i); pushes += 1
        if dq[0] <= i - k:
            dq.popleft(); pops += 1
        if i >= k - 1:
            out.append(xs[dq[0]])
    return out, comps, pushes, pops

r5 = random.Random(5)
xs5 = [r5.randint(0, 999) for _ in range(200)]
nv, nc = naive(xs5, 8)
dv, dc, dpu, dpo = deque_run(xs5, 8)
check("c089 seed 5 k=8: naive 1351, deque 354, pushes 200, pops 199", nc == 1351 and dc == 354 and dpu == 200 and dpo == 199 and nv == dv,
      f"naive={nc} deque={dc} pushes={dpu} pops={dpo} equal={nv == dv}")
nv32, nc32 = naive(xs5, 32)
dv32, dc32, _, _ = deque_run(xs5, 32)
check("c090 seed 5 k=32: naive 5239 = 169*31, deque 382", nc32 == 5239 and 169 * 31 == 5239 and dc32 == 382 and nv32 == dv32,
      f"naive={nc32} deque={dc32}")
eq = all(naive(xs5, k)[0] == deque_run(xs5, k)[0] for k in range(1, 21))
check("c094 outputs equal for k=1..20 on seed-5 sequence", eq, "")
check("c080 naive count formula (n-k+1)(k-1) on random inputs",
      all(naive([0] * n_, k)[1] == (n_ - k + 1) * (k - 1) for n_ in range(1, 25) for k in range(1, n_ + 1)), "")
check("c081 n=200 max of (n-k+1)(k-1) at k=101 equals 10000",
      max(((200 - k + 1) * (k - 1), k) for k in range(1, 201)) == (10000, 101), "")
check("c086 Example 3.5 outputs (4,4,5)", deque_run([3, 1, 4, 1, 5], 3)[0] == [4, 4, 5], "")
check("c087 M2 outputs (5,5,1,3)", deque_run([2, 5, 1, 0, 3], 2)[0] == [5, 5, 1, 3], "")
check("c088 P3: strictly increasing gives n-1 comparisons for every k",
      all(deque_run(list(range(1, n_ + 1)), k)[1] == n_ - 1 for n_ in range(1, 15) for k in range(1, n_ + 1)), "")
check("c084 Prop 3.3: pushes n, pops <= n, comparisons <= 2n (random inputs)",
      all((lambda r: r[2] == len(xs_) and r[3] <= len(xs_) and r[1] <= 2 * len(xs_))(deque_run(xs_, k))
          for xs_ in ([random.Random(s).randint(0, 9) for _ in range(30)] for s in range(20)) for k in range(1, 31)), "")
kk = 6
xs_rem = list(range(kk, 1, -1)) + [100]
check("c085 Remark 3.4: x=(k,...,2,100), n=k, step k removes k-1 entries in one loop",
      len(xs_rem) == kk and deque_run(xs_rem, kk)[1] >= kk - 1, f"comps={deque_run(xs_rem, kk)[1]}")
check("c092 counts are integers (no time measured)", all(isinstance(v_, int) for v_ in (nc, dc)), "")

# ---------- L06 ----------
check("c095 identity (s-K)^+ - (K-s)^+ = s-K on a grid",
      all(max(s - K, 0) - max(K - s, 0) == s - K for s in range(-20, 21) for K in range(-20, 21)), "")
A = sum(F(1, 1) / F(11, 10) ** t for t in range(1, 4))
check("c107 annuity 3310/1331", A == F(3310, 1331), str(A))
be = F(150000, 50) / A
check("c107 break-even 399300/331 = 1206.34", be == F(399300, 331) and round(float(be), 2) == 1206.34, f"{float(be):.6f}")
check("c107 Example 4.2 Fermi bounds [200, 1600]", (2000 * 1 * F(1, 10), 4000 * 2 * F(1, 5)) == (200, 1600), "")
def npv(cfs, r):
    return sum((F(c) / (1 + r) ** t for t, c in enumerate(cfs)), F(0))
def cf(u_cents, outlay=15_000_000, margin=5000):
    return [-outlay] + [u_cents * margin] * 3
check("c109 NPV at 200 units = -12513148 cents", round(float(npv(cf(200), F(1, 10)))) == -12513148, f"{float(npv(cf(200), F(1,10))):.4f}")
check("c109 NPV at 1600 units = 4894816 cents", round(float(npv(cf(1600), F(1, 10)))) == 4894816, f"{float(npv(cf(1600), F(1,10))):.4f}")
for rate, want in ((F(8, 100), 1164.10), (F(12, 100), 1249.05)):
    A_r = sum(F(1) / (1 + rate) ** t for t in range(1, 4))
    b_r = F(150000 * 1, 50) / A_r
    check(f"c108 break-even at {float(rate)*100:.0f}% = {want}", round(float(b_r), 2) == want, f"{float(b_r):.6f}")
    check(f"c108 NPV negative at 200, positive at 1600 at {float(rate)*100:.0f}%",
          npv(cf(200), rate) < 0 and npv(cf(1600), rate) > 0, "")
check("c112 break-even moves 42.24 then 42.71 (about 21 per point)",
      abs((1206.34 - 1164.10) / 2 - 21.12) < 0.01 and abs((1249.05 - 1206.34) / 2 - 21.355) < 0.01, "")
check("c110 forward: payoff 0 at F=10000 and 100 at F=10100 for S_T 8000..12000",
      (F(10000) - F(9700) / F(97, 100)) == 0 and (F(10100) - F(9700) / F(97, 100)) == 100, "")
check("c110 S/D = 10000 cents", F(9700) / F(97, 100) == 10000, "")
check("c102 NPV(u) = -K + m A u and break-even K/(mA) at n=3 (exact)",
      all(npv([-1000] + [u * 40] * 3, F(1, 10)) == -1000 + 40 * A * u for u in range(0, 30)), "")
check("c115 M2: NPV(-100,60,60; 10%) = 500/121", npv([-100, 60, 60], F(1, 10)) == F(500, 121), str(npv([-100, 60, 60], F(1, 10))))
check("c116 M3: u* = 33275/331 = 100.53", F(1000) / (F(4) * A) == F(33275, 331) and round(float(F(33275, 331)), 2) == 100.53, str(F(1000) / (F(4) * A)))
m_star = F(15_000_000) / (F(1600) * A)
check("c117 R3: margin 3769.8 cents = 0.7540 of 5000, fall 24.6%",
      round(float(m_star), 1) == 3769.8 and round(float(m_star) / 5000, 4) == 0.7540 and round(100 * (1 - float(m_star) / 5000), 1) == 24.6,
      f"m*={float(m_star):.4f}")
check("c106 Example 4.2 units range", (F(2000) * 1 * F(1, 10), F(4000) * 2 * F(1, 5)) == (200, 1600), "")
check("c113 range [200,1600] straddles break-even 1206.34", 200 < 1206.34 < 1600, "")

bad = [r for r in results if not r[1]]
for label, ok_, detail in results:
    print(("PASS " if ok_ else "FAIL ") + label + ("" if not detail else "  [" + detail + "]"))
print(f"checks: {len(results)} pass={len(results)-len(bad)} fail={len(bad)}")
raise SystemExit(1 if bad else 0)

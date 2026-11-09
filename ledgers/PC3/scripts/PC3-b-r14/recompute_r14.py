"""Round-14 independent recomputation for PC3 slice b (L04, L05, L06). Written by the verifier, not the builder.

Run: .venv/bin/python -I ledgers/PC3/scripts/PC3-b-r14/recompute_r14.py
"""

import random
from fractions import Fraction as F
from math import comb, floor, log2

print("== L04 ==")


def path_and_arrivals(seed):
    rng = random.Random(seed)
    v = [10000]
    arr = []
    for _ in range(20):
        d = 5 if rng.random() < 0.5 else -5
        v.append(v[-1] + d)
        x = rng.random()
        arr.append("UB" if x < 0.25 else ("US" if x < 0.5 else "I"))
    return v, arr


def sim(seed):
    v, arr = path_and_arrivals(seed)
    inv, cash, last = 0, 0, None
    log = []
    mids = []
    for t in range(1, 21):
        mid = 10000 if last is None else last
        mids.append(mid)
        b, a = mid - 10, mid + 10
        fv = v[t]
        a_kind = arr[t - 1]
        if a_kind == "UB":
            side = -1
        elif a_kind == "US":
            side = +1
        elif fv > a:
            side = -1
        elif fv < b:
            side = +1
        else:
            side = 0
        if side != 0 and abs(inv + side) <= 10:
            price = a if side == -1 else b
            cash += -side * price
            inv += side
            last = price
            log.append((t, side, price))
    settle = v[20]
    fills = len(log)
    cf = sum(-s * p for _, s, p in log)
    pnl = cash + inv * settle
    informed = arr.count("I")
    # claim: mid at turn t equals 10000 - 10 * I_{t-1}; check against the path inventory before each turn
    return dict(fills=fills, cf=cf, inv=inv, settle=settle, pnl=pnl, informed=informed, cash=cash,
                ident=(pnl == cf + inv * settle), mids=mids, log=log)


s0 = sim(0)
s1 = sim(1)
print("seed0", {k: s0[k] for k in ("fills", "cf", "inv", "settle", "pnl", "informed", "ident")})
print("seed1", {k: s1[k] for k in ("fills", "cf", "inv", "settle", "pnl", "informed", "ident")})
# mid identity: mid_t = 10000 - 10*I_{t-1} for every turn of both seeds (check via replay of inventory before each turn)
for name, s in (("seed0", s0), ("seed1", s1)):
    inv_before = {}
    inv = 0
    fills_at = {t: sd for t, sd, _ in s["log"]}
    for t in range(1, 21):
        inv_before[t] = inv
        inv += fills_at.get(t, 0)
    ok = all(s["mids"][t - 1] == 10000 - 10 * inv_before[t] for t in range(1, 21))
    print(f"{name}: mid_t == 10000 - 10*I_(t-1) on all 20 turns: {ok}")

# Part 2: exact enumeration vs closed form on the grid 9980..10020 step 5, quote 9990/10010
p = F(1, 2)
probs = {"UB": F(1, 4), "US": F(1, 4), "I": F(1, 2)}


def enum_term(fv, b, a):
    tot = F(0)
    for k, pr in probs.items():
        if k == "UB":
            side = -1
        elif k == "US":
            side = 1
        elif fv > a:
            side = -1
        elif fv < b:
            side = 1
        else:
            continue
        price = a if side == -1 else b
        tot += pr * (-side * price + side * fv)
    return tot


def closed(fv, b, a):
    h = F(a - b, 2)
    return h / 2 - F(max(fv - a, 0) + max(b - fv, 0), 2)


allok = True
for fv in range(9980, 10025, 5):
    e, c = enum_term(fv, 9990, 10010), closed(fv, 9990, 10010)
    allok &= e == c
    print(f"  v={fv} E={e} closed={c}")
print("Part 2 all equal:", allok)
# general closed form check on a wider random grid of quotes (not just the lab grid) to test Proposition 3.1 as stated
import itertools  # noqa: E402

bad = 0
cnt = 0
for b, a in [(9990, 10010), (9900, 9960), (10001, 10003), (9000, 9200)]:
    for fv in range(b - 60, a + 61, 1):
        cnt += 1
        if enum_term(fv, b, a) != (1 - p) * F(a - b, 2) - p * (max(fv - a, 0) + max(b - fv, 0)):
            bad += 1
print("Prop 3.1 (p=1/2) cells checked:", cnt, "mismatches:", bad)

# Part 3
for I in (0, 1, 3, -3, 10):
    vals = [F(5 * I), F(-5 * I)]
    mean = sum(vals) / 2
    var = sum((x - mean) ** 2 for x in vals) / 2
    print("I", I, "mean", mean, "var", var, "25I^2", 25 * I * I)
# I=10 refusal case: quote 9990/10010, v=10000, I=10
e_I10 = F(1, 4) * (10010 - 10000)  # uninformed buy only (sell refused, informed no trade at v inside quote)
print("L04 Remark 4.2 I=10 expected trade term:", e_I10)
# Remark 4.2 sd values
print("sd at 3 units", 5 * 3, "sd at 10 units", 5 * 10)
# R1 value
print("R1 d =", F((1 - F(3, 5)) * 10) / F(3, 5))
# E2 binomial z
se = (0.25 / 20) ** 0.5
print("E2 se", round(se, 6), "z", round((0.65 - 0.5) / se, 4), "crit", 1.959964)
# Example 1.3 / Remark 3.4 values: quote at v=10020, 9985
print("Example 3.2 values", F(5) - F(1, 2) * max(10020 - 10010, 0), F(5) - F(1, 2) * max(9990 - 9985, 0))
print("Remark 4.2 I=10 Prop3.1 check", F(0))

print("== L05 ==")


def naive(xs, k):
    out, cmp = [], 0
    for s in range(len(xs) - k + 1):
        best = xs[s]
        for x in xs[s + 1: s + k]:
            cmp += 1
            best = max(best, x)
        out.append(best)
    return out, cmp


def surviving(xs, i, k):
    # Definition 3.1, 0-based indices: i-k < j <= i and x_j > x_m for j < m <= i (1-based in the page; mirrored here)
    res = []
    for j in range(max(0, i - k + 1), i + 1):
        if all(xs[j] > xs[m] for m in range(j + 1, i + 1)):
            res.append(j)
    return res


def deque_run(xs, k):
    from collections import deque

    dq = deque()
    out = []
    comps = pops = pushes = 0
    back_removals = 0
    for i, x in enumerate(xs):
        while dq:
            comps += 1
            if xs[dq[-1]] > x:
                break
            dq.pop()
            pops += 1
            back_removals += 1
        dq.append(i)
        pushes += 1
        if dq[0] <= i - k:
            dq.popleft()
            pops += 1
        if i >= k - 1:
            out.append(xs[dq[0]])
        # invariant check (Prop 3.2): deque equals survivors of Definition 3.1 at step i
        assert list(dq) == surviving(xs, i, k), (i, list(dq), surviving(xs, i, k))
    return out, comps, pops, pushes, back_removals


def seq(seed, n=200):
    r = random.Random(seed)
    return [r.randint(0, 999) for _ in range(n)]


x5, x6 = seq(5), seq(6)
print("seed5 first5", x5[:5], "max", max(x5))
for k in (1, 2, 8, 32, 200):
    nout, nc = naive(x5, k)
    dout, dc, dp, dpu, br = deque_run(x5, k)
    print(f"k={k}: naive={nc} formula={(200-k+1)*(k-1)} deque_cmp={dc} pops={dp} pushes={dpu} eq={nout == dout} back_removals={br} cmp<=2n {dc <= 400}")
nout, nc = naive(x6, 8)
dout, dc, dp, dpu, br = deque_run(x6, 8)
print(f"seed6 k=8: naive={nc} deque_cmp={dc} pops={dp} pushes={dpu} eq={nout == dout}")
# outputs equal for k in 1..20 on seed 5
print("seed5 k1..20 equal:", all(naive(x5, k)[0] == deque_run(x5, k)[0] for k in range(1, 21)))
# Prop 3.2 / 3.3 random stress
import random as R  # noqa: E402

rr = R.Random(12345)
viol = 0
for trial in range(400):
    n = rr.randint(1, 30)
    k = rr.randint(1, n)
    xs2 = [rr.randint(0, 5) for _ in range(n)]
    o, c, pp, pu, br = deque_run(xs2, k)  # asserts survivors invariant
    if o != naive(xs2, k)[0] or pu != n or br > n or c > 2 * n:
        viol += 1
print("random stress (400 cases, ties included): violations", viol)
# Prop 3.3 strict-increasing claim, R3 and P3 (n-1 for every k)
incr = list(range(200))
print("increasing n-1 for all k:", all(deque_run(incr, k)[1] == 199 for k in range(1, 201)))
# Remark 3.4 example: x=(k, k-1, ..., 1, k+1), a single step removes k entries
for kk in (1, 2, 5, 9):
    xs3 = list(range(kk, 0, -1)) + [kk + 1]
    dq_before = []
    # count back removals at step n
    from collections import deque as DQ

    dq = DQ()
    removed_last = 0
    for i, x in enumerate(xs3):
        cnt = 0
        while dq and xs3[dq[-1]] <= x:
            dq.pop()
            cnt += 1
        removed_last = cnt
        dq.append(i)
        if dq[0] <= i - kk:
            dq.popleft()
    print(f"Remark3.4 k={kk}: removals at step n = {removed_last}")
# Example 3.5 trace and M2 trace
print("Example 3.5 outputs", deque_run([3, 1, 4, 1, 5], 3)[0])
print("M2 outputs", deque_run([2, 5, 1, 0, 3], 2)[0])
# Remark 2.2: (n-r)r <= n^2/4 with r=k-1; R2 n=200 max at k=101
best = max(range(1, 201), key=lambda k: (200 - k + 1) * (k - 1))
print("R2 argmax k for n=200:", best, (200 - best + 1) * (best - 1))
print("E1 ratio", round(5239 / 382, 4), "M1", (10 - 4 + 1) * (4 - 1))
# Remark 3.6 heap bound
print("heap bound n=200:", 3 * 200 * floor(log2(200)), "2n", 400, "floor log2 200", floor(log2(200)))

print("== L06 ==")


def annuity(r):
    return sum((1 / (1 + r) ** t for t in range(1, 4)), F(0)) if False else sum((F(1) / (1 + r) ** t for t in range(1, 4)), F(0))


r10 = F(1, 10)
A10 = annuity(r10)
print("A10", A10, float(A10))
print("break-even 10%", F(15000000, 5000) / A10, float(F(15000000, 5000) / A10))
for r in (F(8, 100), F(10, 100), F(12, 100)):
    A = annuity(r)
    be = F(3000) / A
    A7 = F(round(float(A) * 10**7), 10**7)
    print(f"r={r}: A exact={float(A):.10f} A(7dp)={float(A):.7f} 3000/A={float(be):.6f} 3000/A(7dp)={3000/float(A7):.6f}")
# NPV grid values
for r in (F(8, 100), F(10, 100), F(12, 100)):
    A = annuity(r)
    npv_lo = -15000000 + 5000 * 200 * A
    npv_hi = -15000000 + 5000 * 1600 * A
    print(f"NPV r={r}: lower {float(npv_lo):.3f} upper {float(npv_hi):.3f}")
print("NPV 1200 exact", -15000000 + 5000 * 1200 * A10, float(-15000000 + 5000 * 1200 * A10))
print("NPV 1300 exact", -15000000 + 5000 * 1300 * A10, float(-15000000 + 5000 * 1300 * A10))
print("E1 A12 7dp", float(annuity(F(12, 100))), "1/1.12+1/1.2544+1/1.404928 =", 1 / 1.12 + 1 / 1.2544 + 1 / 1.404928)
print("R3 margin", float(F(15000000 * 1331, 1600 * 3310)), "ratio", float(F(15000000 * 1331, 1600 * 3310) / 5000), "fall %", float(100 - F(15000000 * 1331, 1600 * 3310) / 50))
print("M3 break-even", F(100000 * 1331, 400 * 3310), float(F(100000 * 1331, 400 * 3310)))
print("M2 NPV", -100 + F(60) / F(11, 10) + F(60) / F(121, 100), float(-100 + F(60) / F(11, 10) + F(60) / F(121, 100)))
print("E2 grid points > breakeven", [u for u in range(200, 1601, 100) if -15000000 + 5000 * u * A10 > 0])
print("Example 4.2 break-even", F(399300, 331), float(F(399300, 331)))
print("Example 4.2 check 3000*1331/3310 =", F(3000 * 1331, 3310))
print("Remark 4.3 steps", float(F(3000) / annuity(F(8, 100)) - F(3000) / A10), float(F(3000) / annuity(F(12, 100)) - F(3000) / A10))
print("E3 avg per point", float((F(3000) / annuity(F(12, 100)) - F(3000) / annuity(F(8, 100))) / 4))
print("Corollary boundary: NPV at u*=I/(mA):", -15000000 + 5000 * (F(399300, 331)) * A10)
print("R1 log width ratios", 4000 / 2000, 2 / 1, (1 / 5) / (1 / 10))
print("P3 bounds", 2000 * 1 * F(1, 10), 4000 * 2 * F(1, 5))
print("Fermi ratio", 1600 / 200)
print("Remark 1.2 p", p)
print("half-up checks", floor(F(-12513148.07) + F(1, 2)))

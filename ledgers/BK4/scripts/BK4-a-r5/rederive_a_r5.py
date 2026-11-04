"""Independent re-derivation for BK4 slice a (L01, L02, L03 and the hub numbers), round 5.

Stdlib only, run as: python3 -I rederive_a_r5.py. Uses its own code paths: RTGS need by binary search on the
opening balance (feasibility), not by the running minimum; netting by a direct per-member sum; sizing by brute force
over all integer margins; waterfall by a separately written layer routine with random checks.
"""
import random
from fractions import Fraction
from math import ceil

out = []
def say(*a):
    out.append(" ".join(str(x) for x in a))

# ---------- L01 ----------
rng = random.Random(20260)
banks = 3
day = []
for seq in range(1, 13):
    s, r = rng.sample(range(banks), 2)
    dollars = rng.randint(100, 5000)
    day.append((s, r, 100 * dollars))
say("L01 gross", sum(a for _, _, a in day))
def feasible(o, bank):
    bal = o
    for s, r, a in day:
        if s == bank:
            bal -= a
        elif r == bank:
            bal += a
        if bal < 0:
            return False
    return True
need, debit, net = {}, {}, {}
for b in range(banks):
    lo, hi = 0, sum(a for _, _, a in day)
    while lo < hi:  # least feasible opening balance by binary search (feasibility is monotone in o)
        mid = (lo + hi) // 2
        if feasible(mid, b):
            hi = mid
        else:
            lo = mid + 1
    need[b] = lo
    net[b] = sum(a for _, r, a in day if r == b) - sum(a for s, _, a in day if s == b)
    debit[b] = max(0, -net[b])
    say("L01 bank", "ABC"[b], "need", need[b], "net", net[b], "debit", debit[b])
say("L01 net sum", sum(net.values()), "need>=debit", all(need[b] >= debit[b] for b in range(banks)))
say("L01 moved", sum(debit.values()), "share", float(Fraction(sum(debit.values()), sum(a for _, _, a in day))))
say("L01 share 4dp half-up", round(float(Fraction(sum(debit.values()), sum(a for _, _, a in day))) , 4))

# ---------- L02 ----------
rng = random.Random(2026)
members = 4
trades = []
for seq in range(1, 7):
    p, r = rng.sample(range(members), 2)
    dollars = rng.randint(500, 20000)
    trades.append((p, r, 100 * dollars))
G = sum(a for _, _, a in trades)
rec = [sum(a for _, r, a in trades if r == m) for m in range(members)]
pay = [sum(a for p, _, a in trades if p == m) for m in range(members)]
n = [rec[m] - pay[m] for m in range(members)]
A = sum(max(0, x) for x in n)
say("L02 G", G, "rec", rec, "pay", pay, "n", n, "sum n", sum(n))
say("L02 A", A, "sum max(0,-n)", sum(max(0, -x) for x in n), "reduction", G - A,
    "bps floor", (10000 * (G - A)) // G, "exact", float(Fraction(10000 * (G - A), G)))

# ---------- L03 ----------
rng = random.Random(2026)
MEMBERS = (1, 2, 3, 4)
im = {i: rng.randint(1000, 5000) for i in MEMBERS}
df = {i: rng.randint(100, 900) for i in MEMBERS}
capital = rng.randint(500, 2000)
losses = [rng.randint(0, 3000) for _ in range(200)]
say("L03 im", im, "df", df, "capital", capital, "max loss", max(losses), "sorted top3", sorted(losses)[-3:])
def sized(target_bps):
    # k = ceil(t S / 10000), exact
    k = ceil(Fraction(target_bps * len(losses), 10000))
    return sorted(losses)[k - 1], k
def brute(target_bps):
    for M in range(0, max(losses) + 1):
        c = sum(1 for x in losses if x <= M)
        if (10000 * c) // len(losses) >= target_bps:
            return M
for t in (9900, 9975):
    m, k = sized(t)
    cov = (10000 * sum(1 for x in losses if x <= m)) // 200
    below = (10000 * sum(1 for x in losses if x <= m - 1)) // 200
    say("L03 target", t, "k", k, "sized", m, "brute", brute(t), "cover at", cov, "cover one below", below,
        "above", sum(1 for x in losses if x > m))
# Example 2.5 and R2/R3 arithmetic
say("L03 ex2.5", Fraction(9900 * 200, 10000), Fraction(9975 * 200, 10000))
say("L03 R3 boundary", [S for S in range(1, 1001) if ceil(Fraction(9975 * S, 10000)) != S][:3],
    "first S with k<S", min(S for S in range(1, 1001) if ceil(Fraction(9975 * S, 10000)) != S))
say("L03 R2", Fraction(9900 * 100, 10000), ceil(Fraction(9900 * 100, 10000)))
# Section 2 example checks
say("M2 cover(4000) with losses 1000,2000,3000,5000", (10000 * 3) // 4, "k", ceil(Fraction(7500 * 4, 10000)))
say("M3 k 8000,8001,10000 on 10..50:", [ceil(Fraction(t * 5, 10000)) for t in (8000, 8001, 10000)])
say("E2 cover 9900 S=200 c=198 check", (10000 * 198) // 200, (10000 * 199) // 200)

# independent waterfall with random checks
def wf(L, d, IM, DF, K):
    a1 = min(L, IM[d]); a2 = min(L - a1, DF[d]); a3 = min(L - a1 - a2, K)
    Z = L - a1 - a2 - a3
    surv = sorted(i for i in DF if i != d)
    D = sum(DF[i] for i in surv)
    pay = {}
    if Z >= D:
        pay = {i: DF[i] for i in surv}; u = Z - D
    else:
        pay = {i: (Z * DF[i]) // D for i in surv}
        left = Z - sum(pay.values())
        assert 0 <= left, "negative leftover"
        for i in surv:
            if left and DF[i] > 0:
                pay[i] += 1; left -= 1
        assert left == 0, "leftover not absorbed"
        u = 0
    return a1, a2, a3, pay, u
rr = random.Random(7)
bad = 0
for _ in range(20000):
    d = rr.randint(1, 4)
    IM = {i: rr.randint(0, 50) for i in range(1, 5)}
    DF = {i: rr.randint(0, 20) for i in range(1, 5)}
    if sum(DF[i] for i in range(1, 5) if i != d) == 0 and rr.random() < 0.5:
        DF[(d % 4) + 1] = 1
    K = rr.randint(0, 50)
    L = rr.randint(0, 200)
    a1, a2, a3, pay, u = wf(L, d, IM, DF, K)
    total = a1 + a2 + a3 + sum(pay.values()) + u
    # ordering invariants of Remark 1.4
    if total != L or (a2 > 0 and a1 != IM[d]) or (a3 > 0 and a2 != DF[d]) or (L - a1 - a2 - a3 > 0 and a3 != K):
        bad += 1
    if any(pay[i] > DF[i] for i in pay):
        bad += 1
say("waterfall random cases 20000, violations", bad)

# Example 1.5 and 1.6 fixture values
for L in (80, 120, 170, 180, 181, 200, 205, 300):
    a1, a2, a3, pay, u = wf(L, 3, {1: 0, 2: 0, 3: 100, 4: 0}, {1: 40, 2: 60, 3: 50, 4: 0}, 30)
    say("fixture", L, a1, a2, a3, pay[1], pay[2], u)
a = wf(1, 4, {1: 0, 2: 0, 3: 0, 4: 0}, {1: 1, 2: 1, 3: 1, 4: 0}, 0)
b = wf(2, 4, {1: 0, 2: 0, 3: 0, 4: 0}, {1: 1, 2: 1, 3: 1, 4: 0}, 0)
say("ex1.6", a[3], b[3])

text = "\n".join(out) + "\n"
print(text)

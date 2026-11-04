"""Round 2 independent recomputation for PC3-b (L04, L05, L06 prose numbers). Written from the page text and the
lab docstrings, not by importing the twins. Run: .venv/bin/python -I ledgers/PC3/scripts/PC3-b-r2/numbers_b2.py"""

from __future__ import annotations

import math
import random
from fractions import Fraction as F

print("== L04 ==")
HORIZON, V0, MOVE, QMAX, LIMIT, H = 20, 10_000, 5, 5, 10, 10


def path_and_arrivals(seed: int):
    rng = random.Random(seed)
    path = [V0]
    arr = []
    for _ in range(HORIZON):
        mv = MOVE if rng.random() < 0.5 else -MOVE
        path.append(path[-1] + mv)
        d = rng.random()
        arr.append("ub" if d < 0.25 else ("us" if d < 0.5 else "inf"))
    return path, arr


def run_game(seed: int):
    path, arr = path_and_arrivals(seed)
    inv, cash, last = 0, 0, None
    fills = []
    log = []
    for t in range(1, HORIZON + 1):
        mid = V0 if last is None else last
        b, a = mid - H, mid + H
        fair = path[t]
        kind = arr[t - 1]
        if kind == "ub":
            side = -1
        elif kind == "us":
            side = 1
        elif fair > a:
            side = -1
        elif fair < b:
            side = 1
        else:
            side = 0
        ok = side != 0 and abs(inv + side) <= LIMIT
        if ok:
            price = a if side < 0 else b
            cash += -side * price
            inv += side
            last = price
            fills.append((t, side, price))
        log.append((t, b, a, kind, ok, inv, cash, fair))
    return path, fills, inv, cash, log


for seed in (0, 1):
    path, fills, inv, cash, log = run_game(seed)
    settle = path[HORIZON]
    pnl = cash + inv * settle
    print(f"seed {seed}: fills={len(fills)} cash_flow={cash} inv_end={inv} settlement={settle} pnl={pnl}")
path0, fills0, inv0, cash0, log0 = run_game(0)
print("seed 0 informed arrivals:", sum(1 for r in log0 if r[3] == "inf"))
last_mid = (log0[-1][1] + log0[-1][2]) // 2
print("seed 0 last quote bid/ask:", log0[-1][1], log0[-1][2], "mid", last_mid)
print("seed 0 P&L at settlement", cash0 + inv0 * path0[-1], "at mid", cash0 + inv0 * last_mid)
print("seed 0 fills count", len(fills0), "max |inv|", max(abs(r[5]) for r in log0))


def trade_term_expect(v, a, b, p, inv_is_zero=True):
    """Exact E[c + sigma v] from the three arrivals, quote fixed, size 1, inventory I; refusal per A5."""
    total = F(0)
    outcomes = [(F(1, 2) * (1 - p), "ub"), (F(1, 2) * (1 - p), "us"), (p, "inf")]
    return outcomes


def expected_trade_term(v, a, b, p, I):
    total = F(0)
    for prob, kind in ((F(1, 2) * (1 - p), "ub"), (F(1, 2) * (1 - p), "us"), (p, "inf")):
        if kind == "ub":
            side = -1
        elif kind == "us":
            side = 1
        elif v > a:
            side = -1
        elif v < b:
            side = 1
        else:
            side = 0
        if side == 0 or abs(I + side) > LIMIT:
            continue
        price = a if side < 0 else b
        total += prob * (-side * price + side * v)
    return total


def closed(v, a, b, p):
    h = F(a - b, 2)
    return (1 - p) * h - p * (max(v - a, 0) + max(b - v, 0))


# Proposition 3.1 at I = 0 for many quotes, fair values and p (exact)
ok = True
for a, b in [(10010, 9990), (10001, 9999), (10040, 9980), (10020, 9980)]:
    for v in range(9950, 10060, 3):
        for p in (F(0), F(1, 3), F(1, 2), F(3, 5), F(1)):
            ok = ok and expected_trade_term(v, a, b, p, 0) == closed(v, a, b, p)
print("Prop 3.1 closed form equals exact enumeration on grid:", ok)

print("Remark 4.2 trade term p=1/2, quote 9990/10010, v=10000:")
for I in (0, 1, 3, 9, 10, -10):
    print(f"  I={I}: {expected_trade_term(10000, 10010, 9990, F(1, 2), I)}")
print("Example 3.2 values:", [closed(v, 10010, 9990, F(1, 2)) for v in (10000, 10020, 9985)])
print("R1 d at p=3/5 h=10:", F(2, 5) * 10 / F(3, 5), float(F(2, 5) * 10 / F(3, 5)))

# Problem E3 numbers
print("E3 at settlement", -9950 + 1 * 9980, "at mid", -9950 + 1 * 9990)

# E2 standard error
se = math.sqrt(0.25 / 20)
print(f"E2 se={se:.6f} z={(0.65 - 0.5) / se:.4f}")

print("== L05 ==")


def seq(seed: int, n: int = 200):
    r = random.Random(seed)
    return [r.randint(0, 999) for _ in range(n)]


def deque_run(xs, k):
    dq: list[int] = []
    out = []
    comps = pushes = pops = 0
    for i, x in enumerate(xs):
        while dq:
            comps += 1
            if xs[dq[-1]] > x:
                break
            dq.pop()
            pops += 1
        dq.append(i)
        pushes += 1
        if dq[0] <= i - k:
            dq.pop(0)
            pops += 1
        if i >= k - 1:
            out.append(xs[dq[0]])
    return out, comps, pushes, pops


def naive(xs, k):
    out = []
    c = 0
    for s in range(len(xs) - k + 1):
        w = xs[s : s + k]
        out.append(max(w))
        c += k - 1
    return out, c


xs5 = seq(5)
print("first five values:", xs5[:5])
o, c, pu, po = deque_run(xs5, 8)
no, nc = naive(xs5, 8)
print("k=8 outputs equal:", o == no, "naive", nc, "deque comps", c, "pushes", pu, "pops", po, "first five maxima", o[:5])
for k in (1, 2, 8, 32, 200):
    _, cc, pp, qq = deque_run(xs5, k)
    print(f"  k={k} deque_comps={cc} pops={qq} pushes={pp} naive_formula={(200 - k + 1) * (k - 1)}")
print("seq5 max", max(xs5))
xs6 = seq(6)
o6, c6, p6, q6 = deque_run(xs6, 8)
n6, nc6 = naive(xs6, 8)
print("seed 6: outputs equal", o6 == n6, "naive", nc6, "deque comps", c6, "pushes", p6, "pops", q6, "bound 400")
ok = all(deque_run(xs5, k)[0] == naive(xs5, k)[0] for k in range(1, 21))
print("seed5 outputs equal k=1..20", ok)
# Proposition 3.3 bound on random sequences
bad = 0
rng = random.Random(123)
for _ in range(300):
    n = rng.randint(1, 60)
    xs = [rng.randint(0, 9) for _ in range(n)]
    k = rng.randint(1, n)
    _, cc, pu2, po2 = deque_run(xs, k)
    if cc > 2 * n or pu2 != n or po2 > n:
        bad += 1
print("Prop 3.3 violations in 300 random cases:", bad)
print("Example 3.5 outputs:", deque_run([3, 1, 4, 1, 5], 3)[0])
print("M2 outputs:", deque_run([2, 5, 1, 0, 3], 2)[0])
# Remark 3.4 example: one step removes k-1 entries
for k in (2, 5, 10, 100, 101):
    x = list(range(k, 1, -1)) + [k + 1]
    # count removals at step k
    dq: list[int] = []
    removed = 0
    for i, v in enumerate(x):
        while dq and x[dq[-1]] <= v:
            dq.pop()
            if i == k - 1:
                removed += 1
        dq.append(i)
        if dq[0] <= i - k:
            dq.pop(0)
    print(f"Remark 3.4 k={k}: len={len(x)} removed at step {k}: {removed} (k-1={k-1})")
# P3 strictly increasing: comparisons n-1 for all k
print("P3 increasing n=50 comps:", {k: deque_run(list(range(50)), k)[1] for k in (1, 3, 49, 50)})
# Naive peak
print("R2 maximiser k for n=200:", max(range(1, 201), key=lambda k: (200 - k + 1) * (k - 1)), (200 - 101 + 1) * 100)
print("E1 ratio 5239/382 =", 5239 / 382)

print("== L06 ==")
D = F(97, 100)
print("no-arb F = 9700/0.97 =", F(9700) / D)
print("payoff at F=10100:", F(10100) - F(9700) / D)
annuity = {r: sum((1 / (1 + r) ** t for t in range(1, 4)), F(0)) for r in (F(8, 100), F(10, 100), F(12, 100))}
print("annuity 10% =", annuity[F(10, 100)], "=", float(annuity[F(10, 100)]))
be = {r: F(3000) / a for r, a in annuity.items()}
for r in be:
    print(f"rate {r}: break-even exact {be[r]} = {float(be[r]):.6f}")
print("M3 break-even 1000/(4*3310/1331) =", F(1000) / (4 * F(3310, 1331)), float(F(1000) / (4 * F(3310, 1331))))
print("M2 NPV at 10%:", -100 + F(60) / F(11, 10) + F(60) / F(11, 10) ** 2, float(-100 + F(60) / F(11, 10) + F(60) / F(11, 10) ** 2))


def npv_machine(units, r):
    cf = [F(-15_000_000)] + [F(units) * 5000] * 3
    return sum((c / (1 + r) ** t for t, c in enumerate(cf)), F(0))


print("NPV(200) exact", npv_machine(F(200), F(1, 10)), float(npv_machine(F(200), F(1, 10))))
print("NPV(1600) exact", npv_machine(F(1600), F(1, 10)), float(npv_machine(F(1600), F(1, 10))))
print("NPV(1200)", float(npv_machine(F(1200), F(1, 10))), "NPV(1300)", float(npv_machine(F(1300), F(1, 10))))
grid = list(range(200, 1601, 100))
pos = [u for u in grid if npv_machine(F(u), F(1, 10)) > 0]
neg = [u for u in grid if npv_machine(F(u), F(1, 10)) < 0]
print("grid positive:", pos, "count", len(pos), "largest negative:", max(neg), "first negative ascending", neg[0])
for r in (F(8, 100), F(12, 100)):
    print(f"NPV at 200 and 1600 at {r}:", float(npv_machine(F(200), r)), float(npv_machine(F(1600), r)))
u_be = {r: F(3000) / annuity[r] for r in annuity}
print("E3 unrounded:", float(u_be[F(8, 100)]), float(u_be[F(10, 100)]), float(u_be[F(12, 100)]))
w = u_be[F(12, 100)] - u_be[F(8, 100)]
print("width", float(w), "per point", float(w / 4), "8->10", float(u_be[F(10, 100)] - u_be[F(8, 100)]), "10->12", float(u_be[F(12, 100)] - u_be[F(10, 100)]))
print("displayed 1249.05-1206.34 =", round(1249.05 - 1206.34, 2))
print("R3 margin m* cents:", F(15_000_000) * F(1331, 3310) / 1600, float(F(15_000_000) * F(1331, 3310) / 1600))
mstar = F(15_000_000) * F(1331, 3310) / 1600
print("ratio", float(mstar / 5000), "fall %", float((1 - mstar / 5000) * 100))
print("E1 12% annuity approx", 1 / 1.12 + 1 / 1.2544 + 1 / 1.404928, "break-even", 3000 / (1 / 1.12 + 1 / 1.2544 + 1 / 1.404928))
print("E2 NPV(1200) approx", float(npv_machine(F(1200), F(1, 10))), "E2 NPV(1300) approx", float(npv_machine(F(1300), F(1, 10))))
print("Example 4.2 break-even", F(399300, 331), float(F(399300, 331)))
print("Remark 4.3 change 8->10", float(u_be[F(10, 100)] - u_be[F(8, 100)]), "10->12", float(u_be[F(12, 100)] - u_be[F(10, 100)]))
print("R1 ln2 check", math.log(4000 / 2000), math.log(2 / 1), math.log((1 / 5) / (1 / 10)))

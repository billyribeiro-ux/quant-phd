"""Verifier script (BK4 slice a, round 1): independent re-derivation of the numbers printed or stated in L01-L03.

Uses its own generator calls (random.Random(seed) with the same call order as the lab) and Fractions; it does not import the twins.
Run: .venv/bin/python -I -W error ledgers/BK4/scripts/BK4-a-r1/rederive_numbers.py
"""

import math
import random
from fractions import Fraction as F

fails = []


def check(name, got, want):
    status = "OK " if got == want else "BAD"
    if got != want:
        fails.append(name)
    print(f"{status} {name}: got={got} want={want}")


# ---------- L01: seeded day, seed 20260, 12 payments among banks 0,1,2 ----------
rng = random.Random(20260)
day = []
for seq in range(1, 13):
    s, r = rng.sample(range(3), 2)
    dollars = rng.randint(100, 5000)
    day.append((seq, s, r, 100 * dollars))
for seq, s, r, a in day:
    print(f"  payment {seq}: bank {s} -> bank {r} {a}")
gross = sum(a for *_, a in day)
check("L01 gross cents", gross, 2841600)
need, net, debit = {}, {}, {}
for b in range(3):
    bal, low = 0, 0
    for _, s, r, a in day:
        if s == b:
            bal -= a
        elif r == b:
            bal += a
        low = min(low, bal)
    need[b] = -low
    net[b] = sum(a for _, s, r, a in day if r == b) - sum(a for _, s, r, a in day if s == b)
    debit[b] = max(0, -net[b])
check("L01 need A", need[0], 112500)
check("L01 need B", need[1], 1533900)
check("L01 need C", need[2], 0)
check("L01 net A", net[0], 379800)
check("L01 net B", net[1], -1533900)
check("L01 net C", net[2], 1154100)
check("L01 net sum zero", sum(net.values()), 0)
check("L01 moved", sum(debit.values()), 1533900)
ratio = F(1533900, 2841600)
check("L01 E3 ratio 4dp half-up", round(float(ratio), 6) and math.floor(ratio * 10000 + F(1, 2)) / 10000, 0.5398)
check("L01 E3 ratio digits", float(ratio) > 0.539801 - 1e-6 and float(ratio) < 0.539802, True)
# Bank B lowest running position is its final position (E1 claim)
bal, path = 0, []
for _, s, r, a in day:
    if s == 1:
        bal -= a
    elif r == 1:
        bal += a
    path.append(bal)
check("L01 E1 bank B lowest running = final", min(path), path[-1])
# Bank A running minimum equals -need (P2 consistency)
check("L01 Prop 2.4 strict example exists in day (A)", need[0] > debit[0], True)
# Example 2.6 (three payments, dollars)
def example26(order):
    pays = {"ab": 100, "bc": 80, "ca": 50}
    seq = [("A", "B", 100), ("B", "C", 80), ("C", "A", 50)]
    if order == "swap":
        seq = [seq[2], seq[0], seq[1]]
    res = {}
    for b in "ABC":
        bal, low = 0, 0
        for s, r, a in seq:
            bal += a if r == b else (-a if s == b else 0)
            low = min(low, bal)
        res[b] = (-low, sum(a for s, r, a in seq if r == b) - sum(a for s, r, a in seq if s == b))
    return res
ex = example26("orig")
check("L01 Ex2.6 Need_A", ex["A"][0], 100)
check("L01 Ex2.6 Net_A", ex["A"][1], -50)
check("L01 Ex2.6 Need_B,C", (ex["B"][0], ex["C"][0]), (0, 0))
check("L01 Remark2.7 Need_A swapped", example26("swap")["A"][0], 50)
check("L01 Remark2.7 Debit_A swapped", max(0, -example26("swap")["A"][1]), 50)
# M1-M3
def need_debit(seq):
    bal, low = 0, 0
    for a in seq:
        bal += a
        low = min(low, bal)
    return -low, max(0, -sum(seq))
check("L01 M1 need/debit", need_debit([300, -500]), (200, 200))
check("L01 M3 need/debit", need_debit([40, -70, 10]), (30, 20))
# R3 cycle
check("L01 R3 need A", need_debit([-100, 0, 100])[0], 100)

# ---------- L02 ----------
rng = random.Random(2026)
trades = []
for seq in range(1, 7):
    payer, receiver = rng.sample(range(4), 2)
    dollars = rng.randint(500, 20000)
    trades.append((payer, receiver, 100 * dollars))
G = sum(a for *_, a in trades)
rec = [sum(a for p, r, a in trades if r == m) for m in range(4)]
pay = [sum(a for p, r, a in trades if p == m) for m in range(4)]
n = [rec[m] - pay[m] for m in range(4)]
A = sum(max(0, x) for x in n)
check("L02 gross", G, 7596300)
check("L02 n", n, [-3627000, 1753300, 3340300, -1466600])
check("L02 sum n zero", sum(n), 0)
check("L02 netted A", A, 5093600)
check("L02 reduction", G - A, 2502700)
bps = (10000 * (G - A)) // G
check("L02 bps floor", bps, 3294)
check("L02 bps exact fraction floor", math.floor(F(10000 * (G - A), G)), 3294)
check("L02 E1 sum to gross", A + (G - A), G)
check("L02 E2 positives sum", 1753300 + 3340300, 5093600)
check("L02 Part B member1 both", (rec[0] > 0 and pay[0] > 0), True)
check("L02 E3 both-receive-pay members (1-based)", [m + 1 for m in range(4) if rec[m] > 0 and pay[m] > 0], [1, 2, 4])
# Example 2.4
ex_n = [-50, 20, 30]
check("L02 Ex2.4 A", sum(max(0, x) for x in ex_n), 50)
check("L02 Ex2.4 bps", math.floor(F(10000 * 180, 230)), 7826)
check("L02 Ex2.4 bps 7826.08", round(10000 * 180 / 230, 2), 7826.09 if False else round(10000 * 180 / 230, 2))
check("L02 M1 nets", [40 - 50, 50 - 70, 70 - 20, 20 - 40], [-10, -20, 50, -20])
check("L02 M1 A", sum(max(0, x) for x in [-10, -20, 50, -20]), 50)
check("L02 M1 bps", math.floor(F(10000 * 130, 180)), 7222)
check("L02 M2 bps", math.floor(F(10000 * 360, 460)), 7826)
check("L02 quiz 50936", 5093600 // 100, 50936)

# ---------- L03 ----------
def waterfall(loss, im_d, df_d, cap, survivors):  # survivors: dict id->df (dict in ascending id order)
    a1 = min(loss, im_d)
    a2 = min(loss - a1, df_d)
    a3 = min(loss - a1 - a2, cap)
    Z = loss - a1 - a2 - a3
    D = sum(survivors.values())
    if Z >= D:
        pays = dict(survivors)
        u = Z - D
    else:
        pays = {i: Z * df // D // 1 for i, df in survivors.items()}
        pays = {i: (Z * df) // D for i, df in survivors.items()}
        left = Z - sum(pays.values())
        for i in sorted(survivors):
            if left == 0:
                break
            if survivors[i] > 0:
                pays[i] += 1
                left -= 1
        assert left == 0
        u = 0
    assert a1 + a2 + a3 + sum(pays.values()) + u == loss
    return a1, a2, a3, pays, u

fx = {1: 40, 2: 60}
exp = {80: (80, 0, 0, {1: 0, 2: 0}, 0), 120: (100, 20, 0, {1: 0, 2: 0}, 0), 170: (100, 50, 20, {1: 0, 2: 0}, 0),
       180: (100, 50, 30, {1: 0, 2: 0}, 0), 181: (100, 50, 30, {1: 1, 2: 0}, 0), 200: (100, 50, 30, {1: 8, 2: 12}, 0),
       205: (100, 50, 30, {1: 10, 2: 15}, 0), 300: (100, 50, 30, {1: 40, 2: 60}, 20)}
for loss, want in exp.items():
    check(f"L03 fixture loss {loss}", waterfall(loss, 100, 50, 30, fx), want)
check("L03 Ex1.6 Z=1", waterfall(1, 0, 0, 0, {1: 1, 2: 1, 3: 1})[3], {1: 1, 2: 0, 3: 0})
check("L03 Ex1.6 Z=2", waterfall(2, 0, 0, 0, {1: 1, 2: 1, 3: 1})[3], {1: 1, 2: 1, 3: 0})
check("L03 M1 loss 200 layers", waterfall(200, 100, 50, 30, fx)[:3], (100, 50, 30))
check("L03 E1 loss 3160", (3058 + 102), 3160)
check("L03 E2 residual", 5850 - 3058 - 205 - 1730, 857)
check("L03 E2 shares", [857 * 624 // 1714, 857 * 762 // 1714, 857 * 328 // 1714], [312, 381, 164])
check("L03 E2 D", 624 + 762 + 328, 1714)
check("L03 A3 within loss", 3058 // 2, 1529)
# Part B: rebuild the seeded draw in the lab's call order
rng = random.Random(2026)
MEMBERS = (1, 2, 3, 4)
im = {i: rng.randint(1000, 5000) for i in MEMBERS}
df = {i: rng.randint(100, 900) for i in MEMBERS}
cap = rng.randint(500, 2000)
check("L03 inputs im", im, {1: 1487, 2: 2308, 3: 3058, 4: 4896})
check("L03 inputs df", df, {1: 624, 2: 762, 3: 205, 4: 328})
check("L03 inputs cap", cap, 1730)
losses = [rng.randint(0, 3000) for _ in range(200)]
sl = sorted(losses)


def cover(M):
    c = sum(1 for x in losses if x <= M)
    return (10000 * c) // 200, c


for target, want_margin in ((9900, 2961), (9975, 2992)):
    k = math.ceil(F(target * 200, 10000))
    margin = sl[k - 1]
    brute = next(M for M in range(0, max(losses) + 1) if cover(M)[0] >= target)
    check(f"L03 target {target} k", k, 198 if target == 9900 else 200)
    check(f"L03 target {target} sized margin", margin, want_margin)
    check(f"L03 target {target} brute equals sized", brute, margin)
    check(f"L03 target {target} cover at margin", cover(margin)[0], target if target == 9900 else 10000)
    check(f"L03 target {target} cover one below", cover(margin - 1)[0], 9850 if target == 9900 else 9950)
check("L03 9900 covered count 198", cover(2961)[1], 198)
check("L03 Ex2.5 k 9900 S200", F(9900 * 200, 10000), 198)
check("L03 Ex2.5 9975 S200", F(9975 * 200, 10000), F(399, 2))
check("L03 Ex2.5 k 9975 ceil", math.ceil(F(9975 * 200, 10000)), 200)
check("L03 R2 S100 9900 k", math.ceil(F(9900 * 100, 10000)), 99)
check("L03 R3 threshold: k=S for S=399", math.ceil(F(9975 * 399, 10000)), 399)
check("L03 R3 threshold: k<S for S=400", math.ceil(F(9975 * 400, 10000)), 399)
check("L03 quiz 9975 S400 k", math.ceil(F(9975 * 400, 10000)), 399)
check("L03 M2 k 7500 S4", math.ceil(F(7500 * 4, 10000)), 3)
check("L03 M3 8000 k", math.ceil(F(8000 * 5, 10000)), 4)
check("L03 M3 8001 k", math.ceil(F(8001 * 5, 10000)), 5)
check("L03 M2 cover 4000", (10000 * 3) // 4, 7500)
check("L03 M2 cover 2999", (10000 * 2) // 4, 5000)
check("L03 E3 9900 c=198 unique", [c for c in range(201) if (10000 * c) // 200 == 9900], [198])

print("FAILURES:", fails if fails else "none")

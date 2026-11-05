"""Independent recomputation of every number the BK4 slice pages (index, L01, L02, L03) print or state.

Uses fractions.Fraction and different algorithms from the lab twins (no shared code). Run: python3 -I recompute_numbers.py
"""

from fractions import Fraction
import math
import random


FAILS = []


def check(name, got, want):
    status = "OK" if got == want else "MISMATCH"
    print(f"{status:9s} {name}: got {got!r} want {want!r}")
    if got != want:
        FAILS.append(name)
    return got == want


ok = True
# ---- L01: recompute the seeded day with a separate generator call order (same seed, same draws)
rng = random.Random(20260)
pay = []
for seq in range(12):
    a, b = rng.sample([0, 1, 2], 2)
    dollars = rng.randint(100, 5000)
    pay.append((a, b, 100 * dollars))
gross = sum(p[2] for p in pay)
check("L01 gross cents", gross, 2841600)
net = [0, 0, 0]
for a, b, c in pay:
    net[a] -= c
    net[b] += c
check("L01 net positions", net, [379800, -1533900, 1154100])
check("L01 net sum zero", sum(net), 0)
need = []
for bank in range(3):
    bal, low = 0, 0
    for a, b, c in pay:  # sending order
        if a == bank:
            bal -= c
        if b == bank:
            bal += c
        low = min(low, bal)
    need.append(-low)
check("L01 RTGS peak need", need, [112500, 1533900, 0])
debit = [max(0, -x) for x in net]
check("L01 DNS debit", debit, [0, 1533900, 0])
check("L01 moved share 1533900/2841600 to 6 places (0.53980152 rounds to 0.539802)",
      round(Fraction(1533900, 2841600) * 10**6), 539802)
check("L01 ratio rounded to 4 places (half up)", round(float(Fraction(1533900, 2841600)), 4), 0.5398)
r = Fraction(1533900, 2841600)
check("L01 share x 10000 floored to 4 places (53.98 percent)", math.floor(r * 10000), 5398)
check("L01 Example 2.6 need A", max(0, -min(0, -100, -100, -50)), 100)
check("L01 Remark 2.7 need A", max(0, -min(0, 50, -50, -50)), 50)
check("L01 M3 need", max(0, -min(0, 40, -30, -20)), 30)
check("L01 M3 debit", max(0, -(-20)), 20)
check("L01 E3 2841600 cents = 28416 dollars", 2841600 // 100, 28416)

# ---- L02
rng = random.Random(2026)
trades = []
for seq in range(6):
    payer, rec = rng.sample([0, 1, 2, 3], 2)
    dollars = rng.randint(500, 20000)
    trades.append((payer, rec, 100 * dollars))
G = sum(t[2] for t in trades)
check("L02 gross notional", G, 7596300)
rec = [sum(t[2] for t in trades if t[1] == m) for m in range(4)]
pay_ = [sum(t[2] for t in trades if t[0] == m) for m in range(4)]
check("L02 receivables", rec, [314500, 2067800, 3340300, 1873700])
check("L02 payables", pay_, [3941500, 314500, 0, 3340300])
n = [rec[m] - pay_[m] for m in range(4)]
check("L02 net obligations", n, [-3627000, 1753300, 3340300, -1466600])
A = sum(max(0, x) for x in n)
check("L02 netted amount", A, 5093600)
check("L02 A equals payers side", A, sum(max(0, -x) for x in n))
check("L02 reduction cents", G - A, 2502700)
check("L02 reduction bps floored", math.floor(Fraction(10000 * (G - A), G)), 3294)
check("L02 Example 2.4 bps floored", math.floor(Fraction(10000 * 180, 230)), 7826)
check("L02 M1 bps floored", math.floor(Fraction(10000 * 130, 180)), 7222)
check("L02 M2 bps floored (doubled)", math.floor(Fraction(10000 * 360, 460)), 7826)
check("L02 E3 members both receive and pay", [m + 1 for m in range(4) if rec[m] > 0 and pay_[m] > 0], [1, 2, 4])

# ---- L03: fixtures and sizing, with a different algorithm (Fraction and linear scan)
def layers(loss, im, df, capital, defaulter, survivors):
    a1 = min(loss, im[defaulter])
    a2 = min(loss - a1, df[defaulter])
    a3 = min(loss - a1 - a2, capital)
    z = loss - a1 - a2 - a3
    D = sum(df[i] for i in survivors)
    if z >= D:
        pays = {i: df[i] for i in survivors}
        u = z - D
    else:
        pays = {i: math.floor(Fraction(z * df[i], D)) for i in survivors}
        left = z - sum(pays.values())
        for i in survivors:
            if left and df[i] > 0:
                pays[i] += 1
                left -= 1
        u = 0
        assert left == 0
    total = a1 + a2 + a3 + sum(pays.values()) + u
    assert total == loss
    return a1, a2, a3, pays, u


im = {1: 0, 2: 0, 3: 100}
df = {1: 40, 2: 60, 3: 50}
for loss, want in [(80, (80, 0, 0, {1: 0, 2: 0}, 0)), (120, (100, 20, 0, {1: 0, 2: 0}, 0)),
                   (170, (100, 50, 20, {1: 0, 2: 0}, 0)), (180, (100, 50, 30, {1: 0, 2: 0}, 0)),
                   (181, (100, 50, 30, {1: 1, 2: 0}, 0)), (200, (100, 50, 30, {1: 8, 2: 12}, 0)),
                   (205, (100, 50, 30, {1: 10, 2: 15}, 0)), (300, (100, 50, 30, {1: 40, 2: 60}, 20))]:
    a1, a2, a3, pays, u = layers(loss, im, df, 30, 3, [1, 2])
    ok = check(f"L03 fixture loss {loss}", (a1, a2, a3, pays, u), want) and ok
im4 = {4: 0, 1: 0, 2: 0, 3: 0}
df4 = {1: 1, 2: 1, 3: 1, 4: 0}
check("L03 remainder residual 1", layers(1, im4, df4, 0, 4, [1, 2, 3])[3], {1: 1, 2: 0, 3: 0})
check("L03 remainder residual 2", layers(2, im4, df4, 0, 4, [1, 2, 3])[3], {1: 1, 2: 1, 3: 0})

# Seeded inputs of Part A3 and Part B
rng = random.Random(2026)
im_s = {i: rng.randint(1000, 5000) for i in (1, 2, 3, 4)}
df_s = {i: rng.randint(100, 900) for i in (1, 2, 3, 4)}
cap = rng.randint(500, 2000)
check("L03 seeded initial margins", [im_s[i] for i in (1, 2, 3, 4)], [1487, 2308, 3058, 4896])
check("L03 seeded default funds", [df_s[i] for i in (1, 2, 3, 4)], [624, 762, 205, 328])
check("L03 seeded capital", cap, 1730)
surv = [1, 2, 4]
sdf = sum(df_s[i] for i in surv)
check("L03 A3 surviving scenario loss", 3058 + 205 + 1730 + sdf // 2, 5850)
a = layers(5850, im_s, df_s, cap, 3, surv)
check("L03 A3 surviving payments", (a[3], a[4]), ({1: 312, 2: 381, 4: 164}, 0))
check("L03 A3 within margin", layers(1529, im_s, df_s, cap, 3, surv)[0], 1529)
check("L03 A3 default fund scenario", (layers(3160, im_s, df_s, cap, 3, surv)[0], layers(3160, im_s, df_s, cap, 3, surv)[1]), (3058, 102))

losses = [rng.randint(0, 3000) for _ in range(200)]
for target, want_k, want_m in [(9900, 198, 2961), (9975, 200, 2992)]:
    k = math.ceil(Fraction(target * 200, 10000))
    s = sorted(losses)
    m_sized = s[k - 1]
    cover = lambda M: math.floor(Fraction(10000 * sum(1 for x in losses if x <= M), 200))
    ok = check(f"L03 target {target} k", k, want_k) and ok
    ok = check(f"L03 target {target} sized margin", m_sized, want_m) and ok
    brute = next(M for M in range(0, 3001) if cover(M) >= target)
    ok = check(f"L03 target {target} brute-force minimum", brute, want_m) and ok
    ok = check(f"L03 target {target} cover at sized margin", cover(m_sized), 9900 if target == 9900 else 10000) and ok
    ok = check(f"L03 target {target} cover one cent below", cover(m_sized - 1), 9850 if target == 9900 else 9950) and ok
print("ALL OK" if not FAILS else f"MISMATCHES: {FAILS}")

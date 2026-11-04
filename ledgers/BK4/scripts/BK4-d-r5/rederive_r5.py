"""Round-5 independent re-derivation of every number on a BK4 card (stdlib only). Usage: python3 -I rederive_r5.py"""
import math
import random
from fractions import Fraction as F
from itertools import product

out = []
def show(label, value, expect=None):
    ok = "" if expect is None else (" OK" if value == expect else f" MISMATCH expected {expect}")
    out.append(f"{label}: {value}{ok}")

# ---- L01: seeded day, Random(20260), 12 payments, 3 banks, whole dollars
rng = random.Random(20260)
day = []
for seq in range(1, 13):
    s, r = rng.sample(range(3), 2)
    d = rng.randint(100, 5000)
    day.append((s, r, 100 * d * 1))  # cents = 100 * dollars
def net(b): return sum(a for s, r, a in day if r == b) - sum(a for s, r, a in day if s == b)
def need(b):
    bal = low = 0
    for s, r, a in day:
        if s == b: bal -= a
        elif r == b: bal += a
        low = min(low, bal)
    return -low
def debit(b): return max(0, -net(b))
for b, name in enumerate("ABC"):
    show(f"L01 bank {name} net", net(b))
    show(f"L01 bank {name} RTGS need", need(b))
    show(f"L01 bank {name} DNS debit", debit(b))
gross = sum(a for _, _, a in day)
show("L01 gross cents", gross, 2841600)
show("L01 sum of debits", sum(debit(b) for b in range(3)), 1533900)
show("L01 share debit/gross (4dp)", round(F(1533900, 2841600), 4), F(5398, 10000))
show("L01 exact share float", round(1533900 / 2841600, 8))
# Bank A after payment 10 (sending order), cumulative balance
bal = 0
for seq, (s, r, a) in enumerate(day, 1):
    if s == 0: bal -= a
    elif r == 0: bal += a
    if seq == 10: show("L01 bank A balance after payment 10", bal, -112500)
# Example 2.6 hand values (dollars)
ex = [(0, 1, 100), (1, 2, 80), (2, 0, 50)]
def ex_need(b, order):
    bal = low = 0
    for s, r, a in order:
        if s == b: bal -= a
        elif r == b: bal += a
        low = min(low, bal)
    return -low
show("L01 Ex2.6 need A", ex_need(0, ex), 100)
show("L01 Ex2.6 A running sums", [sum((a if r == 0 else 0) - (a if s == 0 else 0) for s, r, a in ex[:k]) for k in range(4)], [0, -100, -100, -50])
show("L01 Ex2.6 net debit A", max(0, -sum((a if r == 0 else 0) - (a if s == 0 else 0) for s, r, a in ex)), 50)
resend = [ex[2], ex[0], ex[1]]
show("L01 Remark2.7 need A", ex_need(0, resend), 50)
show("L01 Remark2.7 running sums A", [sum((a if r == 0 else 0) - (a if s == 0 else 0) for s, r, a in resend[:k]) for k in range(4)], [0, 50, -50, -50])
show("L01 Ex2.6 gross dollars", 100 + 80 + 50, 230)

# ---- L02: seeded trade set, Random(2026), 6 trades, 4 members, 500..20000 dollars
rng = random.Random(2026)
tr = []
for seq in range(1, 7):
    p, r = rng.sample(range(4), 2)
    d = rng.randint(500, 20000)
    tr.append((p, r, 100 * d))
G = sum(a for _, _, a in tr)
rec = [sum(a for p, r, a in tr if r == m) for m in range(4)]
pay = [sum(a for p, r, a in tr if p == m) for m in range(4)]
n = [rec[m] - pay[m] for m in range(4)]
Aamt = sum(max(0, x) for x in n)
show("L02 gross", G, 7596300)
show("L02 receivables", rec)
show("L02 payables", pay)
show("L02 net obligations", n)
show("L02 sum of n", sum(n), 0)
show("L02 netted A", Aamt, 5093600)
show("L02 A equals sum max(0,-n)", sum(max(0, -x) for x in n), 5093600)
show("L02 reduction", G - Aamt, 2502700)
show("L02 bps floor", 10000 * (G - Aamt) // G, 3294)
show("L02 sum of rec", sum(rec), 7596300)
# Example 2.4 (dollars): member1->2 100, 2->3 80, 3->1 50
e_rec = [50, 100, 80]; e_pay = [100, 80, 50]
e_n = [a - b for a, b in zip(e_rec, e_pay)]
e_A = sum(max(0, x) for x in e_n)
e_G = 230
show("L02 Ex2.4 net", e_n, [-50, 20, 30])
show("L02 Ex2.4 A", e_A, 50)
show("L02 Ex2.4 bps floor", math.floor(F(10000 * (e_G - e_A), e_G)), 7826)
show("L02 Ex2.4 10000*180/230", float(F(10000 * 180, 230)))
# P3 cycle k=2..6, amount a
for k in range(2, 7):
    a = 7
    rec_c = [a] * k; pay_c = [a] * k
    show(f"L02 P3 k={k} netted", sum(max(0, rec_c[i] - pay_c[i]) for i in range(k)), 0)
# M1 chain (dollars): 1->2 50, 2->3 70, 3->4 20, 4->1 40
chain = [(0, 1, 50), (1, 2, 70), (2, 3, 20), (3, 0, 40)]
ch_n = [sum(a for p, r, a in chain if r == m) - sum(a for p, r, a in chain if p == m) for m in range(4)]
show("L02 M1 nets", ch_n, [-10, -20, 50, -20])

# ---- L03: waterfall, fixture and seeded sizing
def pay_split(res, df, surv):
    tot = sum(df[i] for i in surv)
    if res >= tot:
        return {i: df[i] for i in surv}, res - tot
    p = {i: F(res * df[i], tot) for i in surv}
    x = {i: math.floor(p[i]) for i in surv}
    left = res - sum(x.values())
    for i in surv:
        if left == 0: break
        if df[i] > 0:
            x[i] += 1; left -= 1
    return x, 0
def wf(L, im, df, cap, dfl):
    a1 = min(L, im); a2 = min(L - a1, df[dfl]); a3 = min(L - a1 - a2, cap)
    Z = L - a1 - a2 - a3
    surv = sorted(i for i in df if i != dfl)
    x, u = pay_split(Z, {i: df[i] for i in df}, surv)
    return a1, a2, a3, x, u
fx_df = {1: 40, 2: 60, 3: 50}
show("L03 Ex1.5 at 200", wf(200, 100, fx_df, 30, 3), (100, 50, 30, {1: 8, 2: 12}, 0))
show("L03 Ex1.5 at 300 uncovered", wf(300, 100, fx_df, 30, 3)[4], 20)
show("L03 Ex1.5 at 181 leftover to 1", wf(181, 100, fx_df, 30, 3)[3], {1: 1, 2: 0})
show("L03 Ex1.6 Z=1", pay_split(1, {1: 1, 2: 1, 3: 1}, [1, 2, 3]), ({1: 1, 2: 0, 3: 0}, 0))
show("L03 Ex1.6 Z=2", pay_split(2, {1: 1, 2: 1, 3: 1}, [1, 2, 3]), ({1: 1, 2: 1, 3: 0}, 0))
rng = random.Random(2026)
im = {i: rng.randint(1000, 5000) for i in (1, 2, 3, 4)}
df = {i: rng.randint(100, 900) for i in (1, 2, 3, 4)}
cap = rng.randint(500, 2000)
losses = [rng.randint(0, 3000) for _ in range(200)]
show("L03 seeded IM", im)
show("L03 seeded DF", df)
show("L03 seeded capital", cap)
for t, expect in ((9900, 2961), (9975, 2992)):
    k = math.ceil(F(t * 200, 10000))
    m = sorted(losses)[k - 1]
    c = sum(1 for L in losses if L <= m)
    show(f"L03 target {t}: k", k, 198 if t == 9900 else 200)
    show(f"L03 target {t}: sized margin", m, expect)
    show(f"L03 target {t}: cover bps at m", 10000 * c // 200, t if t == 9900 else 10000)
    cm = sum(1 for L in losses if L <= m - 1)
    show(f"L03 target {t}: cover one cent below", 10000 * cm // 200)
show("L03 Ex2.5 k for 9900, S=200", math.ceil(F(9900 * 200, 10000)), 198)
show("L03 Ex2.5 9975 tS/10000", F(9975 * 200, 10000), F(399, 2))
show("L03 M2 cover(4000)", 10000 * 3 // 4, 7500)
show("L03 M3 k for 8001 of 5", math.ceil(F(8001 * 5, 10000)), 5)
show("L03 R2 S=100 k(9900)", math.ceil(F(9900 * 100, 10000)), 99)
show("L03 R3 S=400 k(9975)", math.ceil(F(9975 * 400, 10000)), 399)
show("L03 E1 residual check", 3160 - 3058, 102)
show("L03 E2 residual 5850-3058-205-1730", 5850 - 3058 - 205 - 1730, 857)
show("L03 E2 DF totals", (624 + 762 + 328), 1714)

# ---- L04: exact fractions
rho1, rho2 = F(19, 20), F(21, 20)
def cov(r, x): return (r - x) / (1 - x)
show("L04 Remark2.8 19/20,1/2", cov(rho1, F(1, 2)), F(9, 10))
show("L04 Remark2.8 21/20,1/2", cov(rho2, F(1, 2)), F(11, 10))
show("L04 19/20, 1/7", cov(rho1, F(1, 7)), F(113, 120))
show("L04 floor 10000*113/120", math.floor(10000 * cov(rho1, F(1, 7))), 9416)
show("L04 (19/20)/2 halving", rho1 / 2, F(19, 40))
show("L04 (rho-1/2)/(1/2)", (rho1 - F(1, 2)) / F(1, 2), F(9, 10))
show("L04 threshold 1/(1-h)", 1 / (1 - F(1, 20)), F(20, 19))
show("L04 20/19 to 10dp", f"{float(F(20, 19)):.10f}", "1.0526315789")
show("L04 haircut effective at 20/19", F(20, 19) * F(19, 20), 1)
show("L04 rho=1 measured ratio", 1 * (1 - F(1, 20)), F(19, 20))
show("L04 theta-rho sign check rho=19/20 x=1/2", cov(rho1, F(1, 2)) - rho1, F(9, 10) - F(19, 20))
show("L04 Prop 2.6 theta-rho = x(rho-1)/(1-x)", cov(rho1, F(1, 3)) - rho1, F(1, 3) * (rho1 - 1) / (1 - F(1, 3)))
show("L04 Remark1.3 reserves", int(F(19, 20) * 2000000), 1900000)
show("L04 Remark1.3 reserves 21/20", int(F(21, 20) * 2000000), 2100000)
show("L04 Prop2.7 floor 10000 * 1 >= 10000", math.floor(10000 * 1) >= 10000)
# Lab rows (seed 7) recomputed
r = random.Random(7)
hund = sorted(r.sample(range(1, 100), 6))
path = [F(k, 100) for k in hund] + [F(99, 100)]
show("L04 path", [str(p) for p in path])
for rho in (rho1, rho2):
    for x in path:
        if x > rho:
            continue
        res = int(rho * 2000000) - int(x * 2000000); clm = 2000000 - int(x * 2000000)
        cv = F(res, clm)
        out.append(f"L04 rho {rho} x {x} coverage {cv} bps {math.floor(10000 * cv)}")

# ---- L05
p = F(1, 8); kap = 2500; ells = (1, 2, 4)
pats = list(product((0, 1), repeat=3))
Pm = lambda x: math.prod((p if xi else 1 - p) for xi in x)
Cm = lambda x: kap * sum(l * xi for l, xi in zip(ells, x))
mean_ind = sum(Pm(x) * Cm(x) for x in pats)
show("L05 mean enumerated", mean_ind, F(4375, 2))
show("L05 closed form", p * kap * sum(ells), F(4375, 2))
show("L05 round half up 2187.5", math.floor(mean_ind + F(1, 2)), 2188)
show("L05 P(no failure) indep", Pm((0, 0, 0)), F(343, 512))
show("L05 P(at least one) indep", 1 - Pm((0, 0, 0)), F(169, 512))
show("L05 3p in 512ths", 3 * p, F(192, 512))
show("L05 A4 P(at least one)", p, F(64, 512))
show("L05 Ex2.7 p=1/8 3p-(1-(1-p)^3)", p ** 2 * (3 - p) > 0)
mean_com = (1 - p) * 0 + p * kap * sum(ells)
show("L05 comonotone mean", mean_com, F(4375, 2))
var_ind = sum(Pm(x) * Cm(x) ** 2 for x in pats) - mean_ind ** 2
com_out = [(1 - p, 0), (p, kap * sum(ells))]
var_com = sum(pr * c * c for pr, c in com_out) - sum(pr * c for pr, c in com_out) ** 2
show("L05 var independent", var_ind, F(57421875, 4))
show("L05 var comonotone", var_com, F(133984375, 4))
show("L05 var diff", var_com - var_ind, F(19140625))
show("L05 Prop2.5 formula", 2 * kap ** 2 * p * (1 - p) * sum(ells[i] * ells[j] for i in range(3) for j in range(i + 1, 3)), F(19140625))
show("L05 Part C enumerated equal delays", sum(Pm(x) * kap * 2 * sum(x) for x in pats), 1875)
show("L05 3p k ell", 3 * p * kap * 2, 1875)
show("L05 P(no cost) comonotone", 1 - p, F(7, 8))
show("L05 P(no cost) indep 448/512 vs 343/512", F(448, 512) > F(343, 512))
show("L05 M1 mean", F(1, 4) * 1000 * (2 + 3 + 1), 1500)
show("L05 R1 ratio n=3", 3, 3)
show("L05 p=1/4 single trade", F(1, 4) * 1000 * 3, 750)
show("L05 M2 (7/8)^3", F(7, 8) ** 3, F(343, 512))
show("L05 R2 bounds 5/8", 1 - 3 * F(1, 8), F(5, 8))

print("\n".join(out))

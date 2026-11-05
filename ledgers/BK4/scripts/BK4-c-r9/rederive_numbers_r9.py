"""Round-9 independent re-derivation of every number on project.html Labs 1-3 and exemplar B (own code, not the lab code)."""
import random
from fractions import Fraction
import math

MARGIN = {1: 30000, 2: 50000, 3: 40000, 4: 20000}
FUND = {1: 4000, 2: 6000, 3: 5000, 4: 3000}
K = 20000
D = 2

def pay(L, im, df, cap, defaulter=D, fund=FUND):
    a1 = min(L, im)
    a2 = min(L - a1, df)
    a3 = min(L - a1 - a2, cap)
    R = L - a1 - a2 - a3
    surv = sorted(m for m in fund if m != defaulter)
    T = sum(fund[m] for m in surv)
    if R >= T:
        return a1, a2, a3, {m: fund[m] for m in surv}, R - T
    sh = {m: (R * fund[m]) // T for m in surv}
    r = R - sum(sh.values())
    for m in surv:
        if r > 0 and fund[m] > 0:
            sh[m] += 1
            r -= 1
    return a1, a2, a3, sh, 0

# Lab 1
print("lab1 layers", pay(80000, MARGIN[D], FUND[D], K))
rng = random.Random(1)
losses = [rng.randint(0, 120000) for _ in range(40)]
print("max loss", max(losses), "n", len(losses))
s = sorted(losses)
for t in (9550, 9500, 9000, 9750):
    k = math.ceil(Fraction(t * 40, 10000))
    exact = Fraction(t * 40, 10000)
    m = s[k - 1]
    cov = Fraction(10000 * sum(1 for x in losses if x <= m), 40)
    covb = Fraction(10000 * sum(1 for x in losses if x <= m - 1), 40)
    cov_floor = (10000 * sum(1 for x in losses if x <= m)) // 40
    covb_floor = (10000 * sum(1 for x in losses if x <= m - 1)) // 40
    # brute force: least whole-cent margin with floored cover >= t
    bf = next(M for M in range(0, 120001) if (10000 * sum(1 for x in losses if x <= M)) // 40 >= t)
    print(f"t={t} exact={float(exact)} k={k} margin={m} cover={cov_floor} below={covb_floor} brute={bf}")
# Lab 2 shares
pool = 12000; R = 4000
print("lab2 floored", {m: R * FUND[m] // pool for m in (1, 3, 4)})
# Lab 3 Part A
for loss in (20000, 55000, 70000, 80000, 100000):
    print("A", loss, pay(loss, MARGIN[D], FUND[D], K))
# Lab 3 Part C
for t in (9500, 9000):
    k = math.ceil(Fraction(t * 40, 10000)); m = s[k - 1]
    past_m = sum(1 for x in losses if x > m)
    past_f = sum(1 for x in losses if x > m + FUND[D])
    past_c = sum(1 for x in losses if x > m + FUND[D] + K)
    past_s = sum(1 for x in losses if x > m + FUND[D] + K + 12000)
    print("C", t, m, past_m, past_f, past_c, past_s)
# Exemplar B arithmetic
print("1334+1666+1000 =", 1334 + 1666 + 1000, "| 111074-105154 =", 111074 - 105154, "| 9500-9000 =", 9500 - 9000)
print("exemplar B 9500 exact position", Fraction(9500 * 40, 10000), "k", math.ceil(Fraction(9500 * 40, 10000)))
print("sum of 4000 residual shares", 1333 + 1666 + 1000, "| pool", 4000 + 5000 + 3000)
print("layer order check 70000:", pay(70000, 50000, 6000, 20000)[:3])
# fixture checks
# layer-order fixture: defaulter 3, IM 100, DF 50, capital 30, survivors 1:40, 2:60
F2 = {1: 40, 2: 60, 3: 50}
for L in (80, 100, 120, 150, 151, 170, 180, 181, 200, 205, 300):
    print("fix", L, pay(L, 100, 50, 30, defaulter=3, fund=F2))
# remainder fixture
F3 = {1: 1, 2: 1, 3: 1, 4: 0}
for L in (1, 2, 4):
    print("rem", L, pay(L, 0, 0, 0, defaulter=4, fund={1:1,2:1,3:1,4:1}))
# sizing fixtures
def margin_for(ls, t):
    k = math.ceil(Fraction(t * len(ls), 10000)); return sorted(ls)[k - 1]
print("size 8000", margin_for([10,20,30,40,50], 8000), "8001", margin_for([10,20,30,40,50], 8001), "10000", margin_for([10,20,30,40,50], 10000), "5000 of 4", margin_for([10,20,30,40], 5000))
print("cover fix1", 10000 * sum(1 for x in [1,5,9] if x <= 4) // 3, "cover fix2", 10000 * sum(1 for x in [1,2,9] if x <= 2) // 3, Fraction(20000, 3))

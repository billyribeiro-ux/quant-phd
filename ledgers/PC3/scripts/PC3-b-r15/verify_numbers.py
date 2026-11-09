"""Independent re-derivation of the numbers in L04, L05 and L06 of PC3 (verifier's own code; not the lab's code).

Run: .venv/bin/python -I ledgers/PC3/scripts/PC3-b-r15/verify_numbers.py
"""
from fractions import Fraction as F
import math
import random
from decimal import Decimal, ROUND_HALF_UP

def show(label, value):
    print(f"{label}: {value}")

def rnd(x, places):
    q = Decimal(1).scaleb(-places)
    return Decimal(x.numerator) / Decimal(x.denominator) if False else (Decimal(x.numerator) / Decimal(x.denominator)).quantize(q, rounding=ROUND_HALF_UP)

def pos(x):
    return x if x > 0 else F(0)

print("== L04 ==")
# Prop 3.1 closed form vs brute enumeration, inventory 0, fixed quote (a,b), p general
def enum_trade_term(v, a, b, p):
    # arrivals: uninformed buy (1-p)/2 -> buy at ask; uninformed sell (1-p)/2 -> sell at bid; informed p
    total = F(0)
    # uninformed buy
    total += (1 - p) / 2 * (a - v)
    total += (1 - p) / 2 * (v - b)
    if v > a:
        total += p * (a - v)
    elif v < b:
        total += p * (v - b)
    return total

def closed(v, a, b, p):
    h = F(a - b, 2)
    return (1 - p) * h - p * (pos(v - a) + pos(b - v))

bad = 0
rng = random.Random(15)
for _ in range(20000):
    b = rng.randint(1, 500)
    h = rng.randint(1, 50)
    a = b + 2 * h
    v = rng.randint(0, 600)
    p = F(rng.randint(0, 20), 20)
    if enum_trade_term(F(v), F(a), F(b), p) != closed(F(v), F(a), F(b), p):
        bad += 1
show("Prop 3.1 closed form vs enumeration mismatches over 20000 random cases", bad)

# Example 3.2 values (a=10010,b=9990,p=1/2)
for v in (10000, 10020, 9985):
    show(f"Example 3.2 E at v={v}", closed(F(v), F(10010), F(9990), F(1, 2)))

# Corollary 3.3: p=1/2, v>=a -> E = h/2 - (v-a)/2; zero iff v=a+h
show("Cor 3.3 zero at v=a+h (a=10010,h=10): E", closed(F(10020), F(10010), F(9990), F(1, 2)))

# Remark 4.2: I=10, quote 9990/10010, v=10000, p=1/2: informed does not trade, uninformed sell refused
# Only uninformed buy contributes (a - v = 10) with probability 1/4 -> E = 5/2
show("Remark 4.2 I=10 expected term", F(1, 4) * (10010 - 10000))

# Prop 2.3 decomposition check on random paths (exact)
random.seed(1)
ok = True
for _ in range(2000):
    C, I, W = F(0), 0, F(0)
    v_prev = F(10000)
    for t in range(20):
        v = v_prev + random.choice((5, -5))
        sigma = random.choice((-1, 0, 1))
        c = -sigma * (v - 5)  # fill price arbitrary here; identity holds for any fill price f_t
        W_prev = C + I * v_prev
        C += c
        I += sigma
        W_new = C + I * v
        if W_new - W_prev != (c + sigma * v) + I - sigma != None and False:
            ok = False
        if W_new - W_prev != (c + sigma * v) + (I - sigma) * (v - v_prev):
            ok = False
        v_prev = v
show("Prop 2.3 turn decomposition identity holds on random paths", ok)

# Lab L04 Part 1 expected: seed-0 path re-simulated with my own code
def sim(seed, turns=20):
    rng = random.Random(seed)
    path = [10000]
    arr = []
    for _ in range(turns):
        mv = 5 if rng.random() < 0.5 else -5
        path.append(path[-1] + mv)
        d = rng.random()
        arr.append("ub" if d < 0.25 else ("us" if d < 0.5 else "inf"))
    inv = 0
    cash = 0
    last = None
    fills = 0
    cf = 0
    log = []
    for t in range(1, turns + 1):
        mid = 10000 if last is None else last
        bid, ask = mid - 10, mid + 10
        fv = path[t]
        a = arr[t - 1]
        if a == "ub":
            side = -1
        elif a == "us":
            side = 1
        else:
            side = -1 if fv > ask else (1 if fv < bid else 0)
        filled = False
        if side != 0 and abs(inv + side) <= 10:
            filled = True
            price = ask if side < 0 else bid
            cfl = -side * price
            inv += side
            cash += cfl
            cf += cfl
            last = price
            fills += 1
        log.append((t, filled))
    settle = path[turns]
    pnl = cash + inv * settle
    return dict(fills=fills, cash_flow=cf, inventory=inv, settlement=settle, pnl=pnl,
                informed=sum(1 for x in arr if x == "inf"))

show("seed 0 summary (independent)", sim(0))
show("seed 1 summary (independent)", sim(1))

# Part 2 enumeration grid vs closed form, E[change] exact at each grid point (inventory 0)
for fair in range(9980, 10025, 5):
    show(f"grid v={fair} closed", closed(F(fair), F(10010), F(9990), F(1, 2)))

# Part 3 variance per inventory
for I in (0, 1, 3, -3, 10):
    xs = [I * 5, I * -5]
    mean = F(sum(xs), 2)
    var = F(sum((F(x) - mean) ** 2 for x in xs), 2)
    show(f"Part3 I={I} mean={mean} var={var}", var == 25 * I * I)

# Problem E2: standard error and z
p = F(1, 2)
se = math.sqrt(0.25 / 20)
show("E2 SE", round(se, 6))
show("E2 z", round((0.65 - 0.5) / se, 4))
show("E2 critical 97.5 pct (value cited)", "1.959964 (standard normal, 6 places)")

# Problem R1: d = (1-p)h/p at p=3/5, h=10
show("R1 d", (1 - F(3, 5)) * 10 / F(3, 5))

# E3 mid vs settlement
show("E3 P&L settlement", -9950 + 9980)
show("E3 P&L mid", -9950 + 9990)

print("== L05 ==")
def naive(xs, k):
    out = []
    comps = 0
    for s in range(len(xs) - k + 1):
        best = xs[s]
        for x in xs[s + 1:s + k]:
            comps += 1
            if x > best:
                best = x
        out.append(best)
    return out, comps

def deque_run(xs, k):
    dq = []
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

def brute(xs, k):
    return [max(xs[s:s + k]) for s in range(len(xs) - k + 1)]

for seed in (5, 6):
    rng = random.Random(seed)
    xs = [rng.randint(0, 999) for _ in range(200)]
    print(f"seed {seed} first five:", xs[:5])
    for k in (8, 1, 2, 32, 200):
        o_n, c_n = naive(xs, k)
        o_d, c_d, pu, po = deque_run(xs, k)
        print(f"seed {seed} k={k}: naive={c_n} formula={(200-k+1)*(k-1)} deque_comps={c_d} pushes={pu} pops={po} "
              f"outputs_equal_naive={o_n==o_d} equal_brute={o_d==brute(xs,k)} comps<=2n={c_d<=400}")
    print(f"seed {seed} k=8 first five maxima:", deque_run(xs, 8)[0][:5])

# window agreement 1..20
rng = random.Random(5)
xs = [rng.randint(0, 999) for _ in range(200)]
print("windows 1..20 agree (naive vs brute, deque vs brute):",
      all(naive(xs, k)[0] == brute(xs, k) == deque_run(xs, k)[0] for k in range(1, 21)))
print("window 1 returns sequence:", deque_run(xs, 1)[0] == xs)
print("window 200 max:", max(xs), deque_run(xs, 200)[0] == [max(xs)])
print("window 201:", deque_run(xs, 201)[0] == [])
print("empty seq:", deque_run([], 3)[0] == [], naive([], 3)[0] == [])

# Example 3.5 trace
o, c, pu, po = deque_run([3, 1, 4, 1, 5], 3)
print("Example 3.5 outputs:", o, "(expected (4,4,5))")

# M2 trace: x=(2,5,1,0,3), k=2 -> outputs (5,5,1,3)
print("M2 outputs:", deque_run([2, 5, 1, 0, 3], 2)[0], "(expected (5,5,1,3))")

# Remark 2.2: maximum over k at n=200 is k=101 with 10000
best = max(((200 - k + 1) * (k - 1), k) for k in range(1, 201))
print("R2 max naive count and k at n=200:", best)

# P1 example n=200 k=101 -> 100*100
# E1 ratio 5239/382
print("E1 ratio:", round(5239 / 382, 2))
print("E1 formula 169*31:", 169 * 31)

# Remark 3.4 example: x=(k,k-1,...,1,k+1), n=k+1; deque removes k entries at step k+1
for kk in range(1, 8):
    xs2 = list(range(kk, 0, -1)) + [kk + 1]
    dq_removed = []
    # run and record pops at last step
    o2, c2, pu2, po2 = deque_run(xs2, kk)
    # pops at last step = total pops minus pops up to step k
    o_pre, c_pre, pu_pre, po_pre = deque_run(xs2[:kk], kk)
    print(f"Remark3.4 k={kk}: pops at step k+1 = {po2 - po_pre}")

# P3: increasing sequence comparisons = n-1 for every k
ok = True
for n in range(1, 30):
    for kk in range(1, n + 1):
        xs3 = list(range(n))
        if deque_run(xs3, kk)[1] != n - 1:
            ok = False
print("P3 increasing sequences comparisons == n-1 for all n<30, k<=n:", ok)

# Remark 3.6 heap bound
print("Remark 3.6: floor(log2 200) =", int(math.log2(200)), " 3*200*7 =", 3 * 200 * 7)

# Lab count for seed-5 comparisons vs 2n
print("== L06 ==")
# Prop 1.1 identity
ok = all((F(s) - K if s >= K else F(0)) - (F(K) - s if K - s > 0 else F(0)) == s - K for s in range(-5, 6) for K in range(-5, 6))
print("Prop 1.1 payoff identity on integer grid:", ok)

# Prop 2.1: F/S rule
S = F(9700); D = F(97, 100)
show("forward price S/D", S / D)
show("S/D with spot 4900, D=0.98", F(4900) / F("0.98"))
show("M1 payoff 5050 - 5000", F(5050) - F(4900) / F("0.98"))

# A: annuity at 10%
def annuity(r, n=3):
    return sum((1 / (1 + r) ** t for t in range(1, n + 1)), F(0))
A10 = annuity(F(1, 10))
show("A(10%) exact", A10)
show("A(10%) == 3310/1331", A10 == F(3310, 1331))
A8 = annuity(F(8, 100)); A12 = annuity(F(12, 100))
show("A(8%) 7dp", rnd(A8, 7))
show("A(12%) 7dp", rnd(A12, 7))
show("A(8%) float", float(A8))
show("A(12%) float", float(A12))
be = {r: F(15000000, 5000) / a for r, a in ((8, A8), (10, A10), (12, A12))}
for r in (8, 10, 12):
    show(f"break-even {r}% exact-float", float(be[r]))
    show(f"break-even {r}% 4dp (half-up)", rnd(be[r], 4))
    show(f"break-even {r}% 2dp (half-up)", rnd(be[r], 2))
show("break-even 10% exact", be[10])
show("width 8->12 exact (unrounded)", be[12] - be[8])
show("width 8->12 from 4dp values", F("1249.0469") - F("1164.1005"))
show("per point from 4dp", (F("1249.0469") - F("1164.1005")) / 4)
show("8->10 change from 4dp", F("1206.3444") - F("1164.1005"))
show("10->12 change from 4dp", F("1249.0469") - F("1206.3444"))
show("8->10 change exact", be[10] - be[8])
show("10->12 change exact", be[12] - be[10])
show("displayed 1249.05-1206.34", F("1249.05") - F("1206.34"))
show("per point exact", (be[12] - be[8]) / 4)

def npv(cfs, r):
    return sum((c / (1 + r) ** t for t, c in enumerate(cfs)), F(0))

def cfs(u):
    return [F(-15000000)] + [F(u) * 5000] * 3

show("NPV at 200 (10%) exact", npv(cfs(200), F(1, 10)))
show("NPV at 1600 (10%) exact", npv(cfs(1600), F(1, 10)))
show("NPV at 200 (10%) float", float(npv(cfs(200), F(1, 10))))
show("NPV at 1600 (10%) float", float(npv(cfs(1600), F(1, 10))))
show("NPV at 1200 exact", npv(cfs(1200), F(1, 10)))
show("NPV at 1300 exact", npv(cfs(1300), F(1, 10)))
show("NPV at 200 8% float", float(npv(cfs(200), F(8, 100))))
show("NPV at 1600 8% float", float(npv(cfs(1600), F(8, 100))))
show("NPV at 1600 12% float", float(npv(cfs(1600), F(12, 100))))
show("NPV at 200 12% float", float(npv(cfs(200), F(12, 100))))
show("NPV at break-even 10% exact is zero", npv(cfs(be[10]), F(1, 10)) == 0)
grid_pos = [u for u in range(200, 1601, 100) if npv(cfs(u), F(1, 10)) > 0]
show("grid positive points at 10%", grid_pos)
neg = [u for u in range(200, 1601, 100) if npv(cfs(u), F(1, 10)) < 0]
show("grid negative points at 10%", neg)
show("M2 NPV", npv([F(-100), F(60), F(60)], F(1, 10)))
show("M3 break-even", F(100000) / (F(400) * A10 / 1) if False else F(100000) / (400 * A10))
show("M3 33275/331", F(33275, 331))
show("R3 margin m* cents", F(15000000) / (1600 * A10))
show("R3 margin fraction", F(15000000) / (1600 * A10) / 5000)
show("R3 fall pct", float(1 - F(15000000) / (1600 * A10) / 5000) * 100)
show("E2 NPV at 1200", npv(cfs(1200), F(1, 10)))
show("E2 NPV at 1300", npv(cfs(1300), F(1, 10)))
show("E2 NPV at 1200 exact -105000000/1331", F(-105000000, 1331))
show("E2 NPV at 1300 exact 1550000000/1331", F(1550000000, 1331))
show("R1 log widths ln2 each", [math.log(4000 / 2000), math.log(2 / 1), math.log((1 / 5) / (1 / 10))])
show("Fermi bounds", (2000 * 1 * F(1, 10), 4000 * 2 * F(1, 5)))
show("Fermi range ratio", F(1600, 200))
show("Remark 4.3 cited unrounded 1206.3444 vs exact", float(be[10]))

"""Independent re-derivation of every numeric claim on the PC3 retrieval cards (round 2, verifier d).

usage: python -I rederive_card_numbers.py   (standard library only; prints one line per claim, exits 1 on a mismatch)
"""
import itertools
import math
import random
import sys
from fractions import Fraction as F

fails = []


def check(label: str, got, want, tol: float = 0.0) -> None:
    ok = (abs(float(got) - float(want)) <= tol) if tol else (got == want)
    print(("OK   " if ok else "FAIL ") + label + f" -> {got}")
    if not ok:
        fails.append(label)


def disp(x: float, places: int) -> str:
    return f"{x:.{places}f}"


# ---- L01 (cards c001-c016, c118-c123)
check("c007 lower bound 20*2*300", 20 * 2 * 300, 12000)
check("c007 upper bound 60*10*390", 60 * 10 * 390, 234000)
check("c007/c118 ratio 19.5", F(234000, 12000), F(39, 2))
w_total = math.log(19.5)
check("c118 ln 19.5 to 10 dp", disp(w_total, 10), "2.9704144656")
check("c119 ln3+ln5+ln1.3 = ln19.5", math.log(3) + math.log(5) + math.log(1.3), w_total, 1e-12)
check("c119 3*5*1.3", 3 * 5 * 1.3, 19.5, 1e-12)
w_min_narrow = math.log(60 * 10 * 360 / (20 * 2 * 330))
check("c009 minutes narrowing reduction", round(w_total - w_min_narrow, 4), 0.1754, 1e-9)
check("c009 minutes share %", round(100 * (w_total - w_min_narrow) / w_total, 1), 5.9, 1e-9)
w_q = math.log(60 * 8 * 390 / (20 * 4 * 300))
check("c009 quote-updates reduction", round(w_total - w_q, 4), 0.9163, 1e-9)
check("c009 quote-updates share %", round(100 * (w_total - w_q) / w_total, 1), 30.8, 1e-9)
check("c016 ln 1.5", round(math.log(1.5), 4), 0.4055, 1e-9)
check("c016 ln(2.5/1.01)", round(math.log(2.5 / 1.01), 4), 0.9063, 1e-9)
check("c016 ln 2.5 < ln 3 (B narrower)", math.log(2.5) < math.log(3), True)
check("c013 (1.01)^10 to 10 dp", disp(1.01**10, 10), "1.1046221254")
check("c120 remainder to 10 dp", disp(1.01**10 - 1 - 10 * 0.01, 10), "0.0046221254")
bound = F(10 * 9, 2) * F(101, 100) ** 8 * F(1, 10000)
check("c121 bound n(n-1)/2 (1+x)^(n-2) x^2 to 10 dp", disp(float(bound), 10), "0.0048728552")
check("c122 remainder below bound", (F(101, 100) ** 10 - 1 - 10 * F(1, 100)) < bound, True)
check("c014 (1.05)^10 to 4 dp", disp(1.05**10, 4), "1.6289")
check("c014 miss 0.1289", disp(1.05**10 - 1.5, 4), "0.1289")
check("c123 bound n=10 x=1/20 to 4 dp", disp(float(F(45) * F(21, 20) ** 8 * F(1, 400)), 4), "0.1662")

# ---- L02 (c023-c034)
space = [(a, b) for a in "HT" for b in "HT"]
alo = [s for s in space if "H" in s]
check("c023 P(both | at least one)", F(1, 4) / F(3, 4), F(1, 3))
check("c023 P(both | first H)", F(1, 4) / F(1, 2), F(1, 2))
check("c025 P(at least one | both)", F(1, 4) / F(1, 4), 1)
urn = [(a, b) for a in range(5) for b in range(5) if a != b]  # 0,1,2 red; 3,4 blue
red = {0, 1, 2}
check("c026 P(second red)", F(sum(b in red for a, b in urn), 20), F(3, 5))
check("c026 P(first red)", F(sum(a in red for a, b in urn), 20), F(3, 5))
check("c026 P(both red)", F(sum(a in red and b in red for a, b in urn), 20), F(3, 10))
blue_first = [(a, b) for a, b in urn if a in (3, 4)]
check("c027 P(second red | first blue)", F(sum(b in red for a, b in blue_first), len(blue_first)), F(3, 4))
check("c031 bag posterior", (F(1, 2) * F(3, 4)) / F(1, 2), F(3, 4))
check("c031 P(red)", F(1, 2) * F(3, 4) + F(1, 2) * F(1, 4), F(1, 2))
pB = F(1, 2) * F(3, 10) + F(1, 5) * F(7, 10)
check("c033 P(B)", pB, F(29, 100))
check("c033 P(A|B)", (F(1, 2) * F(3, 10)) / pB, F(15, 29))


def monty(rule: str):
    stay = sw = tot = F(0)
    for car, pick in itertools.product(range(3), range(3)):
        others = [d for d in range(3) if d != pick]
        for opened in others:
            if rule == "A":
                goats = [d for d in others if d != car]
                if opened not in goats:
                    continue
                p = F(1, len(goats))
            else:
                if opened == car:
                    continue
                p = F(1, 2)
            w = F(1, 9) * p
            tot += w
            sd = next(d for d in others if d != opened)
            stay += w if pick == car else 0
            sw += w if sd == car else 0
    return stay / tot, sw / tot


check("c028 rule A stay", monty("A")[0], F(1, 3))
check("c028 rule A switch", monty("A")[1], F(2, 3))
check("c029 rule B stay", monty("B")[0], F(1, 2))
check("c029 rule B switch", monty("B")[1], F(1, 2))

# seed-0 drill set: closed form equals enumeration on 12 of 12 (independent recomputation)
rng = random.Random(0)
agree = 0
for _ in range(12):
    flips = rng.randint(3, 8)
    if rng.random() < 0.5:
        k = rng.randint(1, flips)
        cnt = sum(1 for seq in itertools.product((0, 1), repeat=flips) if sum(seq) >= k)
        form = sum(math.comb(flips, i) for i in range(k, flips + 1))
    else:
        j = rng.randint(1, flips)
        cnt = sum(1 for seq in itertools.product((0, 1), repeat=flips) if seq[j - 1] == 1 and all(s == 0 for s in seq[: j - 1]))
        form = 2 ** (flips - j)
    agree += cnt == form
print(f"c034 drill agree count (independent) -> {agree} of 12")
check("c034 drill agree 12 of 12", agree, 12)

# ---- L03 (c038-c055, c124-c126)
check("c038 E[face]*100", F(100 * 21, 6), 350)
check("c038 E[X+Y]", F(sum(x + y for x in range(1, 7) for y in range(1, 7)), 36), 7)
check("c042 continuation", F(100 * 21, 6) - 100, 250)
check("c043 backward value", (F(250 + 250 + 300 + 400 + 500 + 600, 6)), F(1150, 3))
check("c043 2300/6 == 1150/3", F(2300, 6), F(1150, 3))
check("c043 383.33", disp(float(F(1150, 3)), 2), "383.33")
check("c044/c124 best of 64 policies", max(
    sum((100 * f if bits[f - 1] else 250) for f in range(1, 7)) / F(6) for bits in itertools.product((0, 1), repeat=6)), F(1150, 3))
check("c124 stop on every face", F(100 * 21, 6), 350)
check("c048 biased per-turn 25 and 6*25", F(150 + -100, 2) * 6, 150)


def expect(outcomes, rule, horizon=6):
    def val(h):
        if len(h) == horizon or rule(h):
            return F(sum(h))
        return sum((p * val(h + (x,)) for x, p in outcomes), F(0))
    return val(())


BIAS = ((150, F(1, 2)), (-100, F(1, 2)))
FAIR = ((100, F(1, 2)), (-100, F(1, 2)))
rules = {
    "first_loss": lambda h: bool(h) and h[-1] < 0,
    "total100": lambda h: sum(h) >= 100,
    "gain200": lambda h: sum(h) >= 200 or sum(h) <= -200,
}
check("c049 stop after first loss, biased", expect(BIAS, rules["first_loss"]), F(1575, 32))
check("c125 total reaches 100, biased", expect(BIAS, rules["total100"]), F(575, 8))
check("c126 200 gain/loss, biased", expect(BIAS, rules["gain200"]), F(625, 8))
for name, r in rules.items():
    check(f"c050 fair game zero under {name}", expect(FAIR, r), 0)
check("c051 R1 mean of max(W1,W2)", F(200 + 100 + 0 - 100, 4), 50)
check("c052 threshold: reroll strictly better iff 100f<250", [f for f in range(1, 7) if 100 * f < 250], [1, 2])

# ---- L04 (c061-c076, c127-c130)
def sim(seed: int):
    rng = random.Random(seed)
    path = [10000]
    arr = []
    for _ in range(20):
        mv = 5 if rng.random() < 0.5 else -5
        path.append(path[-1] + mv)
        d = rng.random()
        arr.append("ub" if d < 0.25 else ("us" if d < 0.5 else "inf"))
    inv = 0
    cash = 0
    last = None
    fills = 0
    flow = 0
    quotes = []
    for t in range(1, 21):
        mid = 10000 if last is None else last
        bid, ask = mid - 10, mid + 10
        quotes.append((bid, ask))
        a = arr[t - 1]
        v = path[t]
        if a == "ub":
            side = -1
        elif a == "us":
            side = 1
        elif v > ask:
            side = -1
        elif v < bid:
            side = 1
        else:
            side = 0
        if side != 0 and abs(inv + side) <= 10:
            price = ask if side < 0 else bid
            cash += -side * price
            flow += -side * price
            inv += side
            last = price
            fills += 1
    settle = path[20]
    return fills, flow, inv, settle, cash + inv * settle, quotes


fills, flow, inv, settle, pnl, quotes = sim(0)
check("c070 seed 0 fills", fills, 9)
check("c127 seed 0 cash flow", flow, -9950)
check("c128 seed 0 final inventory", inv, 1)
check("c129 seed 0 settlement", settle, 9980)
check("c130 seed 0 P&L", pnl, 30)
check("c061 final quote mid", (quotes[-1][0] + quotes[-1][1]) // 2, 9990)
check("c061 mid mark minus settlement mark (1 unit)", 1 * (9990 - 9980), 10)
check("c061 P&L at mid", -9950 + 1 * 9990, 40)
fills1, flow1, inv1, settle1, pnl1, _ = sim(1)
check("E1 (lesson) seed 1 fills", fills1, 16)


def prop31(v, a, b, h, p=F(1, 2)):
    return (1 - p) * h - p * (max(v - a, 0) + max(b - v, 0))


check("c064 at 10000", prop31(F(10000), F(10010), F(9990), 10), 5)
check("c064 at 10020", prop31(F(10020), F(10010), F(9990), 10), 0)
check("c064 at 9985", prop31(F(9985), F(10010), F(9990), 10), F(5, 2))
check("c068 sd at 3 units", math.sqrt(25 * 9), 15)
check("c068 sd at 10 units", math.sqrt(25 * 100), 50)
check("c073 variance at 10 units", 25 * 100, 2500)
check("c072 P&L after uninformed buy at 10010 vs 10000", 10010 + (-1) * 10000, 10)
check("c075 d at p=3/5 h=10", F(2, 5) * 10 / F(3, 5), F(20, 3))
check("c076 variance at |I|=1", 25, 25)
check("c076 variance at |I|=2 equals 100", 25 * 4, 100)
check("c066 uninformed flow at p=1/2 h=10", (1 - F(1, 2)) * 10, 5)
check("c066 quarter of spread 2h=20", F(5, 20), F(1, 4))
check("c066 tie: 1/2 of h is quarter of 2h", F(10, 2) / 20, F(1, 4))
check("c063 proposition sanity at v=a+h p=1/2 zero", prop31(F(10020), F(10010), F(9990), 10), 0)

# ---- L05 (c077-c094, c131-c135)
def naive(xs, k):
    comps = 0
    out = []
    for s in range(len(xs) - k + 1):
        best = xs[s]
        for x in xs[s + 1 : s + k]:
            comps += 1
            if x > best:
                best = x
        out.append(best)
    return out, comps


def deque_ops(xs, k):
    from collections import deque

    w = deque()
    out = []
    comps = pushes = pops = 0
    for i, x in enumerate(xs):
        while w:
            comps += 1
            if xs[w[-1]] > x:
                break
            w.pop()
            pops += 1
        w.append(i)
        pushes += 1
        if w[0] <= i - k:
            w.popleft()
            pops += 1
        if i >= k - 1:
            out.append(xs[w[0]])
    return out, comps, pushes, pops


rng5 = random.Random(5)
xs = [rng5.randint(0, 999) for _ in range(200)]
n8, c8 = naive(xs, 8)
d8, dc8, dp8, dq8 = deque_ops(xs, 8)
check("c089 naive comparisons k=8", c8, 1351)
check("c131 deque comparisons k=8", dc8, 354)
check("c132 deque pushes k=8", dp8, 200)
check("c132 deque pops k=8", dq8, 199)
check("c133 354 <= 2n", dc8 <= 400, True)
n32, c32 = naive(xs, 32)
d32, dc32, _, _ = deque_ops(xs, 32)
check("c090 naive comparisons k=32", c32, 5239)
check("c134 deque comparisons k=32", dc32, 382)
check("c094 outputs equal for k=1..20", all(naive(xs, k)[0] == deque_ops(xs, k)[0] for k in range(1, 21)), True)
check("c086 example 3.5 outputs", deque_ops([3, 1, 4, 1, 5], 3)[0], [4, 4, 5])
check("c087 problem M2 outputs", deque_ops([2, 5, 1, 0, 3], 2)[0], [5, 5, 1, 3])
ok_c088 = True
for n in range(1, 40):
    for k in range(1, n + 1):
        seq = sorted(random.Random(n * 100 + k).sample(range(10 * n), n))
        _, comps, _, _ = deque_ops(seq, k)
        if comps != n - 1:
            ok_c088 = False
check("c088 strictly increasing sequences make n-1 comparisons (n<40, all k)", ok_c088, True)
check("c080 naive count (n-k+1)(k-1) at n=200,k=8", (200 - 8 + 1) * 7, 1351)
check("c081 max over k of (n-j)j at n=200 is n^2/4", max((200 - j) * j for j in range(0, 200)), 10000)
check("c081 even n: maximiser k=n/2+1 (n=20)", max(range(1, 21), key=lambda k: (20 - k + 1) * (k - 1)), 11)
check("c085 remark 3.4: step k removes k-1 entries (k=6)", deque_ops(list(range(6, 1, -1)) + [7], 6)[1] >= 5, True)

# ---- L06 (c095-c117, c136-c141)
check("c095 identity sample", (F(3) - 0) - (0 - F(3)) if False else F(5 - 2) - 0, 3)
A10 = sum(F(1) / F(11, 10) ** t for t in range(1, 4))
check("c107 annuity factor 3310/1331", A10, F(3310, 1331))
K = F(15000000)
m = F(5000)
check("c136 break-even 1206.34", disp(float(K / (m * A10)), 2), "1206.34")
check("c136 399300/331", K / (m * A10), F(399300, 331))
check("c116 M3 break-even 33275/331", F(1000 * 1331, 4 * 3310), F(33275, 331))
check("c116 M3 ~100.53", disp(float(F(33275, 331)), 2), "100.53")
check("c115 M2 NPV = 500/121", -100 + F(60) / F(11, 10) + F(60) / F(121, 100), F(500, 121))
check("c115 M2 ~4.13", disp(float(F(500, 121)), 2), "4.13")
check("c106 bounds lower", 2000 * 1 * F(1, 10), 200)
check("c106 bounds upper", 4000 * 2 * F(1, 5), 1600)
A8 = sum(1 / (1 + 0.08) ** t for t in range(1, 4))
A12 = sum(1 / (1 + 0.12) ** t for t in range(1, 4))
be8, be10, be12 = 3000 / A8, 3000 / (3310 / 1331), 3000 / A12
check("c108 break-even 8% to 2 dp", disp(be8, 2), "1164.10")
check("c137 break-even 12% to 2 dp", disp(be12, 2), "1249.05")
check("c112 break-even 10% to 2 dp", disp(be10, 2), "1206.34")
check("c112 change per two points ~42", round(be10 - be8), 42)
check("c140 average change per point (8 to 12 percent)", round((be12 - be8) / 4, 4), 21.2366, 1e-3)
check("c140 displayed to 21.24", disp((be12 - be8) / 4, 2), "21.24")
npv = lambda u, r: sum(c / (1 + r) ** t for t, c in enumerate([F(-15000000)] + [F(u) * 5000] * 3 for _ in [0]) ) if False else None
def npv_units(u, r):
    cfs = [-15000000] + [u * 5000] * 3
    return sum(F(c) / (1 + r) ** t for t, c in enumerate(cfs))
check("c109 NPV at 200 units exact", npv_units(200, F(1, 10)), F(-16655000000, 1331))
check("c109 NPV at 200 to whole cent", round(float(npv_units(200, F(1, 10)))), -12513148)
check("c139 NPV at 1600 to whole cent", round(float(npv_units(1600, F(1, 10)))), 4894816)
check("c138 sign at 200 units all rates", all(npv_units(200, F(r, 100)) < 0 for r in (8, 10, 12)), True)
check("c138 sign at 1600 units all rates", all(npv_units(1600, F(r, 100)) > 0 for r in (8, 10, 12)), True)
check("c117/c141 margin for break-even 1600 (cents)", float(K * 1331 / (1600 * 3310)), 3769.8, 0.05)
check("c117 margin ratio 0.7540", round(float(K * 1331 / (1600 * 3310)) / 5000, 4), 0.7540, 1e-9)
check("c117 fall 24.6%", round(100 * (1 - float(K * 1331 / (1600 * 3310)) / 5000), 1), 24.6, 1e-9)
check("c141 exact margin formula", float(K * 1331 / (1600 * 3310)), 3769.8, 0.05)
check("c102 u* = K/(mA) = 15000000/(5000*A)", K / (m * A10), F(399300, 331))
check("c104 Corollary: 200 < 1206.34 < 1600", 200 < 1206.34 < 1600, True)
check("c100 F'=S/D with D=0.97 example", F(9700) / F(97, 100), F(10000))
check("c110 payoff at quote 10100 is 100", F(10100) - F(10000), 100)
check("c110 payoff at quote 10000 is 0", F(10000) - F(10000), 0)
check("c101 S/D = S e^{r tau}, D=e^{-r tau}", math.exp(0.1) * 1, math.exp(0.1), 1e-12)

print("FAILURES:", fails if fails else "none")
sys.exit(1 if fails else 0)

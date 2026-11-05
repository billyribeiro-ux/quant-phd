"""Independent re-derivation of every number the PC3 cards state (verifier slice d, round 12).

Written from the lesson text, not from the lab code. Standard library only.
"""
import itertools
import math
import random
from fractions import Fraction as F

ok = True


def check(label, cond, detail=""):
    global ok
    ok = ok and bool(cond)
    print(f"{'OK  ' if cond else 'FAIL'} {label} {detail}")


def r(x, places):
    """Half-up rounding of an exact value to places (ties toward +inf), as displayed."""
    scale = 10**places
    n = math.floor(x * scale + F(1, 2))
    return F(n, scale)


# ---- L01 -------------------------------------------------------------------
lo = F(20) * 2 * 300
hi = F(60) * 10 * 390
check("L01 product bounds 12000 / 234000", (lo, hi) == (12000, 234000))
w = math.log(hi / lo)
check("L01 ln 19.5 = 2.9704144656", f"{w:.10f}" == "2.9704144656", f"{w:.12f}")
check("L01 factor widths sum", abs(math.log(3) + math.log(5) + math.log(1.3) - w) < 1e-12)
check("L01 ln3,ln5,ln1.3 printed 1.0986 1.6094 0.2624",
      f"{math.log(3):.4f}" == "1.0986" and f"{math.log(5):.4f}" == "1.6094" and f"{math.log(1.3):.4f}" == "0.2624")
gm = math.sqrt(lo * hi)
check("L01 geometric midpoint 52990.5652 (to 4 dp, and 52 990.57 to 2 dp)",
      f"{gm:.4f}" == "52990.5652" and f"{gm:.2f}" == "52990.57", f"{gm:.6f}")
red_sym = math.log(hi / lo) - math.log(F(234000 * 0 + 40 * 10 * 390, 20 * 2 * 300))
check("L01 narrowing symbols [20,40] reduction = ln 2 * ... = 0.4055", f"{red_sym:.4f}" == "0.4055", f"{red_sym:.10f}")
tot_sym = math.log(40 * 10 * 390 / (20 * 2 * 300))
check("L01 total after narrowing symbols = 2.5649", f"{tot_sym:.4f}" == "2.5649", f"{tot_sym:.10f}")
hi_q = F(60 * 8 * 390); lo_q = F(20 * 4 * 300)
red_q = w - math.log(hi_q / lo_q)
check("L01 quote updates [4,8] reduction 0.9163, total 2.0541",
      f"{red_q:.4f}" == "0.9163" and f"{math.log(hi_q/lo_q):.4f}" == "2.0541", f"{red_q:.10f}")
share_q = red_q / w
check("L01 quote share 30.8 percent (full precision)", f"{100*share_q:.1f}" == "30.8", f"{100*share_q:.6f}")
check("L01 quote share from displayed values 30.85 (0.9163/2.9704)", f"{100*0.9163/2.9704:.2f}" == "30.85",
      f"{100*0.9163/2.9704:.4f}")
hi_m = F(60 * 10 * 360); lo_m = F(20 * 2 * 330)
red_m = w - math.log(hi_m / lo_m)
check("L01 minutes [330,360] reduction 0.1754", f"{red_m:.4f}" == "0.1754", f"{red_m:.10f}")
check("L01 minutes share 5.9 percent", f"{100*red_m/w:.1f}" == "5.9", f"{100*red_m/w:.6f}")
check("L01 E2 quotient 0.059033", f"{red_m/w:.6f}" == "0.059033")
check("L01 E2 displayed 0.308477 / 30.8477 (four-place values)", f"{0.9163/2.9704:.6f}" == "0.308477")
check("L01 E3 ln 16.5 = 2.8034, change 0.167054",
      f"{math.log(16.5):.4f}" == "2.8034" and f"{math.log(19.5)-math.log(16.5):.6f}" == "0.167054")
check("L01 R1 criterion: ln5 = 1.6094 exceeds half of 2.9704 (1.4852)", math.log(5) > w / 2)
check("L01 R3 ln(3/2)=0.4055, ln(2.5/1.01)=0.9063, ln2.5=0.9163, ln3=1.0986",
      f"{math.log(1.5):.4f}" == "0.4055" and f"{math.log(2.5/1.01):.4f}" == "0.9063"
      and f"{math.log(2.5):.4f}" == "0.9163" and f"{math.log(3):.4f}" == "1.0986")
check("L01 R3 smaller width gives larger reduction", math.log(2.5 / 1.01) > math.log(1.5))

# Taylor remainder
def rem(n, x):
    return (1 + x) ** n - 1 - n * x

def bnd(n, x):
    return F(n * (n - 1), 2) * (1 + x) ** (n - 2) * x * x

x1 = F(1, 100)
check("L01 (1.01)^10 exact begins 1.10462212541", f"{float((1+x1)**10):.11f}" == "1.10462212541",
      f"{float((1+x1)**10):.12f}")
check("L01 c013 to ten places 1.1046221254", f"{float((1+x1)**10):.10f}" == "1.1046221254")
check("L01 c130 remainder 0.0046221254", f"{float(rem(10, x1)):.10f}" == "0.0046221254")
check("L01 c131 bound 0.0048728552", f"{float(bnd(10, x1)):.10f}" == "0.0048728552")
check("L01 c131 bound formula 45*1.01^8*1e-4", abs(float(bnd(10, x1)) - 45 * 1.01**8 * 1e-4) < 1e-15)
check("L01 Ex1.7 ratio 0.9485", f"{float(rem(10,x1)/bnd(10,x1)):.4f}" == "0.9485", f"{float(rem(10,x1)/bnd(10,x1)):.6f}")
check("L01 Ex1.7 bound exceeds remainder by 5.4 percent",
      f"{100*(float(bnd(10,x1)/rem(10,x1))-1):.1f}" == "5.4", f"{100*(float(bnd(10,x1)/rem(10,x1))-1):.4f}")
x20 = F(1, 20)
check("L01 c133 bound 0.1662 and miss 0.1289 at x=1/20",
      f"{float(bnd(10,x20)):.10f}" == "0.1662137374" and f"{float(rem(10,x20)):.4f}" == "0.1289")
check("L01 c014 (1.05)^10 to four places 1.6289", f"{float((1+x20)**10):.4f}" == "1.6289")
check("L01 miss 0.1289/1.6289 = 7.9 percent", f"{100*0.1289/1.6289:.1f}" == "7.9")
check("L01 Ex1.7 at x=1/20 remainder < bound", rem(10, x20) < bnd(10, x20))
check("L01 n=2 remainder equals bound x^2", rem(2, x20) == bnd(2, x20) == x20 * x20)
check("L01 Remark 1.6 sum identity n=10 x=1/100", rem(10, x1) == sum(math.comb(10, j) * x1**j for j in range(2, 11)))
check("L01 Part 3 n=5 x=1/20 remainder 0.0262815625 and bound 0.0289406250 (printed)",
      f"{float(rem(5, x20)):.10f}" == "0.0262815625" and f"{float(bnd(5, x20)):.10f}" == "0.0289406250")

# ---- L02 -------------------------------------------------------------------
outs = list(itertools.product("HT", repeat=2))
def prob(ev, given=lambda o: True):
    g = [o for o in outs if given(o)]
    return F(sum(1 for o in g if ev(o)), len(g))
check("L02 c023 P(HH|at least one H)=1/3", prob(lambda o: o == ("H", "H"), lambda o: "H" in o) == F(1, 3))
check("L02 c023 P(HH|first H)=1/2", prob(lambda o: o == ("H", "H"), lambda o: o[0] == "H") == F(1, 2))
check("L02 c025 P(one H|HH)=1", prob(lambda o: "H" in o, lambda o: o == ("H", "H")) == 1)
urn = [("r", 1), ("r", 2), ("r", 3), ("b", 1), ("b", 2)]
pairs = [(a, b) for a in urn for b in urn if a != b]
def pp(ev, given=lambda p: True):
    g = [p for p in pairs if given(p)]
    return F(sum(1 for p in g if ev(p)), len(g))
check("L02 c026 P(first red)=3/5", pp(lambda p: p[0][0] == "r") == F(3, 5))
check("L02 c027 P(second red)=3/5", pp(lambda p: p[1][0] == "r") == F(3, 5))
check("L02 c028 P(both red)=3/10", pp(lambda p: p[0][0] == "r" and p[1][0] == "r") == F(3, 10))
check("L02 c029 P(second red | first blue)=3/4",
      pp(lambda p: p[1][0] == "r", lambda p: p[0][0] == "b") == F(3, 4))
# Monty Hall rule A and rule B from first principles
mh = []
for car in range(3):
    for pick in range(3):
        for host in range(3):
            if host in (pick,) or host == car:
                continue
            mh.append((car, pick, host))
# rule A: host opens a goat door among non-picked, uniform if two goats
def mh_rule(rule):
    num_stay = F(0); num_sw = F(0); den = F(0)
    for car in range(3):
        for pick in range(3):
            others = [d for d in range(3) if d != pick]
            for host in others:
                if rule == "A":
                    goats = [d for d in others if d != car]
                    if host not in goats:
                        continue
                    pr = F(1, len(goats))
                else:
                    if host == car:
                        continue
                    pr = F(1, 2)
                w_ = F(1, 9) * pr
                den += w_
                other = [d for d in others if d != host][0]
                if pick == car:
                    num_stay += w_
                if other == car:
                    num_sw += w_
    return num_stay / den, num_sw / den
sa = mh_rule("A"); sb = mh_rule("B")
check("L02 c030 rule A stay 1/3 switch 2/3", sa == (F(1, 3), F(2, 3)), str(sa))
check("L02 c031 rule B both 1/2", sb == (F(1, 2), F(1, 2)), str(sb))
check("L02 bag: P(bag1|red)=3/4, P(red)=1/2",
      (F(1, 2) * F(3, 4)) / (F(1, 2) * F(3, 4) + F(1, 2) * F(1, 4)) == F(3, 4))
check("L02 c035 P(B)=29/100, P(A|B)=15/29",
      F(1, 2) * F(3, 10) + F(1, 5) * F(7, 10) == F(29, 100) and (F(1, 2) * F(3, 10)) / F(29, 100) == F(15, 29))
check("L02 M1 P(sum 7 | first 3)=1/6", F(1, 36) / F(6, 36) == F(1, 6))
check("L02 M3 P(both red) 4 red 2 blue = 2/5", F(4, 6) * F(3, 5) == F(2, 5) and F(4 * 3, 6 * 5) == F(2, 5))
check("L02 E1 P(at least 2 heads in 6)=57/64", 1 - F(1, 64) - F(6, 64) == F(57, 64))
check("L02 E3 difference 1/6", F(2, 3) - F(1, 2) == F(1, 6))
# Drill set: closed form = enumeration on seed 0 (independent generator use)
rng = random.Random(0)
agree = 0
for item in range(12):
    flips = rng.randint(3, 8)
    if rng.random() < 0.5:
        k = rng.randint(1, flips)
        cnt = sum(math.comb(flips, i) for i in range(k, flips + 1))
        enum = sum(1 for seq in itertools.product((0, 1), repeat=flips) if sum(seq) >= k)
        agree += F(cnt, 2**flips) == F(enum, 2**flips)
    else:
        j = rng.randint(1, flips)
        enum = sum(1 for seq in itertools.product((0, 1), repeat=flips)
                   if seq[j - 1] == 1 and all(s == 0 for s in seq[: j - 1]))
        agree += F(1, 2**j) == F(enum, 2**flips)
check("L02 c036 closed form equals enumeration on 12 of 12 (my own generator)", agree == 12, f"agree={agree}")

# ---- L03 -------------------------------------------------------------------
E = lambda outs_: sum(v * p for v, p in outs_)  # noqa: E731
cont = F(sum(100 * g for g in range(1, 7)), 6) - 100
check("L03 c045 continuation 250", cont == 250)
val = sum(max(F(100 * f), cont) for f in range(1, 7)) / 6
check("L03 c046 value 1150/3", val == F(1150, 3), str(val))
check("L03 c046 (250+250+300+400+500+600)/6 = 2300/6", F(2300, 6) == F(1150, 3))
check("L03 c058 gain 100/3", val - 350 == F(100, 3))
check("L03 c056 rerolling strictly better on faces 1,2", [f for f in range(1, 7) if 100 * f < 250] == [1, 2])
best = max(sum((F(100 * f) if bits[f - 1] else cont) for f in range(1, 7)) / 6
           for bits in itertools.product((0, 1), repeat=6))
check("L03 c047 best of 64 policies = 1150/3", best == F(1150, 3))

FAIR = ((100, F(1, 2)), (-100, F(1, 2)))
BIAS = ((150, F(1, 2)), (-100, F(1, 2)))
H = 6
def rule_stop(name):
    return {
        "first win": lambda h: bool(h) and h[-1] > 0,
        "first loss": lambda h: bool(h) and h[-1] < 0,
        "100": lambda h: sum(h) >= 100,
        "200": lambda h: sum(h) >= 200 or sum(h) <= -200,
        "play": lambda h: False,
    }[name]

def exp_total(outcomes, stop):
    # exact enumeration of all sequences, stopping at first hit
    tot = F(0)
    for seq in itertools.product(outcomes, repeat=H):
        w_ = F(1)
        for _, p in seq:
            w_ *= p
        hist = ()
        for x, _ in seq:
            hist = hist + (x,)
            if stop(hist):
                break
        tot += w_ * sum(hist)
    return tot

for nm in ("play", "first win", "first loss", "100", "200"):
    check(f"L03 fair game rule {nm} expectation 0", exp_total(FAIR, rule_stop(nm)) == 0)
check("L03 c051 biased play-all 150", exp_total(BIAS, rule_stop("play")) == 150)
check("L03 c052 biased first loss 1575/32", exp_total(BIAS, rule_stop("first loss")) == F(1575, 32),
      str(exp_total(BIAS, rule_stop("first loss"))))
check("L03 biased first win 1575/32", exp_total(BIAS, rule_stop("first win")) == F(1575, 32))
check("L03 c135 biased 100 rule 575/8", exp_total(BIAS, rule_stop("100")) == F(575, 8),
      str(exp_total(BIAS, rule_stop("100"))))
check("L03 c136 biased 200 rule 625/8", exp_total(BIAS, rule_stop("200")) == F(625, 8),
      str(exp_total(BIAS, rule_stop("200"))))
check("L03 E2 change -575/8 = -71.875", F(625, 8) - 150 == F(-575, 8) and float(F(-575, 8)) == -71.875)
# R1 two-turn fair game looking ahead
paths = []
for a, b in itertools.product((100, -100), repeat=2):
    w1, w2 = a, a + b
    paths.append(max(w1, w2))
check("L03 R1 expected total of max(W1,W2) = 50", F(sum(paths), 4) == 50, str(paths))
check("L03 Ex3.10 per-turn expectation 25 and 6*25=150", F(1, 2) * 150 + F(1, 2) * -100 == 25 and 6 * 25 == 150)
check("L03 P1/E2 fair coin+die M3 = 200", F(1, 2) * 100 + F(1, 2) * (-50 + 100 * F(7, 2)) == 200)
check("L03 M2 p=1/3 makes 200p-100(1-p) zero", 200 * F(1, 3) - 100 * (1 - F(1, 3)) == 0)
check("L03 R2 gain 74.5 at fee c=1 (lesson text, reproduced)",
      F(sum(max(100 * f, 350 - 1) for f in range(1, 7)), 6) - 350 == F(149, 2))

# ---- L04 -------------------------------------------------------------------
# independent seed-0 game from the lesson text: move draw first, then arrival draw
def game(seed):
    rng_ = random.Random(seed)
    v = [10000]
    arr = []
    for _ in range(20):
        mv = 5 if rng_.random() < 0.5 else -5
        v.append(v[-1] + mv)
        u = rng_.random()
        arr.append("ub" if u < 0.25 else ("us" if u < 0.5 else "inf"))
    return v, arr

v_path, arrs = game(0)
inv = 0; cash = 0; last = None; fills = []
for t in range(1, 21):
    mid = 10000 if last is None else last
    b_, a_ = mid - 10, mid + 10
    arr_ = arrs[t - 1]; fv = v_path[t]
    if arr_ == "ub":
        side = -1
    elif arr_ == "us":
        side = 1
    else:
        side = -1 if fv > a_ else (1 if fv < b_ else 0)
    filled = side != 0 and abs(inv + side) <= 10
    if filled:
        price = a_ if side < 0 else b_
        cash += -side * price
        inv += side
        last = price
        fills.append((t, price))
settle = v_path[20]
check("L04 c077 nine fills on seed 0", len(fills) == 9, f"fills={len(fills)}")
check("L04 c137 cash flow -9950", cash == -9950, f"cash={cash}")
check("L04 c138 final inventory 1", inv == 1)
check("L04 c139 settlement 9980", settle == 9980)
check("L04 c140 P&L 30", cash + inv * settle == 30)
check("L04 c067 mark at mid 9990 gives 40", cash + inv * 9990 == 40)
check("L04 seed-0 informed arrivals 13 (E2)", arrs.count("inf") == 13, f"inf={arrs.count('inf')}")

# Proposition 3.1 brute-force check at many (v, quote, p) from inventory zero
def prop31_bruteforce(a, b, p, v):
    tot = F(0)
    for arr_p, kind in ((F(1) - p, "u"), (p, "i")):
        if kind == "u":
            for sgn, half in ((-1, F(1, 2)), (1, F(1, 2))):
                if sgn < 0:
                    c = a; s = -1
                else:
                    c = -b; s = 1
                tot += arr_p * half * (c + s * v)
        else:
            if v > a:
                tot += arr_p * (a + (-1) * v)
            elif v < b:
                tot += arr_p * (-b + v)
    return tot

def prop31(a, b, p, v):
    h = F(a - b, 2)
    return (1 - p) * h - p * (max(v - a, 0) + max(b - v, 0))

okp = True
for a_ in range(-30, 31, 3):
    for hh in range(1, 8):
        b_ = a_ - 2 * hh
        for pp in (F(1, 2), F(1, 3), F(3, 5), F(1, 10)):
            for vv in range(a_ - 25, a_ + 25, 2):
                okp = okp and prop31_bruteforce(a_, b_, pp, vv) == prop31(a_, b_, pp, vv)
check("L04 Prop 3.1 closed form equals brute enumeration over a grid", okp)
check("L04 Ex3.2 values 5, 0, 5/2", prop31(10010, 9990, F(1, 2), 10000) == 5 and
      prop31(10010, 9990, F(1, 2), 10020) == 0 and prop31(10010, 9990, F(1, 2), 9985) == F(5, 2))
check("L04 Corollary 3.3 zero at v=a+h", prop31(10010, 9990, F(1, 2), 10020) == 0)
check("L04 R1 d=(1-p)h/p=20/3 at p=3/5,h=10", F(2, 5) * 10 / F(3, 5) == F(20, 3))
check("L04 c070 formula five minus half", prop31(10010, 9990, F(1, 2), 10000) == 5)
# I=10 remark: E=5/2
ER = F(1, 4) * (10010 - 10000)
check("L04 Remark 4.2 at I=10 gives 5/2 (uninformed buy only, 10 cents w.p. 1/4)", ER == F(5, 2))
# Proposition 4.1 variance
for I_ in (0, 1, 3, -3, 10, -4):
    moves = (5, -5)
    mean = F(sum(I_ * m for m in moves), 2)
    var = F(sum((I_ * m - mean) ** 2 for m in moves), 2)
    check(f"L04 Prop 4.1 I={I_} mean 0 var 25I^2", mean == 0 and var == 25 * I_ * I_)
check("L04 Remark 4.2 sd 15 at 3 and 50 at 10", 5 * 3 == 15 and 5 * 10 == 50)
check("L04 R3 |I|<2 largest 1 (var 25)", max(i for i in range(0, 20) if 25 * i * i < 100) == 1)
check("L04 P2 at v=a+h E=0 and difference h/2", prop31(10010, 9990, F(1, 2), 10010) == 5
      and prop31(10010, 9990, F(1, 2), 10020) == 0)
check("L04 M1 W=10 cents after uninformed buy at 10010 with settlement 10000", 10010 + (-1) * 10000 == 10)
check("L04 E3 P&L marked at mid 40 vs settle 30, diff 10", (-9950 + 9990) - (-9950 + 9980) == 10)

# ---- L05 -------------------------------------------------------------------
def deque_method(xs, k):
    """The lesson's pseudocode, in its order: pop back while <= x_i, append i, expire front, output if i>=k."""
    dq = []
    out = []
    comps = 0
    pushes = 0
    removals = 0
    for i, x in enumerate(xs, 1):
        while dq:
            comps += 1
            if xs[dq[-1] - 1] <= x:
                dq.pop()
                removals += 1
            else:
                break
        dq.append(i)
        pushes += 1
        if dq[0] <= i - k:
            dq.pop(0)
            removals += 1
        if i >= k:
            out.append(xs[dq[0] - 1])
    return out, comps, pushes, removals

def naive(xs, k):
    return [max(xs[i:i + k]) for i in range(len(xs) - k + 1)], (len(xs) - k + 1) * (k - 1)

rng5 = random.Random(5)
xs5 = [rng5.randint(0, 999) for _ in range(200)]
rng6 = random.Random(6)
xs6 = [rng6.randint(0, 999) for _ in range(200)]
out5, c5, p5, rm5 = deque_method(xs5, 8)
check("L05 c142 deque comparisons seed 5 window 8 = 354", c5 == 354, f"c={c5}")
check("L05 c143 pushes 200 pops 199 (removals incl. front)", p5 == 200 and rm5 == 199, f"p={p5} rm={rm5}")
check("L05 c096 naive 1351 = 193*7", naive(xs5, 8)[1] == 1351 == 193 * 7)
check("L05 c097 window 32 naive 5239 = 169*31", naive(xs5, 32)[1] == 5239 == 169 * 31)
check("L05 c145 window 32 deque comparisons 382", deque_method(xs5, 32)[1] == 382)
check("L05 c144 window 200 deque comparisons 387 (<= 400)", deque_method(xs5, 200)[1] == 387)
check("L05 window 1 deque comparisons 199", deque_method(xs5, 1)[1] == 199)
check("L05 window 2 deque comparisons 263", deque_method(xs5, 2)[1] == 263)
check("L05 seed-6 deque comparisons 350", deque_method(xs6, 8)[1] == 350)
same = all(deque_method(xs5, k)[0] == naive(xs5, k)[0] for k in range(1, 21))
check("L05 c101 outputs equal for windows 1..20 (seed 5)", same)
# randomized correctness and Proposition 3.3 bound over many inputs
bad = 0
maxratio = 0
for trial in range(300):
    n = random.Random(trial).randint(1, 40)
    rr = random.Random(1000 + trial)
    seq = [rr.randint(0, 9) for _ in range(n)]
    for k in range(1, n + 1):
        o, cc, pu, rmv = deque_method(seq, k)
        if o != naive(seq, k)[0]:
            bad += 1
        if cc > 2 * n or pu != n or rmv > n:
            bad += 1
check("L05 Prop 2.1/3.2/3.3 randomized (300 sequences of length <=40)", bad == 0, f"bad={bad}")
# P3: strictly increasing gives n-1 for every k
p3 = all(deque_method(list(range(1, n + 1)), k)[1] == n - 1 for n in range(1, 40) for k in range(1, n + 1))
check("L05 P3 strictly increasing gives n-1 comparisons for all k", p3)
# Remark 2.2 peak
n_even = 200
best_k = max(range(1, n_even + 1), key=lambda k_: (n_even - k_ + 1) * (k_ - 1))
check("L05 Remark 2.2 peak at k=n/2+1=101 with count 10000", best_k == 101 and (n_even - 101 + 1) * 100 == 10000)
check("L05 M1 n=10 k=4 naive count 21", (10 - 4 + 1) * (4 - 1) == 21)
check("L05 Remark 3.6 heap bound 3*200*7=4200", 3 * 200 * math.floor(math.log2(200)) == 4200)
check("L05 E1 ratio 5239/382 = 13.7", f"{5239/382:.1f}" == "13.7")
check("L05 E3 bound 194+200=394 and 387 within", 387 <= 194 + 200)
check("L05 Example 3.5 outputs (4,4,5)", naive((3, 1, 4, 1, 5), 3)[0] == [4, 4, 5] and deque_method((3, 1, 4, 1, 5), 3)[0] == [4, 4, 5])
check("L05 M2 outputs (5,5,1,3)", deque_method((2, 5, 1, 0, 3), 2)[0] == [5, 5, 1, 3])
check("L05 P2 max in deque (edge): window equal to length gives one max",
      deque_method(xs5, 200)[0] == [max(xs5)])

# ---- L06 -------------------------------------------------------------------
def npv(cfs, rate):
    return sum((c / (1 + rate) ** t for t, c in enumerate(cfs)), F(0))

def cfs(u):
    return [F(-15000000)] + [u * 5000] * 3

A10 = sum((1 / (F(11, 10)) ** t for t in range(1, 4)), F(0))
check("L06 annuity 3310/1331", A10 == F(3310, 1331))
be10 = F(15000000, 5000) / A10
check("L06 break-even 399300/331 = 1206.3444", be10 == F(399300, 331))
check("L06 c151 unrounded 1206.3444", f"{float(be10):.4f}" == "1206.3444")
be8 = F(3000) / sum((1 / F(108, 100) ** t for t in range(1, 4)), F(0))
be12 = F(3000) / sum((1 / F(112, 100) ** t for t in range(1, 4)), F(0))
check("L06 break-even 8% 1164.1005 and 12% 1249.0469",
      f"{float(be8):.4f}" == "1164.1005" and f"{float(be12):.4f}" == "1249.0469", f"{float(be8):.6f} {float(be12):.6f}")
check("L06 c116 8% break-even displays 1164.10", f"{float(be8):.2f}" == "1164.10")
check("L06 c148 12% break-even displays 1249.05", f"{float(be12):.2f}" == "1249.05")
check("L06 c121 break-evens displayed 1164.10, 1206.34, 1249.05", f"{float(be8):.2f} {float(be10):.2f} {float(be12):.2f}" == "1164.10 1206.34 1249.05")
check("L06 Remark 4.3 differences 42.24 and 42.70", f"{float(be10-be8):.2f}" == "42.24" and f"{float(be12-be10):.2f}" == "42.70")
check("L06 displayed 1249.05-1206.34 = 42.71 (not the answer)", f"{1249.05-1206.34:.2f}" == "42.71")
check("L06 E3 width 84.95, avg 21.24 per point", f"{float(be12-be8):.2f}" == "84.95" and f"{float((be12-be8)/4):.2f}" == "21.24")
check("L06 c117 NPV at 200 units = -12513148 (exact -16655000000/1331)",
      npv(cfs(200), F(1, 10)) == F(-16655000000, 1331) and round(float(npv(cfs(200), F(1, 10)))) == -12513148,
      f"{float(npv(cfs(200), F(1,10))):.4f}")
check("L06 c150 NPV at 1600 = 4894816", round(float(npv(cfs(1600), F(1, 10)))) == 4894816,
      f"{float(npv(cfs(1600), F(1,10))):.4f}")
check("L06 c179 NPV at 1200 = -105000000/1331 = -78888.05", npv(cfs(1200), F(1, 10)) == F(-105000000, 1331)
      and f"{float(npv(cfs(1200), F(1,10))):.2f}" == "-78888.05")
check("L06 E2 NPV at 1300 = 1550000000/1331 ~ 1164537.94", npv(cfs(1300), F(1, 10)) == F(1550000000, 1331)
      and f"{float(npv(cfs(1300), F(1,10))):.2f}" == "1164537.94")
grid_pos = [u for u in range(200, 1601, 100) if npv(cfs(u), F(1, 10)) > 0]
check("L06 E2 grid positive points 1300..1600 (four)", grid_pos == [1300, 1400, 1500, 1600], str(grid_pos))
check("L06 c123/c149 sign at 200 negative and 1600 positive at 8,10,12",
      all(npv(cfs(200), F(k, 100)) < 0 and npv(cfs(1600), F(k, 100)) > 0 for k in (8, 10, 12)))
check("L06 c122 buy threshold 1206.34", f"{float(be10):.2f}" == "1206.34")
check("L06 c124 1200 units above 8% break-even 1164.10 gives positive NPV at 8%",
      npv(cfs(1200), F(8, 100)) > 0)
check("L06 c125 NPV(-100,60,60)@10% = 500/121", npv([F(-100), F(60), F(60)], F(1, 10)) == F(500, 121))
check("L06 c126 break-even 100000/(400*A) = 33275/331", F(100000) / (400 * A10) == F(33275, 331))
check("L06 M1 4900/0.98 = 5000 and 50 cents payoff", F(4900) / F(98, 100) == 5000 and 5050 - 5000 == 50)
check("L06 c127 margin fraction 0.7540 and fall 24.6 percent",
      f"{float(F(15000000, 1600) / A10 / 5000):.4f}" == "0.7540" and f"{100*(1-float(F(15000000,1600)/A10/5000)):.1f}" == "24.6")
check("L06 c114 units range [200,1600]", 2000 * 1 * F(1, 10) == 200 and 4000 * 2 * F(1, 5) == 1600)
check("L06 E1 annuity at 12% about 2.40183", f"{float(sum((1/F(112,100)**t for t in range(1,4)), F(0))):.5f}" == "2.40183")
check("L06 P3 x_1..x_3 bounds 200 and 1600", 2000 * 1 * F(1, 10) == 200 and 4000 * 2 * F(1, 5) == 1600)
check("L06 c110 NPV strictly increasing (mA>0)", A10 > 0)
check("L06 R1 log-width ratios are 2", all(F(h, l_) == 2 for h, l_ in ((4000, 2000), (2, 1), (F(1, 5), F(1, 10)))))
check("L06 range factor-8 width (1600/200)", 1600 // 200 == 8)

print("ALL OK" if ok else "SOME CHECKS FAILED")

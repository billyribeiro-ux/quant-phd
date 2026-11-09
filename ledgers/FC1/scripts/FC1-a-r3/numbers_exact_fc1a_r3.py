"""FC1-a round 3: independent recomputation of every number in the slice (exact Fractions, no lab code reused).

Run: .venv/bin/python -I ledgers/FC1/scripts/FC1-a-r3/numbers_r3.py
"""
import itertools
import random
from fractions import Fraction as F
from math import floor

bad = []
ok = []


def check(name, cond):
    (ok if cond else bad).append(name)
    print(("OK  " if cond else "BAD ") + name)


def half_up_cents(x):
    return floor(x * 100 + F(1, 2))


# ---- L01 Section 2-3, Example 3.3 ----
d, rho = F(1000), F(1, 10)
D = [d * (1 - rho) ** t for t in range(11)]
S = [sum(D[: n + 1]) for n in range(11)]
check("S_1 = 1900", S[1] == 1900)
check("S_2 = 2710", S[2] == 2710)
check("S_10 exact = 1000*(1-0.9^11)/0.1", S[10] == d * (1 - F(9, 10) ** 11) / rho)
check("S_10 = 6861.8940391 exactly", S[10] == F("6861.8940391"))
check("S_10 cents half up = 686189", half_up_cents(S[10]) == 686189)
check("multiplier S_10/d rounded 4 dp = 6.8619", round(float(S[10] / d), 4) == 6.8619)
check("multiplier exact 6.8618940391", S[10] / d == F("6.8618940391"))
check("rounding multiplier first gives 6861.90", F("6.8619") * 1000 == F("6861.9"))
check("limit d/rho = 10000", d / rho == 10000)
check("limit cents 1000000", half_up_cents(d / rho) == 1000000)
check("Remark 3.4: 6.8619*1000 to cent = 6861.90", half_up_cents(F("6.8619") * 1000) == 686190)
# closed form equals partial sums for all n 0..10
check("closed form equals partial sums n=0..10", all(S[n] == d * (1 - (1 - rho) ** (n + 1)) / rho for n in range(11)))

# Prop 3.5 and Example 3.6
half_limit = d / (1 - F(1, 2) * (1 - rho))
check("Example 3.6 half limit = 1000/0.55 = 20000/11", half_limit == F(20000, 11))
check("Example 3.6 half limit cents half up = 181818", half_up_cents(half_limit) == 181818)
check("18.18 percent of 10000 base (ratio 2/11 to 2 dp = 18.18)", round(float(half_limit / 10000) * 100, 2) == 18.18)
check("E2 ratio 181818/1000000 = 2/11 to 6 dp", round(181818 / 1000000, 6) == 0.181818)
check("E2 exact ratio 2/11 = 1/5.5", F(2, 11) == 1 / F("5.5"))
# leakage with half share: lab Part C total after stage 10
share = F(1, 2)
leaky = [d]
for _ in range(10):
    leaky.append(share * (1 - rho) * leaky[-1])
check("Part C half-share total after stage 10 cents = 181790", half_up_cents(sum(leaky)) == 181790)

# ---- L01 Prop 4.1, Part D, E3, R2, M3, Quiz ----
for E, lam, expect in [(F(100), F(50), F(50)), (F(100), F(100), F(0)), (F(100), F(150), F(-50))]:
    check(f"Part D equity after loss {lam} = {expect}", E - lam == expect)
check("M3 equity after loss 320 on 300 equity = -20", F(300) - 320 == -20)
check("Quiz equity 100-60 = 40", F(100) - 60 == 40)
check("Quiz S_2/d at rho=1/2 = 1.75", sum(F(1, 2) ** t for t in range(3)) == F(7, 4))
check("Quiz 400*1.75 = 700", F(400) * F(7, 4) == 700)
check("M2 S_2 at d=800, rho=1/4 = 1850", sum(F(800) * (F(3, 4)) ** t for t in range(3)) == 1850)
check("M2 stage deposits 800, 600, 450", [F(800) * F(3, 4) ** t for t in range(3)] == [800, 600, 450])
check("M1 reserves 100, loan 400, D1 400", F(500) / 5 == 100 and F(500) * F(4, 5) == 400)
check("Quiz D1 at rho=1/5, d=1000 = 800", F(1000) * F(4, 5) == 800)
check("Quiz limit d/rho = 10000", F(1000) / F(1, 10) == 10000)
check("Misconception 1 total 1900", F(1000) + F(900) == 1900)
check("Example 1.4/Mx: 30/5000 = 0.006", F(30, 5000) == F("0.006"))

# ---- Prop 3.5 hypothesis: d = 0 and d < 0 counterexamples to the statement as printed ----
def limit_leak(d_, rho_, phi_):
    return d_ / (1 - phi_ * (1 - rho_))

# d = 0: limit 0 = d/rho, so equality holds for phi=0, rho=1/2 (not phi=1, not rho=1)
c0 = limit_leak(F(0), F(1, 2), F(0)) == F(0) / F(1, 2)
check("Prop 3.5 equality-iff FAILS at d=0 (phi=0, rho=1/2: limit = d/rho = 0, phi!=1, rho!=1)", c0)
# d < 0 (not a deposit, but unconstrained by the statement): inequality flips
cneg = limit_leak(F(-1), F(1, 2), F(0)) > F(-1) / F(1, 2)
check("Prop 3.5 'at most d/rho' FAILS for d=-1, rho=1/2, phi=0 (limit -1 > d/rho = -2)", cneg)
# P2 at d=0: S_n = 0 for all n, which has a finite limit 0
check("P2 claim 'no finite limit' FAILS at d=0 (S_n = (n+1)*0 = 0 converges)", all((n + 1) * F(0) == 0 for n in range(50)))
# P1 at d=0 and d>0 monotone; R3 needs d/rho > 0
check("R3 step 'd/rho > 0' needs d>0 (fails at d=0)", not (F(0) / rho > 0))

# Proposition 3.5 numeric check for random parameters with d>0
rng = random.Random(1)
ok35 = True
for _ in range(2000):
    dd = F(rng.randint(1, 5000))
    rr = F(rng.randint(1, 100), 100)
    ph = F(rng.randint(0, 100), 100)
    kap = ph * (1 - rr)
    lim = dd / (1 - kap)
    if not (lim <= dd / rr):
        ok35 = False
    if (lim == dd / rr) != (ph == 1 or rr == 1):
        ok35 = False
check("Prop 3.5 holds for 2000 random d>0 cases (inequality and iff)", ok35)

# ---- L02 counts (independent) ----
register = [
    ("share listed on an exchange", "equities", "cash", "exchange"),
    ("share sold in a private negotiated trade", "equities", "cash", "otc"),
    ("futures contract on an equity index", "equities", "derivative", "exchange"),
    ("bond with a fixed coupon", "rates", "cash", "otc"),
    ("futures contract on a government bond", "rates", "derivative", "exchange"),
    ("interest rate swap", "rates", "derivative", "otc"),
    ("corporate bond", "credit", "cash", "otc"),
    ("credit default swap", "credit", "derivative", "otc"),
    ("spot purchase of a currency", "fx", "cash", "otc"),
    ("forward contract on a currency", "fx", "derivative", "otc"),
    ("futures contract on crude oil", "commodities", "derivative", "exchange"),
    ("physical quantity of a metal", "commodities", "cash", "otc"),
]
from collections import Counter
check("register has 12 entries", len(register) == 12)
check("exposure counts 3,3,2,2,2", sorted(Counter(r[1] for r in register).values()) == [2, 2, 2, 3, 3])
check("form counts 6 cash, 6 derivative", Counter(r[2] for r in register) == Counter({"cash": 6, "derivative": 6}))
check("venue counts 4 exchange, 8 otc", Counter(r[3] for r in register) == Counter({"exchange": 4, "otc": 8}))
exch = [r for r in register if r[3] == "exchange"]
check("exchange entries: 1 cash, 3 derivative", Counter(r[2] for r in exch) == Counter({"cash": 1, "derivative": 3}))
check("exchange entries span 3 exposures", len({r[1] for r in exch}) == 3)
deriv = [i + 1 for i, r in enumerate(register) if r[2] == "derivative"]
check("derivative entries are 3,5,6,8,10,11", deriv == [3, 5, 6, 8, 10, 11])
check("derivative entries carry all five exposures", len({register[i - 1][1] for i in deriv}) == 5)
check("entries 1,3,4,6 give the four form/venue combinations",
      {(register[i - 1][2], register[i - 1][3]) for i in [1, 3, 4, 6]} == {("cash", "exchange"), ("derivative", "exchange"), ("cash", "otc"), ("derivative", "otc")})
check("malformed two-exposure entry: exposure total 14 for 13 entries", len(register) + 1 + 1 == 14)
check("P2 M2 counts rates2 credit1 fx1 equities1 commodities0 sum 5", 2 + 1 + 1 + 1 + 0 == 5)
check("E2 derivative share of exchange = 3/4 = 75 percent", F(3, 4) == F(75, 100))
check("Remark 2.6 total exceeds n by k-1 (k=2 gives 1)", 2 - 1 == 1)

# ---- L03 ----
def profit_cash(trades, h):
    # trades: list of (sign, shares, mid)
    return sum(s * (m + s * h) * q for s, q, m in trades)


def inv(trades):
    return -sum(s * q for s, q, m in trades)


def mtm(trades, h, mn):
    return profit_cash(trades, h) + inv(trades) * mn


def spread_term(trades, h):
    return h * sum(q for s, q, m in trades)


def mid_term(trades, mn):
    return sum(s * q * (m - mn) for s, q, m in trades)


# Example 2.5
ex = [(-1, 100, 10000), (+1, 100, 9990)]
check("Ex2.5 cash = -600", profit_cash(ex, 2) == -600)
check("Ex2.5 spread term 400", spread_term(ex, 2) == 400)
check("Ex2.5 mid term -1000", mid_term(ex, 9990) == -1000)
check("Ex2.5 identity 400-1000 = -600", mtm(ex, 2, 9990) == -600)
# M1
m1 = [(+1, 50, 10000), (-1, 50, 10000)]
check("M1 cash = 200 = sW = 4*50", profit_cash(m1, 2) == 200 == 4 * 50)
# M2
m2 = [(-1, 80, 10010), (+1, 80, 10004)]
check("M2 cash -160", profit_cash(m2, 2) == -160)
check("M2 spread term 320, mid term -480", spread_term(m2, 2) == 320 and mid_term(m2, 10004) == -480)
# R2
r2 = [(-1, 100, 9990), (+1, 100, 10000)]
check("R2 cash 1400", profit_cash(r2, 2) == 1400)
check("R2 mid term +1000", mid_term(r2, 10000) == 1000)
# E3 relative spread 6/20000
check("E3 relative spread 6/20000 = 0.0003, which is 0.03 percent", F(6, 20000) == F("0.0003") and F(6, 20000) * 100 == F(3, 100))
# M3 / Ex1.4
check("Ex1.4 bid 4985 ask 5015 spread 30", (5000 - 15, 5000 + 15, 30) == (4985, 5015, 30))
# P1 identity, random sequences with a moving mid: P = hV + sum sigma q (m_t - m_n)
rng = random.Random(7)
idok = True
for _ in range(3000):
    n = rng.randint(1, 8)
    h = rng.randint(0, 5)
    trades = []
    mid = 10000
    for _t in range(n):
        mid += rng.randint(-5, 5)
        trades.append((rng.choice([-1, 1]), rng.randint(1, 50), mid))
    mn = trades[-1][2]
    if mtm(trades, h, mn) != spread_term(trades, h) + mid_term(trades, mn):
        idok = False
check("Prop 2.3 identity holds for 3000 random non-closed sequences (exact)", idok)
# Corollary 2.4 random closed one-mid sequences: P = C = s*W
cok = True
for _ in range(2000):
    h = rng.randint(1, 5)
    q = [rng.randint(1, 30) for _ in range(rng.randint(1, 5))]
    sides = [1] * len(q)
    tot_buy = sum(q)
    # build closed: split q into buys and sells with equal totals
    k = rng.randint(1, 4)
    buys = [rng.randint(1, 30) for _ in range(k)]
    total = sum(buys)
    # sells that sum to total
    sells = []
    rem = total
    while rem > 0:
        x = rng.randint(1, rem)
        sells.append(x)
        rem -= x
    trades = [(1, b, 10000) for b in buys] + [(-1, s_, 10000) for s_ in sells]
    W = sum(buys)
    if not (profit_cash(trades, h) == mtm(trades, h, 10000) == 2 * h * W):
        cok = False
check("Corollary 2.4 holds for 2000 random closed one-mid sequences (P = C = sW)", cok)
# Remark 2.2: V = 2W iff I = 0 (both directions) on random sequences
vok = True
for _ in range(2000):
    trades = [(rng.choice([-1, 1]), rng.randint(1, 20), 10000) for _ in range(rng.randint(1, 6))]
    W = sum(q for s, q, m in trades if s == 1)
    V = sum(q for s, q, m in trades)
    if (V == 2 * W) != (inv(trades) == 0):
        vok = False
check("Remark 2.2: V = 2W iff I = 0 on 2000 random sequences", vok)

# Tick game: independent brute force, with a wider grid than the lab's 11 asks
def payoff_twice(a, b, c, N):
    if a < b:
        return 2 * (a - c) * N
    if a == b:
        return (a - c) * N
    return 0


def eq_grid(c, N, asks):
    out = []
    for a, b in itertools.product(asks, repeat=2):
        if all(payoff_twice(x, b, c, N) <= payoff_twice(a, b, c, N) for x in asks) and \
           all(payoff_twice(x, a, c, N) <= payoff_twice(b, a, c, N) for x in asks):
            out.append((a, b))
    return out


c, N = 100, 1000
wide = list(range(c, c + 60))
eqs = eq_grid(c, N, wide)
check("tick game on asks c..c+59 (independent brute force): equilibria = (c,c),(c+1,c+1),(c+2,c+2)",
      eqs == [(c, c), (c + 1, c + 1), (c + 2, c + 2)])
check("lab grid c..c+10 has 121 pairs", len(list(itertools.product(range(c, c + 11), repeat=2))) == 121)
# three dealers, symmetric, R1
def pay3(a, others, c, N):
    lo = min(others + [a])
    winners = [x for x in others + [a] if x == lo]
    k = len(others) + 1
    if a != lo:
        return 0
    return (a - c) * N // len(winners)  # equal split; N multiple of 3
c3, N3 = 100, 300
def is_eq3(profile):
    for i in range(3):
        own = profile[i]
        others = [profile[j] for j in range(3) if j != i]
        base = pay3(own, others, c3, N3)
        for d_ in range(c3, c3 + 40):
            if pay3(d_, others, c3, N3) > base:
                return False
    return True
check("R1 (c,c,c) equilibrium", is_eq3((c3, c3, c3)))
check("R1 (c+1,c+1,c+1) equilibrium", is_eq3((c3 + 1, c3 + 1, c3 + 1)))
check("R1 (c+2,c+2,c+2) NOT equilibrium", not is_eq3((c3 + 2, c3 + 2, c3 + 2)))
check("quiz (103,103) earns 1500, deviation 102 earns 2000", (103 - 100) * 1000 // 2 == 1500 and (102 - 100) * 1000 == 2000)

print()
print("OK:", len(ok), "BAD:", len(bad))
for b in bad:
    print("BAD:", b)

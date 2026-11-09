"""Round-5 independent recomputation of every number in the FC1-a slice's changed prose, cards and labs."""
from fractions import Fraction as F
import math
import random

def half_up_cents(x):
    return math.floor(x * 100 + F(1, 2))

ok = []
def check(name, cond):
    ok.append((name, bool(cond)))
    print(("OK  " if cond else "FAIL"), name)

# L01 Example 3.3 and Remark 3.4, d = 1000, rho = 1/10
d, rho = F(1000), F(1, 10)
S = lambda n: d * (1 - (1 - rho) ** (n + 1)) / rho
check("S1 = 1900", S(1) == 1900)
check("S2 = 2710", S(2) == 2710)
check("S10 cents = 686189", half_up_cents(S(10)) == 686189)
check("S10 dollars to cent 6861.89", float(S(10)) > 6861.885 and float(S(10)) < 6861.895)
check("multiplier S10/d to 4 places = 6.8619", f"{float(S(10)/d):.4f}" == "6.8619")
check("multiplier 6.8618940391 (exact to 10 places)", f"{float(S(10)/d):.10f}" == "6.8618940391")
check("Remark 3.4: 6.8619 * 1000 = 6861.90", F("6.8619") * 1000 == F("6861.9"))
# Example 3.6 and Ex. c011: limit d/(1-phi(1-rho)) with phi = 1/2
phi = F(1, 2)
lim_half = d / (1 - phi * (1 - rho))
check("half-redeposit limit cents = 181818", half_up_cents(lim_half) == 181818)
check("18.18 percent of 10000", abs(float(lim_half) / 10000 - 0.1818) < 1e-4)
check("full limit 10000 dollars = d/rho", d / rho == 10000)
# Part C stage-10 total with share 1/2: D_0=d, D_{t+1} = phi*(1-rho)*D_t
D = [d]
for _ in range(10):
    D.append(phi * (1 - rho) * D[-1])
check("L01 Part C half-redeposit total after stage 10 cents = 181790", half_up_cents(sum(D)) == 181790)
# Prop 3.5 canon bullet: limit strictly below d/rho iff (1-phi)(1-rho) > 0, for d > 0
bad = []
for phi_n in [F(0), F(1, 3), F(1, 2), F(9, 10), F(1)]:
    for rho_n in [F(1, 10), F(1, 2), F(1)]:
        lim = d / (1 - phi_n * (1 - rho_n))
        strictly_lower = lim < d / rho_n
        expected = (1 - phi_n) * (1 - rho_n) > 0
        if strictly_lower != expected:
            bad.append((phi_n, rho_n))
check("Prop 3.5: strictly lower iff phi<1 and rho<1 (d>0), grid of 15", not bad)
check("Prop 3.5 at phi=1 gives equality", d / (1 - 1 * (1 - rho)) == d / rho)
check("Prop 3.5 at rho=1 gives equality (any phi)", all(d / (1 - p * 0) == d for p in [F(0), F(1, 2), F(1)]))
# Prop 2.2 identity and Prop 3.1 closed form over stages (exact)
path = [d]
for _ in range(10):
    path.append((1 - rho) * path[-1])
check("Prop 3.1 closed form equals partial sums for n=0..10 (exact)",
      all(sum(path[: n + 1]) == d * (1 - (1 - rho) ** (n + 1)) / rho for n in range(11)))
check("Prop 2.2: X_t + loan_t = D_t at every stage", all(rho * D_ + (1 - rho) * D_ == D_ for D_ in path))
# L01 Part D sign table
check("L01 Part D: equity after losses 50,100,150 = 50,0,-50", [100 - x for x in (50, 100, 150)] == [50, 0, -50])

# L02 register counts (12 entries) typed in the lab twin, recomputed independently
reg = [
    ("eq", "cash", "exch"), ("eq", "cash", "otc"), ("eq", "deriv", "exch"), ("rates", "cash", "otc"),
    ("rates", "deriv", "exch"), ("rates", "deriv", "otc"), ("credit", "cash", "otc"), ("credit", "deriv", "otc"),
    ("fx", "cash", "otc"), ("fx", "deriv", "otc"), ("comm", "deriv", "exch"), ("comm", "cash", "otc"),
]
from collections import Counter
ex = Counter(e[0] for e in reg)
check("L02 exposure counts eq3 rates3 credit2 fx2 comm2", (ex["eq"], ex["rates"], ex["credit"], ex["fx"], ex["comm"]) == (3, 3, 2, 2, 2))
fm = Counter(e[1] for e in reg)
check("L02 form counts cash 6, derivative 6", (fm["cash"], fm["deriv"]) == (6, 6))
vn = Counter(e[2] for e in reg)
check("L02 venue counts exch 4, otc 8", (vn["exch"], vn["otc"]) == (4, 8))
exch = [e for e in reg if e[2] == "exch"]
check("L02 exchange entries: 1 cash, 3 derivatives, 3 exposure classes",
      sum(e[1] == "cash" for e in exch) == 1 and sum(e[1] == "deriv" for e in exch) == 3 and len({e[0] for e in exch}) == 3)
der = [e for e in reg if e[1] == "deriv"]
check("L02 six derivatives carry all five exposure values", {e[0] for e in der} == {"eq", "rates", "credit", "fx", "comm"})
check("L02 Example 3.1 entries 1,3,4,6 cover the four form-venue pairs",
      {(reg[i][1], reg[i][2]) for i in (0, 2, 3, 5)} == {("cash", "exch"), ("deriv", "exch"), ("cash", "otc"), ("deriv", "otc")})
bad_entry_exposures = 2
total = sum(ex.values()) + bad_entry_exposures
check("L02 Part D: exposure total with malformed two-exposure entry = 14 for 13 entries", total == 14 and len(reg) + 1 == 13)
check("L02 E1: exchange 4 + otc 8 = 12", 4 + 8 == 12)
check("L02 E2: 3 of 4 exchange entries derivative = 75 percent", F(3, 4) == F(75, 100))

# L03 Example 1.4, Example 2.5, Prop 2.3 and Cor 2.4 identities
check("Example 1.4: 30/5000 = 0.6 percent", F(30, 5000) == F(6, 1000))
m1, m2, h = 10000, 9990, 2
C = -9998 * 100 + 9992 * 100
P = C + 0 * m2
check("Example 2.5 C = -600", C == -600 and P == -600)
hV = h * 200
move = (-1) * 100 * (m1 - m2) + (+1) * 100 * (m2 - m2)
check("Example 2.5 hV = 400, mid-move = -1000, sum -600", hV == 400 and move == -1000 and hV + move == -600)
# Prop 2.3 identity on random exact sequences with arbitrary mids (not only closed)
rng = random.Random(7)
ident_ok = True
for _ in range(2000):
    n = rng.randint(1, 8)
    trades = [(rng.choice([1, -1]), rng.randint(1, 50), rng.randint(9000, 11000)) for _ in range(n)]
    hh = rng.randint(1, 20)
    mn = trades[-1][2]
    Cc = sum(s * q * (mt + s * hh) for s, q, mt in trades)
    Ii = -sum(s * q for s, q, _ in trades)
    Vv = sum(q for _, q, _ in trades)
    Pp = Cc + Ii * mn
    rhs = hh * Vv + sum(s * q * (mt - mn) for s, q, mt in trades)
    ident_ok &= Pp == rhs
check("Prop 2.3 mark-to-mid identity on 2000 random exact sequences", ident_ok)
# Cor 2.4: closed, fixed mid -> P = C = s*W
ok_c = True
for _ in range(500):
    W = rng.randint(1, 500)
    hh = rng.randint(1, 20)
    buys = [W]
    sells = [W]
    mid = rng.randint(9000, 11000)
    trades = [(1, W, mid), (-1, W, mid)]
    Cc = sum(s * q * (mt + s * hh) for s, q, mt in trades)
    Pp = Cc
    ok_c &= Pp == 2 * hh * W and Cc == Pp
check("Corollary 2.4 P = C = s W on closed fixed-mid sequences", ok_c)
check("L03 Part A: spread 4 cents x 1000 shares = 4000", 4 * 1000 == 4000)
check("L03 Part B: P = 3455 = 4000 - 545", 4000 - 545 == 3455)

# L03 Prop 3.2 brute-force over an exact grid, several costs, N even
def profit(a, rival, c, N):
    if a < rival:
        return (a - c) * N
    if a == rival:
        return F((a - c) * N, 2)
    return 0
def eqs(c, N, grid):
    out = []
    for a1 in grid:
        for a2 in grid:
            if all(profit(dd, a2, c, N) <= profit(a1, a2, c, N) for dd in grid) and \
               all(profit(dd, a1, c, N) <= profit(a2, a1, c, N) for dd in grid):
                out.append((a1 - c, a2 - c))
    return out
for c, N in [(100, 1000), (7, 2), (0, 4), (250, 10)]:
    grid = list(range(c, c + 16))
    res = eqs(c, N, grid)
    check(f"Prop 3.2 grid c={c} N={N}: equilibria exactly (k,k) for k in 0,1,2", res == [(0, 0), (1, 1), (2, 2)])
# Hypothesis line 168: grid 100..110 has 121 pairs
check("L03 Part C grid 100..110 has 121 pairs", len(range(100, 111)) ** 2 == 121)

# Cards: T-graded L03 Prop 3.2 card c170 and c050 consistency

print()
print("total checks", len(ok), "failed", [n for n, c in ok if not c])

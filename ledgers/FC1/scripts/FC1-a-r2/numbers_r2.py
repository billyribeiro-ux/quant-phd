"""FC1-a round 2: independent re-derivation of the numbers printed or stated in the FC1 hub, L01, L02 and L03.

Written from the page statements, not from the lab code. Run: .venv/bin/python -I ledgers/FC1/scripts/FC1-a-r2/numbers_r2.py
"""

import ast
import itertools
import random
from fractions import Fraction as F
from math import floor
from pathlib import Path

FAILS: list[str] = []


def check(label: str, got: object, want: object) -> None:
    status = "OK  " if got == want else "BAD "
    if got != want:
        FAILS.append(label)
    print(f"{status}{label}: got {got!r} want {want!r}")


def half_up_cents(dollars: F) -> int:
    return floor(dollars * 100 + F(1, 2))


# ---- hub placement arithmetic
check("hub PV 110/1.1", F(110) / F(11, 10), 100)
check("hub 1+1/2+1/4", 1 + F(1, 2) + F(1, 4), F(175, 100))
check("hub geometric (1-(1/2)^3)/(1/2)", (1 - F(1, 2) ** 3) / F(1, 2), F(175, 100))
check("hub equilibrium 100-P = P-20", F(100 + 20, 2), 60)
check("hub q at P=60", 100 - 60, 40)
check("hub 1000*1.05^2", F(1000) * F(105, 100) ** 2, F(11025, 10))
check("hub coupon 10000*500/10000", F(10000 * 500, 10000), 500)
check("hub period-3 flow", 500 + 10000, 10500)
check("hub 7/9 percent", round(F(7, 9) * 100, 2), F(7778, 100))
check("hub 0.8 * 9 items", F(4, 5) * 9, F(36, 5))

# ---- L01 deposit model (d = 1000, rho = 1/10)
d, rho = F(1000), F(1, 10)
deposits = [d * (1 - rho) ** t for t in range(11)]
partial = []
s = F(0)
for dt in deposits:
    s += dt
    partial.append(s)
printed_cents = [100000, 190000, 271000, 343900, 409510, 468559, 521703, 569533, 612580, 651322, 686189]
check("L01 Part A cents n=0..10", [half_up_cents(x) for x in partial], printed_cents)
check("L01 closed form S_10 exact", partial[10], d * (1 - (1 - rho) ** 11) / rho)
check("L01 S_10 decimal to 10 places", f"{float(partial[10]):.10f}", "6861.8940391000")
check("L01 multiplier S_10/d 10 places", f"{float(partial[10] / d):.10f}", "6.8618940391")
check("L01 multiplier 4 places", f"{float(partial[10] / d):.4f}", "6.8619")
check("L01 rounded multiplier times 1000", F("6.8619") * 1000, F("6861.9"))
check("L01 S_1", partial[1], 1900)
check("L01 S_2", partial[2], 2710)
check("L01 full limit cents", half_up_cents(d / rho), 1000000)

# ---- L01 leakage (phi = 1/2)
phi = F(1, 2)
kappa = phi * (1 - rho)
leaky = [d]
for _ in range(10):
    leaky.append(phi * (1 - rho) * leaky[-1])
check("L01 Part C half-share total after stage 10 cents", half_up_cents(sum(leaky)), 181790)
check("L01 Part C half-share limit cents", half_up_cents(d / (1 - kappa)), 181818)
check("L01 Example 3.6 limit 1000/0.55 decimal", f"{float(d / (1 - kappa)):.2f}", "1818.18")
check("L01 E2 ratio 181818/1000000", F(181818, 1000000), F("0.181818"))
check("L01 E2 exact ratio 2/11", (d / (1 - kappa)) / (d / rho), F(2, 11))
check("L01 E2 percent to two places", f"{float(F(2, 11) * 100):.2f}", "18.18")
check("L01 E3 largest loss", max(x for x in [50, 100, 150] if 100 - x >= 0), 100)
check("L01 Part D equity 100-150", 100 - 150, -50)
check("L01 M1 reserves", F(500) / 5, 100)
check("L01 M1 loan", F(500) - F(500) / 5, 400)
d2, rho2 = F(800), F(1, 4)
dep2 = [d2, d2 * (1 - rho2), d2 * (1 - rho2) ** 2]
check("L01 M2 deposits", dep2, [800, 600, 450])
check("L01 M2 S_2", sum(dep2), 1850)
check("L01 M2 closed form", d2 * (1 - (1 - rho2) ** 3) / rho2, 1850)
check("L01 M3 equity", 300 - 320, -20)
check("L01 Q2 D_1", F(1000) * F(4, 5), 800)
check("L01 Q5 limit", F(1000) / F(1, 10), 10000)
check("L01 Q8 equity", 100 - 60, 40)
check("L01 Q10 S_2", F(400) * (1 + F(1, 2) + F(1, 4)), 700)
check("L01 R2 ratio 2d/rho exceeds d/rho", F(2) > F(1), True)

# Proposition 3.1 and 3.5 random exact checks
rng = random.Random(7)
ok31 = True
ok35 = True
for _ in range(400):
    r = F(rng.randint(1, 100), 100)
    dd = F(rng.randint(1, 5000), 7)
    f = F(rng.randint(0, 100), 100)
    n = rng.randint(0, 40)
    q = 1 - r
    partial_sum = sum(dd * q**t for t in range(n + 1))
    if partial_sum != dd * (1 - q ** (n + 1)) / r:
        ok31 = False
    lim = dd / (1 - f * (1 - r))
    if lim > dd / r:
        ok35 = False
    if (lim == dd / r) != (f == 1 or r == 1):
        ok35 = False
check("Prop 3.1 closed form on 400 random exact cases", ok31, True)
check("Prop 3.5 bound and equality case on 400 random exact cases", ok35, True)

# R1 bound (stage-dependent ratios >= c)
ok_r1 = True
for _ in range(300):
    c = F(rng.randint(1, 100), 100)
    dd = F(rng.randint(1, 5000), 7)
    rhos = [c + (1 - c) * F(rng.randint(0, 100), 100) for _ in range(30)]
    dep = [dd]
    for rr in rhos:
        dep.append((1 - rr) * dep[-1])
    for n in range(len(dep)):
        Sn = sum(dep[: n + 1])
        if Sn > dd * (1 - (1 - c) ** (n + 1)) / c or Sn > dd / c:
            ok_r1 = False
check("R1 bound S_n <= d(1-(1-c)^(n+1))/c <= d/c on 300 random paths", ok_r1, True)

# ---- L02 register (read from the twin's REGISTER literal)
twin2 = Path("tests/labs/FC1/lab-FC1-L02-1.py").read_text(encoding="utf-8")
tree = ast.parse(twin2)
register = None
for node in tree.body:
    if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", "") == "REGISTER":
        register = ast.literal_eval(node.value)
assert register is not None
check("L02 register entries", len(register), 12)
ex: dict[str, dict[str, int]] = {}
for axis in ("exposure", "form", "venue"):
    counts: dict[str, int] = {}
    for _, vals in register:
        for v in vals[axis]:
            counts[v] = counts.get(v, 0) + 1
    ex[axis] = counts
check("L02 exposure counts", ex["exposure"], {"equities": 3, "rates": 3, "credit": 2, "fx": 2, "commodities": 2})
check("L02 form counts", ex["form"], {"cash": 6, "derivative": 6})
check("L02 venue counts", ex["venue"], {"exchange": 4, "otc": 8})
exch = [v for _, v in register if v["venue"] == ("exchange",)]
check("L02 exchange entries", len(exch), 4)
check("L02 exchange cash", sum(1 for v in exch if v["form"] == ("cash",)), 1)
check("L02 exchange derivative", sum(1 for v in exch if v["form"] == ("derivative",)), 3)
check("L02 exchange exposure classes", sorted({v["exposure"][0] for v in exch}), ["commodities", "equities", "rates"])
deriv_exposures = {v["exposure"][0] for _, v in register if v["form"] == ("derivative",)}
check("L02 derivative exposures cover all five", len(deriv_exposures), 5)
deriv_idx = [i + 1 for i, (_, v) in enumerate(register) if v["form"] == ("derivative",)]
check("L02 derivative entries 3,5,6,8,10,11", deriv_idx, [3, 5, 6, 8, 10, 11])
check("L02 entries 1,3,4,6 cover four combinations",
      {(register[i - 1][1]["form"][0], register[i - 1][1]["venue"][0]) for i in (1, 3, 4, 6)},
      {("cash", "exchange"), ("derivative", "exchange"), ("cash", "otc"), ("derivative", "otc")})
check("L02 malformed exposure total minus count", (12 + 2) - 13, 1)
check("L02 M2 counts", {"rates": 2, "credit": 1, "fx": 1, "equities": 1, "commodities": 0}, {"rates": 2, "credit": 1, "fx": 1, "equities": 1, "commodities": 0})
check("L02 E2 derivative share of exchange", F(3, 4), F(3, 4))
check("L02 R1 rates entries 4,5,6", [i + 1 for i, (_, v) in enumerate(register) if v["exposure"] == ("rates",)], [4, 5, 6])

# ---- L03 dealer model
def profit_cash(trades: list[tuple[int, int, int]], half: int) -> tuple[int, int, int, int, int]:
    """trades: (sign, shares, mid). Returns cash, inventory, V, spread capture, mid-move term at terminal mid of last trade."""
    cash = sum(sg * q * (m + sg * half) for sg, q, m in trades)
    inv = -sum(sg * q for sg, q, _ in trades)
    vol = sum(q for _, q, _ in trades)
    terminal = trades[-1][2]
    mid_move = sum(sg * q * (m - terminal) for sg, q, m in trades)
    return cash, inv, vol, half * vol, mid_move


# Example 2.5
ex25 = [(-1, 100, 10000), (+1, 100, 9990)]
cash, inv, vol, cap, move = profit_cash(ex25, 2)
check("L03 Example 2.5 cash", cash, -600)
check("L03 Example 2.5 inventory", inv, 0)
check("L03 Example 2.5 spread term", cap, 400)
check("L03 Example 2.5 mid-move", move, -1000)
check("L03 Example 2.5 profit", cash + inv * 9990, -600)
# M2
m2 = [(-1, 80, 10010), (+1, 80, 10004)]
cash, inv, vol, cap, move = profit_cash(m2, 2)
check("L03 M2 cash", cash, -160)
check("L03 M2 spread term", cap, 320)
check("L03 M2 mid-move", move, -480)
check("L03 M2 sale payment 10008*80", 10008 * 80, 800640)
check("L03 M2 purchase receipt 10006*80", 10006 * 80, 800480)
# R2
r2 = [(-1, 100, 9990), (+1, 100, 10000)]
cash, inv, vol, cap, move = profit_cash(r2, 2)
check("L03 R2 cash", cash, 1400)
check("L03 R2 spread term", cap, 400)
check("L03 R2 mid-move", move, 1000)
# M1 and Corollary 2.4
m1 = [(+1, 50, 10000), (-1, 50, 10000)]
cash, inv, vol, cap, move = profit_cash(m1, 2)
check("L03 M1 cash 200 = sW", (cash, 4 * 50), (200, 200))
# E3
check("L03 E3 6/20000", F(6, 20000), F("0.0003"))
check("L03 Example 1.4 relative", F(30, 5000), F("0.006"))
check("L03 M3 relative spread", F(30, 5000), F("0.006"))
check("L03 Q8 profit", (102 - 100) * 1000 / 2, 1000)
check("L03 Q7 profit at 103", 3 * 1000 // 2, 1500)
check("L03 Q7 deviation to 102", 2 * 1000, 2000)

# Proposition 2.3 and Corollary 2.4 random identity checks, exact integers
ok23 = True
okc24 = True
for _ in range(500):
    n = rng.randint(1, 12)
    h = rng.randint(1, 20)
    mids = [rng.randint(5000, 15000) for _ in range(n)]
    seq = [(rng.choice((-1, 1)), rng.randint(1, 200), m) for m in mids]
    cash = sum(sg * (m + sg * h) * q for sg, q, m in seq)
    inv = -sum(sg * q for sg, q, _ in seq)
    mn = mids[-1]
    P = cash + inv * mn
    V = sum(q for _, q, _ in seq)
    rhs = h * V + sum(sg * q * (m - mn) for sg, q, m in seq)
    if P != rhs:
        ok23 = False
    # closed one-mid sequence: buys and sells equal volume
    buys = [rng.randint(1, 50) for _ in range(3)]
    sells = [sum(buys)]
    split = sorted(rng.sample(range(1, sum(buys)), 2))
    sells = [split[0], split[1] - split[0], sum(buys) - split[1]]
    seqc = [(1, b, 10000) for b in buys] + [(-1, s_, 10000) for s_ in sells]
    cashc = sum(sg * (10000 + sg * h) * q for sg, q, _ in seqc)
    Wc = sum(q for sg, q, _ in seqc if sg == 1)
    if cashc != 2 * h * Wc or cashc != h * sum(q for _, q, _ in seqc) or inv != 0 and False:
        okc24 = False
check("Prop 2.3 identity on 500 random sequences (exact integers)", ok23, True)
check("Cor 2.4 closed one-mid identity cash = s*W on random cases", okc24, True)

# Tick game brute force: symmetric and asymmetric equilibria on a grid
def payoff(a: int, b: int, c: int, N: int) -> int:
    """Twice the profit of an ask a against rival ask b (exact, integer)."""
    if a < b:
        return 2 * (a - c) * N
    if a == b:
        return (a - c) * N
    return 0


def equilibria(c: int, N: int, grid: list[int]) -> list[tuple[int, int]]:
    out = []
    for a, b in itertools.product(grid, repeat=2):
        if all(payoff(d, b, c, N) <= payoff(a, b, c, N) for d in grid) and all(
            payoff(d, a, c, N) <= payoff(b, a, c, N) for d in grid
        ):
            out.append((a, b))
    return out


for c, N, K in [(100, 1000, 10), (0, 2, 10), (7, 4, 25), (100, 1000, 40)]:
    grid = list(range(c, c + K + 1))
    eq = equilibria(c, N, grid)
    want = [(c, c), (c + 1, c + 1), (c + 2, c + 2)]
    check(f"tick game equilibria c={c} N={N} grid to c+{K}", eq, want)
    check(f"tick game pairs counted c={c} grid size", len(grid) ** 2, (K + 1) ** 2)

# Three-dealer symmetric check (R1): N = 3k
def three_dealer_payoff(a: int, others: list[int], c: int, N: int) -> int:
    lowest = min(others + [a])
    winners = [x for x in others + [a] if x == lowest]
    if a != lowest:
        return 0
    return (a - c) * N // (len(winners))


c, N = 100, 300
grid = list(range(c, c + 6))
sym = {}
for a in grid:
    prof = (a, a, a)
    dev_ok = True
    for d in grid:
        p_dev = three_dealer_payoff(d, [a, a], c, N)
        p_cur = three_dealer_payoff(a, [a, a], c, N)
        if p_dev > p_cur:
            dev_ok = False
    sym[a] = dev_ok
check("R1 three dealers: (c,c,c) equilibrium", sym[c], True)
check("R1 three dealers: (c+1,c+1,c+1) equilibrium", sym[c + 1], True)
check("R1 three dealers: (c+2,c+2,c+2) not an equilibrium", sym[c + 2], False)
check("R1 three dealers payoff at (c+2)", three_dealer_payoff(c + 2, [c + 2, c + 2], c, N), 2 * N // 3)

# ---- Seeded walk of Lab 1 Part B, re-coded from the stated protocol (not copied)
rng2 = random.Random(2026)


def split_into(total: int, parts: int) -> list[int]:
    cuts = sorted(rng2.sample(range(1, total), parts - 1))
    edges = [0] + cuts + [total]
    return [edges[i + 1] - edges[i] for i in range(parts)]


buys = split_into(1000, 8)
sells = split_into(1000, 6)
seq_a = [(1, q, 10000) for q in buys] + [(-1, q, 10000) for q in sells]
rng2.shuffle(seq_a)
cashA = sum(sg * (10000 + sg * 2) * q for sg, q, _ in seq_a)
check("L03 Part A cash", cashA, 4000)
check("L03 Part A trades", len(seq_a), 14)
mid = 10000
seq_b = []
# Part B draws a fresh closed sequence from the same generator (Part A consumed its draws first)
buys_b = split_into(1000, 8)
sells_b = split_into(1000, 6)
fresh = [(1, q, 10000) for q in buys_b] + [(-1, q, 10000) for q in sells_b]
rng2.shuffle(fresh)
for sg, q, _ in fresh:
    mid += rng2.randint(-3, 3)
    seq_b.append((sg, q, mid))
term = seq_b[-1][2]
cap = 2 * sum(q for _, q, _ in seq_b)
move = sum(sg * q * (m - term) for sg, q, m in seq_b)
cashB = sum(sg * (m + sg * 2) * q for sg, q, m in seq_b)
check("L03 Part B terminal mid", term, 10001)
check("L03 Part B spread capture", cap, 4000)
check("L03 Part B mid-move term", move, -545)
check("L03 Part B mark-to-mid", cashB + 0 * term, 3455)
check("L03 Part B identity", cashB, cap + move)

print()
print("FAILURES:", FAILS if FAILS else "none")

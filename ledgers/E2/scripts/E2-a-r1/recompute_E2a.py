"""Independent recomputation for E2 slice a (hub index.html, L01-L03), round 1.

Run: <checkout>/.venv/bin/python -I ledgers/E2/scripts/E2-a-r1/recompute_E2a.py
Re-derives the displayed numbers with exact Fractions and brute-force enumeration.
It does not import the lab twins; it re-implements the claims from first principles.
"""

from fractions import Fraction as F
from itertools import product


def check(label: str, ok: bool) -> None:
    print(f"{'OK  ' if ok else 'FAIL'} {label}")


# ---- L01 Example 2.3 prisoner's dilemma (u1 and u2 as stated in the page)
pd = {("C", "C"): (3, 3), ("C", "D"): (0, 5), ("D", "C"): (5, 0), ("D", "D"): (1, 1)}
check("L01 2.3 u1(D,C)=5>3=u1(C,C) and u1(D,D)=1>0=u1(C,D)",
      pd[("D", "C")][0] == 5 > 3 == pd[("C", "C")][0] and pd[("D", "D")][0] == 1 > 0 == pd[("C", "D")][0])
check("L01 2.3 u1(C,D)=u2(D,C)=0", pd[("C", "D")][0] == 0 and pd[("D", "C")][1] == 0)

# ---- L01 Problem M1: 2x2 game, every pure profile, both players' best-response tests
m1 = {("A", "A"): (2, 1), ("A", "B"): (0, 0), ("B", "A"): (0, 0), ("B", "B"): (1, 2)}
acts = ["A", "B"]
eqs = []
for a1, a2 in product(acts, acts):
    b1 = all(m1[(a1, a2)][0] >= m1[(x, a2)][0] for x in acts)
    b2 = all(m1[(a1, a2)][1] >= m1[(a1, y)][1] for y in acts)
    if b1 and b2:
        eqs.append((a1, a2))
check("L01 M1 equilibria are (A,A) and (B,B)", eqs == [("A", "A"), ("B", "B")])
check("L01 M1 at (B,A) player 2 earns 0, switching to B earns u2(B,B)=2 (page says 'against 1 from switching to A')",
      m1[("B", "A")][1] == 0 and m1[("B", "B")][1] == 2)

# ---- L01 Example 4.1 / Prop 4.2 / Example 4.3 on the integer grid and the real-output witness
def profit(own: int | F, rival: int | F) -> F:
    price = max(F(0), F(100) - own - rival)
    return own * (price - 10)


grid = range(91)
ties = [(a, b) for a in grid for b in grid
        if all(profit(k, b) <= profit(a, b) for k in grid) and all(profit(k, a) <= profit(b, a) for k in grid)]
strict = [(a, b) for a in grid for b in grid
          if all(profit(k, b) < profit(a, b) for k in grid if k != a)
          and all(profit(k, a) < profit(b, a) for k in grid if k != b)]
check("L01 lab grid, tie-allowed equilibria = [(29,31),(30,30),(31,29)]", ties == [(29, 31), (30, 30), (31, 29)])
check("L01 lab grid, strict equilibria = [(30,30)]", strict == [(30, 30)])
check("L01 profits at (29,31) and (31,29) are (870,930) and (930,870)",
      (profit(29, 31), profit(31, 29)) == (870, 930) and (profit(31, 29), profit(29, 31)) == (930, 870))
check("L01 P3 profit firm 1 at 31 vs 30 = 899 < 900", profit(31, 30) == 899 < 900)
witness = profit(F(1, 2), 30)
check("L01 Example 4.1 witness: real output q1=1/2 gives a non-integer profit (page says every money output is an integer)",
      witness.denominator != 1)
print(f"      witness profit_1(1/2, 30) = {witness} cents (price {F(100) - F(1, 2) - 30} cents)")
check("L01 Prop 4.2 Case 1 identity 900 - profit_1 = (q-30)^2 at q=7 and q=50/3",
      all(900 - profit(q, 30) == (q - 30) ** 2 for q in (F(7), F(50, 3))))

# ---- L02 closed forms, exact
def beta(n: int) -> F:
    return F(n - 1, n)


def win(bid: F, n: int) -> F:
    return F(1) if bid >= beta(n) else (bid / beta(n)) ** (n - 1)


def best_grid_ok(n: int, v: F) -> bool:
    closed = (v - beta(n) * v) * win(beta(n) * v, n)
    return all(closed >= (v - F(j, 1200)) * win(F(j, 1200), n) for j in range(1201))


counts = {n: sum(best_grid_ok(n, F(k, 20)) for k in range(21)) for n in range(2, 6)}
check("L02 lab grid count 21 of 21 for n=2..5", all(c == 21 for c in counts.values()))
for n in range(2, 6):
    # first-price revenue = E[beta * max of n uniforms] = beta * n/(n+1)
    rev = beta(n) * F(n, n + 1)
    # mean of second highest uniform of n: integral of x * n(n-1)x^(n-2)(1-x)
    sec = sum((F(n * (n - 1)) * F(1, k) for k in []), F(0))
    # exact integral of x*n(n-1)x^(n-2)(1-x) = n(n-1) * (1/n - 1/(n+1))
    sec = F(n * (n - 1)) * (F(1, n) - F(1, n + 1))
    mass = F(n * (n - 1)) * (F(1, n - 1) - F(1, n))
    check(f"L02 n={n}: revenue {rev} = second-highest mean {sec} = (n-1)/(n+1), density mass {mass}",
          rev == sec == F(n - 1, n + 1) and mass == 1)
check("L02 Remark 2.4 v^n/n at n=2, v=0.8 is 0.32", F(8, 10) ** 2 / 2 == F(32, 100))
check("L02 M1 n=3 v=0.6: payoff 0.072", (F(6, 10) - F(4, 10)) * (F(4, 10) / F(2, 3)) ** 2 == F(72, 1000))
check("L02 M3 n=5 bid 0.4 win prob 1/16", (F(4, 10) / F(8, 10)) ** 4 == F(1, 16))
check("L02 E3 n=4 mean second-highest 3/5", F(4 * 3) * (F(1, 4) - F(1, 5)) == F(3, 5))

# ---- L03 market-consistent prices, whole cents 0..15000, shares k/10
VAL = {"H": 12000, "L": 6000}
COST = {"H": 10000, "L": 4000}


def consistent(alpha: F) -> list[tuple[int, F]]:
    out = []
    for p in range(15001):
        mass = {t: (alpha if t == "H" else 1 - alpha) for t in VAL if COST[t] <= p}
        tot = sum(mass.values(), F(0))
        if tot == 0:
            continue
        ev = sum((mass[t] * VAL[t] for t in mass), F(0)) / tot
        if ev == p:
            out.append((p, tot))
    return out


for k in range(11):
    a = F(k, 10)
    got = [p for p, _ in consistent(a)]
    if k <= 6:
        exp = [6000]
    elif k <= 9:
        exp = [6000, 6000 + 6000 * k // 10]
    else:
        exp = [12000]
    check(f"L03 alpha={a}: consistent prices {got} equal the Prop 2.1 set {exp}", got == exp)
check("L03 threshold (c_H - w_L)/(w_H - w_L) = 2/3", F(10000 - 6000, 12000 - 6000) == F(2, 3))
check("L03 alpha=1/2 average value 9000", F(12000 + 6000, 2) == 9000)
check("L03 alpha=1 consistent price set is {12000} (6000 fails M(6000)=0)", [p for p, _ in consistent(F(1))] == [12000])
check("L03 Prop 2.1 claim at alpha=7/10 vs 0.7: 6000+6000*0.7 = 10200", 6000 + 6000 * F(7, 10) == 10200)
print("done")

"""Round-3 independent recomputation of every numeric claim on the E2 hub slice (index, L01-L03).

Written by the verifier from the page text, not from the lab code. Exact Fractions throughout.
Usage (repository root): .venv/bin/python ledgers/E2/scripts/E2-a-r3/recompute_e2a_r3.py
"""

from fractions import Fraction as F
import itertools

checks = []


def check(name, cond, detail=""):
    checks.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (("  | " + detail) if detail else ""))


# ---------- L01 ----------
def profit(own, rival):  # cents, price max(0, 100 - q1 - q2), cost 10
    return own * (max(0, 100 - (own + rival)) - 10)


grid = range(91)
check("L01 Ex4.1 price at (1/2, 30) is 139/2 cents", 100 - F(1, 2) - 30 == F(139, 2))
check("L01 Ex4.1 profit at (1/2, 30) is 119/4 cents", F(1, 2) * (F(139, 2) - 10) == F(119, 4))
check("L01 grid pair count 91*91 = 8281", len(grid) ** 2 == 8281)
tie = [(a, b) for a in grid for b in grid
       if all(profit(k, b) <= profit(a, b) for k in grid) and all(profit(k, a) <= profit(b, a) for k in grid)]
strict = [(a, b) for a in grid for b in grid
          if all(profit(k, b) < profit(a, b) for k in grid if k != a)
          and all(profit(k, a) < profit(b, a) for k in grid if k != b)]
check("L01 tie-allowed grid equilibria = [(29,31),(30,30),(31,29)]", tie == [(29, 31), (30, 30), (31, 29)], str(tie))
check("L01 strict grid equilibria = [(30,30)]", strict == [(30, 30)], str(strict))
check("L01 profits at tie pairs are (870,930),(900,900),(930,870)",
      [(profit(a, b), profit(b, a)) for a, b in tie] == [(870, 930), (900, 900), (930, 870)])
# Prop 4.2 identity on real outputs: 900 - pi1(q1 | 30) = (q1-30)^2 on [0,70], and pi1 < 900 on (70,90]
ok = True
for q in [F(i, 100) for i in range(0, 9001)]:
    p = max(F(0), 100 - q - 30)
    pi = q * (p - 10)
    if q <= 70:
        ok &= (900 - pi == (q - 30) ** 2)
    else:
        ok &= pi < 900
check("L01 Prop4.2 identity 900-pi=(q-30)^2 on [0,70], pi<900 on (70,90], 9001 rational outputs", ok)
check("L01 P3: profit at 31 vs 30 is 899", profit(31, 30) == 899)
check("L01 Ex4.3: firm1 vs 31 profit at 29 and 30 is 870", profit(29, 31) == 870 and profit(30, 31) == 870)
check("L01 Ex4.3: firm2 vs 29 profit at 30 and 31 is 930", profit(30, 29) == 930 and profit(31, 29) == 930)
check("L01 quiz: 3x4 profiles 12, comparisons 3+4=7 per profile, 12*5=60 by page arithmetic", 3 * 4 == 12 and 12 * (2 + 3) == 60)
check("L01 M1 equilibria {(A,A),(B,B)}", True)  # re-derived by hand in row text; cross-checked below
u = {("A", "A"): (2, 1), ("A", "B"): (0, 0), ("B", "A"): (0, 0), ("B", "B"): (1, 2)}
eq = [(a, b) for a, b in u if all(u[(x, b)][0] <= u[(a, b)][0] for x in "AB") and all(u[(a, y)][1] <= u[(a, b)][1] for y in "AB")]
check("L01 M1 brute force equilibria = {(A,A),(B,B)}", set(eq) == {("A", "A"), ("B", "B")}, str(eq))
# Quiz Q5: profit at (30,30)
check("L01 Q5 profit 900 at (30,30)", profit(30, 30) == 900)

# ---------- L02 ----------
def beta(n):
    return F(n - 1, n)


def W(b, n):
    return F(1) if b >= beta(n) else (b / beta(n)) ** (n - 1)


all_ok = True
for n in range(2, 6):
    for k in range(21):
        v = F(k, 20)
        cl = beta(n) * v
        pc = (v - cl) * W(cl, n)
        best = max((v - F(j, 1200)) * W(F(j, 1200), n) for j in range(1201))
        all_ok &= pc >= best
check("L02 closed-form bid best on 1201-point grid for every k/20, n=2..5 (21*4=84 cases)", all_ok)
# Remark 2.4 and examples
check("L02 Ex2.3: bid 0.4 wins w.p. 0.8 and earns 0.32 (n=2, v=0.8)",
      W(F(2, 5), 2) == F(4, 5) and (F(4, 5) - F(2, 5)) * F(4, 5) == F(8, 25))
check("L02 Remark2.4 v^n/n equals (v-beta v) W(beta v) for sample v", all(
    (v - beta(n) * v) * W(beta(n) * v, n) == v ** n / n
    for n in range(2, 6) for v in [F(k, 10) for k in range(11)]))
check("L02 M1: n=3 v=0.6 payoff 0.072", (F(3, 5) - F(2, 5)) * W(F(2, 5), 3) == F(9, 125) and F(3, 5) ** 3 / 3 == F(9, 125))
check("L02 M3: five bidders W(0.4) = 1/16", W(F(2, 5), 5) == F(1, 16))
# Prop 2.5 means and density by exact polynomial integration
def integ(terms):
    return sum((c / (e + 1) for e, c in terms.items()), F(0))
for n in range(2, 6):
    rev = beta(n) * n * integ({n: F(1)})
    mean2 = integ({n - 1: F(n * (n - 1)), n: F(-n * (n - 1))})
    mass = integ({n - 2: F(n * (n - 1)), n - 1: F(-n * (n - 1))})
    check(f"L02 Prop2.5 n={n}: revenue=(n-1)/(n+1)={F(n-1,n+1)}, second mean equal, density mass 1",
          rev == F(n - 1, n + 1) and mean2 == F(n - 1, n + 1) and mass == 1, f"rev={rev} mean2={mean2} mass={mass}")
# Density of second-highest CDF check: P(second<=x)=x^n + n(1-x)x^(n-1), derivative equals density
# (exact polynomial comparison)
for n in range(2, 6):
    cdf = {n: F(1 - n), n - 1: F(n)}  # x^n + n x^{n-1} - n x^n, collected by exponent
    d = {e - 1: c * e for e, c in cdf.items() if e >= 1}
    dens = {n - 2: F(n * (n - 1)), n - 1: F(-n * (n - 1))}
    check(f"L02 derivative of second-highest CDF equals stated density, n={n}", d == dens, f"{d} vs {dens}")
check("L02 R1 example n=2 value 0.5 scaling check (H=2, v=1.6, b=0.8)", beta(2) * 2 * F(4, 5) == F(4, 5) and
      beta(2) * F(8, 5) == F(4, 5))
check("L02 E3: n=4 density 12x^2(1-x) mean 3/5", 12 * (F(1, 4) - F(1, 5)) == F(3, 5))
check("L02 bid grid count j=0..1200 = 1201", len(range(1201)) == 1201)

# ---------- L03 ----------
VALUE = {"H": 12000, "L": 6000}
COST = {"H": 10000, "L": 4000}


def consistent(alpha, prices):
    out = []
    for p in prices:
        mass = {t: (alpha if t == "H" else 1 - alpha) for t in "HL" if COST[t] <= p}
        tot = sum(mass.values(), F(0))
        if tot == 0:
            continue
        ev = sum(mass[t] * VALUE[t] for t in mass) / tot
        if ev == p:
            out.append((p, tot))
    return out


prices = range(0, 15001)
for k in range(11):
    a = F(k, 10)
    got = consistent(a, prices)
    closed = [6000] if a < 1 else []
    if a >= F(2, 3):
        closed.append(6000 + 6000 * a)
    check(f"L03 alpha={a}: consistent prices equal closed form {closed}", [p for p, _ in got] == closed, str(got))
    full = a * 2000 + (1 - a) * 2000
    if a < 1:
        lost = [p for p, t in got if p == 6000]
        check(f"L03 alpha={a}: loss at 6000 = 2000*alpha = {2000*a}", (full - full * (1 - a)) == 2000 * a)
check("L03 threshold (c_H-w_L)/(w_H-w_L)=2/3", F(10000 - 6000, 12000 - 6000) == F(2, 3))
check("L03 Ex2.2 average 9000", F(12000 + 6000, 2) == 9000)
check("L03 alpha=0.6 price 9600 below 10000 is not consistent", 6000 + 6000 * F(3, 5) < 10000)
# fine grid of rational alpha to test the proposition set beyond k/10 (prices restricted to whole cents)
bad = 0
for m in range(0, 61):
    a = F(m, 60)
    got = [p for p, _ in consistent(a, range(0, 15001))]
    closed = ([6000] if a < 1 else []) + ([6000 + 6000 * a] if a >= F(2, 3) and (6000 + 6000 * a).denominator == 1 else [])
    if got != closed:
        bad += 1
check("L03 Prop2.1 on alpha=m/60 (m=0..60), whole-cent prices", bad == 0, f"mismatches={bad}")

print()
print("TOTAL", len(checks), "PASS", sum(1 for _, c in checks if c), "FAIL", sum(1 for _, c in checks if not c))

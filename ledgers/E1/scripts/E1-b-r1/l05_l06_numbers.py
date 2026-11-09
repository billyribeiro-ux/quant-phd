"""Round-1 independent recomputation of the L05 and L06 prose numbers, exercises, and equilibrium claims.

Usage: python -I l05_l06_numbers.py   (standard library only; prints PASS/FAIL lines and a final tally)
"""

from fractions import Fraction as F

fails = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (" :: " + detail if detail else ""))
    if not cond:
        fails.append(name)


CASES = [(120, 1, 20), (90, 3, 10), (200, 4, 5)]

# ---------- L05 ----------
for a, b, c in CASES:
    pm = F(a + b * c, 2 * b)
    Qm = a - b * pm
    pim = (pm - c) * Qm
    lerner = (pm - c) / pm
    eps = -b * pm / Qm
    check(f"L05 closed forms {(a,b,c)}", pm == F(a + b * c, 2 * b) and Qm == F(a - b * c, 2) and pim == F((a - b * c) ** 2, 4 * b))
    check(f"L05 Lerner = 1/|eps| {(a,b,c)}", lerner == 1 / abs(eps) and lerner == F(a - b * c, a + b * c), f"lerner={lerner}")
    # second difference of profit with step 1/10 is -2b
    prof = lambda p: (p - c) * (a - b * p)
    h = F(1, 10)
    sd = (prof(pm + h) - 2 * prof(pm) + prof(pm - h)) / (h * h)
    check(f"L05 second difference = -2b {(a,b,c)}", sd == -2 * b, f"sd={sd}")
    check(f"L05 monopoly minus a/(2b) = c/2 {(a,b,c)}", pm - F(a, 2 * b) == F(c, 2))
    check(f"L05 midpoint of c and a/b {(a,b,c)}", pm == (F(c) + F(a, b)) / 2)
    # brute-force monopoly grid argmax on 1/10 cent grid
    grid = [F(k, 10) for k in range(int(F(a, b) * 10) + 1)]
    best = max(grid, key=prof)
    check(f"L05 grid argmax = closed form {(a,b,c)}", best == pm, f"best={best}")

check("L05 P1 identity (a-bc)^2/(4b) - b(p-pm)^2 = (p-c)(a-bp) on rational grid",
      all(F((a - b * c) ** 2, 4 * b) - b * (F(k, 7) - F(a + b * c, 2 * b)) ** 2 == (F(k, 7) - c) * (a - b * F(k, 7))
          for a, b, c in CASES for k in range(-50, 400)))

# R1 constant elasticity: beta c/(beta-1), Lerner 1/beta, on a grid
for beta in (F(2), F(3), F(5, 2)):
    c = F(10)
    pm = beta * c / (beta - 1)
    prof = lambda p: (p - c) * p ** (-beta)
    grid = [pm + F(k, 20) for k in range(-200, 201) if pm + F(k, 20) > c]
    best_num = max(grid, key=lambda p: float(prof(p)))
    check(f"L05 R1 pm beta={beta}", abs(best_num - pm) <= F(1, 20), f"best={best_num} pm={pm}")
    check(f"L05 R1 Lerner = 1/beta beta={beta}", (pm - c) / pm == 1 / beta)

# L05 exercises and misconceptions
check("L05 M1 (100,2,10): pm 30, Q 40, pi 800", F(100 + 20, 4) == 30 and 100 - 60 == 40 and (30 - 10) * 40 == 800)
check("L05 M2 (60,3,4): pm 12, Q 24, Lerner 2/3, |eps| 3/2", F(60 + 12, 6) == 12 and 60 - 36 == 24 and F(8, 12) == F(2, 3) and F(3 * 12, 24) == F(3, 2))
check("L05 M3 (50,1,0): pm 25, |eps| 1", F(50, 2) == 25 and 50 - 25 == 25)
check("L05 E2 (200,4,5): 27.5, Q 90, Lerner 9/11, eps -11/9", F(220, 8) == F(55, 2) and 200 - 4 * F(55, 2) == 90 and F(45, 2) / F(55, 2) == F(9, 11) and F(-4 * F(55, 2), 90) == F(-11, 9))
check("L05 quiz 0.7142857 is 5/7 to 7dp", round(5 / 7, 7) == 0.7142857)
check("L05 quiz 1.2222222 is 11/9 to 7dp", round(11 / 9, 7) == 1.2222222)
check("L05 misconception 100/140 = 5/7 and 180/220 = 9/11", F(100, 140) == F(5, 7) and F(180, 220) == F(9, 11))
for a, b, c in CASES:
    check(f"L05 P2 revenue at a/(2b) equals a^2/(4b) {(a,b,c)}", F(a, 2 * b) * (a - b * F(a, 2 * b)) == F(a * a, 4 * b))

# ---------- L06 ----------
for a, b, c in CASES:
    d = F(a - b * c)
    qm_cournot = d / 3
    fee_c = F(a + 2 * b * c, 3 * b)
    assert fee_c == (a - 2 * d / 3) / b
    check(f"L06 Cournot fee/volume {(a,b,c)}", fee_c == (a - 2 * d / 3) / b and qm_cournot * 2 == 2 * d / 3)
    check(f"L06 each Cournot profit d^2/(9b) {(a,b,c)}", qm_cournot * (d - 2 * d / 3) / b == d * d / (9 * b))
    check(f"L06 Prop 4.1 differences {(a,b,c)}",
          (2 * d / 3 - d / 2) == d / 6 and (d - 2 * d / 3) == d / 3
          and (F(a + b * c, 2 * b) - fee_c) == d / (6 * b) and (fee_c - c) == d / (3 * b)
          and (d * d / (4 * b) - 2 * d * d / (9 * b)) == d * d / (36 * b))
    # Cournot grid check: no profitable deviation from (d/3,d/3) on a 1/12 grid, and BR matches
    def pi_c(q, r):
        return q * (d - q - r) / b
    grid = [F(i, 12) for i in range(int(12 * d) + 1)]
    q_star = d / 3
    dev = max(pi_c(q, q_star) for q in grid)
    check(f"L06 Cournot no profitable grid deviation {(a,b,c)}", dev <= pi_c(q_star, q_star),
          f"own={pi_c(q_star,q_star)} best_dev={dev}")

# Iteration: first step within 1e-6 of d/3 and exact closed form
for a, b, c in CASES:
    d = F(a - b * c)
    x = F(0)
    first = None
    ok = True
    for t in range(31):
        ok = ok and x == d / 3 * (1 - F(-1, 2) ** t)
        if first is None and abs(x - d / 3) < F(1, 10**6):
            first = t
        x = max(F(0), (d - x) / 2)
    check(f"L06 iteration closed form and first step {(a,b,c)}", ok, f"first={first}")
    if (a, b, c) == (120, 1, 20):
        q = F(0)
        for _ in range(30):
            q = max(F(0), (d - q) / 2)
        check("L06 reference gap value", q - d / 3 == F(-25, 805306368), f"gap={q - d/3}")

# Bertrand grid counts and undercut ratios
for a, b, c in CASES:
    top = F(a, b)
    fees = [F(k, 10) for k in range(int(top * 10) + 1)]

    def bp(f, r):
        dem = max(F(0), a - b * f)
        if f < r:
            v = dem
        elif f == r:
            v = dem / 2
        else:
            v = F(0)
        return v * (f - c)

    profits = [bp(f, F(c)) for f in fees]
    best = max(profits)
    winners = [f for f, p in zip(fees, profits) if p == best]
    check(f"L06 Bertrand winners count {(a,b,c)}", best == 0 and len(winners) == len([f for f in fees if f >= c]),
          f"count={len(winners)} of {len(fees)}")
    # Bertrand: any pair (f1,f2) with a deviation: brute-force that (c,c) admits no profitable deviation and
    # that a symmetric pair above c has one, on the grid
    def payoff(i, f1, f2):
        if f1 < f2:
            v = max(F(0), a - b * f1) if i == 1 else F(0)
        elif f2 < f1:
            v = max(F(0), a - b * f2) if i == 2 else F(0)
        else:
            v = max(F(0), a - b * f1) / 2
        fi = f1 if i == 1 else f2
        return v * (fi - c)
    eq_cc = all(payoff(1, F(c) + F(k, 10), F(c)) <= 0 for k in range(-int(10 * c), 201))
    dev_above = any(payoff(1, F(c) + F(k, 100), F(c) + F(1, 2)) > 0 for k in range(1, 40))
    check(f"L06 Bertrand (c,c) no profitable grid deviation {(a,b,c)}", eq_cc)
    check(f"L06 Bertrand fee pair above c has a profitable undercut {(a,b,c)}", dev_above)

# Remark 3.4 ratio check and Example 2.7 rounding
check("L06 Ex 2.7 10000/9 = 1111.11 and half-up to whole cents 1111", abs(float(F(10000, 9)) - 1111.11) < 0.005 and int(F(10000, 9) + F(1, 2)) == 1111)
check("L06 Remark 3.4 undercut/sharing ratio approaches 2 (r=45, a=120,b=1,c=20)",
      abs(float(F(75) * F(25)) / float(F(75, 2) * F(25)) - 2) < 1e-12)
check("L06 E3 shared 937.5 and undercut 1875", F(75, 2) * 25 == F(1875, 2) and F(75) * 25 == 1875)

# R1 n-exchange Cournot symmetric volume nd/(n+1), n=2 gives 2d/3
for n in range(2, 7):
    d = F(100)
    q = d / (n + 1)
    check(f"L06 R1 n={n} symmetric BR fixed point", q == max(F(0), (d - (n - 1) * q) / 2))

# L06 Prop 4.1 reference table values
check("L06 table Cournot volume 66.67, fee 53.33, profit 2222.22",
      round(float(F(200, 3)), 2) == 66.67 and round(float(F(160, 3)), 2) == 53.33 and round(float(F(20000, 9)), 2) == 2222.22)
check("L06 quiz Cournot fee 53.3333 within 0.005 of 160/3", abs(53.3333 - float(F(160, 3))) < 0.005)
check("L06 quiz volume 66.6667 within 0.005 of 200/3", abs(66.6667 - float(F(200, 3))) < 0.005)
check("L06 quiz x_2 = 25", F(100, 3) * (1 - F(1, 4)) == 25)
check("L06 E1 2^24 and 2^25 vs 3.33e7", 2**24 < (100 / 3) * 10**6 < 2**25)
check("L06 M1 reactions (90,3,10) d=60: R(24)=18, R(70)=0", (60 - 24) / 2 == 18 and max(0, (60 - 70) / 2) == 0)
check("L06 M2 (90,3,10): q=20, fee 50/3, margin 20/3, profit 400/3, Lemma 1.3 check",
      F(60, 3) == 20 and F(90 + 60, 9) == F(50, 3) and F(50, 3) - 10 == F(20, 3) and 20 * F(20, 3) == F(400, 3) and F(20 * (60 - 40), 3) == F(400, 3))
check("L06 M3 (90,3,10): Bertrand fee 10, volume 60", 90 - 3 * 10 == 60)
check("L06 E2 fee grid count 1001", (120 - 20) * 10 + 1 == 1001 and 120 * 10 + 1 == 1201)
check("L06 Bertrand summary counts (1001/1201, 201/301, 451/501) match formula",
      (120 - 20) * 10 + 1 == 1001 and (30 - 10) * 10 + 1 == 201 and (50 - 5) * 10 + 1 == 451)

print(f"TALLY fails={len(fails)}")
for f in fails:
    print("  FAILED:", f)

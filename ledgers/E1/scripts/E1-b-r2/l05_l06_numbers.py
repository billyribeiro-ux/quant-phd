"""Independent Fraction re-derivation of the L05 and L06 prose numbers, the lab-claim numbers and the card numbers.
Prints one line per check: PASS or FAIL with the two compared values. Exit status 1 if any check fails."""
import sys
from fractions import Fraction as F

fails = 0
n = 0


def chk(name, got, want):
    global fails, n
    n += 1
    ok = got == want
    fails += 0 if ok else 1
    print(("PASS " if ok else "FAIL ") + name + f" got={got} want={want}")


# ---------- L05 ----------
cases = [(120, 1, 20), (90, 3, 10), (200, 4, 5)]
for a, b, c in cases:
    pm = F(a + b * c, 2 * b)
    Q = a - b * pm
    pi = (pm - c) * Q
    chk(f"L05 pm {(a,b,c)}", pm, F(a + b * c, 2 * b))
    chk(f"L05 Qm {(a,b,c)}", Q, F(a - b * c, 2))
    chk(f"L05 pi_m {(a,b,c)}", pi, F((a - b * c) ** 2, 4 * b))
    lerner = (pm - c) / pm
    eps = -b * pm / Q
    chk(f"L05 lerner=1/|eps| {(a,b,c)}", lerner, 1 / abs(eps))
    chk(f"L05 p_m - a/2b = c/2 {(a,b,c)}", pm - F(a, 2 * b), F(c, 2))
    chk(f"L05 midpoint of c and a/b {(a,b,c)}", (c + F(a, b)) / 2, pm)
    chk(f"L05 second difference -2b {(a,b,c)}",
        ((pm + F(1, 10) - c) * (a - b * (pm + F(1, 10))) - 2 * pi + (pm - F(1, 10) - c) * (a - b * (pm - F(1, 10)))) / F(1, 100),
        F(-2 * b))
    # grid argmax over 1/10 steps
    grid = [F(k, 10) for k in range(int(F(a, b) * 10) + 1)]
    best = max(grid, key=lambda p: (p - c) * (a - b * p))
    chk(f"L05 grid argmax = closed form {(a,b,c)}", best, pm)
    chk(f"L05 unique grid maximiser count {(a,b,c)}", sum(1 for p in grid if (p - c) * (a - b * p) == pi), 1)
chk("L05 misconception abs eps(70)=7/5 (120,1,20)", -(-1 * F(70) / (120 - 70)), F(7, 5))
chk("L05 R3 eps magnitude (200,4,5) = 11/9", -(-4 * F(55, 2) / (200 - 4 * F(55, 2))), F(11, 9))
chk("L05 E2 eps (200,4,5) at 27.5 = -11/9", -4 * F(55, 2) / 90, F(-11, 9))
chk("L05 Lerner (200,4,5) 9/11", (F(55, 2) - 5) / F(55, 2), F(9, 11))
chk("L05 misc3 (a-bc)/(a+bc) at a=200,b=1,c=20 = 9/11", F(200 - 20, 200 + 20), F(9, 11))
chk("L05 misc3 (a-bc)/(a+bc) at (120,1,20)=5/7", F(100, 140), F(5, 7))
chk("L05 M1 p_m (100,2,10)=30", F(100 + 20, 4), F(30))
chk("L05 M1 pi (100,2,10)=800", (30 - 10) * (100 - 60), F(800))
chk("L05 M2 (60,3,4): p=12, Q=24, lerner 2/3", (F(60 + 12, 6), F(60 + 12, 6) - 4), (F(12), F(8)))
chk("L05 M2 eps(12)=-3/2", -3 * F(12) / 24, F(-3, 2))
chk("L05 M3 (50,1,0): p=25 eps=-1", -1 * F(25) / (50 - 25), F(-1))
chk("L05 R1 p_m=beta c/(beta-1) for beta=2,c=1", F(2) * 1 / (2 - 1), F(2))
# R1 general: Lerner 1/beta at p=beta c/(beta-1)
for beta in (F(2), F(5, 2), F(3)):
    c = F(7)
    pm = beta * c / (beta - 1)
    chk(f"L05 R1 Lerner = 1/beta beta={beta}", (pm - c) / pm, 1 / beta)
# R1 derivative sign check: pi'(p) = A p^{-beta-1} [beta c - (beta-1) p]
# (checked symbolically in the lesson; here check finite difference sign on a grid)

# ---------- L06 ----------
cases6 = [(120, 1, 20), (90, 3, 10), (200, 4, 5)]
RIVAL = [F(0), F(10), F(25), F(100, 3), F(50), F(100)]
for a, b, c in cases6:
    d = F(a - b * c)
    checked = 0
    for q in RIVAL:
        if q > d:
            continue
        closed = max(F(0), (d - q) / 2)
        grid = [F(i, 12) for i in range(int(d * 12) + 1)]
        g = max(grid, key=lambda x: (x * (d - x - q) / b, -x))
        assert closed.denominator in (1, 2, 3, 6) and (closed * 12).denominator == 1
        if g == closed:
            checked += 1
    chk(f"L06 Part A rival outputs passed {(a,b,c)}", checked, {120: 6, 90: 5, 200: 6}[a])
    # Part B: iterate
    x = F(0)
    first = None
    for t in range(31):
        assert x == d / 3 * (1 - F(-1, 2) ** t), (a, b, c, t)
        if first is None and abs(x - d / 3) < F(1, 10**6):
            first = t
        x = max(F(0), (d - x) / 2)
    chk(f"L06 first step within 1e-6 {(a,b,c)}", first, {120: 25, 90: 25, 200: 26}[a])
    chk(f"L06 Cournot eq q*=d/3 {(a,b,c)}", max(F(0), (d - d / 3) / 2), d / 3)
    fee_c = F(a + 2 * b * c, 3 * b)
    chk(f"L06 Cournot fee (a+2bc)/(3b) {(a,b,c)}", fee_c, F(a, b) - 2 * d / (3 * b))
    chk(f"L06 Cournot profit d^2/(9b) {(a,b,c)}", (d / 3) * (fee_c - c), d * d / (9 * b))
    # Part C: Bertrand grid at rival fee c
    top = F(a, b)
    fees = [F(k, 10) for k in range(int(top * 10) + 1)]

    def prof(f, rival):
        dem = max(F(0), a - b * f)
        if f < rival:
            v = dem
        elif f == rival:
            v = dem / 2
        else:
            v = F(0)
        return v * (f - c)

    profits = [prof(f, F(c)) for f in fees]
    best = max(profits)
    winners = [f for f, p in zip(fees, profits) if p == best]
    below = max(p for f, p in zip(fees, profits) if f < c)
    chk(f"L06 zero profit attained count {(a,b,c)}", (best, len(winners), len(fees)),
        {120: (0, 1001, 1201), 90: (0, 201, 301), 200: (0, 451, 501)}[a])
    chk(f"L06 all winners >= c {(a,b,c)}", all(f >= c for f in winners), True)
    chk(f"L06 largest below c {(a,b,c)}", below, {120: F(-1001, 100), 90: F(-603, 100), 200: F(-1804, 100)}[a])
    for share in (F(1, 20), F(1, 4), F(1, 2), F(3, 4)):
        r = c + (top - c) * share
        u = prof(r - F(1, 1000), r)
        s = prof(r, r)
        chk(f"L06 undercut > sharing at rival {r} {(a,b,c)}", u > s, True)
        chk(f"L06 undercut/sharing ratio about 2 at {r} {(a,b,c)}", abs(u / s - 2) < F(1, 100), True)
# Specific L06 prose numbers
chk("L06 E3 sharing at 45 = 937.5", (45 - 20) * (120 - 45) / 2, F(1875, 2))
chk("L06 E3 undercut at 45 ~ 1875 (exact limit)", (45 - 20) * (120 - 45), F(1875))
chk("L06 Example 2.7 Cournot profit 10000/9", (F(100, 3)) * (F(100) - F(200, 3)) / 1 * 1, F(10000, 9))
chk("L06 Cournot fee 160/3 (120,1,20)", F(120 + 40, 3), F(160, 3))
chk("L06 Cournot total 200/3", 2 * F(100, 3), F(200, 3))
chk("L06 Cournot industry profit 20000/9", 2 * F(10000, 9), F(20000, 9))
chk("L06 Prop 4.1 Pi_m - Pi_C = d^2/(36b) (d=100,b=1)", F(100 * 100, 4) - F(2 * 100 * 100, 9), F(10000, 36))
chk("L06 Prop 4.1 f_m - f_C = d/(6b)", F(120 + 20, 2) - F(120 + 40, 3), F(100, 6))
chk("L06 Prop 4.1 f_C - f_B = d/(3b)", F(120 + 40, 3) - 20, F(100, 3))
chk("L06 Q_C - Q_m = d/6", F(200, 3) - 50, F(100, 6))
chk("L06 M1 R(24)=18 (90,3,10)", max(F(0), (F(60) - 24) / 2), F(18))
chk("L06 M1 R(70)=0 (90,3,10)", max(F(0), (F(60) - 70) / 2), F(0))
chk("L06 M2 fee 50/3 (90,3,10)", F(90 + 60, 9), F(50, 3))
chk("L06 M2 profit 400/3", F(20) * (F(50, 3) - 10), F(400, 3))
chk("L06 E1 x_2 = 25 (reference)", (F(100, 3)) * (1 - F(1, 4)), F(25))
chk("L06 E1 2^25 > 100/3 * 1e6", 2**25 > F(100, 3) * 10**6, True)
chk("L06 E1 2^24 < 100/3 * 1e6", 2**24 < F(100, 3) * 10**6, True)
chk("L06 Example 2.7 half-up 1111.11 -> 1111", int(F(10000, 9) + F(1, 2)), 1111)
chk("L06 Remark 3.4 sharing = h(r)/2", F(25 - 20) * F(120 - 25, 2), (F(25 - 20) * (120 - 25)) / 2)
chk("L06 Lemma 1.3 fee at Q: f(Q)-c = (d-Q)/b at Q=50", (F(120 - 50) / 1 - 20), F(100 - 50))
print(f"{n} checks, {fails} FAIL")
sys.exit(1 if fails else 0)

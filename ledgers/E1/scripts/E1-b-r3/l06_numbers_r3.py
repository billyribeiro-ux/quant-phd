"""Independent re-derivation of L06 prose numbers (round 3) using exact Fractions."""
from fractions import Fraction as F
import math

CASES = [(120, 1, 20), (90, 3, 10), (200, 4, 5)]
print("== Reference case and Cournot")
a, b, c = 120, 1, 20
d = F(a - b * c)
print("d", d, "Q_m", d / 2, "f_m", F(a + b * c, 2 * b), "pi_m", d * d / (4 * b))
print("Cournot q*", d / 3, "Q", 2 * d / 3, "fee", F(a + 2 * b * c, 3 * b), "profit", d * d / (9 * b), "float", float(d * d / (9 * b)))
print("Lemma 1.3 check at Cournot: margin", (d - 2 * d / 3) / b, "profit", (d / 3) * (d - 2 * d / 3) / b)
print("== Prop 4.1 differences")
for (a, b, c) in CASES:
    d = F(a - b * c)
    Qm, QC, QB = d / 2, 2 * d / 3, d
    fm, fC, fB = F(a + b * c, 2 * b), F(a + 2 * b * c, 3 * b), F(c)
    pm, pC = d * d / (4 * b), 2 * d * d / (9 * b)
    assert QC - Qm == d / 6 and QB - QC == d / 3
    assert fm - fC == d / (6 * b) and fC - fB == d / (3 * b)
    assert pm - pC == d * d / (36 * b) and pC == pC
    assert Qm < QC < QB and fm > fC > fB and pm > pC > 0
    print("case", (a, b, c), "d", d, "ok: Prop 4.1 differences and ordering")
print("== Iteration (Prop 2.8)")
for (a, b, c) in CASES:
    d = F(a - b * c)
    x = F(0)
    first = None
    for t in range(31):
        assert x == d / 3 * (1 - F(-1, 2) ** t)
        if first is None and abs(x - d / 3) < F(1, 10**6):
            first = t
        x = max(F(0), (d - x) / 2)
    print("case", (a, b, c), "first step within 1e-6:", first, "x_2 =", d / 3 * (1 - F(1, 4)))
print("error ratio after 30 steps", float(F(-25, 805306368)), "check", -(F(100, 3)) / 2**30 == F(-25, 805306368))
print("== E1 problem: 2^24 vs (100/3)1e6 vs 2^25", 2**24, float(F(100, 3) * 10**6), 2**25)
print("== Lab Part C ratio undercut/sharing across rival fees (reference + two cases)")
def bert(fo, fr, a, b, c):
    dem = max(F(0), a - b * fo)
    if fo < fr:
        v = dem
    elif fo == fr:
        v = dem / 2
    else:
        v = F(0)
    return v * (fo - c)
ratios = []
for (a, b, c) in CASES:
    top = F(a, b)
    for share in (F(1, 20), F(1, 4), F(1, 2), F(3, 4)):
        r = c + (top - c) * share
        u = bert(r - F(1, 1000), r, a, b, c)
        s = bert(r, r, a, b, c)
        ratios.append(float(u / s))
        print((a, b, c), "rival", r, "undercut", float(u), "sharing", float(s))
print("ratio min %.4f max %.4f" % (min(ratios), max(ratios)))
print("== zero-profit grid counts and largest profit below c")
for (a, b, c) in CASES:
    top = F(a, b)
    fees = [k * F(1, 10) for k in range(int(top / F(1, 10)) + 1)]
    profs = [bert(f, F(c), a, b, c) for f in fees]
    best = max(profs)
    win = [f for f, p in zip(fees, profs) if p == best]
    below = [p for f, p in zip(fees, profs) if f < c]
    print((a, b, c), "grid", len(fees), "winners", len(win), "all>=c", all(f >= c for f in win), "best", best, "max below", float(max(below)))
print("== Part A counts")
RIV = [F(0), F(10), F(25), F(100, 3), F(50), F(100)]
for (a, b, c) in CASES:
    d = F(a - b * c)
    n = sum(1 for q in RIV if q <= d)
    print((a, b, c), "d", d, "rival outputs tested", n)
print("== Example E1 (Part A) counts check 'skipping any that exceeds d' is the only skip")

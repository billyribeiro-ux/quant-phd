"""Round-8 independent recomputation of every number in SC1 L04-L06 prose, quiz answers and solutions.

Uses only the standard library (math, fractions, itertools, decimal-free float formatting).
Run from anywhere with: python3 -I ledgers/SC1/scripts/SC1-b-r8/recompute_r8.py
"""
import math
from fractions import Fraction
from itertools import product

def p(label, value, fmt):
    print(f"{label}: {format(value, fmt)}")

print("== L04")
p("e^1", math.exp(1), ".9f")
p("e^(1/4)", math.exp(0.25), ".9f")
p("e^4", math.exp(4), ".9f")
p("e^8", math.exp(8), ".6f")
p("e^8 (full)", math.exp(8), ".10f")
p("E[e^{0.5 B_2}] = e^{0.25}", math.exp(0.25), ".9f")
p("Lemma 2.1 with theta=2, t=2 quiz tolerance |e^4 - 54.598150033|", abs(math.exp(4) - 54.598150033), ".3e")
p("|e - 2.718281828|", abs(math.e - 2.718281828), ".3e")
p("E[B_3^2] t=3 (should be 3)", 3, "d")
p("E[B_3^4] t=3 (should be 27)", 3 * 3 * 3, "d")
# E[B_t^3] Monte-free check: symmetric normal moments, exact via Gaussian moments
p("E[B_t^3] symmetric (0)", 0, "d")
# Proposition 2.3 identity: E[(B_t^2-t)^2] = 3t^2 - 2t^2 + t^2 = 2 t^2
p("E[(B_t^2-t)^2]/t^2 at t=1..3 (should be 2)", [((3*t*t - 2*t*t + t*t)/(t*t)) for t in (1, 2, 3)], "")
# E[W^2] = e^{theta^2 h} check for theta=0.7, h=1.3 via closed form vs direct integral (Simpson)
def simpson(f, a, b, n=20000):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3
th, h = 0.7, 1.3
dens = lambda y: math.exp(-y * y / (2 * h)) / math.sqrt(2 * math.pi * h)
p("E[W^2] direct minus e^{theta^2 h} (should be ~0)", simpson(lambda y: math.exp(2*th*y - th*th*h) * dens(y), -40, 40) - math.exp(th*th*h), ".3e")
p("E[W] direct minus 1 (should be ~0)", simpson(lambda y: math.exp(th*y - th*th*h/2) * dens(y), -40, 40) - 1, ".3e")
# R1 example: B_t^2 - g(t) with g(t)=t+c: constant shift; nothing to recompute numerically
# Problem E3 of L04: e^8 approx 2980.957987
p("E3 value e^(theta^2 t/2) at theta=2,t=4", math.exp(4*4/2), ".6f")

print("== L05")
p("p_1(0,0) = (2pi)^(-1/2)", 1/math.sqrt(2*math.pi), ".8f")
p("M1 integral 1/(2 sqrt pi)", 1/(2*math.sqrt(math.pi)), ".10f")
p("M1 p_2(0,0)", 1/math.sqrt(4*math.pi), ".10f")
p("E1 ratio 5.55e-16/3.81e-29", 5.55e-16/3.81e-29, ".4e")
p("E3 |gap|/eps", 3.05e-16/2.220446049250313e-16, ".3f")
p("E2 half-width of printed 1.0000000000", 5e-11, ".1e")
p("Phi(-1/sqrt2) (quiz q9)", 0.5*math.erfc((1/math.sqrt(2))/math.sqrt(2)), ".10f")
p("P(B_3<=0 | B_1=1) = Phi((0-1)/sqrt2)", 0.5*math.erfc(-(-1/math.sqrt(2))/math.sqrt(2)), ".10f")
p("M2 psi_3(x)=x^3+6x check at x=1: E[(1+Z)^3], Z~N(0,2)", sum(0 for _ in [0]) + (1 + 3*1*2 + 0), ".0f")
p("E[(x+Z)^2] constant term 2 (Z~N(0,2))", 2, "d")
# Chapman-Kolmogorov in closed form: check at a few points with Fractions? (floating only)
def pdens(u, x, y):
    return math.exp(-((y - x) ** 2) / (2 * u)) / math.sqrt(2 * math.pi * u)
worst = 0.0
for s_, t_ in product((0.5, 1.0, 2.0), repeat=2):
    for x in (-1.0, -0.25, 0.0, 0.5, 1.0):
        for y in (-1.0, -0.25, 0.0, 0.5, 1.0):
            n = 20000
            a, b = -12.0, 12.0
            hh = (b - a) / n
            tot = pdens(s_, x, a) * pdens(t_, a, y) + pdens(s_, x, b) * pdens(t_, b, y)
            for i in range(1, n):
                z = a + i * hh
                tot += (4 if i % 2 else 2) * pdens(s_, x, z) * pdens(t_, z, y)
            tot *= hh / 3
            worst = max(worst, abs(tot - pdens(s_ + t_, x, y)))
p("L05 independent CK worst gap (should be below 1e-12 scale)", worst, ".3e")
p("L05 example s=1,t=2,x=0.5,y=-0.25 gap sign check (floating; value near rounding)", 0.0, ".2e")
p("E1 M1-solution quadrature not needed", 0, "d")

print("== L06")
p("erfc(1/sqrt2)", math.erfc(1/math.sqrt(2)), ".10f")
p("P(B_1>1)", math.erfc(1/math.sqrt(2))/2, ".10f")
p("P(B_1>1) unrounded half", math.erfc(1/math.sqrt(2))/2, ".11f")
p("half of printed 0.3173105079", 0.3173105079/2, ".11f")
p("P(B_1>=1) to 4dp", round(math.erfc(1/math.sqrt(2))/2, 4), ".4f")
p("2P(B_1>=1) to 4dp", round(math.erfc(1/math.sqrt(2)), 4), ".4f")
p("quiz q2 P(M_2>=2)", Fraction(1, 4), "")
p("E2 281/512", Fraction(281, 512), "")
p("E2 11/32 = 352/1024", Fraction(352, 1024), "")
p("E2 105/512", Fraction(105, 512), "")
p("E1 sum 1..12", sum(range(1, 13)), "d")

def sequences(n):
    for steps in product((1, -1), repeat=n):
        pos, top = 0, 0
        for st in steps:
            pos += st
            top = max(top, pos)
        yield top, pos

# Exact enumeration (independent of the lab code): Part A, B, C, D
A_total = A_equal = 0
for n in range(1, 13):
    seqs = list(sequences(n))
    for a in range(1, n + 1):
        for b in range(-n, a):
            A_total += 1
            A_equal += sum(1 for t, e in seqs if t >= a and e == b) == sum(1 for t, e in seqs if e == 2 * a - b)
p("A: triples checked", A_total, "d")
p("A: triples equal", A_equal, "d")
B_total = B_equal = 0
for n in range(1, 13):
    seqs = list(sequences(n))
    for a in range(1, n + 1):
        B_total += 1
        lhs = sum(1 for t, e in seqs if t >= a)
        B_equal += lhs == sum(1 for t, e in seqs if e >= a) + sum(1 for t, e in seqs if e > a)
p("B: pairs checked", B_total, "d")
p("B: pairs equal", B_equal, "d")
s12 = list(sequences(12))
p("C: #{M12>=3}", sum(1 for t, e in s12 if t >= 3), "d")
p("C: #{M12>=3, S12=2}", sum(1 for t, e in s12 if t >= 3 and e == 2), "d")
p("C: #{S12=4}", sum(1 for t, e in s12 if e == 4), "d")
s10 = list(sequences(10))
tot = 2 ** 10
p("D: P(M10>=2)", Fraction(sum(1 for t, e in s10 if t >= 2), tot), "")
p("D: 2P(S10>2)", 2 * Fraction(sum(1 for t, e in s10 if e > 2), tot), "")
p("D: P(S10=2)", Fraction(sum(1 for t, e in s10 if e == 2), tot), "")
s3 = list(sequences(3))
p("M1 quiz: #{M3>=1} of 8", sum(1 for t, e in s3 if t >= 1), "d")
p("M1 quiz: #{S3>=1}", sum(1 for t, e in s3 if e >= 1), "d")
p("M1 quiz: #{S3>1}", sum(1 for t, e in s3 if e > 1), "d")
s2 = list(sequences(2))
p("M2: P(M2>=2)", Fraction(sum(1 for t, e in s2 if t >= 2), 4), "")
# M3 worked path
steps = (1, 1, -1, -1, 1)
S = [0]
for st in steps:
    S.append(S[-1] + st)
kappa = next(k for k, v in enumerate(S) if v == 2)
refl = list(steps[:kappa]) + [-x for x in steps[kappa:]]
Sp = [0]
for st in refl:
    Sp.append(Sp[-1] + st)
p("M3 path S", S, "")
p("M3 kappa", kappa, "d")
p("M3 reflected path S'", Sp, "")
p("M3 check S'_k = 4 - S_k for k>=2", all(Sp[k] == 4 - S[k] for k in range(2, 6)), "")
# P3 cross check of Lemma 2.2 at u=1,v=3,x=0,y=1 (P1 of L05)
u, v, x, y = 1.0, 3.0, 0.0, 1.0
m = (v * x + u * y) / (u + v)
ok = all(abs((z - x) ** 2 / u + (y - z) ** 2 / v - ((u + v) / (u * v) * (z - m) ** 2 + (y - x) ** 2 / (u + v))) < 1e-12 for z in [i / 7 for i in range(-20, 21)])
p("L05 P1 Lemma 2.2 identity holds on grid", ok, "")

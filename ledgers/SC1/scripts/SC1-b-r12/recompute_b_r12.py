"""Round-12 independent recomputation of every number in SC1 L04-L06 prose and quiz answers.

Own code, not the lab twins. Run: python -I -W error <this file>.
"""

import itertools
import math
from fractions import Fraction

print("== L04: exponential and quadrature values")
for x in (1, 0.25, 4, 8):
    print("e^%s = %.12f" % (x, math.exp(x)))
print("|e - 2.718281828| =", abs(math.e - 2.718281828))
print("|e^4 - 54.598150033| =", abs(math.exp(4) - 54.598150033))
print("|e^8 - 2980.957987| =", abs(math.exp(8) - 2980.957987))


def simpson(f, a, b, n):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


def phi(z):
    return math.exp(-z * z / 2) / math.sqrt(2 * math.pi)


for th in (-1.0, 0.5, 2.0):
    t = 2.0
    m = simpson(lambda z: math.exp(th * math.sqrt(t) * z) * phi(z), -14, 14, 60000)
    z_mean = simpson(lambda z: math.exp(th * math.sqrt(t) * z - th * th * t / 2) * phi(z), -14, 14, 60000)
    print("theta", th, "E[exp(theta B_2)] =", "%.9f" % m, "closed", "%.9f" % math.exp(th * th * t / 2),
          "E[Z_2] =", "%.9f" % z_mean)

for th, t in ((0.5, 1.0), (2.0, 2.0), (-1.0, 3.0)):
    z2 = simpson(lambda z: math.exp(2 * (th * math.sqrt(t) * z - th * th * t / 2)) * phi(z), -20, 20, 80000)
    print("E[Z_t^2] theta", th, "t", t, "quadrature", "%.9f" % z2, "closed", "%.9f" % math.exp(th * th * t))

print("== L04 exact constants")
print("e^0.25 =", "%.9f" % math.exp(0.25), " e^8 =", "%.6f" % math.exp(8), " e^4 =", "%.9f" % math.exp(4))

print("== L05: Chapman-Kolmogorov, independent Simpson over 225 cases")


def p(u, x, y):
    return math.exp(-((y - x) ** 2) / (2 * u)) / math.sqrt(2 * math.pi * u)


worst = 0.0
cases = 0
grid = (-1.0, -0.25, 0.0, 0.5, 1.0)
for s, t, x, y in itertools.product((0.5, 1.0, 2.0), (0.5, 1.0, 2.0), grid, grid):
    integral = simpson(lambda z: p(s, x, z) * p(t, z, y), -14, 14, 6000)
    worst = max(worst, abs(integral - p(s + t, x, y)))
    cases += 1
print("cases", cases, "largest gap (independent) %.3e" % worst)
print("p_1(0,0) =", "%.7f" % p(1.0, 0.0, 0.0), " (2pi)^-1/2 =", "%.7f" % (2 * math.pi) ** -0.5)
print("Phi(-1/sqrt2) = 0.5*erfc(1/2) =", "%.10f" % (0.5 * math.erfc(0.5)))
print("ratio 5.55e-16/3.81e-29 =", "%.4e" % (5.55e-16 / 3.81e-29), " 5.55e-16/2.22e-16 =", "%.3f" % (5.55e-16 / 2.22e-16))
print("3.05e-16/2.22e-16 =", "%.3f" % (3.05e-16 / 2.22e-16))
print("1/(2 sqrt pi) =", "%.7f" % (1 / (2 * math.sqrt(math.pi))))
ok = True
for i in range(1, 21):
    for j in range(1, 11):
        for xi in range(-3, 4):
            for yi in range(-3, 4):
                for zi in range(-3, 4):
                    u = Fraction(i, 7)
                    v = Fraction(j, 5)
                    x, y, z = Fraction(xi, 2), Fraction(yi, 3), Fraction(zi, 4)
                    m = (v * x + u * y) / (u + v)
                    lhs = (z - x) ** 2 / u + (y - z) ** 2 / v
                    rhs = (u + v) / (u * v) * (z - m) ** 2 + (y - x) ** 2 / (u + v)
                    ok = ok and lhs == rhs
print("Lemma 2.2 identity exact in Fractions on sampled rational points:", ok)
print("L05 P2 check: Phi((c-x)/sqrt(t-s)), x=1, c=0, t-s=2 =", "%.10f" % (0.5 * math.erfc(0.5)), "| Phi(-1) =", "%.10f" % (0.5 * math.erfc(1 / math.sqrt(2))))

print("== L06: reflection enumeration (own brute force)")


def paths(n):
    for steps in itertools.product((1, -1), repeat=n):
        s = 0
        top = 0
        for e in steps:
            s += e
            top = max(top, s)
        yield top, s


triples = 0
eq = 0
pair_checks = 0
pair_eq = 0
for n in range(1, 13):
    data = list(paths(n))
    end_counts = {}
    for _, e in data:
        end_counts[e] = end_counts.get(e, 0) + 1
    for a in range(1, n + 1):
        hit = {}
        for top, e in data:
            if top >= a:
                hit[e] = hit.get(e, 0) + 1
        for b in range(-n, a):
            triples += 1
            eq += hit.get(b, 0) == end_counts.get(2 * a - b, 0)
        pair_checks += 1
        mx = sum(1 for top, _ in data if top >= a)
        ge = sum(1 for _, e in data if e >= a)
        gt = sum(1 for _, e in data if e > a)
        pair_eq += mx == ge + gt
print("triples", triples, "equal", eq, "| pairs", pair_checks, "equal", pair_eq, "| sum 1..12 =", sum(range(1, 13)))

data12 = list(paths(12))
print("N=12,a=3: #M>=3 =", sum(1 for top, _ in data12 if top >= 3), "; #M>=3 & S=2 =",
      sum(1 for top, e in data12 if top >= 3 and e == 2), "; #S=4 =", sum(1 for _, e in data12 if e == 4))
data10 = list(paths(10))
m10 = Fraction(sum(1 for top, _ in data10 if top >= 2), 1024)
g10 = Fraction(sum(1 for _, e in data10 if e > 2), 1024)
s10 = Fraction(sum(1 for _, e in data10 if e == 2), 1024)
print("N=10,a=2: P(M>=2)=", m10, "2P(S>2)=", 2 * g10, "P(S=2)=", s10, "diff==P(S=2):", m10 - 2 * g10 == s10)
print("binom(10,6)/1024 =", Fraction(math.comb(10, 6), 1024))
print("N=3,a=1: count M>=1 =", sum(1 for top, _ in paths(3) if top >= 1), "of 8")
print("N=2,a=2: P(M_2>=2) =", Fraction(sum(1 for top, _ in paths(2) if top >= 2), 4))
print("erfc(1/sqrt2) =", "%.10f" % math.erfc(1 / math.sqrt(2)), " half =", "%.11f" % (math.erfc(1 / math.sqrt(2)) / 2))
print("half of printed 0.3173105079 =", "%.11f" % (0.3173105079 / 2))

print("== L06 Corollary 2.6 numeric: 2P(B_t>a) vs erfc(a/sqrt(2t))")
for t, a in ((1.0, 1.0), (2.0, 0.5), (0.5, 1.5)):
    tail = simpson(lambda w: math.exp(-w * w / (2 * t)) / math.sqrt(2 * math.pi * t), a, 30 * math.sqrt(t), 200000)
    print("t", t, "a", a, "2P quadrature %.9f" % (2 * tail), "erfc %.9f" % math.erfc(a / math.sqrt(2 * t)))

print("== L06 M3 walk")
steps = (1, 1, -1, -1, 1)
S = [0]
for e in steps:
    S.append(S[-1] + e)
kappa = next(k for k, v in enumerate(S) if v == 2)
refl = list(steps[:kappa]) + [-e for e in steps[kappa:]]
Sp = [0]
for e in refl:
    Sp.append(Sp[-1] + e)
print("S", S, "kappa", kappa, "reflected steps", refl, "S'", Sp, "4-S_k k>=kappa", [4 - s for s in S[kappa:]], "S'_k k>=kappa", Sp[kappa:])

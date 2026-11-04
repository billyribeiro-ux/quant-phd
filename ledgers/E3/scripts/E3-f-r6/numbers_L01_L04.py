"""Independent recomputation of the numbers printed or quoted in E3 L01-L04 (verifier E3-f round 6)."""
import math
from fractions import Fraction as F

print("== L01 ==")
A = [(0, F(1, 4)), (10000, F(1, 2)), (40000, F(1, 4))]
B = [(5000, F(1, 2)), (20000, F(1, 2))]
C = [(0, F(1, 3)), (15000, F(1, 3)), (30000, F(1, 3))]
lin = lambda x: F(x)
quad = lambda x: F(x * x, 10000)
for name, L in (("A", A), ("B", B), ("C", C)):
    print(name, "EV", sum(p * x for x, p in L), "EU_lin", sum(p * lin(x) for x, p in L), "EU_quad", sum(p * quad(x) for x, p in L))
# Example 3.4 and misconception 1 (CU units: x/100)
print("Ex3.4 EU_quad(C) CU^2", sum(p * (F(x, 100) ** 2) for x, p in [(0, F(1, 3)), (150, F(1, 3)), (300, F(1, 3))]))
print("Ex1.4 EU_quad(A) CU^2", sum(p * (F(x, 100) ** 2) for x, p in [(0, F(1, 4)), (100, F(1, 2)), (400, F(1, 4))]))
# M1
m1 = [(20, F(1, 5)), (50, F(3, 10)), (80, F(1, 2))]
print("M1 EX", sum(p * x for x, p in m1), "Eu", sum(p * x * x for x, p in m1), "u(EX)", 59 * 59, "diff", sum(p * x * x for x, p in m1) - 59 * 59)
# M2
L_ = [(0, F(1, 2)), (100, F(1, 2))]
M_ = [(100, F(1, 4)), (200, F(3, 4))]
mix = {}
for x, p in L_:
    mix[x] = mix.get(x, 0) + F(1, 3) * p
for x, p in M_:
    mix[x] = mix.get(x, 0) + F(2, 3) * p
print("M2 mix", mix, "EU", sum(p * x for x, p in mix.items()), "rhs", F(1, 3) * sum(p * x for x, p in L_) + F(2, 3) * sum(p * x for x, p in M_))
# M3
X = [(10, F(1, 2)), (30, F(1, 2))]
Y = [(0, F(1, 4)), (40, F(3, 4))]
print("M3 EX", sum(p * x for x, p in X), "EY", sum(p * x for x, p in Y), "Ev(X) v=5+3x", sum(p * (5 + 3 * x) for x, p in X), "Ev(Y)", sum(p * (5 + 3 * x) for x, p in Y))
# E1 / E2 / R3
print("E2 1/3*45000+2/3*37500 =", F(1, 3) * 45000 + F(2, 3) * 37500)
print("R3 EU_X", (100 ** 2 + 200 ** 2) / 2, "EU_Y", 150 ** 2, "EX", (100 + 200) / 2, "EY", 150)
print("Pb: lottery 1/2,1/3 sum", F(1, 2) + F(1, 3), "neg lottery sum", F(-1, 2) + F(3, 2))
print("Quiz: mixture 1/3 A + 2/3 D P(0) =", F(1, 3) * F(1, 4) + F(2, 3) * F(1, 2))

print("== L02 ==")
r = 1/4*math.sqrt(40)+1/2*math.sqrt(100)+1/4*math.sqrt(160)
print("Ex1.5 E sqrtW", r, "CE", r*r, "premium", 100 - r*r, "cents CE", round(r*r*100, 4), "premium cents", (100 - r*r)*100)
print("Ex1.5 check 1/4 sqrt40 + 1/2*10 + 1/4 sqrt160 =", 0.25*math.sqrt(40)+0.5*10+0.25*math.sqrt(160))
var = 1/4*3600 + 1/4*3600
print("Var X", var)
ra = 0.5/100  # r_A for sqrt at 100: 1/(2w)
print("rA sqrt at 100", ra, "rR", ra*100, "half-var rule", var/2, "pratt approx", 0.5*ra*var)
def ce(eps, sqrt=True):
    # Lab 1 utility: sqrt on W = 100 + eps X
    vals = [(100 + eps*x, float(p)) for x, p in [(-60, F(1, 4)), (0, F(1, 2)), (60, F(1, 4))]]
    if sqrt:
        e = sum(p*math.sqrt(w) for w, p in vals); return e*e
    return sum(p*w for w, p in vals)
prem1 = 100 - ce(1.0)
print("eps=1 CE", ce(1.0), "premium", prem1, "premium cents half-up", math.floor(prem1*100+0.5), "CE cents", math.floor(ce(1.0)*100+0.5))
print("error", prem1 - 4.5, "share of exact", (prem1 - 4.5)/prem1, "share of approx", (prem1-4.5)/4.5)
for eps in (1.0, 0.5, 0.25, 0.1, 0.01):
    ratio = (100 - ce(eps)) / eps**2
    print("eps", eps, "ratio", round(ratio, 6), "gap", round(abs(ratio-4.5), 6))
print("E1 gap ratio 0.028811/0.004565 =", 0.028811/0.004565, " eps^2 factor", (0.25/0.1)**2)
print("E2 0.565835/5.065835", 0.565835/5.065835, "0.565835/4.5", 0.565835/4.5)
print("E3 CE unrounded cents", ce(1.0)*100, "premium cents", prem1*100)
print("Lab linear r_A zero, ce linear", sum(p*w for w, p in [(100 + 1.0*x, float(p)) for x, p in [(-60, F(1, 4)), (0, F(1, 2)), (60, F(1, 4))]]))
print("M1 check: u=w^{1/2}-1 scaled; M2 ln: r_A=1/w; M3 exp: r_A=a")
print("E1 M1 L02: CE 9 premium", 10-9, "E sqrt(W)=", 0.5*2+0.5*4)

print("== L03 ==")
PR = (5000, 10000, 20000); PB = (F(1, 4), F(1, 2), F(1, 4))
mean = sum(p*x for p, x in zip(PB, PR))
print("L03 exact EV", mean, "geo mean", math.exp(sum(float(p)*math.log(x) for p, x in zip(PB, PR))))
def CE(g):
    p = [float(q) for q in PB]
    if g == 1.0:
        return math.exp(sum(pi*math.log(x) for pi, x in zip(p, PR)))
    s = 1.0 - g
    return (sum(pi*x**s for pi, x in zip(p, PR))) ** (1/s)
for g in (0.0, 0.25, 0.5, 1.0, 2.0, 4.0):
    v = CE(g)
    print("gamma", g, "CE", f"{v:.4f}", "cents", math.floor(v+0.5))
print("gamma2 exact 80000/9", 80000/9, "M", sum(p/x for p, x in zip(PB, PR)), F(9, 80000))
print("L03 Ex2.5 CE2", 1/(0.5/1000+0.5/4000), "CE1", math.sqrt(1000*4000))
print("M2 L03", 1/(F(1, 4)/1000 + F(3, 4)/9000), "E", F(1, 4)*1000+F(3, 4)*9000)
print("M3 L03", 1/(F(1, 4)/3000 + F(3, 4)/27000))
print("M1 L03 r_A(4) for u=(w^.5-1)/.5:", 0.5/4, "direct", -(-0.5*4**-1.5)/(4**-0.5))
print("E1 L03 rounding 10615.8009 ->", math.floor(10615.8009+0.5))
print("E2 L03 8888.8889 vs 80000/9 =", 80000/9)
print("E3 L03 (k+1)/2 at k=10 =", 11/2)
print("L03 A2 e^h-1/h at h=1e-6:", (math.exp(1e-6)-1)/1e-6)
for g in (1.0,):
    pass
print("Remark2.8 check, k=10 random grid")
import random
rng = random.Random(1)
worst = 0
for _ in range(20000):
    v = rng.uniform(0, 1e5)
    kk = rng.choice([2, 3, 10])
    R = lambda z: math.floor(z+0.5)
    worst = max(worst, abs(R(kk*v) - kk*R(v)) / ((kk+1)/2))
print("worst ratio to (k+1)/2 bound", worst)

print("== L04 ==")
S = (1000, 2000, 3000, 4000, 5000)
def pm(d): return tuple(F(d.get(x, 0)) for x in S)
Xa = pm({2000: F(1, 2), 4000: F(1, 2)}); Ya = pm({1000: F(1, 4), 3000: F(1, 2), 5000: F(1, 4)})
Xb = Xa; Yb = pm({3000: F(1, 2), 4000: F(1, 2)})
Xc = pm({1000: F(1, 2), 5000: F(1, 2)}); Yc = pm({3000: F(1)})
def I(p, t): return sum(pi*max(t-x, 0) for pi, x in zip(p, S))
def Fc(p, t): return sum(pi for pi, x in zip(p, S) if x <= t)
for nm, a, b in (("A", Xa, Ya), ("B", Xb, Yb), ("C", Xc, Yc)):
    print(nm, "means", sum(p*x for p, x in zip(a, S)), sum(p*x for p, x in zip(b, S)))
    print(nm, "I_X", [str(I(a, t)) for t in S], "I_Y", [str(I(b, t)) for t in S])
    print(nm, "F_X", [str(Fc(a, t)) for t in S], "F_Y", [str(Fc(b, t)) for t in S])
    fx = all(Fc(a, t) <= Fc(b, t) for t in S); fy = all(Fc(b, t) <= Fc(a, t) for t in S)
    ix = all(I(a, t) <= I(b, t) for t in S); iy = all(I(b, t) <= I(a, t) for t in S)
    print(nm, "FOSD X<=Y", fx, "Y<=X", fy, "SOSD X<=Y", ix, "Y<=X", iy)
print("Ex1.7 check F", [str(Fc(pm({2000: F(1,2), 4000: F(1,2)}), t)) for t in (2000,3000,4000)], [str(Fc(pm({3000: F(1,2), 4000: F(1,2)}), t)) for t in (2000,3000,4000)])
print("L04 M2: I_Y(3000) Ex2.5", I(Ya, 3000), "I_X(3000)", I(Xa, 3000))
print("L04 M3: I_X(3000) for 1/4@1000, 3/4@5000 =", F(1,4)*2000)
print("L04 E1: I_Y(4000) pair B", I(Yb, 4000))
print("L04 R1: I_X(t) vs I_Y(t) Ex2.5 gives F X(2000)=1/2 > F_Y(2000)=1/4 ->", Fc(Xa, 2000), Fc(Ya, 2000), "F_Y(3000)", Fc(Ya, 3000), "F_X(3000)", Fc(Xa, 3000))
print("L04 M1 means: X", sum(p*x for p, x in zip(pm({1000: F(1,2), 4000: F(1,2)}), S)))

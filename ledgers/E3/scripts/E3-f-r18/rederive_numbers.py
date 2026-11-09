# Independent re-derivation (own code, not the lab's) of the numbers printed or stated in the changed L01 and L03 hunks.
from fractions import Fraction as F
import math
# L01 lotteries (cents)
A = [(0, F(1, 4)), (10000, F(1, 2)), (40000, F(1, 4))]
B = [(5000, F(1, 2)), (20000, F(1, 2))]
C = [(0, F(1, 3)), (15000, F(1, 3)), (30000, F(1, 3))]
lin = lambda x: F(x)
quad = lambda x: F(x) ** 2 / 10000
eu = lambda L, u: sum(p * u(x) for x, p in L)
ev = lambda L: sum(p * x for x, p in L)
print("L01 EV A,B,C:", ev(A), ev(B), ev(C))
print("L01 EU quad A,B,C:", eu(A, quad), eu(B, quad), eu(C, quad))
def mix(xi, L, M):
    w = {}
    for x, p in L: w[x] = w.get(x, F(0)) + xi * p
    for x, p in M: w[x] = w.get(x, F(0)) + (1 - xi) * p
    return sorted(w.items())
for xi in (F(1, 4), F(1, 3), F(1, 2)):
    m = mix(xi, A, C)
    print("xi", xi, "quad mix", eu(m, quad), "lin comb", xi * eu(A, quad) + (1 - xi) * eu(C, quad), "lin mix", eu(m, lin))
# L01 Example 1.4 / 3.4 / M1-M3 / R3 / E1
print("Ex1.4 A EV, quad EU:", ev(A), eu(A, quad))
Cx = [(0, F(1, 3)), (150, F(1, 3)), (300, F(1, 3))]
print("Ex3.4 C quad EU (CU^2):", F(0)+F(150**2,1)/3+F(300**2,1)/3)
M1 = [(20, F(1, 5)), (50, F(3, 10)), (80, F(1, 2))]
print("M1 EV, EU sq, u(EV):", ev(M1), eu(M1, lambda x: F(x)**2), F(ev(M1))**2)
# M2 mixture 1/3 L + 2/3 M
Lm = [(0, F(1, 2)), (100, F(1, 2))]; Mm = [(100, F(1, 4)), (200, F(3, 4))]
mm = mix(F(1, 3), Lm, Mm); print("M2 mixture", mm, "EU", eu(mm, lambda x: F(x)), "rhs", F(1,3)*ev(Lm)+F(2,3)*ev(Mm))
# M3
X = [(10, F(1, 2)), (30, F(1, 2))]; Y = [(0, F(1, 4)), (40, F(3, 4))]
print("M3 Eu(X),Eu(Y):", eu(X, lambda x: F(x)), eu(Y, lambda x: F(x)), "tilde:", eu(X, lambda x: 5+3*F(x)), eu(Y, lambda x: 5+3*F(x)))
# L03 CRRA certainty equivalents (own float code)
prizes = [5000, 10000, 20000]; probs = [0.25, 0.5, 0.25]
def ce(g):
    if g == 1: return math.exp(sum(p*math.log(x) for p, x in zip(probs, prizes)))
    s = 1 - g
    return (sum(p * x**s for p, x in zip(probs, prizes))) ** (1/s)
for g in (0, 0.25, 0.5, 1, 2, 4):
    v = ce(g); print("L03 CE gamma", g, f"{v:.4f}", math.floor(v + 0.5))
print("L03 exact gamma2 80000/9 =", 80000/9)
# L03 Example 2.5 and M2/M3
print("Ex2.5 CE2:", 1/(0.5/1000+0.5/4000), "CE1:", math.exp(0.5*math.log(1000)+0.5*math.log(4000)))
print("M2 CE2 =", 1/(0.25/1000+0.75/9000), "M3 CE2(3X)=", 1/(0.25/3000+0.75/27000))
print("E1 round 10615.8009 ->", math.floor(10615.8009+0.5))
# L03 Remark 2.8 check k=10
print("Remark 2.8 bound (k+1)/2 at k=10 =", (10+1)/2)

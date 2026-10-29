"""Independent recomputation of the L04-L06 prose numbers (exact Fractions, no lab code reused)."""
from fractions import Fraction as Fr
import math

def E(pmf, f):
    return sum((p * f(x) for x, p in pmf.items()), Fr(0))

def I(pmf, t):  # integrated distribution = E[(t-X)^+]
    return E(pmf, lambda x: max(t - x, 0))

def F(pmf, t):
    return sum((p for x, p in pmf.items() if x <= t), Fr(0))

print("== L04 Example 2.5")
X = {2000: Fr(1, 2), 4000: Fr(1, 2)}
Y = {1000: Fr(1, 4), 3000: Fr(1, 2), 5000: Fr(1, 4)}
print("means", E(X, lambda x: x), E(Y, lambda x: x))
print("I_X", [str(I(X, t)) for t in (1000, 2000, 3000, 4000, 5000)])
print("I_Y", [str(I(Y, t)) for t in (1000, 2000, 3000, 4000, 5000)])
print("F_X(2000), F_Y(2000), F_Y(3000), F_X(3000)", F(X, 2000), F(Y, 2000), F(Y, 3000), F(X, 3000))
print("== L04 Example 2.6")
X6 = {1000: Fr(1, 2), 5000: Fr(1, 2)}; Y6 = {3000: Fr(1)}
print("means", E(X6, lambda x: x), E(Y6, lambda x: x))
print("I_X", [str(I(X6, t)) for t in (1000, 3000, 5000)], "I_Y", [str(I(Y6, t)) for t in (1000, 3000, 5000)])
print("== L04 Example 1.7 / E1 (I_Y(4000) pair B)", I({3000: Fr(1, 2), 4000: Fr(1, 2)}, 4000))
print("== L04 M3", I({1000: Fr(1, 4), 5000: Fr(3, 4)}, 3000))
print("== L04 Example 2.5 check of chord-based claims: I_X<=I_Y at support points",
      all(I(X, t) <= I(Y, t) for t in (1000, 2000, 3000, 4000, 5000)))
print("== L04 R3 numbers: lambda_R for p=1/3,g=1000,l=300,alpha=1/2 ->",
      (Fr(1,3) / Fr(2,3)) * math.sqrt(float((1000 - Fr(400,3)) / (300 + Fr(400,3)))))

print("== L05")
def a_of(psi): return 1 - 1 / psi
def ce(pmf, g): return E(pmf, lambda c: c ** (1 - g)) ** (1 / (1 - g))
def ez(c0, pmf, beta, g, psi):
    a = a_of(psi); return ((1 - beta) * c0 ** a + beta * ce(pmf, g) ** a) ** (1 / a)
def crra_u(c, g): return c ** (1 - g) / (1 - g)
tree = {1: Fr(1, 2), 4: Fr(1, 2)}
beta, g, psi, c0 = Fr(9, 10), 2, Fr(1, 2), Fr(2)
V0 = ez(c0, tree, beta, g, psi)
U = (1 - beta) * crra_u(c0, g) + beta * E(tree, lambda c: crra_u(c, g))
print("V0", V0, "U", U, "CE1", ce(tree, 2), "mean", E(tree, lambda c: c))
print("E2 variant: CE", ce({1: Fr(1, 4), 4: Fr(3, 4)}, 2), "V0", ez(c0, {1: Fr(1, 4), 4: Fr(3, 4)}, beta, 2, psi))
print("M1 L05: CE", ce({1: Fr(1, 4), 3: Fr(3, 4)}, 2), "mean", E({1: Fr(1, 4), 3: Fr(3, 4)}, lambda c: c))
print("M2 L05: V0 det c1=3 beta=1/2 psi=1/2", ez(Fr(1), {3: Fr(1)}, Fr(1, 2), 2, Fr(1, 2)))
print("Gamma grid CE1 of tree:", [float(ce({1: 0.5, 4: 0.5}, gg)) for gg in (0.5, 2.0, 3.0)])
print("(4,4) vs (1,10) at psi=2,gamma=2,beta=1/2: U", float(crra_u(4.0, 2.0)*0.5+0.5*crra_u(4.0,2.0)),
      float(0.5*crra_u(1.0,2.0)+0.5*crra_u(10.0,2.0)))
print("V0(1,10) psi=2:", float(((0.5 * 1.0 ** 0.5) + 0.5 * 10.0 ** 0.5) ** 2), "V0(4,4):", float(((0.5*4**0.5)+0.5*4**0.5)**2))
print("== L06")
def W(p, g, l, lam, al=1, de=1):
    return p * Fr(g) ** al - (1 - p) * lam * Fr(l) ** de if al == 1 and de == 1 else p * math.pow(g, al) - (1 - p) * lam * math.pow(l, de)
for lam in (Fr(1), Fr(3, 2), Fr(2)):
    print("W lam", lam, W(Fr(1, 2), 1000, 600, lam))
print("lam* 5/3:", Fr(1, 2) * 1000 / ((1 - Fr(1, 2)) * 600))
print("alpha=delta=1/2 lam*", math.sqrt(1000/600), "W(2)", 0.5*math.sqrt(1000) - 0.5*2*math.sqrt(600))
print("Remark2.5 combined at 2:", Fr(1,4)*2000 + Fr(1,2)*400 - Fr(1,4)*2*1200, "separate:", 2*(500 - 300*2))
print("E3 L06 at 3/2: combined", 700 - 300*Fr(3,2), "separate", 1000 - 600*Fr(3,2))
print("M1 L06 lam*", Fr(1,3)*900/((Fr(2,3))*300), "W(2)", Fr(1,3)*900 - Fr(2,3)*2*300)
print("M2 L06 EV", Fr(1,2)*100 - Fr(1,2)*100, "W", Fr(1,2)*100 - Fr(1,2)*2*100)
print("R3 L06 v(2+(-1)) vs v(2)+v(-1) at lam=2:", 1, 2 + 2*(-1))

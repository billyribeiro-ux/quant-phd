"""Round-14 independent recomputation of numbers quoted on the E3 cards (L05-L08 cards included in the slice)."""
import math
from fractions import Fraction as Fr

def omega(p, eta=0.5):
    # omega_{1/2}(p) = sqrt(p) / (1 + 2 sqrt(p(1-p)))  (card c121)
    return math.sqrt(p) / (1 + 2 * math.sqrt(p * (1 - p)))

print("omega(3/10)", omega(0.3), "omega(3/5)", omega(0.6), "omega(1/2)", omega(0.5))
print("c123 2*omega(3/10)", 2 * omega(0.3), "c125 ratio", omega(0.3) / omega(0.6))
print("c125 thresholds", 1 / (1 + 2 ** -1.0), 1 / (1 + 2 ** -0.5))
print("c132 weighted value", 100 * omega(0.01) + 50 * omega(0.99), "EV", 100 * 0.01 + 50 * 0.99)
print("c127 Gamma(A) alpha=1", omega(0.3) * (50 + 100), "Gamma(B)", omega(0.6) * 100)
print("c127 Gamma(A) alpha=.5", omega(0.3) * (math.sqrt(50) + 10), "Gamma(B)", omega(0.6) * 10)
print("c187 diff unrounded", omega(0.3) * 150 - omega(0.6) * 100)
# crossing point of omega(p) = p on a 1001-point grid (c122)
grid = [i / 1000 for i in range(1001)]
last = max(p for p in grid if 0 < p < 1 and omega(p) > p)
print("c122 last grid point with omega(p) > p:", last)
sgn = [(p, omega(p) > p) for p in grid[1:-1]]
changes = [sgn[i][0] for i in range(1, len(sgn)) if sgn[i][1] != sgn[i - 1][1]]
print("c122 sign changes of omega(p)-p at", changes)
# c151 maxmin
def eu_ce(p):
    return 1 / (p / 110000 + (1 - p) / 95000)
ps = [Fr(k, 90) for k in range(30, 61)]
vals = [(-(float(p) / 110000 + (1 - float(p)) / 95000), p) for p in ps]
mn = min(vals)
print("c151 maxmin CE", 1 / -mn[0], "at P(red)=", mn[1])
print("c149 CE at 1/2", 1 / (0.5 / 110000 + 0.5 / 95000), 4180000 / 41)
print("c152 premium", 102500 - 1 / (0.5 / 110000 + 0.5 / 95000))
# c166 prospect wealth equivalent
v = 0.5 * math.sqrt(10000) - 2 * 0.5 * math.sqrt(5000)
x = -(-v / 2) ** 2
print("c166 value", v, "CE change", x, "wealth", 100000 + x)
print("c150 prospect value CU^(1/2)", 0.5 * math.sqrt(100) - 2 * 0.5 * math.sqrt(50), 5 - math.sqrt(50))
# c113 threshold
EV = 1000 / 3 - 300 * 2 / 3
print("c113 lambda_R", (1 / 3 * math.sqrt(1000 - EV)) / (2 / 3 * math.sqrt(EV + 300)), math.sqrt(2) / 2)
# c116 power threshold and W
print("c116 threshold", math.sqrt(1000) / math.sqrt(600), math.sqrt(5 / 3))
print("c116 W at lambda=2", 0.5 * math.sqrt(1000) - 0.5 * 2 * math.sqrt(600))
# c096 CE1
for g in (0.5, 2, 3):
    e = 0.5 * 1 ** (1 - g) + 0.5 * 4 ** (1 - g)
    print("c096 gamma", g, "CE1", e ** (1 / (1 - g)))
# c095 EZ and CRRA
def ez(c0, c1s, beta, psi, gamma):
    a = 1 - 1 / psi
    ev = sum(p * c ** (1 - gamma) for p, c in c1s) ** (1 / (1 - gamma))
    return ((1 - beta) * c0 ** a + beta * ev ** a) ** (1 / a)
print("c095 V0(4,4)", ez(4, [(1, 4)], 0.5, 2, 2), "V0(1,10)", ez(1, [(1, 10)], 0.5, 2, 2))
def crra_u(c0, c1s, beta, gamma):
    uf = lambda c: c ** (1 - gamma) / (1 - gamma)
    return (1 - beta) * uf(c0) + beta * sum(p * uf(c) for p, c in c1s)
print("c095 U(4,4)", crra_u(4, [(1, 4)], 0.5, 2), "U(1,10)", crra_u(1, [(1, 10)], 0.5, 2))
print("c169 U", crra_u(2, [(Fr(1, 2), 1), (Fr(1, 2), 4)], 0.9, 2), -49 / 80)
print("c184 closed form MRS", (1 - 0.9) / 0.9 * (4 / 2) ** (1 / 0.5))

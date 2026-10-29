"""Recompute the L04 card number: grid gap on the restricted dual grid lambda = (0, 0), nu in steps of 1/10 on [-1, 0]."""
from fractions import Fraction as F
S = [[F(2), F(1)], [F(1), F(2)]]
det = S[0][0]*S[1][1]-S[0][1]*S[1][0]
Si = [[S[1][1]/det, -S[0][1]/det], [-S[1][0]/det, S[0][0]/det]]
mu = [F(3, 2), F(1, 5)]
def g(lam, nu):
    r = [mu[i] + lam[i] - nu for i in range(2)]
    q = sum(r[i]*Si[i][j]*r[j] for i in range(2) for j in range(2))
    return -q/2 - nu
nus = [F(-k, 10) for k in range(11)]
best0 = max(g((F(0), F(0)), nu) for nu in nus)
print("max over restricted grid", str(best0), float(best0))
print("grid gap = -1/2 - max", str(F(-1, 2) - best0))
print("g(0,0)", str(g((F(0),F(0)), F(0))))
full = max(g((F(a,10), F(b,10)), F(-c,10)) for a in range(11) for b in range(11) for c in range(11))
print("full grid max", str(full))

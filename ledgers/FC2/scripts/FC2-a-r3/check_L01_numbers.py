"""Independent re-derivation of the L01 numbers (FC2-a round 3). Standard library only."""
from fractions import Fraction as F
from itertools import product

def cost(h, p): return h[0]*p[0] + h[1]*p[1]
def pay(h, X): return [h[0]*r[0] + h[1]*r[1] for r in X]  # X rows = states (u,d), cols = (bond, stock)
def is_arb(h, p, X):
    c = cost(h, p); pr = pay(h, X)
    if c > 0 or any(x < 0 for x in pr): return False
    return c < 0 or any(x > 0 for x in pr)

X = [[F(1), F(3)], [F(1), F(1)]]
A = [F(9,10), F(1)]; B = [F(9,10), F(1,2)]
BOX = range(-10, 11); SMALL = range(-2, 3)
print("A box arbs", sum(is_arb(h, A, X) for h in product(BOX, BOX)))
print("B box arbs", sum(is_arb(h, B, X) for h in product(BOX, BOX)))
def dom(p):
    H = list(product(SMALL, SMALL)); d = v = 0
    for a in H:
        for b in H:
            pa, pb = pay(a, X), pay(b, X)
            if all(x >= y for x, y in zip(pa, pb)):
                d += 1
                if cost(a, p) < cost(b, p): v += 1
    return d, v
print("A dom", dom(A)); print("B dom", dom(B))
# zero-cost strictly positive first holding in B
z = [h for h in product(BOX, BOX) if cost(h, B) == 0 and all(x > 0 for x in pay(h, X))]
print("first zero-cost strictly positive B", z[0], pay(z[0], X))
# Example 2.4
a = (0, 2); b = (1, 1)
print("Ex2.4 cost a,b", cost(a, [F(9,10), F(1)]), cost(b, [F(9,10), F(1)]), "pay a", pay(a, X), "pay b", pay(b, X))
# Remark 3.3 determinant
print("det", X[0][0]*X[1][1]-X[1][0]*X[0][1])
# E2 count of arbitrage portfolios in box for B vs. zero-cost multiples
print("B arbs with cost<0", sum(1 for h in product(BOX, BOX) if is_arb(h, B, X) and cost(h, B) < 0))
# Misconception 1
print("miscon1 cost", F(1) - 2*F(9,10), "pay", [1*1 - 2*1 , 3-2*1 , ][0], 3-2, 1-2)
# Q8 and M1 numbers
print("M1 cost", 2*F(9,10) - 1, "pay", 2*1 - 3*1, 2 - 1)
print("psi at q=1", (F(1)-F(9,10))/2, (F(27,10)-1)/2, "sum", (F(1)-F(9,10))/2 + (F(27,10)-1)/2)
print("M2 psi", (F(1,5))/2, F(4,5)-F(1,10))
print("Q6 stock 27/10 portfolio (3,-1) cost", 3*F(9,10) - F(27,10) + 0, "pay", 3-3, 3-1)

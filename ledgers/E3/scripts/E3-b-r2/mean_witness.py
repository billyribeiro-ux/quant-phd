# Round 2 witness for L05 Remark 1.5 and card E3-c082: two date-1 lotteries with the same mean and different V0.
from fractions import Fraction as F
gamma, psi, beta, c0 = F(2), F(1, 2), F(9, 10), F(2)
a = 1 - 1 / psi
def ce(plan):
    m = sum((p * c ** (1 - gamma) for p, c in plan), F(0))
    return m ** (1 / (1 - gamma))  # exponent 1/(1-gamma) = -1 is an integer here
def v0(plan):
    k = ce(plan)
    bracket = (1 - beta) * c0 ** int(a) + beta * k ** int(a)
    return bracket ** (1 / a)
A = [(F(1, 2), F(1)), (F(1, 2), F(4))]
B = [(F(1), F(5, 2))]
print("mean A", sum(p * c for p, c in A), "CE A", ce(A), "V0 A", v0(A))
print("mean B", sum(p * c for p, c in B), "CE B", ce(B), "V0 B", v0(B))
print("same mean:", sum(p * c for p, c in A) == sum(p * c for p, c in B), "different V0:", v0(A) != v0(B))

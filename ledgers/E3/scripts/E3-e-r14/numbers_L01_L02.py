"""Independent recomputation of the prose numbers in E3 L01 and L02 (verifier round 14, slice e)."""
from fractions import Fraction as F
import math

# L01 Example 1.4 and Misconception 1
A = [(0, F(1, 4)), (100, F(1, 2)), (400, F(1, 4))]
print("L01 EX1.4 E X =", sum(p * x for x, p in A), " E x^2 =", sum(p * x * x for x, p in A))
print("L01 Ex1.4 cents linear", sum(p * 100 * x for x, p in A), " quad x^2/1e4 cents", sum(p * F((100 * x) ** 2, 10000) for x, p in A))
# L01 M1
M1 = [(20, F(1, 5)), (50, F(3, 10)), (80, F(1, 2))]
EX = sum(p * x for x, p in M1); Eu = sum(p * x * x for x, p in M1)
print("L01 M1 EX", EX, "Eu", Eu, "u(EX)", EX * EX, "diff", Eu - EX * EX, "ratio A misc", F(45000, 22500))
# L01 M2 mixture weights
L = [(0, F(1, 2)), (100, F(1, 2))]; M = [(100, F(1, 4)), (200, F(3, 4))]
w = {}
for x, p in L: w[x] = w.get(x, 0) + F(1, 3) * p
for x, p in M: w[x] = w.get(x, 0) + F(2, 3) * p
print("L01 M2 weights", w, "EU", sum(p * x for x, p in w.items()), float(sum(p * x for x, p in w.items())))
print("L01 M2 RHS", F(1, 3) * sum(p * x for x, p in L) + F(2, 3) * sum(p * x for x, p in M))
# L01 M3
X = [(10, F(1, 2)), (30, F(1, 2))]; Y = [(0, F(1, 4)), (40, F(3, 4))]
print("L01 M3 EuX EuY", sum(p * x for x, p in X), sum(p * x for x, p in Y), "v:", sum(p * (5 + 3 * x) for x, p in X), sum(p * (5 + 3 * x) for x, p in Y))
# L01 P3 countable example partial sums
print("L01 P3 partial sums of p_i*x_i =", sum(F(1, 2**i) * 2**i for i in range(1, 11)))
# L01 E1/E2/E3/R3
print("L01 R3 X EU", F(1, 2) * (100**2) + F(1, 2) * 200**2, "Y", 150**2)
# L01 quiz q7 mixture
print("L01 q7", F(1, 3) * F(1, 4) + F(2, 3) * F(1, 2))
# L02 Example 1.5
W = [(40, F(1, 4)), (100, F(1, 2)), (160, F(1, 4))]
EW = sum(p * x for x, p in W)
Eu = F(1, 4) * math.sqrt(40) + F(1, 2) * 10 + F(1, 4) * math.sqrt(160)
CE = Eu ** 2
print("L02 EX1.5 E W", EW, "E sqrtW", repr(Eu), "CE", repr(CE), "premium", 100 - CE)
print("L02 squaring printed 9.743416 ->", 9.743416 ** 2)
print("L02 cents CE", CE * 100, "premium cents", (100 - CE) * 100)
# L02 Lab 1 numbers
var = sum(p * x * x for x, p in [(-60, F(1, 4)), (0, F(1, 2)), (60, F(1, 4))])
print("L02 variance", var, "half-r_A*var", 0.5 * 0.005 * float(var), "half var", float(var) / 2)
print("L02 E2 share", 0.565835 / 5.065835, 0.565835 / 4.5)
print("L02 E1 ratio", 0.028811 / 0.004565, (0.25 / 0.1) ** 2, 4.504565 - 4.5)
print("L02 Part A CE/premium ex act", math.sqrt(0) if False else None)

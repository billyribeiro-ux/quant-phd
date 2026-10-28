# Verifier scratch check for L10 claims (round 5): closed forms, E1 gap, 16/3, 15/16, Part B ratio, 2/3 rounding.
from fractions import Fraction as F
for n in (4, 10, 100, 1000):
    r = F((n + 1) * (4 * n - 1), 6 * n * n) - F(2, 3)
    l = F(4 * n * n - 3 * n - 1, 6 * n * n) - F(2, 3)
    assert r == F(3 * n - 1, 6 * n * n) and l == -F(3 * n + 1, 6 * n * n)
    print(n, float(r), float(l))
print("n=10 errors as fractions", F(29, 600), F(-31, 600), "gap", F(31, 600) - F(29, 600), float(F(1, 300)))
print("printed-digit gap", 0.051666666667 - 0.048333333333)
print("M1 sum", F(1, 2) * F(1, 8) + 1 * F(7, 8), "M2 int_0^2 x d(x^2)", 2 * F(8, 3))
print("(1001)(3999)/(6e6)", F(1001 * 3999, 6 * 10**6), float(F(1001 * 3999, 6 * 10**6)))
print("1/(2n) n=1000", 1 / 2000, "right-half", 0.500500000000 - 0.5, "2/3 6dp", round(2 / 3, 6))
print("n=1000 right err vs 0.0006", abs(0.667166500000 - 2 / 3) < 0.0006, abs(0.666166500000 - 2 / 3) < 0.0006)
print("right+left avg at n=1000", (1001 / 2000 + 999 / 2000) / 2)

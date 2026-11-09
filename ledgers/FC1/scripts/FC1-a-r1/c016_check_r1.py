# Exact check of FC1-c016 (back) and of the L01 Proposition 3.1 closed form, by the recursion of Section 2.
from fractions import Fraction as F

ok = True
for rho in [F(1, 10), F(1, 2), F(9, 10), F(99, 100), F(1)]:
    d = F(1000)
    D = d
    S = F(0)
    for n in range(0, 11):
        S += D
        closed = (1 - (1 - rho) ** (n + 1)) / rho
        if S / d != closed:
            ok = False
        smaller = closed < 1 / rho
        equal = closed == 1 / rho
        # card: 'smaller than 1/rho at every finite n when rho < 1'; 'equals 1/rho at every stage when rho = 1'
        if rho < 1 and not smaller:
            ok = False
        if rho == 1 and not (equal and closed == 1):
            ok = False
        D = (1 - rho) * D
    print("rho", rho, "stage0 multiplier", closed if False else (S / d), "n10 multiplier", float(closed), "1/rho", 1 / rho)
print("c016 claims hold on tested grid:", ok)

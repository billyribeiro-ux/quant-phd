"""Shows that Proposition 3.5's hypothesis set (A1, A2-prime, A3 kept) is inconsistent for any leakage share phi < 1.

A3 (L01.html line 76): 'No cash leaves the bank'. A2-prime (line 132): the share (1 - phi) of each loan 'is held as cash outside the bank'.
Under A2-prime the cash held outside the bank is (1 - phi) * loan > 0 whenever phi < 1 and rho < 1, which is a cash outflow.
"""
from fractions import Fraction as F

d, rho = F(1000), F(1, 10)
for phi in (F(1), F(1, 2), F(9, 10)):
    D = [d]
    cash_out = F(0)
    for t in range(60):
        loan = (1 - rho) * D[-1]
        cash_out += (1 - phi) * loan   # cash held outside the bank at stage t
        D.append(phi * loan)
    limit = sum(D)
    print(f"phi={phi}: cumulative cash outside bank after 60 stages = {float(cash_out):.4f}; "
          f"sum D_t = {float(limit):.4f}; d/(1-phi(1-rho)) = {float(d / (1 - phi * (1 - rho))):.4f}")
print("A3 violated (cash outflow > 0) for every phi < 1: the Prop 3.5 hypothesis set with A3 kept is empty for those phi")

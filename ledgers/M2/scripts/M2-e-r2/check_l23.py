"""Re-derive the L23 lab numbers (SIMULATED bond: face 100000, coupon 5000 x 9 and 105000 at year 10; y0 = 0.04)."""
from fractions import Fraction as Fr

c = [5000.0] * 9 + [105000.0]
N = 10
y0 = 0.04

def P(y):
    return sum(ct * (1 + y) ** (-(t + 1)) for t, ct in enumerate(c))

def P1d(y):
    return -sum((t + 1) * ct * (1 + y) ** (-(t + 1) - 1) for t, ct in enumerate(c))

def P2d(y):
    return sum((t + 1) * (t + 2) * ct * (1 + y) ** (-(t + 1) - 2) for t, ct in enumerate(c))

print("unrounded price at 4%:", f"{P(y0):.6f}", "rounded:", round(P(y0)))
h = 1e-5
print("P'(y0) closed", f"{P1d(y0):.6f}", "central", f"{(P(y0 + h) - P(y0 - h)) / (2 * h):.6f}")
print("P''(y0) closed", f"{P2d(y0):.6f}", "central", f"{(P(y0 + h) - 2 * P(y0) + P(y0 - h)) / h**2:.6f}")
print("preview -P'/P", f"{-P1d(y0)/P(y0):.6f}", "P''/P", f"{P2d(y0)/P(y0):.6f}")
for d in (0.01, 0.005, 0.0025):
    fo = P(y0 + d) - (P(y0) + P1d(y0) * d)
    so = P(y0 + d) - (P(y0) + P1d(y0) * d + 0.5 * P2d(y0) * d * d)
    print(f"shift {d}: first-order error {fo:.6e}  second-order error {so:.6e}")
print("price at +0.01 (yield 0.05):", f"{P(0.05):.6f}", round(P(0.05)))
print("price at -0.01 (yield 0.03):", f"{P(0.03):.6f}", round(P(0.03)))
print("exact-fraction price at 5%:", sum(Fr(ct).limit_denominator() * (Fr(1) / (1 + Fr(1, 20))) ** (t + 1) for t, ct in enumerate(c)))

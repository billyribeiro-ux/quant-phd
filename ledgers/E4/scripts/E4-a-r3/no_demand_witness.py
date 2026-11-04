"""Verifier check (E4 slice a, round 3): does A1, A3 and A4 guarantee that a demand exists at every q in (0, inf)^S?

A4 requires u strictly increasing, strictly concave and differentiable on (0, inf); U(x) = -inf at a zero entry.
Witness: u(x) = 1 - exp(-x) (bounded, u'(0) = 1), pi = (0.1, 0.9), wealth w = 1, prices q = (1, 25).
Along the budget line x1 = (1 - 25 x2) / 1 the best interior bundle is at x2 -> 0+, and the boundary bundle
x2 = 0 has U = -inf, so no bundle in the budget set maximises U.  Pure stdlib; run with python -I.
"""

import math

PI = (0.1, 0.9)
Q = (1.0, 25.0)
W = 1.0


def u(x: float) -> float:
    return 1.0 - math.exp(-x)


def util(x1: float, x2: float) -> float:
    if x1 <= 0.0 or x2 <= 0.0:
        return -math.inf
    return PI[0] * u(x1) + PI[1] * u(x2)


# interior points on the budget line Q.x = W with both entries positive
best_val = -math.inf
best_x2 = None
steps = 200000
for k in range(1, steps):
    x2 = (W / Q[1]) * k / steps
    x1 = (W - Q[1] * x2) / Q[0]
    v = util(x1, x2)
    if v > best_val:
        best_val, best_x2 = v, x2
print(f"sup over interior budget bundles: U = {best_val:.9f} attained near x2 = {best_x2:.3e}")
print(f"boundary bundle (x1, 0) with x1 = W/Q1 = {W / Q[0]}: U = {util(W / Q[0], 0.0)}")
print(f"utility at x2 = 1e-6 along the line: {util((W - Q[1] * 1e-6) / Q[0], 1e-6):.9f}")
print("best interior x2 is at the lower end of the grid (corner), so no maximiser over the budget set:",
      best_x2 is not None and best_x2 < 1e-3)
# derivative at the corner, with the budget line x1 = (W - Q2 x2) / Q1
h = 1e-7
d = (util((W - Q[1] * h) / Q[0], h) - util(W / Q[0], 0.0 + 0.0)) if False else None
d_num = (util((W - Q[1] * 2e-7) / Q[0], 2e-7) - util((W - Q[1] * 1e-7) / Q[0], 1e-7)) / 1e-7
print(f"numerical slope of U along the budget line at x2 -> 0: {d_num:.6f} (negative means corner optimum)")

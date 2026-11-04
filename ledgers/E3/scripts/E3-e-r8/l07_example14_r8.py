"""Round-8: re-derive the numbers and the derivative of Lesson 7, Example 1.4 and Observation 1.5 (eta = 1/2 weighting).

Checks: (1) the closed form omega(p) = sqrt(p) / (1 + 2 sqrt(p(1-p))) equals p^eta / (p^eta + (1-p)^eta)^(1/eta);
(2) the derivative (q + 2p^2) / (2 sqrt(p) q (1 + 2q)^2) matches a central finite difference on (0, 1);
(3) the printed values to eight decimals and ten decimals; (4) the grid facts on 1001 probabilities: nondecreasing,
number of sign changes of omega(p) - p, and the last grid point with omega(p) > p; (5) the bound 0 <= omega <= sqrt(p) <= 1.
Run: .venv/bin/python -I ledgers/E3/scripts/E3-e-r8/l07_example14_r8.py
"""

import math

ETA = 0.5


def omega_general(p: float) -> float:
    if p == 0.0:
        return 0.0
    if p == 1.0:
        return 1.0
    return p**ETA / (p**ETA + (1.0 - p) ** ETA) ** (1.0 / ETA)


def omega_closed(p: float) -> float:
    q = math.sqrt(p * (1.0 - p))
    return math.sqrt(p) / (1.0 + 2.0 * q)


def omega_derivative_claimed(p: float) -> float:
    q = math.sqrt(p * (1.0 - p))
    return (q + 2.0 * p * p) / (2.0 * math.sqrt(p) * q * (1.0 + 2.0 * q) ** 2)


worst_closed = max(abs(omega_general(i / 1000) - omega_closed(i / 1000)) for i in range(1, 1000))
print(f"(1) max |general - closed| on interior grid: {worst_closed:.3e}")

worst_deriv = 0.0
for i in range(1, 1000):
    p = i / 1000
    h = 1e-7
    fd = (omega_closed(p + h) - omega_closed(p - h)) / (2 * h)
    worst_deriv = max(worst_deriv, abs(fd - omega_derivative_claimed(p)))
print(f"(2) max |finite difference - claimed derivative| on (0,1) grid: {worst_deriv:.3e}")

print(f"(3) omega(3/10) = {omega_closed(0.3):.10f}  omega(3/5) = {omega_closed(0.6):.10f}  "
      f"omega(1/2) = {omega_closed(0.5):.10f}  1/(2 sqrt 2) = {1 / (2 * math.sqrt(2)):.10f}")

grid = [i / 1000 for i in range(1001)]
vals = [omega_closed(p) for p in grid]
nondecreasing = all(vals[i + 1] >= vals[i] for i in range(1000))
in_unit = all(0.0 <= v <= 1.0 for v in vals)
diffs = [v - p for v, p in zip(vals, grid, strict=True)]
interior = diffs[1:1000]  # grid points 0.001 to 0.999
sign_changes = sum(1 for i in range(len(interior) - 1) if (interior[i] > 0) != (interior[i + 1] > 0))
last_above = max(p for p, d in zip(grid, diffs, strict=True) if d > 0)
print(f"(4) nondecreasing on grid: {nondecreasing}; in [0,1]: {in_unit}; sign changes of omega-p between interior grid "
      f"points: {sign_changes}; last grid point with omega(p) > p: {last_above}")
bound_ok = all(0.0 <= omega_closed(p) <= math.sqrt(p) <= 1.0 for p in grid[1:])
print(f"(5) 0 <= omega(p) <= sqrt(p) <= 1 on (0,1]: {bound_ok}")

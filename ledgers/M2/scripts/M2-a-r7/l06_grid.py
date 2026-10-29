"""Exact check of the L06 Lab 1 claims: f = x^3 - 3x on the grid -2 to 2, step 1/4."""
from fractions import Fraction as F

f = lambda x: x**3 - 3 * x
df = lambda x: 3 * x**2 - 3
grid = [F(-2) + F(k, 4) for k in range(17)]
sign_ok = all((df(x) > 0) == (x**2 > 1) and (df(x) < 0) == (x**2 < 1) for x in grid)
inc = 0
agree = 0
for a, b in zip(grid, grid[1:]):
    mid = (a + b) / 2
    up = f(b) > f(a)
    inc += up
    agree += up == (df(mid) > 0)
print("points", len(grid), "intervals", len(grid) - 1)
print("grid intervals on which f increases:", inc, "of", len(grid) - 1)
print("increase agrees with sign of f' at midpoint on", agree, "of", len(grid) - 1)
print("f(-1) =", f(F(-1)), "f(1) =", f(F(1)))
print("sign check at grid points:", sign_ok)
print("midpoints are odd multiples of 1/8:", all(((a + b) / 2) * 8 % 2 == 1 for a, b in zip(grid, grid[1:])))

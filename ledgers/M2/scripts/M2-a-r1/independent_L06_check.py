from fractions import Fraction as F
f = lambda x: x**3 - 3*x
fp = lambda x: 3*x*x - 3
grid = [F(-2) + F(k, 4) for k in range(17)]
print('grid points', len(grid))
print('sign of f\' matches 3(x-1)(x+1) at all 17 points:', all(fp(x) == 3*(x-1)*(x+1) for x in grid))
inc = 0
for a, b in zip(grid, grid[1:]):
    m = (a + b) / 2
    if fp(m) > 0:
        inc += 1
    assert (f(b) > f(a)) == (fp(m) > 0)
print('increasing grid intervals:', inc, 'of', len(grid) - 1)
print('f(-1) =', f(F(-1)), ' f(1) =', f(F(1)))

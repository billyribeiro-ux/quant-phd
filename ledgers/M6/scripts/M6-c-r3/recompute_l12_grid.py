"""Independent check of L12 Part A grid error and second moment, n = 0..10 (no twin import)."""
from fractions import Fraction as F

for n in range(0, 11):
    cells = 2 ** n
    worst = F(0)
    sm = F(0)
    for j in range(4097):
        x = F(j, 4096)
        idx = min(int(x * cells), cells - 1)
        mid = F(2 * idx + 1, 2 * cells)
        worst = max(worst, abs(mid - x))
    for j in range(cells):
        a, b = F(j, cells), F(j + 1, cells)
        c = (a + b) / 2
        sm += c * c * (b - a)
    print(n, "largest_grid_error", worst, worst == F(1, 2 ** (n + 1)), "E_M2_ok", sm == F(1, 3) - F(1, 12 * 4 ** n))

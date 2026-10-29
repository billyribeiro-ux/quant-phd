# Independent recomputation for L10: Example 3.3 closed forms (exact), Part B bound (seeded), Part C, Part D.
import random
from fractions import Fraction as F
ok = True
for n in range(1, 60):
    # right tag sum for f=x, G=x^2 on uniform partition: sum_i (i/n)*((i/n)^2-((i-1)/n)^2)
    r = sum(F(i, n) * (F(i, n) ** 2 - F(i - 1, n) ** 2) for i in range(1, n + 1))
    l = sum(F(i - 1, n) * (F(i, n) ** 2 - F(i - 1, n) ** 2) for i in range(1, n + 1))
    ok &= r == F((n + 1) * (4 * n - 1), 6 * n * n) and l == F(4 * n * n - 3 * n - 1, 6 * n * n)
    ok &= r - F(2, 3) == F(3 * n - 1, 6 * n * n) and l - F(2, 3) == -F(3 * n + 1, 6 * n * n)
    ok &= abs(r - F(2, 3)) <= F(1, n) and abs(l - F(2, 3)) <= F(1, n)
print("example 3.3 closed forms n<60 and |err|<=1/n:", ok)
# Part B recomputation with the same draw order as the twin
rng = random.Random(20261028)
worst = 0.0; mx = 0.0; allw = True
for _ in range(200):
    m = rng.randint(1, 30)
    interior = sorted(rng.random() for _ in range(m))
    b = [0.0] + interior + [1.0]
    tags = [lo + rng.random() * (hi - lo) for lo, hi in zip(b, b[1:])]
    S = sum(t * (b[i + 1] ** 2 - b[i] ** 2) for i, t in enumerate(tags))
    mesh = max(hi - lo for lo, hi in zip(b, b[1:]))
    e = abs(S - 2 / 3)
    allw &= e <= 2 * mesh + 1e-12
    worst = max(worst, e / mesh); mx = max(mx, mesh)
print("partB largest mesh %.6f largest err/mesh %.6f all<=2mesh %s" % (mx, worst, allw))
# Part D identity integrator, n=1000
n = 1000
print("partD right", sum(F(i, n) * F(1, n) for i in range(1, n + 1)) == F(n + 1, 2 * n), "left", sum(F(i - 1, n) * F(1, n) for i in range(1, n + 1)) == F(n - 1, 2 * n))
print("E1 gap", float(F(31, 600) - F(29, 600)))
print("quiz n=1000 right", float(F(1001 * 3999, 6 * 10**6)))

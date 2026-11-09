"""Re-derive the L10 numbers: Example 3.3 closed forms, Part B statistics, P2 and R2/R3 checks, quiz values.

Usage: python3 -I l10_numbers.py <repo-root>
"""

import itertools
import pathlib
import random
import subprocess
import sys
from fractions import Fraction

root = pathlib.Path(sys.argv[1])
twin = root / "tests/labs/M5/lab-M5-L10-1.py"
out = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, check=False)
print("twin exit", out.returncode, "stderr", repr(out.stderr))
print(out.stdout)

# Example 3.3 closed forms, exact, for many n
ok = True
for n in range(1, 400):
    right = sum(Fraction(i, n) * (Fraction(i, n) ** 2 - Fraction(i - 1, n) ** 2) for i in range(1, n + 1))
    left = sum(Fraction(i - 1, n) * (Fraction(i, n) ** 2 - Fraction(i - 1, n) ** 2) for i in range(1, n + 1))
    if right != Fraction((n + 1) * (4 * n - 1), 6 * n * n) or left != Fraction(4 * n * n - 3 * n - 1, 6 * n * n):
        ok = False
    if right - Fraction(2, 3) != Fraction(3 * n - 1, 6 * n * n) or left - Fraction(2, 3) != -Fraction(3 * n + 1, 6 * n * n):
        ok = False
    if abs(right - Fraction(2, 3)) > Fraction(1, n) or abs(left - Fraction(2, 3)) > Fraction(1, n):
        ok = False
print("Example 3.3 closed forms and 1/n bound, n=1..399:", ok)
print("E1 n=10: right err 29/600 =", Fraction(29, 600), float(Fraction(29, 600)), " left -31/600 =", float(Fraction(-31, 600)))
print("E1 gap |left err| - right err (float):", 0.051666666667 - 0.048333333333, " 1/300 =", 1 / 300)
print("Example 3.3 n=1000 right exact:", float(Fraction(1001 * 3999, 6 * 10**6)), " left:", float(Fraction(4 * 10**6 - 3000 - 1, 6 * 10**6)))
print("1001*3999 =", 1001 * 3999, " 6e6 =", 6 * 10**6)

# Part B statistics, same draw order as the twin
SEED = 20261028
rng = random.Random(SEED)
worst_ratio = 0.0
max_mesh = 0.0
all_within = True
for _ in range(200):
    m = rng.randint(1, 30)
    interior = sorted(rng.random() for _ in range(m))
    bounds = [0.0, *interior, 1.0]
    tags = [lo + rng.random() * (hi - lo) for lo, hi in itertools.pairwise(bounds)]
    total = 0.0
    for i, tag in enumerate(tags, start=1):
        total += tag * (bounds[i] ** 2 - bounds[i - 1] ** 2)
    mesh = max(hi - lo for lo, hi in itertools.pairwise(bounds))
    err = abs(total - 2 / 3)
    all_within = all_within and err <= 2 * mesh + 1e-12
    worst_ratio = max(worst_ratio, err / mesh)
    max_mesh = max(max_mesh, mesh)
print("Part B recomputed: largest_mesh", max_mesh, "largest_error_over_mesh", worst_ratio, "all_within", all_within)

# P2 check: |S - 2/3| <= mesh for random tagged partitions of [0,1] (f = x, G = x^2)
rng2 = random.Random(7)
worstP2 = 0.0
for _ in range(20000):
    m = rng2.randint(1, 12)
    interior = sorted(rng2.random() for _ in range(m))
    bounds = [0.0, *interior, 1.0]
    tags = [lo + rng2.random() * (hi - lo) for lo, hi in itertools.pairwise(bounds)]
    S = sum(t * (bounds[i] ** 2 - bounds[i - 1] ** 2) for i, t in enumerate(tags, start=1))
    mesh = max(hi - lo for lo, hi in itertools.pairwise(bounds))
    worstP2 = max(worstP2, abs(S - 2 / 3) / mesh)
print("P2 check: max |S-2/3|/mesh over 20000 random tagged partitions =", worstP2)

# R2 / Prop 4.2 check: step at c, f continuous (f = x), uniform and random partitions: |S - c| <= mesh
def step_sum(bounds, tags, c):
    def G(x):
        return 1.0 if x >= c else 0.0
    return sum(f(t) * (G(bounds[i]) - G(bounds[i - 1])) for i, t in enumerate(tags, start=1))

def f(x):
    return x

worstP4 = 0.0
for c in (0.5, 0.3, 0.77):
    for _ in range(3000):
        m = rng2.randint(1, 12)
        interior = sorted(rng2.random() for _ in range(m))
        bounds = [0.0, *interior, 1.0]
        tags = [lo + rng2.random() * (hi - lo) for lo, hi in itertools.pairwise(bounds)]
        S = step_sum(bounds, tags, c)
        mesh = max(hi - lo for lo, hi in itertools.pairwise(bounds))
        worstP4 = max(worstP4, abs(S - c) / mesh)
print("Prop 4.2 / R2 check at c in {0.5,0.3,0.77}: max |S-c|/mesh =", worstP4)

# R3: adding a constant to G leaves the sums unchanged (exact)
same = True
for _ in range(200):
    m = rng2.randint(1, 8)
    interior = sorted(Fraction(rng2.randint(1, 999), 1000) for _ in range(m))
    bounds = [Fraction(0), *interior, Fraction(1)]
    tags = [lo + (hi - lo) / 2 for lo, hi in itertools.pairwise(bounds)]
    S1 = sum(t * ((bounds[i] ** 2 + 5) - (bounds[i - 1] ** 2 + 5)) for i, t in enumerate(tags, start=1))
    S0 = sum(t * (bounds[i] ** 2 - bounds[i - 1] ** 2) for i, t in enumerate(tags, start=1))
    same = same and S0 == S1
print("R3 check: constant leaves exact sums unchanged:", same)

# quiz and M-values
print("Q2 2/3 =", 2 / 3, " Q6 n=1000 right =", 1001 * 3999 / (6 * 10**6), " Q9 3*(1/4) =", 3 * 0.25)
print("M1 S =", Fraction(1, 2) * Fraction(1, 8) + Fraction(7, 8), " M2 16/3 =", Fraction(16, 3))
print("Example 3.3 bound at n=10 right/left |err|:", float(Fraction(29, 600)), float(Fraction(31, 600)))

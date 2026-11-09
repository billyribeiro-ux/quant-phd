"""Independent recomputation of the L03 lab outputs and prose numbers (exact fractions where the lesson says exact)."""
import math
import random
from fractions import Fraction as Fr

# Part A: seeded path, recomputed without the twin's functions
rng = random.Random(20261028)
path = [5000]
for _ in range(10):
    path.append(path[-1] + rng.randint(-40, 40))
margins = [path[i] - path[i - 1] for i in range(1, 11)]
print("A path", *path)
print("A margins", *margins, "sum", sum(margins), "settlement-initial", path[-1] - path[0])
print("A loss days", sum(1 for m in margins if m < 0), "balance", sum(margins))

# Part B: exact
z = [Fr(3, 100), Fr(7, 200), Fr(4, 100), Fr(9, 200), Fr(5, 100)]
df = [Fr(1)] + [Fr(1) / (1 + zi) ** i for i, zi in enumerate(z, start=1)]
ann = sum(df[1:], Fr(0))
R = (1 - df[5]) / ann
print("B DF1..5", [f"{float(d):.6f}" for d in df[1:]])
print("B par", float(R), f"{float(R) * 100:.4f} percent")
notional = 100_000_000  # cents
def half_up(x):
    return math.floor(x + Fr(1, 2))
print("B payment cents", half_up(R * notional))
K = R + Fr(1, 100)
print("B value to payer cents", half_up((1 - df[5] - K * ann) * notional), "minus 1pct*annuity*N", half_up(-Fr(1, 100) * ann * notional))
print("B annuity", float(ann))
print("B par is strictly between 4% and 5%:", Fr(4, 100) < R < Fr(5, 100), "; differs from all zero rates:", all(R != zi for zi in z))
# M2: flat 6% three-year
print("M2 DF3", 1 / 1.06 ** 3, round(1 / 1.06 ** 3, 6), "1.06^3", 1.06 ** 3)
# M3: flat 6% curve, 3 periods, 5% fixed on 100 dollars
dfs = [1 / 1.06 ** i for i in (1, 2, 3)]
print("M3 sum unrounded", sum(dfs), "displayed sum", round(1/1.06, 6) + round(1/1.06**2, 6) + round(1/1.06**3, 6))
print("M3 value per 100 dollars", 100 * 0.01 * sum(dfs))
# R3: DF1=1/1.03, f2=5%
df1 = 1 / 1.03
df2 = df1 / 1.05
print("R3 DF1 DF2", round(df1, 6), round(df2, 6), "Rpar", (1 - df2) / (df1 + df2), "flat 3% DF2", 1.03 ** -2)
# E1: largest loss in printed margins
print("E1 largest loss", min(margins), "day", margins.index(min(margins)) + 1)
# P2 check: value at R+h equals -h*sum DF
h = Fr(1, 100)
print("P2 -h*annuity cents", float(-h * ann * notional))

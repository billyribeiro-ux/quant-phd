"""Re-derive the L01 Example 3.5, canon-breaks and Example 3.6 numbers (closing delta, pin 85b109f8)."""
from fractions import Fraction as Fr
import math

def ceil_frac(x):
    return math.ceil(x)

# Example 3.5 / canon-breaks bullet 2 / M3 / quiz: index ceil(pn) for n equally likely distinct values
for n, p in [(200, Fr(99, 100)), (150, Fr(99, 100)), (40, Fr(9, 10)), (40, Fr(901, 1000))]:
    pn = n * p
    print(f"n={n} p={p} pn={float(pn)} ceil={ceil_frac(pn)} floor={math.floor(pn)}")

# brute-force check of Prop 3.4 for n equally likely distinct values: Q(p) = least j with j/n >= p
def Q_brute(n, p):
    F = [Fr(j, n) for j in range(1, n + 1)]
    return next(j for j in range(1, n + 1) if F[j - 1] >= p)

for n, p in [(150, Fr(99, 100)), (200, Fr(99, 100)), (40, Fr(9, 10)), (40, Fr(901, 1000))]:
    assert Q_brute(n, p) == ceil_frac(n * p), (n, p)
print("brute force agrees with ceil(pn) for the four cases")
print("148/150 =", Fr(148, 150), "=", float(Fr(148, 150)), "; 74/75 =", Fr(74, 75), "; below 0.99:", Fr(148, 150) < Fr(99, 100))

# Example 3.6 table
vals = [-2, -1, 0, 1, 2, 3]
w = [Fr(1, 10), Fr(2, 10), Fr(3, 10), Fr(2, 10), Fr(1, 10), Fr(1, 10)]
assert sum(w) == 1
F = {}
acc = Fr(0)
for x, wi in zip(vals, w):
    acc += wi
    F[x] = acc
print("F:", {k: str(v) for k, v in F.items()})
def Q(p):
    return min(x for x in vals if F[x] >= p)
for p in [Fr(1, 20), Fr(1, 10), Fr(11, 100), Fr(1, 2), Fr(3, 5), Fr(61, 100), Fr(9, 10), Fr(91, 100), Fr(99, 100), Fr(1)]:
    print("Q(", p, ") =", Q(p))
grid_ok = all(F[Q(Fr(j, 100))] >= Fr(j, 100) for j in range(1, 101))
print("F(Q(p)) >= p at 100 grid points:", grid_ok)
print("strict rule inf{x: F(x) > 3/5} =", min(x for x in vals if F[x] > Fr(3, 5)))

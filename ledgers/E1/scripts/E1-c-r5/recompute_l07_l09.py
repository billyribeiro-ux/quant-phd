"""Independent recomputation of the L07-L09 numbers (verifier round 5). Exact Fractions only."""
from fractions import Fraction as F
import math

def cents_half_up(x):
    return math.floor(x + F(1, 2))

print("== L07 closed forms vs. direct integration, cases (a,b,c)")
for a, b, c in [(120, 1, 20), (90, 3, 10), (200, 4, 5)]:
    d = F(a - b * c)
    W = lambda Q: F(2) * d * Q / (2 * b) - Q * Q / (2 * b)
    W_star = d * d / (2 * b)
    rows = {}
    for name, Q, fee in [("mono", d / 2, F(a + b * c, 2 * b)), ("cour", 2 * d / 3, F(a + 2 * b * c, 3 * b)), ("bert", d, F(c))]:
        assert fee == (a - Q) / b, (name, fee)            # fee is P(Q)
        CS = Q * Q / (2 * b); PS = (fee - c) * Q; Wq = CS + PS
        assert Wq == W(Q)
        DWL = W_star - Wq
        assert DWL == (d - Q) ** 2 / (2 * b)
        rows[name] = (CS, PS, Wq, DWL)
        print(name, "CS", CS, "PS", PS, "W", Wq, "DWL", DWL, "cents", [cents_half_up(v) for v in (CS, PS, Wq, DWL)])
    assert rows["mono"][3] > rows["cour"][3] > 0 and rows["bert"][3] == 0
    assert rows["mono"][1] > rows["cour"][1] > rows["bert"][1] == 0
    assert rows["cour"][0] > rows["mono"][0] and rows["bert"][0] > rows["cour"][0]
    assert rows["mono"][2] < rows["cour"][2] < rows["bert"][2]
    print("  shares", rows["mono"][3] / W_star, rows["cour"][3] / W_star)
print("== L07 ratio DWL_M/DWL_C", (F(1, 8)) / (F(1, 18)))
print("== L07 R1 root", float(1 - math.sqrt(2) / 4), "cournot/mono loss", (F(1, 18)) / (F(1, 8)))
print("== L07 R3 difference (7 lam - 2)/72 at lam=2/7", F(7) * F(2, 7) - 2)
print("== L07 M2 cournot loss", F(20 * 20, 6), float(F(20 * 20, 6)), cents_half_up(F(400, 6)))
print("== L07 accounting: CS diff", F(2, 9) - F(1, 8), "PS diff", F(1, 4) - F(2, 9), "W diff", F(4, 9) - F(3, 8))

print("== L08 grid")
X, Y = 8, 4
def ua(x, y): return F(x) * F(y)
def ub(x, y): return (F(X) - F(x)) * (F(Y) - F(y))
grid = [(x, y) for x in range(X + 1) for y in range(Y + 1)]
def dom(z, w):
    return ua(*z) >= ua(*w) and ub(*z) >= ub(*w) and (ua(*z) > ua(*w) or ub(*z) > ub(*w))
eff = [w for w in grid if not any(dom(z, w) for z in grid)]
print("grid-efficient", len(eff), "interior", sum(1 for x, y in eff if 0 < x < X and 0 < y < Y))
interior_eff = [(x, y) for x, y in eff if 0 < x < X and 0 < y < Y]
off = [(x, y) for x, y in interior_eff if y * X != x * Y]
print("off diagonal", len(off))
# Witness search: a rational improvement for each off-diagonal point with a denominator-based search
def improve(x, y):
    # brute search over rational grid of step 1/120 in the box for a strict Pareto improvement
    best = None
    for i in range(1, 120 * X):
        for j in range(1, 120 * Y):
            zx, zy = F(i, 120), F(j, 120)
            if ua(zx, zy) > ua(x, y) and ub(zx, zy) > ub(x, y):
                return (zx, zy)
    return None
for x, y in off:
    z = improve(x, y)
    print((x, y), "witness", z is not None)
# printed amounts from lab Part C (copied from embedded output) and the integer-check claim of L08 line 144
printed = [((6,5),(7,7)),]  # placeholder not used
import re
out = open("/tmp/e1c-v/r5/lab-E1-L08-1.out", encoding="utf-8").read()
A_B = re.findall(r"A = \(([^)]*)\) and B = \(([^)]*)\)", out)
print("Part C printed pairs", len(A_B))
ints = []
for a_s, b_s in A_B:
    amts = [t.strip() for t in (a_s + "," + b_s).split(",")]
    frac = ["/" in t for t in amts]
    integer = [("/" not in t) for t in amts]
    ints.append(integer)
    print(a_s, "|", b_s, "integer amounts:", [t for t, i in zip(amts, integer) if i])
print("pairs where every printed amount is a non-integer:", sum(1 for r in ints if not any(r)), "of", len(ints))
print("pairs with at least one non-integer amount:", sum(1 for r in ints if not all(r)), "of", len(ints))

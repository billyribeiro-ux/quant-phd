"""LX2-d round 6: recompute every number on the LX2 cards from exact fractions (independent of the lab code)."""
from fractions import Fraction as F
from itertools import product

# Part A table as printed by the L04 lab twin (t, forecast, realised, error, hit)
rows = [
    (1, 99, 95, 4, 0), (2, 99, 96, 3, 0), (3, 99, 97, 2, 1), (4, 105, 94, 11, 0), (5, 105, 98, 7, 0),
    (6, 105, 105, 0, 1), (7, 99, 95, 4, 0), (8, 100, 101, -1, 1), (9, 105, 99, 6, 0), (10, 102, 96, 6, 0),
    (11, 104, 99, 5, 0), (12, 102, 105, -3, 0), (13, 100, 101, -1, 1), (14, 105, 97, 8, 0), (15, 97, 95, 2, 1),
    (16, 101, 95, 6, 0), (17, 105, 97, 8, 0), (18, 100, 101, -1, 1), (19, 103, 95, 8, 0), (20, 97, 99, -2, 1),
    (21, 104, 95, 9, 0), (22, 100, 96, 4, 0), (23, 101, 103, -2, 1), (24, 97, 98, -1, 1),
]
for t, f, y, e, h in rows:
    assert f - y == e, t
    assert h == (1 if abs(e) <= 2 else 0), t
H = len(rows)
hits = sum(r[4] for r in rows)
bias = F(sum(r[3] for r in rows), H)
print("Part A hits", hits, "of", H, "hit rate", F(hits, H), "bias", bias, "sum", sum(r[3] for r in rows))
print("Part A MAE", F(sum(abs(r[3]) for r in rows), H))
# Part B windows
for lo, hi in ((0, 12), (12, 24)):
    w = rows[lo:hi]
    print("window", lo + 1, hi, "hit rate", F(sum(r[4] for r in w), len(w)), "bias", F(sum(r[3] for r in w), len(w)))
# Part C
errs = [3, -3, 3, -3]
print("Part C bias", F(sum(errs), 4), "hits", sum(1 for e in errs if abs(e) <= 2), "MAE", F(sum(abs(e) for e in errs), 4))
# Part D: exact generator expectations (A1: U uniform -6..6 realised, V uniform -4..4 forecast; e = (101+V)-(100+U))
pairs = list(product(range(-4, 5), range(-6, 7)))  # (V, U)
n = len(pairs)
Ee = F(sum(1 + v - u for v, u in pairs), n)
Ph = F(sum(1 for v, u in pairs if abs(1 + v - u) <= 2), n)
print("Part D pairs", n, "E[e]", Ee, "P(hit)", Ph, float(Ph), round(float(Ph), 4))
print("Check card 44/117", F(44, 117), round(float(F(44, 117)), 4))
# Proposition 4.4 gap: A2 standard error (E3) for the printed bias
from fractions import Fraction
var_e = F(81 - 1, 12) + F(169 - 1, 12)
print("Var(e)", var_e, "gap", F(41, 12) - 1, "gap/se^2 check", float((F(41, 12) - 1) / ((var_e / 24) ** F(1, 2))))

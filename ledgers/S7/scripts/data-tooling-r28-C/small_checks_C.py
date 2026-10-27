"""Round-28 part C: small re-derivations. (1) S7-c205 / Example 1.4 arithmetic (L07 lines 89-96; card back).
(2) Holm 'second significant digit of test 6' comment (figures-L02.js line 101) from the figure's own T_STATS and
REPORTED_P (lines 37-38). (3) F5 is a module id in curriculum/curriculum.json. Run: python -I small_checks_C.py <checkout>"""
import json
import sys
from fractions import Fraction
from statistics import NormalDist

CK = sys.argv[1]
N = NormalDist()

# (1) Example 1.4 with skewness -2, kurtosis 9, rho-free: V = 1 - s*sigma... as printed: 1 - (-2)(0.1) + (9-1)/4 (0.1)^2
v = Fraction(1) - Fraction(-2) * Fraction(1, 10) + Fraction(9 - 1, 4) * Fraction(1, 10) ** 2
normal = 1 + Fraction(1, 10) ** 2 / 2
print("c205 V =", float(v), "(page 1.22); normal formula =", float(normal), "(page 1.005)")
print("c205 understatement 1 - normal/V =", round(float(1 - normal / v), 4), "-> 18% (page)")

# (2) Holm step five, figures-L02.js: T_STATS[5] = 2.64 (test 6), REPORTED_P[5] = 0.84%, m = 10, step k = 5
t6 = 2.64
p_rec = 2 * (1 - N.cdf(t6))
thr = 0.05 / (10 + 1 - 5)
print(f"Holm step 5: recomputed p(test 6) = {p_rec * 100:.4f}% ; threshold 0.05/6 = {thr * 100:.4f}% ; "
      f"published 0.84% -> {'reject' if 0.0084 <= thr else 'no reject'}; recomputed -> {'reject' if p_rec <= thr else 'no reject'}")
t_stats = [1.99, 2.63, 2.21, 3.43, 2.17, 2.64, 4.56, 5.34, 2.75, 2.49]
rec = [2 * (1 - N.cdf(t)) for t in t_stats]
order = sorted(range(10), key=lambda i: rec[i])
print("recomputed order (test numbers, 1-based):", [i + 1 for i in order], "-> test 6 is in position", order.index(5) + 1)
rep = [0.0466, 0.0085, 0.0271, 0.0005, 0.030, 0.0084, 0.0, 0.0, 0.006, 0.0128]
order_rep = sorted(range(10), key=lambda i: rep[i])
print("published order (test numbers, 1-based):", [i + 1 for i in order_rep], "-> test 6 is in position", order_rep.index(5) + 1)

# (3) F5 module id
cur = json.load(open(f"{CK}/curriculum/curriculum.json", encoding="utf-8"))
mods = [m["id"] for part in cur["parts"] for m in part["modules"]]
print("F5 in curriculum modules:", "F5" in mods)

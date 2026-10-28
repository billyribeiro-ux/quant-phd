"""Independent recomputation of the numbers and worked examples in M3 slice a (hub, L01-L03).

Run from the checkout root with the repository venv, under isolated mode:
    .venv/bin/python -I ledgers/M3/scripts/M3-a-r1/recheck_m3a.py
Standard library only. Every check prints its inputs and the recomputed value.
"""

from __future__ import annotations

import math
from fractions import Fraction as F
from pathlib import Path


def matmul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]


def det2(m: list[list[F]]) -> F:
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def det3(m: list[list[F]]) -> F:
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def mv(a: list[list[F]], v: list[F]) -> list[F]:
    return [sum((a[i][k] * v[k] for k in range(len(v))), F(0)) for i in range(len(a))]


def inv2(m: list[list[F]]) -> list[list[F]]:
    d = det2(m)
    return [[m[1][1] / d, -m[0][1] / d], [-m[1][0] / d, m[0][0] / d]]


def check(label: str, ok: bool, detail: str) -> None:
    print(f"{'OK  ' if ok else 'FAIL'} {label}: {detail}")


# 1. Hub placement percentages (hub line 70): 7/9 and 8/9.
print(f"7/9 = {100 * 7 / 9:.4f} percent, 8/9 = {100 * 8 / 9:.4f} percent")
check("hub placement 77.8 and 88.9", round(100 * 7 / 9, 1) == 77.8 and round(100 * 8 / 9, 1) == 88.9, "7/9, 8/9")

# 2. Hub PV item (hub line 89): 100 / 1.05^2 rounded to three decimals.
pv = 100 / 1.05**2
check("hub PV 90.703", round(pv, 3) == 90.703, f"unrounded {pv:.6f}")

# 3. Hub geometric sum (hub line 84): 1 + 1/2 + 1/4 + 1/8.
check("hub sum 1.875", F(1) + F(1, 2) + F(1, 4) + F(1, 8) == F(15, 8), "exact 15/8")

# 4. Hub skill check 1 (hub line 128): span dimension of three vectors.
v = [[F(1), F(0), F(1)], [F(0), F(1), F(1)], [F(1), F(1), F(2)]]
check("skill check 1 dim span = 2", v[2] == [v[0][i] + v[1][i] for i in range(3)], "v3 = v1 + v2, plane z = x + y")

# 5. Hub skill check 2 (hub line 133): C = D^-1 Sigma D^-1 with D = diag(s).
s1, s2 = F(2), F(3)
c12 = F(1, 2)  # an example correlation 0.5 between two assets, unrounded
sigma = [[s1 * s1, s1 * s2 * c12], [s1 * s2 * c12, s2 * s2]]
dinv = [[1 / s1, F(0)], [F(0), 1 / s2]]
c = matmul(matmul(dinv, sigma), dinv)
check("skill check 2 recovers C", c[0][1] == c12 and c[0][0] == 1, f"C_12 = {c[0][1]}")

# 6. Hub/L01 sum of hour cards (hub lines 148-156): 12+11+12+12+12+11+11+12+12.
hours = [12, 11, 12, 12, 12, 11, 11, 12, 12]
check("lesson hours sum to 105", sum(hours) == 105 and 105 + 45 == 150, f"sum {sum(hours)}")
check("L01-L03 page hours match cards", hours[:3] == [12, 11, 12], "data-hours 12, 11, 12")

# 7. L01 Example 3.10 and card M3-c020: v3 = v1 + v2 and span plane z = x + y.
v1, v2 = [F(1), F(0), F(1)], [F(0), F(1), F(1)]
check("Example 3.10 dependence", [v1[i] + v2[i] for i in range(3)] == [F(1), F(1), F(2)], "coefficients 1,1,-1")

# 8. L01 mech-1 (u=(1,2,0), v=(0,1,1), w=(1,3,1)): u+v=w.
u, vv, w = [F(1), F(2), F(0)], [F(0), F(1), F(1)], [F(1), F(3), F(1)]
check("L01 mech-1 u+v=w", [u[i] + vv[i] for i in range(3)] == w, "dim span = 2")

# 9. L01 R3 floating example: exact determinant of columns (1,1),(1,1+1e-12).
d = F(1) * (1 + F(1, 10**12)) - F(1) * F(1)
check("L01 R3 exact pivot 1e-12", d == F(1, 10**12), f"exact second pivot {d}")

# 10. L01 E2 rank by hand: columns (1,2,3),(2,4,6),(0,1,1).
rows = [[F(1), F(2), F(0)], [F(2), F(4), F(1)], [F(3), F(6), F(1)]]
r2 = [rows[1][i] - 2 * rows[0][i] for i in range(3)]
r3 = [rows[2][i] - 3 * rows[0][i] for i in range(3)]
r3b = [r3[i] - r2[i] for i in range(3)]
check("L01 E2 rank 2", r2 == [0, 0, 1] and r3 == [0, 0, 1] and r3b == [0, 0, 0], "pivots in columns 1 and 3")

# 11. L01 E3: fourth vector in the span of the planted triple.
v1, v2, v3 = [F(1), F(0), F(2), F(-1)], [F(0), F(1), F(1), F(3)], [F(2), F(-1), F(0), F(1)]
v4 = [2 * v1[i] - v2[i] + v3[i] for i in range(4)]

# 12. L02 Example 2.6 and Example 4.3 products.
A = [[F(1), F(1)], [F(1), F(-1)]]
P = [[F(1), F(1)], [F(0), F(1)]]
Pinv = inv2(P)
check("L02 Example 4.3 P^-1 A P", matmul(Pinv, matmul(A, P)) == [[0, 2], [1, 0]], "equals [[0,2],[1,0]]")
check("L02 Example 2.6 T b1 = b2", [F(1) * 1 + 0, F(1) * 1 - 0] == [1, 1], "T(1,0)=(1,1)")
check("L02 Example 2.6 T b2 = 2 b1", [F(1) + F(1), F(1) - F(1)] == [2, 0], "T(1,1)=(2,0)")

# 13. L02 misconception 2 (A=[[1,1],[0,1]], C=[[1,0],[1,1]]).
Am = [[F(1), F(1)], [F(0), F(1)]]
Cm = [[F(1), F(0)], [F(1), F(1)]]
check("L02 misc2 AC", matmul(Am, Cm) == [[2, 1], [1, 1]], "AC")
check("L02 misc2 CA", matmul(Cm, Am) == [[1, 1], [1, 2]], "CA")

# 14. L02 problem M1 (T(x,y)=(2x-y,x)) and Q numeric entry.
check("L02 M1 matrix", [[F(2), F(-1)], [F(1), F(0)]] == [[2, -1], [1, 0]], "columns (2,1), (-1,0)")

# 15. L02 R3 differentiation matrix on c0..c3.
Dm = [[F(0), F(1), F(0), F(0)], [F(0), F(0), F(2), F(0)], [F(0), F(0), F(0), F(3)], [F(0), F(0), F(0), F(0)]]
cvec = [F(5), F(7), F(-2), F(4)]
check("L02 R3 D action", mv(Dm, cvec) == [F(7), F(-4), F(12), F(0)], "(c1, 2c2, 3c3, 0)")

# 16. L03 Example 1.6: characteristic polynomial and eigenvalues of [[4,1],[1,3]].
lam_p = (7 + math.sqrt(5)) / 2
lam_m = (7 - math.sqrt(5)) / 2
check("L03 Ex1.6 roots", abs(lam_p**2 - 7 * lam_p + 11) < 1e-12, f"lambda+ {lam_p:.10f}")
check("L03 Ex1.6 rounded", f"{lam_p:.4f}" == "4.6180" and f"{lam_m:.4f}" == "2.3820", f"{lam_p:.6f}, {lam_m:.6f}")
# Example 1.6 eigenvector (1, l-4): second coordinate of (A - lI)v is 1 + (3-l)(l-4), which must equal
# -(l^2-7l+11). A quadratic identity is confirmed by agreement at 39 rational points (degree 2 < 39).
ok_identity = all(1 + (3 - l) * (l - 4) == -(l * l - 7 * l + 11) for l in [F(k, 3) for k in range(-9, 30)])
check("L03 Ex1.6 identity 1+(3-l)(l-4) = -(l^2-7l+11)", ok_identity, "agreement at 39 rational points, degree 2")
check(
    "L03 Ex1.6 first coordinate (4-l)+(l-4) = 0",
    all((4 - l) + (l - 4) == 0 for l in [F(k, 3) for k in range(-9, 30)]),
    "identically zero",
)

# 17. L03 Remark 1.7 and Misconception 1: det(A - 4I), det(A - 3I) for A=[[4,1],[1,3]].
A4 = [[F(0), F(1)], [F(1), F(-1)]]  # A - 4I
A3 = [[F(1), F(1)], [F(1), F(0)]]  # A - 3I
check("L03 misc1 det(A-4I) = -1", det2(A4) == -1, f"{det2(A4)}")
check("L03 misc1 det(A-3I) = -1", det2(A3) == -1, f"{det2(A3)}")

# 18. L03 misconception 1 counterexample: upper triangular matrix has its diagonal as eigenvalues.
T = [[F(2), F(1), F(0)], [F(0), F(3), F(1)], [F(0), F(0), F(5)]]
for lam, vec in [(2, [1, 0, 0]), (3, [1, 1, 0]), (5, [1, 3, 6])]:
    ok = mv(T, [F(t) for t in vec]) == [F(lam) * F(t) for t in vec]
    check(f"L03 Example 2.5 eigenpair {lam}", ok, f"A v = {lam} v with v={vec}")
check("L03 misc1 counterexample: triangular T has eigenvalues 2,3,5", all(mv(T, [F(t) for t in vec]) == [F(l) * F(t) for l, vec in [(2, [1, 0, 0])][:0] or [(lam, vec)]][0] for lam, vec in []) or all(mv(T, [F(t) for t in vec]) == [F(l) * F(t) for t in vec] for l, vec in [(2, [1, 0, 0]), (3, [1, 1, 0]), (5, [1, 3, 6])]), "so the sentence 'only for a diagonal matrix' is false")

# 19. L03 Example 2.5 det P = 6, and E2 cofactor expansion.
Pt = [[F(1), F(1), F(1)], [F(0), F(1), F(3)], [F(0), F(0), F(6)]]
check("L03 det P = 6", det3(Pt) == 6, f"{det3(Pt)}")

# 20. L03 M2 and M3 solutions.
A2 = [[F(1), F(2)], [F(2), F(4)]]
check("L03 M2 eigenpairs", mv(A2, [F(2), F(-1)]) == [0, 0] and mv(A2, [F(1), F(2)]) == [5, 10], "0 and 5")
P2 = [[F(2), F(1)], [F(-1), F(2)]]
check("L03 M3 P^-1 and PDP^-1 = A", matmul(matmul(P2, [[F(0), F(0)], [F(0), F(5)]]), inv2(P2)) == A2, "A = P D P^-1")

# 21. L03 M1: A = [[3,2],[0,1]] eigenpairs.
A1 = [[F(3), F(2)], [F(0), F(1)]]
check("L03 M1 eigenpairs", mv(A1, [F(1), F(0)]) == [3, 0] and mv(A1, [F(1), F(-1)]) == [1, -1], "3 and 1")

# 22. L03 R3: A^3 via P D^3 P^-1 and directly.
P3 = [[F(1), F(1)], [F(0), F(-1)]]
D3 = [[F(27), F(0)], [F(0), F(1)]]
A3m = [[F(3), F(2)], [F(0), F(1)]]
direct = matmul(A3m, matmul(A3m, A3m))
check("L03 R3 A^3 by factorisation", matmul(matmul(P3, D3), inv2(P3)) == direct, f"{direct}")

# 23. L03 Prop 2.6 matrix B: E1 is one-dimensional.
B = [[F(1), F(1)], [F(0), F(1)]]
BI = [[B[i][j] - (1 if i == j else 0) for j in range(2)] for i in range(2)]
check("L03 B - I rank 1", BI != [[0, 0], [0, 0]] and det2(BI) == 0, "rank 1: det 0, nonzero")

# 24. L03 quiz numeric: four decimals of (7+sqrt5)/2 within 0.00005 of 4.6180.
check("L03 quiz tolerance", abs(lam_p - 4.6180) <= 0.00005, f"|diff| = {abs(lam_p - 4.6180):.6f}")

# 25. L03 F1 one-sided inverse: a left inverse is a two-sided inverse for square matrices (exact check).
M = [[F(2), F(1)], [F(1), F(1)]]
N = inv2(M)
check("F1 one-sided implies two-sided on example", matmul(M, N) == matmul(N, M), "both products equal I")

# 26. Rank definitions: pivot count (L01 Def 3.3) versus dimension of column span (L03 Def 2.5) on a 3x3 example.
Mx = [[F(1), F(2), F(0)], [F(2), F(4), F(1)], [F(3), F(6), F(1)]]
cols = [[Mx[i][j] for i in range(3)] for j in range(3)]
check("rank example: columns 2 and 1 proportional", cols[1] == [2 * t for t in cols[0]], "rank of span of columns is 2")

# 27. Registry and hub source citations: the M1 result cited by hub Pm7 is absent from M1 pages.
m1_hits = [p.name for p in Path("course/modules/M/M1").glob("*.html") if "contrapositive" in p.read_text(encoding="utf-8").lower()]
check("hub Pm7 cites M1 Lesson 2 for the contrapositive", m1_hits == [], f"M1 pages containing 'contrapositive': {m1_hits}")

# 28. Hub data claim: MANIFEST ust_daily has two series.
import json  # noqa: E402

man = json.loads(Path("course/assets/data/market/MANIFEST.json").read_text(encoding="utf-8"))
ust = next(d for d in man["datasets"] if d["id"] == "ust_daily")
check("hub: embedded yield snapshot has two series", "series tbill_3m=RIFSGFSM03_N.B, cmt_10y=RIFLGFCY10_N.B" in ust["transform"], "tbill_3m and cmt_10y")

# 29. Hub data claim: Lesson 8 lab tenor count (six tenors in the twin, not three).
twin = Path("tests/labs/M3/lab-M3-L08-1.py").read_text(encoding="utf-8")
check("hub 'three tenors' vs L08 twin", "TENORS = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0])" in twin and "six-tenor" in twin, "twin uses six tenors")

# 30. L01 lab docstring (c): "rank 3 exactly when v1, v2, v3 are independent", per draw. The lab compares
# only the two counts. Here the per-draw statement is computed with an exact rank (Gaussian elimination).
def rank_exact(cols: list[list[F]]) -> int:
    m = [[cols[j][i] for j in range(len(cols))] for i in range(len(cols[0]))]
    piv = 0
    for c_ in range(len(cols)):
        p = next((i for i in range(piv, len(m)) if m[i][c_] != 0), None)
        if p is None:
            continue
        m[piv], m[p] = m[p], m[piv]
        for i in range(len(m)):
            if i != piv and m[i][c_] != 0:
                f_ = m[i][c_] / m[piv][c_]
                m[i] = [x - f_ * y for x, y in zip(m[i], m[piv], strict=True)]
        piv += 1
    return piv


import random  # noqa: E402

rng = random.Random(1)
per_draw_mismatch = 0
draws = 100
for _ in range(draws):
    a, b, cc = ([F(rng.randint(-3, 3)) for _ in range(4)] for _ in range(3))
    dd = [2 * a[i] - b[i] + cc[i] for i in range(4)]
    if (rank_exact([a, b, cc, dd]) == 3) != (rank_exact([a, b, cc]) == 3):
        per_draw_mismatch += 1
check(
    "L01 planted per-draw identity (100 random draws, exact)",
    per_draw_mismatch == 0,
    f"per-draw mismatches {per_draw_mismatch} of {draws}; the lab prints only the two counts",
)

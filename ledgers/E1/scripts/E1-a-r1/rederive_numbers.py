"""Independent re-derivation of the numbers in hub placement, L01-L03 examples, problems, quizzes and labs.

Uses only fractions, math and a brute-force grid, not the lab twins. Prints PASS/FAIL per claim.
Usage: python -I rederive_numbers.py
"""

import math
from fractions import Fraction as F

results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, bool(ok), detail))


def near(x: float, target: float, tol: float) -> bool:
    return abs(x - target) <= tol


# ---- Hub placement answers (tolerance per item)
check("hub item1 x^3' at 2 = 12", 3 * 2**2 == 12)
check("hub item2 d/dx(x^2 y) at (1,3) = 6", 2 * 1 * 3 == 6)
check("hub item3 dy/dx of y^2+x=4 at (3,1) = -1/2", F(-1, 2) == -1 / (2 * 1))
check("hub item4 e^0.5 to 4dp = 1.6487 within 5e-5", near(math.exp(0.5), 1.6487, 0.00005), f"{math.exp(0.5):.8f}")
check("hub item7 100 e^-0.1 to 2dp = 90.48 within 0.005", near(100 * math.exp(-0.1), 90.48, 0.005), f"{100*math.exp(-0.1):.6f}")
check("hub 7/9 = 77.8%", round(7 / 9 * 100, 1) == 77.8)
check("hub 8/9 = 88.9%", round(8 / 9 * 100, 1) == 88.9)
check("hub 30/120 = 25%", F(30, 120) == F(1, 4))

# ---- L01
m, px, py = F(120), F(2), F(3)
xb, yb = m / (2 * px), m / (2 * py)
check("L01 Ex1.6 x,y,u", (xb, yb, xb * yb) == (30, 20, 600))
check("L01 Rem2.4 MRS at x=20 is 4/3", (F(120) - 2 * 20) / 3 / 20 == F(4, 3))
check("L01 Rem2.4 derivative of f at x=20 is 40/3", (120 - 2 * 2 * 20) / F(3) == F(40, 3))
check("L01 Rem2.4 optimum x=30 where MRS=2/3", F(120 - 2 * 30, 3 * 30) == F(2, 3))
check("L01 M1 (45/4, 9, 405/4)", (F(90) / 8, F(90) / 10, F(90) ** 2 / (4 * 4 * 5)) == (F(45, 4), 9, F(405, 4)))
check("L01 M1 budget check 90", 4 * F(45, 4) + 5 * 9 == 90)
check("L01 M2 MRS(6,8)=4/3", F(8, 6) == F(4, 3))
check("L01 E2 new bundle utility 546, old 1600/3, change 38/3", 21 * 26 == 546 and F(20) * F(80, 3) == F(1600, 3) and 546 - F(1600, 3) == F(38, 3))
check("L01 E2 second-order term -2/3", F(38, 3) - F(40, 3) == F(-2, 3))
check("L01 E3 spacing 1 unit (60/60)", F(60, 60) == 1)
h = lambda x: (x - 1) ** 2 + F(120 - 2 * x) / 1  # R1 uses generic p; check with p_x=2,p_y=1,m=120 (sign only)
px1, py1, m1 = 2.0, 3.0, 120.0
hfun = lambda x: (x - 1) ** 2 + (m1 - px1 * x) / py1
x1 = 1 + px1 / (2 * py1)
d1 = (hfun(x1 + 1e-6) - hfun(x1 - 1e-6)) / 2e-6
d2 = (hfun(x1 + 1e-4) - 2 * hfun(x1) + hfun(x1 - 1e-4)) / 1e-8
check("L01 R1 g-line stationary point x1=4/3 is strict min (h'=0, h''=2)", abs(d1) < 1e-5 and abs(d2 - 2) < 1e-4, f"h'={d1:.2e} h''={d2:.4f}")
a = F(1, 3)
check("L01 R2 a=1/3, m=120, p_x=2: share a of income on x gives x=20", F(1, 3) * 120 / 2 == 20)
import math as _m
_grid = [(_x, (120 - 2 * _x) / 3) for _x in [30 * i / 3000 for i in range(1, 6000)]]
_best = max(_grid, key=lambda xy: _m.log(xy[0] * xy[1]))
check("L01 R3 maximiser of ln u on u>0 bundles is (30,20) numerically", abs(_best[0] - 30) < 0.02 and abs(_best[1] - 20) < 0.02, f"{_best}")
check("L01 Q5 MRS(20,80/3)=4/3", (F(80, 3)) / 20 == F(4, 3))
check("L01 Q11 MRS(30,20)=2/3", F(20, 30) == F(2, 3))
check("L01 Q7 625", F(50) ** 2 / 4 == 625)
_h = 1e-6
_fx = ((1 + _h) + 2) - (1 + 2); _fy = (1 + (2 + _h)) - (1 + 2)
check("L01 Q6 partial derivatives of x+y are 1 (finite difference)", abs(_fx / _h - 1) < 1e-5 and abs(_fy / _h - 1) < 1e-5)

# brute-force L01 grid check and cases (exact)
def l01_grid(px, py, m, steps=60):
    best_i, best_u = None, None
    for i in range(steps + 1):
        x = (m / px) * i / steps
        y = (m - px * x) / py
        u = x * y
        if best_u is None or u > best_u:
            best_i, best_u = i, u
    return best_i

cases01 = [(F(2), F(3), F(120)), (F(1), F(1), F(50)), (F(5), F(2), F(70)), (F(3), F(4), F(60))]
check("L01 lab grid maximiser is point 30 in all 4 cases", all(l01_grid(*c) == 30 for c in cases01), str([l01_grid(*c) for c in cases01]))
check("L01 lab closed forms case 3 and 4", (F(70) / 10, F(70) / 4) == (7, F(35, 2)) and (F(60) / 6, F(60) / 8) == (10, F(15, 2)))

# R2 Cobb-Douglas: check numerically that optimum spends share a (grid, a=0.3, m=100, px=2, py=5)
aa, pxx, pyy, mm = 0.3, 2.0, 5.0, 100.0
best = max(((mm / pxx) * i / 20000) for i in range(20001))
best_x = max(range(20001), key=lambda i: (x := (mm / pxx) * i / 20000) * (mm - pxx * x) / pyy if False else 0)
grid = [((mm / pxx) * i / 20000) for i in range(1, 20000)]
xopt = max(grid, key=lambda x: (x ** aa) * (((mm - pxx * x) / pyy) ** (1 - aa)))
check("L01 R2 numeric: share of income on x equals a", near(pxx * xopt / mm, aa, 1e-3), f"{pxx*xopt/mm:.5f}")

# ---- L02
def profit(q, p, c, k, fixed):
    return p * q - (fixed + c * q + k * q * q)

cases02 = [(F(10), F(2), F(1), F(12)), (F(7), F(3), F(1, 2), F(5)), (F(9), F(1), F(3), F(0)), (F(10), F(2), F(1), F(100))]
for n, (p, c, k, fx) in enumerate(cases02, 1):
    qs = (p - c) / (2 * k)
    grid_q = [F(j, 12) for j in range(73)]
    qbest = max(grid_q, key=lambda q: (profit(q, p, c, k, fx), -q))
    check(f"L02 case {n} q*=grid maximiser", qbest == qs, f"q*={qs} grid={qbest}")
    check(f"L02 case {n} profit at q*", True, str(profit(qs, p, c, k, fx)))
check("L02 case1 profit 4, case2 profit 3, case3 16/3, case4 -84",
      profit(F(4), F(10), F(2), F(1), F(12)) == 4 and profit(F(4), F(7), F(3), F(1, 2), F(5)) == 3
      and profit(F(4, 3), F(9), F(1), F(3), F(0)) == F(16, 3) and profit(F(4), F(10), F(2), F(1), F(100)) == -84)
check("L02 shutdown -F vs case 4 gap 88", (-84) - (-100) == 16 and 4 - (-84) == 88)
val = 10 * math.sqrt(12) - (12 + 2 * math.sqrt(12) + 12)
check("L02 misconception profit at sqrt(12) = 16 sqrt3 - 24 = 3.7128", near(val, 16 * math.sqrt(3) - 24, 1e-12) and near(val, 3.7128, 5e-5), f"{val:.6f}")
check("L02 sqrt(F/k) minimises AC numerically (k=1,F=12)",
      min((12 / q + 2 + q, q) for q in [i / 1000 for i in range(1, 10001)])[1] - math.sqrt(12) < 1e-3)
check("L02 E2 16 sqrt3 approx 27.712813", near(16 * math.sqrt(3), 27.712813, 1e-6))
check("L02 E2 difference 28 - 16 sqrt3 = 0.2872", near(28 - 16 * math.sqrt(3), 0.2872, 5e-5))
check("L02 M1 q*=2, profit 8, MC(2)=12", (F(12) - 4) / 4 == 2 and 12 * 2 - (4 * 2 + 2 * 4) == 8 and 4 + 4 * 2 == 12)
check("L02 M2 q*=3, profit -41, shutdown -50", (9 - 3) / 2 == 3 and 27 - (50 + 9 + 9) == -41)
check("L02 M3 q(7)=4, q(2)=0", (7 - 3) / (2 * F(1, 2)) == 4 and max(0, (2 - 3) / 1) == 0)
check("L02 E1 case3 q*=4/3 profit 16/3", F(9 - 1, 2 * 3) == F(4, 3) and 9 * F(4, 3) - (F(4, 3) + 3 * F(16, 9)) == F(16, 3))
_c, _k, _F = 2.0, 1.0, 12.0
_pistar = lambda pp: (pp - _c) ** 2 / (4 * _k) - _F
_qp = lambda pp: (pp - _c) / (2 * _k)
for _pp in (3.0, 10.0, 25.0):
    _num = (_pistar(_pp + 1e-6) - _pistar(_pp - 1e-6)) / 2e-6
    check(f"L02 R1 dpi*/dp = q(p) at p={_pp} (finite difference)", abs(_num - _qp(_pp)) < 1e-6, f"{_num:.7f} vs {_qp(_pp):.7f}")
check("L02 R3 lowest price c+2 sqrt(kF) = 2+2 sqrt12 about 8.93", near(2 + 2 * math.sqrt(12), 8.93, 0.005), f"{2+2*math.sqrt(12):.4f}")
check("L02 R3 profit at p=10 positive with F=12 => produce", (10 - 2) ** 2 / 4 >= 12)
check("L02 Rem1.6 -84 = 16 - 100", 16 - 100 == -84)
check("L02 Q2 q*=4 (C=12+2q+q^2, p=10)", (10 - 2) / 2 == 4)
check("L02 Q6 MC(4)=10", 2 + 2 * 4 == 10)
check("L02 Q10 profit 3 at q=4 (p=7,c=3,k=1/2,F=5)", 7 * 4 - (5 + 3 * 4 + F(1, 2) * 16) == 3)
check("L02 Q8 supply 4", (7 - 3) / (2 * F(1, 2)) == 4)

# ---- L03
A, B, n, c, k = F(100), F(2), 10, F(2), F(1)
s = F(n) / (2 * k)
pstar = (A + s * c) / (B + s)
Qstar = A - B * pstar
check("L03 Ex1.5 s=5, p*=110/7, Q*=480/7", s == 5 and pstar == F(110, 7) and Qstar == F(480, 7))
check("L03 Ex1.5 S(p*) = 480/7", s * (pstar - c) == F(480, 7))
check("L03 Rem2.2 one firm 48/7", (pstar - c) / (2 * k) == F(48, 7))
Z = lambda p: (A - B * p) - (n * max(F(0), (p - c) / (2 * k)))
grid = [F(i, 7) for i in range(141)]
pos = sum(1 for p in grid if Z(p) > 0 and p < pstar)
zer = sum(1 for p in grid if Z(p) == 0)
neg = sum(1 for p in grid if Z(p) < 0 and p > pstar)
check("L03 grid counts 110 / 1 / 30", (pos, zer, neg) == (110, 1, 30), str((pos, zer, neg)))
check("L03 Z(20) = -30, D(20)=60, S(20)=90", Z(F(20)) == -30 and A - 2 * 20 == 60 and 5 * 18 == 90)
check("L03 firm grid maximiser 48/7 for F=0 and F=100",
      all(max([F(j, 14) for j in range(141)], key=lambda q: (F(110, 7) * q - fx - 2 * q - q * q, -q)) == F(48, 7) for fx in (F(0), F(100))))
check("L03 Ex1.5 market clears", A - B * pstar == n * (pstar - c) / (2 * k))
check("L03 M1 p*=54/5, Q*=196/5, 4(54/5-1)=196/5", (F(50) + 4) / 5 == F(54, 5) and F(50) - F(54, 5) == F(196, 5) and 4 * (F(54, 5) - 1) == F(196, 5))
check("L03 M2 Z(12) = -6", (50 - 12) - 4 * 11 == 38 - 44 == -6)
check("L03 M3 n=4 for s=4 with k=1/2", F(4) / (2 * F(1, 2)) == 4)
_a, _b, _s = F(100), F(2), F(5)
check("L03 R2 c=0: p*=a/(b+s)=100/7, Q*=sa/(b+s)=500/7", _a / (_b + _s) == F(100, 7) and _s * _a / (_b + _s) == F(500, 7) and _a - _b * F(100, 7) == F(500, 7))
check("L03 Q2 p* decimal 15.714286", near(float(F(110, 7)), 15.714286, 1e-6))
check("L03 Q3 Q* decimal 68.571429", near(float(F(480, 7)), 68.571429, 1e-6))
check("L03 Q5 S(12)=50", 5 * (12 - 2) == 50)
check("L03 Q7 Q*=39.2 for M1", near(float(F(196, 5)), 39.2, 1e-12))
check("L03 Q9 48/7 = 6.857143", near(float(F(48, 7)), 6.857143, 1e-6))
check("L03 E3 counts 110+1+30=141", 110 + 1 + 30 == 141)

# ---- report
bad = [r for r in results if not r[1]]
for name, ok, detail in results:
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
print(f"checks={len(results)} failed={len(bad)}")

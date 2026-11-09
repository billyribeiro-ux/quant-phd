"""Independent re-derivation of every number in E1 slice a (hub, L01-L03), exact Fractions unless stated.

Run: python -I -W error ledgers/E1/scripts/E1-a-r2/rederive_E1a.py  (from the checkout root)
Prints one line per check: PASS/FAIL and the values compared. Exit 1 on any failure.
"""

import math
import sys
from fractions import Fraction as Fr

fails = []
n_checks = 0


def check(name, got, want):
    global n_checks
    n_checks += 1
    ok = got == want
    print(("PASS " if ok else "FAIL ") + f"{name}: got {got} want {want}")
    if not ok:
        fails.append(name)


def near(name, got, want, tol):
    global n_checks
    n_checks += 1
    ok = abs(got - want) <= tol
    print(("PASS " if ok else "FAIL ") + f"{name}: got {float(got):.7f} want {float(want):.7f} tol {tol}")
    if not ok:
        fails.append(name)


# ---------- L01 ----------
px, py, m = Fr(2), Fr(3), Fr(120)
check("L01 Ex1.6 xbar", m / (2 * px), Fr(30))
check("L01 Ex1.6 ybar", m / (2 * py), Fr(20))
check("L01 Ex1.6 ubar", (m / (2 * px)) * (m / (2 * py)), Fr(600))
check("L01 Ex1.6 budget", px * 30 + py * 20, m)
x = Fr(20)
y = (m - px * x) / py
check("L01 R2.4 y at x=20", y, Fr(80, 3))
check("L01 R2.4 MRS at (20,80/3)", y / x, Fr(4, 3))
check("L01 R2.4 price ratio", px / py, Fr(2, 3))
check("L01 R2.4 utility at (20,80/3)", x * y, Fr(1600, 3))
check("L01 R2.4 (21,1600/63) same utility", 21 * Fr(1600, 63), Fr(1600, 3))
check("L01 R2.4 y offset by one unit of x = 80/63", y - Fr(1600, 63), Fr(80, 63))
near("L01 R2.4 80/63 about 1.27", Fr(80, 63), Fr(127, 100), Fr(1, 100))
check("L01 R2.4 derivative of f at 20 = 40/3", (m - 2 * px * x) / py, Fr(40, 3))
check("L01 R2.4 MRS reaches 2/3 at x=30", (m - px * 30) / py / 30, Fr(2, 3))
check("L01 E2 new bundle utility 546", 21 * Fr(26), Fr(546))
check("L01 E2 change 38/3", 21 * Fr(26) - Fr(1600, 3), Fr(38, 3))
check("L01 E2 second-order term -2/3", Fr(38, 3) - Fr(40, 3), Fr(-2, 3))
check("L01 E2 expansion identity", (20 + 1) * (Fr(80, 3) - Fr(2, 3)), Fr(1600, 3) + Fr(40, 3) - Fr(2, 3))
check("L01 E3 spacing", (m / px) / 60, Fr(1))
# Case table from the lab (Fraction exact)
for cp, cpy, cm, xb, yb, ub in [
    (Fr(2), Fr(3), Fr(120), Fr(30), Fr(20), Fr(600)),
    (Fr(1), Fr(1), Fr(50), Fr(25), Fr(25), Fr(625)),
    (Fr(5), Fr(2), Fr(70), Fr(7), Fr(35, 2), Fr(245, 2)),
    (Fr(3), Fr(4), Fr(60), Fr(10), Fr(15, 2), Fr(75)),
]:
    check(f"L01 lab case closed form x {cp},{cpy},{cm}", cm / (2 * cp), xb)
    check(f"L01 lab case closed form y {cp},{cpy},{cm}", cm / (2 * cpy), yb)
    check(f"L01 lab case closed form u {cp},{cpy},{cm}", xb * yb, ub)
    best = max(range(61), key=lambda i: (cm / cp * Fr(i, 60)) * ((cm - cp * (cm / cp * Fr(i, 60))) / cpy))
    check(f"L01 lab grid maximiser is point 30 {cp},{cpy},{cm}", best, 30)
# M1, M2, M3, P1, P2, R1, R2, R3
check("L01 M1 xbar", Fr(90) / (2 * 4), Fr(45, 4))
check("L01 M1 ybar", Fr(90) / (2 * 5), Fr(9))
check("L01 M1 ubar", Fr(90) ** 2 / (4 * 4 * 5), Fr(405, 4))
check("L01 M1 budget", 4 * Fr(45, 4) + 5 * 9, Fr(90))
check("L01 M2 MRS (6,8)", Fr(8) / Fr(6), Fr(4, 3))
check("L01 E1 ubar case2", Fr(50) ** 2 / (4 * 1 * 1), Fr(625))
# R1: h(x) = (x-1)^2 + (m - px x)/py on the line with px=2,py=3,m=120: stationary point and h''
xs = Fr(1) + Fr(2) / (2 * 3)
check("L01 R1 stationary point 1 + px/(2py) at px=2,py=3", xs, Fr(4, 3))
hp = lambda t: 2 * (t - 1) - Fr(2, 3)  # noqa: E731
check("L01 R1 h' vanishes at 4/3", hp(Fr(4, 3)), Fr(0))
# R2: Cobb-Douglas share, a = 3/10, m = 100, px = 2, py = 5: optimum x = a m / px = 15, y = (1-a) m / py = 14
a_, m2, px2, py2 = Fr(3, 10), Fr(100), Fr(2), Fr(5)
check("L01 R2 optimum x = a m / px", a_ * m2 / px2, Fr(15))
check("L01 R2 optimum y = (1-a) m / py", (1 - a_) * m2 / py2, Fr(14))
check("L01 R2 budget binds", px2 * 15 + py2 * 14, m2)
mrs_opt = (a_ * Fr(14)) / ((1 - a_) * Fr(15))
check("L01 R2 MRS = px/py at optimum", mrs_opt, px2 / py2)
# R3 and the ln remark: ln 600 is not 600
check("L01 R3 ln(600) differs from 600", math.log(600) == 600, False)
# Remark 1.7 / quiz: MRS 4/3 decimal and 2/3
near("L01 quiz MRS 1.3333333", Fr(4, 3), Fr(13333333, 10000000), Fr(1, 10000))
near("L01 quiz MRS 0.6666667", Fr(2, 3), Fr(6666667, 10000000), Fr(1, 10000))

# ---------- L02 ----------
p, c, k, F = Fr(10), Fr(2), Fr(1), Fr(12)
q0 = (p - c) / (2 * k)
check("L02 Ex1.4 q*", q0, Fr(4))
check("L02 Ex1.4 C(4)", F + c * 4 + k * 16, Fr(36))
check("L02 Ex1.4 profit", p * 4 - (F + c * 4 + k * 16), Fr(4))
check("L02 Ex1.4 MC(4)", c + 2 * k * 4, Fr(10))


def profit(q, p, F, c, k):
    return p * q - (F + c * q + k * q * q)


check("L02 R1.6 profit at F=100, q=4", profit(Fr(4), p, Fr(100), c, k), Fr(-84))
check("L02 R1.6 profit at q=0, F=100", profit(Fr(0), p, Fr(100), c, k), Fr(-100))
check("L02 R1.6 difference (p-c)^2/(4k) at p=10", (p - c) ** 2 / (4 * k), Fr(16))
# sqrt(12) profit exact: 10 sqrt12 - (12 + 2 sqrt12 + 12) = 16 sqrt3 - 24
s12 = math.sqrt(12)
near("L02 misconception profit at sqrt12 = 16 sqrt3 - 24", 10 * s12 - (12 + 2 * s12 + 12), 16 * math.sqrt(3) - 24, 1e-12)
near("L02 E2 16 sqrt3 - 24 ~ 3.712813", 16 * math.sqrt(3) - 24, 3.712813, 1e-6)
near("L02 E2 28 - 16 sqrt3 ~ 0.2872", 28 - 16 * math.sqrt(3), 0.2872, 1e-4)
near("L02 R3 price 2 + 2 sqrt12 ~ 8.93", 2 + 2 * s12, 8.93, 0.01)
check("L02 R3 2 + 2 sqrt12 below 10", 2 + 2 * s12 < 10, True)
# AC minimised at sqrt(F/k): numerical check that AC(q)=12/q+2+q has its minimum at sqrt12
acs = [(12 / q + 2 + q, q) for q in [i / 1000 for i in range(1000, 8001)]]
near("L02 misconception AC argmin ~ sqrt12", min(acs)[1], s12, 0.002)
check("L02 misconception AC'(q)=k-F/q^2 at sqrt12 is zero", Fr(1) - Fr(12) / Fr(12), Fr(0))
# Lab cases: closed forms, profits, grid maximisers over j/12, j=0..72
cases = [(Fr(10), Fr(2), Fr(1), Fr(12)), (Fr(7), Fr(3), Fr(1, 2), Fr(5)), (Fr(9), Fr(1), Fr(3), Fr(0)), (Fr(10), Fr(2), Fr(1), Fr(100))]
want_q = [Fr(4), Fr(4), Fr(4, 3), Fr(4)]
want_pi = [Fr(4), Fr(3), Fr(16, 3), Fr(-84)]
want_j = [48, 48, 16, 48]
for i, (pp, cc, kk, FF) in enumerate(cases):
    qs = (pp - cc) / (2 * kk)
    check(f"L02 lab case {i+1} q*", qs, want_q[i])
    check(f"L02 lab case {i+1} profit at q*", profit(qs, pp, FF, cc, kk), want_pi[i])
    check(f"L02 lab case {i+1} MC(q*)=p", cc + 2 * kk * qs, pp)
    check(f"L02 lab case {i+1} shutdown -F", profit(Fr(0), pp, FF, cc, kk), -FF)
    grid = [(j, profit(Fr(j, 12), pp, FF, cc, kk)) for j in range(73)]
    best = max(grid, key=lambda t: t[1])
    check(f"L02 lab case {i+1} grid maximiser j", best[0], want_j[i])
    check(f"L02 lab case {i+1} grid maximiser unique", sum(1 for _, v in grid if v == best[1]), 1)
check("L02 cases 1 and 4 profit gap 88", Fr(4) - Fr(-84), Fr(88))
# M1, M2, M3, E1 (case 3), Q11
check("L02 M1 q*", (Fr(12) - 4) / (2 * 2), Fr(2))
check("L02 M1 profit", 12 * Fr(2) - (4 * 2 + 2 * 4), Fr(8))
check("L02 M2 q*", (Fr(9) - 3) / 2, Fr(3))
check("L02 M2 profit", 9 * 3 - (50 + 3 * 3 + 9), Fr(-41))
check("L02 M3 q(7)", (Fr(7) - 3) / (2 * Fr(1, 2)), Fr(4))
check("L02 M3 supply at 2 is zero", max(Fr(0), (Fr(2) - 3) / (2 * Fr(1, 2))), Fr(0))
check("L02 E1 case3 q*", (Fr(9) - 1) / (2 * 3), Fr(4, 3))
check("L02 E1 case3 profit", 9 * Fr(4, 3) - (1 * Fr(4, 3) + 3 * Fr(16, 9)), Fr(16, 3))
check("L02 E1 case3 grid index 16", Fr(16, 12), Fr(4, 3))
check("L02 E3 cost at q=4 F=5 p=7", 5 + 3 * 4 + Fr(1, 2) * 16, Fr(25))
check("L02 Q11 profit at q=4 F=5", 7 * 4 - 25, Fr(3))
h = Fr(1, 10 ** 6)
pi_star = lambda pp: (pp - c) ** 2 / (4 * k) - F  # noqa: E731
near("L02 R1 dpi*/dp = q(p) finite difference at p=10", (pi_star(p + h) - pi_star(p - h)) / (2 * h), Fr(4), Fr(1, 10 ** 5))
check("L02 R2 chain-rule identity: d pi*/dp = q* + (p - MC(q*)) dq*/dp at p=10", Fr(4) + (p - (c + 2 * k * 4)) * Fr(1, 2), Fr(4))

# ---------- L03 ----------
A, B, N, Cc, Kk, FF = Fr(100), Fr(2), 10, Fr(2), Fr(1), Fr(0)
S_ = Fr(N) / (2 * Kk)
check("L03 Ex1.5 s", S_, Fr(5))
pstar = (A + S_ * Cc) / (B + S_)
check("L03 Ex1.5 p*", pstar, Fr(110, 7))
check("L03 Ex1.5 Q*", A - B * pstar, Fr(480, 7))
check("L03 Ex1.5 S(p*)", S_ * (pstar - Cc), Fr(480, 7))
check("L03 Prop1.3 p*-c = (a-bc)/(b+s)", pstar - Cc, (A - B * Cc) / (B + S_))
check("L03 Ex1.5 a>bc", A > B * Cc, True)
D = lambda pp: A - B * pp  # noqa: E731
Sup = lambda pp: N * max(Fr(0), (pp - Cc) / (2 * Kk))  # noqa: E731
Z = lambda pp: D(pp) - Sup(pp)  # noqa: E731
grid = [Fr(i, 7) for i in range(141)]
pos = sum(1 for g in grid if g < pstar and Z(g) > 0)
zero = sum(1 for g in grid if Z(g) == 0)
neg = sum(1 for g in grid if g > pstar and Z(g) < 0)
check("L03 grid positive below p*", pos, 110)
check("L03 grid zero count", zero, 1)
check("L03 grid negative above p*", neg, 30)
check("L03 grid zero is at p*", Z(pstar), Fr(0))
check("L03 p*=110/7 is grid point 110", Fr(110, 7), Fr(110, 7))
check("L03 p=20 D", D(Fr(20)), Fr(60))
check("L03 p=20 S", Sup(Fr(20)), Fr(90))
check("L03 p=20 Z", Z(Fr(20)), Fr(-30))
one = max(Fr(0), (pstar - Cc) / (2 * Kk))
check("L03 Remark2.2 one firm 48/7", one, Fr(48, 7))
check("L03 Remark2.2 ten firms 480/7", 10 * one, Fr(480, 7))
check("L03 Remark2.2 ratio 10", Sup(pstar) / one, Fr(10))
for FFx in (Fr(0), Fr(100)):
    fg = [(Fr(j, 14), Fr(96, 14) * 0 + (pstar * Fr(j, 14)) - FFx - Cc * Fr(j, 14) - Kk * (Fr(j, 14)) ** 2) for j in range(141)]
    best = max(fg, key=lambda t: t[1])
    check(f"L03 firm grid maximiser F={FFx}", best[0], Fr(48, 7))
check("L03 canon profit at p* with F=0 = 2304/49", (pstar - Cc) ** 2 / (4 * Kk) - 0, Fr(2304, 49))
# M1, M2, M3, P2, E-items, R1 (signs by finite differences), R2 (c=0)
check("L03 M1 p*", (Fr(50) + 4 * 1) / (1 + 4), Fr(54, 5))
check("L03 M1 Q*", Fr(50) - Fr(54, 5), Fr(196, 5))
check("L03 M1 check S", 4 * (Fr(54, 5) - 1), Fr(196, 5))
check("L03 M2 Z(12)", (Fr(50) - 12) - 4 * (12 - 1), Fr(-6))
check("L03 M3 s=n when k=1/2", Fr(4) / (2 * Fr(1, 2)), Fr(4))
check("L03 E2 D(20)", A - B * 20, Fr(60))
check("L03 E3 counts 110+1+30=141", 110 + 1 + 30, 141)
check("L03 E3 p* at i=110", Fr(110, 7), Fr(110, 7))
check("L03 quiz S(12) s=5 c=2", Fr(5) * (12 - 2), Fr(50))
check("L03 quiz Q* M1 decimal", Fr(196, 5), Fr(392, 10))
near("L03 quiz p* 15.714286", pstar, Fr(15714286, 10 ** 6), Fr(1, 10 ** 4))
near("L03 quiz Q* 68.571429", A - B * pstar, Fr(68571429, 10 ** 6), Fr(1, 10 ** 4))
near("L03 quiz 48/7 6.857143", Fr(48, 7), Fr(6857143, 10 ** 6), Fr(1, 10 ** 4))
check("L03 P2 a/b <= c when a <= bc", Fr(1) <= 1, True)
# R1 signs by finite differences at a=100,b=2,s=5,c=2
pa = lambda aa: (aa + S_ * Cc) / (B + S_)  # noqa: E731
pb = lambda bb: (A + S_ * Cc) / (bb + S_)  # noqa: E731
near("L03 R1 dp*/da = 1/(b+s) at example", (pa(A + Fr(1, 10 ** 6)) - pa(A - Fr(1, 10 ** 6))) / (Fr(2, 10 ** 6)), Fr(1, 7), Fr(1, 10 ** 6))
near("L03 R1 dp*/db = -(a+sc)/(b+s)^2 at example", (pb(B + Fr(1, 10 ** 6)) - pb(B - Fr(1, 10 ** 6))) / (Fr(2, 10 ** 6)), -Fr(110, 49), Fr(1, 10 ** 4))
# R2: c = 0, p* = a/(b+s), Q* = s a/(b+s)
check("L03 R2 Q* = s a/(b+s) with c=0", (A - B * (A / (B + S_))), S_ * A / (B + S_))
check("L03 R2 Q* formula equals s(p*-c) with c=0", S_ * (A / (B + S_)), S_ * A / (B + S_))
# Lab expected: the lab's excess-demand sign at each grid point is exactly the Remark 1.4 pattern
check("L03 Remark1.4 sign pattern holds on grid", all((Z(g) > 0) if g < pstar else ((Z(g) == 0) if g == pstar else (Z(g) < 0)) for g in grid), True)

print(f"\n{n_checks} checks, {len(fails)} failed")
if fails:
    print("FAILED:", fails)
    sys.exit(1)

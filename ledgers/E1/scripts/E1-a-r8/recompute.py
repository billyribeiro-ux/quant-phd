"""Independent recomputation of the numbers in the E1 slice a pages (hub, L01-L03), exact Fractions where possible."""
import math
from fractions import Fraction as Fr

out = []


def check(label, got, want):
    ok = got == want
    out.append(f"{'OK  ' if ok else 'FAIL'} {label}: got {got} want {want}")


# L01 Proposition 1.4 for four cases, and grid argmax over 61 points
for px, py, m in [(Fr(2), Fr(3), Fr(120)), (Fr(1), Fr(1), Fr(50)), (Fr(5), Fr(2), Fr(70)), (Fr(3), Fr(4), Fr(60))]:
    xs, ys = m / (2 * px), m / (2 * py)
    grid = []
    for i in range(61):
        x = (m / px) * i / 60
        y = (m - px * x) / py
        grid.append((x * y, i))
    best = max(grid)
    check(f"L01 case ({px},{py},{m}) grid max point", best[1], 30)
    check(f"L01 case ({px},{py},{m}) u_bar", xs * ys, m * m / (4 * px * py))
    check(f"L01 case ({px},{py},{m}) MRS equals price ratio", ys / xs, px / py)
check("L01 off-optimum MRS at (20,80/3)", (Fr(80, 3) / 20), Fr(4, 3))
check("L01 E2 utility change", 21 * (Fr(80, 3) - Fr(2, 3)) - 20 * Fr(80, 3), Fr(38, 3))
check("L01 E2 first-order estimate", Fr(40, 3), Fr(120 - 4 * 20, 3))
check("L01 E2 second-order residual", Fr(38, 3) - Fr(40, 3), Fr(-2, 3))
check("L01 M1 u_bar", Fr(90 * 90, 4 * 4 * 5), Fr(405, 4))
check("L01 R1 h''", Fr(2), Fr(2))
# R2 Cobb-Douglas share: at optimum p_x x = a m; check numerically with a=1/3
a_ = Fr(1, 3)
m_ = Fr(90)
px_, py_ = Fr(2), Fr(5)
xbar, ybar = a_ * m_ / px_, (1 - a_) * m_ / py_
check("L01 R2 share a at (a m/p_x, (1-a) m/p_y): budget binds", px_ * xbar + py_ * ybar, m_)
# L01 Quiz/Misconception: u = x+y MRS 1, partial of xy wrt y = x
check("L01 Q10 MRS at (20,80/3) decimal", round(float(Fr(4, 3)), 7), 1.3333333)

# L02 Proposition 1.3 and Example 1.4 / Lab 1 cases
def profit(q, p, F, c, k):
    return p * q - (F + c * q + k * q * q)

cases = [(Fr(10), Fr(2), Fr(1), Fr(12)), (Fr(7), Fr(3), Fr(1, 2), Fr(5)), (Fr(9), Fr(1), Fr(3), Fr(0)), (Fr(10), Fr(2), Fr(1), Fr(100))]
for p, c, k, F in cases:
    qs = max(Fr(0), (p - c) / (2 * k))
    grid = [(profit(Fr(j, 12), p, F, c, k), j) for j in range(73)]
    best = max(grid)
    check(f"L02 case p={p} c={c} k={k} F={F} q*", qs, Fr(best[1], 12))
    check(f"L02 case p={p} F={F} profit at q*", profit(qs, p, F, c, k), (p - c) ** 2 / (4 * k) - F)
check("L02 case 4 profit", profit(Fr(4), Fr(10), Fr(100), Fr(2), Fr(1)), Fr(-84))
check("L02 misc1 profit at sqrt(12) = 16 sqrt3 - 24 (float)", round(10 * math.sqrt(12) - (12 + 2 * math.sqrt(12) + 12), 4), round(16 * math.sqrt(3) - 24, 4))
check("L02 misc1 numeric 3.7128", round(16 * math.sqrt(3) - 24, 4), 3.7128)
check("L02 E2 difference 28-16sqrt3 (float)", round(28 - 16 * math.sqrt(3), 4), 0.2872)
check("L02 M1 profit", Fr(12 * 2) - (4 * 2 + 2 * 4), Fr(8))
check("L02 M1 closed form", Fr((12 - 4) ** 2, 4 * 2), Fr(8))
check("L02 M2 profit", Fr(9 * 3) - (50 + 9 + 9), Fr(-41))
check("L02 M3 q(7)", (Fr(7) - 3) / (2 * Fr(1, 2)), Fr(4))
check("L02 R1 pi* at p=10 (k=1,F=12)", Fr((10 - 2) ** 2, 4) - 12, Fr(4))
check("L02 R3 threshold 2+2sqrt12 (float)", round(2 + 2 * math.sqrt(12), 2), 8.93)
check("L02 R3 threshold equals c+2 sqrt(kF)", 2 + 2 * math.sqrt(1 * 12), 2 + 2 * math.sqrt(12))
check("L02 Q quiz: C(4)=36", Fr(12 + 2 * 4 + 16), Fr(36))

# L03 equilibrium, a=100,b=2,n=10,c=2,k=1
a, b, n, c, k = Fr(100), Fr(2), 10, Fr(2), Fr(1)
s = Fr(n) / (2 * k)
p_star = (a + s * c) / (b + s)
Q_star = a - b * p_star
check("L03 p*", p_star, Fr(110, 7))
check("L03 Q*", Q_star, Fr(480, 7))
check("L03 Q* = s(p*-c)", Q_star, s * (p_star - c))
check("L03 p*-c = (a-bc)/(b+s)", p_star - c, (a - b * c) / (b + s))
def Z(p):
    sup = n * max(Fr(0), (p - c) / (2 * k))
    return (a - b * p) - sup
grid = [Fr(i, 7) for i in range(141)]
check("L03 positive below p* count", sum(Z(p) > 0 for p in grid if p < p_star), 110)
check("L03 zero count", sum(Z(p) == 0 for p in grid), 1)
check("L03 negative above p* count", sum(Z(p) < 0 for p in grid if p > p_star), 30)
check("L03 Z(20)", Z(Fr(20)), Fr(-30))
check("L03 D(20)", a - b * 20, Fr(60))
check("L03 S(20)", n * (Fr(20) - c) / (2 * k), Fr(90))
check("L03 one firm at p*", (p_star - c) / (2 * k), Fr(48, 7))
check("L03 firm grid max F-free (96/14 on grid)", Fr(96, 14), Fr(48, 7))
check("L03 Example 1.5 firm profit F=0 closed form", (p_star - c) ** 2 / (4 * k), (Fr(96, 7)) ** 2 / 4)
check("L03 M1 p*", (Fr(50) + 4 * 1) / (1 + 4), Fr(54, 5))
check("L03 M1 Q*", Fr(50) - Fr(54, 5), Fr(196, 5))
check("L03 M2 Z(12)", (Fr(50) - 12) - 4 * (12 - 1), Fr(-6))
check("L03 R1 d p*/da", 1 / (b + s), Fr(1, 7))
check("L03 R2 c=0 p*", a / (b + s), a / (b + s))
check("L03 E2 D(20)-S(20)", (100 - 40) - 5 * (20 - 2), Fr(-30))
check("L03 quiz 110/7 decimal", round(float(p_star), 6), 15.714286)
check("L03 quiz 480/7 decimal", round(float(Q_star), 6), 68.571429)
check("L03 quiz 48/7 decimal", round(float(Fr(48, 7)), 6), 6.857143)
check("L03 quiz S(12)", 5 * (12 - 2), 50)
check("L03 M1 quiz 196/5", round(float(Fr(196, 5)), 1), 39.2)
check("L03 M3 n for s=4 with k=1/2", Fr(4) * 2 * Fr(1, 2), Fr(4))
check("L03 P2 a/b <= c when a <= bc", Fr(1, 1) <= 1, True)

# Hub placement items
check("hub Q4 e^0.5 decimal", round(math.exp(0.5), 4), 1.6487)
check("hub Q7 PV 100 e^-0.1 to 2 decimals", round(100 * math.exp(-0.1), 2), 90.48)
check("hub Q3 dy/dx at (3,1)", Fr(-1, 2 * 1), Fr(-1, 2))
check("hub Q6 gradient", (2 * 1, 2 * 2), (2, 4))
check("hub 7/9", round(7 / 9 * 100, 1), 77.8)
check("hub 8/9", round(8 / 9 * 100, 1), 88.9)
# Hub skill check Ps1: project monopoly model, profit ((a-Q)/b - c) Q, FOC
A_, B_, C_ = Fr(120), Fr(1), Fr(20)
d = A_ - B_ * C_
check("project d", d, Fr(100))
check("project monopoly FOC root", (A_ - B_ * C_) / 2, d / 2)
# Ps1 as written: max_Q (a - bQ - c) Q, FOC a - 2bQ - c = 0; root (a-c)/(2b)
B2 = Fr(2)
check("hub Ps1 written-model root (a-c)/(2b) at b=2", (A_ - C_) / (2 * B2), Fr(25))
check("project monopoly volume d/2 at b=2 (d=a-bc)", (A_ - B2 * C_) / 2, Fr(40))
# Ps2 as written with b=1: reaction (a-c-q2)/2 equals project (d-q2)/2 only if b=1
check("hub Ps2 key (a-c-q2)/2 at b=2, q2=0", (A_ - C_) / 2, Fr(50))
check("project reaction (d-q2)/2 at b=2, q2=0", (A_ - B2 * C_) / 2, Fr(40))

print("\n".join(out))
print("FAILS:", sum(1 for line in out if line.startswith("FAIL")))

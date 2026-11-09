"""Independent re-derivation of every number in slice a (hub, L01-L03) with exact Fractions and float checks (verifier r3)."""
import math
from fractions import Fraction as Fr

ok = []
def check(name, cond):
    ok.append(cond)
    print(("PASS " if cond else "FAIL ") + name)

# hub placement arithmetic
check("7/9 = 77.8 %", round(7 / 9 * 100, 1) == 77.8)
check("8/9 = 88.9 %", round(8 / 9 * 100, 1) == 88.9)
check("0.8*9 = 7.2 so 8 items needed", math.ceil(0.8 * 9) == 8)
check("e^0.5 to 4 dp = 1.6487 within 5e-5", abs(math.exp(0.5) - 1.6487) < 5e-5)
check("100 e^-0.1 to 2 dp = 90.48 within 0.005", abs(100 * math.exp(-0.1) - 90.48) < 0.005)
check("d/dx of y^2+x=4 at (3,1) = -1/2", Fr(-1, 2) == -Fr(1, 2 * 1))
a, b, c = Fr(120), Fr(3), Fr(7)
Q = Fr(5)
h = Fr(1, 10**9)
f = lambda Q_: ((a - Q_) / b - c) * Q_
check("monopoly FOC numeric derivative matches (a-bc-2Q)/b", abs(float((f(Q + h) - f(Q)) / h) - float((a - b * c - 2 * Q) / b)) < 1e-6)
x1, x2, cc, aa, bb = Fr(3), Fr(4), Fr(2), Fr(120), Fr(1)
g = lambda q1: ((aa - q1 - x2) / bb - cc) * q1
q1 = Fr(7)
check("Cournot FOC numeric derivative matches (a-2q1-q2-bc)/b", abs(float((g(q1 + h) - g(q1)) / h) - float((aa - 2 * q1 - x2 - bb * cc) / bb)) < 1e-6)
check("Cournot best response (a-bc-q2)/2 at q2=4", (aa - bb * cc - x2) / 2 == Fr(114, 2))

# L01
def cf(px, py, m):
    return m / (2 * px), m / (2 * py), m * m / (4 * px * py)
check("L01 Example 1.6 closed form 30, 20, 600", cf(Fr(2), Fr(3), Fr(120)) == (30, 20, 600))
check("L01 case 2 closed form 25, 25, 625", cf(Fr(1), Fr(1), Fr(50)) == (25, 25, 625))
check("L01 case 3 closed form 7, 35/2, 245/2", cf(Fr(5), Fr(2), Fr(70)) == (7, Fr(35, 2), Fr(245, 2)))
check("L01 case 4 closed form 10, 15/2, 75", cf(Fr(3), Fr(4), Fr(60)) == (10, Fr(15, 2), 75))
x = Fr(20); y = (Fr(120) - 2 * x) / 3
check("Remark 2.4: y at x=20 is 80/3", y == Fr(80, 3))
check("Remark 2.4: MRS = 4/3", y / x == Fr(4, 3))
check("Remark 2.4: 80/63 offset", Fr(80, 3) - Fr(1600, 63) == Fr(80, 63))
check("Remark 2.4: 21*1600/63 = 1600/3", 21 * Fr(1600, 63) == Fr(1600, 3))
check("Remark 2.4: utility change for +1 x, -2/3 y is 38/3", 21 * 26 - 20 * Fr(80, 3) == Fr(38, 3))
check("Remark 2.4: f'(20) = 40/3", (Fr(120) - 4 * 20) / 3 == Fr(40, 3))
check("E2: first-order estimate 40/3 and difference -2/3", Fr(40, 3) - Fr(38, 3) == Fr(2, 3))
dx = Fr(1)
check("E2 expansion at dx=1 equals exact", (20 + dx) * (Fr(80, 3) - 2 * dx / 3) == Fr(1600, 3) + 40 * dx / 3 - 2 * dx * dx / 3)
check("M1 closed form 45/4, 9, 405/4", cf(Fr(4), Fr(5), Fr(90)) == (Fr(45, 4), 9, Fr(405, 4)))
check("M2 MRS 4/3", Fr(8, 6) == Fr(4, 3))
check("L01 grid spacing 1, midpoint 30", Fr(60) / 60 == 1 and 30 == 60 // 2)

# R1 (L01): h(x) = (x-1)^2 + (m - px x)/py
px_, py_, m_ = Fr(2), Fr(3), Fr(120)
hh = lambda t: (t - 1) ** 2 + (m_ - px_ * t) / py_
x1s = 1 + px_ / (2 * py_)
d = float((hh(x1s + h) - hh(x1s - h)) / (2 * h))
check("L01 R1 stationary point gives h'=0", abs(d) < 1e-6)
check("L01 R1 second derivative 2", abs(float((hh(x1s + h) - 2 * hh(x1s) + hh(x1s - h)) / h / h) - 2) < 1e-3)
# R2 (L01): Cobb-Douglas share, check spend share numerically
aa2 = Fr(3, 10); m2 = Fr(100); px2 = Fr(2); py2 = Fr(5)
xs2 = aa2 * m2 / px2; ys2 = (1 - aa2) * m2 / py2
check("L01 R2 optimum spends share a on x (x=15, y=14)", xs2 == 15 and ys2 == 14)
mrs2 = (aa2 * ys2) / ((1 - aa2) * xs2)
check("L01 R2 MRS equals price ratio at that bundle", mrs2 == px2 / py2)
# R3 (L01): ln
check("L01 R3 ln(600) approx 6.3969", abs(math.log(600) - 6.3969) < 1e-4)

# L02
C = lambda q, F, c_, k: F + c_ * q + k * q * q
pi = lambda q, p, F, c_, k: p * q - C(q, F, c_, k)
check("L02 Example 1.4: q*=4, C(4)=36, profit 4", (Fr(10) - 2) / 2 == 4 and C(Fr(4), 12, 2, 1) == 36 and pi(Fr(4), 10, 12, 2, 1) == 4)
check("L02 Example 1.4: MC(4)=10", 2 + 2 * 4 == 10)
check("L02 Remark 1.6: F=100 profit at q*=4 is -84", pi(Fr(4), 10, 100, 2, 1) == -84)
check("L02 case 2: q*=4, profit 3", pi(Fr(4), 7, 5, 3, Fr(1, 2)) == 3)
check("L02 case 3: q*=4/3, profit 16/3", pi(Fr(4, 3), 9, 0, 1, 3) == Fr(16, 3))
check("L02 case 3 grid index 16 = 4/3 * 12", Fr(4, 3) * 12 == 16)
check("L02 M1: C=4q+2q^2, p=12: q*=2 profit 8", pi(Fr(2), 12, 0, 4, 2) == 8 and (12 - 4) / (2 * 2) == 2)
check("L02 M2: C=50+3q+q^2, p=9: q*=3 profit -41, shutdown -50", pi(Fr(3), 9, 50, 3, 1) == -41 and pi(Fr(0), 9, 50, 3, 1) == -50)
check("L02 M3: q(7)=4, q(2)=0", (7 - 3) / (2 * Fr(1, 2)) == 4 and max(Fr(0), (2 - 3) / 1) == 0)
# grid argmax over j/12, j=0..72 for the four cases, exact
cases = [(10, 2, 1, 12), (7, 3, Fr(1, 2), 5), (9, 1, 3, 0), (10, 2, 1, 100)]
for n, (p, c_, k, F) in enumerate(cases, 1):
    best = max(range(73), key=lambda j: (pi(Fr(j, 12), p, F, c_, k), -j))
    qs = Fr(p - c_) / (2 * k)
    check(f"L02 case {n} grid maximiser equals closed form", Fr(best, 12) == qs)
# AC argmin and profits at sqrt(12)
q_ac = math.sqrt(12)
ac = lambda q: 12 / q + 2 + q
grid_ac = min((ac(1 + i * 0.001), 1 + i * 0.001) for i in range(7001))
check("AC argmin on [1,8] within 0.002 of sqrt12", abs(grid_ac[1] - q_ac) < 0.002)
pi_root = 10 * q_ac - (12 + 2 * q_ac + q_ac ** 2)
check("profit at sqrt12 = 3.7128 to 4 dp", f"{pi_root:.4f}" == "3.7128")
check("16 sqrt3 - 24 = profit at sqrt12", abs(16 * math.sqrt(3) - 24 - pi_root) < 1e-12)
check("8 sqrt12 - 24 = 16 sqrt3 - 24", abs(8 * math.sqrt(12) - 24 - (16 * math.sqrt(3) - 24)) < 1e-12)
check("28 - 16 sqrt3 approx 0.2872", f"{28 - 16 * math.sqrt(3):.4f}" == "0.2872")
check("2 + 2 sqrt12 approx 8.93 < 10", f"{2 + 2 * math.sqrt(12):.2f}" == "8.93" and 2 + 2 * math.sqrt(12) < 10)
check("R3 threshold: profit at p=c+2sqrt(kF) equals 0", abs((2 * math.sqrt(12)) ** 2 / 4 - 12) < 1e-9)
check("L02 misconception AC'(q)=k-F/q^2 zero at sqrt(F/k)", abs(1 - 12 / 12) < 1e-12)
check("L02 shutdown: pi(q*) >= -F at p=10,F=100", pi(Fr(4), 10, 100, 2, 1) >= -100)
# R1 (L02): d pi*/dp = q(p) numerically for p=9, c=2, k=1
pstar = lambda p: (p - 2) ** 2 / 4 - 12
dd = (pstar(9 + 1e-6) - pstar(9 - 1e-6)) / 2e-6
check("L02 R1 envelope derivative equals q(9) = 7/2", abs(dd - 3.5) < 1e-6)
# P1 / P3 (L02) quick checks
check("L02 P2: pi(q+1)-pi(q) = p-c for k=0", pi(Fr(3) + 1, 5, 2, 1, 0) - pi(Fr(3), 5, 2, 1, 0) == 5 - 1)

# L03
A_, B_, n_, c3, k3 = Fr(100), Fr(2), 10, Fr(2), Fr(1)
s3 = Fr(n_) / (2 * k3)
p3 = (A_ + s3 * c3) / (B_ + s3)
Qs = A_ - B_ * p3
check("L03 p*=110/7, Q*=480/7", p3 == Fr(110, 7) and Qs == Fr(480, 7))
check("L03 S(p*) = s(p*-c) = 480/7", s3 * (p3 - c3) == Fr(480, 7))
check("L03 p*-c = (a-bc)/(b+s)", p3 - c3 == (A_ - B_ * c3) / (B_ + s3))
S3 = lambda p: n_ * max(Fr(0), (p - c3) / (2 * k3))
Z3 = lambda p: (A_ - B_ * p) - S3(p)
grid = [Fr(i, 7) for i in range(141)]
pos = sum(1 for p in grid if p < p3 and Z3(p) > 0)
zer = sum(1 for p in grid if Z3(p) == 0)
neg = sum(1 for p in grid if p > p3 and Z3(p) < 0)
check(f"L03 grid counts 110/1/30 (got {pos}/{zer}/{neg})", (pos, zer, neg) == (110, 1, 30))
check("L03 Z(20)=-30, D=60, S=90", Z3(Fr(20)) == -30 and A_ - B_ * 20 == 60 and S3(Fr(20)) == 90)
check("L03 one-firm supply 48/7, ratio 10", (p3 - c3) / 2 == Fr(48, 7) and S3(p3) / ((p3 - c3) / 2) == 10)
check("L03 Remark 2.2: 10 * 48/7 = 480/7", 10 * Fr(48, 7) == Fr(480, 7))
# firm grid j/14 maximiser for F=0 and F=100
for F_ in (0, 100):
    best = max(range(141), key=lambda j: (pi(Fr(j, 14), p3, F_, c3, k3), -j))
    check(f"L03 firm grid maximiser F={F_} = 48/7", Fr(best, 14) == Fr(48, 7))
check("L03 canon: profit at p* with F=0 is (p*-c)^2/(4k) = 2304/49", (p3 - c3) ** 2 / 4 == Fr(2304, 49))
# R1 (L03) signs by finite difference
pf = lambda a_, b_: (a_ + s3 * c3) / (b_ + s3)
dpa = (pf(A_ + h, B_) - pf(A_, B_)) / h
dpb = (pf(A_, B_ + h) - pf(A_, B_)) / h
check("L03 R1 dp*/da = 1/(b+s) = 1/7", abs(float(dpa) - 1 / 7) < 1e-6)
check("L03 R1 dp*/db = -(a+sc)/(b+s)^2 = -110/49", abs(float(dpb) + 110 / 49) < 1e-6)
# R2 (L03) c=0
s0 = Fr(5); a0 = Fr(100); b0 = Fr(2)
check("L03 R2 c=0 closed form", (a0 / (b0 + s0), s0 * a0 / (b0 + s0)) == (Fr(100, 7), Fr(500, 7)))
# M1 (L03)
check("L03 M1 p*=54/5, Q*=196/5", (Fr(50) + 4) / 5 == Fr(54, 5) and 50 - Fr(54, 5) == Fr(196, 5))
check("L03 M1 check 4(54/5-1)=196/5", 4 * (Fr(54, 5) - 1) == Fr(196, 5))
check("L03 M2 Z(12)=-6", (50 - 12) - 4 * (12 - 1) == -6)
check("L03 Example 1.5 decimals", f"{float(Fr(110,7)):.6f}" == "15.714286" and f"{float(Fr(480,7)):.6f}" == "68.571429" and f"{float(Fr(48,7)):.6f}" == "6.857143")
check("L03 quiz S(12)=50 with s=5,c=2", 5 * (12 - 2) == 50)
check("L03 quiz Q* decimal M1 39.2", float(Fr(196, 5)) == 39.2)
print("ALL PASS" if all(ok) else "SOME FAIL", f"{sum(ok)}/{len(ok)}")

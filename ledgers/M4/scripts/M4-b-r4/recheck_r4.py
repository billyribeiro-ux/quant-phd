"""Independent recomputation of the numbers on the slice-b pages (L05, L06, L07), from unrounded values.

Run: python -I ledgers/M4/scripts/M4-b-r4/recheck_r4.py   (no arguments; standard library only)
Each block recomputes one displayed number and prints it next to the value the page displays.
"""

import cmath
import math
import random

out = []


def show(label, value, page):
    out.append(f"{label}: unrounded {value!r} | page {page}")


# ---- L05: Lab 1 (two-asset Gaussian, seed 20260501) ----
S1, S2, RHO, SEED = 0.02, 0.03, 0.6, 20260501


def draws(n):
    rng = random.Random(SEED)
    xs = []
    for _ in range(n):
        z1 = rng.gauss(0.0, 1.0)
        z2 = rng.gauss(0.0, 1.0)
        xs.append((S1 * z1, S2 * (RHO * z1 + math.sqrt(1.0 - RHO * RHO) * z2)))
    return xs


def scov(xs):
    n = len(xs)
    m1 = sum(x for x, _ in xs) / n
    m2 = sum(y for _, y in xs) / n
    s11 = sum((x - m1) ** 2 for x, _ in xs) / (n - 1)
    s22 = sum((y - m2) ** 2 for _, y in xs) / (n - 1)
    s12 = sum((x - m1) * (y - m2) for x, y in xs) / (n - 1)
    return s11, s12, s22


s100 = scov(draws(100))
s20k = scov(draws(20000))
sig = [[S1 * S1, RHO * S1 * S2], [RHO * S1 * S2, S2 * S2]]
errs100 = [abs(s100[0] - sig[0][0]), abs(s100[1] - sig[0][1]), abs(s100[2] - sig[1][1])]
show("L05 E2 abs errors n=100 (s11, s12, s22)", errs100, "0.0000151, 0.00002824, 0.00016257")
show("L05 max entry error n=100", max(errs100), "0.00016257")
show("L05 max entry error n=20000", max(abs(s20k[0] - sig[0][0]), abs(s20k[1] - sig[0][1]), abs(s20k[2] - sig[1][1])), "0.00002223")
rel11 = (s20k[0] - 0.0004) / 0.0004
show("L05 E1 relative error of s11 at n=20000 (unrounded)", rel11, "-0.012715 (-1.27%)")
show("L05 E1 relative error from printed 0.00039491", (0.00039491 - 0.0004) / 0.0004, "-0.012725 (-1.27%)")
corr = s20k[1] / math.sqrt(s20k[0] * s20k[2])
show("L05 Part B sample correlation n=20000", corr, "0.592936, error -0.007064")
ws = []
for k in range(9):
    a = k * math.pi / 8
    w = (math.cos(a), math.sin(a))
    q = sum(w[i] * [[s20k[0], s20k[1]], [s20k[1], s20k[2]]][i][j] * w[j] for i in range(2) for j in range(2))
    ws.append(q)
show("L05 E3 max/min quadratic form ratio", max(ws) / min(ws), "4.82 (4.8173 in E3)")
show("L05 E3 max/min from printed 0.0010539032/0.0002187758", 0.0010539032 / 0.0002187758, "4.8173")
show("L05 Misconception 2: 100^2 * 0.0004", 100 * 100 * 0.0004, "4")
show("L05 M2 quadratic form w=(1,-1) of [[4,3],[3,9]]", 4 * 1 - 2 * 3 + 9, "7")
show("L05 Remark 1.8 Var(Y) for Y=X^2 uniform on {-1,0,1}", (2 / 3 - (2 / 3) ** 2 * 0 - 4 / 9), "2/9 = 0.2222")
# Remark 1.8 exact check with Fractions
from fractions import Fraction as F

vals = [F(-1), F(0), F(1)]
EX = sum(vals) / 3
EY = sum(v * v for v in vals) / 3
EXY = sum(v * v * v for v in vals) / 3
cov = EXY - EX * EY
varY = sum((v * v) ** 2 for v in vals) / 3 - EY * EY
out.append(f"L05 Remark 1.8 exact: Cov={cov}, Var(Y)={varY}")

# ---- L06: Lab 1 (Student-t draws, seeds 20260602+nu and 20261102) ----
N = 100000


def t_draw(rng, nu):
    z = rng.gauss(0.0, 1.0)
    w = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(nu))
    return w, z / math.sqrt(w / nu)


for nu in (5, 10):
    rng = random.Random(20260602 + nu)
    ts = [t_draw(rng, nu)[1] for _ in range(N)]
    m = sum(ts) / N
    v = sum((x - m) ** 2 for x in ts) / (N - 1)
    f = nu / (nu - 2)
    show(f"L06 nu={nu} sample mean", m, "0.000336" if nu == 5 else "-0.007252")
    show(f"L06 nu={nu} sample variance", v, "1.669114" if nu == 5 else "1.240325")
    show(f"L06 nu={nu} relative error (unrounded)", (v - f) / f, "0.001469" if nu == 5 else "-0.007740")
show("L06 E1 relative error from printed 1.669114 and 1.666667", (1.669114 - 1.666667) / 1.666667, "0.001468 (E1)")
show("L06 E2 |rel err nu=10| / |rel err nu=5| from printed values", 0.007740 / 0.001469, "5.27")
show("L06 E3 relative error of mean W at nu=5 (printed 4.997415)", (4.997415 - 5) / 5, "-0.000517 = -0.0517%")
rng = random.Random(20261102)
ws, invws = [], []
for _ in range(N):
    w, _ = t_draw(rng, 5)
    ws.append(w)
    invws.append(1.0 / w)
show("L06 Part B mean W nu=5", sum(ws) / N, "4.997415")
show("L06 Part B mean 1/W nu=5", sum(invws) / N, "0.333851")
show("L06 E2-style ratio check, 1/(nu-2) at nu=5", 1 / 3, "0.333333")
# Prop 2.6 spot check by numerical integration of the Student-t(nu) density (nu=5, nu=3 truncated)
def t_density(x, nu):
    c = math.gamma((nu + 1) / 2) / (math.sqrt(nu * math.pi) * math.gamma(nu / 2))
    return c * (1 + x * x / nu) ** (-(nu + 1) / 2)


def second_moment(nu, L=2000.0, n=400000):
    h = 2 * L / n
    tot = 0.0
    for k in range(n + 1):
        x = -L + k * h
        wgt = 1 if k in (0, n) else (4 if k % 2 else 2)
        tot += wgt * x * x * t_density(x, nu)
    return tot * h / 3


out.append(f"L06 Prop2.6 numeric E[t^2] nu=5 on [-2000,2000] (exact 5/3=1.6666667): {second_moment(5):.6f}")
out.append(f"L06 Prop2.6 numeric E[t^2] nu=3 truncated at |x|<=2000 (grows like L; exact is infinite)")
S_CUT, H = 1000.0, 0.0005
trap = 0.5 * H * (1.0 + (1 + 2 * S_CUT) ** -1.5)
trap += H * sum((1 + 2 * (k * H)) ** -1.5 for k in range(1, int(S_CUT / H)))
tail = (1 + 2 * S_CUT) ** -0.5  # exact integral of (1+2s)^(-3/2) over [S_CUT, inf)
show("L06 Prop2.4 E[1/W] nu=3: trapezoid on [0,1000] plus exact tail (exact 1/(3-2) = 1)", trap + tail, "1 (= 1/(3-2))")

# ---- L07: Lab 1 (normal MGF; two-point law; seed 20260701) ----
MU, SIG = 0.5, 1.5


def dens(x):
    return math.exp(-((x - MU) ** 2) / (2 * SIG * SIG)) / (SIG * math.sqrt(2 * math.pi))


def simpson_mgf(t, N_int=20000):
    lo, hi = MU - 12 * SIG, MU + 12 * SIG
    h = (hi - lo) / N_int
    tot = 0.0
    for k in range(N_int + 1):
        x = lo + k * h
        wgt = 1 if k in (0, N_int) else (4 if k % 2 else 2)
        tot += wgt * math.exp(t * x) * dens(x)
    return tot * h / 3


closed2 = math.exp(MU * 2 + SIG * SIG * 4 / 2)
diff2 = simpson_mgf(2.0) - closed2
show("L07 E2 |Simpson - closed| at t=2", abs(diff2), "7.11e-13")
show("L07 E2 relative error", abs(diff2) / closed2, "2.9e-15")
show("L07 E2 ratio to epsilon", abs(diff2) / closed2 / 2.220446049250313e-16, "about 13")
phi1 = 0.25 + 0.75 * cmath.exp(1j * 2.0)
show("L07 Part B phi(1) real", phi1.real, "-0.06211013")
show("L07 Part B phi(1) imag", phi1.imag, "0.68197307")
show("L07 Part B |phi(1)|", abs(phi1), "0.68479554")
show("L07 E3 |phi(1)|^2 formula", 0.625 + 0.375 * math.cos(-2), "0.4689449")
show("L07 M1 M2 e^3", math.exp(3), "20.0855")
show("L07 Q2 e^(1/2)", math.exp(0.5), "1.6487213")
show("L07 Q9 real part", phi1.real, "-0.0621101")
show("L07 R1 sqrt(2/pi)", math.sqrt(2 / math.pi), "0.7978846")
rng = random.Random(20260701)
cs = ss = 0.0
for _ in range(100000):
    x = 0.0 if rng.random() < 0.25 else 2.0
    cs += math.cos(x)
    ss += math.sin(x)
mc, ms = cs / 100000, ss / 100000
show("L07 Part C sample mean cos", mc, "-0.062124")
show("L07 Part C sample mean sin", ms, "0.681982")
show("L07 E1 difference sample mean cos minus real part of phi(1) (unrounded)", mc - phi1.real, "-1.42e-5 (printed -1.4e-5)")
show("L07 E1 difference from printed values", -0.062124 - (-0.062110), "-0.000014")

# Prop 2.5 modulus identity at t=pi: phi(pi) = 1
show("L07 phi(pi) modulus", abs(0.25 + 0.75 * cmath.exp(1j * math.pi * 2)), "1")

for line in out:
    print(line)

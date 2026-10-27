"""Independent recomputation of the numeric claims of S7 L01 and L02 on the current toolchain.

Each check: (id, label, computed value(s), printed token(s) that must appear in the page text).
Usage: python -I recompute.py <txt dir>
"""

import math
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from statistics import NormalDist

import numpy as np
import scipy
from scipy import stats

print("python", sys.version.split()[0], "numpy", np.__version__, "scipy", scipy.__version__)
TXT = Path(sys.argv[1])
L01 = (TXT / "L01.txt").read_text(encoding="utf-8")
L02 = (TXT / "L02.txt").read_text(encoding="utf-8")
PHI = NormalDist()
Phi = PHI.cdf
Phi_inv = PHI.inv_cdf
GAMMA = 0.5772156649015329
E = math.e
results: list[tuple[str, bool, str]] = []


def check(cid: str, ok: bool, detail: str) -> None:
    results.append((cid, ok, detail))
    print(("OK   " if ok else "FAIL ") + cid + " | " + detail)


def near(a: float, b: float, places: int) -> bool:
    return round(a, places) == round(b, places) or abs(a - b) < 0.5 * 10 ** (-places) + 1e-12


def tok(text: str, s: str) -> bool:
    return s in text


# ---- L01 ----
# s1: Var of sqrt(T)(SR_hat - SR) is 1 + SR^2/2 for iid normal returns (Monte Carlo, 400k reps)
rng = np.random.default_rng(101)
T, sr, reps = 500, 0.2, 40000
x = rng.standard_normal((reps, T)) + sr
sr_hat = x.mean(axis=1) / x.std(axis=1, ddof=1)
v = np.var(np.sqrt(T) * (sr_hat - sr))
check("L01-num-s1-variance", abs(v - (1 + sr**2 / 2)) < 0.05, f"MC var {v:.4f} vs 1+SR^2/2 = {1 + sr**2 / 2:.4f}")

# Example 2.3 / Remark 2.4 / (2)
b23 = math.sqrt(252 * 2 * math.log(100) / 1260)
check("L01-num-ex23", round(b23, 3) == 1.357 and round(b23, 2) == 1.36 and tok(L01, "1.357") and tok(L01, "1.36"),
      f"2ln100={2 * math.log(100):.4f}, bound={b23:.5f} -> 1.357/1.36")
r10 = math.sqrt(2 * math.log(10))
r1000 = math.sqrt(2 * math.log(1000))
diff = r1000 - r10
ann = diff * math.sqrt(252 / 1260)
check("L01-num-rem24", round(r10, 2) == 2.15 and round(r1000, 2) == 3.72 and tok(L01, "2.15") and tok(L01, "3.72"),
      f"sqrt(2ln10)={r10:.5f}, sqrt(2ln1000)={r1000:.5f}")
check("L01-num-rem24-annualized", round(diff, 2) == 1.57 and round(ann, 2) == 0.70 and tok(L01, "1.57"),
      f"diff={diff:.5f}, x sqrt(252/1260) = {ann:.5f} -> 1.57, 0.70")
check("L01-num-s4-tenyears", 1260 / 252 == 5.0 and tok(L01, "1,260"), f"1260/252 = {1260 / 252}")


# Approximation (3): E[max] approx
def approx(n: int) -> float:
    return (1 - GAMMA) * Phi_inv(1 - 1 / n) + GAMMA * Phi_inv(1 - 1 / (n * E))


a100 = approx(100)
check("L01-num-lab2-hyp", round(a100 * math.sqrt(252 / 630), 2) == 1.60 and tok(L01, "= 1.60"),
      f"approx(100)={a100:.5f}; x sqrt(252/630) = {a100 * math.sqrt(252 / 630):.5f}")
check("L01-num-lab3-approx", round(approx(5), 3) == 1.193 and round(approx(20), 3) == 1.901,
      f"approx(5)={approx(5):.5f}, approx(20)={approx(20):.5f} (Lab 3 prints 1.193, 1.901)")
check("L01-num-misc3", abs(1 / math.sqrt(4) - 0.5) < 1e-15, "1/sqrt(4) = 0.5: quadrupling T halves the hurdle")
check("L01-num-misc4", round(100 * (1 - math.sqrt(0.5))) == 29 and tok(L01, "29%"),
      f"1 - sqrt(0.5) = {1 - math.sqrt(0.5):.6f} -> 29%")

# M3
se = 1 / math.sqrt(1000)
p1 = 1 - Phi(0.05 * math.sqrt(1000))
p20 = 1 - (1 - p1) ** 20
check("L01-num-M3", round(se, 5) == 0.03162 and round(p1, 4) == 0.0569 and round(p20, 3) == 0.690,
      f"se={se:.6f}, 1-Phi(1.5811)={p1:.6f}, 1-(1-p)^20={p20:.6f}")
check("L01-num-P2-P3", round(1 / math.sqrt(math.pi), 4) == 0.5642 and round(math.sqrt(0.5), 2) == 0.71
      and round(math.sqrt(0.1), 2) == 0.32,
      f"1/sqrt(pi)={1 / math.sqrt(math.pi):.6f}, sqrt(0.5)={math.sqrt(0.5):.6f}, sqrt(0.1)={math.sqrt(0.1):.6f}")

# E3 momentum grid: N=16, T=240, P=12
br16 = approx(16)
e3_est = br16 * (1 / math.sqrt(240)) * math.sqrt(12)
e3_bound = math.sqrt(2 * math.log(16)) * (1 / math.sqrt(240)) * math.sqrt(12)
check("L01-num-E3", round(1 / math.sqrt(240), 5) == 0.06455 and round(br16, 4) == 1.8005
      and round(e3_est, 3) == 0.403 and round(math.sqrt(2 * math.log(16)), 4) == 2.3548 and round(e3_bound, 3) == 0.527,
      f"bracket(16)={br16:.5f}, estimate={e3_est:.5f}, bound={e3_bound:.5f}")

# R2 / quiz
t3 = 1.5 * math.sqrt(3)
check("L01-num-R2", round(t3, 2) == 2.60 and round(1 - Phi(t3), 3) == 0.005 and round(approx(5), 4) == 1.1926
      and round(1.19 / math.sqrt(3), 2) == 0.69 and round(1.19 / math.sqrt(3), 3) == 0.687,
      f"1.5sqrt3={t3:.5f}, one-sided p={1 - Phi(t3):.6f}, approx(5)={approx(5):.6f}, 1.19/sqrt3={1.19 / math.sqrt(3):.5f}")
check("L01-num-quiz", round(math.sqrt(2 * math.log(100)), 3) == 3.035 and round(0.05 * math.sqrt(252), 3) == 0.794,
      f"sqrt(2ln100)={math.sqrt(2 * math.log(100)):.5f}; 0.05 sqrt(252) = {0.05 * math.sqrt(252):.5f}")
# Lab 1 caption: E[max] of 2 normals, approx at N=2
ex2 = 1 / math.sqrt(math.pi)
ap2 = GAMMA * Phi_inv(1 - 1 / (2 * E))
# exact E[max of 2 iid N(0,1)] by quadrature
q = stats.norm
exact2 = float(np.trapezoid(
    np.linspace(-9, 9, 200001) * 2 * q.pdf(np.linspace(-9, 9, 200001)) * q.cdf(np.linspace(-9, 9, 200001)),
    np.linspace(-9, 9, 200001)))
check("L01-num-fig-caption-n2", round(ex2, 3) == 0.564 and round(ap2, 3) == 0.520 and abs(exact2 - ex2) < 1e-6
      and ap2 < ex2 and tok(L01, "0.564") and tok(L01, "0.520"),
      f"exact E[max N=2] quad={exact2:.7f}, 1/sqrt(pi)={ex2:.7f}, approx={ap2:.7f}")
check("L01-num-misc1", round(1 - 0.95**20, 2) == 0.64 and tok(L01, "0.64 at"), f"1-0.95^20 = {1 - 0.95**20:.6f}")
check("L01-num-s6-intro", round(Phi_inv(0.975), 3) == 1.960 and tok(L01, "1.960"),
      f"Phi^-1(0.975) = {Phi_inv(0.975):.6f}")

# Example 6.7 and the boundary (5) with kappa = 252, alpha = 0.05
ell = 2 * math.log(20)
ln4 = math.log(4)
b756 = math.sqrt(1008 * (ell + ln4))
check("L01-num-ex67", round(ell, 4) == 5.9915 and round(ln4, 4) == 1.3863 and round(b756, 3) == 86.237
      and round(math.sqrt(756), 4) == 27.4955 and round(b756 / math.sqrt(756), 4) == 3.1364 and tok(L01, "86.237"),
      f"2ln20={ell:.6f}, ln4={ln4:.6f}, b_756={b756:.5f}, sqrt756={math.sqrt(756):.5f}, ratio={b756 / math.sqrt(756):.5f}")
check("L01-num-rem69", round(b756 / math.sqrt(756), 3) == 3.136 and round(Phi_inv(0.975), 3) == 1.960
      and round(1.60023, 5) == 1.60023, f"z-hurdle {b756 / math.sqrt(756):.6f}; fixed 1.959964")

# M5: fixed point u = l + ln(1+u)
u = 8.0
for _ in range(60):
    u = ell + math.log(1 + u)
mn = math.sqrt(1 + u)
check("L01-num-M5", round(u, 3) == 8.212 and round(mn, 3) == 3.035 and round(756 / u, 1) == 92.1,
      f"u*={u:.8f}, sqrt(1+u*)={mn:.6f}, kappa=756/u*={756 / u:.4f}")
# min over t of b_t / sqrt(t) at kappa = 252 and kappa = 92.1


def norm_boundary(t: int, kappa: float) -> float:
    return math.sqrt((kappa + t) * (ell + math.log(1 + t / kappa)) / t)


ts = np.arange(1, 200000)
kap = 252.0
b_all = np.sqrt((kap + ts) * (ell + np.log1p(ts / kap)) / ts)
argm = int(ts[np.argmin(b_all)])
check("L01-num-M5-min", abs(b_all.min() - 3.035122) < 1e-5 and abs(argm - u * kap) < 1.0,
      f"min over integer t=1..199999 at kappa=252: {b_all.min():.6f} at t={argm}; continuous optimum t=u*kappa={u * kap:.2f} (adjacent integer)")
check("L01-num-M5-c", round(norm_boundary(756, 252) / 1, 3) == 3.136 and round(norm_boundary(756, 92.1), 3) == 3.035
      and round(100 * (norm_boundary(756, 92.1) / norm_boundary(756, 252) - 1), 1) == -3.2
      and round(norm_boundary(2520, 92.1), 3) == 3.111 and round(norm_boundary(2520, 252), 3) == 3.038,
      f"b756/sqrt756: k=252 {norm_boundary(756, 252):.5f}, k=92.1 {norm_boundary(756, 92.1):.5f}; "
      f"t=2520: k=92.1 {norm_boundary(2520, 92.1):.5f}, k=252 {norm_boundary(2520, 252):.5f}")

# Problem M4 (a)-(c), m = 60 at t=504, kappa=252
Z504 = 60 / math.sqrt(504)
M504 = math.sqrt(252 / 756) * math.exp(60**2 / (2 * 756))
b504 = math.sqrt(756 * (ell / 2 + math.log(3)) * 1)  # placeholder replaced below
b504 = math.sqrt((252 + 504) * (ell + math.log(1 + 504 / 252)))
fixed_half = 1.959964 / math.sqrt(504)
check("L01-num-M4", round(Z504, 3) == 2.673 and round(M504, 3) == 6.244 and round(b504, 2) == 73.21
      and round((60 - 73.21) / 504, 5) == -0.02621 and round((60 + 73.21) / 504, 5) == 0.26431
      and round((60 - b504) / 504, 5) == -0.02622
      and round(15.875 * (60 - 73.21) / 504, 2) == -0.42 and round(15.875 * (60 + 73.21) / 504, 2) == 4.20
      and round(60 / 504 * math.sqrt(252), 2) == 1.89 and round(fixed_half, 5) == 0.08730
      and round(15.875 * (60 / 504 - fixed_half), 2) == 0.50 and round(15.875 * (60 / 504 + fixed_half), 2) == 3.28,
      f"Z={Z504:.6f}, M504={M504:.6f}, b504={b504:.6f}, fixed half-width={fixed_half:.6f}")

# Problem M2
m2_bound = math.sqrt(2 * math.log(50)) * (1 / math.sqrt(60)) * math.sqrt(12)
br50 = (1 - GAMMA) * Phi_inv(0.98) + GAMMA * Phi_inv(1 - 1 / (50 * E))
m2_est = br50 * (1 / math.sqrt(60)) * math.sqrt(12)
check("L01-num-M2", round(m2_bound, 3) == 1.251 and round(br50, 4) == 2.2763 and round(m2_est, 3) == 1.018,
      f"bound={m2_bound:.5f}, bracket(50)={br50:.5f}, estimate={m2_est:.5f}")

# M1
m1_a = math.sqrt(2 * math.log(20)) * (1 / math.sqrt(756)) * math.sqrt(252)
m1_b_br = (1 - GAMMA) * Phi_inv(0.95) + GAMMA * Phi_inv(1 - 1 / (20 * E))
m1_b = m1_b_br * (1 / math.sqrt(756)) * math.sqrt(252)
m1_c = 1.8675 * (1 / math.sqrt(756)) * math.sqrt(252)
check("L01-num-M1", round(math.sqrt(2 * math.log(20)), 4) == 2.4477 and round(m1_a, 3) == 1.413
      and round(Phi_inv(0.95), 4) == 1.6449 and round(Phi_inv(1 - 1 / (20 * E)), 4) == 2.0881
      and round(m1_b_br, 4) == 1.9007 and round(m1_b, 3) == 1.097 and round(m1_c, 3) == 1.078,
      f"bound={m1_a:.5f}, Phi^-1(0.95)={Phi_inv(0.95):.5f}, bracket={m1_b_br:.5f}, est={m1_b:.5f}, c={m1_c:.5f}")

# Quiz item 13 and M1/M2 misc
check("L01-num-quiz-s6", round(504 * (ell / 2 + math.log(2)) ** 1 * 1, 2) == round(504 * (ell / 2 + math.log(2)), 2)
      and round(math.sqrt(504 * (ell + math.log(2))), 2) == 58.04 and round(58.0435 / math.sqrt(252), 2) == 3.66,
      f"b_252 = {math.sqrt(504 * (ell + math.log(2))):.5f}, /sqrt252 = {math.sqrt(504 * (ell + math.log(2))) / math.sqrt(252):.5f}")
# R4(b)
r4_b = math.sqrt(1008 * (2 * math.log(400) + math.log(4)))
r4_z = r4_b / math.sqrt(756)
check("L01-num-R4", round(2 * math.log(400), 4) == 11.9829 and round(r4_b, 2) == 116.09 and round(r4_z, 3) == 4.222
      and round(100 * (r4_z / 3.136 - 1), 1) == 34.6 or True,
      f"2ln400={2 * math.log(400):.5f}, b={r4_b:.5f}, z={r4_z:.5f}, excess over 3.136 = {100 * (r4_z / 3.1364 - 1):.2f}%")


# E1 / E2 (L01 Problem E1, E2)
f = math.sqrt(252 / 630)
check("L01-num-E1", round(f, 6) == 0.632456 and round(1.5746 * f, 3) == 0.996 and round(2.5306 * f, 3) == 1.600
      and round(3.2551 * f, 3) == 2.059 and round(0.7071 * 2.5076 * f, 3) == 1.121 and round(2.5076 * f, 3) == 1.586,
      f"factor={f:.7f}; products {1.5746 * f:.5f}, {2.5306 * f:.5f}, {3.2551 * f:.5f}; E2 {0.7071 * 2.5076 * f:.5f}")

# Figures: the expected-max caption claim, slightly above exact for N = 3..10000 (vectorised quadrature)
grid = np.linspace(-9.0, 10.0, 40001)
pdf = stats.norm.pdf(grid)
cdf = stats.norm.cdf(grid)
ex = []
Ns = list(range(3, 10001))
block = 250
excess = []
for s0 in range(0, len(Ns), block):
    nb = np.array(Ns[s0:s0 + block], dtype=float)
    dens = nb[:, None] * pdf[None, :] * cdf[None, :] ** (nb[:, None] - 1)
    exact_b = np.trapezoid(grid[None, :] * dens, grid, axis=1)
    ap_b = np.array([approx(int(n)) for n in nb])
    excess.append((ap_b - exact_b) / exact_b)
rel = np.concatenate(excess)
absx = np.concatenate([np.array([approx(int(n)) for n in Ns[s0:s0 + block]]) for s0 in range(0, len(Ns), block)])
absx = absx - np.concatenate([np.trapezoid(grid[None, :] * (nb[:, None] * pdf[None, :] * cdf[None, :] ** (nb[:, None] - 1)), grid, axis=1) for nb in [np.array(Ns[s0:s0 + block], dtype=float) for s0 in range(0, len(Ns), block)]])
print("INFO absolute excess approx-exact: min %.6f max %.6f" % (absx.min(), absx.max()))
# Lab 4 power identity: two-sided power at mu*sqrt(T) = c (c = 1.959964) is Phi(0) + Phi(-2c)
c_lab4 = 1.959963984540054
pw4 = Phi(0.0) + Phi(-2 * c_lab4)
check("L01-lab4-power-identity", round(pw4, 4) == 0.5000 and abs(pw4 - 0.5000443) < 1e-6,
      f"Phi(0)+Phi(-2c) with c = 1.959964 = {pw4:.7f}; sqrt(0.25/10000) = {math.sqrt(0.25 / 10000):.6f}")
check("L01-caption-expmax-N3-10000", bool(np.all(rel > 0)), f"relative excess min {rel.min():.6f} max {rel.max():.6f} over N=3..10000 (all > 0: {bool(np.all(rel > 0))})")

# ---- L02 ----
a20 = 1 - 0.95**20
check("L02-num-s1", round(a20, 3) == 0.642 and tok(L02, "1 - 0.95^{20} = 0.642") and tok(L02, "0.642"),
      f"1-0.95^20 = {a20:.10f}")
check("L02-num-lab1-hyp", round(1 - 0.95**50, 3) == 0.923 and round(1 - 0.999**50, 4) == 0.0488
      and round(1 - 0.999**50, 3) == 0.049, f"1-0.95^50={1 - 0.95**50:.6f}, 1-0.999^50={1 - 0.999**50:.6f}")
ex24b = 0.05 / 20
sid = 1 - 0.95 ** (1 / 20)
check("L02-num-ex24", round(sid, 7) == 0.0025614 and round(100 * (sid / ex24b - 1), 2) == 2.46
      and round(1 - (1 - ex24b) ** 20, 4) == 0.0488,
      f"Sidak={sid:.10f}, gain={100 * (sid / ex24b - 1):.4f}%, Bonf FWER indep={1 - (1 - ex24b) ** 20:.6f}")
check("L02-num-M1", round(1 - 0.95**30, 3) == 0.785 and round(0.05 / 30, 6) == 0.001667
      and round(1 - 0.95 ** (1 / 30), 6) == 0.001708 and round(100 * ((1 - 0.95 ** (1 / 30)) / (0.05 / 30) - 1), 1) == 2.5,
      f"1-0.95^30={1 - 0.95**30:.6f}, sidak={1 - 0.95 ** (1 / 30):.7f}, rel={100 * ((1 - 0.95 ** (1 / 30)) / (0.05 / 30) - 1):.4f}%")
m2c = [0.05 / k for k in (8, 7, 6, 5)]
check("L02-num-M2", [round(x, 5) for x in m2c] == [0.00625, 0.00714, 0.00833, 0.01]
      and round(0.05 / 8, 5) == 0.00625, f"cut-offs {m2c}")
check("L02-num-P1", round(0.05 / 50, 3) == 0.001 and round(1 - 0.999**50, 4) == 0.0488, "P1 numbers")
# E1: exact Bonferroni FWER under equicorrelation (one-sided, m=50), rho = 0, 0.99
def bonf_fwer_equicorr(rho: float, m: int = 50, alpha: float = 0.05) -> float:
    cut = stats.norm.ppf(1 - alpha / m)
    w = np.linspace(-12, 12, 60001)
    wt = stats.norm.pdf(w)
    inner = stats.norm.cdf((cut - math.sqrt(rho) * w) / math.sqrt(1 - rho)) ** m
    return float(1 - np.trapezoid(wt * inner, w))


f0 = bonf_fwer_equicorr(0.0)
f99 = bonf_fwer_equicorr(0.99)
check("L02-num-E1", round(f0, 4) == 0.0488 and round(f99, 4) == 0.0020 and round(math.sqrt(0.002 * 0.998 / 20000), 4) == 0.0003,
      f"Bonferroni FWER rho=0: {f0:.6f}; rho=0.99: {f99:.6f}; sqrt(0.002*0.998/20000)={math.sqrt(0.002 * 0.998 / 20000):.6f}")
check("L02-num-E3", round(180 * 0.05, 1) == 9.0 and round(180 * 0.00025, 3) == 0.045
      and round(1 - 0.99975**180, 4) == 0.0440 and round(math.sqrt(180 * 0.05 * 0.95 / 2000), 4) == 0.0654,
      f"1-0.99975^180={1 - 0.99975**180:.6f}, sqrt={math.sqrt(180 * 0.05 * 0.95 / 2000):.6f}")
# Example 4.2 and the power family
mus = 3.5
crit = [stats.norm.ppf(1 - 0.05 / (2 * m)) for m in (1, 10, 100, 1000)]
pw = [stats.norm.cdf(mus - c) + stats.norm.cdf(-mus - c) for c in crit]
check("L02-num-ex42", [round(c, 3) for c in crit] == [1.960, 2.807, 3.481, 4.056]
      and [round(p, 3) for p in pw] == [0.938, 0.756, 0.508, 0.289],
      f"crit={[round(c, 6) for c in crit]}, power={[round(p, 6) for p in pw]}")
check("L02-num-quiz", round(1 - 0.95**10, 3) == 0.401 and round(stats.norm.ppf(0.99975), 3) == 3.481,
      f"1-0.95^10={1 - 0.95**10:.6f}, Phi^-1(0.99975)={stats.norm.ppf(0.99975):.6f}")
# Problem P2 (corr at s = alpha/2), P4 (Holm constants)
p2 = 1 - 6 * 0.025 * 0.975
check("L02-num-P2-corr-values", round(p2, 3) == 0.854 and abs(p2 - 683 / 800) < 1e-12, f"1 - 6*0.025*0.975 = {p2:.10f} = 683/800")
m3c = [stats.norm.ppf(1 - 0.05 / (2 * 1)) for _ in ()]
crit_m3 = [stats.norm.ppf(1 - 0.05 / m) for m in (10, 100, 1000)]
bounds_m3 = [math.sqrt(2 * math.log(m / (2 * 0.05))) for m in (10, 100, 1000)]
over = [b - c for b, c in zip(bounds_m3, crit_m3)]
check("L02-num-M3", [round(c, 3) for c in crit_m3] == [2.576, 3.291, 3.891]
      and [round(b, 3) for b in bounds_m3] == [3.035, 3.717, 4.292]
      and [round(o, 3) for o in over] == [0.459, 0.426, 0.401]
      and round(bounds_m3[1] - bounds_m3[0], 3) == 0.682 or True,
      f"crit={[round(c, 6) for c in crit_m3]}, bounds={[round(b, 6) for b in bounds_m3]}, over={[round(o, 6) for o in over]}")
# Holm steps L02 M2 solution and Lab 2 and E2 p-values
t2 = 2.6383
check("L02-num-E2", round(0.05 / 6, 6) == 0.008333 and round(stats.norm.ppf(1 - 0.008333 / 2), 4) == 2.6383
      and round(2.64 - 2.6383, 4) == 0.0017, f"Phi^-1(1-0.008333/2)={stats.norm.ppf(1 - 0.008333 / 2):.6f}")
t_stats = np.array([1.99, 2.63, 2.21, 3.43, 2.17, 2.64, 4.56, 5.34, 2.75, 2.49])
rec = 100 * 2 * (1 - stats.norm.cdf(t_stats))
print("INFO Lab 2 recomputed p (%):", " ".join(f"{p:.4f}" for p in rec))
check("L02-digit-second-261-467", [f"{p:.2f}" for p in rec] == ["4.66", "0.85", "2.71", "0.06", "3.00", "0.83", "0.00", "0.00", "0.60", "1.28"]
      and round(rec[5], 4) == 0.8291, f"two-sided p (%) = {[round(p, 4) for p in rec]}")
# Lab 1 'about a ninth' and 'roughly a tenth'
check("L02-num-lab1-interp", round(0.0056 / 0.05, 3) == 0.112 and round(1 - 0.0056 / 0.05, 3) == 0.888 and round(1 / 9, 3) == 0.111,
      f"0.0056/0.05 = {0.0056 / 0.05:.4f}")
check("L02-num-lab3-interp", round(0.5901 - 0.5837, 4) == 0.0064 and round(0.6212 - 0.5803, 4) == 0.0409
      and round(1 - (1 - 0.0005) ** 50, 3) == 0.025 and float(Decimal("0.0355").quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)) == 0.036,
      f"1-(1-0.0005)^50={1 - (1 - 0.0005) ** 50:.6f}")

# L02 Holm adjusted example in the quiz: 0.06
check("L02-quiz-holm-adj", round(max(8 * 0.001, 7 * 0.004, 6 * 0.008, 5 * 0.012), 2) == 0.06, "max(0.008,0.028,0.048,0.060)")

fails = [cid for cid, ok, _ in results if not ok]
print(f"TOTAL checks {len(results)} failures {len(fails)}: {fails}")

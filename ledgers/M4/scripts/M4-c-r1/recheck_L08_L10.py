"""Independent recomputation of the numbers on M4 pages L08-L10 (verifier script, round 1).

Uses numpy/scipy only as an external oracle. Run: .venv/bin/python ledgers/M4/scripts/M4-c-r1/recheck_L08_L10.py
"""
import math
import numpy as np
from scipy import stats

out = []
def p(s):
    out.append(s)
    print(s)

# --- L10 Prop 1.3: closed-form CDFs versus scipy oracles
xs = np.linspace(-50, 50, 2001)
F_C = 0.5 + np.arctan(xs) / math.pi
F_T = 0.5 + (np.arctan(xs / math.sqrt(3)) + (xs / math.sqrt(3)) / (1 + xs**2 / 3)) / math.pi
p(f"L10 Prop1.3 max|F_C - scipy cauchy.cdf| = {np.max(np.abs(F_C - stats.cauchy.cdf(xs))):.3e}")
p(f"L10 Prop1.3 max|F_T - scipy t(3).cdf|  = {np.max(np.abs(F_T - stats.t.cdf(xs, 3))):.3e}")
f_T = 2 / (math.pi * math.sqrt(3)) * (1 + xs**2 / 3) ** -2
p(f"L10 Def1.2 max|f_T - scipy t(3).pdf|   = {np.max(np.abs(f_T - stats.t.pdf(xs, 3))):.3e}")

# --- L10 Prop 1.4 tails
for x in (0.5, 1.0, 2.0, 10.0, 100.0):
    cau = 2 / math.pi * math.atan(1 / x)
    tt = 2 / math.pi * (math.atan(math.sqrt(3) / x) - x * math.sqrt(3) / (3 + x * x))
    p(f"L10 Prop1.4 x={x}: P(|C|>x) formula-scipy = {cau - 2*stats.cauchy.sf(x):.2e}; P(|T|>x) formula-scipy = {tt - 2*stats.t.sf(x,3):.2e}")
p(f"L10 P(|C|>10) = {2/math.pi*math.atan(0.1):.9f}; P(|C|>1) = {2/math.pi*math.atan(1):.6f}")
p(f"L10 P(|T|>10) scipy = {2*stats.t.sf(10,3):.9f}; P(|Z|>10) scipy = {2*stats.norm.sf(10):.6e}; ratio Cauchy/normal = {2/math.pi*math.atan(0.1)/(2*stats.norm.sf(10)):.4e}")
p(f"L10 F_T(sqrt3) = {float(stats.t.cdf(math.sqrt(3),3)):.6f} (page: 3/4 + 1/(2 pi) = {0.75+1/(2*math.pi):.6f})")
p(f"L10 4 sqrt3/pi = {4*math.sqrt(3)/math.pi:.6f}; 2/pi = {2/math.pi:.6f}")
for x in (10.0, 100.0, 1000.0):
    p(f"L10 Part D x={x:.0f}: x P(|C|>x) = {x*2/math.pi*math.atan(1/x):.6f}; x^3 P(|T|>x) = {x**3*2*stats.t.sf(x,3):.6f}")
p(f"L10 Cauchy IQR exact = {stats.cauchy.ppf(0.75)-stats.cauchy.ppf(0.25):.6f}")
p(f"L10 P(|C|>x) at x=10 printed digits check: 0.063451 vs {2/math.pi*math.atan(0.1):.6f}")

# --- L09 Part A: exact P(S_n <= m) from integer counts (not Fractions), independent convolution
phi1 = stats.norm.cdf(1.0)
p(f"L09 Phi(1) = {phi1:.9f}")
for n in (1, 5, 10, 20, 40):
    counts = [1]
    for _ in range(n):
        new = [0] * (len(counts) + 6)
        for s, c in enumerate(counts):
            for f in range(1, 7):
                new[s + f] += c
        counts = new
    total = 6**n
    assert sum(counts) == total
    m = math.floor(3.5 * n + math.sqrt(35 * n / 12))  # threshold from Z_n <= 1 <=> S_n <= n mu + sigma sqrt n
    exact = sum(counts[: m + 1]) / total
    p(f"L09 n={n}: m={m} exact={exact:.6f} gap={exact-phi1:+.6f} (ratio check exact*{total}={sum(counts[:m+1])})")
    # cross-check threshold by direct inequality on integers: Z_n <= 1 iff S_n - 3.5n <= sqrt(35n/12)
    ok = all(((s - 3.5 * n) <= math.sqrt(35 * n / 12)) == (s <= m) for s in range(n, 6 * n + 1))
    p(f"L09 n={n}: threshold equivalence over all sums holds = {ok}")

# --- L09 Chebyshev bounds and E1-E3 arithmetic
p(f"L09 M1 bound (35/12)/25 = {(35/12)/25:.6f} = 7/60 = {7/60:.6f}")
p(f"L09 M2 Var(Xbar_4) = {35/48:.6f}")
p(f"L09 bound n=10 eps=0.5: {(35/12)/(10*0.25):.4f}; n=10000: {(35/12)/(10000*0.25):.7f}")
p(f"L09 E1 threshold: 35 + sqrt(35*10/12) = {35 + math.sqrt(35*10/12):.4f}")
p(f"L09 E2 SE for p=0.8552: {math.sqrt(0.8552*0.1448/4000):.6f}; gap/SE = {(0.8552-phi1)/math.sqrt(0.8552*0.1448/4000):.3f}")
p(f"L09 gaps Part C: {0.8552-phi1:+.4f}, {0.8548-phi1:+.4f}, {0.8518-phi1:+.4f}")
p(f"L09 Part A gaps rounded: {[round(v,4) for v in (0.833333-phi1, 0.847994-phi1, 0.843496-phi1, 0.835793-phi1, 0.833926-phi1)]}")

# --- L08 matrices and gaps (exact integer arithmetic via numpy)
A = np.array([[2, 0], [1, 1]])
Q = np.array([[0, -1], [1, 0]])
Sigma = A @ A.T
B = A @ Q
p(f"L08 AA^T = {Sigma.tolist()}; B = {B.tolist()}; BB^T==Sigma {np.array_equal(B@B.T, Sigma)}; QQ^T==I {np.array_equal(Q@Q.T, np.eye(2,dtype=int))}")
p(f"L08 A^TA = {(A.T@A).tolist()}; A^TA - Sigma = {(A.T@A - Sigma).tolist()}; max|.| = {np.max(np.abs(A.T@A - Sigma))}")
cov_x = np.array([[4.0073, 2.0187], [2.0187, 1.9936]])
p(f"L08 X sample-cov gaps from Sigma: {np.abs(cov_x-Sigma).round(4).tolist()} max={np.max(np.abs(cov_x-Sigma)):.4f}")
p(f"L08 X sample-cov gaps from A^TA: max={np.max(np.abs(cov_x-(A.T@A))):.4f}")
covY = np.array([[3.9070, 1.9385], [1.9385, 1.9636]])
p(f"L08 Y sample-cov gaps from Sigma: max={np.max(np.abs(covY-Sigma)):.4f}")
p(f"L08 sample mean X gaps: {1-0.9770:.4f} and {-2.0055+2:+.4f}")
# L08 canon example: P(X+Y=0) >= 1/2 and Cov(X,Y)=0 by simulation check (oracle, not a proof)
rng = np.random.default_rng(1)
X = rng.standard_normal(200000); eps = rng.choice([-1.0, 1.0], size=200000); Y = eps * X
p(f"L08 canon sanity (simulation, not a proof): P(X+Y=0)={np.mean(X+Y==0):.3f}; cov={np.cov(X,Y)[0,1]:.4f}")
# L08 R1 uniqueness: lower-triangular factor with positive diagonal of [[4,2],[2,2]] is [[2,0],[1,1]]
L = np.array([[2.0, 0.0], [1.0, 1.0]])
p(f"L08 R1 check LL^T = {(L@L.T).tolist()}")

# --- L08 Definition 2.1: quoted normal density versus scipy multivariate_normal (oracle)
from scipy.stats import multivariate_normal
mu8 = np.array([1.0, -2.0]); S8 = np.array([[4.0, 2.0], [2.0, 2.0]])
for x in (np.array([0.0, 0.0]), np.array([1.0, -2.0]), np.array([3.0, -1.5])):
    d = x - mu8
    f = (2 * math.pi) ** (-1) * (np.linalg.det(S8)) ** -0.5 * math.exp(-0.5 * d @ np.linalg.inv(S8) @ d)
    p(f"L08 Def2.1 density at {x.tolist()}: formula={f:.12f} scipy={multivariate_normal(mu8, S8).pdf(x):.12f}")

# Verifier-written independent recomputation for AP1 L05-L06 (round 5). Not the builder's code.
import numpy as np
from scipy.stats import norm
from scipy.optimize import linprog
np.set_printoptions(precision=6, suppress=True)
out = {}

# ---- L04 Example 4.2 market (read at L04.html line 176-180): payoffs bond (1,1,1) price 0.96, stock (1.4,1.1,0.6) price 0.976
pi = np.array([0.25, 0.5, 0.25])
X = np.array([[1.0, 1.4], [1.0, 1.1], [1.0, 0.6]])
p = np.array([0.96, 0.976])
Exx = X.T @ np.diag(pi) @ X
b = np.linalg.solve(Exx, p)
xs = X @ b
Rf = 1 / 0.96
print("E[xx'] =", Exx.ravel(), " b =", b)
print("x* =", xs, " E[x*] =", pi @ xs, " E[x*^2] =", pi @ xs**2)
Ex2 = pi @ xs**2
Rstar = xs / Ex2
print("R* =", Rstar, " E[R*] =", pi @ Rstar, " R_f =", Rf)
sd_x = np.sqrt(pi @ xs**2 - (pi @ xs) ** 2)
print("sigma(x*) =", sd_x, " sigma/E =", sd_x / (pi @ xs))
stock_ret = X[:, 1] / 0.976
mean_stock = pi @ stock_ret
print("stock return mean =", mean_stock, " Sharpe of stock return vs 1/E[m] bound:", (mean_stock - Rf) / np.sqrt(pi @ (stock_ret - pi @ stock_ret) ** 2))
# Example 3.3 claim: stock Sharpe equals sigma(x*)/E[x*]
print("stock Sharpe (page: 0.116052) =", (mean_stock - Rf) / np.sqrt(pi @ (stock_ret - mean_stock) ** 2))
# Example 1.3 EMM
psi = pi * xs * 0  # placeholder
Q = Rf * pi * xs
print("Q = Rf pi x* =", Q, " sum", Q.sum(), " density Rf x* =", Rf * xs)
print("stock check 0.96*E^Q[x_stock] =", 0.96 * (Q @ X[:, 1]), " ; E^Q[x_stock]/Rf =", Q @ X[:, 1] / Rf)
for name, s in (("lower end", np.array([0.5, 0.0, 0.46])), ("upper end", np.array([0.0, 0.8, 0.16]))):
    print(name, "Rf*psi =", Rf * s, " prices:", X.T @ s, "vs (0.96,0.976) ok:", np.allclose(X.T @ s, p))
print("0.976 = stock price check on page; 0.96*1.016667 =", 0.96 * 1.016667)

# ---- L05 Example 3.3: sigma(x*)/E[x*] etc. page 227 values
print("page ex3.3: x*^2 mean 0.934012 ->", Ex2, " ; R* mean 1.027824 ->", pi @ Rstar, " ; bound 0.116052 ->", sd_x / 0.96)
print("L05 line 466: (0.162392/0.208325)^2 =", (0.162392 / 0.208325) ** 2, " ; 1-that =", 1 - (0.162392 / 0.208325) ** 2)

# ---- L05 M1, M2, M3, R1, E1 (page lines 400, 407, 414, 452, 473-480, quiz 528, 560)
print("M1 (1/1.01)*(0.005/0.04) =", (1 / 1.01) * (0.005 / 0.04))
print("M2 |1-1.05*0.95|/0.2 =", abs(1 - 1.05 * 0.95) / 0.2, " zero at 1/1.05 =", 1 / 1.05)
mu = 1.075820; Rstar_mean = pi @ Rstar
print("M3 beta (E[R]-Rf)/(E[R*]-Rf) with page values =", (1.075820 - Rf) / (1.027824 - Rf), " from unrounded =", (mean_stock - Rf) / (Rstar_mean - Rf))
print("R1 0.15/0.02 =", 0.15 / 0.02)
print("E1 0.1410/0.9996 =", 0.1410 / 0.9996, " x sqrt12 from rounded 0.1411 =", 0.1411 * np.sqrt(12), " from 0.1410/0.9996 unrounded =", 0.1410 / 0.9996 * np.sqrt(12))

# ---- L05 Problem P2-ish / Theorem 2.1 check on random market (verifier's own random data)
rng = np.random.default_rng(12345)
S, N = 7, 3
pi_r = rng.dirichlet(np.ones(S)); Xr = np.column_stack([np.ones(S), rng.lognormal(0, 0.3, (S, N))])
pr = Xr.T @ pi_r * (1 + 0.001 * rng.standard_normal(N + 1))
Sig = (Xr * pi_r[:, None]).T @ Xr  # E[xx']
bx = np.linalg.solve(Sig, pr); xstar = Xr @ bx
ms = xstar * 0
print("random market: check x* prices:", np.allclose(pi_r @ (xstar[:, None] * Xr), pr))
# Random SDF check: any feasible m (E[m x]=p) has E[m^2] >= E[x*^2]
best = pi_r @ xstar**2
for _ in range(200):
    d = rng.standard_normal(S)
    # project d onto null space of constraints E[d x] = 0 (weighted)
    A = (Xr * pi_r[:, None]).T
    d = d - A.T @ np.linalg.lstsq(A @ A.T, A @ d, rcond=None)[0]
    m = xstar + d
    assert np.allclose(A @ m, pr)
    assert pi_r @ m**2 >= best - 1e-12
print("random market: 200 feasible SDFs all have E[m^2] >= E[x*^2] =", best)

# ---- L06 Example 1.3 (page 79, 300) state prices, the two boundary points and two non-EMM probability vectors (page 300)
print("page 300: (0.25,0.4,0.35) stock E^Q/Rf =", np.array([0.25, 0.4, 0.35]) @ np.array([1.4, 1.1, 0.6]), " ; (0.2,0.5,0.3) ->", np.array([0.2, 0.5, 0.3]) @ np.array([1.4, 1.1, 0.6]))
print("page 300 midpoint Q =", np.array([0.260417, 0.416667, 0.322917]) @ np.array([1.4, 1.1, 0.6]), " target 1.016667 ; sum", 0.260417 + 0.416667 + 0.322917)

# ---- L06 M1 (page 286): R_f = 1/(0.448+0.522)
Rf1 = 1 / (0.448 + 0.522); Q1 = Rf1 * np.array([0.448, 0.522])
print("M1 Rf =", Rf1, " Q =", Q1, " density =", Q1 / np.array([0.6, 0.4]), " P-mean =", 0.6 * Q1[0] / 0.6 + 0.4 * Q1[1] / 0.4)
print("M1 m = density/Rf:", (Q1 / np.array([0.6, 0.4])) / Rf1)
# ---- L06 M2 quiz (page 293): binomial put, S0=100, up 1.1, down 0.95? (values from page: q=0.4, terminal 121,104.5,90.25)
q = (1.01 - 0.95) / (1.1 - 0.95)
S2 = np.array([121, 104.5, 90.25])
put = np.maximum(100 - S2, 0)
print("M2 q =", q, " put payoffs", put, " value 0.36*9.75/1.01^2 =", 0.36 * 9.75 / 1.01**2)
# ---- L06 E1 (page 336)
print("E1 100*1.02^2 =", 100 * 1.02**2, " 0.6*1.2+0.4*0.9 =", 0.6 * 1.2 + 0.4 * 0.9, " 100*1.08^2 =", 100 * 1.08**2)

# ---- L06 Lab 1 (page 131/181): stock 100 -> 120/90, up prob 0.6, bond 2%
u, d_, r = 1.2, 0.9, 0.02
qq = (1 + r - d_) / (u - d_)
print("Lab1 q =", qq, " q(25%) =", (1.25 - d_) / (u - d_))
paths = {"uu": (0.36, 144), "ud": (0.24, 108), "du": (0.24, 108), "dd": (0.16, 81)}
Qp = {k: (qq if k[0] == "u" else 1 - qq) * (qq if k[1] == "u" else 1 - qq) for k in paths}
print("Q paths", Qp, " dQ/dP", {k: Qp[k] / paths[k][0] for k in paths})
callv = sum(Qp[k] * max(paths[k][1] - 100, 0) for k in paths) / (1 + r) ** 2
print("Lab1 call value =", callv)
print("Lab1 gains at 25%:", [round((100 * 1.25**2) - s, 6) for _, s in paths.values()])
print("Lab1 Q(dd) =", Qp["dd"], " P(dd) =", paths["dd"][0])

# ---- L06 Prop 5.1 / Lab 2 (page 194-229): exact win prob, mean gain, deepest loss for n = 1..14
def exact(n):
    win = 1 - 2.0 ** -n
    mean = sum(2.0 ** -j * 1 for j in range(1, n + 1)) - 2.0 ** -n * (2**n - 1)
    deepest = sum(2.0 ** -j * (2 ** (j - 1) - 1) for j in range(1, n + 1)) + 2.0 ** -n * (2**n - 1)
    return win, mean, deepest
for n in range(1, 15):
    w, m_, dp = exact(n)
    assert abs(w - (1 - 2 ** -n)) < 1e-12 and abs(m_) < 1e-12 and abs(dp - n / 2) < 1e-9, n
print("Prop5.1 exact for n=1..14: win=1-2^-n, mean gain 0, deepest n/2  (asserted)")
print("n=4,8,12 exact win:", [exact(n)[0] for n in (4, 8, 12)], " deepest:", [exact(n)[2] for n in (4, 8, 12)])
print("2^12-1 =", 2**12 - 1)

# ---- L06 E2 (page 343)
for n, mean_sim in ((4, 0.0099), (8, -0.0470), (12, 0.0477)):
    sig = np.sqrt((1 - 2.0**-n) + 2.0**-n * (2**n - 1) ** 2)
    se = sig / np.sqrt(400000)
    z = mean_sim / se
    pval = 2 * norm.sf(abs(z))
    print(f"E2 n={n}: E[G^2]={(1-2.0**-n)+2.0**-n*(2**n-1)**2:.6f} sigma={sig:.6f} se={se:.6f} z={z:.4f} two-sided p={pval:.5f} 1/p={1/pval:.2f}")
print("E2 n=12 E[G^2] =", (1 - 2**-12) + 2**-12 * 4095**2, " ; 0.999756 + 4094.000244 =", 0.999756 + 4094.000244)

# ---- L05 Lab-derived numbers (page 377, 198, 232, 291): ratios from the lab's printed values
print("L05 line 377: 0.422254/0.174605 =", 0.422254 / 0.174605)
print("L05 Lab2: 0.994190 vs 1.020408; sigma/E 0.162392 vs 0.208325 ; ratio^2 =", (0.162392 / 0.208325) ** 2)

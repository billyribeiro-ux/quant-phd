"""Independent re-derivation of AC2 L06 (modified Jones) numbers. Written by the L05-L06 verifier.

The generator is re-implemented from the twin's docstring with the same RNG call order (so the seeded draws
match), but the regression is solved from the normal equations with an explicit linear solve and the classical
standard errors use s^2 (X'X)^-1 with df n-3. Run: python -I verify_l06.py
"""

from statistics import NormalDist

import numpy as np

N = NormalDist()
SEED, NFIRMS, SHARE = 606, 2000, 0.10
C = np.array([0.05, 0.10, -0.08])
NOISE = 0.01


def sample(seed: int, shift: float, n: int) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    lag = np.exp(rng.normal(np.log(1000.0), 0.6, n))
    drev = lag * rng.normal(0.10, 0.20, n)
    drec = drev * rng.uniform(0.10, 0.30, n) + lag * rng.normal(0.0, 0.02, n)
    ppe = lag * rng.uniform(0.20, 0.60, n)
    manip = np.zeros(n, dtype=bool)
    manip[rng.permutation(n)[: round(SHARE * n)]] = True
    v = rng.standard_normal(n)
    da = shift * manip + NOISE * v
    nda = C[0] / lag + C[1] * (drev - drec) / lag + C[2] * ppe / lag
    total = lag * (nda + da)
    return {"lag": lag, "drev": drev, "drec": drec, "ppe": ppe, "manip": manip, "total": total}


def xy(s: dict[str, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    x = np.column_stack([1 / s["lag"], (s["drev"] - s["drec"]) / s["lag"], s["ppe"] / s["lag"]])
    return x, s["total"] / s["lag"]


def ols(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return np.linalg.solve(x.T @ x, x.T @ y)  # normal equations, independent of lstsq


def classical_se(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    b = ols(x, y)
    e = y - x @ b
    s2 = (e @ e) / (y.size - x.shape[1])
    return np.sqrt(np.diag(s2 * np.linalg.inv(x.T @ x)))


def flags_report(label: str, s: dict[str, np.ndarray], shift_label: str) -> None:
    x, y = xy(s)
    m = s["manip"]
    b_all = ols(x, y)
    da_all = y - x @ b_all
    b_or = ols(x[~m], y[~m])
    da_or = y - x @ b_or
    print(f"{label} coef_all {np.round(b_all, 4).tolist()} coef_nonmanip {np.round(b_or, 4).tolist()}")
    se = classical_se(x[~m], y[~m])
    print(f"{label} se_nonmanip {np.round(se, 4).tolist()} se_a1_over_planted {se[0] / 0.05:.3f}")
    print(f"{label} a1_shift {b_all[0] - b_or[0]:.4f} in_se_units {(b_all[0] - b_or[0]) / se[0]:.3f}")
    print(f"{label} a2_minus_planted {b_or[1] - 0.10:.4f} in_se {(b_or[1] - 0.10) / se[1]:.3f}")
    print(f"{label} a3_minus_planted {b_or[2] + 0.08:.4f} in_se {(b_or[2] + 0.08) / se[2]:.3f}")
    print(f"{label} mean_da_manip {da_all[m].mean():.4f} mean_da_others {da_all[~m].mean():.4f}")
    cut_a = np.quantile(da_all, 0.9)
    cut_o = np.quantile(da_or, 0.9)
    fa = da_all >= cut_a
    fo = da_or >= cut_o
    tp_a, fp_a = fa[m].sum(), fa[~m].sum()
    tp_o, fp_o = fo[m].sum(), fo[~m].sum()
    print(f"{label} all: flagged {fa.sum()} TP {tp_a} FP {fp_a} TPR {tp_a / m.sum():.4f} FPR {fp_a / (~m).sum():.4f}")
    print(f"{label} oracle: flagged {fo.sum()} TP {tp_o} FP {fp_o} TPR {tp_o / m.sum():.4f} FPR {fp_o / (~m).sum():.4f}")
    diff = fa != fo
    print(f"{label} differing_positions {int(diff.sum())} only_in_all {int((fa & ~fo).sum())} only_in_oracle {int((fo & ~fa).sum())}")
    print(f"{label} precision_all {tp_a / fa.sum():.4f} precision_oracle {tp_o / fo.sum():.4f}")


s_strong = sample(SEED, 0.05, NFIRMS)
s_weak = sample(SEED, 0.01, NFIRMS)
flags_report("strong", s_strong, "0.05")
flags_report("weak", s_weak, "0.01")

# se_scaling: classical SE of a1 on non-manipulators, seeds 606-610, n in (2000, 64000)
for n in (2000, 64000):
    ses = []
    for sd in range(606, 611):
        s = sample(sd, 0.05, n)
        x, y = xy(s)
        ses.append(classical_se(x[~s["manip"]], y[~s["manip"]])[0])
    print(f"se_a1_mean n={n} {np.mean(ses):.4f} sqrt_rule {0.2781 * np.sqrt(2000 / n):.4f}")
print(f"n_for_se_0.05 {2000 * (0.2781 / 0.05) ** 2:.0f}")

# Scale invariance (P2): multiply every money item by k
k = 2.5
sk = {key: (val * k if key in ("lag", "drev", "drec", "ppe", "total") else val) for key, val in s_strong.items()}
x1, y1 = xy(s_strong)
x2, y2 = xy(sk)
b1, b2 = ols(x1, y1), ols(x2, y2)
da1 = y1 - x1 @ b1
da2 = y2 - x2 @ b2
print(f"scale k={k}: a1 ratio {b2[0] / b1[0]:.6f} a2 diff {abs(b2[1] - b1[1]):.2e} a3 diff {abs(b2[2] - b1[2]):.2e}")
print(f"scale resid max diff {float(np.max(np.abs(da2 - da1))):.2e}")

# Remark 3.2 and P1
X = np.array([[1.0], [0.5]])
Y = np.array([1.0, 1.0])
b = np.linalg.solve(X.T @ X, X.T @ Y)
e = Y - X @ b
print(f"remark32 b {b.tolist()} fitted {(X @ b).ravel().tolist()} resid {e.tolist()} sum {e.sum():.4f}")
# Proposition 3.1 as printed says 'residuals sum to zero iff 1 in col(X)'. Counter-check for a fixed y:
X2 = np.array([[1.0], [0.5]])
y_fix = np.array([1.0, 0.5])
e2 = y_fix - X2 @ np.linalg.solve(X2.T @ X2, X2.T @ y_fix)
print(f"prop31_fixed_y resid {e2.tolist()} sum {e2.sum():.2e} ones_in_colspace {bool(np.linalg.matrix_rank(np.column_stack([X2, np.ones(2)])) == 1)}")

# Proposition 3.3: the mean error is (X'X)^-1 X'd (3-vector) and the projection X(X'X)^-1 X'd (n-vector)
rng = np.random.default_rng(1)
n = 4000
lagp = np.exp(rng.normal(np.log(1000.0), 0.6, n))
Xp = np.column_stack([1 / lagp, rng.normal(0, 0.1, n) / lagp, rng.uniform(0.2, 0.6, n)])
bstar = np.array([0.05, 0.10, -0.08])
d = 0.01 * (1 / lagp > np.median(1 / lagp)) * 1.0  # a discretionary term that co-moves with 1/A
mean_err = np.linalg.solve(Xp.T @ Xp, Xp.T @ d)
proj = Xp @ mean_err
print(f"prop33 mean_error_shape {mean_err.shape} projection_shape {proj.shape}")
reps = []
for _ in range(400):
    u = rng.normal(0, 0.005, n)
    yv = Xp @ bstar + d + u
    reps.append(ols(Xp, yv) - bstar)
reps = np.array(reps)
print(f"prop33 mc_mean_error {np.round(reps.mean(axis=0), 6).tolist()} formula {np.round(mean_err, 6).tolist()}")

# Proposition 3.1 requires an intercept column check: column of ones in col space
# M1 / M2 / E-series arithmetic
nda = 0.05 / 1000 + 0.10 * (120 - 30) / 1000 - 0.08 * 400 / 1000
print(f"M1 nda {nda:.6f} da {(-30 / 1000) - nda:.6f}")
c = 0.01 * N.inv_cdf(0.95)
print(f"M2 c {c:.6f} detect {N.cdf((0.05 - c) / 0.01):.6f} z_detect {(0.05 - c) / 0.01:.4f}")
print(f"M3 diff {0.3891 - 0.1806:.4f} units {(0.3891 - 0.1806) / 0.2824:.4f}")
print(f"E1 precision {71 / 200:.4f} factor {(71 / 200) / 0.10:.4f} fp_count {0.0717 * 1800:.2f} false_share {129 / 200:.4f}")
print(f"E2 precision {197 / 200:.4f} fp_count {0.0017 * 1800:.2f}")
z_a2 = (0.1031 - 0.10) / 0.0015
two_sided = 2 * (1 - N.cdf(z_a2))
one_sided = 1 - N.cdf(z_a2)
print(f"E3 z {z_a2:.4f} two_sided_tail {two_sided:.4f} one_sided_tail {one_sided:.4f}")
print(f"R1 sqrt_rule_value {0.2781 * np.sqrt(2000 / 64000):.4f}")
print(f"a1_se_ratio_planted {0.2824 / 0.05:.4f}")

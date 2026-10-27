"""Independent re-derivation of the L06 numbers (own code, written from the lab's docstring spec).

Draw order mirrors the lab (lag, drev, drec, ppe, manipulator permutation, noise) so seed 606 reproduces.
Checks: printed coefficients, SEs, the exact a1 decomposition, the conditional-mean bias of a1 (Monte Carlo over
manipulator and noise draws with X fixed), the SE scaling, and the flag counts.
"""

import math

import numpy as np

C = np.array([0.05, 0.10, -0.08])
SHIFT_STRONG, SHIFT_WEAK = 0.05, 0.01
NOISE_SD = 0.01
MANIP = 0.10
N = 2000


def draw_x(seed: int, n: int = N):
    rng = np.random.default_rng(seed)
    lag = np.exp(rng.normal(np.log(1000.0), 0.6, n))
    drev = lag * rng.normal(0.10, 0.20, n)
    drec = drev * rng.uniform(0.10, 0.30, n) + lag * rng.normal(0.0, 0.02, n)
    ppe = lag * rng.uniform(0.20, 0.60, n)
    perm = rng.permutation(n)
    manip = np.zeros(n, dtype=bool)
    manip[perm[: round(MANIP * n)]] = True
    noise = rng.standard_normal(n)
    return lag, drev, drec, ppe, manip, noise


def xmat(lag, drev, drec, ppe):
    return np.column_stack([1.0 / lag, (drev - drec) / lag, ppe / lag])


def ols(x, y):
    return np.linalg.solve(x.T @ x, x.T @ y)


def run(seed: int, shift: float):
    lag, drev, drec, ppe, manip, noise_raw = draw_x(seed)
    x = xmat(lag, drev, drec, ppe)
    noise = NOISE_SD * noise_raw
    planted = shift * manip.astype(float)
    y = x @ C + planted + noise  # total/lag, ratio units
    b_all = ols(x, y)
    nm = ~manip
    b_nm = ols(x[nm], y[nm])
    # classical SE on nm rows
    xk, yk = x[nm], y[nm]
    resid = yk - xk @ b_nm
    s2 = resid @ resid / (yk.size - 3)
    se_nm = np.sqrt(np.diag(s2 * np.linalg.inv(xk.T @ xk)))
    xtx_inv = np.linalg.inv(x.T @ x)
    proj_planted = (xtx_inv @ x.T @ planted)[0]
    proj_noise = (xtx_inv @ x.T @ noise)[0]
    dev_nm = (np.linalg.inv(xk.T @ xk) @ xk.T @ noise[nm])[0]
    resid_decomp = (b_all[0] - b_nm[0]) - (proj_planted + proj_noise - dev_nm)
    # conditional mean given X: E[planted | X] = shift * MANIP (a constant); bias = (X'X)^-1 X' E[d|X]
    cm = (xtx_inv @ x.T @ np.full(N, shift * MANIP))[0]
    # flags
    da_all = y - x @ b_all
    da_or = y - x @ b_nm
    cut = np.quantile(da_all, 1 - MANIP)
    f_all = da_all >= cut
    cut_o = np.quantile(da_or, 1 - MANIP)
    f_or = da_or >= cut_o
    out = dict(
        b_all=b_all, b_nm=b_nm, se_nm=se_nm, diff=b_all[0] - b_nm[0],
        proj_planted=proj_planted, proj_noise=proj_noise, dev_nm=dev_nm, resid=resid_decomp, cond_mean=cm,
        tpr=np.mean(f_all[manip]), fpr=np.mean(f_all[nm]), tp=int(np.sum(f_all & manip)),
        flags_only_all=int(np.sum(f_all & ~f_or)), flags_only_or=int(np.sum(f_or & ~f_all)),
        mean_da_m=float(da_all[manip].mean()), mean_da_o=float(da_all[nm].mean()),
        tpr_o=float(np.mean(f_or[manip])), fpr_o=float(np.mean(f_or[nm])),
    )
    return out, (x, lag, drev, drec, ppe)


for label, shift in [("strong", SHIFT_STRONG), ("weak", SHIFT_WEAK)]:
    o, _ = run(606, shift)
    print(f"{label} b_all {o['b_all'][0]:.4f} {o['b_all'][1]:.4f} {o['b_all'][2]:.4f}")
    print(f"{label} b_nm {o['b_nm'][0]:.4f} {o['b_nm'][1]:.4f} {o['b_nm'][2]:.4f}  se_nm {o['se_nm'][0]:.4f} {o['se_nm'][1]:.4f} {o['se_nm'][2]:.4f}")
    print(f"{label} diff_unrounded {o['diff']:.6f} proj_planted {o['proj_planted']:.4f} proj_noise {o['proj_noise']:.4f} dev_nm {o['dev_nm']:.4f} resid {o['resid']:.2e}")
    print(f"{label} cond_mean_bias_a1 {o['cond_mean'][0] if np.ndim(o['cond_mean']) else o['cond_mean']:.4f}")
    print(f"{label} tpr_all {o['tpr']:.4f} fpr_all {o['fpr']:.4f} tp {o['tp']} tpr_oracle {o['tpr_o']:.4f} fpr_oracle {o['fpr_o']:.4f}")
    print(f"{label} flags_only_all {o['flags_only_all']} flags_only_oracle {o['flags_only_or']} mean_da_m {o['mean_da_m']:.4f} mean_da_o {o['mean_da_o']:.4f}")
    print(f"{label} z_a2 {(o['b_nm'][1]-0.10)/o['se_nm'][1]:.3f} unit_se_ratio_a1 {o['diff']/o['se_nm'][0]:.4f}  0.2824/0.05 {o['se_nm'][0]/0.05:.3f}")

# Monte Carlo: E[a1_all - a1_nm | X] and E[a1_all | X] - C with X fixed at seed 606, manipulators and noise redrawn.
lag, drev, drec, ppe, _, _ = draw_x(606)
x = xmat(lag, drev, drec, ppe)
xtx_inv = np.linalg.inv(x.T @ x)
rng = np.random.default_rng(12345)
R = 4000
diffs = np.empty(R)
bias_all = np.empty(R)
for r in range(R):
    manip = np.zeros(N, dtype=bool)
    manip[rng.permutation(N)[:200]] = True
    noise = NOISE_SD * rng.standard_normal(N)
    y = x @ C + SHIFT_STRONG * manip + noise
    b_all = ols(x, y)
    b_nm = ols(x[~manip], y[~manip])
    diffs[r] = b_all[0] - b_nm[0]
    bias_all[r] = b_all[0] - C[0]
print(f"MC_R {R} strong E[a1_all-a1_nm|X] {diffs.mean():.4f} se {diffs.std(ddof=1)/math.sqrt(R):.4f}")
print(f"MC_R {R} strong E[a1_all-C|X] {bias_all.mean():.4f} se {bias_all.std(ddof=1)/math.sqrt(R):.4f}")
print(f"MC_R {R} strong sd_of_diff {diffs.std(ddof=1):.4f}")
print(f"analytic_cond_mean a1 {(xtx_inv @ x.T @ np.full(N, 0.005))[0]:.4f}")

# SE scaling over seeds 606-610 on non-manipulator rows
for n in (2000, 64000):
    ses = []
    rows = []
    for sd in range(606, 611):
        lag, drev, drec, ppe, manip, _ = draw_x(sd, n)
        x = xmat(lag, drev, drec, ppe)
        nm = ~manip
        xk = x[nm]
        # classical SE needs y; y only enters through residuals, so regenerate noise exactly as the lab does
        noise_raw = np.random.default_rng(sd)  # placeholder, replaced below
        rng2 = np.random.default_rng(sd)
        rng2.normal(np.log(1000.0), 0.6, n); rng2.normal(0.10, 0.20, n); rng2.uniform(0.10, 0.30, n)
        rng2.normal(0.0, 0.02, n); rng2.uniform(0.20, 0.60, n); rng2.permutation(n)
        nz = rng2.standard_normal(n)
        y = x @ C + SHIFT_STRONG * manip + NOISE_SD * nz
        yk = y[nm]
        b = ols(xk, yk)
        resid = yk - xk @ b
        s2 = resid @ resid / (yk.size - 3)
        ses.append(math.sqrt(s2 * np.linalg.inv(xk.T @ xk)[0, 0]))
        rows.append(int(nm.sum()))
    print(f"se_scaling firms {n} nm_rows {rows[0]} seeds 5 mean_se_a1 {np.mean(ses):.4f}")
print(f"rule_rows {0.2781*math.sqrt(1800/57600):.4f}  rows_for_0.05 {1800*(0.2781/0.05)**2:.0f}  firm_years {1800*(0.2781/0.05)**2/0.9:.0f}")

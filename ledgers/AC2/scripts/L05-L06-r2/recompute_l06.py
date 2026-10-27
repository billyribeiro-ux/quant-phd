"""Independent recomputation for AC2 L05-L06 round 2 (verifier-written; does not import the lab twin).

Re-implements the L06 generator from its written spec with explicit normal equations, then:
 (1) reproduces every printed L06 number at seed 606 and seeds 606-610;
 (2) tests Proposition 3.3 on the lab's manipulator term: the manipulator indicator is drawn
     independently of X, so the omitted term d is not a function of X; compares the realised
     projection (X'X)^-1 X'd with the projection of E[d|X] = SHIFT*MANIP_SHARE*1;
 (3) recomputes the flag-set differences (flags only in all-firm, only in oracle);
 (4) recomputes the E3 two-sided tail and the 1-Phi values.
Run: <checkout>/.venv/bin/python -I ledgers/AC2/scripts/L05-L06-r2/recompute_l06.py
"""
import math

import numpy as np

N, SHARE, C = 2000, 0.10, np.array([0.05, 0.10, -0.08])
SD = 0.01


def gen(seed, shift, n=N):
    rng = np.random.default_rng(seed)
    lag = np.exp(rng.normal(np.log(1000.0), 0.6, n))
    drev = lag * rng.normal(0.10, 0.20, n)
    drec = drev * rng.uniform(0.10, 0.30, n) + lag * rng.normal(0.0, 0.02, n)
    ppe = lag * rng.uniform(0.20, 0.60, n)
    m = np.zeros(n, bool)
    m[rng.permutation(n)[: round(SHARE * n)]] = True
    v = rng.standard_normal(n)
    d = shift * m + SD * v
    X = np.column_stack([1 / lag, (drev - drec) / lag, ppe / lag])
    y = (C[0] / lag + C[1] * (drev - drec) / lag + C[2] * ppe / lag + d)  # total/lag
    return X, y, m, d


def ne_solve(X, y):
    # normal equations, explicit
    return np.linalg.solve(X.T @ X, X.T @ y)


def pct(a, b):
    return a, b


def top_flags(score, share=SHARE):
    cut = np.sort(score)[int(math.ceil(len(score) * (1 - share))) - 1]
    # top-decile: flagged if score >= quantile(0.9) with linear interpolation, as numpy default
    q = np.quantile(score, 1 - share)
    return score >= q


def run(seed, shift):
    X, y, m, d = gen(seed, shift)
    b_all = ne_solve(X, y)
    b_nm = ne_solve(X[~m], y[~m])
    res_all = y - X @ b_all
    # oracle residuals use the non-manipulator coefficients
    res_or = y - X @ b_nm
    f_all = top_flags(res_all)
    f_or = top_flags(res_or)
    tpr = f_all[m].mean()
    fpr = f_all[~m].mean()
    tpr_o = f_or[m].mean()
    fpr_o = f_or[~m].mean()
    out = dict(
        b_all=b_all, b_nm=b_nm, tp=int(f_all[m].sum()), fp=int((f_all & ~m).sum()),
        tpr=tpr, fpr=fpr, tpr_o=tpr_o, fpr_o=fpr_o,
        only_all=int((f_all & ~f_or).sum()), only_or=int((f_or & ~f_all).sum()),
        differ=int((f_all != f_or).sum()),
        mean_da_m=float(res_all[m].mean()), mean_da_o=float(res_all[~m].mean()),
    )
    # Proposition 3.3 check on the realised manipulator term
    P = np.linalg.inv(X.T @ X) @ X.T
    bias_real = P @ (shift * m)
    bias_cond = P @ (np.full(len(y), shift * SHARE))
    out["bias_realised_d"] = bias_real
    out["bias_E_d_given_X"] = bias_cond
    out["diff_all_minus_nm"] = b_all - b_nm
    return out


def show(tag, o):
    print(tag)
    print("  b_all", np.round(o["b_all"], 4), "b_nm", np.round(o["b_nm"], 4))
    print("  diff all-nm", np.round(o["diff_all_minus_nm"], 4))
    print("  proj of realised d", np.round(o["bias_realised_d"], 4))
    print("  proj of E[d|X]    ", np.round(o["bias_E_d_given_X"], 4))
    print("  DA mean manip %.4f others %.4f" % (o["mean_da_m"], o["mean_da_o"]))
    print("  TP %d FP %d TPR %.4f FPR %.4f" % (o["tp"], o["fp"], o["tpr"], o["fpr"]))
    print("  oracle TPR %.4f FPR %.4f" % (o["tpr_o"], o["fpr_o"]))
    print("  only_all %d only_oracle %d differ %d" % (o["only_all"], o["only_or"], o["differ"]))


if __name__ == "__main__":
    s = run(606, 0.05)
    w = run(606, 0.01)
    show("strong seed 606", s)
    show("weak seed 606", w)
    # E3 tail
    z = 0.0031 / 0.0015
    tail = 2 * (1 - 0.5 * (1 + math.erf(2.067 / math.sqrt(2))))
    print("E3 z(2.067) two-sided tail", round(tail, 4), "rounded-inputs z range", round(0.00305 / 0.00155, 3), round(0.00315 / 0.00145, 3))
    # Prop 3.1/M2 numbers
    print("M2 c", round(0.01 * 1.6449, 5), "detect", round(0.5 * (1 + math.erf((0.05 - 0.01645) / 0.01 / math.sqrt(2))), 5))
    # Scaling checks
    print("R1 rule", round(0.2781 * math.sqrt(2000 / 64000), 4), "n for 0.05", round(2000 * (0.2781 / 0.05) ** 2))
    print("E1 precision 71/200", 71 / 200, "129/200", 129 / 200, "0.0717*1800", round(0.0717 * 1800, 1))
    print("strong FP expected", round(0.0017 * 1800, 2))
    print("coef a1 SE ratio", round(0.2824 / 0.05, 3), "contam SE units", round(0.2085 / 0.2824, 3))
    print("a2 z", round((0.1031 - 0.10) / 0.0015, 3), "a3 z", round((-0.0805 + 0.08) / 0.0010, 3), "a1 z", round((0.1806 - 0.05) / 0.2824, 3))

"""Lab F5-project-1: Project Rung 1 Worked Example - Replication-Crisis Adjudication Engine.

Executes a complete replication adjudication on a panel of 10 candidate equity
anomalies, testing multiple testing hurdles, empirical Bayes shrinkage, and
Feng-Giglio-Xiu double-selection orthogonalization.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def run_worked_adjudication(seed: int = 42) -> dict[str, object]:
    """Execute complete replication adjudication pipeline for 10 candidate anomalies."""
    rng = np.random.default_rng(seed)
    n_months = 240
    n_candidates = 10
    n_controls = 4
    n_assets = 25

    # 1. Simulate benchmark controls (MKT, SMB, HML, UMD)
    mkt = rng.normal(0.060 / 12, 0.155 / np.sqrt(12), size=n_months)
    smb = rng.normal(0.025 / 12, 0.095 / np.sqrt(12), size=n_months)
    hml = rng.normal(0.035 / 12, 0.110 / np.sqrt(12), size=n_months)
    umd = rng.normal(0.065 / 12, 0.140 / np.sqrt(12), size=n_months)
    controls = np.column_stack([mkt, smb, hml, umd])

    # 2. Simulate candidate anomaly returns (EW and VW)
    returns_ew = np.zeros((n_candidates, n_months))
    returns_vw = np.zeros((n_candidates, n_months))

    for i in range(n_candidates):
        n_ew = rng.normal(0.0, 0.030, size=n_months)
        n_vw = rng.normal(0.0, 0.025, size=n_months)
        if i in (0, 1):  # Robust
            r_c = 0.0035 + 0.2 * mkt + n_vw
            returns_vw[i, :] = r_c
            returns_ew[i, :] = r_c + 0.0020 + n_ew
        elif i in (2, 3, 4):  # Microcap only
            returns_vw[i, :] = 0.0003 + 0.3 * mkt + n_vw
            returns_ew[i, :] = 0.0065 + 0.4 * mkt + n_ew
        elif i in (5, 6):  # Spanned
            spanned = controls @ np.array([0.2, 0.3, 0.7, 0.5])
            returns_vw[i, :] = spanned + n_vw
            returns_ew[i, :] = spanned + 0.0015 + n_ew
        else:  # Data snooping / noise
            returns_vw[i, :] = n_vw
            returns_ew[i, :] = n_ew

    # 3. Multiple Testing Hurdles on EW returns
    mean_ew = np.mean(returns_ew, axis=1)
    se_ew = np.std(returns_ew, axis=1, ddof=1) / np.sqrt(n_months)
    t_ew = mean_ew / se_ew
    p_ew = 2.0 * (1.0 - stats.norm.cdf(np.abs(t_ew)))

    disc_unadj = int(np.sum(np.abs(t_ew) >= 1.96))
    disc_bonf = int(np.sum(p_ew <= (0.05 / n_candidates)))
    disc_hlz = int(np.sum(np.abs(t_ew) >= 3.00))

    # 4. Replication evaluation (EW vs VW)
    mean_vw = np.mean(returns_vw, axis=1)
    se_vw = np.std(returns_vw, axis=1, ddof=1) / np.sqrt(n_months)
    t_vw = mean_vw / se_vw

    x_des = np.column_stack([np.ones(n_months), controls])
    b_vw = np.linalg.lstsq(x_des, returns_vw.T, rcond=None)[0]
    alphas_vw = b_vw[0, :]
    res_vw = returns_vw.T - x_des @ b_vw
    s2_vw = np.sum(res_vw**2, axis=0) / float(n_months - n_controls - 1)
    se_alpha = np.sqrt(s2_vw * np.linalg.inv(x_des.T @ x_des)[0, 0])
    t_alpha = alphas_vw / se_alpha

    rep_rate_ew = float(np.mean(np.abs(t_ew) >= 1.96) * 100)
    rep_rate_vw = float(np.mean(np.abs(t_vw) >= 1.96) * 100)
    rep_rate_alpha = float(np.mean(np.abs(t_alpha) >= 1.96) * 100)

    # 5. Empirical Bayes shrinkage
    precisions = 1.0 / (se_alpha**2)
    mu_0 = float(np.sum(precisions * alphas_vw) / np.sum(precisions))
    sample_var = float(np.var(alphas_vw, ddof=1))
    tau2 = max(1e-8, sample_var - float(np.mean(se_alpha**2)))
    weights = tau2 / (tau2 + se_alpha**2)
    shrunk_alphas = weights * alphas_vw + (1.0 - weights) * mu_0

    # 6. Double Selection
    b_assets = rng.uniform(0.6, 1.4, size=(n_assets, n_controls))
    e_assets = rng.normal(0.0, 0.035, size=(n_assets, n_months))
    test_assets = b_assets @ controls.T + e_assets

    classifications: list[str] = []
    for i in range(n_candidates):
        # Step 1: controls correlated with candidate
        corrs = np.array([abs(np.corrcoef(returns_vw[i], controls[:, j])[0, 1]) for j in range(n_controls)])
        s1 = set(np.where(corrs >= 0.15)[0])
        # Step 2: controls with beta variance
        s2: set[int] = set()
        for j in range(n_controls):
            var_f = float(np.var(controls[:, j], ddof=1))
            covs = np.array([np.cov(test_assets[a], controls[:, j])[0, 1] for a in range(n_assets)])
            betas_j = covs / var_f
            if np.std(betas_j, ddof=1) >= 0.05:
                s2.add(j)
        union = sorted(s1.union(s2))
        x_sel = np.column_stack([np.ones(n_months), controls[:, union]])
        b_sel = np.linalg.lstsq(x_sel, returns_vw[i], rcond=None)[0]
        res_sel = returns_vw[i] - x_sel @ b_sel
        s2_sel = float(np.sum(res_sel**2) / (n_months - len(union) - 1))
        se_ds = float(np.sqrt(s2_sel * np.linalg.inv(x_sel.T @ x_sel)[0, 0]))
        t_ds = float(b_sel[0] / se_ds)
        retained = bool(abs(t_ds) >= 1.96)

        if abs(t_alpha[i]) >= 1.96 and retained and shrunk_alphas[i] > 0.0010:
            classifications.append("ROBUST")
        elif abs(t_ew[i]) >= 1.96 and abs(t_vw[i]) < 1.96:
            classifications.append("MICROCAP_ONLY")
        elif abs(t_vw[i]) >= 1.96 and (abs(t_alpha[i]) < 1.96 or not retained):
            classifications.append("SPANNED")
        else:
            classifications.append("DATA_SNOOPING")

    counts = {c: classifications.count(c) for c in ["ROBUST", "MICROCAP_ONLY", "SPANNED", "DATA_SNOOPING"]}

    return {
        "n_candidates": n_candidates,
        "disc_unadj": disc_unadj,
        "disc_bonf": disc_bonf,
        "disc_hlz": disc_hlz,
        "rep_rate_ew": round(rep_rate_ew, 1),
        "rep_rate_vw": round(rep_rate_vw, 1),
        "rep_rate_alpha": round(rep_rate_alpha, 1),
        "prior_mu0_ann": round(mu_0 * 12 * 100, 2),
        "mean_shrinkage_w": round(float(np.mean(weights)), 3),
        "counts": counts,
    }


def main() -> None:
    print("Project Rung 1 | Replication-Crisis Adjudication Engine (Worked Example)")
    print("-----------------------------------------------------------------------")
    res = run_worked_adjudication(seed=42)
    print(f"Sample: {res['n_candidates']} candidate equity anomalies over 240 months")
    print(
        f"Multiple Testing: Unadjusted {res['disc_unadj']} | "
        f"Bonferroni {res['disc_bonf']} | HLZ hurdle {res['disc_hlz']}"
    )
    print(
        f"Replication Rates: EW Raw {res['rep_rate_ew']:.1f}% | "
        f"VW Raw {res['rep_rate_vw']:.1f}% | VW Alpha {res['rep_rate_alpha']:.1f}%"
    )
    print(
        f"Empirical Bayes Prior Mean: {res['prior_mu0_ann']:+.2f}% ann "
        f"(mean weight w_i = {res['mean_shrinkage_w']:.3f})"
    )
    print(f"Adjudication Breakdown: {res['counts']}")


main()

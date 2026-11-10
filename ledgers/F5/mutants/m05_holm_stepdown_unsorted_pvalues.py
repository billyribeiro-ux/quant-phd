"""Student error: fails to sort p-values in ascending order in Holm step-down procedure."""

from __future__ import annotations

import numpy as np
from scipy import stats


def multiple_testing_hurdles(
    t_stats: np.ndarray,
    alpha: float = 0.05,
) -> dict[str, object]:
    m = len(t_stats)
    p_values = 2.0 * (1.0 - stats.norm.cdf(np.abs(t_stats)))

    unadjusted_mask = np.abs(t_stats) >= 1.96

    alpha_bonf = alpha / m
    crit_bonf = float(stats.norm.ppf(1.0 - alpha_bonf / 2.0))
    bonferroni_mask = p_values <= alpha_bonf

    # BUG: compares un-sorted p_values to holm thresholds
    holm_thresholds = alpha / (m - np.arange(m))
    holm_passed = p_values <= holm_thresholds
    holm_mask = np.zeros(m, dtype=bool)
    if np.any(holm_passed):
        first_fail = int(np.argmin(holm_passed)) if not np.all(holm_passed) else m
        holm_mask[:first_fail] = True

    sort_idx = np.argsort(p_values)
    sorted_p = p_values[sort_idx]
    bh_thresholds = (np.arange(1, m + 1) / m) * alpha
    bh_passed = sorted_p <= bh_thresholds
    bh_mask = np.zeros(m, dtype=bool)
    if np.any(bh_passed):
        max_idx = int(np.max(np.where(bh_passed)[0]))
        bh_mask[sort_idx[: max_idx + 1]] = True

    hlz_mask = np.abs(t_stats) >= 3.00

    return {
        "m_tests": int(m),
        "unadjusted_mask": unadjusted_mask,
        "n_unadjusted": int(np.sum(unadjusted_mask)),
        "crit_bonferroni": float(crit_bonf),
        "bonferroni_mask": bonferroni_mask,
        "n_bonferroni": int(np.sum(bonferroni_mask)),
        "holm_mask": holm_mask,
        "n_holm": int(np.sum(holm_mask)),
        "bh_mask": bh_mask,
        "n_bh": int(np.sum(bh_mask)),
        "hlz_mask": hlz_mask,
        "n_hlz": int(np.sum(hlz_mask)),
    }


def evaluate_replication(
    returns_ew: np.ndarray,
    returns_vw: np.ndarray,
    controls: np.ndarray,
) -> dict[str, object]:
    n_candidates, t_obs = returns_ew.shape
    k_controls = controls.shape[1]
    x_des = np.column_stack([np.ones(t_obs), controls])
    inv_xtx = np.linalg.inv(x_des.T @ x_des)

    mean_ew = np.mean(returns_ew, axis=1)
    se_ew = np.std(returns_ew, axis=1, ddof=1) / np.sqrt(t_obs)
    t_ew_raw = mean_ew / se_ew
    pass_ew_raw = np.abs(t_ew_raw) >= 1.96

    mean_vw = np.mean(returns_vw, axis=1)
    se_vw = np.std(returns_vw, axis=1, ddof=1) / np.sqrt(t_obs)
    t_vw_raw = mean_vw / se_vw
    pass_vw_raw = np.abs(t_vw_raw) >= 1.96

    b_hat_vw = np.linalg.lstsq(x_des, returns_vw.T, rcond=None)[0]
    alphas_vw = b_hat_vw[0, :]
    residuals_vw = returns_vw.T - x_des @ b_hat_vw
    res_var_vw = np.sum(residuals_vw**2, axis=0) / float(t_obs - k_controls - 1)
    se_alpha_vw = np.sqrt(res_var_vw * inv_xtx[0, 0])
    t_alpha_vw = alphas_vw / se_alpha_vw

    pass_vw_alpha = np.abs(t_alpha_vw) >= 1.96
    pass_vw_conservative = np.abs(t_alpha_vw) >= 3.00

    rep_rate_ew_raw = float(np.mean(pass_ew_raw) * 100.0)
    rep_rate_vw_raw = float(np.mean(pass_vw_raw) * 100.0)
    rep_rate_vw_alpha = float(np.mean(pass_vw_alpha) * 100.0)
    rep_rate_vw_conservative = float(np.mean(pass_vw_conservative) * 100.0)

    return {
        "n_candidates": int(n_candidates),
        "t_ew_raw": t_ew_raw,
        "pass_ew_raw": pass_ew_raw,
        "rep_rate_ew_raw": float(rep_rate_ew_raw),
        "t_vw_raw": t_vw_raw,
        "pass_vw_raw": pass_vw_raw,
        "rep_rate_vw_raw": float(rep_rate_vw_raw),
        "alphas_vw": alphas_vw,
        "se_alpha_vw": se_alpha_vw,
        "t_alpha_vw": t_alpha_vw,
        "pass_vw_alpha": pass_vw_alpha,
        "rep_rate_vw_alpha": float(rep_rate_vw_alpha),
        "pass_vw_conservative": pass_vw_conservative,
        "rep_rate_vw_conservative": float(rep_rate_vw_conservative),
    }


def empirical_bayes_shrinkage(
    alphas: np.ndarray,
    standard_errors: np.ndarray,
) -> dict[str, object]:
    n = len(alphas)
    precisions = 1.0 / (standard_errors**2)
    mu_0 = float(np.sum(precisions * alphas) / np.sum(precisions))
    sample_var = float(np.var(alphas, ddof=1)) if n > 1 else float(alphas[0] ** 2)
    mean_se2 = float(np.mean(standard_errors**2))
    tau2 = max(1e-8, sample_var - mean_se2)
    tau = float(np.sqrt(tau2))

    weights = tau2 / (tau2 + standard_errors**2)
    shrunk_alphas = weights * alphas + (1.0 - weights) * mu_0

    return {
        "prior_mean": float(mu_0),
        "prior_tau": float(tau),
        "prior_tau2": float(tau2),
        "weights": weights,
        "mean_weight": float(np.mean(weights)),
        "shrunk_alphas": shrunk_alphas,
    }


def double_selection_test(
    candidate_return: np.ndarray,
    controls: np.ndarray,
    test_assets: np.ndarray,
    corr_thresh: float = 0.15,
) -> dict[str, object]:
    t_obs, k_controls = controls.shape
    n_assets = test_assets.shape[0]

    corrs = np.zeros(k_controls)
    for j in range(k_controls):
        corrs[j] = float(np.corrcoef(candidate_return, controls[:, j])[0, 1])
    selected_step1 = set(np.where(np.abs(corrs) >= corr_thresh)[0])

    selected_step2: set[int] = set()
    for j in range(k_controls):
        var_fj = float(np.var(controls[:, j], ddof=1))
        if var_fj > 1e-10:
            covs = np.array([float(np.cov(test_assets[i], controls[:, j])[0, 1]) for i in range(n_assets)])
            betas_j = covs / var_fj
            if np.std(betas_j, ddof=1) >= 0.05:
                selected_step2.add(j)

    selected_union = sorted(selected_step1.union(selected_step2))
    n_selected = len(selected_union)

    if n_selected == 0:
        orth_alpha = float(np.mean(candidate_return))
        se_orth = float(np.std(candidate_return, ddof=1) / np.sqrt(t_obs))
        t_stat = float(orth_alpha / se_orth)
    else:
        x_sel = np.column_stack([np.ones(t_obs), controls[:, selected_union]])
        b_proj = np.linalg.lstsq(x_sel, candidate_return, rcond=None)[0]
        orth_alpha = float(b_proj[0])
        res_orth = candidate_return - x_sel @ b_proj
        res_var = float(np.sum(res_orth**2) / (t_obs - n_selected - 1))
        inv_xx = np.linalg.inv(x_sel.T @ x_sel)
        se_orth = float(np.sqrt(res_var * inv_xx[0, 0]))
        t_stat = float(orth_alpha / se_orth)

    is_retained = bool(abs(t_stat) >= 1.96)

    return {
        "selected_step1": sorted(selected_step1),
        "selected_step2": sorted(selected_step2),
        "selected_union": selected_union,
        "n_selected": int(n_selected),
        "orthogonal_alpha": float(orth_alpha),
        "se_orthogonal": float(se_orth),
        "t_stat": float(t_stat),
        "is_retained": is_retained,
    }


def adjudicate_factors(instance: dict[str, object]) -> dict[str, object]:
    returns_ew = np.asarray(instance["returns_ew"], dtype=np.float64)
    returns_vw = np.asarray(instance["returns_vw"], dtype=np.float64)
    controls = np.asarray(instance["controls"], dtype=np.float64)
    test_assets = np.asarray(instance["test_assets"], dtype=np.float64)
    raw_names = instance["candidate_names"]
    candidate_names: list[str] = (
        [str(x) for x in raw_names] if isinstance(raw_names, (list, tuple, np.ndarray)) else []
    )
    n_candidates = len(candidate_names)

    rep = evaluate_replication(returns_ew, returns_vw, controls)
    t_ew_raw = np.asarray(rep["t_ew_raw"], dtype=np.float64)
    alphas_vw = np.asarray(rep["alphas_vw"], dtype=np.float64)
    se_alpha_vw = np.asarray(rep["se_alpha_vw"], dtype=np.float64)
    pass_vw_alpha = np.asarray(rep["pass_vw_alpha"], dtype=bool)
    pass_ew_raw = np.asarray(rep["pass_ew_raw"], dtype=bool)
    pass_vw_raw = np.asarray(rep["pass_vw_raw"], dtype=bool)

    mt = multiple_testing_hurdles(t_ew_raw, alpha=0.05)
    bayes = empirical_bayes_shrinkage(alphas_vw, se_alpha_vw)
    shrunk_alphas = np.asarray(bayes["shrunk_alphas"], dtype=np.float64)

    classifications: list[str] = []
    ds_retained = np.zeros(n_candidates, dtype=bool)
    ds_t_stats = np.zeros(n_candidates, dtype=np.float64)

    for i in range(n_candidates):
        ds_res = double_selection_test(returns_vw[i, :], controls, test_assets)
        ds_retained[i] = bool(ds_res["is_retained"])
        t_stat_val = ds_res["t_stat"]
        ds_t_stats[i] = float(t_stat_val) if isinstance(t_stat_val, (int, float, np.floating)) else 0.0

        if pass_vw_alpha[i] and ds_retained[i] and shrunk_alphas[i] > 0.0010:
            classifications.append("ROBUST")
        elif pass_ew_raw[i] and not pass_vw_raw[i]:
            classifications.append("MICROCAP_ONLY")
        elif pass_vw_raw[i] and (not pass_vw_alpha[i] or not ds_retained[i]):
            classifications.append("SPANNED")
        else:
            classifications.append("DATA_SNOOPING")

    counts = {
        "ROBUST": int(classifications.count("ROBUST")),
        "MICROCAP_ONLY": int(classifications.count("MICROCAP_ONLY")),
        "SPANNED": int(classifications.count("SPANNED")),
        "DATA_SNOOPING": int(classifications.count("DATA_SNOOPING")),
    }

    return {
        "candidate_names": candidate_names,
        "replication": rep,
        "multiple_testing": mt,
        "bayes_shrinkage": bayes,
        "ds_retained": ds_retained,
        "ds_t_stats": ds_t_stats,
        "classifications": classifications,
        "classification_counts": counts,
    }

"""Reference implementation of the CR3 credit cycle & macro-credit module.

Implements all six core analytical functions:
1. decompose_credit_spread: Gilchrist-Zakrajšek (2012) cross-sectional spread regression & EBP.
2. construct_credit_sentiment_index: López-Salido, Stein & Zakrajšek (2017) sentiment index.
3. predict_spread_reversals: Predictive regressions with Newey-West HAC inference.
4. fit_recession_probit: Maximum likelihood logistic/probit recession forecasting.
5. evaluate_recession_forecasts: Brier score, ROC-AUC, and classification metrics.
6. simulate_leveraged_loan_waterfall: Cov-lite vs maintenance debt recovery waterfall.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
from scipy import optimize, stats


def validate_bond_data(bond_data: dict[str, list[float]]) -> None:
    """Validate cross-sectional bond panel data."""
    required = ["spread_bps", "duration", "coupon", "amount_outstanding", "merton_edf", "industry_id"]
    for k in required:
        if k not in bond_data:
            raise ValueError(f"Missing required key in bond_data: {k}")
        if not isinstance(bond_data[k], list):
            raise TypeError(f"bond_data['{k}'] must be a list")

    n = len(bond_data["spread_bps"])
    if n < 10:
        raise ValueError(f"bond_data requires at least 10 bonds for regression, got {n}")

    for k in required:
        if len(bond_data[k]) != n:
            raise ValueError(f"Length mismatch: {k} has length {len(bond_data[k])}, expected {n}")

    for i in range(n):
        if bond_data["spread_bps"][i] <= 0:
            raise ValueError(f"spread_bps[{i}] must be strictly positive, got {bond_data['spread_bps'][i]}")
        if bond_data["duration"][i] <= 0:
            raise ValueError(f"duration[{i}] must be strictly positive, got {bond_data['duration'][i]}")
        if bond_data["coupon"][i] < 0:
            raise ValueError(f"coupon[{i}] must be non-negative, got {bond_data['coupon'][i]}")
        if bond_data["amount_outstanding"][i] <= 0:
            raise ValueError(f"amount_outstanding[{i}] must be strictly positive")
        edf = bond_data["merton_edf"][i]
        if not (0.0 < edf < 1.0):
            raise ValueError(f"merton_edf[{i}] must be in (0, 1), got {edf}")


def validate_sentiment_inputs(
    hy: list[float],
    spreads: list[float],
    ebp: list[float],
    weights: list[float] | None,
) -> None:
    """Validate credit market sentiment inputs."""
    if not (isinstance(hy, list) and isinstance(spreads, list) and isinstance(ebp, list)):
        raise TypeError("hy, spreads, and ebp must be lists of floats")
    n = len(hy)
    if n < 8:
        raise ValueError(f"Sentiment time series requires at least 8 periods, got {n}")
    if len(spreads) != n or len(ebp) != n:
        raise ValueError(f"Length mismatch among sentiment series: {n}, {len(spreads)}, {len(ebp)}")

    for i in range(n):
        if not math.isfinite(hy[i]) or not math.isfinite(spreads[i]) or not math.isfinite(ebp[i]):
            raise ValueError(f"Non-finite value at index {i}")
        if not (0.0 <= hy[i] <= 1.0):
            raise ValueError(f"High-yield issuance share at index {i} must be in [0, 1], got {hy[i]}")
        if spreads[i] <= 0:
            raise ValueError(f"Credit spread at index {i} must be positive, got {spreads[i]}")

    if weights is not None:
        if len(weights) != 3:
            raise ValueError(f"weights must have length 3, got {len(weights)}")
        if any(w < 0 for w in weights) or sum(weights) <= 0:
            raise ValueError("weights must be non-negative and sum to positive value")


def validate_recession_inputs(
    indicator: list[float],
    term_spread: list[float],
    recessions: list[int],
) -> None:
    """Validate recession probit regression inputs."""
    n = len(indicator)
    if n < 15:
        raise ValueError(f"Recession regression requires at least 15 observations, got {n}")
    if len(term_spread) != n or len(recessions) != n:
        raise ValueError(f"Length mismatch in recession series: {n}, {len(term_spread)}, {len(recessions)}")

    n_rec = sum(recessions)
    if n_rec == 0 or n_rec == n:
        raise ValueError("recessions series must contain both 0 and 1 outcomes")

    for i in range(n):
        if recessions[i] not in (0, 1):
            raise ValueError(f"recession_flags[{i}] must be 0 or 1, got {recessions[i]}")
        if not math.isfinite(indicator[i]) or not math.isfinite(term_spread[i]):
            raise ValueError(f"Non-finite predictor at index {i}")


def validate_evaluation_inputs(y_true: list[int], y_prob: list[float], threshold: float) -> None:
    """Validate forecast evaluation inputs."""
    n = len(y_true)
    if n < 2:
        raise ValueError(f"Evaluation requires at least 2 observations, got {n}")
    if len(y_prob) != n:
        raise ValueError(f"Length mismatch: y_true has {n}, y_prob has {len(y_prob)}")
    if not (0.0 < threshold < 1.0):
        raise ValueError(f"threshold must be in (0, 1), got {threshold}")

    for i in range(n):
        if y_true[i] not in (0, 1):
            raise ValueError(f"y_true[{i}] must be 0 or 1, got {y_true[i]}")
        if not (0.0 <= y_prob[i] <= 1.0):
            raise ValueError(f"y_prob[{i}] must be in [0, 1], got {y_prob[i]}")


def validate_loan_params(
    debt: float,
    ebitda: float,
    addback: float,
    senior_share: float,
    distress: float,
) -> None:
    """Validate leveraged loan waterfall parameters."""
    if debt <= 0:
        raise ValueError(f"initial_debt must be strictly positive, got {debt}")
    if ebitda <= 0:
        raise ValueError(f"ebitda must be strictly positive, got {ebitda}")
    if addback < 0:
        raise ValueError(f"addback_fraction must be non-negative, got {addback}")
    if not (0.0 < senior_share <= 1.0):
        raise ValueError(f"senior_share must be in (0, 1], got {senior_share}")
    if not (0.0 <= distress <= 1.0):
        raise ValueError(f"distress_factor must be in [0, 1], got {distress}")


def decompose_credit_spread(bond_data: dict[str, list[float]]) -> dict[str, Any]:
    """Decompose corporate bond credit spreads into default-risk and Excess Bond Premium components.

    Following Gilchrist & Zakrajšek (2012, AER), estimates cross-sectional log-linear regression:
      ln(s_it) = beta_0 + beta_1 D_it + beta_2 c_it + beta_3 ln(amt_it) + beta_4 ln(EDF_it) + industry_FE + eps_it
    and calculates EBP = S_GZ - S_hat with Jensen's inequality correction.
    """
    validate_bond_data(bond_data)

    spreads = np.array(bond_data["spread_bps"], dtype=np.float64)
    durations = np.array(bond_data["duration"], dtype=np.float64)
    coupons = np.array(bond_data["coupon"], dtype=np.float64)
    amounts = np.array(bond_data["amount_outstanding"], dtype=np.float64)
    edfs = np.array(bond_data["merton_edf"], dtype=np.float64)
    industries = np.array(bond_data["industry_id"], dtype=np.int64)

    n = len(spreads)
    y = np.log(spreads)

    # Build design matrix with intercept, characteristics, and industry dummies
    x_intercept = np.ones(n, dtype=np.float64)
    x_dur = durations
    x_coup = coupons
    x_amt = np.log(amounts)
    x_edf = np.log(edfs)

    # Industry dummies (industries 1, 2, 3; baseline 0)
    ind_dummies = [np.where(industries == k, 1.0, 0.0) for k in [1, 2, 3]]

    cols = [x_intercept, x_dur, x_coup, x_amt, x_edf, *ind_dummies]
    x_mat = np.column_stack(cols)

    # OLS estimation
    beta = np.linalg.lstsq(x_mat, y, rcond=None)[0]
    y_pred_log = x_mat @ beta
    e = y - y_pred_log

    k = x_mat.shape[1]
    res_var = float(np.sum(e**2) / max(1, n - k))
    res_std = math.sqrt(res_var)

    # Jensen's inequality correction: E[exp(ln s)] = exp(x_mat beta + 0.5 * sigma^2)
    s_hat_i = np.exp(y_pred_log + 0.5 * res_var)

    gz_spread = float(np.mean(spreads))
    pred_spread = float(np.mean(s_hat_i))
    ebp = float(gz_spread - pred_spread)

    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    ss_res = float(np.sum(e**2))
    r_squared = float(1.0 - ss_res / ss_tot) if ss_tot > 0 else 0.0

    return {
        "gz_spread_bps": round(gz_spread, 4),
        "predicted_spread_bps": round(pred_spread, 4),
        "ebp_bps": round(ebp, 4),
        "coefficients": {
            "intercept": float(beta[0]),
            "duration": float(beta[1]),
            "coupon": float(beta[2]),
            "log_amount": float(beta[3]),
            "log_edf": float(beta[4]),
        },
        "r_squared": round(r_squared, 4),
        "residual_std": round(res_std, 4),
    }


def construct_credit_sentiment_index(
    hy_issuance_share: list[float],
    credit_spreads: list[float],
    ebp: list[float],
    weights: list[float] | None = None,
) -> dict[str, Any]:
    """Construct a composite credit-market sentiment index.

    Following López-Salido, Stein & Zakrajšek (2017) and Greenwood & Hanson (2013):
      Sentiment_t = w_1 * z(HY_share) - w_2 * z(Spread) - w_3 * z(EBP)
    where high sentiment indicates aggressive risk-taking (high issuance, compressed spreads, depressed EBP).
    """
    validate_sentiment_inputs(hy_issuance_share, credit_spreads, ebp, weights)

    hy_arr = np.array(hy_issuance_share, dtype=np.float64)
    spr_arr = np.array(credit_spreads, dtype=np.float64)
    ebp_arr = np.array(ebp, dtype=np.float64)

    def z_score(arr: np.ndarray) -> np.ndarray:
        s = float(np.std(arr, ddof=1))
        if s < 1e-12:
            return np.zeros_like(arr)
        return (arr - float(np.mean(arr))) / s

    z_hy = z_score(hy_arr)
    z_spr = z_score(spr_arr)
    z_ebp = z_score(ebp_arr)

    if weights is None:
        norm_w = [1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0]
    else:
        tot = sum(weights)
        norm_w = [w / tot for w in weights]

    sentiment = norm_w[0] * z_hy - norm_w[1] * z_spr - norm_w[2] * z_ebp

    # First-order autocorrelation
    s_mean = float(np.mean(sentiment))
    s_centered = sentiment - s_mean
    gamma0 = float(np.sum(s_centered**2))
    if gamma0 > 1e-12:
        gamma1 = float(np.sum(s_centered[:-1] * s_centered[1:]))
        rho1 = gamma1 / gamma0
    else:
        rho1 = 0.0

    return {
        "sentiment_index": [round(float(x), 4) for x in sentiment],
        "autocorrelation_lag1": round(float(rho1), 4),
        "z_scores": {
            "hy_share": [round(float(x), 4) for x in z_hy],
            "spread": [round(float(x), 4) for x in z_spr],
            "ebp": [round(float(x), 4) for x in z_ebp],
        },
        "weights": [round(float(w), 4) for w in norm_w],
    }


def predict_spread_reversals(
    sentiment_series: list[float],
    spread_series: list[float],
    horizon_steps: int = 4,
) -> dict[str, Any]:
    """Estimate predictive regressions of future credit spread changes on current sentiment.

    Following López-Salido, Stein & Zakrajšek (2017):
      Spread_{t+h} - Spread_t = alpha + beta_rev * Sentiment_t + eps_{t+h}
    Inference uses Newey-West HAC standard errors with Bartlett lag window L = h.
    """
    if len(sentiment_series) != len(spread_series):
        raise ValueError("sentiment_series and spread_series must have equal lengths")
    t_len = len(sentiment_series)
    if horizon_steps < 1 or horizon_steps >= t_len:
        raise ValueError(f"horizon_steps must be in 1..{t_len - 1}, got {horizon_steps}")

    m = t_len - horizon_steps
    if m < 8:
        raise ValueError(f"Need at least 8 effective observations after horizon, got {m}")

    y_change = np.zeros(m, dtype=np.float64)
    x_sent = np.zeros(m, dtype=np.float64)

    for t in range(m):
        y_change[t] = spread_series[t + horizon_steps] - spread_series[t]
        x_sent[t] = sentiment_series[t]

    x_mat = np.column_stack([np.ones(m, dtype=np.float64), x_sent])
    beta = np.linalg.lstsq(x_mat, y_change, rcond=None)[0]
    y_pred = x_mat @ beta
    u = y_change - y_pred

    # OLS R-squared
    ss_tot = float(np.sum((y_change - np.mean(y_change)) ** 2))
    ss_res = float(np.sum(u**2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

    # Newey-West HAC covariance matrix
    # Q = x_mat'x_mat / m
    q_inv = np.linalg.inv((x_mat.T @ x_mat) / m)

    # Gamma_0
    gamma0 = np.zeros((2, 2), dtype=np.float64)
    for t in range(m):
        xt = x_mat[t : t + 1, :].T
        gamma0 += (u[t] ** 2) * (xt @ xt.T)
    gamma0 /= m

    # Gamma_lag for lag = 1 .. h
    omega = gamma0.copy()
    h_lags = horizon_steps
    for lag in range(1, h_lags + 1):
        weight = 1.0 - float(lag) / (h_lags + 1.0)
        gamma_l = np.zeros((2, 2), dtype=np.float64)
        for t in range(lag, m):
            xt = x_mat[t : t + 1, :].T
            xt_prev = x_mat[t - lag : t - lag + 1, :].T
            gamma_l += u[t] * u[t - lag] * (xt @ xt_prev.T)
        gamma_l /= m
        omega += weight * (gamma_l + gamma_l.T)

    v_hac = (q_inv @ omega @ q_inv) / m
    se_beta = math.sqrt(max(1e-12, float(v_hac[1, 1])))
    t_stat = float(beta[1] / se_beta)
    p_val = float(2.0 * (1.0 - stats.norm.cdf(abs(t_stat))))

    return {
        "beta_reversal": round(float(beta[1]), 4),
        "intercept": round(float(beta[0]), 4),
        "t_stat_hac": round(t_stat, 4),
        "p_value": round(p_val, 4),
        "r_squared": round(r2, 4),
        "predicted_spread_changes": [round(float(p), 4) for p in y_pred],
    }


def fit_recession_probit(
    indicator_series: list[float],
    term_spread_series: list[float],
    recession_flags: list[int],
) -> dict[str, Any]:
    """Fit a logistic/probit recession forecasting regression.

    Models P(Recession_t = 1) = Lambda(beta_0 + beta_1 * Indicator_t + beta_2 * TermSpread_t).
    Calculates maximum likelihood estimates, asymptotic standard errors, and McFadden's pseudo-R^2.
    """
    validate_recession_inputs(indicator_series, term_spread_series, recession_flags)

    x1 = np.array(indicator_series, dtype=np.float64)
    x2 = np.array(term_spread_series, dtype=np.float64)
    y = np.array(recession_flags, dtype=np.float64)
    n = len(y)

    x_mat = np.column_stack([np.ones(n, dtype=np.float64), x1, x2])

    def neg_log_lik(b: np.ndarray) -> float:
        z = np.clip(x_mat @ b, -25.0, 25.0)
        p = 1.0 / (1.0 + np.exp(-z))
        p = np.clip(p, 1e-12, 1.0 - 1e-12)
        ll = np.sum(y * np.log(p) + (1.0 - y) * np.log(1.0 - p))
        return -float(ll)

    # Initial guess via linear probability OLS
    b0 = np.linalg.lstsq(x_mat, y, rcond=None)[0]
    res = optimize.minimize(neg_log_lik, b0, method="BFGS")
    b_opt = res.x

    log_lik = -float(res.fun)

    # Null log-likelihood
    p_null = float(np.mean(y))
    p_null = max(1e-12, min(1.0 - 1e-12, p_null))
    null_ll = float(np.sum(y * np.log(p_null) + (1.0 - y) * np.log(1.0 - p_null)))
    pseudo_r2 = float(1.0 - log_lik / null_ll) if null_ll < 0 else 0.0

    # Asymptotic standard errors from Hessian / information matrix
    z_opt = np.clip(x_mat @ b_opt, -20.0, 20.0)
    p_opt = 1.0 / (1.0 + np.exp(-z_opt))
    p_opt = np.clip(p_opt, 1e-5, 1.0 - 1e-5)
    w = p_opt * (1.0 - p_opt)
    # Information matrix: x_mat' W x_mat
    inf_mat = x_mat.T @ (x_mat * w[:, None])
    try:
        cov_mat = np.linalg.inv(inf_mat)
        se = np.sqrt(np.maximum(1e-12, np.diag(cov_mat)))
    except np.linalg.LinAlgError:
        se = np.array([0.1, 0.1, 0.1])

    return {
        "beta": {
            "intercept": round(float(b_opt[0]), 4),
            "credit_indicator": round(float(b_opt[1]), 4),
            "term_spread": round(float(b_opt[2]), 4),
        },
        "standard_errors": {
            "intercept": round(float(se[0]), 4),
            "credit_indicator": round(float(se[1]), 4),
            "term_spread": round(float(se[2]), 4),
        },
        "log_likelihood": round(log_lik, 4),
        "pseudo_r_squared": round(pseudo_r2, 4),
        "fitted_probabilities": [round(float(p), 6) for p in p_opt],
    }


def evaluate_recession_forecasts(
    y_true: list[int],
    y_prob: list[float],
    threshold: float = 0.5,
) -> dict[str, Any]:
    """Evaluate recession forecasting accuracy out-of-sample.

    Calculates Brier score, ROC-AUC, sensitivity, specificity, and confusion matrix.
    """
    validate_evaluation_inputs(y_true, y_prob, threshold)

    y_arr = np.array(y_true, dtype=np.int64)
    p_arr = np.array(y_prob, dtype=np.float64)

    brier = float(np.mean((p_arr - y_arr) ** 2))

    y_pred = (p_arr >= threshold).astype(np.int64)
    tp = int(np.sum((y_pred == 1) & (y_arr == 1)))
    fp = int(np.sum((y_pred == 1) & (y_arr == 0)))
    tn = int(np.sum((y_pred == 0) & (y_arr == 0)))
    fn = int(np.sum((y_pred == 0) & (y_arr == 1)))

    precision = float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0
    recall = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
    specificity = float(tn / (tn + fp)) if (tn + fp) > 0 else 0.0

    # Exact non-parametric ROC-AUC via Mann-Whitney U
    pos = p_arr[y_arr == 1]
    neg = p_arr[y_arr == 0]
    n_pos = len(pos)
    n_neg = len(neg)
    if n_pos == 0 or n_neg == 0:
        auc = 0.5
    else:
        concordant = 0.0
        for p_val in pos:
            concordant += float(np.sum(p_val > neg)) + 0.5 * float(np.sum(p_val == neg))
        auc = float(concordant / (n_pos * n_neg))

    return {
        "brier_score": round(brier, 4),
        "auc_roc": round(auc, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "specificity": round(specificity, 4),
        "confusion_matrix": {
            "tp": tp,
            "fp": fp,
            "tn": tn,
            "fn": fn,
        },
    }


def simulate_leveraged_loan_waterfall(
    initial_debt: float,
    ebitda: float,
    addback_fraction: float,
    senior_share: float,
    cov_lite: bool,
    distress_factor: float,
) -> dict[str, Any]:
    """Simulate leveraged loan and private credit restructuring loss waterfalls.

    Models cov-lite vs maintenance covenant breach, EBITDA add-back distortion,
    and recovery rates across senior secured and junior debt tranches.
    """
    validate_loan_params(initial_debt, ebitda, addback_fraction, senior_share, distress_factor)

    reported_ebitda = ebitda * (1.0 + addback_fraction)
    distressed_ebitda = max(1e-6, ebitda * (1.0 - distress_factor))

    reported_leverage = initial_debt / reported_ebitda
    actual_leverage = initial_debt / ebitda

    # Maintenance covenant check: leverage ceiling of 6.5x
    covenant_threshold = 6.5
    covenant_breached = bool((initial_debt / distressed_ebitda) > covenant_threshold) if not cov_lite else False

    # Enterprise valuation at restructuring: early trigger preserves 7.0x multiple; cov-lite delay erodes 35%
    base_multiple = 7.0
    enterprise_value = distressed_ebitda * base_multiple if not cov_lite else distressed_ebitda * base_multiple * 0.65

    # Debt capital structure
    senior_debt = initial_debt * senior_share
    junior_debt = initial_debt * (1.0 - senior_share)

    # Priority waterfall
    senior_recovered = min(senior_debt, enterprise_value)
    remaining_ev = max(0.0, enterprise_value - senior_recovered)
    junior_recovered = min(junior_debt, remaining_ev)

    senior_recovery_rate = float(senior_recovered / senior_debt)
    junior_recovery_rate = float(junior_recovered / junior_debt) if junior_debt > 0 else 1.0
    total_recovered = senior_recovered + junior_recovered
    total_recovery_rate = float(total_recovered / initial_debt)
    lgd = float(1.0 - total_recovery_rate)

    return {
        "covenant_breached": covenant_breached,
        "enterprise_value": round(enterprise_value, 2),
        "senior_recovery_rate": round(senior_recovery_rate, 4),
        "junior_recovery_rate": round(junior_recovery_rate, 4),
        "total_recovery_rate": round(total_recovery_rate, 4),
        "loss_given_default": round(lgd, 4),
        "reported_leverage": round(reported_leverage, 2),
        "actual_leverage": round(actual_leverage, 2),
    }

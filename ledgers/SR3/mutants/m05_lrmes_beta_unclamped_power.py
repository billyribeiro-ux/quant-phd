"""compute_lrmes sets LRMES directly equal to market beta, ignoring exponential crisis drop scaling."""

from __future__ import annotations

from typing import Any

import numpy as np
from scipy.optimize import linprog  # type: ignore[import-untyped]


def fit_linear_quantile_regression(y: np.ndarray[Any, Any], x: np.ndarray[Any, Any], q: float = 0.05) -> np.ndarray[Any, Any]:
    if not (0.0 < q < 1.0):
        raise ValueError("Invalid q")
    y_arr = np.asarray(y, dtype=np.float64)
    x_arr = np.asarray(x, dtype=np.float64)
    t_obs, k_vars = x_arr.shape
    c = np.concatenate([np.zeros(k_vars), q * np.ones(t_obs), (1.0 - q) * np.ones(t_obs)])
    eye_t = np.eye(t_obs)
    res = linprog(c, A_eq=np.hstack([x_arr, eye_t, -eye_t]), b_eq=y_arr, bounds=[(None, None)] * k_vars + [(0.0, None)] * (2 * t_obs), method="highs")
    return np.asarray(res.x[:k_vars], dtype=np.float64)


def compute_covar(r_system: np.ndarray[Any, Any], r_institution: np.ndarray[Any, Any], state_vars: np.ndarray[Any, Any] | None = None, alpha: float = 0.05) -> dict[str, float]:
    r_sys = np.asarray(r_system, dtype=np.float64)
    r_inst = np.asarray(r_institution, dtype=np.float64)
    t_obs = r_sys.shape[0]
    ones = np.ones((t_obs, 1), dtype=np.float64)
    if state_vars is None:
        var_inst_alpha = float(np.quantile(r_inst, alpha))
        var_inst_median = float(np.quantile(r_inst, 0.50))
        x_sys = np.column_stack([ones, r_inst])
        beta_sys = fit_linear_quantile_regression(r_sys, x_sys, q=alpha)
        covar = float(beta_sys[0] + beta_sys[1] * var_inst_alpha)
        covar_median = float(beta_sys[0] + beta_sys[1] * var_inst_median)
        delta_covar = float(covar - covar_median)
        b_q = float(beta_sys[1])
    else:
        m_arr = np.asarray(state_vars, dtype=np.float64)
        x_inst = np.hstack([ones, m_arr])
        b_inst_alpha = fit_linear_quantile_regression(r_inst, x_inst, q=alpha)
        b_inst_median = fit_linear_quantile_regression(r_inst, x_inst, q=0.50)
        m_mean = np.mean(m_arr, axis=0)
        eval_x = np.concatenate([[1.0], m_mean])
        var_inst_alpha = float(np.dot(b_inst_alpha, eval_x))
        var_inst_median = float(np.dot(b_inst_median, eval_x))
        x_sys = np.column_stack([ones, r_inst, m_arr])
        beta_sys = fit_linear_quantile_regression(r_sys, x_sys, q=alpha)
        covar = float(beta_sys[0] + beta_sys[1] * var_inst_alpha + np.dot(beta_sys[2:], m_mean))
        covar_median = float(beta_sys[0] + beta_sys[1] * var_inst_median + np.dot(beta_sys[2:], m_mean))
        delta_covar = float(covar - covar_median)
        b_q = float(beta_sys[1])
    return {"covar": covar, "covar_median": covar_median, "delta_covar": delta_covar, "beta_quantile": b_q, "var_institution": var_inst_alpha}


def compute_mes(r_system: np.ndarray[Any, Any], r_institution: np.ndarray[Any, Any], alpha: float = 0.05) -> float:
    r_sys = np.asarray(r_system, dtype=np.float64)
    r_inst = np.asarray(r_institution, dtype=np.float64)
    var_s = float(np.quantile(r_sys, alpha))
    crisis_mask = r_sys <= var_s
    return float(-np.mean(r_inst[crisis_mask]))


def compute_lrmes(r_system: np.ndarray[Any, Any], r_institution: np.ndarray[Any, Any], alpha: float = 0.05, crisis_drop: float = 0.40) -> float:
    r_sys = np.asarray(r_system, dtype=np.float64)
    r_inst = np.asarray(r_institution, dtype=np.float64)
    var_sys = float(np.var(r_sys, ddof=1))
    cov_val = float(np.cov(r_inst, r_sys, ddof=1)[0, 1])
    beta = cov_val / var_sys
    # MUTANT ERROR: returns beta directly, exceeding [0, 1) and ignoring crisis_drop
    return float(beta)


def compute_srisk(equity_value: float, debt_value: float, lrmes: float, prudential_ratio: float = 0.08) -> float:
    if equity_value <= 0.0 or debt_value < 0.0:
        raise ValueError("Invalid balance sheet items")
    k = prudential_ratio
    cs = k * debt_value - (1.0 - k) * (1.0 - lrmes) * equity_value
    return float(max(0.0, cs))


def compute_systemic_srisk_panel(equities: np.ndarray[Any, Any], debts: np.ndarray[Any, Any], lrmes_values: np.ndarray[Any, Any], prudential_ratio: float = 0.08) -> dict[str, Any]:
    w = np.asarray(equities, dtype=np.float64)
    d = np.asarray(debts, dtype=np.float64)
    lrmes = np.asarray(lrmes_values, dtype=np.float64)
    k = prudential_ratio
    cs = k * d - (1.0 - k) * (1.0 - lrmes) * w
    srisk = np.maximum(0.0, cs)
    total_srisk = float(np.sum(srisk))
    srisk_pct = srisk / total_srisk if total_srisk > 1e-9 else np.zeros_like(srisk)
    return {"srisk_individual": srisk, "capital_shortfall": cs, "total_srisk": total_srisk, "srisk_pct": srisk_pct}


def compute_network_clearing(nominal_liabilities: np.ndarray[Any, Any], external_assets: np.ndarray[Any, Any], senior_liabilities: np.ndarray[Any, Any] | None = None, max_iter: int = 1000, tol: float = 1e-10) -> dict[str, Any]:
    l_mat = np.asarray(nominal_liabilities, dtype=np.float64)
    z_vec = np.asarray(external_assets, dtype=np.float64)
    n_nodes = l_mat.shape[0]
    b_vec = np.zeros(n_nodes, dtype=np.float64) if senior_liabilities is None else np.asarray(senior_liabilities, dtype=np.float64)
    p_bar = np.sum(l_mat, axis=1)
    pi_mat = np.zeros_like(l_mat)
    has_liab = p_bar > 1e-12
    pi_mat[has_liab] = l_mat[has_liab] / p_bar[has_liab, None]
    p = p_bar.copy()
    rounds = 0
    for _ in range(max_iter):
        rounds += 1
        p_next = np.minimum(p_bar, np.maximum(0.0, z_vec + pi_mat.T @ p - b_vec))
        if np.max(np.abs(p_next - p)) < tol:
            p = p_next
            break
        p = p_next
    defaults = (p < p_bar - 1e-7).astype(np.int64)
    equity = np.maximum(0.0, z_vec + pi_mat.T @ p - b_vec - p_bar)
    return {"clearing_payments": p, "equity_values": equity, "defaults": defaults, "default_count": int(np.sum(defaults)), "cascade_rounds": rounds, "total_shortfall": float(np.sum(p_bar - p))}


class SystemicRiskMonitor:
    def __init__(self, thresholds: dict[str, float] | None = None) -> None:
        self.thresholds = {"delta_covar": -0.015, "mes": 0.035, "srisk_pct": 0.30, "network_defaults": 1.0}
        if thresholds:
            self.thresholds.update(thresholds)

    def evaluate(self, metrics: dict[str, Any]) -> dict[str, Any]:
        breaches = {}
        if "delta_covar" in metrics:
            breaches["delta_covar"] = float(metrics["delta_covar"]) < self.thresholds["delta_covar"]
        if "mes" in metrics:
            breaches["mes"] = float(metrics["mes"]) > self.thresholds["mes"]
        if "srisk_pct" in metrics:
            val = np.max(metrics["srisk_pct"]) if isinstance(metrics["srisk_pct"], (list, np.ndarray)) else metrics["srisk_pct"]
            breaches["srisk_pct"] = float(val) > self.thresholds["srisk_pct"]
        if "network_defaults" in metrics:
            breaches["network_defaults"] = float(metrics["network_defaults"]) >= self.thresholds["network_defaults"]
        total = sum(1 for b in breaches.values() if b)
        severity = "NORMAL" if total == 0 else ("WATCH" if total == 1 else ("WARNING" if total == 2 else "CRITICAL"))
        return {"breaches": breaches, "total_breaches": total, "severity": severity, "is_alert": total > 0}

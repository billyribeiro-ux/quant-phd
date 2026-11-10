"""Reference implementation for Atlas A19 Systemic-Risk Monitor (`atlas.systemic`).

Provides quantitative implementations of CoVaR, Delta-CoVaR, Marginal Expected Shortfall,
Long-Run MES, SRISK conditional capital shortfall, and Eisenberg-Noe network cascade clearing.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from scipy.optimize import linprog


def fit_linear_quantile_regression(
    y: np.ndarray[Any, Any],
    x: np.ndarray[Any, Any],
    q: float = 0.05,
) -> np.ndarray[Any, Any]:
    """Estimate linear quantile regression coefficients beta_q minimizing pinball loss.

    Solves the linear programming formulation:
        min_{beta, u+, u-} sum_t (q * u+_t + (1 - q) * u-_t)
        s.t. y - X beta = u+ - u-,  u+ >= 0, u- >= 0

    Parameters
    ----------
    y : np.ndarray
        1D dependent variable array of length T.
    x : np.ndarray
        2D design matrix of shape (T, K).
    q : float
        Quantile level in (0, 1), default 0.05.

    Returns
    -------
    np.ndarray
        Estimated parameter vector beta of shape (K,).
    """
    if not (0.0 < q < 1.0):
        raise ValueError(f"Quantile q must be strictly between 0 and 1, got {q}")

    y_arr = np.asarray(y, dtype=np.float64)
    x_arr = np.asarray(x, dtype=np.float64)

    if y_arr.ndim != 1:
        raise ValueError(f"y must be a 1D array, got shape {y_arr.shape}")
    if x_arr.ndim != 2:
        raise ValueError(f"x must be a 2D array, got shape {x_arr.shape}")
    t_obs, k_vars = x_arr.shape
    if y_arr.shape[0] != t_obs:
        raise ValueError(f"Length of y ({y_arr.shape[0]}) does not match x rows ({t_obs})")
    if t_obs < k_vars:
        raise ValueError(f"Observations ({t_obs}) must exceed parameter count ({k_vars})")

    # Linear programming formulation: variables [beta (K), u+ (T), u- (T)]
    c = np.concatenate([np.zeros(k_vars), q * np.ones(t_obs), (1.0 - q) * np.ones(t_obs)])
    eye_t = np.eye(t_obs)
    a_eq = np.hstack([x_arr, eye_t, -eye_t])
    b_eq = y_arr

    bounds = [(None, None)] * k_vars + [(0.0, None)] * (2 * t_obs)

    res = linprog(c, A_eq=a_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if not res.success:
        raise ValueError(f"Quantile regression optimization failed: {res.message}")

    return np.asarray(res.x[:k_vars], dtype=np.float64)


def compute_covar(
    r_system: np.ndarray[Any, Any],
    r_institution: np.ndarray[Any, Any],
    state_vars: np.ndarray[Any, Any] | None = None,
    alpha: float = 0.05,
) -> dict[str, float]:
    """Compute CoVaR, median CoVaR, and Delta-CoVaR for an institution.

    Parameters
    ----------
    r_system : np.ndarray
        1D array of system returns of length T.
    r_institution : np.ndarray
        1D array of institution returns of length T.
    state_vars : np.ndarray or None
        Optional 2D array of lagged macro state variables of shape (T, K).
    alpha : float
        Quantile level in (0, 1), default 0.05.

    Returns
    -------
    dict[str, float]
        Dictionary with covar, covar_median, delta_covar, beta_quantile, and var_institution.
    """
    if not (0.0 < alpha < 1.0):
        raise ValueError(f"Confidence level alpha must be in (0, 1), got {alpha}")

    r_sys = np.asarray(r_system, dtype=np.float64)
    r_inst = np.asarray(r_institution, dtype=np.float64)

    if r_sys.ndim != 1 or r_inst.ndim != 1:
        raise ValueError("r_system and r_institution must be 1D arrays")
    if r_sys.shape[0] != r_inst.shape[0]:
        raise ValueError(f"Length mismatch: r_system ({r_sys.shape[0]}) vs r_institution ({r_inst.shape[0]})")
    t_obs = r_sys.shape[0]

    ones = np.ones((t_obs, 1), dtype=np.float64)

    if state_vars is None:
        # Static CoVaR estimation without macro state variables
        # Institution VaR at alpha and median (0.50)
        var_inst_alpha = float(np.quantile(r_inst, alpha))
        var_inst_median = float(np.quantile(r_inst, 0.50))

        # System quantile regression: R_sys = a_q + b_q * R_inst
        x_sys = np.column_stack([ones, r_inst])
        beta_sys = fit_linear_quantile_regression(r_sys, x_sys, q=alpha)

        covar = float(beta_sys[0] + beta_sys[1] * var_inst_alpha)
        covar_median = float(beta_sys[0] + beta_sys[1] * var_inst_median)
        delta_covar = float(covar - covar_median)
        b_q = float(beta_sys[1])
    else:
        m_arr = np.asarray(state_vars, dtype=np.float64)
        if m_arr.ndim != 2 or m_arr.shape[0] != t_obs:
            raise ValueError(f"state_vars must be shape ({t_obs}, K)")

        # State-conditioned institution VaR
        x_inst = np.hstack([ones, m_arr])
        b_inst_alpha = fit_linear_quantile_regression(r_inst, x_inst, q=alpha)
        b_inst_median = fit_linear_quantile_regression(r_inst, x_inst, q=0.50)

        # Evaluate at average state conditions
        m_mean = np.mean(m_arr, axis=0)
        eval_x = np.concatenate([[1.0], m_mean])
        var_inst_alpha = float(np.dot(b_inst_alpha, eval_x))
        var_inst_median = float(np.dot(b_inst_median, eval_x))

        # System quantile regression: R_sys = a_q + b_q * R_inst + gamma_q * M
        x_sys = np.column_stack([ones, r_inst, m_arr])
        beta_sys = fit_linear_quantile_regression(r_sys, x_sys, q=alpha)

        covar = float(beta_sys[0] + beta_sys[1] * var_inst_alpha + np.dot(beta_sys[2:], m_mean))
        covar_median = float(beta_sys[0] + beta_sys[1] * var_inst_median + np.dot(beta_sys[2:], m_mean))
        delta_covar = float(covar - covar_median)
        b_q = float(beta_sys[1])

    return {
        "covar": covar,
        "covar_median": covar_median,
        "delta_covar": delta_covar,
        "beta_quantile": b_q,
        "var_institution": var_inst_alpha,
    }


def compute_mes(
    r_system: np.ndarray[Any, Any],
    r_institution: np.ndarray[Any, Any],
    alpha: float = 0.05,
) -> float:
    """Compute non-parametric Marginal Expected Shortfall (MES).

    Defined as the average loss of institution i on days when the system
    experiences its alpha-worst returns (R_sys <= VaR_alpha(R_sys)):
        MES_alpha = -E[R_i | R_sys <= VaR_alpha(R_sys)]

    Returns a positive number representing loss.
    """
    if not (0.0 < alpha < 1.0):
        raise ValueError(f"alpha must be in (0, 1), got {alpha}")

    r_sys = np.asarray(r_system, dtype=np.float64)
    r_inst = np.asarray(r_institution, dtype=np.float64)

    if r_sys.ndim != 1 or r_inst.ndim != 1:
        raise ValueError("Returns must be 1D arrays")
    if r_sys.shape[0] != r_inst.shape[0]:
        raise ValueError("Return arrays must have identical length")

    var_s = float(np.quantile(r_sys, alpha))
    crisis_mask = r_sys <= var_s

    if not np.any(crisis_mask):
        return float(-np.quantile(r_inst, alpha))

    # Expressed as a positive loss
    return float(-np.mean(r_inst[crisis_mask]))


def compute_lrmes(
    r_system: np.ndarray[Any, Any],
    r_institution: np.ndarray[Any, Any],
    alpha: float = 0.05,
    crisis_drop: float = 0.40,
) -> float:
    """Compute Long-Run Marginal Expected Shortfall (LRMES) over a multi-month crisis.

    Under the Acharya et al. and Brownlees-Engle dynamic tail model,
    LRMES is the projected percentage equity loss when the broad market
    drops by fraction crisis_drop (typically 40%):
        LRMES = 1 - exp(ln(1 - crisis_drop) * beta_i) = 1 - (1 - crisis_drop)^beta_i
    where beta_i = Cov(R_i, R_s) / Var(R_s).
    """
    if not (0.0 < crisis_drop < 1.0):
        raise ValueError(f"crisis_drop must be in (0, 1), got {crisis_drop}")

    r_sys = np.asarray(r_system, dtype=np.float64)
    r_inst = np.asarray(r_institution, dtype=np.float64)

    var_sys = float(np.var(r_sys, ddof=1))
    if var_sys <= 1e-12:
        raise ValueError("System return variance is effectively zero")

    cov_val = float(np.cov(r_inst, r_sys, ddof=1)[0, 1])
    beta = cov_val / var_sys

    if beta <= 0.0:
        return 0.0

    # LRMES fraction bounded in [0, 1)
    lrmes = float(1.0 - (1.0 - crisis_drop) ** beta)
    return max(0.0, min(0.9999, lrmes))


def compute_srisk(
    equity_value: float,
    debt_value: float,
    lrmes: float,
    prudential_ratio: float = 0.08,
) -> float:
    """Compute individual institution SRISK (conditional capital shortfall).

    Formula (Brownlees & Engle 2017):
        SRISK_i = max(0, k * D_i - (1 - k) * (1 - LRMES_i) * W_i)

    Parameters
    ----------
    equity_value : float
        Market value of equity W_i (must be > 0).
    debt_value : float
        Book value of debt / liabilities D_i (must be >= 0).
    lrmes : float
        Long-Run Marginal Expected Shortfall in [0, 1].
    prudential_ratio : float
        Prudential capital requirement k in (0, 1), default 0.08 (8%).

    Returns
    -------
    float
        SRISK in dollar / currency units (>= 0).
    """
    if equity_value <= 0.0:
        raise ValueError(f"equity_value must be strictly positive, got {equity_value}")
    if debt_value < 0.0:
        raise ValueError(f"debt_value cannot be negative, got {debt_value}")
    if not (0.0 < prudential_ratio < 1.0):
        raise ValueError(f"prudential_ratio must be in (0, 1), got {prudential_ratio}")
    if not (0.0 <= lrmes <= 1.0):
        raise ValueError(f"lrmes must be in [0, 1], got {lrmes}")

    k = prudential_ratio
    cs = k * debt_value - (1.0 - k) * (1.0 - lrmes) * equity_value
    return float(max(0.0, cs))


def compute_systemic_srisk_panel(
    equities: np.ndarray[Any, Any],
    debts: np.ndarray[Any, Any],
    lrmes_values: np.ndarray[Any, Any],
    prudential_ratio: float = 0.08,
) -> dict[str, Any]:
    """Compute multi-firm SRISK panel, total systemic SRISK, and percentage contributions.

    Parameters
    ----------
    equities : np.ndarray
        1D array of firm market equity values W.
    debts : np.ndarray
        1D array of firm debt values D.
    lrmes_values : np.ndarray
        1D array of firm LRMES tail losses.
    prudential_ratio : float
        Prudential capital fraction k (default 0.08).

    Returns
    -------
    dict[str, Any]
        Dictionary with srisk_individual, capital_shortfall, total_srisk, and srisk_pct.
    """
    w = np.asarray(equities, dtype=np.float64)
    d = np.asarray(debts, dtype=np.float64)
    lrmes = np.asarray(lrmes_values, dtype=np.float64)

    if w.ndim != 1 or d.ndim != 1 or lrmes.ndim != 1:
        raise ValueError("equities, debts, and lrmes_values must be 1D arrays")
    n_firms = w.shape[0]
    if d.shape[0] != n_firms or lrmes.shape[0] != n_firms:
        raise ValueError("Input arrays must have equal length")

    k = prudential_ratio
    cs = k * d - (1.0 - k) * (1.0 - lrmes) * w
    srisk = np.maximum(0.0, cs)
    total_srisk = float(np.sum(srisk))
    srisk_pct = srisk / total_srisk if total_srisk > 1e-9 else np.zeros(n_firms, dtype=np.float64)

    return {
        "srisk_individual": srisk,
        "capital_shortfall": cs,
        "total_srisk": total_srisk,
        "srisk_pct": srisk_pct,
    }


def compute_network_clearing(
    nominal_liabilities: np.ndarray[Any, Any],
    external_assets: np.ndarray[Any, Any],
    senior_liabilities: np.ndarray[Any, Any] | None = None,
    max_iter: int = 1000,
    tol: float = 1e-10,
) -> dict[str, Any]:
    """Solve Eisenberg-Noe network clearing vectors and cascade propagation.

    Parameters
    ----------
    nominal_liabilities : np.ndarray
        Square matrix L of nominal interbank liabilities where L[i, j] is debt
        owed by institution i to institution j. L[i, i] == 0.
    external_assets : np.ndarray
        1D array z of outside liquid assets available for payment.
    senior_liabilities : np.ndarray or None
        Optional 1D array b of non-bank / senior outside liabilities.
    max_iter : int
        Maximum Picard iterations for the fixed point.
    tol : float
        Convergence tolerance on ||p_{k+1} - p_k||_inf.

    Returns
    -------
    dict[str, Any]
        Dictionary with clearing_payments, equity_values, defaults, default_count,
        cascade_rounds, and total_shortfall.
    """
    l_mat = np.asarray(nominal_liabilities, dtype=np.float64)
    z_vec = np.asarray(external_assets, dtype=np.float64)

    if l_mat.ndim != 2 or l_mat.shape[0] != l_mat.shape[1]:
        raise ValueError("nominal_liabilities must be a square 2D matrix")
    n_nodes = l_mat.shape[0]
    if z_vec.shape != (n_nodes,):
        raise ValueError(f"external_assets must be a 1D array of length {n_nodes}")
    if np.any(np.diag(l_mat) != 0.0):
        raise ValueError("Diagonal entries of nominal liabilities must be zero")
    if np.any(l_mat < 0.0):
        raise ValueError("Nominal liabilities cannot be negative")

    if senior_liabilities is None:
        b_vec = np.zeros(n_nodes, dtype=np.float64)
    else:
        b_vec = np.asarray(senior_liabilities, dtype=np.float64)
        if b_vec.shape != (n_nodes,):
            raise ValueError(f"senior_liabilities must match node count {n_nodes}")

    p_bar = np.sum(l_mat, axis=1)

    # Relative liabilities matrix Pi: Pi[i, j] = L[i, j] / p_bar[i]
    pi_mat = np.zeros_like(l_mat)
    has_liab = p_bar > 1e-12
    pi_mat[has_liab] = l_mat[has_liab] / p_bar[has_liab, None]

    # Monotone Picard iteration starting from full payment p_bar
    p = p_bar.copy()
    rounds = 0
    converged = False

    for _ in range(max_iter):
        rounds += 1
        # Incoming payment to bank i is sum_j Pi[j, i] * p[j] = (Pi.T @ p)[i]
        inflows = pi_mat.T @ p
        p_next = np.minimum(p_bar, np.maximum(0.0, z_vec + inflows - b_vec))

        if np.max(np.abs(p_next - p)) < tol:
            p = p_next
            converged = True
            break
        p = p_next

    if not converged:
        raise ValueError(f"Clearing vector failed to converge in {max_iter} iterations")

    defaults = (p < p_bar - 1e-7).astype(np.int64)
    equity = np.maximum(0.0, z_vec + pi_mat.T @ p - b_vec - p_bar)
    total_shortfall = float(np.sum(p_bar - p))

    return {
        "clearing_payments": p,
        "equity_values": equity,
        "defaults": defaults,
        "default_count": int(np.sum(defaults)),
        "cascade_rounds": rounds,
        "total_shortfall": total_shortfall,
    }


class SystemicRiskMonitor:
    """Enterprise systemic risk monitor with configurable alert thresholds."""

    def __init__(self, thresholds: dict[str, float] | None = None) -> None:
        default_thresholds = {
            "delta_covar": -0.015,
            "mes": 0.035,
            "srisk_pct": 0.30,
            "network_defaults": 1.0,
        }
        self.thresholds: dict[str, float] = default_thresholds
        if thresholds is not None:
            self.thresholds.update(thresholds)

    def evaluate(self, metrics: dict[str, Any]) -> dict[str, Any]:
        """Evaluate systemic indicators against prudential thresholds.

        Parameters
        ----------
        metrics : dict[str, Any]
            Dictionary containing computed risk metrics: delta_covar, mes,
            srisk_pct, and network_defaults.

        Returns
        -------
        dict[str, Any]
            Dictionary containing breaches per metric, total breach count,
            and aggregate severity level ("NORMAL", "WATCH", "WARNING", "CRITICAL").
        """
        breaches: dict[str, bool] = {}

        if "delta_covar" in metrics:
            # Breach if delta_covar is more negative than threshold
            breaches["delta_covar"] = float(metrics["delta_covar"]) < self.thresholds["delta_covar"]

        if "mes" in metrics:
            # Breach if MES exceeds positive loss threshold
            breaches["mes"] = float(metrics["mes"]) > self.thresholds["mes"]

        if "srisk_pct" in metrics:
            # Breach if maximum firm SRISK contribution exceeds concentration threshold
            s_pct = metrics["srisk_pct"]
            val = np.max(s_pct) if isinstance(s_pct, (list, np.ndarray)) else s_pct
            breaches["srisk_pct"] = float(val) > self.thresholds["srisk_pct"]

        if "network_defaults" in metrics:
            # Breach if interbank default count >= network threshold
            breaches["network_defaults"] = float(metrics["network_defaults"]) >= self.thresholds["network_defaults"]

        total_breaches = sum(1 for b in breaches.values() if b)

        if total_breaches == 0:
            severity = "NORMAL"
        elif total_breaches == 1:
            severity = "WATCH"
        elif total_breaches == 2:
            severity = "WARNING"
        else:
            severity = "CRITICAL"

        return {
            "breaches": breaches,
            "total_breaches": total_breaches,
            "severity": severity,
            "is_alert": total_breaches > 0,
        }

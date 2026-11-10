"""Autograder test suite for module S2 project: Inference Engine.

All tests evaluate properties, invariants, and exact conditions on the instance.
No expected numbers are hard-coded in failure messages.
"""

from __future__ import annotations

import copy
import os
from typing import Any

import numpy as np
import scipy.stats

try:
    import inference_engine as sol  # type: ignore[import-not-found]
except ImportError:
    try:
        from . import reference as sol  # type: ignore[import-not-found, no-redef]
    except ImportError:
        import reference as sol  # type: ignore[import-not-found, no-redef]

try:
    from instance import make_instance  # type: ignore[import-not-found]
except ImportError:
    from .instance import make_instance  # type: ignore[import-not-found]

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)
X: list[list[float]] = INST["X"]
Y: list[float] = INST["y"]
BETA_TRUE: list[float] = INST["beta_true"]
LAGS: int = INST["lags"]
CLUSTER_A: list[Any] = INST["cluster_a"]
CLUSTER_B: list[Any] = INST["cluster_b"]
DRAWS_Y: list[list[float]] = INST["draws_y"]


def check(condition: bool, message: str) -> None:
    """Fail with message when condition is false. The message names the property; it never reveals expected numbers."""
    __tracebackhide__ = True
    assert condition, message


def test_ols_normal_equations_and_orthogonality() -> None:
    """OLS beta must satisfy the normal equations (X'X)beta = X'y and yield orthogonal residuals X'e = 0."""
    b_hat = sol.ols_beta(X, Y)
    check(len(b_hat) == len(X[0]), "ols_beta must return a list of length equal to the number of columns k")
    x_arr = np.asarray(X, dtype=float)
    y_arr = np.asarray(Y, dtype=float)
    b_arr = np.asarray(b_hat, dtype=float)
    resid = y_arr - x_arr @ b_arr

    # Residual orthogonality: X'e ~ 0
    xt_e = x_arr.T @ resid
    check(
        bool(np.max(np.abs(xt_e)) < 1e-7),
        "Residuals must be orthogonal to the columns of X: max(|X'e|) exceeds 1e-7",
    )

    # Normal equations: (X'X)beta ~ X'y
    xt_x_b = (x_arr.T @ x_arr) @ b_arr
    xt_y = x_arr.T @ y_arr
    check(
        bool(np.max(np.abs(xt_x_b - xt_y)) < 1e-7),
        "OLS coefficient vector does not satisfy the normal equations (X'X)beta = X'y",
    )


def test_classical_standard_errors() -> None:
    """Classical standard errors must match sigma_hat * sqrt(diag((X'X)^{-1})) with divisor n - k."""
    se = sol.se_classical(X, Y)
    n = len(X)
    k = len(X[0])
    check(len(se) == k, "se_classical must return a list of length k")

    x_arr = np.asarray(X, dtype=float)
    y_arr = np.asarray(Y, dtype=float)
    b_arr = np.linalg.solve(x_arr.T @ x_arr, x_arr.T @ y_arr)
    resid = y_arr - x_arr @ b_arr
    rss = float(np.sum(resid**2))

    sigma2_unbiased = rss / (n - k)
    inv_xtx = np.linalg.inv(x_arr.T @ x_arr)
    expected_se = np.sqrt(sigma2_unbiased * np.diag(inv_xtx))

    # Check match to direct formula
    se_arr = np.asarray(se, dtype=float)
    rel_diff = np.abs(se_arr - expected_se) / expected_se
    check(
        bool(np.max(rel_diff) < 1e-7),
        "se_classical does not match the classical OLS covariance formula with n - k divisor",
    )

    # Mutant m08 check: must not use divisor n
    sigma2_biased = rss / n
    biased_se = np.sqrt(sigma2_biased * np.diag(inv_xtx))
    check(
        bool(np.max(np.abs(se_arr - biased_se)) > 1e-6),
        "se_classical appears to use divisor n rather than degrees-of-freedom divisor n - k",
    )


def test_white_hc0_standard_errors() -> None:
    """White standard errors must implement the HC0 sandwich (X'X)^{-1} (sum e_i^2 x_i x_i') (X'X)^{-1}."""
    se_w = sol.se_white(X, Y)
    k = len(X[0])
    check(len(se_w) == k, "se_white must return a list of length k")

    x_arr = np.asarray(X, dtype=float)
    y_arr = np.asarray(Y, dtype=float)
    b_arr = np.linalg.solve(x_arr.T @ x_arr, x_arr.T @ y_arr)
    resid = y_arr - x_arr @ b_arr
    inv_xtx = np.linalg.inv(x_arr.T @ x_arr)

    # Compute HC0 meat
    meat = np.zeros((k, k), dtype=float)
    for i in range(len(X)):
        xi = x_arr[i : i + 1, :]
        meat += (resid[i] ** 2) * (xi.T @ xi)
    expected_se = np.sqrt(np.diag(inv_xtx @ meat @ inv_xtx))

    se_w_arr = np.asarray(se_w, dtype=float)
    rel_diff = np.abs(se_w_arr - expected_se) / expected_se
    check(
        bool(np.max(rel_diff) < 1e-7),
        "se_white does not match the HC0 sandwich variance formula",
    )

    # Mutant m02 check: must not use absolute residual in meat
    meat_abs = np.zeros((k, k), dtype=float)
    for i in range(len(X)):
        xi = x_arr[i : i + 1, :]
        meat_abs += abs(resid[i]) * (xi.T @ xi)
    bad_abs_se = np.sqrt(np.diag(inv_xtx @ meat_abs @ inv_xtx))
    check(
        bool(np.max(np.abs(se_w_arr - bad_abs_se)) > 1e-5),
        "se_white must square the residuals in the sandwich meat, not use absolute values",
    )


def test_newey_west_lag_zero_identity() -> None:
    """With lags = 0, Newey-West standard errors must equal White HC0 standard errors exactly."""
    se_nw0 = sol.se_newey_west(X, Y, lags=0)
    se_w = sol.se_white(X, Y)
    se_nw0_arr = np.asarray(se_nw0, dtype=float)
    se_w_arr = np.asarray(se_w, dtype=float)
    diff = np.max(np.abs(se_nw0_arr - se_w_arr))
    check(
        bool(diff < 1e-8),
        "At lags = 0, Newey-West covariance must reduce identically to White HC0",
    )


def test_newey_west_bartlett_weights() -> None:
    """Newey-West standard errors for lags L >= 1 must apply Bartlett triangular weights."""
    lags = LAGS
    se_nw = sol.se_newey_west(X, Y, lags=lags)
    k = len(X[0])
    check(len(se_nw) == k, "se_newey_west must return a list of length k")

    x_arr = np.asarray(X, dtype=float)
    y_arr = np.asarray(Y, dtype=float)
    b_arr = np.linalg.solve(x_arr.T @ x_arr, x_arr.T @ y_arr)
    resid = y_arr - x_arr @ b_arr
    inv_xtx = np.linalg.inv(x_arr.T @ x_arr)

    # Meat with Bartlett weights
    omega = np.zeros((k, k), dtype=float)
    for t in range(len(X)):
        xt = x_arr[t : t + 1, :]
        omega += (resid[t] ** 2) * (xt.T @ xt)
    for j in range(1, lags + 1):
        weight = 1.0 - (float(j) / (lags + 1.0))
        gamma_j = np.zeros((k, k), dtype=float)
        for t in range(j, len(X)):
            xt = x_arr[t : t + 1, :]
            xt_prev = x_arr[t - j : t - j + 1, :]
            gamma_j += resid[t] * resid[t - j] * (xt.T @ xt_prev)
        omega += weight * (gamma_j + gamma_j.T)
    expected_se = np.sqrt(np.diag(inv_xtx @ omega @ inv_xtx))

    se_nw_arr = np.asarray(se_nw, dtype=float)
    rel_diff = np.abs(se_nw_arr - expected_se) / expected_se
    check(
        bool(np.max(rel_diff) < 1e-7),
        "se_newey_west does not match the Bartlett-weighted HAC sandwich formula",
    )

    # Mutant m03 check: uniform weights (no taper) must differ when lags >= 1 and autocorrelated
    omega_unif = np.zeros((k, k), dtype=float)
    for t in range(len(X)):
        xt = x_arr[t : t + 1, :]
        omega_unif += (resid[t] ** 2) * (xt.T @ xt)
    for j in range(1, lags + 1):
        gamma_j = np.zeros((k, k), dtype=float)
        for t in range(j, len(X)):
            xt = x_arr[t : t + 1, :]
            xt_prev = x_arr[t - j : t - j + 1, :]
            gamma_j += resid[t] * resid[t - j] * (xt.T @ xt_prev)
        omega_unif += 1.0 * (gamma_j + gamma_j.T)
    bad_unif_se = np.sqrt(np.diag(np.maximum(0.0, inv_xtx @ omega_unif @ inv_xtx)))
    check(
        bool(np.max(np.abs(se_nw_arr - bad_unif_se)) > 1e-6),
        "se_newey_west must apply Bartlett triangular weights 1 - j/(L+1), not uniform weights",
    )


def test_cluster_robust_standard_errors() -> None:
    """Cluster-robust standard errors must aggregate score vectors at the cluster level."""
    se_c = sol.se_cluster(X, Y, CLUSTER_A)
    k = len(X[0])
    check(len(se_c) == k, "se_cluster must return a list of length k")

    x_arr = np.asarray(X, dtype=float)
    y_arr = np.asarray(Y, dtype=float)
    b_arr = np.linalg.solve(x_arr.T @ x_arr, x_arr.T @ y_arr)
    resid = y_arr - x_arr @ b_arr
    inv_xtx = np.linalg.inv(x_arr.T @ x_arr)

    cluster_scores: dict[Any, np.ndarray] = {}
    for i, g in enumerate(CLUSTER_A):
        score_i = resid[i] * x_arr[i, :]
        if g not in cluster_scores:
            cluster_scores[g] = np.zeros(k, dtype=float)
        cluster_scores[g] += score_i

    meat = np.zeros((k, k), dtype=float)
    for s_g in cluster_scores.values():
        meat += np.outer(s_g, s_g)

    expected_se = np.sqrt(np.diag(inv_xtx @ meat @ inv_xtx))
    se_c_arr = np.asarray(se_c, dtype=float)
    rel_diff = np.abs(se_c_arr - expected_se) / expected_se
    check(
        bool(np.max(rel_diff) < 1e-7),
        "se_cluster does not match the CR0 cluster sandwich formula",
    )

    # Mutant m05 check: treating each observation as an individual cluster must differ
    se_w = sol.se_white(X, Y)
    check(
        bool(np.max(np.abs(se_c_arr - np.asarray(se_w, dtype=float))) > 1e-6),
        "se_cluster must sum scores by cluster group, not treat each row as a distinct cluster",
    )


def test_two_way_clustering() -> None:
    """Two-way clustering must compute V_A + V_B - V_{A cap B} and satisfy identical-clustering reduction."""
    # Identity: when clusterings are identical, V_two_way reduces to one-way cluster variance
    se_identical = sol.se_two_way(X, Y, CLUSTER_A, CLUSTER_A)
    se_single = sol.se_cluster(X, Y, CLUSTER_A)
    diff_id = np.max(np.abs(np.asarray(se_identical, dtype=float) - np.asarray(se_single, dtype=float)))
    check(
        bool(diff_id < 1e-8),
        "Two-way clustering with identical cluster groupings must equal one-way clustering identically",
    )

    # Formula check on distinct clusterings
    se_2way = sol.se_two_way(X, Y, CLUSTER_A, CLUSTER_B)
    check(len(se_2way) == len(X[0]), "se_two_way must return a list of length k")

    # Mutant m06 check: adding intersection term instead of subtracting must differ
    x_arr = np.asarray(X, dtype=float)
    y_arr = np.asarray(Y, dtype=float)
    b_arr = np.linalg.solve(x_arr.T @ x_arr, x_arr.T @ y_arr)
    resid = y_arr - x_arr @ b_arr
    inv_xtx = np.linalg.inv(x_arr.T @ x_arr)

    def get_var(cl: list[Any]) -> np.ndarray:
        scores: dict[Any, np.ndarray] = {}
        for i, g in enumerate(cl):
            s = resid[i] * x_arr[i, :]
            scores[g] = scores.get(g, np.zeros(len(s), dtype=float)) + s
        m = sum(np.outer(s, s) for s in scores.values())
        return inv_xtx @ m @ inv_xtx

    va = get_var(CLUSTER_A)
    vb = get_var(CLUSTER_B)
    vab = get_var([(CLUSTER_A[i], CLUSTER_B[i]) for i in range(len(X))])
    bad_additive = np.sqrt(np.diag(va + vb + vab))
    se_2way_arr = np.asarray(se_2way, dtype=float)
    check(
        bool(np.max(np.abs(se_2way_arr - bad_additive)) > 1e-6),
        "Two-way clustering must subtract the intersection covariance V_{A cap B}, not add it",
    )


def test_t_critical_values() -> None:
    """t_critical must return the 97.5th percentile of Student-t, differing from normal 1.96 for small df."""
    test_dfs = [1, 2, 5, 10, 30, 100]
    for df in test_dfs:
        crit = sol.t_critical(df)
        expected = float(scipy.stats.t.ppf(0.975, df))
        check(
            abs(crit - expected) < 1e-7,
            f"t_critical({df}) does not match scipy.stats.t.ppf(0.975, {df})",
        )

    # Mutant m09 check: must not return constant 1.96 for small df
    crit_1 = sol.t_critical(1)
    check(
        abs(crit_1 - 1.96) > 0.1,
        "t_critical must compute Student-t quantiles, not return a constant standard normal 1.96",
    )


def test_coverage_evaluation() -> None:
    """coverage must evaluate interval hits across draws for the requested method and column."""
    draws = [
        {
            "X": X,
            "y": y_i,
            "beta_true": BETA_TRUE,
            "lags": LAGS,
            "cluster_a": CLUSTER_A,
            "cluster_b": CLUSTER_B,
        }
        for y_i in DRAWS_Y
    ]

    cov_classical = sol.coverage(draws, "classical", 0)
    check(
        0.0 <= cov_classical <= 1.0,
        "coverage rate must be between 0.0 and 1.0",
    )

    cov_white = sol.coverage(draws, "white", 0)
    check(
        0.0 <= cov_white <= 1.0,
        "coverage rate must be between 0.0 and 1.0",
    )

    # Mutant m10 check: verify coverage is computed dynamically on the input draws, not a hardcoded seed-0 constant
    mock_draws = [
        {
            "X": X,
            "y": [val + 1000.0 for val in DRAWS_Y[0]],
            "beta_true": BETA_TRUE,
            "lags": LAGS,
            "cluster_a": CLUSTER_A,
            "cluster_b": CLUSTER_B,
        }
    ]
    shifted_cov = sol.coverage(mock_draws, "classical", 0)
    check(
        shifted_cov == 0.0,
        "coverage on severely shifted responses must be 0.0",
    )


def test_edge_cases() -> None:
    """All estimation functions must support minimal valid inputs: k = 1 (intercept only)."""
    n_small = 10
    x_single = [[1.0] for _ in range(n_small)]
    y_small = [2.0 + 0.1 * i for i in range(n_small)]
    cl_single = [i % 3 for i in range(n_small)]

    b_hat = sol.ols_beta(x_single, y_small)
    check(len(b_hat) == 1, "ols_beta must support k = 1 univariate regression")

    se_c = sol.se_classical(x_single, y_small)
    check(len(se_c) == 1 and se_c[0] > 0.0, "se_classical must support k = 1")

    se_w = sol.se_white(x_single, y_small)
    check(len(se_w) == 1 and se_w[0] > 0.0, "se_white must support k = 1")

    se_nw = sol.se_newey_west(x_single, y_small, lags=1)
    check(len(se_nw) == 1 and se_nw[0] > 0.0, "se_newey_west must support k = 1")

    se_cl = sol.se_cluster(x_single, y_small, cl_single)
    check(len(se_cl) == 1 and se_cl[0] > 0.0, "se_cluster must support k = 1")


def test_value_error_conditions() -> None:
    """ValueError must be raised for E1 (rank defect), E2 (n <= k), E3 (length mismatch), and E4 (lags bound)."""
    # E1: Rank deficiency
    # Duplicated column -> non-full rank
    x_bad = [[*row, row[-1]] for row in X]
    raised_e1 = False
    try:
        sol.ols_beta(x_bad, Y)
    except ValueError:
        raised_e1 = True
    check(raised_e1, "ols_beta must raise ValueError when X does not have full column rank (E1)")

    # E2: n <= k
    x_eq = X[: len(X[0])]
    y_eq = Y[: len(X[0])]
    raised_e2 = False
    try:
        sol.ols_beta(x_eq, y_eq)
    except ValueError:
        raised_e2 = True
    check(raised_e2, "ols_beta must raise ValueError when n <= k (E2)")

    # E3: Length mismatch
    y_short = Y[:-1]
    raised_e3_y = False
    try:
        sol.ols_beta(X, y_short)
    except ValueError:
        raised_e3_y = True
    check(raised_e3_y, "ols_beta must raise ValueError when len(y) != len(X) (E3)")

    raised_e3_cl = False
    try:
        sol.se_cluster(X, Y, CLUSTER_A[:-1])
    except ValueError:
        raised_e3_cl = True
    check(raised_e3_cl, "se_cluster must raise ValueError when cluster length != n (E3)")

    # E4: Lags out of bounds
    n = len(X)
    raised_e4_neg = False
    try:
        sol.se_newey_west(X, Y, lags=-1)
    except ValueError:
        raised_e4_neg = True
    check(raised_e4_neg, "se_newey_west must raise ValueError when lags < 0 (E4)")

    raised_e4_big = False
    try:
        sol.se_newey_west(X, Y, lags=n)
    except ValueError:
        raised_e4_big = True
    check(raised_e4_big, "se_newey_west must raise ValueError when lags >= n (E4)")

    # Valid boundary lags = n - 1 must succeed
    sol.se_newey_west(X, Y, lags=n - 1)


def test_no_input_mutation() -> None:
    """Functions must not mutate their input matrices or vectors."""
    x_copy = copy.deepcopy(X)
    y_copy = copy.deepcopy(Y)
    cl_a_copy = copy.deepcopy(CLUSTER_A)
    cl_b_copy = copy.deepcopy(CLUSTER_B)

    _ = sol.ols_beta(X, Y)
    _ = sol.se_classical(X, Y)
    _ = sol.se_white(X, Y)
    _ = sol.se_newey_west(X, Y, lags=LAGS)
    _ = sol.se_cluster(X, Y, CLUSTER_A)
    _ = sol.se_two_way(X, Y, CLUSTER_A, CLUSTER_B)

    check(x_copy == X, "Inputs must not be mutated: X was modified during computation")
    check(y_copy == Y, "Inputs must not be mutated: y was modified during computation")
    check(cl_a_copy == CLUSTER_A, "Inputs must not be mutated: cluster_a was modified")
    check(cl_b_copy == CLUSTER_B, "Inputs must not be mutated: cluster_b was modified")

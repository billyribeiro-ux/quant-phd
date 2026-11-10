"""Student error: inverts the Kalman gain formula as F / P_pred instead of P_pred / F."""

from __future__ import annotations

import math
from collections.abc import Sequence


def garch11_variance(returns: Sequence[float], omega: float, alpha: float, beta: float) -> list[float]:
    """Compute GARCH(1,1) conditional variance sequence h_t.

    h_0 is set to the sample variance of returns (divisor n).
    For t >= 1: h_t = omega + alpha * returns[t-1]^2 + beta * h_{t-1}.
    """
    n = len(returns)
    if n < 2:
        raise ValueError("fewer than 2 returns")
    if omega <= 0.0:
        raise ValueError("omega must be strictly positive")
    if alpha < 0.0:
        raise ValueError("alpha must be non-negative")
    if beta < 0.0:
        raise ValueError("beta must be non-negative")

    mean_r = sum(returns) / n
    h0 = sum((r - mean_r) ** 2 for r in returns) / n
    if h0 <= 0.0:
        h0 = 1e-6

    h: list[float] = [h0]
    for t in range(1, n):
        ht = omega + alpha * (returns[t - 1] ** 2) + beta * h[-1]
        h.append(ht)
    return h


def garch11_loglik(returns: Sequence[float], omega: float, alpha: float, beta: float) -> float:
    """Compute Gaussian quasi-log-likelihood for GARCH(1,1).

    loglik = -0.5 * sum_{t=0}^{n-1} [ln(2*pi) + ln(h_t) + returns[t]^2 / h_t].
    """
    h = garch11_variance(returns, omega, alpha, beta)
    log2pi = math.log(2.0 * math.pi)
    total = 0.0
    for r, ht in zip(returns, h, strict=True):
        if ht <= 0.0:
            return -1e15
        total += log2pi + math.log(ht) + (r * r) / ht
    return -0.5 * total


def garch11_fit(returns: Sequence[float]) -> dict[str, float]:
    """Fit GARCH(1,1) model by quasi-maximum likelihood."""
    n = len(returns)
    if n < 50:
        raise ValueError("fewer than 50 returns")
    for r in returns:
        if not math.isfinite(r):
            raise ValueError("non-finite return in input")

    mean_r = sum(returns) / n
    var_r = sum((r - mean_r) ** 2 for r in returns) / n
    if var_r <= 0.0:
        var_r = 1e-6

    # Nelder-Mead on 3 parameters: [omega, alpha, beta]
    def obj(p: list[float]) -> float:
        om, al, be = p[0], p[1], p[2]
        if om <= 1e-8 or al < 0.0 or be < 0.0 or al + be >= 0.9999:
            return 1e15
        return -garch11_loglik(returns, om, al, be)

    dim = 3
    x0 = [0.05 * var_r, 0.08, 0.85]
    sim = [list(x0)]
    steps = [0.01 * var_r, 0.02, 0.02]
    for i in range(dim):
        p = list(x0)
        p[i] += steps[i]
        sim.append(p)

    scores = [obj(p) for p in sim]
    for _ in range(250):
        indices = sorted(range(dim + 1), key=lambda k: scores[k])
        sim = [sim[k] for k in indices]
        scores = [scores[k] for k in indices]

        if scores[-1] - scores[0] < 1e-5:
            break

        centroid = [sum(sim[k][j] for k in range(dim)) / dim for j in range(dim)]
        xr = [centroid[j] + 1.0 * (centroid[j] - sim[-1][j]) for j in range(dim)]
        sr = obj(xr)

        if scores[0] <= sr < scores[-2]:
            sim[-1] = xr
            scores[-1] = sr
            continue
        if sr < scores[0]:
            xe = [centroid[j] + 2.0 * (xr[j] - centroid[j]) for j in range(dim)]
            se = obj(xe)
            if se < sr:
                sim[-1] = xe
                scores[-1] = se
            else:
                sim[-1] = xr
                scores[-1] = sr
            continue

        xc = [centroid[j] + 0.5 * (sim[-1][j] - centroid[j]) for j in range(dim)]
        sc = obj(xc)
        if sc < scores[-1]:
            sim[-1] = xc
            scores[-1] = sc
            continue

        for i in range(1, dim + 1):
            sim[i] = [sim[0][j] + 0.5 * (sim[i][j] - sim[0][j]) for j in range(dim)]
            scores[i] = obj(sim[i])

    best = sim[0]
    return {
        "omega": best[0],
        "alpha": best[1],
        "beta": best[2],
        "loglik": -scores[0],
    }


def har_design(rv: Sequence[float]) -> tuple[list[list[float]], list[float]]:
    """Build HAR design matrix X and response vector y for t >= 22 (0-indexed)."""
    n = len(rv)
    if n < 23:
        raise ValueError("fewer than 23 observations in rv")
    for v in rv:
        if v <= 0.0 or not math.isfinite(v):
            raise ValueError("all realized volatility values must be positive and finite")

    x_mat: list[list[float]] = []
    y: list[float] = []
    for t in range(22, n):
        d = rv[t - 1]
        w = sum(rv[t - 5 : t]) / 5.0
        m = sum(rv[t - 22 : t]) / 22.0
        x_mat.append([1.0, d, w, m])
        y.append(rv[t])
    return x_mat, y


def _inv4(a_mat: list[list[float]]) -> list[list[float]]:
    """Invert 4x4 matrix using Gauss-Jordan elimination with partial pivoting."""
    n = 4
    m_mat = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(a_mat)]
    for i in range(n):
        pivot_row = i
        max_val = abs(m_mat[i][i])
        for r in range(i + 1, n):
            if abs(m_mat[r][i]) > max_val:
                max_val = abs(m_mat[r][i])
                pivot_row = r
        if max_val < 1e-12:
            raise ValueError("singular design matrix")
        if pivot_row != i:
            m_mat[i], m_mat[pivot_row] = m_mat[pivot_row], m_mat[i]

        pivot = m_mat[i][i]
        for c in range(2 * n):
            m_mat[i][c] /= pivot
        for r in range(n):
            if r != i:
                factor = m_mat[r][i]
                for c in range(2 * n):
                    m_mat[r][c] -= factor * m_mat[i][c]

    return [[m_mat[i][j] for j in range(n, 2 * n)] for i in range(n)]


def har_fit(rv: Sequence[float]) -> list[float]:
    """Fit HAR-RV model via OLS normal equations."""
    x_mat, y = har_design(rv)
    n_rows = len(x_mat)
    n_cols = 4

    # Check for constant column or degenerate variation
    for c in range(1, n_cols):
        vals = [x_mat[r][c] for r in range(n_rows)]
        m_val = sum(vals) / n_rows
        var_col = sum((v - m_val) ** 2 for v in vals)
        if var_col < 1e-14:
            raise ValueError("singular design matrix")

    xt_mat = [[x_mat[r][c] for r in range(n_rows)] for c in range(n_cols)]
    xtx_mat = [[sum(xt_mat[i][k] * x_mat[k][j] for k in range(n_rows)) for j in range(n_cols)] for i in range(n_cols)]
    inv_xtx = _inv4(xtx_mat)
    xty_vec = [sum(xt_mat[i][k] * y[k] for k in range(n_rows)) for i in range(n_cols)]
    beta = [sum(inv_xtx[i][j] * xty_vec[j] for j in range(n_cols)) for i in range(n_cols)]
    return beta


def har_forecast(rv: Sequence[float], t: int, coefs: Sequence[float]) -> float:
    """Compute one-step out-of-sample HAR forecast for index t using rv[0:t]."""
    if t < 22 or t > len(rv):
        raise ValueError("t out of bounds for HAR forecast")
    d = rv[t - 1]
    w = sum(rv[t - 5 : t]) / 5.0
    m = sum(rv[t - 22 : t]) / 22.0
    return float(coefs[0] + coefs[1] * d + coefs[2] * w + coefs[3] * m)


def qlike(realized: float, forecast: float) -> float:
    """Compute QLIKE loss: (realized / forecast) - ln(realized / forecast) - 1.0."""
    if realized <= 0.0 or forecast <= 0.0:
        raise ValueError("realized and forecast must be strictly positive")
    ratio = realized / forecast
    return float(ratio - math.log(ratio) - 1.0)


def mse_loss(realized: float, forecast: float) -> float:
    """Compute mean squared error loss: (realized - forecast)^2."""
    diff = realized - forecast
    return float(diff * diff)


def kalman_local_level_filter(y: Sequence[float], sigma_w2: float, sigma_v2: float) -> list[float]:
    """Filter the local-level model x_t = x_{t-1} + w_t, y_t = x_t + v_t."""
    n = len(y)
    if n == 0:
        raise ValueError("y must not be empty")
    if sigma_w2 < 0.0:
        raise ValueError("sigma_w2 must be non-negative")
    if sigma_v2 <= 0.0:
        raise ValueError("sigma_v2 must be strictly positive")

    # Initial state
    a = y[0]
    p_cov = sigma_v2

    filtered: list[float] = [float(a)]
    for t in range(1, n):
        a_pred = a
        p_pred = p_cov + sigma_w2
        v = y[t] - a_pred
        f_var = p_pred + sigma_v2
        k_gain = f_var / p_pred
        a = a_pred + k_gain * v
        p_cov = p_pred * (1.0 - k_gain)
        filtered.append(float(a))
    return filtered


def arma11_fit(x: Sequence[float]) -> dict[str, float]:
    """Fit ARMA(1,1) model by conditional sum of squares."""
    n = len(x)
    if n < 30:
        raise ValueError("fewer than 30 observations in x")

    mean_x = sum(x) / n
    tx = [v - mean_x for v in x]

    def css(phi: float, theta: float) -> float:
        if abs(phi) >= 0.999 or abs(theta) >= 0.999:
            return 1e15
        eps = [0.0]
        total = 0.0
        for t in range(1, n):
            e = tx[t] - phi * tx[t - 1] - theta * eps[-1]
            eps.append(e)
            total += e * e
        return total

    # 2D Nelder-Mead on [phi, theta]
    p0 = [0.2, 0.2]
    sim = [list(p0), [p0[0] + 0.1, p0[1]], [p0[0], p0[1] + 0.1]]
    scores = [css(p[0], p[1]) for p in sim]

    for _ in range(120):
        idx = sorted(range(3), key=lambda k: scores[k])
        sim = [sim[k] for k in idx]
        scores = [scores[k] for k in idx]

        if scores[-1] - scores[0] < 1e-6:
            break

        c = [(sim[0][j] + sim[1][j]) / 2.0 for j in range(2)]
        xr = [c[j] + 1.0 * (c[j] - sim[2][j]) for j in range(2)]
        sr = css(xr[0], xr[1])

        if scores[0] <= sr < scores[1]:
            sim[2] = xr
            scores[2] = sr
            continue
        if sr < scores[0]:
            xe = [c[j] + 2.0 * (xr[j] - c[j]) for j in range(2)]
            se = css(xe[0], xe[1])
            if se < sr:
                sim[2] = xe
                scores[2] = se
            else:
                sim[2] = xr
                scores[2] = sr
            continue

        xc = [c[j] + 0.5 * (sim[2][j] - c[j]) for j in range(2)]
        sc = css(xc[0], xc[1])
        if sc < scores[2]:
            sim[2] = xc
            scores[2] = sc
            continue

        for i in range(1, 3):
            sim[i] = [sim[0][j] + 0.5 * (sim[i][j] - sim[0][j]) for j in range(2)]
            scores[i] = css(sim[i][0], sim[i][1])

    best = sim[0]
    sigma2 = scores[0] / (n - 1)
    return {
        "phi": float(best[0]),
        "theta": float(best[1]),
        "sigma2": float(sigma2),
    }

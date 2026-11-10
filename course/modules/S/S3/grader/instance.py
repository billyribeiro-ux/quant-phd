"""Instance generator for the S3 project: Pairs-trading audit.

SIMULATED instances: generates synthetic currency and asset pairs with planted
statistical properties to test cointegration analysis, half-life estimation,
and out-of-sample survival filtering.

Deterministic for each seed in [0, 49].
"""

from __future__ import annotations

import functools
import math
import random
from typing import Any

CRITICAL_VALUES: dict[int, tuple[float, float]] = {
    240: (-2.8512, -3.3378),
    270: (-2.8568, -3.3395),
    300: (-2.8658, -3.3449),
    330: (-2.8820, -3.3630),
    360: (-2.8576, -3.3375),
    4023: (-2.8611, -3.3287),
}


def _ols_1d(y: list[float], x: list[float]) -> tuple[float, float]:
    m = len(y)
    mean_x = sum(x) / m
    mean_y = sum(y) / m
    cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(m))
    var = sum((x[i] - mean_x) ** 2 for i in range(m))
    beta = cov / var
    alpha = mean_y - beta * mean_x
    return alpha, beta


def _eg_t(y: list[float], x: list[float], split: int, lags: int = 1) -> float:
    alpha, beta = _ols_1d(y[:split], x[:split])
    u = [y[t] - alpha - beta * x[t] for t in range(split)]
    m = len(u)
    du = [u[i] - u[i - 1] for i in range(1, m)]
    y_dep = du[1:]
    x_mat = [[u[t - 1], du[t - 2]] for t in range(2, m)]
    n_obs = len(y_dep)
    s_xx00 = sum(x_mat[r][0] * x_mat[r][0] for r in range(n_obs))
    s_xx01 = sum(x_mat[r][0] * x_mat[r][1] for r in range(n_obs))
    s_xx11 = sum(x_mat[r][1] * x_mat[r][1] for r in range(n_obs))
    det2 = s_xx00 * s_xx11 - s_xx01 * s_xx01
    inv00 = s_xx11 / det2
    inv01 = -s_xx01 / det2
    inv11 = s_xx00 / det2
    s_xy0 = sum(x_mat[r][0] * y_dep[r] for r in range(n_obs))
    s_xy1 = sum(x_mat[r][1] * y_dep[r] for r in range(n_obs))
    gamma = inv00 * s_xy0 + inv01 * s_xy1
    delta = inv01 * s_xy0 + inv11 * s_xy1
    res = [y_dep[r] - (gamma * x_mat[r][0] + delta * x_mat[r][1]) for r in range(n_obs)]
    s2 = sum(r * r for r in res) / (n_obs - 2)
    se_gamma = math.sqrt(s2 * inv00)
    return gamma / se_gamma


def _adf_t(series: list[float], lags: int = 1) -> float:
    m = len(series)
    dy = [series[i] - series[i - 1] for i in range(1, m)]
    y_dep = dy[1:]
    x_rows = [[1.0, series[t - 1], dy[t - 2]] for t in range(2, m)]
    n_obs = len(y_dep)
    xtx = [[sum(x_rows[r][i] * x_rows[r][j] for r in range(n_obs)) for j in range(3)] for i in range(3)]
    xty = [sum(x_rows[r][i] * y_dep[r] for r in range(n_obs)) for i in range(3)]

    def det3(a: list[list[float]]) -> float:
        return (
            a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
        )

    d = det3(xtx)
    inv11 = (xtx[0][0] * xtx[2][2] - xtx[0][2] * xtx[2][0]) / d
    inv10 = (xtx[1][2] * xtx[2][0] - xtx[1][0] * xtx[2][2]) / d
    inv12 = (xtx[0][2] * xtx[1][0] - xtx[0][0] * xtx[1][2]) / d
    b1 = inv10 * xty[0] + inv11 * xty[1] + inv12 * xty[2]

    # For residuals, need full b vector
    inv00 = (xtx[1][1] * xtx[2][2] - xtx[1][2] * xtx[2][1]) / d
    inv01 = (xtx[0][2] * xtx[2][1] - xtx[0][1] * xtx[2][2]) / d
    inv02 = (xtx[0][1] * xtx[1][2] - xtx[0][2] * xtx[1][1]) / d
    b0 = inv00 * xty[0] + inv01 * xty[1] + inv02 * xty[2]
    inv20 = (xtx[1][0] * xtx[2][1] - xtx[1][1] * xtx[2][0]) / d
    inv21 = (xtx[0][1] * xtx[2][0] - xtx[0][0] * xtx[2][1]) / d
    inv22 = (xtx[0][0] * xtx[1][1] - xtx[0][1] * xtx[1][0]) / d
    b2 = inv20 * xty[0] + inv21 * xty[1] + inv22 * xty[2]

    b = [b0, b1, b2]
    res = [y_dep[r] - sum(x_rows[r][j] * b[j] for j in range(3)) for r in range(n_obs)]
    s2 = sum(r * r for r in res) / (n_obs - 3)
    se = math.sqrt(s2 * inv11)
    return b1 / se


@functools.lru_cache(maxsize=128)
def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic synthetic pairs-trading dataset for the given seed.

    Returns a dictionary containing:
    - seed: int
    - n: int, total sample length in {400, 450, 500, 550, 600}
    - split: int, formation window length floor(0.6 * n)
    - df_critical_5pct: float, precomputed 5% DF critical value
    - eg_critical_5pct: float, precomputed 5% EG critical value
    - pairs: list of 6 pair dictionaries with series 'y' and 'x'
    """
    rng = random.Random(seed * 7919 + 17)
    lengths = [400, 450, 500, 550, 600]
    n = lengths[seed % len(lengths)]
    split = math.floor(0.6 * n)
    df_crit, eg_crit = CRITICAL_VALUES[split]

    pairs: list[dict[str, Any]] = []

    # Pair 0: noise-free exact linear relation for alpha_beta test
    alpha_0 = 1.5 + (seed % 7) * 0.25
    beta_0 = 0.8 + (seed % 5) * 0.15
    x0 = [10.0 + rng.gauss(0.0, 1.0) + 0.05 * t for t in range(n)]
    y0 = [alpha_0 + beta_0 * val for val in x0]
    pairs.append(
        {
            "name": "noise_free",
            "y": y0,
            "x": x0,
            "true_alpha": alpha_0,
            "true_beta": beta_0,
            "expected_survives": False,
        }
    )

    # Pair 1: strong cointegration (passes EG and trading half-life)
    alpha_1 = 2.0 + rng.uniform(-0.5, 0.5)
    beta_1 = 1.2 + rng.uniform(-0.2, 0.2)
    phi_1 = 0.70 + (seed % 4) * 0.03
    x1: list[float] = []
    y1: list[float] = []
    for _ in range(30):
        rw1 = [0.0]
        for _ in range(n - 1):
            rw1.append(rw1[-1] + rng.gauss(0.0, 1.0))
        x1 = [50.0 + rw1[t] for t in range(n)]
        s1 = [0.0]
        for _ in range(n - 1):
            s1.append(phi_1 * s1[-1] + rng.gauss(0.0, 0.5))
        y1 = [alpha_1 + beta_1 * x1[t] + s1[t] for t in range(n)]
        stat1 = _eg_t(y1, x1, split, lags=1)
        if stat1 < eg_crit:
            break

    pairs.append(
        {
            "name": "coint_1",
            "y": y1,
            "x": x1,
            "true_alpha": alpha_1,
            "true_beta": beta_1,
            "planted_phi": phi_1,
            "expected_survives": True,
        }
    )

    # Pair 2: marginal pair strictly between eg_crit and df_crit
    # Calibrated dynamically per seed
    alpha_2 = 1.0 + rng.uniform(-0.3, 0.3)
    beta_2 = 0.75 + rng.uniform(-0.1, 0.1)
    rw2 = [0.0]
    for _ in range(n - 1):
        rw2.append(rw2[-1] + rng.gauss(0.0, 1.0))
    x2 = [60.0 + rw2[t] for t in range(n)]

    phi_2 = 0.90
    y2: list[float] = []
    for _ in range(30):
        s2 = [0.0]
        for _ in range(n - 1):
            s2.append(phi_2 * s2[-1] + rng.gauss(0.0, 0.5))
        y2 = [alpha_2 + beta_2 * x2[t] + s2[t] for t in range(n)]
        stat2 = _eg_t(y2, x2, split, lags=1)
        if eg_crit < stat2 < df_crit:
            break
        phi_2 = min(0.985, phi_2 + 0.015) if stat2 <= eg_crit else max(0.75, phi_2 - 0.015)

    pairs.append(
        {
            "name": "marginal_pair",
            "y": y2,
            "x": x2,
            "true_alpha": alpha_2,
            "true_beta": beta_2,
            "expected_survives": False,
        }
    )

    # Pair 3: independent random walk 1 (no cointegration)
    x3: list[float] = []
    y3: list[float] = []
    for _ in range(100):
        rw3_x = [0.0]
        rw3_y = [0.0]
        for _ in range(n - 1):
            rw3_x.append(rw3_x[-1] + rng.gauss(0.0, 1.0))
            rw3_y.append(rw3_y[-1] + rng.gauss(0.0, 1.0))
        x3 = [80.0 + rw3_x[t] for t in range(n)]
        y3 = [60.0 + rw3_y[t] for t in range(n)]
        stat3 = _eg_t(y3, x3, split, lags=1)
        stat_adf3 = _adf_t(y3[:split], lags=1)
        if stat3 > eg_crit and stat_adf3 > df_crit:
            break

    pairs.append(
        {
            "name": "rw_indep_1",
            "y": y3,
            "x": x3,
            "expected_survives": False,
        }
    )

    # Pair 4: independent random walk 2 (no cointegration)
    x4: list[float] = []
    y4: list[float] = []
    for _ in range(100):
        rw4_x = [0.0]
        rw4_y = [0.0]
        for _ in range(n - 1):
            rw4_x.append(rw4_x[-1] + rng.gauss(0.0, 1.0))
            rw4_y.append(rw4_y[-1] + rng.gauss(0.0, 1.0))
        x4 = [120.0 + rw4_x[t] for t in range(n)]
        y4 = [90.0 + rw4_y[t] for t in range(n)]
        stat4 = _eg_t(y4, x4, split, lags=1)
        stat_adf4 = _adf_t(y4[:split], lags=1)
        if stat4 > eg_crit and stat_adf4 > df_crit:
            break

    pairs.append(
        {
            "name": "rw_indep_2",
            "y": y4,
            "x": x4,
            "expected_survives": False,
        }
    )

    # Pair 5: break pair (cointegrated in formation, explosive/unit-root in trading)
    alpha_5 = 3.0 + rng.uniform(-0.2, 0.2)
    beta_5 = 1.1 + rng.uniform(-0.1, 0.1)
    rw5 = [0.0]
    for _ in range(n - 1):
        rw5.append(rw5[-1] + rng.gauss(0.0, 1.0))
    x5 = [70.0 + rw5[t] for t in range(n)]
    s5_form = [0.0]
    for _ in range(split - 1):
        s5_form.append(0.65 * s5_form[-1] + rng.gauss(0.0, 0.4))
    s5_trading = [s5_form[-1]]
    for _ in range(n - split):
        s5_trading.append(1.03 * s5_trading[-1] + 0.1 + rng.gauss(0.0, 0.05))
    s5_full = s5_form + s5_trading[1:]
    y5 = [alpha_5 + beta_5 * x5[t] + s5_full[t] for t in range(n)]
    pairs.append(
        {
            "name": "break_pair",
            "y": y5,
            "x": x5,
            "true_alpha": alpha_5,
            "true_beta": beta_5,
            "expected_survives": False,
        }
    )

    return {
        "seed": seed,
        "n": n,
        "split": split,
        "df_critical_5pct": df_crit,
        "eg_critical_5pct": eg_crit,
        "pairs": pairs,
    }

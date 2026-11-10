"""Reference solution and pricing library for Atlas milestone A6 (atlas.pricing).

Provides analytical Black-Scholes-Merton, binomial trees, trinomial trees,
finite difference PDE solvers, European Monte Carlo, Longstaff-Schwartz LSMC,
and cross-method pricing consistency validation.
"""

from __future__ import annotations

import math
from typing import Any, NamedTuple

import numpy as np


class PriceResult(NamedTuple):
    """Container for option pricing results and Greeks."""

    price: float
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    se: float | None = None


def _validate_basic_inputs(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    dividend_yield: float,
) -> None:
    if spot <= 0.0:
        raise ValueError(f"Spot price must be positive, got {spot}")
    if strike <= 0.0:
        raise ValueError(f"Strike price must be positive, got {strike}")
    if vol <= 0.0:
        raise ValueError(f"Volatility must be positive, got {vol}")
    if maturity <= 0.0:
        raise ValueError(f"Maturity must be positive, got {maturity}")
    if dividend_yield < 0.0:
        raise ValueError(f"Dividend yield must be non-negative, got {dividend_yield}")


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def bsm_price(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    is_call: bool = True,
    dividend_yield: float = 0.0,
) -> PriceResult:
    """Analytical Black-Scholes-Merton European option pricing and exact Greeks."""
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)

    sqrt_t = math.sqrt(maturity)
    d1 = (math.log(spot / strike) + (rate - dividend_yield + 0.5 * vol * vol) * maturity) / (vol * sqrt_t)
    d2 = d1 - vol * sqrt_t

    df_r = math.exp(-rate * maturity)
    df_q = math.exp(-dividend_yield * maturity)

    pdf_d1 = _norm_pdf(d1)
    cdf_d1 = _norm_cdf(d1)
    cdf_d2 = _norm_cdf(d2)

    if is_call:
        price = spot * df_q * cdf_d1 - strike * df_r * cdf_d2
        delta = df_q * cdf_d1
        theta = (
            -(spot * vol * df_q * pdf_d1) / (2.0 * sqrt_t)
            - rate * strike * df_r * cdf_d2
            + dividend_yield * spot * df_q * cdf_d1
        )
        rho = strike * maturity * df_r * cdf_d2
    else:
        cdf_neg_d1 = _norm_cdf(-d1)
        cdf_neg_d2 = _norm_cdf(-d2)
        price = strike * df_r * cdf_neg_d2 - spot * df_q * cdf_neg_d1
        delta = -df_q * cdf_neg_d1
        theta = (
            -(spot * vol * df_q * pdf_d1) / (2.0 * sqrt_t)
            + rate * strike * df_r * cdf_neg_d2
            - dividend_yield * spot * df_q * cdf_neg_d1
        )
        rho = -strike * maturity * df_r * cdf_neg_d2

    gamma = df_q * pdf_d1 / (spot * vol * sqrt_t)
    vega = spot * df_q * sqrt_t * pdf_d1

    return PriceResult(price=price, delta=delta, gamma=gamma, theta=theta, vega=vega, rho=rho)


def binomial_tree_price(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    n_steps: int = 200,
    is_call: bool = True,
    is_american: bool = False,
    dividend_yield: float = 0.0,
) -> PriceResult:
    """Cox-Ross-Rubinstein recombining binomial tree with early-exercise capability."""
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    if n_steps < 2:
        raise ValueError(f"Number of tree steps must be at least 2, got {n_steps}")

    dt = maturity / n_steps
    u = math.exp(vol * math.sqrt(dt))
    d = 1.0 / u
    df = math.exp(-rate * dt)
    drift = math.exp((rate - dividend_yield) * dt)
    p = (drift - d) / (u - d)

    if not (0.0 < p < 1.0):
        p = max(1e-8, min(1.0 - 1e-8, p))

    # Terminal stock prices and payoffs
    s_terminal = spot * (u ** np.arange(n_steps + 1)) * (d ** np.arange(n_steps, -1, -1))
    v = np.maximum(s_terminal - strike, 0.0) if is_call else np.maximum(strike - s_terminal, 0.0)

    v_level2 = np.zeros(3, dtype=float)
    v_level1 = np.zeros(2, dtype=float)

    for k in range(n_steps - 1, -1, -1):
        v_next = df * (p * v[1 : k + 2] + (1.0 - p) * v[0 : k + 1])
        if is_american:
            s_k = spot * (u ** np.arange(k + 1)) * (d ** np.arange(k, -1, -1))
            intrinsic = np.maximum(s_k - strike if is_call else strike - s_k, 0.0)
            v_next = np.maximum(v_next, intrinsic)
        v = v_next
        if k == 2:
            v_level2 = v.copy()
        elif k == 1:
            v_level1 = v.copy()

    price = float(v[0])

    # Greeks extracted directly from lattice nodes
    s_1_0 = spot * d
    s_1_1 = spot * u
    delta = float((v_level1[1] - v_level1[0]) / (s_1_1 - s_1_0))

    s_2_0 = spot * d * d
    s_2_1 = spot
    s_2_2 = spot * u * u
    d1_val = (v_level2[2] - v_level2[1]) / (s_2_2 - s_2_1)
    d0_val = (v_level2[1] - v_level2[0]) / (s_2_1 - s_2_0)
    gamma = float((d1_val - d0_val) / (0.5 * (s_2_2 - s_2_0)))
    theta = float((v_level2[1] - price) / (2.0 * dt))

    # Vega and Rho via analytical BSM consistency
    bsm_equiv = bsm_price(spot, strike, rate, vol, maturity, is_call, dividend_yield)
    vega = bsm_equiv.vega
    rho = bsm_equiv.rho

    return PriceResult(price=price, delta=delta, gamma=gamma, theta=theta, vega=vega, rho=rho)


def trinomial_tree_price(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    n_steps: int = 150,
    is_call: bool = True,
    is_american: bool = False,
    dividend_yield: float = 0.0,
) -> PriceResult:
    """Boyle (1977) 3-branch recombining trinomial tree matching drift and variance."""
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    if n_steps < 2:
        raise ValueError(f"Number of tree steps must be at least 2, got {n_steps}")

    dt = maturity / n_steps
    dx = vol * math.sqrt(3.0 * dt)
    u = math.exp(dx)
    d = 1.0 / u
    df = math.exp(-rate * dt)
    nu = (rate - dividend_yield - 0.5 * vol * vol) * dt

    pu = 1.0 / 6.0 + 0.5 * (nu * nu / (dx * dx) + nu / dx)
    pm = 2.0 / 3.0 - (nu * nu / (dx * dx))
    pd = 1.0 / 6.0 + 0.5 * (nu * nu / (dx * dx) - nu / dx)

    if pu < 0.0 or pm < 0.0 or pd < 0.0:
        pu = max(1e-8, min(1.0 - 2e-8, pu))
        pd = max(1e-8, min(1.0 - 2e-8, pd))
        pm = max(1e-8, 1.0 - pu - pd)

    indices = np.arange(-n_steps, n_steps + 1)
    s_terminal = spot * np.exp(indices * dx)

    v = np.maximum(s_terminal - strike, 0.0) if is_call else np.maximum(strike - s_terminal, 0.0)

    v_level1 = np.zeros(3, dtype=float)

    for k in range(n_steps - 1, -1, -1):
        v_next = df * (pu * v[2 : 2 * k + 3] + pm * v[1 : 2 * k + 2] + pd * v[0 : 2 * k + 1])
        if is_american:
            k_indices = np.arange(-k, k + 1)
            s_k = spot * np.exp(k_indices * dx)
            intrinsic = np.maximum(s_k - strike if is_call else strike - s_k, 0.0)
            v_next = np.maximum(v_next, intrinsic)
        v = v_next
        if k == 1:
            v_level1 = v.copy()

    price = float(v[0])

    # Greeks from step 1
    s_down = spot * d
    s_mid = spot
    s_up = spot * u

    delta = float((v_level1[2] - v_level1[0]) / (s_up - s_down))
    d_up = (v_level1[2] - v_level1[1]) / (s_up - s_mid)
    d_down = (v_level1[1] - v_level1[0]) / (s_mid - s_down)
    gamma = float((d_up - d_down) / (0.5 * (s_up - s_down)))
    theta = float((v_level1[1] - price) / dt)

    bsm_equiv = bsm_price(spot, strike, rate, vol, maturity, is_call, dividend_yield)
    vega = bsm_equiv.vega
    rho = bsm_equiv.rho

    return PriceResult(price=price, delta=delta, gamma=gamma, theta=theta, vega=vega, rho=rho)


def _thomas_solve(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Solve tridiagonal linear system A x = d using Thomas algorithm (O(N))."""
    n = len(d)
    c_prime = np.zeros(n, dtype=float)
    d_prime = np.zeros(n, dtype=float)
    x = np.zeros(n, dtype=float)

    c_prime[0] = c[0] / b[0]
    d_prime[0] = d[0] / b[0]

    for i in range(1, n):
        denom = b[i] - a[i] * c_prime[i - 1]
        c_prime[i] = c[i] / denom if i < n - 1 else 0.0
        d_prime[i] = (d[i] - a[i] * d_prime[i - 1]) / denom

    x[-1] = d_prime[-1]
    for i in range(n - 2, -1, -1):
        x[i] = d_prime[i] - c_prime[i] * x[i + 1]

    return x


def pde_price(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    n_time_steps: int = 100,
    n_spot_steps: int = 100,
    is_call: bool = True,
    is_american: bool = False,
    dividend_yield: float = 0.0,
    scheme: str = "crank_nicolson",
) -> PriceResult:
    """Finite difference solver for Black-Scholes PDE on log-spot grid."""
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    if n_time_steps <= 0:
        raise ValueError(f"Time steps must be positive, got {n_time_steps}")
    if n_spot_steps < 3:
        raise ValueError(f"Spot steps must be at least 3, got {n_spot_steps}")
    if scheme not in ("explicit", "implicit", "crank_nicolson"):
        raise ValueError(f"Scheme must be explicit, implicit, or crank_nicolson, got {scheme}")

    std = vol * math.sqrt(maturity)
    x_max = 4.5 * std + max(0.0, (rate - dividend_yield) * maturity)
    x_min = -4.5 * std + min(0.0, (rate - dividend_yield) * maturity)

    dx = (x_max - x_min) / (n_spot_steps - 1)
    dt = maturity / n_time_steps

    x = np.linspace(x_min, x_max, n_spot_steps)
    s_grid = strike * np.exp(x)

    v = np.maximum(s_grid - strike, 0.0) if is_call else np.maximum(strike - s_grid, 0.0)

    mu = rate - dividend_yield - 0.5 * vol * vol
    alpha = 0.5 * (vol * vol) / (dx * dx)
    beta = 0.5 * mu / dx

    a_coef = alpha - beta
    b_coef = -2.0 * alpha - rate
    c_coef = alpha + beta

    theta_weight = 0.5 if scheme == "crank_nicolson" else (1.0 if scheme == "implicit" else 0.0)

    if scheme == "explicit":
        dt_max = dx * dx / (vol * vol + 1e-12)
        sub_steps = max(1, math.ceil(dt / dt_max) * 2)
        dt_sub = dt / sub_steps
        actual_time_steps = n_time_steps * sub_steps

        for _ in range(actual_time_steps):
            v_new = v.copy()
            v_new[1:-1] = v[1:-1] + dt_sub * (a_coef * v[:-2] + b_coef * v[1:-1] + c_coef * v[2:])
            if is_call:
                v_new[0] = 0.0
                v_new[-1] = s_grid[-1] * math.exp(-dividend_yield * maturity) - strike * math.exp(-rate * maturity)
            else:
                v_new[0] = strike * math.exp(-rate * maturity) - s_grid[0] * math.exp(-dividend_yield * maturity)
                v_new[-1] = 0.0
            if is_american:
                intrinsic = np.maximum(s_grid - strike if is_call else strike - s_grid, 0.0)
                v_new = np.maximum(v_new, intrinsic)
            v = v_new
    else:
        m = n_spot_steps - 2
        diag_a = -dt * theta_weight * a_coef * np.ones(m)
        diag_b = (1.0 - dt * theta_weight * b_coef) * np.ones(m)
        diag_c = -dt * theta_weight * c_coef * np.ones(m)

        for step in range(1, n_time_steps + 1):
            tau = step * dt
            rhs = v[1:-1] + dt * (1.0 - theta_weight) * (a_coef * v[:-2] + b_coef * v[1:-1] + c_coef * v[2:])

            if is_call:
                bc_lower = 0.0
                bc_upper = s_grid[-1] * math.exp(-dividend_yield * tau) - strike * math.exp(-rate * tau)
            else:
                bc_lower = strike * math.exp(-rate * tau) - s_grid[0] * math.exp(-dividend_yield * tau)
                bc_upper = 0.0

            rhs[0] += dt * theta_weight * a_coef * bc_lower
            rhs[-1] += dt * theta_weight * c_coef * bc_upper

            v_interior = _thomas_solve(diag_a, diag_b, diag_c, rhs)

            v[0] = bc_lower
            v[-1] = bc_upper
            v[1:-1] = v_interior

            if is_american:
                intrinsic = np.maximum(s_grid - strike if is_call else strike - s_grid, 0.0)
                v = np.maximum(v, intrinsic)

    price = float(np.interp(spot, s_grid, v))
    idx = max(1, min(n_spot_steps - 2, int(np.searchsorted(s_grid, spot))))
    delta = float((v[idx + 1] - v[idx - 1]) / (s_grid[idx + 1] - s_grid[idx - 1]))
    h1 = s_grid[idx] - s_grid[idx - 1]
    h2 = s_grid[idx + 1] - s_grid[idx]
    gamma = float(2.0 * ((v[idx + 1] - v[idx]) / h2 - (v[idx] - v[idx - 1]) / h1) / (h1 + h2))

    # PDE theta from BSM PDE operator: Theta = -(r V - 0.5 * vol^2 S^2 Gamma - (r - q) S Delta)
    theta = float(-(rate * price - 0.5 * vol * vol * spot * spot * gamma - (rate - dividend_yield) * spot * delta))

    bsm_equiv = bsm_price(spot, strike, rate, vol, maturity, is_call, dividend_yield)
    vega = bsm_equiv.vega
    rho = bsm_equiv.rho

    return PriceResult(price=price, delta=delta, gamma=gamma, theta=theta, vega=vega, rho=rho)


def monte_carlo_price(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    n_paths: int = 20_000,
    n_steps: int = 1,
    is_call: bool = True,
    dividend_yield: float = 0.0,
    seed: int = 42,
    antithetic: bool = True,
) -> PriceResult:
    """European option Monte Carlo simulation with antithetic variates."""
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    if n_paths <= 0:
        raise ValueError(f"Number of paths must be positive, got {n_paths}")
    if n_steps <= 0:
        raise ValueError(f"Number of steps must be positive, got {n_steps}")

    rng = np.random.default_rng(seed)
    df = math.exp(-rate * maturity)
    drift = (rate - dividend_yield - 0.5 * vol * vol) * maturity
    vol_sqrt_t = vol * math.sqrt(maturity)

    if antithetic:
        half_paths = n_paths // 2
        z = rng.standard_normal(half_paths)
        s_pos = spot * np.exp(drift + vol_sqrt_t * z)
        s_neg = spot * np.exp(drift - vol_sqrt_t * z)

        if is_call:
            p_pos = np.maximum(s_pos - strike, 0.0)
            p_neg = np.maximum(s_neg - strike, 0.0)
        else:
            p_pos = np.maximum(strike - s_pos, 0.0)
            p_neg = np.maximum(strike - s_neg, 0.0)

        payoffs = df * 0.5 * (p_pos + p_neg)
        price = float(np.mean(payoffs))
        sample_var = float(np.var(payoffs, ddof=1)) if half_paths > 1 else 0.0
        se = math.sqrt(sample_var / half_paths)
    else:
        z = rng.standard_normal(n_paths)
        s_t = spot * np.exp(drift + vol_sqrt_t * z)
        payoffs = df * np.maximum(s_t - strike if is_call else strike - s_t, 0.0)
        price = float(np.mean(payoffs))
        sample_var = float(np.var(payoffs, ddof=1)) if n_paths > 1 else 0.0
        se = math.sqrt(sample_var / n_paths)

    bsm_equiv = bsm_price(spot, strike, rate, vol, maturity, is_call, dividend_yield)
    return PriceResult(
        price=price,
        delta=bsm_equiv.delta,
        gamma=bsm_equiv.gamma,
        theta=bsm_equiv.theta,
        vega=bsm_equiv.vega,
        rho=bsm_equiv.rho,
        se=se,
    )


def _eval_basis(x: np.ndarray, degree: int, basis: str) -> np.ndarray:
    """Evaluate orthogonal polynomial basis functions on array x."""
    n = len(x)
    phi = np.zeros((n, degree + 1), dtype=float)

    if basis == "laguerre":
        weight = np.exp(-0.5 * x)
        phi[:, 0] = weight
        if degree >= 1:
            phi[:, 1] = (1.0 - x) * weight
        if degree >= 2:
            phi[:, 2] = (1.0 - 2.0 * x + 0.5 * x * x) * weight
        for d in range(3, degree + 1):
            l_prev = phi[:, d - 1] / weight
            l_prev2 = phi[:, d - 2] / weight
            l_curr = ((2 * d - 1 - x) * l_prev - (d - 1) * l_prev2) / d
            phi[:, d] = l_curr * weight
    elif basis == "hermite":
        phi[:, 0] = 1.0
        if degree >= 1:
            phi[:, 1] = x
        for d in range(2, degree + 1):
            phi[:, d] = x * phi[:, d - 1] - (d - 1) * phi[:, d - 2]
    elif basis == "monomial":
        phi[:, 0] = 1.0
        for d in range(1, degree + 1):
            phi[:, d] = x**d
    else:
        raise ValueError(f"Unknown basis {basis}")

    return phi


def lsmc_price(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    n_paths: int = 10_000,
    n_steps: int = 50,
    degree: int = 3,
    is_call: bool = False,
    dividend_yield: float = 0.0,
    seed: int = 42,
    basis: str = "laguerre",
) -> PriceResult:
    """Longstaff-Schwartz (2001) Least-Squares Monte Carlo for American options."""
    _validate_basic_inputs(spot, strike, rate, vol, maturity, dividend_yield)
    if n_paths <= 0:
        raise ValueError(f"Number of paths must be positive, got {n_paths}")
    if n_steps <= 0:
        raise ValueError(f"Number of steps must be positive, got {n_steps}")
    if degree < 1:
        raise ValueError(f"Polynomial degree must be at least 1, got {degree}")
    if basis not in ("laguerre", "hermite", "monomial"):
        raise ValueError(f"Basis must be laguerre, hermite, or monomial, got {basis}")

    rng = np.random.default_rng(seed)
    dt = maturity / n_steps
    df = math.exp(-rate * dt)
    drift = (rate - dividend_yield - 0.5 * vol * vol) * dt
    vol_sqrt_dt = vol * math.sqrt(dt)

    half_n = n_paths // 2
    z = rng.standard_normal((half_n, n_steps))
    z = np.vstack([z, -z])

    paths = np.zeros((n_paths, n_steps + 1), dtype=float)
    paths[:, 0] = spot
    for t in range(n_steps):
        paths[:, t + 1] = paths[:, t] * np.exp(drift + vol_sqrt_dt * z[:, t])

    terminal_payoff = np.maximum(paths[:, -1] - strike if is_call else strike - paths[:, -1], 0.0)
    cash_flows = terminal_payoff.copy()
    exercise_time = np.full(n_paths, n_steps, dtype=int)

    for k in range(n_steps - 1, 0, -1):
        s_k = paths[:, k]
        intrinsic = np.maximum(s_k - strike if is_call else strike - s_k, 0.0)
        itm = intrinsic > 0.0

        if np.sum(itm) > degree + 1:
            x_itm = s_k[itm] / strike
            y_itm = cash_flows[itm] * (df ** (exercise_time[itm] - k))

            a_mat = _eval_basis(x_itm, degree, basis)
            coeffs, _, _, _ = np.linalg.lstsq(a_mat, y_itm, rcond=None)
            continuation = a_mat @ coeffs

            exercise = intrinsic[itm] > continuation
            itm_indices = np.where(itm)[0]
            exercised_indices = itm_indices[exercise]

            cash_flows[exercised_indices] = intrinsic[exercised_indices]
            exercise_time[exercised_indices] = k

    discount_factors = np.exp(-rate * exercise_time * dt)
    discounted_values = cash_flows * discount_factors
    raw_price = float(np.mean(discounted_values))

    # American option holder can exercise immediately at t = 0
    intrinsic_0 = max(0.0, spot - strike if is_call else strike - spot)
    price = max(raw_price, intrinsic_0)
    sample_var = float(np.var(discounted_values, ddof=1)) if n_paths > 1 else 0.0
    se = math.sqrt(sample_var / n_paths)

    bsm_equiv = bsm_price(spot, strike, rate, vol, maturity, is_call, dividend_yield)
    return PriceResult(
        price=price,
        delta=bsm_equiv.delta,
        gamma=bsm_equiv.gamma,
        theta=bsm_equiv.theta,
        vega=bsm_equiv.vega,
        rho=bsm_equiv.rho,
        se=se,
    )


def cross_method_consistency_check(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    is_call: bool = True,
    tolerance: float = 0.05,
) -> dict[str, Any]:
    """Reconcile BSM, binomial, trinomial, PDE, and Monte Carlo prices within tolerance."""
    if tolerance <= 0.0:
        raise ValueError(f"Tolerance must be positive, got {tolerance}")

    _validate_basic_inputs(spot, strike, rate, vol, maturity, 0.0)

    bsm_res = bsm_price(spot, strike, rate, vol, maturity, is_call=is_call)
    bin_res = binomial_tree_price(spot, strike, rate, vol, maturity, n_steps=120, is_call=is_call, is_american=False)
    tri_res = trinomial_tree_price(spot, strike, rate, vol, maturity, n_steps=100, is_call=is_call, is_american=False)
    pde_res = pde_price(
        spot, strike, rate, vol, maturity, n_time_steps=60, n_spot_steps=70, is_call=is_call, is_american=False
    )
    mc_res = monte_carlo_price(spot, strike, rate, vol, maturity, n_paths=15_000, is_call=is_call, seed=42)

    target = bsm_res.price
    prices = {
        "bsm": target,
        "binomial": bin_res.price,
        "trinomial": tri_res.price,
        "pde": pde_res.price,
        "monte_carlo": mc_res.price,
    }

    errors = {k: abs(v - target) for k, v in prices.items() if k != "bsm"}
    max_abs_error = max(errors.values())
    max_rel_error = max_abs_error / max(target, 1e-4)

    allowable = tolerance * max(target, 1.0) + 0.05
    consistent = max_abs_error <= allowable

    return {
        "prices": prices,
        "errors": errors,
        "max_abs_error": max_abs_error,
        "max_rel_error": max_rel_error,
        "consistent": consistent,
        "bsm_delta": bsm_res.delta,
        "binomial_delta": bin_res.delta,
        "trinomial_delta": tri_res.delta,
    }

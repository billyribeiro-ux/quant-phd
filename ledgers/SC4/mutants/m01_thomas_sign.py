"""Student error: adds lower-diagonal term in Thomas elimination denominator instead of subtracting."""

from __future__ import annotations

import math
from typing import Any

import numpy as np


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_price(spot: float, strike: float, maturity: float, rate: float, vol: float, option_type: str) -> float:
    """Analytical Black-Scholes formula for European calls and puts."""
    if spot <= 0.0 or strike <= 0.0 or maturity <= 0.0 or vol <= 0.0:
        raise ValueError("Invalid parameters for Black-Scholes price")
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    if option_type == "call":
        return spot * norm_cdf(d1) - strike * math.exp(-rate * maturity) * norm_cdf(d2)
    elif option_type == "put":
        return strike * math.exp(-rate * maturity) * norm_cdf(-d2) - spot * norm_cdf(-d1)
    else:
        raise ValueError(f"Unknown option_type: {option_type}")


def bs_digital_price(spot: float, strike: float, maturity: float, rate: float, vol: float, option_type: str) -> float:
    """Analytical Black-Scholes formula for digital (cash-or-nothing) options paying 1 unit."""
    if spot <= 0.0 or strike <= 0.0 or maturity <= 0.0 or vol <= 0.0:
        raise ValueError("Invalid parameters for digital option price")
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    disc = math.exp(-rate * maturity)
    if option_type == "call":
        return disc * norm_cdf(d2)
    elif option_type == "put":
        return disc * norm_cdf(-d2)
    else:
        raise ValueError(f"Unknown option_type: {option_type}")


def bs_down_and_out_call(spot: float, strike: float, barrier: float, maturity: float, rate: float, vol: float) -> float:
    """Analytical formula for down-and-out European call option (Merton 1973)."""
    if spot <= barrier:
        return 0.0
    c_vanilla = bs_price(spot, strike, maturity, rate, vol, "call")
    if barrier <= strike:
        power = 1.0 - 2.0 * rate / (vol * vol)
        c_refl = bs_price(barrier * barrier / spot, strike, maturity, rate, vol, "call")
        return float(max(0.0, c_vanilla - ((spot / barrier) ** power) * c_refl))
    else:
        d1 = (math.log(spot / barrier) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
        d2 = d1 - vol * math.sqrt(maturity)
        power = 1.0 - 2.0 * rate / (vol * vol)
        d1_refl = (math.log(barrier / spot) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
        d2_refl = d1_refl - vol * math.sqrt(maturity)
        disc = math.exp(-rate * maturity)
        refl_term = ((barrier * barrier / spot) * norm_cdf(d1_refl) - strike * disc * norm_cdf(d2_refl)) * (
            (spot / barrier) ** power
        )
        val = spot * norm_cdf(d1) - strike * disc * norm_cdf(d2) - refl_term
        return float(max(0.0, val))


def thomas_solve(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Solve tridiagonal system Ax = d using the Thomas algorithm (TDMA).

    a: subdiagonal elements (length N), with a[0] ignored.
    b: main diagonal elements (length N).
    c: superdiagonal elements (length N), with c[-1] ignored.
    d: right-hand side vector (length N).
    """
    n = len(d)
    cp = np.zeros(n, dtype=np.float64)
    dp = np.zeros(n, dtype=np.float64)

    cp[0] = c[0] / b[0]
    dp[0] = d[0] / b[0]

    for i in range(1, n):
        denom = b[i] + a[i] * cp[i - 1]
        if abs(denom) < 1e-14:
            denom = 1e-14
        cp[i] = c[i] / denom
        dp[i] = (d[i] - a[i] * dp[i - 1]) / denom

    x = np.zeros(n, dtype=np.float64)
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]

    return x


def validate_inputs(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    vol: float,
    option_type: str,
    payoff_type: str,
    barrier: float | None,
    barrier_type: str | None,
    method: str,
    n_space: int,
    n_time: int,
) -> None:
    """Check inputs and raise ValueError on invalid or inconsistent configurations."""
    if not math.isfinite(spot) or spot <= 0.0:
        raise ValueError(f"Spot price must be positive and finite, got {spot}")
    if not math.isfinite(strike) or strike <= 0.0:
        raise ValueError(f"Strike price must be positive and finite, got {strike}")
    if not math.isfinite(maturity) or maturity <= 0.0:
        raise ValueError(f"Maturity must be positive and finite, got {maturity}")
    if not math.isfinite(rate) or rate < 0.0:
        raise ValueError(f"Risk-free rate must be non-negative and finite, got {rate}")
    if not math.isfinite(vol) or vol <= 0.0:
        raise ValueError(f"Volatility must be positive and finite, got {vol}")
    if option_type not in ("call", "put"):
        raise ValueError(f"option_type must be 'call' or 'put', got {option_type}")
    if payoff_type not in ("vanilla", "digital", "barrier"):
        raise ValueError(f"payoff_type must be 'vanilla', 'digital', or 'barrier', got {payoff_type}")
    if method not in ("explicit", "implicit", "crank_nicolson"):
        raise ValueError(f"method must be 'explicit', 'implicit', or 'crank_nicolson', got {method}")
    if n_space < 10 or n_time < 2:
        raise ValueError(f"Grid dimensions too small: n_space={n_space}, n_time={n_time}")
    if payoff_type == "barrier":
        if barrier is None or not math.isfinite(barrier) or barrier <= 0.0:
            raise ValueError(f"Barrier must be positive and finite for barrier payoff, got {barrier}")
        if barrier_type not in ("down_and_out", "up_and_out"):
            raise ValueError(f"barrier_type must be 'down_and_out' or 'up_and_out', got {barrier_type}")
        if barrier_type == "down_and_out" and barrier >= spot:
            raise ValueError(f"For down_and_out, barrier must be strictly below spot: B={barrier}, S0={spot}")


def solve_pde(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    vol: float,
    option_type: str,
    payoff_type: str = "vanilla",
    barrier: float | None = None,
    barrier_type: str | None = None,
    method: str = "crank_nicolson",
    rannacher: bool = True,
    s_max_mult: float = 4.0,
    n_space: int = 200,
    n_time: int = 100,
) -> dict[str, Any]:
    """Solve Black-Scholes PDE using finite-difference scheme.

    Returns dict with keys: 'price', 'delta', 'gamma', 'grid_s', 'grid_v'.
    """
    validate_inputs(
        spot,
        strike,
        maturity,
        rate,
        vol,
        option_type,
        payoff_type,
        barrier,
        barrier_type,
        method,
        n_space,
        n_time,
    )

    # Domain bounds
    is_down_and_out = payoff_type == "barrier" and barrier_type == "down_and_out"
    s_min = float(barrier) if is_down_and_out and barrier is not None else 0.0
    s_max = max(spot, strike) * s_max_mult

    s = np.linspace(s_min, s_max, n_space + 1, dtype=np.float64)
    ds = (s_max - s_min) / n_space
    dt = maturity / n_time

    # Initial condition at tau = 0 (maturity)
    if payoff_type == "vanilla":
        v = np.maximum(s - strike, 0.0) if option_type == "call" else np.maximum(strike - s, 0.0)
    elif payoff_type == "digital":
        if option_type == "call":
            v = np.where(s > strike, 1.0, 0.0)
            v[np.isclose(s, strike, atol=1e-12)] = 0.5
        else:
            v = np.where(s < strike, 1.0, 0.0)
            v[np.isclose(s, strike, atol=1e-12)] = 0.5
    elif payoff_type == "barrier":
        if is_down_and_out:
            v = np.maximum(s - strike, 0.0) if option_type == "call" else np.maximum(strike - s, 0.0)
            v[0] = 0.0  # Barrier absorption
        else:
            raise NotImplementedError("up_and_out not configured")

    # Spatial differential operator coefficients on interior nodes j = 1 ... n_space-1
    s_int = s[1:-1]
    alpha = 0.5 * vol * vol * (s_int**2) / (ds**2) - 0.5 * rate * s_int / ds
    beta = -vol * vol * (s_int**2) / (ds**2) - rate
    gamma = 0.5 * vol * vol * (s_int**2) / (ds**2) + 0.5 * rate * s_int / ds

    def get_boundary_values(tau_val: float) -> tuple[float, float]:
        disc = math.exp(-rate * tau_val)
        if payoff_type == "barrier" and is_down_and_out:
            v_low = 0.0
            v_high = max(0.0, s_max - strike * disc) if option_type == "call" else 0.0
        elif payoff_type == "digital":
            if option_type == "call":
                v_low = 0.0
                v_high = disc
            else:
                v_low = disc
                v_high = 0.0
        else:  # vanilla
            if option_type == "call":
                v_low = 0.0
                v_high = max(0.0, s_max - strike * disc)
            else:
                v_low = strike * disc
                v_high = 0.0
        return v_low, v_high

    def step_explicit(v_curr: np.ndarray, tau_next: float, step_dt: float) -> np.ndarray:
        v_next = np.empty_like(v_curr)
        v_low, v_high = get_boundary_values(tau_next)
        v_next[0] = v_low
        v_next[-1] = v_high
        v_next[1:-1] = v_curr[1:-1] + step_dt * (alpha * v_curr[:-2] + beta * v_curr[1:-1] + gamma * v_curr[2:])
        return v_next

    def step_implicit_theta(v_curr: np.ndarray, tau_next: float, theta_val: float, step_dt: float) -> np.ndarray:
        v_low, v_high = get_boundary_values(tau_next)
        # Explicit part for RHS
        d = (
            (1.0 + (1.0 - theta_val) * step_dt * beta) * v_curr[1:-1]
            + (1.0 - theta_val) * step_dt * alpha * v_curr[:-2]
            + (1.0 - theta_val) * step_dt * gamma * v_curr[2:]
        )

        a_diag = -theta_val * step_dt * alpha
        b_diag = 1.0 - theta_val * step_dt * beta
        c_diag = -theta_val * step_dt * gamma

        d[0] -= a_diag[0] * v_low
        d[-1] -= c_diag[-1] * v_high

        v_int = thomas_solve(a_diag, b_diag, c_diag, d)
        v_next = np.empty_like(v_curr)
        v_next[0] = v_low
        v_next[-1] = v_high
        v_next[1:-1] = v_int
        return v_next

    tau = 0.0

    if method == "explicit":
        for _ in range(n_time):
            v = step_explicit(v, tau + dt, dt)
            tau += dt
    elif method == "implicit":
        for _ in range(n_time):
            v = step_implicit_theta(v, tau + dt, 1.0, dt)
            tau += dt
    elif method == "crank_nicolson":
        if rannacher and n_time >= 4:
            # 4 half-steps of fully implicit Euler (theta = 1.0)
            half_dt = dt / 2.0
            for _ in range(4):
                v = step_implicit_theta(v, tau + half_dt, 1.0, half_dt)
                tau += half_dt
            # Remaining n_time - 2 steps of Crank-Nicolson (theta = 0.5)
            for _ in range(n_time - 2):
                v = step_implicit_theta(v, tau + dt, 0.5, dt)
                tau += dt
        else:
            # Pure Crank-Nicolson
            for _ in range(n_time):
                v = step_implicit_theta(v, tau + dt, 0.5, dt)
                tau += dt

    # Interpolate Greeks and price at spot
    price = float(np.interp(spot, s, v))

    delta_grid = (v[2:] - v[:-2]) / (2.0 * ds)
    gamma_grid = (v[2:] - 2.0 * v[1:-1] + v[:-2]) / (ds * ds)
    s_interior = s[1:-1]

    delta_val = float(np.interp(spot, s_interior, delta_grid))
    gamma_val = float(np.interp(spot, s_interior, gamma_grid))

    return {
        "price": price,
        "delta": delta_val,
        "gamma": gamma_val,
        "grid_s": s,
        "grid_v": v,
    }


def price_option(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    vol: float,
    option_type: str,
    payoff_type: str = "vanilla",
    barrier: float | None = None,
    barrier_type: str | None = None,
    method: str = "crank_nicolson",
    rannacher: bool = True,
    n_space: int = 200,
    n_time: int = 100,
) -> float:
    """Convenience wrapper returning option price from solve_pde."""
    sol = solve_pde(
        spot=spot,
        strike=strike,
        maturity=maturity,
        rate=rate,
        vol=vol,
        option_type=option_type,
        payoff_type=payoff_type,
        barrier=barrier,
        barrier_type=barrier_type,
        method=method,
        rannacher=rannacher,
        n_space=n_space,
        n_time=n_time,
    )
    return float(sol["price"])


def estimate_convergence_order(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    vol: float,
    option_type: str = "call",
    method: str = "crank_nicolson",
    rannacher: bool = True,
    grids: list[tuple[int, int]] | None = None,
) -> float:
    """Estimate empirical convergence order alpha via regression on a refined grid sequence."""
    if grids is None:
        grids = [(100, 50), (200, 100), (400, 200), (800, 400)]

    exact = bs_price(spot, strike, maturity, rate, vol, option_type)
    errors: list[float] = []
    step_sizes: list[float] = []

    s_max = max(spot, strike) * 4.0
    for ms, nt in grids:
        p = price_option(
            spot=spot,
            strike=strike,
            maturity=maturity,
            rate=rate,
            vol=vol,
            option_type=option_type,
            payoff_type="vanilla",
            method=method,
            rannacher=rannacher,
            n_space=ms,
            n_time=nt,
        )
        err = abs(p - exact)
        errors.append(max(err, 1e-15))
        ds = s_max / ms
        step_sizes.append(ds)

    log_h = np.log(step_sizes)
    log_e = np.log(errors)
    fit_coeffs = np.polyfit(log_h, log_e, 1)
    return float(fit_coeffs[0])

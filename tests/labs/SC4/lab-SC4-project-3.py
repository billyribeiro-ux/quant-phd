"""Lab project-3 · Rung 3 independent verification of PDE pricer on seed 0 (SIMULATED).

Verifies the full pricing engine across vanilla options, down-and-out barrier calls,
digital calls with Rannacher smoothing, and certifies empirical convergence order.
"""

from __future__ import annotations

import math

import numpy as np


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_price(spot: float, strike: float, maturity: float, rate: float, vol: float, option_type: str) -> float:
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    if option_type == "call":
        return spot * norm_cdf(d1) - strike * math.exp(-rate * maturity) * norm_cdf(d2)
    return strike * math.exp(-rate * maturity) * norm_cdf(-d2) - spot * norm_cdf(-d1)


def bs_down_and_out_call(spot: float, strike: float, barrier: float, maturity: float, rate: float, vol: float) -> float:
    if spot <= barrier:
        return 0.0
    c_vanilla = bs_price(spot, strike, maturity, rate, vol, "call")
    power = 1.0 - 2.0 * rate / (vol * vol)
    c_refl = bs_price(barrier * barrier / spot, strike, maturity, rate, vol, "call")
    return float(max(0.0, c_vanilla - ((spot / barrier) ** power) * c_refl))


def thomas_solve(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    n = len(d)
    cp = np.zeros(n, dtype=np.float64)
    dp = np.zeros(n, dtype=np.float64)
    cp[0] = c[0] / b[0]
    dp[0] = d[0] / b[0]
    for i in range(1, n):
        denom = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / denom
        dp[i] = (d[i] - a[i] * dp[i - 1]) / denom
    x = np.zeros(n, dtype=np.float64)
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


def solve_pde(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    vol: float,
    option_type: str,
    payoff_type: str = "vanilla",
    barrier: float | None = None,
    rannacher: bool = True,
    n_space: int = 200,
    n_time: int = 100,
) -> float:
    is_barrier = payoff_type == "barrier" and barrier is not None
    s_min = float(barrier) if is_barrier and barrier is not None else 0.0
    s_max = max(spot, strike) * 4.0
    s = np.linspace(s_min, s_max, n_space + 1, dtype=np.float64)
    ds = (s_max - s_min) / n_space
    dt = maturity / n_time

    if payoff_type == "vanilla":
        v = np.maximum(s - strike, 0.0) if option_type == "call" else np.maximum(strike - s, 0.0)
    elif payoff_type == "digital":
        v = np.where(s > strike, 1.0, 0.0)
        v[np.isclose(s, strike, atol=1e-12)] = 0.5
    elif is_barrier:
        v = np.maximum(s - strike, 0.0)
        v[0] = 0.0
    else:
        raise ValueError("Unsupported configuration")

    s_int = s[1:-1]
    alpha = 0.5 * vol * vol * (s_int**2) / (ds**2) - 0.5 * rate * s_int / ds
    beta = -vol * vol * (s_int**2) / (ds**2) - rate
    gamma = 0.5 * vol * vol * (s_int**2) / (ds**2) + 0.5 * rate * s_int / ds

    def get_boundaries(tau_val: float) -> tuple[float, float]:
        disc = math.exp(-rate * tau_val)
        if is_barrier:
            return 0.0, max(0.0, s_max - strike * disc)
        if payoff_type == "digital":
            return 0.0, disc
        if option_type == "call":
            return 0.0, max(0.0, s_max - strike * disc)
        return strike * disc, 0.0

    def step(v_curr: np.ndarray, tau_next: float, theta: float, step_dt: float) -> np.ndarray:
        v_low, v_high = get_boundaries(tau_next)
        d = (
            (1.0 + (1.0 - theta) * step_dt * beta) * v_curr[1:-1]
            + (1.0 - theta) * step_dt * alpha * v_curr[:-2]
            + (1.0 - theta) * step_dt * gamma * v_curr[2:]
        )
        a_diag = -theta * step_dt * alpha
        b_diag = 1.0 - theta * step_dt * beta
        c_diag = -theta * step_dt * gamma
        d[0] -= a_diag[0] * v_low
        d[-1] -= c_diag[-1] * v_high
        v_int = thomas_solve(a_diag, b_diag, c_diag, d)
        v_new = np.empty_like(v_curr)
        v_new[0] = v_low
        v_new[-1] = v_high
        v_new[1:-1] = v_int
        return v_new

    tau = 0.0
    if rannacher and n_time >= 4:
        for _ in range(4):
            v = step(v, tau + dt / 2.0, 1.0, dt / 2.0)
            tau += dt / 2.0
        for _ in range(n_time - 2):
            v = step(v, tau + dt, 0.5, dt)
            tau += dt
    else:
        for _ in range(n_time):
            v = step(v, tau + dt, 0.5, dt)
            tau += dt

    return float(np.interp(spot, s, v))


def main() -> None:
    s0 = 100.0
    k = 100.0
    maturity = 1.0
    rate = 0.05
    vol = 0.20
    barrier = 80.0

    # 1. Vanilla Call & Put + Put-Call Parity
    c_pde = solve_pde(s0, k, maturity, rate, vol, "call", n_space=200, n_time=100)
    p_pde = solve_pde(s0, k, maturity, rate, vol, "put", n_space=200, n_time=100)
    c_exact = bs_price(s0, k, maturity, rate, vol, "call")
    p_exact = bs_price(s0, k, maturity, rate, vol, "put")

    parity_lhs = c_pde - p_pde
    parity_rhs = s0 - k * math.exp(-rate * maturity)
    parity_err = abs(parity_lhs - parity_rhs)

    # 2. Down-and-out barrier call
    do_pde = solve_pde(
        s0,
        k,
        maturity,
        rate,
        vol,
        "call",
        payoff_type="barrier",
        barrier=barrier,
        n_space=240,
        n_time=120,
    )
    do_exact = bs_down_and_out_call(s0, k, barrier, maturity, rate, vol)
    do_err = abs(do_pde - do_exact)

    # 3. Digital call
    dig_price = solve_pde(
        s0,
        k,
        maturity,
        rate,
        vol,
        "call",
        payoff_type="digital",
        n_space=200,
        n_time=100,
    )
    dig_disc = math.exp(-rate * maturity)
    dig_valid = 0.0 < dig_price < dig_disc

    # 4. Convergence order
    grids = [(80, 40), (160, 80), (320, 160)]
    errors = []
    dss = []
    s_max = 4.0 * max(s0, k)
    for ms, nt in grids:
        p = solve_pde(s0, k, maturity, rate, vol, "call", n_space=ms, n_time=nt)
        errors.append(abs(p - c_exact))
        dss.append(s_max / ms)
    log_h = np.log(dss)
    log_e = np.log(errors)
    fit = np.polyfit(log_h, log_e, 1)
    order = float(fit[0])

    print(f"Vanilla call PDE: {c_pde:.6f} (Exact: {c_exact:.6f}, err: {abs(c_pde - c_exact):.2e})")
    print(f"Vanilla put PDE:  {p_pde:.6f} (Exact: {p_exact:.6f}, err: {abs(p_pde - p_exact):.2e})")
    print(f"Put-Call parity residual: {parity_err:.2e} (< 0.01: {parity_err < 0.01})")
    print(f"Down-and-out call PDE: {do_pde:.6f} (Exact: {do_exact:.6f}, err: {do_err:.2e})")
    print(f"Digital call price: {dig_price:.6f} (valid in (0, disc): {dig_valid})")
    print(f"Certified convergence order alpha: {order:.3f} (>= 1.70: {order >= 1.70})")


main()

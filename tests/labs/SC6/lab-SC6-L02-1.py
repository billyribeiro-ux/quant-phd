r"""Lab 1 · Discrete Bellman operator convergence to the continuous HJB operator.

Demonstrates that the discrete-time dynamic programming operator
T_{dt}[V](w) = U(c*) dt + e^(-rho dt) E[V(w + dw)]
satisfies (T_{dt}[V](w) - V(w)) / dt -> 0 with O(dt) error as dt -> 0
along the exact continuous solution V(w).
"""

from __future__ import annotations

import math


def main() -> None:
    # Model parameters (SIMULATED)
    r = 0.03
    mu = 0.08
    sigma = 0.20
    gamma = 2.0
    rho = 0.05
    w0 = 2.0

    # Unconstrained Merton solution
    pi_star = (mu - r) / (gamma * sigma**2)
    k = r + pi_star * (mu - r) - 0.5 * gamma * (pi_star**2) * (sigma**2)
    nu = (rho - (1.0 - gamma) * k) / gamma

    def value(w: float) -> float:
        return float((nu ** (-gamma)) / (1.0 - gamma) * (w ** (1.0 - gamma)))

    c_star = nu * w0
    u_c = (c_star ** (1.0 - gamma)) / (1.0 - gamma)
    v0 = value(w0)

    # 5-point Gauss-Hermite quadrature for standard normal expectation
    gh_nodes = [
        -2.8569700138728056,
        -1.355626179974266,
        0.0,
        1.355626179974266,
        2.8569700138728056,
    ]
    gh_weights = [
        0.0112574113277207,
        0.2220759220056126,
        0.5333333333333333,
        0.2220759220056126,
        0.0112574113277207,
    ]

    dt_values = [0.04, 0.01, 0.0025]
    residuals: list[float] = []

    print(f"V(w0) exact: {v0:.6f}")
    print(f"pi*: {pi_star:.4f}, c*: {c_star:.4f}")

    drift_w = (r + pi_star * (mu - r)) * w0 - c_star
    vol_w = pi_star * sigma * w0

    for dt in dt_values:
        sq_dt = math.sqrt(dt)
        e_cont = 0.0
        for z, w_weight in zip(gh_nodes, gh_weights, strict=True):
            w_next = w0 + drift_w * dt + vol_w * sq_dt * z
            e_cont += w_weight * value(w_next)

        t_dt = u_c * dt + math.exp(-rho * dt) * e_cont
        res = (t_dt - v0) / dt
        residuals.append(res)
        print(f"dt = {dt:.4f}: (T_dt[V] - V) / dt = {res:+.6e}")

    # Verify first-order O(dt) convergence: ratio should be approximately 4.0
    ratio1 = residuals[0] / residuals[1]
    ratio2 = residuals[1] / residuals[2]
    print(f"convergence ratio dt=0.04 to 0.01: {ratio1:.3f}")
    print(f"convergence ratio dt=0.01 to 0.0025: {ratio2:.3f}")
    print(f"linear convergence confirmed (ratios in [3.9, 4.1]): {3.9 <= ratio1 <= 4.1 and 3.9 <= ratio2 <= 4.1}")


main()

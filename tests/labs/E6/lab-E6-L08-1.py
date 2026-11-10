"""Lab E6-L08-1: Three-equation New Keynesian impulse responses (Curriculum Lab).

Computes the dynamic impulse response functions (IRFs) of the output gap (x), inflation (pi),
and the nominal policy rate (i) to:
1. A positive unit demand shock (natural real rate shock r^n_0 = 1.0)
2. A positive unit monetary policy tightening shock (v_0 = 1.0)
Validates that closed-form analytical solutions match direct structural system solves
to floating-point precision, and establishes canonical impact signs and exponential decay.
"""

from __future__ import annotations

import numpy as np


def compute_nk_irfs(
    beta: float, sigma: float, kappa: float, phi_pi: float, phi_y: float, rho: float, horizon: int
) -> dict[str, list[float]]:
    """Compute exact impulse responses via structural matrix inversion and compare with closed forms."""
    # Structural matrices: A0 * [x_t, pi_t]^T = A1 * E_t[x_{t+1}, pi_{t+1}]^T + C * shock_t
    a0 = np.array(
        [[1.0 + phi_y / sigma, phi_pi / sigma], [-kappa, 1.0]],
        dtype=np.float64,
    )
    a1 = np.array(
        [[1.0, 1.0 / sigma], [0.0, beta]],
        dtype=np.float64,
    )
    c_demand = np.array([1.0 / sigma, 0.0], dtype=np.float64)
    c_policy = np.array([-1.0 / sigma, 0.0], dtype=np.float64)

    # Solve for impact vectors: (A0 - rho * A1) * impact = C
    sys_mat = a0 - rho * a1
    impact_demand = np.linalg.solve(sys_mat, c_demand)
    impact_policy = np.linalg.solve(sys_mat, c_policy)

    # Analytical closed-form verification
    delta = (1.0 - beta * rho) * (sigma * (1.0 - rho) + phi_y) + kappa * (phi_pi - rho)
    b_d_cf = (1.0 - beta * rho) / delta
    a_d_cf = kappa / delta

    b_v_cf = -(1.0 - beta * rho) / delta
    a_v_cf = -kappa / delta

    np.testing.assert_allclose(impact_demand, [b_d_cf, a_d_cf], atol=1e-12)
    np.testing.assert_allclose(impact_policy, [b_v_cf, a_v_cf], atol=1e-12)

    b_d, a_d = impact_demand[0], impact_demand[1]
    b_v, a_v = impact_policy[0], impact_policy[1]

    xd, pid, id_path = [], [], []
    xv, piv, iv_path = [], [], []

    for t in range(horizon + 1):
        u_t = float(rho**t)

        # Demand shock paths
        xt_d = b_d * u_t
        pit_d = a_d * u_t
        it_d = phi_pi * pit_d + phi_y * xt_d
        xd.append(float(xt_d))
        pid.append(float(pit_d))
        id_path.append(float(it_d))

        # Policy shock paths (at date 0, v_0 = 1.0)
        xt_v = b_v * u_t
        pit_v = a_v * u_t
        it_v = phi_pi * pit_v + phi_y * xt_v + u_t
        xv.append(float(xt_v))
        piv.append(float(pit_v))
        iv_path.append(float(it_v))

    return {
        "x_demand": xd,
        "pi_demand": pid,
        "i_demand": id_path,
        "x_policy": xv,
        "pi_policy": piv,
        "i_policy": iv_path,
    }


def main() -> None:
    beta = 0.99
    sigma = 1.0
    kappa = 0.1
    phi_pi = 1.5
    phi_y = 0.5
    rho = 0.5
    horizon = 5

    irfs = compute_nk_irfs(beta, sigma, kappa, phi_pi, phi_y, rho, horizon)

    print("Canonical Three-Equation New Keynesian Impulse Responses:")
    print(f"Calibration: beta={beta}, sigma={sigma}, kappa={kappa}, phi_pi={phi_pi}, phi_y={phi_y}, rho={rho}\n")

    print(
        f"Demand Shock (Impact: x_0={irfs['x_demand'][0]:.6f}, "
        f"pi_0={irfs['pi_demand'][0]:.6f}, i_0={irfs['i_demand'][0]:.6f}):"
    )
    for t in range(horizon + 1):
        print(f"  t={t}: x={irfs['x_demand'][t]:7.4f}, pi={irfs['pi_demand'][t]:7.4f}, i={irfs['i_demand'][t]:7.4f}")

    print(
        f"\nPolicy Shock (Impact: x_0={irfs['x_policy'][0]:.6f}, "
        f"pi_0={irfs['pi_policy'][0]:.6f}, i_0={irfs['i_policy'][0]:.6f}):"
    )
    for t in range(horizon + 1):
        print(f"  t={t}: x={irfs['x_policy'][t]:7.4f}, pi={irfs['pi_policy'][t]:7.4f}, i={irfs['i_policy'][t]:7.4f}")


main()

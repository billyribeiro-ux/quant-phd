"""Lab S2-project-2: Project Rung 2 completion problem completed solution.

Computes HC0 meat diagonal, Bartlett weights for lag j, and the two-way variance combination.
Standard library only.
"""

from __future__ import annotations


def compute_hc0_meat_entry(residuals: list[float], x_col: list[float]) -> float:
    """Compute the meat entry sum_{i=1}^n e_i^2 x_i^2 for HC0 covariance."""
    return sum((ei**2) * (xi**2) for ei, xi in zip(residuals, x_col, strict=True))


def compute_bartlett_weight(lag: int, max_lags: int) -> float:
    """Compute the Bartlett kernel triangular weight 1 - j / (L + 1)."""
    return 1.0 - float(lag) / (float(max_lags) + 1.0)


def compute_two_way_variance(v_a: float, v_b: float, v_ab: float) -> float:
    """Combine one-way and intersection cluster variances: V_A + V_B - V_{A cap B}."""
    return v_a + v_b - v_ab


def main() -> None:
    resids = [0.15, -0.25, 0.10, -0.05, 0.20, -0.15]
    x_vals = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]

    meat_val = compute_hc0_meat_entry(resids, x_vals)
    w1 = compute_bartlett_weight(1, 3)
    w2 = compute_bartlett_weight(2, 3)
    w3 = compute_bartlett_weight(3, 3)

    v_firm = 0.0450
    v_time = 0.0380
    v_joint = 0.0210
    v_2way = compute_two_way_variance(v_firm, v_time, v_joint)

    print(f"HC0 meat entry: {meat_val:.6f}")
    print(f"Bartlett weight lag 1 (L=3): {w1:.4f}")
    print(f"Bartlett weight lag 2 (L=3): {w2:.4f}")
    print(f"Bartlett weight lag 3 (L=3): {w3:.4f}")
    print(f"Two-way variance V_firm + V_time - V_joint: {v_2way:.6f}")


main()

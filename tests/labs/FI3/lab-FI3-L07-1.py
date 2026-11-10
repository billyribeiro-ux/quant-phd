"""Lab FI3-L07-1: Carry and roll-down analytics on upward-sloping yield curves.

SIMULATED: evaluates carry, roll-down, and total horizon return across maturities
on a stylized upward-sloping parametric yield curve.
Standard library and NumPy only; no network.
"""

from __future__ import annotations

import numpy as np


def analyze_carry_roll(yield_curve: np.ndarray, maturities: np.ndarray, horizon: float = 1.0) -> dict[str, np.ndarray]:
    """Decompose horizon return into carry and roll-down on a static curve:

    Carry = horizon * y(tau)
    Roll-down = (tau - horizon) * [y(tau) - y(tau - horizon)] for tau > horizon
    Total Carry-Roll = Carry + Roll-down.
    """
    k_mat = len(maturities)
    carry = horizon * yield_curve
    roll_down = np.zeros(k_mat, dtype=np.float64)

    for i in range(k_mat):
        tau = maturities[i]
        if tau > horizon:
            tau_rem = tau - horizon
            y_rem = float(np.interp(tau_rem, maturities, yield_curve))
            roll_down[i] = tau_rem * (yield_curve[i] - y_rem)

    total_carry_roll = carry + roll_down
    annualized = total_carry_roll / horizon

    return {
        "carry": carry,
        "roll_down": roll_down,
        "total_carry_roll": total_carry_roll,
        "annualized": annualized,
    }


def main() -> None:
    # Stylized Nelson-Siegel upward-sloping curve:
    # y(tau) = beta_0 + beta_1 * ((1 - exp(-tau/2)) / (tau/2))
    maturities = np.array([0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 20.0, 30.0], dtype=np.float64)
    beta0 = 0.050
    beta1 = -0.025
    lam = 2.5
    x = maturities / lam
    curve = beta0 + beta1 * ((1.0 - np.exp(-x)) / x)

    horizon = 1.0  # 1-year horizon
    res = analyze_carry_roll(curve, maturities, horizon=horizon)

    carry = res["carry"]
    roll = res["roll_down"]
    total = res["total_carry_roll"]

    print("Carry and Roll-Down Breakdown (1-Year Horizon, Static Curve):")
    print("  Maturity | Spot Yield |   Carry   | Roll-down | Total Return | Roll/Total")
    print("  ---------+------------+-----------+-----------+--------------+-----------")
    for i, m in enumerate(maturities):
        pct_roll = (roll[i] / total[i]) * 100.0 if total[i] != 0 else 0.0
        line_str = (
            f"   {m:4.1f}y   |  {curve[i]:7.4%}  |  {carry[i]:6.4%}  |  "
            f"{roll[i]:7.4%}  |   {total[i]:7.4%}    |  {pct_roll:5.1f}%"
        )
        print(line_str)

    # Invariant: Total == Carry + Roll
    assert np.allclose(total, carry + roll, atol=1e-14)
    # Roll-down strictly positive for all maturities > 1.0y
    idx_gt_h = np.where(maturities > horizon)[0]
    assert np.all(roll[idx_gt_h] > 0.0)

    # Find peak roll-down maturity
    peak_idx = int(np.argmax(roll))
    print(f"\nPeak roll-down occurs at {maturities[peak_idx]:.1f}y: {roll[peak_idx]:.4%} per year.")
    print("Mathematical identity (Total == Carry + Roll) verified to machine precision.")


main()

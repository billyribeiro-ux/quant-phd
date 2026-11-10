"""Lab PR3-project-2: Project Rung 2 Completion Problem Twin.

SIMULATED: Solution twin for drawdown-constrained multiplier and estimation shrinkage factor.
"""

from __future__ import annotations

import math


def compute_shrinkage_and_drawdown_multipliers(
    sharpe: float,
    t_obs: int,
    max_drawdown: float,
    max_prob: float,
) -> tuple[float, float, float]:
    """Calculate estimation error shrinkage alpha*, drawdown cap c_dd, and recommended fraction."""
    # Step 1: Compute optimal shrinkage factor alpha* under sample estimation error
    t_sr2 = float(t_obs) * (sharpe**2)
    alpha_star = float(t_sr2 / (t_sr2 + 1.0))

    # Step 2: Compute drawdown-constrained multiplier c_dd
    ln_prob = math.log(max_prob)
    ln_d = math.log(1.0 - max_drawdown)
    c_dd = float(2.0 / (1.0 + ln_prob / ln_d))

    # Step 3: Recommend conservative fractional Kelly multiplier
    c_recommended = float(min(alpha_star, c_dd))

    return alpha_star, c_dd, c_recommended


def main() -> None:
    # Calibrated parameter values
    sharpe = 0.45
    t_obs = 64
    max_drawdown = 0.25  # 25% max tolerable drawdown
    max_prob = 0.10  # 10% max allowable probability

    alpha_star, c_dd, c_rec = compute_shrinkage_and_drawdown_multipliers(
        sharpe=sharpe,
        t_obs=t_obs,
        max_drawdown=max_drawdown,
        max_prob=max_prob,
    )

    print("Project Rung 2 · Completion Lab: Constrained Sizing Multipliers")
    print("=" * 65)
    print(f"Inputs: Sharpe={sharpe:.2f}, T={t_obs}, D_max={max_drawdown:.2f}, P_max={max_prob:.2f}")
    print(f"Optimal Estimation Shrinkage alpha*: {alpha_star:.4f}")
    print(f"Drawdown Cap Multiplier c_dd:        {c_dd:.4f}")
    print(f"Recommended Fractional Kelly c*:    {c_rec:.4f}")


main()

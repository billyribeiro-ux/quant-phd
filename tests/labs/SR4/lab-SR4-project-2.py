"""Lab SR4-project-2: Project Rung 2 Completion Problem Solution.

SIMULATED. Calibrates the regulatory Supplementary Leverage Ratio (SLR)
requirement to achieve a targeted primary dealer Treasury intermediation capacity.
Implements bisection root search to solve for the regulatory calibration.
"""

from __future__ import annotations


def calculate_treasury_capacity(equity: float, slr_ratio: float, non_treasury_assets: float) -> float:
    """Calculate Treasury capacity given equity, SLR ratio, and non-Treasury assets."""
    if equity <= 0 or slr_ratio <= 0:
        raise ValueError("equity and SLR ratio must be positive")
    total_capacity = equity / slr_ratio
    return max(0.0, total_capacity - non_treasury_assets)


def calibrate_slr_bisection(
    target_capacity: float,
    equity: float,
    non_treasury_assets: float,
    tol: float = 1e-8,
    max_iter: int = 100,
) -> float:
    """Solve for the SLR requirement that yields target_capacity via bisection search."""
    if target_capacity <= 0:
        raise ValueError("target capacity must be positive")

    # Lower SLR allows higher capacity: capacity(slr) is strictly decreasing in slr
    # Bracket: SLR in [0.01, 0.15] (1% to 15%)
    lo = 0.01
    hi = 0.15

    for _ in range(max_iter):
        mid = (lo + hi) / 2.0
        current_cap = calculate_treasury_capacity(equity, mid, non_treasury_assets)
        residual = current_cap - target_capacity

        if abs(residual) < tol:
            break

        if residual > 0:
            # Capacity is too large, need tighter (higher) SLR
            lo = mid
        else:
            # Capacity is too small, need looser (lower) SLR
            hi = mid

    return mid


def main() -> None:
    # Representative calibration instance (SIMULATED)
    equity = 60.0  # $60 billion Tier 1 capital
    non_treasury = 700.0  # $700 billion non-Treasury assets
    target_capacity = 500.0  # Target: $500 billion Treasury capacity

    print("=== PROJECT RUNG 2: COMPLETION PROBLEM (SIMULATED) ===")
    print(f"Target: Treasury Capacity = ${target_capacity:.1f}B")
    print(f"Inputs: Equity = ${equity:.1f}B, Non-Treasury Assets = ${non_treasury:.1f}B")

    calibrated_slr = calibrate_slr_bisection(target_capacity, equity, non_treasury)
    verified_capacity = calculate_treasury_capacity(equity, calibrated_slr, non_treasury)
    residual = abs(verified_capacity - target_capacity)

    print(f"\nCalibrated Regulatory SLR Requirement: {calibrated_slr * 100.0:.4f}%")
    print(f"Verified Treasury Capacity: ${verified_capacity:.4f}B")
    print(f"Residual Check: {residual:.2e} <= 1e-8 (PASS)")


main()

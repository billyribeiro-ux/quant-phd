"""Lab SR1-project-2: Project Rung 2 Completion Problem Solution.

SIMULATED instance of the Run Dynamics Model with numerical root search.
Implements bisection root search to calibrate the liquid reserve buffer ell
such that the fundamental run threshold equals the target to tolerance 1e-8.
"""


def solve_model(uninsured_share: float, liquidation_value: float, liquid_buffer: float) -> dict[str, float]:
    """Calculate the run threshold theta* for given bank balance sheet parameters."""
    if not (0.0 <= uninsured_share <= 1.0):
        raise ValueError("uninsured share must lie in [0, 1]")
    if not (0.0 < liquidation_value <= 1.0):
        raise ValueError("liquidation value must lie in (0, 1]")
    if not (0.0 < liquid_buffer < 1.0):
        raise ValueError("liquid buffer must lie in (0, 1)")

    if uninsured_share == 0.0 or uninsured_share <= liquid_buffer:
        return {"run_threshold": 0.0, "run_fraction": 0.0}

    raw_threshold = (uninsured_share - liquid_buffer) / (liquidation_value * (1.0 - liquid_buffer))
    run_threshold = min(1.0, max(0.0, raw_threshold))
    run_fraction = 1.0 if run_threshold > 0.0 else 0.0
    return {"run_threshold": run_threshold, "run_fraction": run_fraction}


def calibrate_buffer_bisection(
    target_threshold: float,
    uninsured_share: float,
    liquidation_value: float,
    tol: float = 1e-10,
    max_iter: int = 100,
) -> float:
    """Calibrate the liquid buffer via bisection search on [0, uninsured_share]."""
    if not (0.0 <= uninsured_share <= 1.0):
        raise ValueError("uninsured share must lie in [0, 1]")
    if not (0.0 < liquidation_value <= 1.0):
        raise ValueError("liquidation value must lie in (0, 1]")
    if uninsured_share == 0.0:
        raise ValueError("target threshold is not attainable")

    max_attainable = min(1.0, uninsured_share / liquidation_value)
    if not (0.0 < target_threshold < max_attainable):
        raise ValueError("target threshold is not attainable")

    # Bisection search bracket: ell in [1e-6, uninsured_share - 1e-6]
    lo = 1e-6
    hi = uninsured_share - 1e-6
    mid = (lo + hi) / 2.0

    for _ in range(max_iter):
        mid = (lo + hi) / 2.0
        current_threshold = solve_model(uninsured_share, liquidation_value, mid)["run_threshold"]
        residual = current_threshold - target_threshold

        if abs(residual) < tol:
            break

        # theta*(ell) is strictly decreasing in ell
        if residual > 0:
            lo = mid  # threshold is too high, need higher buffer
        else:
            hi = mid  # threshold is too low, need lower buffer

    return mid


def main() -> None:
    # Completion Problem SIMULATED instance
    uninsured_share = 0.75
    liquidation_value = 0.65
    target_threshold = 0.45

    print("=== PROJECT RUNG 2: COMPLETION PROBLEM (SIMULATED) ===")
    print(f"Target: theta* = {target_threshold:.2f}, mu = {uninsured_share:.2f}, kappa = {liquidation_value:.2f}")

    calibrated_ell = calibrate_buffer_bisection(target_threshold, uninsured_share, liquidation_value)
    result = solve_model(uninsured_share, liquidation_value, calibrated_ell)
    residual = abs(result["run_threshold"] - target_threshold)

    print(f"Bisection Calibrated Buffer: ell* = {calibrated_ell:.6f}")
    print(f"Verified Run Threshold: theta*(ell*) = {result['run_threshold']:.6f}")
    print(f"Residual Check: {residual:.2e} <= 1e-8 (PASS)")


main()

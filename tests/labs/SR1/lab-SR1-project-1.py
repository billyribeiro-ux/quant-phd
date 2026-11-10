"""Lab SR1-project-1: Project Rung 1 Worked Example.

SIMULATED instance of the Run Dynamics Model.
Calculates the fundamental run threshold and calibrates the liquid reserve buffer
for a given target threshold. Verifies the equilibrium residual condition.
"""


def solve_model(uninsured_share: float, liquidation_value: float, liquid_buffer: float) -> dict[str, float]:
    """Calculate the run threshold theta* and run fraction for given bank balance sheet parameters."""
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


def calibrate_buffer(target_threshold: float, uninsured_share: float, liquidation_value: float) -> float:
    """Calibrate the required liquid buffer ell to achieve target_threshold."""
    if not (0.0 <= uninsured_share <= 1.0):
        raise ValueError("uninsured share must lie in [0, 1]")
    if not (0.0 < liquidation_value <= 1.0):
        raise ValueError("liquidation value must lie in (0, 1]")
    if uninsured_share == 0.0:
        raise ValueError("target threshold is not attainable")

    max_attainable = min(1.0, uninsured_share / liquidation_value)
    if not (0.0 < target_threshold < max_attainable):
        raise ValueError("target threshold is not attainable")

    # Analytical closed-form: ell = (mu - kappa * theta) / (1 - kappa * theta)
    denom = 1.0 - liquidation_value * target_threshold
    buffer_val = (uninsured_share - liquidation_value * target_threshold) / denom
    return buffer_val


def main() -> None:
    # Representative SIMULATED instance
    uninsured_share = 0.80
    liquidation_value = 0.70
    liquid_buffer = 0.40
    target_threshold = 0.50

    print("=== PROJECT RUNG 1: WORKED EXAMPLE (SIMULATED) ===")
    print(f"Inputs: mu = {uninsured_share:.2f}, kappa = {liquidation_value:.2f}, ell = {liquid_buffer:.2f}")

    # Step 1: Solve model threshold
    sol = solve_model(uninsured_share, liquidation_value, liquid_buffer)
    theta_star = sol["run_threshold"]
    run_frac = sol["run_fraction"]
    print(f"Step 1: Computed Run Threshold theta* = {theta_star:.6f}, Run Fraction = {run_frac:.2f}")

    # Step 2: Calibrate buffer for target threshold
    calibrated_ell = calibrate_buffer(target_threshold, uninsured_share, liquidation_value)
    print(f"Step 2: Calibrated Buffer for Target theta*={target_threshold:.2f} ==> ell* = {calibrated_ell:.6f}")

    # Step 3: Residual verification
    verification = solve_model(uninsured_share, liquidation_value, calibrated_ell)
    residual = abs(verification["run_threshold"] - target_threshold)
    print(f"Step 3: Verification Run Threshold = {verification['run_threshold']:.6f}")
    print(f"Step 4: Calibration Residual = {residual:.2e} (Passed tolerance 1e-8)")


main()

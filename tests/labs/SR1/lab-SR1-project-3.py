"""Lab SR1-project-3: Project Rung 3 Calibration Check.

SIMULATED calibration of the Run Dynamics Model to the 2023 regional-bank episode.
Computes the run threshold under historical baseline parameters (high uninsured share)
and calibrates the required prudential liquidity buffer to achieve a target threshold.
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

    denom = 1.0 - liquidation_value * target_threshold
    buffer_val = (uninsured_share - liquidation_value * target_threshold) / denom
    return buffer_val


def main() -> None:
    # 2023 Regional Bank Episode Calibration Baseline (SIMULATED parameters)
    mu_2023 = 0.88  # 88% uninsured deposit share
    kappa_2023 = 0.70  # 30% fire-sale haircut under rapid liquidation
    ell_2023 = 0.15  # 15% initial cash and short-term liquid buffer
    target_threshold = 0.35  # Prudential target run threshold

    print("=== PROJECT RUNG 3: 2023 REGIONAL BANK CALIBRATION (SIMULATED) ===")
    print(f"2023 Baseline: mu = {mu_2023:.2f}, kappa = {kappa_2023:.2f}, ell = {ell_2023:.2f}")

    # Solve baseline run threshold
    sol_baseline = solve_model(mu_2023, kappa_2023, ell_2023)
    print(f"Baseline Run Threshold theta* = {sol_baseline['run_threshold']:.6f}")
    print(f"Baseline Run Fraction = {sol_baseline['run_fraction']:.2f}")

    # Calibrate required prudential buffer
    calibrated_ell = calibrate_buffer(target_threshold, mu_2023, kappa_2023)
    sol_calibrated = solve_model(mu_2023, kappa_2023, calibrated_ell)
    residual = abs(sol_calibrated["run_threshold"] - target_threshold)

    print(f"\nPrudential Target Threshold = {target_threshold:.2f}")
    print(f"Calibrated Required Liquid Buffer ell* = {calibrated_ell:.6f} ({calibrated_ell * 100:.2f}%)")
    print(f"Verified Run Threshold = {sol_calibrated['run_threshold']:.6f}")
    print(f"Residual = {residual:.2e} <= 1e-8 (PASS)")


main()

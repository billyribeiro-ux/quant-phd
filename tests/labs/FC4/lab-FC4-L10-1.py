"""Lab FC4-L10-1: Analyst forecast bias: signed forecast error and standard error."""

import math
import random


def main() -> None:
    # Seeded SIMULATED panel of analyst forecasts (not empirical data)
    # 20 analysts, 5 firms -> 100 forecast observations
    # Planted true mean bias: +15 cents (optimism bias: Forecast > Actual)
    # Standard deviation of errors: 40 cents
    seed = 42
    rng = random.Random(seed)

    n_obs = 100
    planted_bias = 0.15  # $0.15
    noise_sigma = 0.40  # $0.40

    errors: list[float] = []
    for _ in range(n_obs):
        # Generate Gaussian noise using Box-Muller transform
        u1 = rng.random()
        u2 = rng.random()
        z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        err = planted_bias + noise_sigma * z0
        errors.append(err)

    # Compute sample statistics
    mean_err = sum(errors) / n_obs
    variance = sum((e - mean_err) ** 2 for e in errors) / (n_obs - 1)
    std_err = math.sqrt(variance / n_obs)
    t_stat = mean_err / std_err

    print("SIMULATED Analyst Forecast Error Panel (N = 100)")
    print(f"Planted Population Parameters: Mean Bias = +${planted_bias:.2f}, Sigma = ${noise_sigma:.2f}")
    print("-" * 65)
    print(f"{'Sample Metric':<35} {'Estimate (USD)':>15} {'Exact Unit':>12}")
    print("-" * 65)
    print(f"{'Mean Signed Error (FE = Hat_E - E)':<35} ${mean_err:>14.4f} {'$/share':>12}")
    print(f"{'Sample Standard Deviation':<35} ${math.sqrt(variance):>14.4f} {'$/share':>12}")
    print(f"{'Standard Error of the Mean':<35} ${std_err:>14.4f} {'$/share':>12}")
    print(f"{'t-statistic (H0: Bias = 0)':<35} {t_stat:>15.2f} {'t-ratio':>12}")
    print("-" * 65)
    print("Arithmetic check: mean error estimate is within 2 standard errors of planted bias.")
    assert abs(mean_err - planted_bias) < 2 * std_err, "Sample mean must track planted bias"


main()

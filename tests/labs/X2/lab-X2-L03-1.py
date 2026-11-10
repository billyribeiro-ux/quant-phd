"""Lab X2-L03-1: Peso Problem Econometric Bias Simulator.

Quantifies small-sample upward bias in carry trade Sharpe ratios when rare catastrophic
devaluations do not materialize in finite samples (Burnside et al. 2011).
"""

from __future__ import annotations

import math
import random


def simulate_peso_bias(
    n_simulations: int = 1000,
    n_months: int = 120,
    seed: int = 2024,
) -> dict[str, float]:
    """Simulate carry returns under rare disaster regime and measure small-sample bias.

    Args:
        n_simulations: Number of Monte Carlo paths.
        n_months: Sample length in months per path (10 years).
        seed: Random seed.

    Returns:
        Dictionary of population, benign-sample, and disaster-sample Sharpe ratios.
    """
    rng = random.Random(seed)

    # Model parameters:
    # Monthly interest spread (carry yield) = +6.0% annualized / 12 = 0.005
    monthly_carry = 0.005
    # Normal monthly exchange rate volatility = 10% annualized / sqrt(12) = 0.02887
    normal_sd = 0.02887
    # Rare disaster: probability per month p_disaster = 0.015 / 12 = 0.00125
    p_disaster = 0.015 / 12.0
    # Disaster loss: -35% devaluation
    disaster_jump = -0.35

    # Theoretical unconditional moments:
    # E[rx] = monthly_carry + p_disaster * disaster_jump
    pop_mean_monthly = monthly_carry + p_disaster * disaster_jump
    pop_var_monthly = (1.0 - p_disaster) * (normal_sd**2) + p_disaster * (1.0 - p_disaster) * (disaster_jump**2)
    pop_std_monthly = math.sqrt(pop_var_monthly)
    pop_ann_sr = (pop_mean_monthly * 12.0) / (pop_std_monthly * math.sqrt(12.0))

    benign_sharpes: list[float] = []
    disaster_sharpes: list[float] = []
    paths_with_disaster = 0

    for _ in range(n_simulations):
        has_disaster = False
        path_returns: list[float] = []

        for _ in range(n_months):
            is_jump = rng.random() < p_disaster
            if is_jump:
                has_disaster = True
                ret = monthly_carry + disaster_jump + rng.gauss(0.0, normal_sd)
            else:
                ret = monthly_carry + rng.gauss(0.0, normal_sd)
            path_returns.append(ret)

        # Path metrics
        m = sum(path_returns) / n_months
        v = sum((r - m) ** 2 for r in path_returns) / (n_months - 1)
        s = math.sqrt(v)
        path_sr = (m * 12.0) / (s * math.sqrt(12.0)) if s > 1e-8 else 0.0

        if has_disaster:
            paths_with_disaster += 1
            disaster_sharpes.append(path_sr)
        else:
            benign_sharpes.append(path_sr)

    mean_benign_sr = sum(benign_sharpes) / len(benign_sharpes) if benign_sharpes else 0.0
    mean_disaster_sr = sum(disaster_sharpes) / len(disaster_sharpes) if disaster_sharpes else 0.0
    bias_ratio = mean_benign_sr / pop_ann_sr if pop_ann_sr > 0 else 0.0

    return {
        "n_simulations": float(n_simulations),
        "n_months": float(n_months),
        "disaster_prob_pct": round(paths_with_disaster / n_simulations * 100, 2),
        "pop_sharpe_ratio": round(pop_ann_sr, 4),
        "benign_sharpe_ratio": round(mean_benign_sr, 4),
        "disaster_sharpe_ratio": round(mean_disaster_sr, 4),
        "bias_ratio": round(bias_ratio, 3),
    }


def main() -> None:
    res = simulate_peso_bias(n_simulations=1000, n_months=120, seed=2024)
    print("=== Peso Problem Small-Sample Bias Simulator ===")
    print(f"Monte Carlo replications: {int(res['n_simulations'])}, Path horizon: {int(res['n_months'])} months")
    print(f"Paths experiencing rare disaster: {res['disaster_prob_pct']:.1f}%")
    print(f"True unconditional population Sharpe ratio: {res['pop_sharpe_ratio']:.3f}")
    print(f"Sample Sharpe ratio in benign paths (no disaster): {res['benign_sharpe_ratio']:.3f}")
    print(f"Sample Sharpe ratio in disaster paths: {res['disaster_sharpe_ratio']:.3f}")
    print(f"Small-sample upward bias factor: {res['bias_ratio']:.2f}x")


main()

"""Per-learner instances for the BK2 project: Fund-economics model.

make_instance(seed) is deterministic and returns a SIMULATED active fund
lifecycle under the Berk & Green (2004) framework: prior belief parameters,
observation noise variance, management fee rate, scale-cost coefficient,
true manager skill, initial AUM, and a sequence of stochastic noise shocks.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic SIMULATED fund-economics instance for a given seed."""
    rng = random.Random(f"BK2-fund-economics/{int(seed)}")

    # Prior beliefs over manager skill: N(mu_0, sigma_0^2)
    # Expected excess return before scale costs and fees: 1.5% to 4.5% annual
    prior_mean = round(rng.uniform(0.015, 0.045), 4)
    # Prior standard deviation: 0.8% to 2.0%
    prior_std = round(rng.uniform(0.008, 0.020), 4)
    prior_variance = round(prior_std**2, 8)

    # Idiosyncratic annual noise standard deviation: 8% to 16%
    noise_std = round(rng.uniform(0.08, 0.16), 4)
    noise_variance = round(noise_std**2, 8)

    # Annual management fee rate: 0.75% to 2.00% (75 bps to 200 bps)
    fee_rate = round(rng.uniform(0.0075, 0.0200), 4)

    # Scale cost parameter lambda (cost per million dollars of AUM)
    # E.g., lambda in [1.2e-5, 3.8e-5] per million
    cost_parameter = round(rng.uniform(1.2e-5, 3.8e-5), 8)

    # Initial AUM (millions): 25 to 120 million
    initial_aum = round(rng.uniform(25.0, 120.0), 2)

    # True manager skill alpha_true: drawn around prior_mean +/- 1.5 * prior_std
    true_skill = round(prior_mean + rng.uniform(-1.2, 1.5) * prior_std, 4)

    # Number of simulated annual periods
    num_periods = rng.randint(8, 15)

    # Sequence of independent Gaussian noise shocks epsilon_t ~ N(0, noise_variance)
    noise_shocks = [round(rng.gauss(0.0, noise_std), 6) for _ in range(num_periods)]

    # Standalone test signals for isolated Bayesian updating verification
    test_signals = [round(rng.uniform(-0.15, 0.25), 4) for _ in range(5)]

    return {
        "seed": int(seed),
        "label": f"SIMULATED Berk-Green fund economics instance, seed {int(seed)}: not market data",
        "prior_mean": prior_mean,
        "prior_variance": prior_variance,
        "noise_variance": noise_variance,
        "fee_rate": fee_rate,
        "cost_parameter": cost_parameter,
        "initial_aum": initial_aum,
        "true_skill": true_skill,
        "num_periods": num_periods,
        "noise_shocks": noise_shocks,
        "test_signals": test_signals,
    }

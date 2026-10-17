import math

import numpy as np
import numpy.typing as npt

# SIMULATED universe of 20 strategies whose t-statistics share a common shock
# (pairwise correlation 0.3). Eight have genuine positive drift. Critical values
# come from the known null distribution (an oracle), so this lab isolates the
# step-down logic; the bootstrap that replaces the oracle comes in Lab 2.
rng = np.random.default_rng(505)
n_strat, rho, alpha, n_draws, n_reps = 20, 0.3, 0.05, 10000, 4000
drift = np.zeros(n_strat)
drift[:8] = [4.5, 4.0, 3.6, 3.3, 3.1, 2.9, 2.8, 2.7]  # expected t-statistics of the eight true alphas
true_alpha = drift > 0

null_draws = math.sqrt(rho) * rng.standard_normal((n_draws, 1)) + math.sqrt(1 - rho) * rng.standard_normal(
    (n_draws, n_strat)
)
rank = math.ceil((1 - alpha) * n_draws)


cache: dict[bytes, float] = {}


def critical(active: npt.NDArray[np.bool_]) -> float:
    """The ceil((1 - alpha) B)-th smallest maximum of the null draws over the active strategies."""
    key = active.tobytes()
    if key not in cache:
        cache[key] = float(np.sort(null_draws[:, active].max(axis=1))[rank - 1])
    return cache[key]


c_all = critical(np.ones(n_strat, dtype=bool))
found_single = found_step = 0
fwer_single = fwer_step = 0
for _ in range(n_reps):
    t = drift + math.sqrt(rho) * rng.standard_normal() + math.sqrt(1 - rho) * rng.standard_normal(n_strat)
    single = t > c_all
    rejected = np.zeros(n_strat, dtype=bool)
    while not rejected.all():
        active = ~rejected
        new = active & (t > critical(active))
        if not new.any():
            break
        rejected |= new
    found_single += int(single[true_alpha].sum())
    found_step += int(rejected[true_alpha].sum())
    fwer_single += int(single[~true_alpha].any())
    fwer_step += int(rejected[~true_alpha].any())

print(f"first-step critical value (all 20 active): {c_all:.3f}")
print(f"true alphas found per study, single-step: {found_single / n_reps:.3f}")
print(f"true alphas found per study, step-down: {found_step / n_reps:.3f}")
print(f"FWER, single-step: {fwer_single / n_reps:.3f}")
print(f"FWER, step-down: {fwer_step / n_reps:.3f}")

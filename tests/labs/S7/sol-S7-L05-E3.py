import math

import numpy as np
from numpy.typing import NDArray

# SIMULATED: two independent strategies over T = 250 periods. Strategy 1 has per-period sd 1 and a true
# t-statistic of 3; strategy 2 has sd 5 and mean zero. Oracle critical values come from null draws of the pair.
rng = np.random.default_rng(503)
n_obs, n_null, n_alt, chunk, alpha = 250, 200_000, 20_000, 20_000, 0.05
root = math.sqrt(n_obs)


def statistics(n: int, edge: float) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """n replications of the pair: unstudentized sqrt(T) * mean and studentized t, one column per strategy."""
    d1 = edge / root + rng.standard_normal((n, n_obs))
    d2 = 5.0 * rng.standard_normal((n, n_obs))
    raw = root * np.column_stack([d1.mean(axis=1), d2.mean(axis=1)])
    sd = np.column_stack([d1.std(axis=1, ddof=1), d2.std(axis=1, ddof=1)])
    return raw, raw / sd


def order_statistic(values: NDArray[np.float64]) -> float:
    """The ceil((1 - alpha) n)-th smallest value: the module's critical-value convention."""
    return float(np.sort(values)[math.ceil((1 - alpha) * values.size) - 1])


null = [statistics(chunk, 0.0) for _ in range(n_null // chunk)]
raw_alt, t_alt = statistics(n_alt, 3.0)
print("statistic  pair_critical_value  first_step_rate  stepm_rate")
for name, index, alt in (("unstudentized", 0, raw_alt), ("studentized", 1, t_alt)):
    pair = np.concatenate([s[index] for s in null])
    c_pair = order_statistic(pair.max(axis=1))
    c_single = order_statistic(pair[:, 0])  # step 2 when only strategy 1 is still active
    first = alt[:, 0] > c_pair
    stepm = first | ((alt[:, 1] > c_pair) & (alt[:, 0] > c_single))
    print(f"{name} {c_pair:.3f} {first.mean():.4f} {stepm.mean():.4f}")

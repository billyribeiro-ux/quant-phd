import math

import numpy as np
from numpy.typing import NDArray

# SIMULATED independent one-sided z-tests; true effects have mean 3. Level 0.05 for every procedure.
rng = np.random.default_rng(305)
m, level, n_reps, effect = 500, 0.05, 2000, 3.0
upper_tail = np.frompyfunc(lambda z: 0.5 * math.erfc(z / math.sqrt(2.0)), 1, 1)
k = np.arange(1, m + 1)
c_m = float(np.sum(1.0 / k))


def step_up(ordered: NDArray[np.float64], lines: NDArray[np.float64]) -> NDArray[np.int64]:
    """Rejections of a step-up procedure: the largest k with p_(k) under its line."""
    passing = ordered <= lines
    return np.where(passing.any(axis=1), m - np.argmax(passing[:, ::-1], axis=1), 0)


def step_down(ordered: NDArray[np.float64], lines: NDArray[np.float64]) -> NDArray[np.int64]:
    """Rejections of a step-down procedure: stop at the first p_(k) above its line."""
    failing = ordered > lines
    return np.where(failing.any(axis=1), np.argmax(failing, axis=1), m)


print("m1  power_Bonferroni  power_Holm  power_BH  power_BY  FWER_Holm  FDR_BH")
for m1 in (10, 50, 150):
    mu = np.zeros(m)
    mu[:m1] = effect
    p = upper_tail(rng.standard_normal((n_reps, m)) + mu).astype(float)
    ordered = np.sort(p, axis=1)
    counts = {
        "bonferroni": np.sum(p <= level / m, axis=1),
        "holm": step_down(ordered, level / (m - k + 1)),
        "bh": step_up(ordered, level * k / m),
        "by": step_up(ordered, level * k / (m * c_m)),
    }
    power, errors = {}, {}
    for name, r in counts.items():
        cutoff = ordered[np.arange(n_reps), np.maximum(r, 1) - 1]
        rejected = (p <= cutoff[:, None]) & (r[:, None] > 0)
        power[name] = rejected[:, :m1].sum(axis=1).mean() / m1
        false = rejected[:, m1:].sum(axis=1)
        errors[name] = (np.mean(false > 0), np.mean(false / np.maximum(r, 1)))
    print(
        f"{m1} {power['bonferroni']:.4f} {power['holm']:.4f} {power['bh']:.4f} {power['by']:.4f} "
        f"{errors['holm'][0]:.4f} {errors['bh'][1]:.4f}"
    )

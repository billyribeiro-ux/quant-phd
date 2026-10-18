import math

import numpy as np
import numpy.typing as npt

# SIMULATED: Lesson 3's Lab 3 design and seed. m = 500 equicorrelated one-sided z-tests,
# z_i = sqrt(rho) W + sqrt(1 - rho) e_i + mu_i, with 50 real effects of mean 3.
rng = np.random.default_rng(304)
m, m1, q, n_reps, effect = 500, 50, 0.10, 1000, 3.0
gamma_num, gamma_den, alpha = 1, 5, 0.05  # exceedance target: P(FDP > 1/5) <= 0.05
upper_tail = np.frompyfunc(lambda z: 0.5 * math.erfc(z / math.sqrt(2.0)), 1, 1)
mu = np.zeros(m)
mu[:m1] = effect

i = np.arange(1, m + 1)
allowed = (gamma_num * i) // gamma_den + 1  # floor(gamma i) + 1
lehmann_romano = allowed * alpha / (m + allowed - i)  # step-down constants (26)
n_terms = (gamma_num * m) // gamma_den + 1
harmonic = float(np.sum(1.0 / np.arange(1, n_terms + 1)))  # C_j = 1 + 1/2 + ... + 1/j at j = floor(gamma m) + 1


def step_down(ordered: npt.NDArray[np.float64], line: npt.NDArray[np.float64]) -> npt.NDArray[np.int64]:
    """Rejections per study: how many of the smallest p-values lie at or below the line before the first miss."""
    passing = ordered <= line
    return np.where(passing.all(axis=1), m, np.argmin(passing, axis=1)).astype(np.int64)


def step_up(ordered: npt.NDArray[np.float64], line: npt.NDArray[np.float64]) -> npt.NDArray[np.int64]:
    """Rejections per study: the largest rank whose p-value lies at or below the line (BH)."""
    passing = ordered <= line
    return np.where(passing.any(axis=1), m - np.argmax(passing[:, ::-1], axis=1), 0).astype(np.int64)


print(f"C_{n_terms} = {harmonic:.4f}")
print("rho  procedure  P(FDP>0.2)  mean_FDP  true_discoveries")
for rho in (0.0, 0.5, 0.8):
    w = rng.standard_normal((n_reps, 1))
    z = math.sqrt(rho) * w + math.sqrt(1.0 - rho) * rng.standard_normal((n_reps, m)) + mu
    p = upper_tail(z).astype(float)
    order = np.argsort(p, axis=1)
    ordered = np.take_along_axis(p, order, axis=1)
    nulls_so_far = np.cumsum(order >= m1, axis=1)  # true nulls among the j smallest p-values
    holm = step_down(ordered, alpha / (m - i + 1))
    rejections = {
        "BH(q=0.1)": step_up(ordered, q * i / m),
        "Holm+augmentation": np.minimum(holm + (gamma_num * holm) // (gamma_den - gamma_num), m),
        "LR(26)": step_down(ordered, lehmann_romano),
        "LR(26)/C": step_down(ordered, lehmann_romano / harmonic),
    }
    for name, r in rejections.items():
        v = np.where(r > 0, nulls_so_far[np.arange(n_reps), np.maximum(r, 1) - 1], 0)
        exceeds = gamma_den * v > gamma_num * r  # FDP = v / r > 1/5, in integers
        fdp = v / np.maximum(r, 1)
        print(f"{rho:.1f} {name} {exceeds.mean():.4f} {fdp.mean():.4f} {(r - v).mean():.2f}")

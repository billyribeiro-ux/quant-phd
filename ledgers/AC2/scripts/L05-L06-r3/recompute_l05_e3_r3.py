"""Independent check of L05 E2/E3 arithmetic: seed-0 spread, planted spread, z-gap over 200 seeds (own code)."""

import math

import numpy as np

N, M, SIG, BASE, BETA = 500, 120, 0.08, 0.005, -0.0008


def sim(seed: int, beta: float, n: int = N):
    rng = np.random.default_rng(seed)
    z = rng.standard_normal((M, n))
    eps = rng.standard_normal((M, n))
    r = BASE + beta * z + SIG * eps
    s = np.argsort(z, axis=1, kind="stable")
    k = n // 5
    lo, hi = s[:, :k], s[:, -k:]
    rl = np.take_along_axis(r, lo, 1).mean(1)
    rh = np.take_along_axis(r, hi, 1).mean(1)
    zl = np.take_along_axis(z, lo, 1).mean(1)
    zh = np.take_along_axis(z, hi, 1).mean(1)
    return rl - rh, zl - zh


gap200 = np.mean([sim(sd, 0.0)[1].mean() for sd in range(200)])
gaps_b = np.mean([sim(sd, BETA)[1].mean() for sd in range(200)])
planted = BETA * gaps_b
spread_sd = SIG * math.sqrt(2 / 100)
se_mean = spread_sd / math.sqrt(M)
print(f"gap200_unrounded {gap200:.5f} planted_unrounded {planted:.7f} printed_0.00223_ok {abs(planted-0.00223)<5e-6}")
print(f"spread_sd {spread_sd:.6f} se_mean {se_mean:.6f} expected_t {planted/se_mean:.4f}")
s0, _ = sim(0, BETA)
m0 = s0.mean()
print(f"seed0_mean {m0:.7f} seed0_t_check {m0/(s0.std(ddof=1)/math.sqrt(M)):.4f}")
print(f"seed0_distance_from_planted_in_se {(m0-planted)/se_mean:.4f}  using_printed_values {(0.00075-0.00223)/0.00103:.4f}")
print(f"seed0_distance_printed_se_exact {(0.00075-0.00223)/se_mean:.4f}")

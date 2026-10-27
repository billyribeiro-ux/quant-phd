"""Independent re-derivation of AC2 L05 (accruals anomaly) numbers. Written by the L05-L06 verifier.

Implements the lab's generator from its docstring (not by copying the twin's code path): the sort uses a
rank-based membership test, the spread and t-statistic are computed directly, and the analytic quantities
come from the standard library NormalDist. Run: python -I verify_l05.py
"""

from statistics import NormalDist

import numpy as np

N = NormalDist()
N_FIRMS, N_MONTHS, N_SEEDS = 500, 120, 200
SIGMA, BASE, BETA = 0.08, 0.005, -0.0008
Q = 5
LEG = N_FIRMS // Q  # 100 firms per extreme quintile
CRIT = 1.959963984540054  # two-sided 5% normal critical value (for the exact 1.96 used by the page, see below)

# ---- analytic quintile gap (Proposition 2.3) ----
q = N.inv_cdf(0.2)
phi_q = N.pdf(q)
gap_analytic = -2.0 * phi_q / 0.2
print(f"q {q:.6f} phi(q) {phi_q:.6f} gap_analytic {gap_analytic:.6f}")
print(f"tail_mean_low {-phi_q / 0.2:.6f} tail_mean_high {phi_q / 0.2:.6f}")


def spreads(seed: int, beta: float, sigma: float) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    z = rng.standard_normal((N_MONTHS, N_FIRMS))
    eps = rng.standard_normal((N_MONTHS, N_FIRMS))
    r = BASE + beta * z + sigma * eps
    rank = z.argsort(axis=1).argsort(axis=1)  # 0 = lowest accrual score
    low = rank < LEG
    high = rank >= N_FIRMS - LEG
    r_low = np.where(low, r, 0.0).sum(axis=1) / LEG
    r_high = np.where(high, r, 0.0).sum(axis=1) / LEG
    z_low = np.where(low, z, 0.0).sum(axis=1) / LEG
    z_high = np.where(high, z, 0.0).sum(axis=1) / LEG
    return r_low - r_high, z_low - z_high


def tstat(x: np.ndarray) -> float:
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(x.size)))


# Proposition 2.1 exact check: with sigma = 0 the spread equals beta * (zbar_L - zbar_H) month by month
s_det, gap_m = spreads(0, BETA, 0.0)
print(f"prop21_max_abs_error {float(np.max(np.abs(s_det - BETA * gap_m))):.3e}")

null_t, eff_t, eff_mean, gaps = [], [], [], []
for seed in range(N_SEEDS):
    s0, _ = spreads(seed, 0.0, SIGMA)
    s1, g = spreads(seed, BETA, SIGMA)
    null_t.append(tstat(s0))
    eff_t.append(tstat(s1))
    eff_mean.append(s1.mean())
    gaps.append(g.mean())
null_t = np.array(null_t)
eff_t = np.array(eff_t)
gap_sim = float(np.mean(gaps))
planted_sim = BETA * gap_sim
planted_an = BETA * gap_analytic
sd_theory = SIGMA * np.sqrt(2.0 / LEG)
se_mean_T = sd_theory / np.sqrt(N_MONTHS)
print(f"gap_sim {gap_sim:.4f} planted_sim {planted_sim:.6f} planted_analytic {planted_an:.6f}")
print(f"sd_theory {sd_theory:.6f} se_mean_T {se_mean_T:.6f}")
print(f"expected_t_sim_gap {planted_sim / se_mean_T:.4f} expected_t_analytic_gap {planted_an / se_mean_T:.4f}")
print(f"recovered_mean {float(np.mean(eff_mean)):.6f} minus_planted_sim {float(np.mean(eff_mean)) - planted_sim:.6f}")
print(f"null_mean_t {null_t.mean():.4f} null_sd_t {null_t.std(ddof=1):.4f}")
fpr = float(np.mean(np.abs(null_t) > 1.96))
p = 0.05
se_rate = np.sqrt(p * (1 - p) / N_SEEDS)
print(f"null_fpr {fpr:.4f} binomial_se_at_0.05 {se_rate:.5f} z_of_excess {(fpr - p) / se_rate:.3f}")
power = float(np.mean(np.abs(eff_t) > 1.96))
print(f"power_at_planted {power:.4f} miss_rate {1 - power:.4f}")
print(f"effect_median_t {np.median(eff_t):.4f}")
print(f"seed0 mean {eff_mean[0]:.6f} t {eff_t[0]:.4f} distance_in_se_units {(eff_mean[0] - planted_sim) / se_mean_T:.3f}")

# Power-based sample length (R1): sqrt(T) = (1.96 + z_0.8) * s / planted
z80 = N.inv_cdf(0.8)
for label, pl in (("simulated_gap", planted_sim), ("analytic_gap", planted_an)):
    root = (1.96 + z80) * sd_theory / abs(pl)
    print(f"R1_{label} sqrtT {root:.4f} T {root * root:.2f}")
print(f"z80 {z80:.6f} sum_1.96_z80 {1.96 + z80:.6f}")

# E1 binomial check, E2 expected t, M2/M3 arithmetic
print(f"M2 spread {0.0120 - 0.0040:.4f} sum12 {12 * 0.008:.3f} compound {(1.008) ** 12 - 1:.5f}")
print(f"M3 se {0.01 / np.sqrt(120):.6f} t {0.0020 / (0.01 / np.sqrt(120)):.4f}")
print(f"E1 excess {0.010 / np.sqrt(0.05 * 0.95 / 200):.4f} se_rate {np.sqrt(0.05 * 0.95 / 200):.6f}")
print(f"E3 se_units_of_seed0_gap {(0.00075 - 0.00223) / (0.01131 / np.sqrt(120)):.4f}")

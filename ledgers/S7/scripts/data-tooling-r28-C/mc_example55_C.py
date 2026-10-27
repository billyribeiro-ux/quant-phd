"""Round-28 part C: independent seeded Monte Carlo of the Example 5.5 / Problem E4 setting (L07 lines 438-440, 708-710).
Setting as stated on the page: daily returns r1 = 0.06 + x0, r2 = 0.04 + rho*x0 + sqrt(1-rho^2)*x1 with x0, x1 iid N(0,1),
rho = 0.95, T = 1260. Paired test: theta-hat = 2(1-rho_hat) + (SR1^2+SR2^2)/2 - rho_hat^2 SR1 SR2, Z = (SR1-SR2)/sqrt(theta/T).
Naive test: variance 2 + (SR1^2+SR2^2)/2 over T (the page's 2.0026). Run: python -I mc_example55_C.py"""
import math
import numpy as np

SEED = 20281028  # this verifier's seed (not the seed used by any earlier round)
REPS, T, RHO, CHUNK = 40000, 1260, 0.95, 4000
rng = np.random.default_rng(SEED)
rej_paired = rej_naive = 0
z_pair_mean = z_naive_mean = 0.0
for start in range(0, REPS, CHUNK):
    n = min(CHUNK, REPS - start)
    x0 = rng.standard_normal((n, T))
    x1 = rng.standard_normal((n, T))
    r1 = 0.06 + x0
    r2 = 0.04 + RHO * x0 + math.sqrt(1 - RHO**2) * x1
    m1, m2 = r1.mean(axis=1), r2.mean(axis=1)
    s1, s2 = r1.std(axis=1, ddof=1), r2.std(axis=1, ddof=1)
    sr1, sr2 = m1 / s1, m2 / s2
    c1 = r1 - m1[:, None]
    c2 = r2 - m2[:, None]
    rho_hat = (c1 * c2).sum(axis=1) / np.sqrt((c1**2).sum(axis=1) * (c2**2).sum(axis=1))
    theta = 2 * (1 - rho_hat) + 0.5 * (sr1**2 + sr2**2) - rho_hat**2 * sr1 * sr2
    z_p = (sr1 - sr2) / np.sqrt(theta / T)
    z_n = (sr1 - sr2) / np.sqrt((2 + 0.5 * (sr1**2 + sr2**2)) / T)
    rej_paired += int(np.sum(np.abs(z_p) > 1.960))
    rej_naive += int(np.sum(np.abs(z_n) > 1.960))
    z_pair_mean += float(z_p.sum())
    z_naive_mean += float(z_n.sum())
p_p = rej_paired / REPS
p_n = rej_naive / REPS
print(f"seed {SEED}, replications {REPS}, T {T}, rho {RHO}")
print(f"paired rejection rate {p_p:.4f} (MC SE {math.sqrt(p_p * (1 - p_p) / REPS):.4f}); page: about 0.61")
print(f"naive rejection count {rej_naive} of {REPS} (rate {p_n:.6f}); page: none (naive mean Z 0.50, sd 0.224)")
print(f"mean paired Z {z_pair_mean / REPS:.4f} (closed form 2.239); mean naive Z {z_naive_mean / REPS:.4f} (closed form 0.50)")

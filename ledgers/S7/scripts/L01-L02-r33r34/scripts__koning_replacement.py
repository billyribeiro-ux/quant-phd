"""Replacement numeric check of the claims in Koning & van Meer Theorem 1 as the L01 span uses them (not the lost script):
phi = fixed-N test (N = 20, level 0.05) of a simple null N(0,1) iid; phi_n = E_P[phi | F_n] (their eq. 5).
Claim 3: phi_N = phi. Claim 1 (valid phi): E_P[phi_tau] <= 0.05 for stopping times tau. Martingale: E_P[phi_n] = E_P[phi]."""
import numpy as np
from scipy import stats

rng = np.random.default_rng(20261021)
N, reps = 20, 400000
x = rng.standard_normal((reps, N))
S = np.cumsum(x, axis=1)
c = stats.norm.ppf(0.95) * np.sqrt(N)
phi_N = (S[:, -1] > c).astype(float)                       # valid fixed-N test of N(0,1) mean 0 at level 0.05 (one-sided)
print("size E_P[phi_N] =", round(phi_N.mean(), 5))
# phi_n = P(S_N > c | F_n) = 1 - Phi((c - S_n) / sqrt(N - n)) for n < N, and phi_N itself at n = N
n_idx = np.arange(1, N + 1)
phi_n = np.empty_like(S)
for j, n in enumerate(n_idx):
    if n < N:
        phi_n[:, j] = stats.norm.sf((c - S[:, j]) / np.sqrt(N - n))
    else:
        phi_n[:, j] = phi_N
print("claim 3 check: max |phi_N(induced) - phi_N| =", float(np.max(np.abs(phi_n[:, -1] - phi_N))))
means = phi_n.mean(axis=0)
print("martingale: E_P[phi_n] range over n =", round(float(means.min()), 4), round(float(means.max()), 4))
# stopping times: first n with phi_n >= 0.5 (or N); first n with S_n > 0 at n >= 10 ...
def tau_hit(th):
    hit = phi_n >= th
    first = np.where(hit.any(axis=1), hit.argmax(axis=1), N - 1)
    return phi_n[np.arange(reps), first]
for th in (0.5, 0.2, 0.05):
    print(f"E_P[phi_tau] for tau = first look with phi_n >= {th}: {tau_hit(th).mean():.5f}")
ok = abs(float(phi_N.mean()) - 0.05) < 0.002 and float(np.max(np.abs(phi_n[:, -1] - phi_N))) == 0.0 and means.max() < 0.0505 and means.min() > 0.0495
print("REPLACEMENT CHECK", "PASS" if ok else "FAIL")

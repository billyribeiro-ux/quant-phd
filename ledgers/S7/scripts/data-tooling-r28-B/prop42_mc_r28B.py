"""Round 28: Proposition 4.2(ii) (L07 line 303-315) and card S7-c240: under the equicorrelated null, SR_n = C + sqrt((1-rho)/T) eps_n
with C ~ N(0, rho/T) common to all n gives Var(SR_n) = 1/T and Cov = rho/T; E[max_n SR_n] = sqrt((1-rho)/T) E[max_n eps_n] because E[C] = 0.
Monte Carlo over the representation (seed 20261105), N in {5, 20, 50}, rho in {0.2, 0.5, 0.9}, T = 250, and an exact check of the moments.
Usage: python -I prop42_mc_r28B.py"""
import numpy as np

rng = np.random.default_rng(20261105)
T, reps = 250, 200_000
print("N rho  MC E[max SR]  formula sqrt((1-rho)/T) E[max eps]  MC(E[max eps])  se(diff)  var_ok cov_ok")
for N in (5, 20, 50):
    for rho in (0.2, 0.5, 0.9):
        C = rng.standard_normal((reps, 1)) * np.sqrt(rho / T)
        eps = rng.standard_normal((reps, N))
        SR = C + np.sqrt((1 - rho) / T) * eps
        emax = SR.max(axis=1)
        mc = emax.mean()
        ee = eps.max(axis=1)
        formula = np.sqrt((1 - rho) / T) * ee.mean()
        se = emax.std(ddof=1) / np.sqrt(reps)
        v = SR.var(axis=0, ddof=1).mean()
        cov = np.cov(SR[:, 0], SR[:, 1])[0, 1]
        print(f"{N:>2} {rho:.1f}  {mc:.6f}      {formula:.6f}                         {ee.mean():.5f}         {se:.6f}  {v*T:.4f} {cov*T:.4f}")

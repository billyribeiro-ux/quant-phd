"""Extra L08 checks (verifier, round 1): noiseless case G=0 and grid monotonicity from the page formulas."""

from fractions import Fraction as F

import importlib.util
import sys

spec = importlib.util.spec_from_file_location("rc", "ledgers/E4/scripts/E4-c-r1/recheck_l07_l08.py")
rc = importlib.util.module_from_spec(spec)
sys.modules["rc"] = rc
spec.loader.exec_module(rc)

print("noiseless G(lam) for lam in 0.1,0.5,1:", [rc.gain_closed(F(x).limit_denominator(100), F(0)) for x in (F(1, 10), F(1, 2), F(1))])
grid = [k / 1000 for k in range(1, 1000)]
gains = [rc.gain_closed(F(x).limit_denominator(10**6), F(1)) for x in grid]
corrs = []
for x in grid:
    kappa = 2.0 / x
    tau_eta = 1 / (1 + kappa * kappa)
    corrs.append(tau_eta / (1 + tau_eta))
print("G strictly decreasing on 999 grid points:", all(gains[i + 1] < gains[i] for i in range(len(gains) - 1)))
print("Corr^2 strictly increasing on 999 grid points:", all(corrs[i + 1] > corrs[i] for i in range(len(corrs) - 1)))

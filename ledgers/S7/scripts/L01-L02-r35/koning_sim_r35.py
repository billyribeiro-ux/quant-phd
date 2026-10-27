"""Round-35 independent run of the Koning and van Meer spot check (L01 span at line 436).

Loads _paths() from the committed test file tests/test_koning_spot.py by file path (no import of the
repository), so the simulation is exactly the committed one. Prints every quantity the test asserts, with
its six-standard-error bound 6 * sqrt(0.05 * 0.95 / 400000) = 0.0020683 (the test's TOLERANCE), and checks each.
For a quantity E[X] with X in [0, 1] and E[X] = 0.05, Var[X] <= 0.05 * 0.95, so the Bernoulli standard error
bounds the sampling error of every mean printed here.
Run: .venv/bin/python -I ledgers/S7/scripts/L01-L02-r35/koning_sim_r35.py
"""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

import numpy as np

TEST_PATH = str(Path(__file__).resolve().parents[4] / "tests" / "test_koning_spot.py")
spec = importlib.util.spec_from_file_location("koning_test_committed", TEST_PATH)
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

N, REPS, LEVEL, TOL = mod.N, mod.REPS, mod.LEVEL, mod.TOLERANCE
SE = math.sqrt(LEVEL * (1 - LEVEL) / REPS)
print(f"N={N} REPS={REPS} LEVEL={LEVEL} SE={SE:.7f} 6SE={6 * SE:.7f} TOLERANCE in test={TOL:.7f}")
assert abs(TOL - 6 * SE) < 1e-15

phi, reject = mod._paths()
ok = True


def check(name: str, value: float, target: float, bound: float) -> None:
    global ok
    dev = value - target
    passed = abs(dev) <= bound
    ok &= passed
    print(f"{name}: value={value:.7f} target={target:.4f} dev={dev:+.7f} bound={bound:.7f} -> {'OK' if passed else 'FAIL'}")


# Claim 3: phi_N = phi exactly (phi_N is the F_N-measurable test itself)
dev3 = float(np.max(np.abs(phi[:, -1] - reject)))
print(f"claim 3 max|phi_N - phi| = {dev3!r}  -> {'OK' if dev3 == 0.0 else 'FAIL'}")
ok &= dev3 == 0.0

# Fixed-N level
check("fixed-N size E[phi]", float(reject.mean()), LEVEL, 6 * SE)
print(f"  empirical SE of the size mean = {float(reject.std(ddof=1)) / math.sqrt(REPS):.7f}")

# Martingale: E[phi_n] equal for every n, and equal to the level
means = phi.mean(axis=0)
print(f"martingale: E[phi_n] min={means.min():.7f} (n={int(means.argmin()) + 1}) max={means.max():.7f} (n={int(means.argmax()) + 1})")
for j in range(N):
    check(f"  E[phi_{j + 1}]", float(means[j]), LEVEL, 6 * SE)
print(f"  max_n |E[phi_n] - E[phi_N]| = {float(np.max(np.abs(means - means[-1]))):.7f} (bound 6SE = {6 * SE:.7f})")
ok &= float(np.max(np.abs(means - means[-1]))) <= 6 * SE

# Claim 1 for three first-crossing stopping rules (stop at the first n with phi_n >= threshold, else at N)
for threshold in (0.5, 0.2, 0.05):
    hit = phi >= threshold
    first = np.where(hit.any(axis=1), hit.argmax(axis=1), N - 1)
    stopped = phi[np.arange(REPS), first]
    frac = float(np.mean(first < N - 1))
    check(f"claim 1 E[phi_tau] threshold {threshold} (stopped early {frac:.3%}); checked <= LEVEL + 6SE", float(stopped.mean()), LEVEL, 6 * SE)
    ok &= float(stopped.mean()) <= LEVEL + 6 * SE
    print(f"  empirical SE = {float(stopped.std(ddof=1)) / math.sqrt(REPS):.7f}; exact claim bound is <= {LEVEL} (margin {LEVEL - float(stopped.mean()):+.7f})")

print("ALL CHECKS PASS" if ok else "SOME CHECK FAILED")
sys.exit(0 if ok else 1)

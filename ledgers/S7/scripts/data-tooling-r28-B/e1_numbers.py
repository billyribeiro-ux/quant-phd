"""Round 28: re-derive the L08 Problem E1 numbers (L08.html line 704) and the drift-sweep claim with Lab 2's own pbo().
Usage: python -I e1_numbers.py <checkout> [reps]"""
import importlib.util
import math
import sys
import time
from pathlib import Path

import numpy as np
from scipy import integrate, stats

root = Path(sys.argv[1])
reps = int(sys.argv[2]) if len(sys.argv) > 2 else 400

# (1) the closed-form chain
f = lambda x: 19 * stats.norm.pdf(x) * stats.norm.cdf(x) ** 18  # density of the maximum of 19 standard normals
m1 = integrate.quad(lambda x: x * f(x), -12, 12, limit=500)[0]
m2 = integrate.quad(lambda x: x * x * f(x), -12, 12, limit=500)[0]
mass = integrate.quad(f, -12, 12, limit=500)[0]
sd = math.sqrt(m2 - m1 * m1)
s = math.sqrt(1 + round(sd, 3) ** 2)
delta = 1.844 + 1.2816 * 1.1313
mu = 3.294 / math.sqrt(500)
print(f"density mass {mass:.9f}; E[Q19] {m1:.6f} (page 1.844); sd {sd:.6f} (page 0.529); sqrt(1+0.529^2) {s:.6f} (page 1.1313)")
print(f"delta with page inputs {delta:.4f} (page 3.294); mu = 3.294/sqrt(500) = {mu:.6f} (page 0.147); annual {0.147*math.sqrt(252):.4f} (page 2.3); unrounded {3.294/math.sqrt(500)*math.sqrt(252):.4f}")
# the exact-normal shortcut: P(Z - Q19 + delta > 0) check at delta = 3.294 with exact law of Q19
pi_exact = integrate.quad(lambda q: f(q) * stats.norm.sf(q - 3.294 * 0 - 0) * 0 + f(q) * stats.norm.cdf(3.294 + 0 * q), -12, 12, limit=500)[0]
print(f"P(Z + delta > Q19) with the exact law of Q19 at delta=3.294: {integrate.quad(lambda q: f(q) * stats.norm.sf(q - 3.294), -12, 12, limit=500)[0]:.6f} (page's approximation claims 0.9)")

# (2) Lab 2's pbo, copied from the twin (tests/labs/S7/lab-S7-L08-2.py)
src = (root / "tests/labs/S7/lab-S7-L08-2.py").read_text(encoding="utf-8")
head = src.split("# SIMULATED daily returns")[0]
ns: dict = {}
exec(compile(head, "lab-S7-L08-2-head", "exec"), ns)
pbo = ns["pbo"]

# (3) drift sweep over 0.0010..0.0020 step 0.00025, 1000 days, 20 configurations, 10 blocks, seed 20261101
drifts = [0.0010, 0.00125, 0.0015, 0.00175, 0.0020]
rng = np.random.default_rng(20261101)
t0 = time.time()
res = {}
for dr in drifts:
    vals = []
    for _ in range(reps):
        mm = rng.standard_normal((1000, 20)) * 0.01
        mm[:, 0] += dr
        vals.append(pbo(mm, 10))
    v = np.array(vals)
    res[dr] = v
    print(f"drift {dr:.5f} (daily Sharpe {dr/0.01:.3f}): mean PBO {v.mean():.4f} (se {v.std(ddof=1)/math.sqrt(reps):.4f}), reps {reps}", flush=True)
print(f"elapsed {time.time()-t0:.1f}s")

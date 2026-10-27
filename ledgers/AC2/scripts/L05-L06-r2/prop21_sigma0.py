"""Prop 2.1 identity check (verifier-written): with sigma = 0, S_t equals beta * (zbar_L - zbar_H) exactly.
Run: <checkout>/.venv/bin/python -I ledgers/AC2/scripts/L05-L06-r2/prop21_sigma0.py
"""
import numpy as np

rng = np.random.default_rng(3)
N, Q = 500, 100
errs = []
for _ in range(120):
    z = rng.standard_normal(N)
    a, b = 0.005, -0.0008
    r = a + b * z  # sigma = 0: no noise
    o = np.argsort(z, kind="stable")
    lo, hi = o[:Q], o[-Q:]
    S = r[lo].mean() - r[hi].mean()
    errs.append(abs(S - b * (z[lo].mean() - z[hi].mean())))
print("max |S - beta*(zbar_L - zbar_H)| with sigma=0:", max(errs))

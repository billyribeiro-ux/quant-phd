"""Round 29: card S7-c235 claim: at SR = 0 a finite variance suffices for asymptotic normality of sqrt(T) SR-hat; with
a finite variance the t-test at the nominal level rejects at about 5%. Re-run of the finite-variance simulation: iid
Student-t returns with mean zero, T = 2000, 20000 replications, seed 235 (as the release evidence). Prints the two-sided
rejection rate at 1.96 and the sd of sqrt(T) SR-hat for df 2.5 (finite variance, infinite fourth moment), 3, 8.
Run: .venv/bin/python -I ledgers/S7/scripts/data-tooling-r29-A/c235_finite_variance.py
"""

from __future__ import annotations

import numpy as np

rng = np.random.default_rng(235)
T, R = 2000, 20000
for df in (2.5, 3.0, 8.0):
    x = rng.standard_t(df, size=(R, T))
    mu = x.mean(axis=1)
    sd = x.std(axis=1, ddof=1)
    sr = mu / sd  # SR-hat with mean zero true SR: sqrt(T) SR-hat = sqrt(T) mu / sigma-hat
    z = np.sqrt(T) * sr
    print(f"df={df}: P(|sqrt(T) SR-hat| > 1.96) = {np.mean(np.abs(z) > 1.96):.4f}; sd = {z.std():.4f}")

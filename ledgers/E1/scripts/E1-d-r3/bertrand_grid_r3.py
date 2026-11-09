"""Grid check of Proposition 3: pure profiles on a grid, deviations on a 1/64 grid over [0, a/b]."""

from __future__ import annotations

import numpy as np

a, b, c = 40, 1, 10
dev = np.arange(0, 40 * 64 + 1) / 64.0  # deviation fees, 1/64 steps over [0, a/b]
demand = a - b * dev


def payoff(own: float, rival: float) -> np.ndarray:
    """Profit of an exchange charging each dev fee against a rival at fee `rival`."""
    share = np.where(dev < rival, 1.0, np.where(dev == rival, 0.5, 0.0))
    return (dev - c) * demand * share


profiles = np.arange(0, 40 * 2 + 1) / 2.0  # profile fees on a half grid over [0, a/b]
eq = []
for f1 in profiles:
    for f2 in profiles:
        # exchange 1 payoff at its own fee f1 against f2; exchange 2 symmetric
        own1 = (f1 - c) * (a - b * f1) * (1.0 if f1 < f2 else 0.5 if f1 == f2 else 0.0)
        own2 = (f2 - c) * (a - b * f2) * (1.0 if f2 < f1 else 0.5 if f2 == f1 else 0.0)
        best1 = payoff(f1, f2).max()
        best2 = np.where(dev < f1, 1.0, np.where(dev == f1, 0.5, 0.0))
        best2 = ((dev - c) * demand * best2).max()
        if best1 <= own1 + 1e-9 and best2 <= own2 + 1e-9:
            eq.append((f1, f2))
print("half-grid profiles (fees 0..40, step 1/2):", len(profiles) ** 2)
print("grid equilibria (deviation grid 1/64):", eq)

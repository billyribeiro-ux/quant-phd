"""Check when the three shapes of L08 Definition 3.1 can be normalized (curvature shape nonzero).

Follows L08 Section 3 exactly: iota, centred tenors, centred squared tenors orthogonalized against the first two.
Run: python -I -W error ledgers/M3/scripts/M3-c-r7/l08_definition31_degenerate.py
"""
import numpy as np


def curvature_norm(tenors):
    t = np.asarray(tenors, dtype=float)
    n = t.size
    level = np.ones(n) / np.sqrt(n)
    slope_raw = t - t.mean()
    slope = slope_raw / np.linalg.norm(slope_raw) if np.linalg.norm(slope_raw) > 0 else None
    quad = t ** 2 - (t ** 2).mean()
    quad = quad - (quad @ level) * level
    if slope is not None:
        quad = quad - (quad @ slope) * slope
    return float(np.linalg.norm(quad))


for tenors in ([1.0, 2.0], [1.0, 1.0, 2.0], [1.0, 2.0, 3.0], [0.25, 0.5, 1.0, 2.0, 5.0, 10.0]):
    print(f"tenors {tenors}: norm of unnormalized curvature shape = {curvature_norm(tenors):.6g}")

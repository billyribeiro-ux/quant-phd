"""Witness for the is_psd boundary survivor (r3d_m01) and the equivalence check for r3d_m05 over seeds 0-49.

Run from the scratch copy of the reference: python -I survivor_witness.py <dir-with-covariance_doctor-and-instance>
"""

import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
sys.dont_write_bytecode = True
import instance  # noqa: E402
import covariance_doctor as ref  # noqa: E402

spec = importlib.util.spec_from_file_location("m01", sys.argv[2])
m01 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m01)
a = [[-0.5, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
print("witness diag(-0.5,1,1) tol=0.5: reference", ref.is_psd(a, tol=0.5), "| strict mutant", m01.is_psd(a, tol=0.5))
worst = 0.0
worst_offdiag = 0.0
for seed in range(50):
    inst = instance.make_instance(seed)
    n = inst["k"]
    x = ref.projection_repair(inst["corr"])
    # r3d_m05 returns the last PSD iterate y; recompute y from the same loop to measure its diagonal deviation
    a0 = ref._as_matrix(inst["corr"])
    xx = a0
    cs = [[0.0] * n for _ in range(n)]
    cu = [[0.0] * n for _ in range(n)]
    for _ in range(500):
        y = ref._psd_projection([[xx[i][j] + cs[i][j] for j in range(n)] for i in range(n)])
        cs = [[xx[i][j] + cs[i][j] - y[i][j] for j in range(n)] for i in range(n)]
        nx = [[y[i][j] + cu[i][j] for j in range(n)] for i in range(n)]
        for i in range(n):
            nx[i][i] = 1.0
        cu = [[y[i][j] + cu[i][j] - nx[i][j] for j in range(n)] for i in range(n)]
        gap = ref._frobenius(nx, y)
        step = ref._frobenius(nx, xx)
        xx = nx
        if gap <= 1e-10 and step <= 1e-10:
            break
    worst = max(worst, max(abs(y[i][i] - 1.0) for i in range(n)))
    worst_offdiag = max(worst_offdiag, max(abs(y[i][j] - x[i][j]) for i in range(n) for j in range(n)))
print("r3d_m05 over seeds 0-49: largest |y_ii - 1| =", f"{worst:.3e}", "| largest |y - reference| entry =", f"{worst_offdiag:.3e}")

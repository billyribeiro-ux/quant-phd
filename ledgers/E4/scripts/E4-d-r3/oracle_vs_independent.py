"""Compare the grader oracle (test_project.py) and the reference solver against the verifier's independent model on the
grader's instances (seeds 0-49, and the second instance of each seed), and the boundary-rule sign on a dense box grid.

Usage: .venv/bin/python -I ledgers/E4/scripts/E4-d-r3/oracle_vs_independent.py <repo-root>
The grader and reference are loaded from a scratch copy so that nothing in the repository is written.
"""

import importlib.util
import math
import os
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

root = Path(sys.argv[1])
here = Path(__file__).resolve().parent
sys.path.insert(0, str(here))
import indep_model as im  # noqa: E402

grader = root / "course/modules/E/E4/grader"
work = Path(tempfile.mkdtemp(prefix="e4d3-oracle-"))
shutil.copy(grader / "test_project.py", work / "test_project.py")
shutil.copy(grader / "instance.py", work / "instance.py")
shutil.copy(grader / "reference.py", work / "solver.py")
sys.path.insert(0, str(work))
os.environ["QF_SEED"] = "0"
spec = importlib.util.spec_from_file_location("tp", work / "test_project.py")
tp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tp)
import solver  # noqa: E402
from instance import make_instance  # noqa: E402

max_oracle_gap_err = 0.0
max_ref_gap_err = 0.0
max_ref_lam_err = 0.0
max_oracle_root_err = 0.0
max_oracle_info_err = 0.0
n = 0
for seed in range(50):
    for s_ in (seed, seed + 7919):
        inst = make_instance(s_)
        sd, c = inst["noise_sd"], inst["info_cost"]
        out = solver.solve_model(sd, c)
        lam = out["informed_fraction"]
        ind_gap, ind_info, _, _ = im.gap_and_info(lam, sd, c) if 0 < lam < 1 else (None, None, None, None)
        if lam == 0.0:
            ind_gap = im.gap_at_small(sd, c)
            ind_info = 0.0
        elif lam == 1.0:
            ind_gap, ind_info, _, _ = im.gap_and_info(1.0, sd, c)
        ind_root = im.closed_root(sd, c)
        max_ref_lam_err = max(max_ref_lam_err, abs(lam - ind_root))
        max_ref_gap_err = max(max_ref_gap_err, abs(out["indifference_gap"] - ind_gap))
        max_oracle_gap_err = max(max_oracle_gap_err, abs(tp.oracle_gap(lam, sd, c) - ind_gap))
        max_oracle_root_err = max(max_oracle_root_err, abs(tp.oracle_root(sd, c) - ind_root))
        if 0 < lam < 1:
            max_oracle_info_err = max(max_oracle_info_err, abs(tp.oracle_informativeness(lam, sd) - ind_info))
        n += 1
print(f"instances compared: {n}")
print(f"reference lam vs independent root, max abs error: {max_ref_lam_err:.3e}")
print(f"reference gap vs independent gap, max abs error: {max_ref_gap_err:.3e}")
print(f"oracle gap at reference lam vs independent gap, max abs error: {max_oracle_gap_err:.3e}")
print(f"oracle root vs independent root, max abs error: {max_oracle_root_err:.3e}")
print(f"oracle informativeness vs independent (interior), max abs error: {max_oracle_info_err:.3e}")
# dense box grid: interior condition gap(0+) > 0 and gap(1) < 0 at every point (11 x 11 grid, corners included)
bad = 0
pts = 0
for sd in np.linspace(0.5, 0.75, 11):
    for c in np.linspace(0.12, 0.15, 11):
        pts += 1
        g0 = im.gap_at_small(sd, c)
        g1, _, _, _ = im.gap_and_info(1.0, sd, c)
        if not (g0 > 0 and g1 < 0):
            bad += 1
print(f"box grid 11x11: points {pts}, interior condition violated at {bad}")
shutil.rmtree(work, ignore_errors=True)

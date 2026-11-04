"""Round-8 verifier (M3 slice d): validity and diversity of grader instances, seeds 0-49 (sample of 20 reported).

Checks, per seed: k in {3,4,5}; vols in [0.05, 0.40]; corr symmetric, unit diagonal, off-diagonal in [-0.95, 0.95],
smallest eigenvalue (numpy) below -0.02; psd_corr symmetric unit diagonal positive definite; psd_spectrum[0] == 0 and
the others in [0, 2]; spectrum in [-0.6, 1.4]; eigenvectors orthonormal. Across seeds 0-49: the answers (smallest
eigenvalue of corr, comparison_weights of psd_corr) differ between seeds.
Run from the checkout root: .venv/bin/python -I ledgers/M3/scripts/M3-d-r8/instance_check_r8.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path.cwd() / "course/modules/M/M3/grader"))
from instance import make_instance  # noqa: E402

bad = []
answers = []
for seed in range(50):
    inst = make_instance(seed)
    k = inst["k"]
    corr = np.array(inst["corr"])
    psd = np.array(inst["psd_corr"])
    ev = np.array(inst["eigenvectors"])
    if k not in (3, 4, 5):
        bad.append((seed, "k")) 
    if not all(0.05 <= v <= 0.40 for v in inst["vols"]):
        bad.append((seed, "vols"))
    if not np.allclose(corr, corr.T, atol=0) or not np.allclose(np.diag(corr), 1):
        bad.append((seed, "corr sym/diag"))
    off = corr[np.triu_indices(k, 1)]
    if not (np.all(off >= -0.95) and np.all(off <= 0.95)):
        bad.append((seed, "corr range"))
    if not np.linalg.eigvalsh(corr)[0] < -0.02:
        bad.append((seed, "corr not non-PSD by 0.02"))
    if not (np.allclose(psd, psd.T) and np.allclose(np.diag(psd), 1) and np.linalg.eigvalsh(psd)[0] > 0):
        bad.append((seed, "psd_corr not PD unit"))
    ps = inst["psd_spectrum"]
    if ps[0] != 0.0 or not all(0.0 <= s <= 2.0 for s in ps[1:]):
        bad.append((seed, "psd_spectrum"))
    if not all(-0.6 <= s <= 1.4 for s in inst["spectrum"]):
        bad.append((seed, "spectrum range"))
    if not np.allclose(ev @ ev.T, np.eye(k), atol=1e-9):
        bad.append((seed, "eigenvectors not orthonormal"))
    w = np.linalg.solve(np.diag(inst["vols"]) @ psd @ np.diag(inst["vols"]), np.ones(k))
    w = w / w.sum()
    answers.append((seed, k, round(float(np.linalg.eigvalsh(corr)[0]), 6), tuple(round(float(x), 6) for x in w)))
print("instances checked: 50; problems:", bad if bad else "none")
print("first 20 seeds (seed, k, min eig of corr, weights of psd_corr):")
for row in answers[:20]:
    print("  ", row)
print("distinct min-eig values over seeds 0-49:", len({r[2] for r in answers}))
print("distinct weight vectors over seeds 0-49:", len({r[3] for r in answers}))
print("distinct k over seeds 0-49:", sorted({r[1] for r in answers}))

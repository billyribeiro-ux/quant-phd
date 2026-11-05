"""Round-11 verifier: check grader instances for seeds 0-19 against the contract in project.html, and that the planted
eigenvalue lists give distinct minimum eigenvalues. Run from the checkout root with the grader directory on sys.path."""

import sys
from pathlib import Path

import numpy as np

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "course/modules/M/M3/grader"))
from instance import make_instance  # noqa: E402

mins = []
weights = []
for seed in range(20):
    inst = make_instance(seed)
    k = inst["k"]
    assert k in (3, 4, 5)
    c = np.array(inst["corr"])
    assert np.allclose(np.diag(c), 1.0) and np.allclose(c, c.T)
    assert np.max(np.abs(c[~np.eye(k, dtype=bool)])) <= 0.95
    assert np.linalg.eigvalsh(c)[0] < -0.02, seed
    p = np.array(inst["psd_corr"])
    assert np.allclose(np.diag(p), 1.0) and np.linalg.eigvalsh(p)[0] > 0
    assert len(inst["vols"]) == k and all(0.05 <= v <= 0.40 for v in inst["vols"])
    assert inst["psd_spectrum"][0] == 0.0
    v = np.array(inst["eigenvectors"])
    assert np.max(np.abs(v @ v.T - np.eye(k))) < 1e-10
    mins.append(float(np.linalg.eigvalsh(np.array(inst["corr"]))[0]))
    w = np.linalg.solve(np.diag(inst["vols"]) @ p @ np.diag(inst["vols"]), np.ones(k))
    weights.append(tuple(np.round(w / w.sum(), 9)))
print("seeds 0-19: all instance checks passed")
print("min eigenvalues of corr distinct across seeds:", len(set(np.round(mins, 12))) == 20)
print("weight vectors distinct across seeds:", len(set(weights)) == 20)

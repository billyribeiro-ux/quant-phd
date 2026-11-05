"""Round-10 verifier (M3 slice d): sample 20 seeds of grader/instance.py, check every instance's contract with NumPy,
and check that the answers differ across seeds (not only the labels). Run: python -I <this file> from the checkout root."""

import sys

import numpy as np

sys.path.insert(0, "course/modules/M/M3/grader")
from instance import make_instance  # noqa: E402

ok = True
mins, weights_rows = [], []
for seed in list(range(20)):
    inst = make_instance(seed)
    k = inst["k"]
    corr = np.array(inst["corr"])
    psd = np.array(inst["psd_corr"])
    v = np.array(inst["vols"])
    problems = []
    if k not in (3, 4, 5):
        problems.append("k")
    if not np.allclose(corr, corr.T, atol=0, rtol=0):
        problems.append("corr symmetric")
    if not np.all(np.diag(corr) == 1.0):
        problems.append("corr unit diagonal")
    off = corr[~np.eye(k, dtype=bool)]
    if np.any(np.abs(off) > 0.95):
        problems.append("corr range")
    lam = float(np.linalg.eigvalsh(corr)[0])
    if not lam < -0.02:
        problems.append(f"corr not non-PSD by margin 0.02 (min eig {lam:.6f})")
    if not (np.allclose(psd, psd.T, atol=1e-12) and np.allclose(np.diag(psd), 1.0, atol=1e-12)):
        problems.append("psd_corr symmetric unit diagonal")
    if not np.linalg.eigvalsh(psd)[0] > 0:
        problems.append("psd_corr positive definite")
    if not (np.all(v >= 0.05) and np.all(v <= 0.40) and len(v) == k):
        problems.append("vols")
    if len(inst["spectrum"]) != k or len(inst["psd_spectrum"]) != k or inst["psd_spectrum"][0] != 0.0:
        problems.append("spectra")
    E = np.array(inst["eigenvectors"])
    if E.shape != (k, k) or np.max(np.abs(E @ E.T - np.eye(k))) > 1e-9:
        problems.append("eigenvectors orthonormal")
    if inst["label"] != "SIMULATED":
        problems.append("label")
    sigma = np.diag(v) @ psd @ np.diag(v)
    w = np.linalg.solve(sigma, np.ones(k))
    w = w / w.sum()
    mins.append(round(lam, 6))
    weights_rows.append(tuple(round(float(x), 4) for x in w))
    status = "OK" if not problems else "PROBLEMS: " + ", ".join(problems)
    ok = ok and not problems
    print(f"seed {seed:2d} k={k} min_eig(corr)={lam:+.6f} |psd_corr min eig|={np.linalg.eigvalsh(psd)[0]:.4f} {status}")
print("instances valid:", ok)
print("distinct k values:", sorted({make_instance(s)["k"] for s in range(20)}))
print("distinct min eigenvalues of corr across 20 seeds:", len(set(mins)))
print("distinct weight vectors (NumPy, psd_corr with vols) across 20 seeds:", len(set(weights_rows)))

"""Round-5 verifier: sample instance.make_instance over seeds 0-199 and check the contract stated on project.html."""
import sys
import numpy as np
sys.path.insert(0, "/private/tmp/verifyD5-M3-d-ws")
from instance import make_instance

bad = []
mins = []
for seed in range(200):
    d = make_instance(seed)
    k = d["k"]
    corr = np.array(d["corr"])
    assert k in (3, 4, 5)
    if not (len(d["vols"]) == k and all(0.05 <= v <= 0.40 for v in d["vols"])):
        bad.append((seed, "vols"))
    if not (np.allclose(corr, corr.T, atol=0) and np.allclose(np.diag(corr), 1.0)):
        bad.append((seed, "corr shape"))
    lam = float(np.linalg.eigvalsh(corr)[0])
    mins.append(lam)
    if not lam < -0.02:
        bad.append((seed, "corr margin", lam))
    p = np.array(d["psd_corr"])
    if not (np.allclose(np.diag(p), 1.0) and np.linalg.eigvalsh(p)[0] > 0 and np.allclose(p, p.T)):
        bad.append((seed, "psd_corr"))
    ev = np.array(d["eigenvectors"])
    if not np.allclose(ev @ ev.T, np.eye(k), atol=1e-9):
        bad.append((seed, "eigvec orthonormal"))
    if d["psd_spectrum"][0] != 0.0:
        bad.append((seed, "psd_spectrum first"))
print("seeds 0-199, problems:", bad[:10], "count", len(bad))
print("min eig of corr: max over seeds = %.6f, min over seeds = %.6f" % (max(mins), min(mins)))

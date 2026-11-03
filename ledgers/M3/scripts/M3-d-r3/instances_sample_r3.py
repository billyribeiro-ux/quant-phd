"""Sample 20 seeded instances (verifier round 3): validity against the page's contract and that the answers differ.

Validity: square, symmetric, unit diagonal, corr not PSD by a margin of 0.02 (independent eigenvalues from numpy),
psd_corr positive definite with unit diagonal, volatilities strictly positive, k in {3,4,5}, psd_spectrum has a zero.
Answers: the clip and projection distances from corr, computed by numpy for each seed, to show the answers change.
Run from the checkout root with -I (numpy is the oracle only).
"""

import sys

import numpy as np

sys.path.insert(0, "course/modules/M/M3/grader")
from instance import make_instance  # noqa: E402

rows = []
for seed in range(20):
    inst = make_instance(seed)
    c = np.array(inst["corr"])
    k = inst["k"]
    ok = (
        k in (3, 4, 5)
        and np.allclose(c, c.T, atol=0)
        and np.allclose(np.diag(c), 1.0)
        and np.linalg.eigvalsh(c).min() < -0.02
        and np.linalg.eigvalsh(np.array(inst["psd_corr"])).min() > 0
        and np.allclose(np.diag(inst["psd_corr"]), 1.0)
        and all(v > 0 for v in inst["vols"])
        and inst["psd_spectrum"][0] == 0.0
    )
    w, v = np.linalg.eigh(c)
    clip = (v * np.maximum(w, 0)) @ v.T
    d = np.sqrt(np.diag(clip))
    clip = clip / np.outer(d, d)
    rows.append((seed, k, ok, round(float(np.linalg.eigvalsh(c).min()), 6), round(float(np.linalg.norm(clip - c)), 6)))
for r in rows:
    print("seed %2d k=%d valid=%s min_eig(corr)=%.6f clip_distance=%.6f" % r)
print("all valid:", all(r[2] for r in rows), "| distinct clip distances:", len({r[4] for r in rows}))

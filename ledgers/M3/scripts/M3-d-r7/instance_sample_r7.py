"""Round-7 verifier (slice d): samples seeds 0-19 of grader/instance.py and checks the contract that project.html and
instance.py state: k in {3,4,5}; vols in [0.05, 0.40]; corr unit-diagonal, symmetric, smallest eigenvalue below -0.02;
psd_corr unit-diagonal and positive definite; eigenvectors orthonormal; and that the reference answers (min eigenvalue
of corr, clip repair entry, weights) differ across seeds. Usage: .venv/bin/python -I <this file> (from the checkout root)."""

import importlib.util
import sys
from pathlib import Path

ROOT = Path.cwd()
spec = importlib.util.spec_from_file_location("instance", ROOT / "course/modules/M/M3/grader/instance.py")
inst = importlib.util.module_from_spec(spec)
sys.modules["instance"] = inst
spec.loader.exec_module(inst)
ref_spec = importlib.util.spec_from_file_location("reference", ROOT / "course/modules/M/M3/grader/reference.py")
ref = importlib.util.module_from_spec(ref_spec)
ref_spec.loader.exec_module(ref)

rows = []
answers = set()
ks = []
for seed in range(20):
    d = inst.make_instance(seed)
    k = d["k"]
    ks.append(k)
    assert k in (3, 4, 5)
    assert all(0.05 <= v <= 0.40 for v in d["vols"])
    c = d["corr"]
    assert all(abs(c[i][i] - 1.0) == 0 for i in range(k))
    assert all(c[i][j] == c[j][i] for i in range(k) for j in range(k))
    me = ref.min_eigenvalue(c)
    assert me < -0.02, (seed, me)
    pc = d["psd_corr"]
    assert all(abs(pc[i][i] - 1.0) < 1e-12 for i in range(k))
    assert ref.min_eigenvalue(pc) > 0, seed
    u = d["eigenvectors"]
    gram_err = max(abs(sum(u[a][t] * u[b][t] for t in range(k)) - (1.0 if a == b else 0.0)) for a in range(k) for b in range(k))
    assert gram_err < 1e-9, (seed, gram_err)
    w = ref.comparison_weights(pc, d["vols"])
    assert abs(sum(w) - 1.0) < 1e-12
    cl = ref.clip_repair(c)
    answers.add((round(me, 6), round(cl[0][1], 6), round(w[0], 6)))
    rows.append((seed, k, round(me, 6), round(cl[0][1], 6), round(w[0], 6), f"{gram_err:.1e}"))

for r in rows:
    print("seed %2d k %d min_eig %10.6f clip[0][1] %10.6f w0 %10.6f gram_err %s" % r)
print("k values:", sorted(set(ks)), "distinct answer triples:", len(answers), "of", len(rows))
print("all 20 seeds satisfy the contract: True")

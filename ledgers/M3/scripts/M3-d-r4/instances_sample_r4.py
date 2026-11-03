"""Round-4 verifier: sample 20 seeds, check every instance is valid under the page's contract, and that the reference
answers differ materially across the sample. Usage (from the checkout root):
    .venv/bin/python -I ledgers/M3/scripts/M3-d-r4/instances_sample_r4.py
"""

import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "course/modules/M/M3/grader"))
import instance  # noqa: E402
import reference as ref  # noqa: E402

SEEDS = [0, 1, 2, 3, 5, 8, 13, 21, 34, 4, 7, 11, 17, 19, 23, 29, 31, 37, 41, 49]
answers = []
problems = []
for s in SEEDS:
    d = instance.make_instance(s)
    k = d["k"]
    if k not in (3, 4, 5) or len(d["vols"]) != k or any(not (0.05 <= v <= 0.40) for v in d["vols"]):
        problems.append((s, "k or vols out of range"))
    if not (ref.min_eigenvalue(d["corr"]) < -0.02):
        problems.append((s, "corr not non-PSD by margin 0.02"))
    if any(abs(d["corr"][i][i] - 1.0) > 1e-12 or abs(d["psd_corr"][i][i] - 1.0) > 1e-9 for i in range(k)):
        problems.append((s, "unit diagonal violated"))
    if ref.min_eigenvalue(d["psd_corr"]) <= 0:
        problems.append((s, "psd_corr not positive definite"))
    if abs(d["psd_spectrum"][0]) != 0.0:
        problems.append((s, "psd_spectrum first entry not 0"))
    for a in range(k):
        for b in range(k):
            dot = sum(x * y for x, y in zip(d["eigenvectors"][a], d["eigenvectors"][b], strict=True))
            if abs(dot - (1.0 if a == b else 0.0)) > 1e-9:
                problems.append((s, "eigenvectors not orthonormal"))
    w = ref.comparison_weights(d["psd_corr"], d["vols"])
    answers.append((s, k, round(ref.min_eigenvalue(d["corr"]), 6), round(sum(w), 9), [round(x, 4) for x in w]))
for row in answers:
    print("seed", row[0], "k", row[1], "min_eig(corr)", row[2], "sum(weights)", row[3], "weights", row[4])
print("distinct corr matrices:", len({tuple(map(tuple, instance.make_instance(s)["corr"])) for s in SEEDS}))
print("distinct weight vectors:", len({tuple(a[4]) for a in answers}))
print("seeds sampled:", len(SEEDS), "| seeds whose corr is non-PSD by the margin:", sum(1 for s in SEEDS if ref.min_eigenvalue(instance.make_instance(s)["corr"]) < -0.02))
print("problems:", problems if problems else "none")

"""Scan the SC1 statistical tolerances against the reference over seeds 0-2999 (stdlib + the grader's own modules).

Usage: python scan_bands_r3.py <repo-root>
Prints the number of seeds where the reference fails (a) the one-step band with the sample standard error (as in
test_project.py), (b) the one-step band with the target's standard error, (c) the coarse-1 band with the sample
standard error (as in test_project.py), (d) the same with the target's standard error.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / "course/modules/SC/SC1/grader"))
import reference as ref  # noqa: E402
from instance import make_instance  # noqa: E402

one_sample, one_target, coarse_sample, coarse_target = [], [], [], []
for s in range(3000):
    for inst in (make_instance(s), make_instance(s + 7919)):
        est, se = ref.discrete_max_exceedance(inst, 1)
        t = ref.reflection_tail(inst["a"], inst["H"]) / 2.0
        if not abs(est - t) <= 5 * se + 1 / inst["n_paths"]:
            one_sample.append((s, inst["seed"]))
        se_t = math.sqrt(t * (1 - t) / inst["n_paths"])
        if not abs(est - t) <= 5 * se_t + 1 / inst["n_paths"]:
            one_target.append((s, inst["seed"]))
    inst = make_instance(s)
    _, coarse = ref.nested_grid_counts(inst, 8, 1)
    est = coarse / inst["n_paths"]
    t = ref.reflection_tail(inst["a"], inst["H"]) / 2.0
    se = math.sqrt(est * (1 - est) / (inst["n_paths"] - 1))
    if not abs(est - t) <= 5 * se + 1 / inst["n_paths"]:
        coarse_sample.append(s)
    se_t = math.sqrt(t * (1 - t) / inst["n_paths"])
    if not abs(est - t) <= 5 * se_t + 1 / inst["n_paths"]:
        coarse_target.append(s)

print(f"(a) one-step, sample SE, as in test_project.py: {len(one_sample)} of 6000 instances fail; seeds (student, instance) {one_sample[:8]}")
print(f"(b) one-step, target SE: {len(one_target)} of 6000 instances fail")
print(f"(c) coarse-1 (n_fine 8), sample SE, as in test_project.py: {len(coarse_sample)} of 3000 student seeds fail; seeds {coarse_sample[:8]}")
print(f"(d) coarse-1, target SE: {len(coarse_target)} of 3000 student seeds fail")

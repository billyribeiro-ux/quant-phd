"""Compare the reference gap at 0 and at 1e-12 with the grader's oracle gap at 0, over seeds 0-49 and a wider box.

Run: python3 -I measure_oracle_gap0_r9.py <scratch-dir-with-solver.py-instance.py-test_project.py>
"""
import sys
from pathlib import Path

scratch = Path(sys.argv[1])
sys.path.insert(0, str(scratch))
import importlib  # noqa: E402

sol = importlib.import_module("solver")
inst_mod = importlib.import_module("instance")
tp = importlib.import_module("test_project")  # oracle functions; solver is loaded from scratch/solver.py

worst_oracle = 0.0
worst_g1e12 = 0.0
for seed in range(50):
    inst = inst_mod.make_instance(seed)
    sd, c = inst["noise_sd"], inst["info_cost"]
    worst_oracle = max(worst_oracle, abs(sol.gap_at_zero(sd, c) - tp.oracle_gap(0.0, sd, c)))
    worst_g1e12 = max(worst_g1e12, abs(sol.indifference_gap(1e-12, sd, c) - sol.gap_at_zero(sd, c)))
print(f"seeds 0-49: max |reference gap_at_zero - oracle_gap(0)| = {worst_oracle:.3e}")
print(f"seeds 0-49: max |G(1e-12) - G(0)| = {worst_g1e12:.3e}")
wide = 0.0
for sd in [0.01, 0.1, 0.5, 0.75, 1.0, 3.0, 10.0]:
    for c in [0.0, 0.05, 0.12, 0.15, 0.3, 1.0]:
        wide = max(wide, abs(sol.indifference_gap(1e-12, sd, c) - sol.gap_at_zero(sd, c)))
print(f"wider grid: max |G(1e-12) - G(0)| = {wide:.3e}")

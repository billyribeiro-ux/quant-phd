"""Round 16 check of the equivalence claims in ledgers/E4/equivalent/README.md.

(a) literal_price_sign.py: outputs of solve_model equal the reference's bit-for-bit on random inputs.
(b) stop-rule / midpoint variants (ruling 17): reported fraction within 1e-10 * root of the reference's root,
    and the gap and informativeness identical to the reference at the same fraction tolerance.
Usage: python -I equiv_check_r16.py <checkout-root>
"""
import importlib.util
import math
import random
import sys
from pathlib import Path

root = Path(sys.argv[1])


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(root / "course/modules/E/E4/grader/reference.py", "ref")
lit = load(root / "ledgers/E4/equivalent/literal_price_sign.py", "lit")
rng = random.Random(16)
cases = [(rng.uniform(0.05, 3.0), rng.uniform(0.0, 0.4)) for _ in range(3000)]
cases += [(rng.uniform(0.5, 0.75), rng.uniform(0.12, 0.15)) for _ in range(1000)]
max_abs = 0.0
mismatch = 0
for sd, c in cases:
    a, b = ref.solve_model(sd, c), lit.solve_model(sd, c)
    for k in a:
        if a[k] != b[k]:
            mismatch += 1
        max_abs = max(max_abs, abs(a[k] - b[k]))
print(f"(a) literal_price_sign: {len(cases)} cases, bitwise mismatches={mismatch}, max abs diff={max_abs:.3e}")

for name in ["mutant_r6_08_reports_lower_end.py", "mutant_r7_01_reports_bracket_lower_end.py",
             "mutant_v9_02_stop_rule_relative_to_lower_end.py"]:
    m = load(root / "ledgers/E4/equivalent" / name, name.replace(".py", ""))
    worst = 0.0
    worst_gap = 0.0
    n_interior = 0
    for sd, c in cases[:3000:3] + [(1e-50, 0.1707691121), (1e-12, 0.13), (1e-40, 0.13), (0.6, 0.13)]:
        a, b = ref.solve_model(sd, c), m.solve_model(sd, c)
        lam = a["informed_fraction"]
        if 0.0 < lam < 1.0:
            n_interior += 1
            worst = max(worst, abs(a["informed_fraction"] - b["informed_fraction"]) / lam)
        worst_gap = max(worst_gap, abs(a["indifference_gap"] - b["indifference_gap"]))
    print(f"(b) {name}: interior cases={n_interior}, max |dlam|/lam={worst:.3e} (ruling 17 needs <= 1e-10), "
          f"max |dgap|={worst_gap:.3e}")

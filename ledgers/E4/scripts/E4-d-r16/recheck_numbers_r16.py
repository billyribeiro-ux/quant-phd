"""Round 16 re-derivation of the numeric claims in E4 project.html and test_project.py docstrings.

Loads grader/reference.py as solver and the suite's own oracles (test_project.py) from a scratch copy, so
the oracle values are the suite's, not recomputed by the reference. Prints each claim with the computed value.
Usage: python -I recheck_numbers_r16.py <checkout-root> <scratch-dir>
"""
import importlib
import math
import shutil
import sys
from pathlib import Path

root, scratch = Path(sys.argv[1]), Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
g = root / "course/modules/E/E4/grader"
shutil.copy(g / "test_project.py", scratch / "test_project.py")
shutil.copy(g / "instance.py", scratch / "instance.py")
shutil.copy(g / "reference.py", scratch / "solver.py")
sys.path.insert(0, str(scratch))
import os  # noqa: E402

os.environ["QF_SEED"] = "0"
tp = importlib.import_module("test_project")
ref = importlib.import_module("solver")

print("tau-bar(0.150) =", f"{2 * math.exp(-0.6) - 1:.10f}", " tau-bar(0.120) =", f"{2 * math.exp(-0.48) - 1:.10f}")
print("1/(1+4*0.75^2) =", f"{1 / (1 + 4 * 0.75**2):.10f}")
print("2^-240 =", f"{2.0**-240:.4e}", " 2^-200 =", f"{2.0**-200:.4e}", " 2^-53 =", f"{2.0**-53:.4e}")
print("threshold root above which 240 halvings give 1e-12 relative width: 2^-240 * 1e12 =", f"{2.0**-240 * 1e12:.4e}")

# Claim (test_project.py 382-386): gap at fraction 1e-12 differs from the limit by 1e-13..4e-13 at the listed inputs,
# and the oracle agrees with the limit to at most 1.1e-16 there.
worst_oracle = 0.0
d_lo, d_hi = float("inf"), 0.0
for sd, cost in [(0.5, 0.30), (0.6, 0.30), (0.75, 0.30), (0.5, 0.50), (0.6, 0.50), (0.75, 0.50)]:
    limit = ref.gap_at_zero(sd, cost)
    near = ref.indifference_gap(1e-12, sd, cost)
    d = abs(near - limit)
    d_lo, d_hi = min(d_lo, d), max(d_hi, d)
    o = abs(tp.oracle_gap(0.0, sd, cost) - limit)
    worst_oracle = max(worst_oracle, o)
print(f"|gap(1e-12) - limit|: min {d_lo:.3e} max {d_hi:.3e} (claim: 1e-13 to 4e-13)")
print(f"|oracle(0) - reference limit|: max {worst_oracle:.3e} (claim: at most 1.1e-16)")

# Claim (test_project.py 565): sd=1e-50, cost=0.1707691121 gives tau-bar just above 1e-2 and a root about 2e-51.
sd, cost = 1e-50, 0.1707691121
tb = 2 * math.exp(-4 * cost) - 1
root = tp.closed_form_root(sd, cost)
print(f"corner: tau-bar = {tb:.6e}, closed-form root = {root:.6e}, reference root = {ref.solve_model(sd, cost)['informed_fraction']:.6e}")
# Claim (test_project.py 566): a 200-halving search leaves a bracket wider than 1e-10 times that root.
w200 = 2.0**-200
print(f"200-halving bracket width {w200:.3e} vs 1e-10*root {1e-10 * root:.3e}: wider = {w200 > 1e-10 * root}")
w240 = 2.0**-240
print(f"240-halving bracket width {w240:.3e} vs 1e-10*root {1e-10 * root:.3e}: ok = {w240 <= 1e-10 * root}")

# Claim (page exception table): finite outputs up to noise volume 1e150 and cost 350.
for sd, cost in [(1e150, 0.5), (0.5, 350.0), (1e150, 350.0), (1e-50, 0.5)]:
    try:
        out = ref.solve_model(sd, cost)
        print(f"range check sd={sd:g} c={cost:g}:", {k: v for k, v in out.items()}, "finite =", all(math.isfinite(v) for v in out.values()))
    except Exception as e:  # noqa: BLE001
        print(f"range check sd={sd:g} c={cost:g}: raised {type(e).__name__}: {e}")

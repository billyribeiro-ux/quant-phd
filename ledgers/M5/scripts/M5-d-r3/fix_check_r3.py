"""Round 3, slice d: does a candidate test change kill the three new survivors, and does the reference still pass?

Writes a patched COPY of test_project.py into a scratch directory (the repository is not edited) and runs the reference
and the three survivors on seeds 0-9 with the browser flags. Usage: python3 -I fix_check_r3.py <checkout-root> <scratch>.
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
scratch = Path(sys.argv[2]).resolve()
grader = root / "course/modules/M/M5/grader"
src = (grader / "test_project.py").read_text(encoding="utf-8")

# Fix A: the definition test and the contraction test also draw signed vectors (the page defines B for any V).
a_old = "        values = [rng.uniform(0.0, 3.0) for _ in grid]\n        got = sol.bellman_operator(p, grid, values)"
a_new = "        values = [rng.uniform(-3.0, 3.0) for _ in grid]\n        got = sol.bellman_operator(p, grid, values)"
assert src.count(a_old) == 1, src.count(a_old)
patched = src.replace(a_old, a_new)

# Fix B: a successor one ulp above the resources is refused (feasibility is exact).
b_anchor = "def test_saving_above_the_current_capital_is_feasible_within_resources() -> None:"
b_new = '''def test_successor_one_ulp_above_the_resources_is_infeasible() -> None:
    """Feasibility is exact: the successor one unit in the last place above k**alpha is infeasible."""
    __tracebackhide__ = True
    p = {"beta": 0.5, "alpha": 0.5}
    grid = [0.25, math.nextafter(0.5, 1.0)]
    got = sol.bellman_operator(p, grid, [0.0, 1.0e6])
    expect(close(float(got[0]), 0.5, 1e-12), "a successor one ulp above k**alpha is infeasible: no tie tolerance")


'''
assert patched.count(b_anchor) == 1
patched = patched.replace(b_anchor, b_new + b_anchor)
work = scratch / "patched"
work.mkdir(parents=True, exist_ok=True)
(work / "test_project.py").write_text(patched, encoding="utf-8")
shutil.copy(grader / "instance.py", work / "instance.py")

cands = {
    "reference": grader / "reference.py",
    "r3_01": root / "ledgers/M5/mutants/r3_01_operator_clamps_each_image_at_zero.py",
    "r3_02": root / "ledgers/M5/mutants/r3_02_continuation_uses_absolute_value.py",
    "r3_03": root / "ledgers/M5/mutants/r3_03_feasibility_tie_tolerance_of_1e-14.py",
}
for name, path in cands.items():
    shutil.copy(path, work / "contraction_solver.py")
    results = []
    for seed in range(10):
        r = subprocess.run(
            [str(root / ".venv/bin/python"), "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work, capture_output=True, text=True, check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            timeout=600,
        )
        last = re.findall(r"\d+ (?:passed|failed)[^\n]*", r.stdout)
        results.append(f"{seed}:{'P' if r.returncode == 0 else 'F'}")
    print(f"patched suite, {name}: " + " ".join(results))

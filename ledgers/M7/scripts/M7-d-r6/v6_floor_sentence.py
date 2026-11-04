"""Round 6 (M7-d): test the page's floor sentence (project.html, dual-residual paragraph) on learner answers.

Learner answer = the reference's exact multipliers, each inequality multiplier raised by delta (so all are positive when
the reference's are non-negative), with the dual residual reported WITHOUT the floor (-min multiplier), the reported
primal/stationarity/CS left as the reference's. Run for delta in {2e-9, 5e-10} and report which suite checks fail.
Usage: python -I v6_floor_sentence.py <delta>   (writes the answer into a scratch dir and runs the suite there)
"""

import os
import shutil
import subprocess
import sys
from fractions import Fraction

delta = float(sys.argv[1])
ROOT = "/Users/billyribeiro/.fanout/wt/verifyD6-M7-d"
G = os.path.join(ROOT, "course/modules/M/M7/grader")
D = f"/tmp/m7d-r6-floor-{sys.argv[1]}"
shutil.rmtree(D, ignore_errors=True)
os.makedirs(D)
for f in ("test_project.py", "instance.py"):
    shutil.copy(os.path.join(G, f), D)
src = open(os.path.join(G, "reference.py"), encoding="utf-8").read()
src += f'''

_DELTA = Fraction(repr({delta!r}))


def allocate(instance):  # noqa: F811  learner variant: raise every inequality multiplier, report dual unfloored
    problem = _parse(instance)
    sol = _solve(problem)
    for key in ("lower", "upper", "sector", "plus", "minus"):
        sol[key] = [v + _DELTA for v in sol[key]]
    sol["kappa"] = sol["kappa"] + _DELTA
    sol["kappa"] = sol["kappa"]
    base = _certificate(problem, sol)
    ineq = [*sol["lower"], *sol["upper"], *sol["sector"], *sol["plus"], *sol["minus"], sol["kappa"]]
    base["dual_residual"] = float(-min(ineq))
    multipliers = {{
        "budget": float(sol["budget"]),
        "lower": [float(v) for v in sol["lower"]],
        "upper": [float(v) for v in sol["upper"]],
        "sector": [float(v) for v in sol["sector"]],
        "turnover_plus": [float(v) for v in sol["plus"]],
        "turnover_minus": [float(v) for v in sol["minus"]],
        "turnover_total": float(sol["kappa"]),
    }}
    return {{"weights": [float(v) for v in sol["w"]], "multipliers": multipliers, "certificate": base}}
'''
open(os.path.join(D, "constrained_allocator.py"), "w", encoding="utf-8").write(src)
PY = os.path.join(ROOT, ".venv/bin/python")
for seed in (0, 1, 2):
    res = subprocess.run(
        [PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py",
         "-k", "agrees or residuals_are_within or complementary or dual or certificate"],
        cwd=D, capture_output=True, text=True, env={**os.environ, "QF_SEED": str(seed), "PYTHONDONTWRITEBYTECODE": "1"},
    )
    lines = [l for l in res.stdout.splitlines() if l.startswith("FAILED") or "passed" in l or "failed" in l]
    print(f"delta={delta!r} seed {seed}: {lines[-1] if lines else res.stdout[-300:]}")
    for l in lines[:-1]:
        print("   ", l)

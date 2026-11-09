"""Probe the two surviving round-2 mutants against the reference on the inputs the suite does not use (round 2)."""

import importlib.util
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(os.path.join(REPO, "course/modules/M/M5/grader/reference.py"), "ref")
m1 = load(os.path.join(REPO, "ledgers/M5/mutants/d3_01_feasibility_allows_a_tie_tolerance_of_1e-12.py"), "m1")
m2 = load(os.path.join(REPO, "ledgers/M5/mutants/d3_02_first_point_bound_checked_only_for_longer_grids.py"), "m2")
p = {"beta": 0.5, "alpha": 0.5}
g = [0.25, 0.5 + 5e-13]
print("tie-tolerance grid", g, "values [0,1e6]")
print("  reference bellman:", ref.bellman_operator(p, g, [0.0, 1.0e6]))
try:
    print("  mutant d3_01 bellman:", m1.bellman_operator(p, g, [0.0, 1.0e6]))
except ValueError as exc:
    print("  mutant d3_01 raises ValueError:", exc)
print("one-point grid [1.5]")
try:
    print("  reference:", ref.solve({"beta": 0.9, "alpha": 0.5}, [1.5], 1e-6, 5))
except ValueError as exc:
    print("  reference raises ValueError:", exc)
try:
    print("  mutant d3_02 solve:", m2.solve({"beta": 0.9, "alpha": 0.5}, [1.5], 1e-6, 5))
except ValueError as exc:
    print("  mutant d3_02 raises ValueError:", exc)

"""Accuracy of reference.py and of mutant_r12_04 against the Proposition 4 closed form where tau-bar is near 1 (inside the page's domain)."""
import importlib.util
import math

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

ref = load("course/modules/E/E4/grader/reference.py", "ref")
mut = load("ledgers/E4/mutants/mutant_r12_04_stops_when_midpoint_gap_is_tiny.py", "mut")

def closed(sd, c):
    t = 2.0 * math.exp(-4.0 * c) - 1.0
    if t <= 0:
        return 0.0
    if t >= 1.0 / (1.0 + 4.0 * sd * sd):
        return 1.0
    return 2.0 * sd * math.sqrt(t / (1.0 - t))

for sd, c in [(1.4306323575597607e-38, 3.5044039648594804e-05), (1e-50, 1e-6), (1e-50, 0.0), (1e-40, 1e-4), (1e-30, 0.0), (1e-12, 1e-3)]:
    ex = closed(sd, c)
    lr = ref.solve_model(sd, c)["informed_fraction"]
    lm = mut.solve_model(sd, c)["informed_fraction"]
    print(f"sd={sd:.3e} cost={c:.3e} closed={ex:.16e} reference_rel={abs(lr-ex)/ex:.2e} mutant_rel={abs(lm-ex)/ex:.2e}")

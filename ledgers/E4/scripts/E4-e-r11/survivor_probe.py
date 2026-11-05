"""Round 11: quantify the surviving mutant mutant_r10_02_cost_factor_relative_error against the reference solver.

Loads both modules by path, compares the interior gap and the solved informed fraction at a few instances, and prints
the largest relative differences. Run from the checkout root with -I."""
import importlib.util
import math

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

ref = load("course/modules/E/E4/grader/reference.py", "ref")
mut = load("ledgers/E4/mutants/mutant_r10_02_cost_factor_relative_error.py", "mut")
worst_gap = 0.0
worst_root = 0.0
for sd in (0.05, 0.3, 1.0, 3.0):
    for cost in (0.0, 0.1, 0.2, 0.4):
        for lam in (0.1, 0.5, 0.9):
            g_ref = ref.indifference_gap(lam, sd, cost)
            g_mut = mut.indifference_gap(lam, sd, cost)
            rel = abs(g_mut - g_ref) / max(1.0, abs(g_ref))
            worst_gap = max(worst_gap, rel)
        r_ref = ref.solve_model(sd, cost)["informed_fraction"]
        r_mut = mut.solve_model(sd, cost)["informed_fraction"]
        if 0.0 < r_ref < 1.0:
            worst_root = max(worst_root, abs(r_mut - r_ref) / r_ref)
print(f"largest relative gap difference at interior fractions: {worst_gap:.3e}")
print(f"largest relative root difference (interior roots): {worst_root:.3e}")

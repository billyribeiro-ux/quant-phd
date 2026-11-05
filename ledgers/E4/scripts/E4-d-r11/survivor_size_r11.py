"""Size of the surviving mutant's gap error at the reference's reported fraction, seeds 0-49, and the oracle's agreement.
Usage: python3 -I survivor_size_r11.py <root>"""
import importlib.util
import sys

root = sys.argv[1]
sys.path.insert(0, f"{root}/course/modules/E/E4/grader")
import instance  # noqa: E402


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(f"{root}/course/modules/E/E4/grader/reference.py", "ref")
mut = load(f"{root}/ledgers/E4/mutants/mutant_r10_02_cost_factor_relative_error.py", "mut")
worst = 0.0
worst_rel = 0.0
for seed in range(50):
    inst = instance.make_instance(seed)
    sd, c = float(inst["noise_sd"]), float(inst["info_cost"])
    out = ref.solve_model(sd, c)
    lam = out["informed_fraction"]
    if not (0.0 < lam < 1.0):
        continue
    g_ref = ref.indifference_gap(lam, sd, c)
    g_mut = mut.indifference_gap(lam, sd, c)
    worst = max(worst, abs(g_mut - g_ref))
    worst_rel = max(worst_rel, abs(g_mut - g_ref) / max(1.0, abs(g_ref)))
print(f"interior seeds: max |mutant gap - reference gap| = {worst:.3e}; relative to max(1,|gap|) = {worst_rel:.3e}")

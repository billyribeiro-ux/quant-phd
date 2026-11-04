import importlib.util, math, sys, pathlib
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD7-M4-d")
REF = ROOT / "course/modules/M/M4/grader/reference.py"
MUT = ROOT / "ledgers/M4/mutants"
import math
def sample_variance(xs):
    mean = math.fsum(xs) / len(xs)
    return math.fsum((x - mean) ** 2 for x in xs) / (len(xs) - 1)
def cross_measured(sol, seed):
    w1, w2 = 1_000_000, 1_000_000
    cov = [[4e-4, 4.8e-4], [4.8e-4, 9e-4]]
    target = 4.0 * w1 * w2 * cov[0][1]
    plus = sol.simulate_losses([w1, w2], cov, 100_000, seed, "student_t", 5)
    minus = sol.simulate_losses([w1, -w2], cov, 100_000, seed, "student_t", 5)
    measured = sample_variance(plus) - sample_variance(minus)
    return abs(measured / target - 1.0)
ref = load(REF, "ref")
errs = [cross_measured(ref, s) for s in range(50)]
print("reference max rel err seeds 0-49:", round(max(errs), 4), "argmax", errs.index(max(errs)))
print("reference rel err seeds 0-9:", [round(e, 4) for e in errs[:10]])

m83 = load(MUT / "r8_03_student_t_matched_scale_on_first_asset_only.py", "m83")
m92 = load(MUT / "r9_02_student_t_second_asset_own_chi_square.py", "m92")
e83 = [cross_measured(m83, s) for s in range(10)]
e92 = [cross_measured(m92, s) for s in range(10)]
print("r8_03 rel err seeds 0-9 (min, max):", round(min(e83),3), round(max(e83),3))
print("r9_02 rel err seeds 0-9 (min, max):", round(min(e92),3), round(max(e92),3))

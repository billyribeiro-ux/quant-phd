import importlib.util, math
from pathlib import Path
M = Path("/Users/billyribeiro/.fanout/wt/verifyD12-M4-d/ledgers/M4/mutants")
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
def var(xs):
    m = math.fsum(xs) / len(xs); return math.fsum((x - m) ** 2 for x in xs) / (len(xs) - 1)
mods = {
    "r8_03": load(next(M.glob("r8_03*.py")), "r8_03"),
    "r9_02": load(next(M.glob("r9_02*.py")), "r9_02"),
}
for k, mod in mods.items():
    errs = []
    for seed in range(10):
        w1 = w2 = 1_000_000
        cov = [[4e-4, 4.8e-4], [4.8e-4, 9e-4]]
        target = 4.0 * w1 * w2 * cov[0][1]
        plus = mod.simulate_losses([w1, w2], cov, 100_000, seed, "student_t", 5)
        minus = mod.simulate_losses([w1, -w2], cov, 100_000, seed, "student_t", 5)
        errs.append((var(plus) - var(minus)) / target - 1)
    print(k, "signed errors seeds 0-9:", [round(e, 4) for e in errs], "abs min", round(min(abs(e) for e in errs), 4), "abs max", round(max(abs(e) for e in errs), 4))

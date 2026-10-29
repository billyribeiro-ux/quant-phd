"""Re-derive the cross-term error figures in test_project.py lines 43-48 (reference over seeds 0-49; mutants over seeds 0-9)."""
import sys, math, importlib.util
sys.path.insert(0, "/tmp/M4-d-r10-scratch/ref")
path, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
spec = importlib.util.spec_from_file_location("m", path)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
def fsum_var(xs):
    m = math.fsum(xs) / len(xs)
    return math.fsum((x - m) ** 2 for x in xs) / (len(xs) - 1)
w1, w2 = 1_000_000, 1_000_000
cov = [[4e-4, 4.8e-4], [4.8e-4, 9e-4]]
target = 4.0 * w1 * w2 * cov[0][1]
worst = 0.0
for seed in range(lo, hi):
    plus = mod.simulate_losses([w1, w2], cov, 100_000, seed, "student_t", 5)
    minus = mod.simulate_losses([w1, -w2], cov, 100_000, seed, "student_t", 5)
    measured = fsum_var(plus) - fsum_var(minus)
    e = abs(measured / target - 1.0)
    worst = max(worst, e)
    print(seed, f"{e:.5f}", flush=True)
print("WORST", f"{worst:.5f}", path)

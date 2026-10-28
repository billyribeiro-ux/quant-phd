import sys, math
sys.path.insert(0, sys.argv[1] + "/course/modules/M/M4/grader")
import importlib.util, instance
s = importlib.util.spec_from_file_location("ref", sys.argv[1] + "/course/modules/M/M4/grader/reference.py")
ref = importlib.util.module_from_spec(s); s.loader.exec_module(ref)
def sv(xs):
    m = math.fsum(xs) / len(xs); return math.fsum((x - m) ** 2 for x in xs) / (len(xs) - 1)
worst = 0.0; ws = None
for seed in range(2000):
    inst = instance.make_instance(seed); pos, cov, nd = inst["positions_cents"], inst["cov"], inst["n_draws"]
    t = math.fsum(pos[i]*pos[j]*cov[i][j] for i in range(len(pos)) for j in range(len(pos)))
    e = abs(sv(ref.simulate_losses(pos, cov, nd, seed, "gaussian", None)) / t - 1.0)
    if e > worst: worst, ws = e, seed
print("gaussian reference max relative error seeds 0-1999:", round(worst, 6), "at seed", ws)

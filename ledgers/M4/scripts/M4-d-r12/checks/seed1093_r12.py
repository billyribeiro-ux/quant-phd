import importlib.util, math, sys
from pathlib import Path
G = Path("/Users/billyribeiro/.fanout/wt/verifyD12-M4-d/course/modules/M/M4/grader")
sys.path.insert(0, str(G))
import instance
spec = importlib.util.spec_from_file_location("ref", G / "reference.py")
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
def var(xs):
    m = math.fsum(xs) / len(xs); return math.fsum((x - m) ** 2 for x in xs) / (len(xs) - 1)
inst = instance.make_instance(1093)
p, c = inst["positions_cents"], inst["cov"]
n = len(p)
target = math.fsum(p[i]*p[j]*c[i][j] for i in range(n) for j in range(n))
print("seed 1093 nu", inst["nu"], "n_draws", inst["n_draws"], "positions", p, "target", target)
t = ref.simulate_losses(p, c, inst["n_draws"], 1093, "student_t", inst["nu"])
print("reference student_t rel error at seed 1093:", var(t)/target - 1)
print("max abs loss", max(abs(x) for x in t))

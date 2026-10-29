import sys, importlib.util
from fractions import Fraction as F
spec = importlib.util.spec_from_file_location("l6", "tests/labs/M7/lab-M7-L06-1.py")
m6 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m6)
sigma, mu, _ = m6.simulate_inputs()[0], None, None
res = m6.simulate_inputs()
sigma, mu = res[2], res[1]
print("sigma", [[str(x) for x in r] for r in sigma]); print("mu", [str(x) for x in mu])
g = F(16)
w_eq, _ = m6.equality_frontier_point(sigma, mu, g, list(range(4)))
best = None
for item in m6.nonnegative_candidates(sigma, mu, g):
    obj = m6.objective(sigma, mu, g, item[1])
    if best is None or obj < best[0]: best = (obj, item[1])
o_eq = m6.objective(sigma, mu, g, w_eq)
print("gamma16 eq obj", float(o_eq), "nn obj", float(best[0]), "diff exact", float(best[0]-o_eq), "diff frac", best[0]-o_eq)
g4 = F(4)
kept = m6.nonnegative_candidates(sigma, mu, g4)
bw = min(kept, key=lambda it: m6.objective(sigma, mu, g4, it[1]))[1]
w0 = [F(1,4)]*4
tu = sum(abs(bw[i]-w0[i]) for i in range(4))
print("gamma4 weights exact", [str(x) for x in bw], "turnover exact", tu, float(tu))
six = [round(float(x),6) for x in bw]
print("six-place weights", six, "turnover from six-place", round(sum(abs(six[i]-0.25) for i in range(4)),6), sum(abs(six[i]-0.25) for i in range(4)))

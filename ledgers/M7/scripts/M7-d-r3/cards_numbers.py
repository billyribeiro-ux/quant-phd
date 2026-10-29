"""Recompute card numbers: M7 L06 Part D turnover and Part B/A objective gap (exact), L04 grid gap for lambda=0, L05 Part A objective."""
import importlib.util
import sys
from fractions import Fraction as F
from itertools import product

spec = importlib.util.spec_from_file_location("l06", "/tmp/verifyB3-M7-d/tests/labs/M7/lab-M7-L06-1.py")
l06 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(l06)
_m, mu, sigma = l06.simulate_inputs()
print("mu", [str(x) for x in mu], "diag", [str(sigma[i][i]) for i in range(4)])
print("sigma", [[str(x) for x in row] for row in sigma])
g = l06.GAMMAS
w0 = [F(1, 4)] * 4
_, w4 = min(l06.nonnegative_candidates(sigma, mu, g[2]), key=lambda it: l06.objective(sigma, mu, g[2], it[1]))
turn = sum((abs(w4[i] - w0[i]) for i in range(4)), F(0))
print("gamma4 weights", [str(x) for x in w4], "turnover exact", str(turn), float(turn))
# gamma 16 objective gap
eq16, _ = l06.equality_frontier_point(sigma, mu, g[4], list(range(4)))
nn16 = min(l06.nonnegative_candidates(sigma, mu, g[4]), key=lambda it: l06.objective(sigma, mu, g[4], it[1]))[1]
oe = l06.objective(sigma, mu, g[4], eq16)
on = l06.objective(sigma, mu, g[4], nn16)
print("gamma16 obj equality", float(oe), "nonneg", float(on), "gap exact", str(on - oe), float(on - oe))

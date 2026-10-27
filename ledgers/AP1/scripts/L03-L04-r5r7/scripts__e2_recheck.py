# Independent recheck of Problem E2 numbers (scratch; re-implements the market and the two LPs).
import numpy as np
from scipy.optimize import linprog
rng = np.random.default_rng(303)
X = 1.0 + 0.3 * rng.standard_normal((12, 6))
psi = rng.uniform(0.02, 0.14, 12)
fair = X.T @ psi
others = [0, 1, 2, 4, 5]
# Lowest arbitrage-free price of asset 4: min X[:,3].theta s.t. X[:,others].T theta = fair[others], theta >= 0
lo = linprog(X[:, 3], A_eq=X[:, others].T, b_eq=fair[others], bounds=[(0, None)] * 12, method="highs")
gap = fair[3] - lo.fun
print("gap %.9f" % gap)
def margin(p):
    # max t s.t. X.T phi = p, phi_s >= t for all states  -> phi_s - t >= 0 ; t <= 1
    c = np.zeros(13); c[-1] = -1
    A_ub = np.hstack([-np.eye(12), np.ones((12, 1))])
    A_eq = np.hstack([X.T, np.zeros((6, 1))])
    r = linprog(c, A_ub=A_ub, b_ub=np.zeros(12), A_eq=A_eq, b_eq=p, bounds=[(None, None)] * 12 + [(None, 1)], method="highs")
    return -r.fun
for s in (0.2078, gap - 1e-9, gap - 1e-12, gap):
    p = fair.copy(); p[3] -= s
    print("shade %.12f margin %+.4e" % (s, margin(p)))
print("margin/distance at 1e-9: %.4f ; at 1e-12: %.4f ; at 0.2078: %.4f" % (margin(np.r_[fair[:3], fair[3]-(gap-1e-9), fair[4:]])/1e-9, margin(np.r_[fair[:3], fair[3]-(gap-1e-12), fair[4:]])/1e-12, margin(np.r_[fair[:3], fair[3]-0.2078, fair[4:]])/(gap-0.2078)))

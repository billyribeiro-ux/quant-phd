import sys, math
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyB6-M5-d/course/modules/M/M5/grader")
from instance import make_instance

def sweep(beta, alpha, grid, values):
    out = []
    for k in grid:
        avail = k**alpha
        out.append(max(math.sqrt(avail - kp) + beta*c for kp, c in zip(grid, values) if kp <= avail))
    return out

interior = []
total = 0
argmax_last_all_sweeps = 0
for seed in range(0, 200):
    for which in (seed, seed + 7919):
        inst = make_instance(which)
        beta, alpha, grid, tol = inst["beta"], inst["alpha"], inst["grid"], inst["tol"]
        vals = [0.0]*len(grid)
        ok = True
        for n in range(1, 400):
            new = sweep(beta, alpha, grid, vals)
            diffs = [abs(a-b) for a, b in zip(new, vals)]
            m = max(diffs)
            idx = [i for i, d in enumerate(diffs) if d == m]
            if len(grid) - 1 not in idx:
                interior.append((which, n, idx, len(grid)))
            vals = new
            if beta/(1-beta)*m <= tol:
                break
        total += 1
print("instances", total, "cases where sup change not at last point (seed, sweep, argmax idx, m):", len(interior))
print(interior[:10])

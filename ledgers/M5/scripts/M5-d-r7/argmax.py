import sys, math
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyB7-M5-d/course/modules/M/M5/grader")
import instance as I
seed = int(sys.argv[1])
inst = I.make_instance(seed)
beta, alpha, grid = inst["beta"], inst["alpha"], inst["grid"]
def sweep(values):
    out = []
    for k in grid:
        r = k**alpha
        out.append(max(math.sqrt(r - kp) + beta*v for kp, v in zip(grid, values) if kp <= r))
    return out
vals = [0.0]*len(grid)
for n in range(1, 4):
    new = sweep(vals)
    d = [abs(a-b) for a, b in zip(new, vals)]
    m = max(d); j = d.index(m)
    print(f"seed {seed} sweep {n}: sup change {m:.6g} at index {j} of {len(grid)-1}; last change {d[-1]:.6g}")
    vals = new

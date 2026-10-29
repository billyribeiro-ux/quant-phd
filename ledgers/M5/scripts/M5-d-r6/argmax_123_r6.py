import sys, math
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyB6-M5-d/course/modules/M/M5/grader")
from instance import make_instance
def sweep(beta, alpha, grid, values):
    out = []
    for k in grid:
        avail = k**alpha
        out.append(max(math.sqrt(avail - kp) + beta*c for kp, c in zip(grid, values) if kp <= avail))
    return out
bad = []; n_inst = 0; first_interior = {}
for seed in range(0, 200):
    for which in (seed, seed + 7919):
        inst = make_instance(which); n_inst += 1
        beta, alpha, grid = inst["beta"], inst["alpha"], inst["grid"]
        vals = [0.0]*len(grid)
        for n in range(1, 400):
            new = sweep(beta, alpha, grid, vals)
            diffs = [abs(a-b) for a, b in zip(new, vals)]
            m = max(diffs)
            if len(grid)-1 not in [i for i, d in enumerate(diffs) if d == m]:
                first_interior.setdefault(which, n)
            vals = new
print("instances", n_inst)
print("instances whose first interior-argmax sweep index:", len(first_interior), "min over instances", min(first_interior.values()) if first_interior else None)
print("sample", list(first_interior.items())[:8])
# SEED 0 instances, per sweep argmax for sweeps 1..3
for which in (0, 7919):
    inst = make_instance(which); beta, alpha, grid = inst["beta"], inst["alpha"], inst["grid"]
    vals=[0.0]*len(grid)
    for n in range(1,4):
        new = sweep(beta, alpha, grid, vals); diffs=[abs(a-b) for a,b in zip(new,vals)]
        print("which",which,"sweep",n,"argmax",[i for i,d in enumerate(diffs) if d==max(diffs)],"len",len(grid))
        vals=new

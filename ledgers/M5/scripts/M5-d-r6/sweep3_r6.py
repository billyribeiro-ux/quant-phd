import sys, math
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyB6-M5-d/course/modules/M/M5/grader")
from instance import make_instance
def sweep(beta, alpha, grid, values):
    out = []
    for k in grid:
        avail = k**alpha
        out.append(max(math.sqrt(avail - kp) + beta*c for kp, c in zip(grid, values) if kp <= avail))
    return out
inst = make_instance(7919); beta, alpha, grid = inst["beta"], inst["alpha"], inst["grid"]
vals=[0.0]*len(grid)
for n in range(1,4):
    new = sweep(beta, alpha, grid, vals); diffs=[abs(a-b) for a,b in zip(new,vals)]
    m = max(diffs)
    print("sweep", n, "max %.17g" % m, "last %.17g" % diffs[-1], "gap %.3e" % (m-diffs[-1]), "argmax", [i for i,d in enumerate(diffs) if d==m])
    vals=new

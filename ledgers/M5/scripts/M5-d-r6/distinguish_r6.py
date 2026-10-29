import math
def sweep(beta, alpha, grid, values):
    out = []
    for k in grid:
        avail = k**alpha
        out.append(max(math.sqrt(avail - kp) + beta*c for kp, c in zip(grid, values) if kp <= avail))
    return out
cases = {"SMALL_GRID b.9 a.5": (0.9, 0.5, [0.5, 0.9, 1.4]), "lab1 b.9 a.3 10pt": (0.9, 0.3, [0.45+0.25*j for j in range(10)])}
for name, (beta, alpha, grid) in cases.items():
    vals = [0.0]*len(grid)
    for n in range(1, 8):
        new = sweep(beta, alpha, grid, vals); diffs=[abs(a-b) for a,b in zip(new,vals)]; m=max(diffs)
        print(name, "sweep", n, "argmax", [i for i,d in enumerate(diffs) if d==m], "sup %.17g last %.17g gap %.3e" % (m, diffs[-1], m-diffs[-1]))
        vals=new

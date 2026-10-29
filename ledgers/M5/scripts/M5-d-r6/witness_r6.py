import math, itertools
def sweep(beta, alpha, grid, values):
    out = []
    for k in grid:
        avail = k**alpha
        out.append(max(math.sqrt(avail - kp) + beta*c for kp, c in zip(grid, values) if kp <= avail))
    return out
# small structured search: 2-3 point grids with nice values
best = None
for beta in (0.5, 0.9):
  for alpha in (0.5, 0.99, 0.3):
    for g in itertools.combinations([0.1, 0.2, 0.25, 0.4, 0.5, 0.6, 0.75, 0.9, 1.0, 1.2, 1.5, 2.0], 2):
        grid = list(g)
        if grid[0] > 1: continue
        vals=[0.0,0.0]
        for n in range(1, 40):
            new = sweep(beta, alpha, grid, vals)
            d=[abs(a-b) for a,b in zip(new, vals)]
            if d[0] > 0 and d[1] < d[0]*0.5 and (best is None or d[0]-d[1] > best[0]):
                best=(d[0]-d[1], beta, alpha, grid, n, d, new)
            vals=new
print(best)

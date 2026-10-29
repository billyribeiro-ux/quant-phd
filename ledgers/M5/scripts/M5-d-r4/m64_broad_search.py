import math, random, sys
def sweep(beta, alpha, grid, values):
    out = []
    for k in grid:
        av = k**alpha
        out.append(max(math.sqrt(av - s) + beta * c for s, c in zip(grid, values) if s <= av))
    return out
rng = random.Random(int(sys.argv[1]))
bad = 0; trials = 0; worst_gap = 0.0
for _ in range(int(sys.argv[2])):
    beta = rng.uniform(0.5, 0.99); alpha = rng.uniform(0.05, 0.95)
    m = rng.randint(2, 30)
    lo = rng.uniform(0.01, 1.0)
    grid = sorted(set(lo * (1 + rng.random()*3) for _ in range(m)))
    grid = [g for g in grid]
    grid.sort()
    if grid[0] > 1 or len(grid) < 2:
        grid = [min(lo,1.0)] + [x for x in grid if x > min(lo,1.0)]
        if len(grid) < 2: continue
    trials += 1
    v = [0.0]*len(grid)
    for n in range(1, 400):
        new = sweep(beta, alpha, grid, v)
        d = [abs(a-b) for a, b in zip(new, v)]
        sup = max(d)
        if sup == 0: break
        if d[-1] < sup - max(1e-6*sup, 1e-12):
            bad += 1
            if bad <= 3: print("witness beta %.4f alpha %.4f n %d grid %s d %s" % (beta, alpha, n, [round(g,3) for g in grid], [f"{x:.3e}" for x in d]))
            break
        v = new
print("trials", trials, "sweeps where last-point change is not the sup change:", bad)

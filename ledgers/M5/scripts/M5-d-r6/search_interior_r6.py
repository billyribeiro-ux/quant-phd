import math, random
def sweep(beta, alpha, grid, values):
    out = []
    for k in grid:
        avail = k**alpha
        out.append(max(math.sqrt(avail - kp) + beta*c for kp, c in zip(grid, values) if kp <= avail))
    return out
rng = random.Random(1)
best = (0.0, None)
for trial in range(20000):
    beta = rng.choice([0.3, 0.5, 0.8, 0.9, 0.99]); alpha = rng.uniform(0.02, 0.98)
    m = rng.randint(2, 12)
    first = rng.uniform(0.001, 1.0)
    grid = [first]
    for _ in range(m-1): grid.append(grid[-1] + rng.uniform(0.001, 3.0))
    vals = [0.0]*m
    for n in range(1, 60):
        new = sweep(beta, alpha, grid, vals); d = [abs(a-b) for a,b in zip(new, vals)]
        mx = max(d); gap = mx - d[-1]
        if gap > best[0]:
            best = (gap, (beta, round(alpha,4), [round(g,4) for g in grid], n, [round(x,6) for x in d]))
        vals = new
print("largest sup-minus-last gap found:", best[0]); print(best[1])

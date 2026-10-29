import random, math
rng = random.Random(7)
def sweep(beta, alpha, grid, values):
    out = []
    for k in grid:
        r = k**alpha
        out.append(max(math.sqrt(r - kp) + beta*v for kp, v in zip(grid, values) if kp <= r))
    return out
worst = 0.0; cases = 0; strict = 0
for trial in range(3000):
    beta = rng.uniform(0.05, 0.99); alpha = rng.uniform(0.05, 0.95)
    m = rng.randint(2, 25)
    first = rng.uniform(0.001, 1.0)
    grid = sorted({first + rng.uniform(0, 5) for _ in range(m)})
    grid = [first] + [g for g in grid if g > first]
    vals = [0.0]*len(grid)
    for n in range(1, 40):
        new = sweep(beta, alpha, grid, vals)
        d = [abs(a-b) for a, b in zip(new, vals)]
        gap = max(d) - d[-1]
        worst = max(worst, gap); cases += 1
        if gap > 1e-9: strict += 1
        vals = new
print(f"sweeps checked {cases}, worst (sup - last) = {worst:.3e}, sweeps with gap > 1e-9: {strict}")

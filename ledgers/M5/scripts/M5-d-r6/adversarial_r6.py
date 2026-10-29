import math, random
def sweep(beta, alpha, grid, values):
    out = []
    for k in grid:
        avail = k**alpha
        out.append(max(math.sqrt(avail - kp) + beta*c for kp, c in zip(grid, values) if kp <= avail))
    return out
rng = random.Random(4242)
worst_gap = 0.0; mono_viol = 0; cases = 0; worst_case = None
for t in range(6000):
    beta = rng.choice([0.01, 0.3, 0.5, 0.8, 0.9, 0.95, 0.99, 0.999])
    alpha = rng.choice([0.01, 0.05, 0.3, 0.5, 0.7, 0.95, 0.99])
    m = rng.randint(2, 30)
    grid = []
    x = rng.choice([1e-6, 0.01, 0.2, 0.9, 1.0])
    for i in range(m):
        grid.append(x); x = x + rng.choice([1e-6, 1e-3, 0.05, 0.5, 2.0, 10.0]) * rng.random() + 1e-9
    vals = [0.0]*m
    for n in range(1, 60):
        new = sweep(beta, alpha, grid, vals)
        d = [a-b for a, b in zip(new, vals)]
        ad = [abs(v) for v in d]; mx = max(ad)
        gap = (mx - ad[-1]) if mx > 1e-6 else 0.0
        cases += 1
        if gap > worst_gap:
            worst_gap = gap; worst_case = (beta, alpha, m, n, grid, [round(v,12) for v in ad], [round(v,12) for v in new])
        if any(d[i] > d[i+1] + 1e-8 for i in range(m-1)):
            mono_viol += 1
        vals = new
        if mx == 0: break
print("WORST", worst_case)
print("cases", cases, "worst absolute (sup-last) for sup>1e-6", worst_gap, "at", worst_case)
print("sweeps where d_n not nondecreasing in k (tolerance 1e-8 absolute):", mono_viol)

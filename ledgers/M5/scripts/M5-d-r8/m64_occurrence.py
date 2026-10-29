import random, importlib.util
spec = importlib.util.spec_from_file_location("ref", "/Users/billyribeiro/.fanout/wt/verifyB8-M5-d/course/modules/M/M5/grader/reference.py")
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
rng = random.Random(11)
cnt_grids = 0; cnt_lt = 0; examples = []
for trial in range(4000):
    m = rng.randint(2, 6)
    base = sorted(set(round(rng.uniform(0.02, 1.0), 3) for _ in range(m)))
    if len(base) < 2: continue
    pts = base
    beta = rng.choice([0.3, 0.5, 0.8, 0.9, 0.95]); alpha = rng.choice([0.1, 0.3, 0.5, 0.7, 0.9])
    vals = [0.0]*len(pts)
    grid_hit = False
    for sweep in range(1, 400):
        new = ref._sweep(beta, alpha, pts, vals)
        d = [abs(a-b) for a,b in zip(new, vals)]
        ch_all = max(d); ch_last = d[-1]
        if ch_all > 1e-9 and ch_last < ch_all*0.999999 and not grid_hit:
            grid_hit = True
            if len(examples) < 5: examples.append((pts, beta, alpha, sweep, ch_all, ch_last))
        vals = new
        if ch_all < 1e-13: break
    cnt_grids += 1
    cnt_lt += grid_hit
print("grids", cnt_grids, "grids where last change < max change at some sweep", cnt_lt)
for e in examples: print(e)

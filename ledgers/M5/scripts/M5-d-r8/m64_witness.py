import sys, random, math, importlib.util
spec = importlib.util.spec_from_file_location("ref", "/Users/billyribeiro/.fanout/wt/verifyB8-M5-d/course/modules/M/M5/grader/reference.py")
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
rng = random.Random(7)
found = 0
for trial in range(3000):
    m = rng.randint(2, 5)
    pts = sorted(rng.sample([round(rng.uniform(0.05, 3.0), 3) for _ in range(12)], m))
    if pts[0] > 1: continue
    if len(set(pts)) != m: continue
    beta = rng.choice([0.5, 0.8, 0.9, 0.95]); alpha = rng.choice([0.2, 0.5, 0.8])
    vals = [0.0]*m
    for sweep in range(1, 2000):
        new = ref._sweep(beta, alpha, pts, vals)
        ch_all = max(abs(a-b) for a,b in zip(new, vals))
        ch_last = abs(new[-1]-vals[-1])
        if ch_last < ch_all * 0.5:
            # stopping decision difference at tol 1e-6
            fac = beta/(1-beta)
            if (fac*ch_last <= 1e-6) != (fac*ch_all <= 1e-6) or (fac*ch_last <= 1e-3) != (fac*ch_all <= 1e-3):
                print("WITNESS grid", pts, "beta", beta, "alpha", alpha, "sweep", sweep, "ch_all", ch_all, "ch_last", ch_last)
                found += 1
            break
        vals = new
        if fac*ch_all < 1e-12 if False else False: break
    if found >= 3: break
print("found", found)

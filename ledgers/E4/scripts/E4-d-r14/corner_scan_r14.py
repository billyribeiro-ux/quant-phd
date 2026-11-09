"""Round-14 independent re-run of the corner accuracy scan in ledgers/E4/equivalent/README.md (cap 200 and cap 240)."""
import importlib.util, math, sys
REF = "/Users/billyribeiro/.fanout/wt/verifyE14-E4-d/course/modules/E/E4/grader/reference.py"
spec = importlib.util.spec_from_file_location("ref", REF)
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
def closed(sd, c):
    t = 2.0 * math.exp(-4.0 * c) - 1.0
    return 2.0 * sd * math.sqrt(t / (1.0 - t))
c_edge = -math.log(1.01 / 2.0) / 4.0
for cap in (200, 240):
    ref.MAX_BISECTION_STEPS = cap
    n = 0; over = 0; worst = (0.0, None); smin = (9, None); smax = (0, None)
    for i in range(300):
        sd = 1e-50 * (1 + 0.002 * i)
        for j in range(300):
            c = c_edge - 0.0005 + 0.0005 * j / 299
            t = 2 * math.exp(-4 * c) - 1
            if t < 1e-2: continue
            ex = closed(sd, c)
            if ex >= 1.0 or ex <= 0: continue
            n += 1
            out = ref.solve_model(sd, c)["informed_fraction"]
            rel = abs(out - ex) / ex
            if rel > 1e-10: over += 1
            if rel > worst[0]: worst = (rel, (sd, c, t, ex, out))
    print(f"cap {cap}: cases {n} over-1e-10 {over} max-rel {worst[0]:.4e} at sd={worst[1][0]:.6e} cost={worst[1][1]!r} root={worst[1][3]:.6e}", flush=True)

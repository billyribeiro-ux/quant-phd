"""Round-14 accuracy sweep: random interior instances with sd in [1e-50, ~4.9] (log-uniform) and taubar in [1e-2, tau_y(1)),
comparing the reference root with the closed form of Proposition 4 (relative error must be <= 1e-10)."""
import importlib.util, math, random
REF = "/Users/billyribeiro/.fanout/wt/verifyE14-E4-d/course/modules/E/E4/grader/reference.py"
spec = importlib.util.spec_from_file_location("ref", REF); ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
rng = random.Random(20260211)
def closed(sd, c):
    t = 2.0 * math.exp(-4.0 * c) - 1.0
    return 2.0 * sd * math.sqrt(t / (1.0 - t))
n = 0; over = []; worst = (0.0, None)
for k in range(20000):
    sd = 10 ** rng.uniform(-50, math.log10(4.9))
    ty1 = 1.0 / (1.0 + 4.0 * sd * sd)
    tb_hi = min(ty1, 0.9999999)
    if tb_hi <= 0.01: continue
    tb = rng.uniform(0.01, tb_hi)
    c = -math.log((tb + 1.0) / 2.0) / 4.0
    ex = closed(sd, c)
    if not (0.0 < ex < 1.0): continue
    out = ref.solve_model(sd, c)["informed_fraction"]
    rel = abs(out - ex) / ex
    n += 1
    if rel > worst[0]: worst = (rel, (sd, c, tb, ex, out))
    if rel > 1e-10: over.append((sd, c, tb, rel))
print("interior cases", n, "over 1e-10:", len(over), "max rel", f"{worst[0]:.3e}", "at", worst[1])
print("first overs", over[:5])
